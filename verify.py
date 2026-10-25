# -*- coding: utf-8 -*-
"""Exact polynomial certificates for the trefoil and harmonic figure-eight.

Install: python -m pip install -r requirements.txt
Run: python -u verify.py
No external coefficient files are required.

The checks establish polynomiality and inverse identities through exact
polynomial certificates, cancellation, and explicitly invertible outer maps.
They do not expand all six final composition components in a single step.
See MECHANISM.md for the algebraic justification, including the fibre x = 0.
"""
from time import perf_counter
import os
# Use SymPy's pure Python arithmetic even if FLINT is installed.
# Set this before importing SymPy: run this file in a fresh Python process.
os.environ["SYMPY_GROUND_TYPES"] = "python"
from sympy import QQ
from sympy.polys.rings import ring as polynomial_ring

# Work in QQ[a,x,y,z,t]/(a^2-a+1), with exact coefficients.
# x,y,z are the arguments of each map; t is the curve parameter.
ring, a, x, y, z, t = polynomial_ring("a,x,y,z,t", QQ)
relation = a*a-a+1
one = ring(1)
zero = ring(0)


def red(p):
    """Reduce coefficients using the relation a^2 = a - 1."""
    return p % relation


def at(p, xx=x, yy=y, zz=z, tt=t):
    """Perform simultaneous exact polynomial substitution."""
    terms = p.to_dict()
    images = (a, xx, yy, zz, tt)
    powers = []
    for i, image in enumerate(images):
        degree = max((mon[i] for mon in terms), default=0)
        row = [one]
        for _ in range(degree):
            row.append(red(row[-1]*image))
        powers.append(row)
    answer = zero
    for mon, coefficient in terms.items():
        term = ring(coefficient)
        for i, exponent in enumerate(mon):
            term = red(term*powers[i][exponent])
        answer += term
    return red(answer)


def div_x(p, power):
    """Divide by x^power, requiring divisibility of every monomial."""
    result = {}
    for mon, coefficient in red(p).to_dict().items():
        if mon[1] < power:
            raise ArithmeticError("The numerator is not divisible by the required power of x")
        new_mon = list(mon)
        new_mon[1] -= power
        result[tuple(new_mon)] = coefficient
    return ring.from_dict(result)


def check(label, *differences):
    # Explicit exceptions keep all checks active even under python -O.
    for difference in differences:
        if red(difference) != 0:
            raise AssertionError(label)
    print("PASS:", label)


def derivative(p, index):
    """Formal derivative; variable indices: x=1, y=2, z=3."""
    result = {}
    for mon, coefficient in p.to_dict().items():
        if mon[index]:
            new_mon = list(mon)
            new_mon[index] -= 1
            result[tuple(new_mon)] = coefficient*mon[index]
    return ring.from_dict(result)


def degrees(polynomials, expected):
    actual = tuple(max(sum(mon[1:4]) for mon in p.to_dict())
                   for p in polynomials)
    if actual != expected:
        raise AssertionError((actual, expected))
    print("PASS: component degrees", actual)


started = perf_counter()

# Common base coordinate pair H,W. In f, y denotes the second argument.
H = red(a*x**3*y**2+2*x**2*y*z+(1-a)*x*z**2
        +((a-1)*x**3-a*x)*y+(-1+a*x**2-a*x**4)*z
        -2*x**5+(6-2*a)*x**3-2*(1-a)*x)
f = red(-y+x*((1-a)*y**2+2*a-2)+x**2*(2*a*y**3-5*a*y)
        +x**3*(-5*y**4+15*y**2-2*a)
        +x**4*(14*(1-a)*y**5+50*(a-1)*y**3+(29-24*a)*y))
W = div_x(a*(a*x*y+z-at(f, yy=H)), 5)

# R,S are the second and third components of the inverse of (x,H,W).
chi = div_x(a*(y-at(H, yy=zero, zz=f)), 5)
R = red(-chi+(-1+a*x**2-a*x**4+2*(1-a)*x*f)*z
        +(1-a)**2*x**6*z**2)
S = red(f+(1-a)*x**5*z-a*x*R)

check("base polynomial identity for W",
      x**5*W-a*(a*x*y+z-at(f, yy=H)))
check("base inverse: first nontrivial component",
      at(H, yy=R, zz=S)-y)
check("base inverse: certificate for the other component",
      a*x*R+S-f-(1-a)*x**5*z)
# The preceding three checks and a(1-a)=1 give x^5*(W(x,R,S)-z)=0.
# The polynomial ring is a domain: cancelling x^5 proves W(x,R,S)=z.
check("inverse after forward: both nontrivial components expanded",
      at(R, yy=H, zz=W)-y, at(S, yy=H, zz=W)-z)

# TREFOIL. Return to the original coordinates via y -> y+2, z -> z-5x.
h_t = at(H, yy=y+2, zz=z-5*x)
w_t = at(W, yy=y+2, zz=z-5*x)
phi_t = (h_t, red(x-h_t**3+3*h_t), red(w_t-8+14*h_t**2))


def trefoil_forward(X, Y, Z):
    return tuple(at(p, xx=X, yy=Y, zz=Z) for p in phi_t)


def trefoil_inverse(X, Y, Z):
    # X,Y,Z are function arguments, not additional unknown coefficients.
    return (red(X**3-3*X+Y),
            red(at(R, xx=X**3-3*X+Y, yy=X, zz=Z+8-14*X**2)-2),
            red(at(S, xx=X**3-3*X+Y, yy=X, zz=Z+8-14*X**2)
                +5*(X**3-3*X+Y)))


# Bind the public inverse callable to its proved polynomial factors.
check("the trefoil inverse callable matches the proved factorization",
      *(p-target for p, target in zip(
          trefoil_inverse(y, x-y**3+3*y, z-8+14*y**2),
          (x, R-2, S+5*x))))

# Check the outer coordinate changes and their inverses.
check("the original trefoil normalization is invertible",
      (y+2)-2-y, (z-5*x)+5*x-z)
check("the trefoil outer map is invertible in both directions",
      y**3-3*y+(x-y**3+3*y)-x,
      (z-8+14*y**2)+8-14*y**2-z,
      (x**3-3*x+y)-x**3+3*x-y,
      (z+8-14*x**2)-8+14*x**2-z)
check("the trefoil maps to (t,0,0)",
      *(p-target for p, target in zip(
          trefoil_forward(t**3-3*t, t**4-4*t**2, t**5-10*t), (t, zero, zero))))
check("the inverse recovers the trefoil from the axis",
      *(p-target for p, target in zip(trefoil_inverse(t, zero, zero),
          (t**3-3*t, t**4-4*t**2, t**5-10*t))))
degrees(phi_t, (5, 15, 24))
check("the base relative Jacobian determinant is -1",
      derivative(H, 2)*derivative(W, 3)-derivative(H, 3)*derivative(W, 2)+1)
# Swapping the output coordinates x and H changes the sign: the rectifier has determinant +1.

# HARMONIC FIGURE-EIGHT: the second component has the linear term +5t.
correction = red(42*(a-1)*y**6+175*(1-a)*y**4+(147*a-161)*y**2+8)
h_h = at(H, yy=x*z-y**2+2, zz=y)
w_b = at(W, yy=x*z-y**2+2, zz=y)
q_h = div_x(w_b-at(correction, yy=h_h), 1)

# Inverse of the relative map (x,h_h,q_h).
lift_y = at(R, zz=x*z+correction)
inverse_y = at(S, zz=x*z+correction)
inverse_z = div_x(lift_y+inverse_y**2-2, 1)
check("polynomiality of the forward figure-eight transfer",
      x*q_h-w_b+at(correction, yy=h_h))
check("polynomiality of the inverse figure-eight transfer",
      x*inverse_z-inverse_y**2+2-lift_y)
# After inverting x, these formulas compose explicitly invertible maps:
# (x,y,z) -> (x,xz-y^2+2,y), then (x,H,W), then
# (x,y,z) -> (x,y,(z-correction(x,y))/x).
# Their inverses, applied in reverse order: (x,y,z) -> (x,y,xz+correction(x,y)), then (x,R,S),
# then (x,y,z) -> (x,z,(y+z^2-2)/x).
# div_x has already established polynomiality of the resulting maps. Thus both
# compositions are identities even at x=0: localization of this domain is injective.

phi_h = (h_h, red(x-h_h**3+3*h_h),
         red(q_h-(1-a)*(42*h_h**3-49*h_h)))


def harmonic_forward(X, Y, Z):
    return tuple(at(p, xx=X, yy=Y, zz=Z) for p in phi_h)


def harmonic_inverse(X, Y, Z):
    return (red(X**3-3*X+Y),
            at(inverse_y, xx=X**3-3*X+Y, yy=X,
               zz=Z+(1-a)*(42*X**3-49*X)),
            at(inverse_z, xx=X**3-3*X+Y, yy=X,
               zz=Z+(1-a)*(42*X**3-49*X)))


# The outer shear cancels before substitution, avoiding large compositions.
check("the figure-eight inverse callable matches the proved factorization",
      *(p-target for p, target in zip(
          harmonic_inverse(y, x-y**3+3*y,
                           z-(1-a)*(42*y**3-49*y)),
          (x, inverse_y, inverse_z))))

check("the figure-eight outer map is invertible in both directions",
      y**3-3*y+(x-y**3+3*y)-x,
      (z-(1-a)*(42*y**3-49*y))+(1-a)*(42*y**3-49*y)-z,
      (x**3-3*x+y)-x**3+3*x-y,
      (z+(1-a)*(42*x**3-49*x))-(1-a)*(42*x**3-49*x)-z)
check("the harmonic figure-eight maps to (t,0,0)",
      *(p-target for p, target in zip(harmonic_forward(
          t**3-3*t, t**5-5*t**3+5*t, t**7-7*t**5+14*t**3-7*t),
          (t, zero, zero))))
check("the inverse recovers the figure-eight from the axis",
      *(p-target for p, target in zip(harmonic_inverse(t, zero, zero),
          (t**3-3*t, t**5-5*t**3+5*t, t**7-7*t**5+14*t**3-7*t))))
degrees(phi_h, (7, 21, 41))
check("the figure-eight relative Jacobian determinant is +1",
      derivative(h_h, 2)*derivative(q_h, 3)
      -derivative(h_h, 3)*derivative(q_h, 2)-1)
# The final figure-eight rectifier has Jacobian determinant -1.
print("BOTH RECTIFICATIONS VERIFIED; elapsed:", round(perf_counter()-started, 2), "s")

# Optionally display the expanded formulas:
# print(trefoil_forward(x, y, z))
# print(trefoil_inverse(x, y, z))
# print(harmonic_forward(x, y, z))
# print(harmonic_inverse(x, y, z))
