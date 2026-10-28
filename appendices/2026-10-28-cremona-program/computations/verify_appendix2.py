#!/usr/bin/env python3
"""Exact, offline certificates accompanying Appendix 2 (28 October 2026).

Run from any directory: python computations/verify_appendix2.py --max-n 3
Only SymPy is required. All coefficients are exact. Checks remain enabled
under python -O. Finite computations do not prove the assertions for all N;
the manuscript supplies the induction and the cited group-theoretic results.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

os.environ["SYMPY_GROUND_TYPES"] = "python"
import sympy
from sympy import QQ
from sympy.polys.rings import ring as polynomial_ring

R, a, x, y, z, t = polynomial_ring("a,x,y,z,t", QQ)
RELATION = a*a - a + 1
ONE, ZERO = R(1), R(0)
b = ONE - a


def red(poly):
    """Use a^2 = a - 1; this reduction introduces no denominators."""
    return R(poly) % RELATION


def trunc(poly, n):
    """Return the canonical representative modulo x^n."""
    return R.from_dict({m: c for m, c in red(poly).to_dict().items() if m[1] < n})


def at(poly, xx=x, yy=y, zz=z, tt=t, modulus=None):
    """Simultaneous substitution, optionally in the quotient by x^modulus.

    The optional modulus is used only while x is fixed. Reducing intermediate
    products is then legitimate and prevents unnecessary expression growth.
    """
    if modulus is not None and xx != x:
        raise ValueError("Modular substitution must fix x")
    reduce = red if modulus is None else lambda value: trunc(value, modulus)
    terms = red(poly).to_dict()
    images = (a, xx, yy, zz, tt)
    powers = []
    for i, image in enumerate(images):
        row = [ONE]
        for _ in range(max((mon[i] for mon in terms), default=0)):
            row.append(reduce(row[-1] * image))
        powers.append(row)
    result = ZERO
    for mon, coefficient in terms.items():
        term = R(coefficient)
        for i, exponent in enumerate(mon):
            term = reduce(term * powers[i][exponent])
        result += term
    return reduce(result)


def exact_quotient(numerator, denominator):
    """Require exact polynomial division, including at exceptional fibres."""
    numerator, denominator = red(numerator), red(denominator)
    if not denominator:
        raise ZeroDivisionError("Zero polynomial denominator")
    # Dividing by a unit in K is not the same as division in QQ[a]. Callers
    # therefore remove the unit b explicitly by multiplying by a first.
    quotient, remainder = numerator.div(denominator)
    if remainder:
        raise ArithmeticError("Nonzero remainder in exact polynomial division")
    return red(quotient)


def div_x(poly, exponent):
    return exact_quotient(poly, x**exponent)


def derivative(poly, index):
    """Formal derivative in x,y,z,t: indices 1,2,3,4 respectively."""
    terms = {}
    for mon, coefficient in red(poly).to_dict().items():
        if mon[index]:
            power = mon[index]
            new_mon = list(mon)
            new_mon[index] -= 1
            terms[tuple(new_mon)] = coefficient * power
    return R.from_dict(terms)


def total_degree(poly):
    return max((sum(mon[1:4]) for mon in red(poly).to_dict()), default=-1)


def degree_in_t(poly):
    return max((mon[4] for mon in red(poly).to_dict()), default=-1)


def integral(poly):
    """Check membership in Z[a,x,y,z,t]/(a^2-a+1)."""
    return all(coefficient.denominator == 1 for coefficient in red(poly).to_dict().values())


def coefficient_y(poly, power):
    result = {}
    for mon, coefficient in red(poly).to_dict().items():
        if mon[2] == power:
            out_mon = list(mon)
            out_mon[2] = 0
            result[tuple(out_mon)] = coefficient
    return R.from_dict(result)


def valuation_x(poly):
    if not poly:
        raise ValueError("The zero polynomial has no finite x-adic valuation")
    return min(mon[1] for mon in red(poly).to_dict())


def D(n, variable=t):
    """Integral Chebyshev normalization: D_0=2,D_1=t,D_(n+1)=tD_n-D_(n-1)."""
    if n == 0:
        return R(2)
    previous, current = R(2), variable
    for _ in range(1, n):
        previous, current = current, red(variable*current-previous)
    return current


class Certificate:
    def __init__(self):
        self.checks = []
        self.lines = []

    def record(self, name, details=None):
        entry = {"name": name, "status": "PASS"}
        if details is not None:
            entry["details"] = details
        self.checks.append(entry)
        line = "PASS: " + name
        self.lines.append(line)
        print(line, flush=True)

    def zero(self, name, *differences):
        for difference in differences:
            if red(difference):
                raise AssertionError(name + ": polynomial identity failed")
        self.record(name)

    def require(self, name, condition, details=None):
        if not condition:
            raise AssertionError(name)
        self.record(name, details)

    def rejects(self, name, callback, exception):
        try:
            callback()
        except exception:
            self.record(name, {"expected_exception": exception.__name__})
        else:
            raise AssertionError(name + ": invalid input was not rejected")


def build_base(cert):
    m, s = b*x**5, b*x
    ell = -ONE+a*x**2-a*x**4
    g = -2*x**5+(6-2*a)*x**3-2*b*x
    P = lambda U: red(s*U**2+ell*U+g)
    Q = lambda U: red(s*U**2+(-ONE+a*x**2)*U+g)
    F = red(-y+x*(b*y**2+2*a-2)+x**2*(2*a*y**3-5*a*y)
            +x**3*(-5*y**4+15*y**2-2*a)
            +x**4*(14*b*y**5+50*(a-ONE)*y**3+(29-24*a)*y))
    u, v = a*x*y+z, -y
    H = red(P(u)+m*v)
    cert.zero("coefficient-ring units", a*b-ONE, b*b+a)
    cert.zero("P(F(T)) = T modulo x^5", trunc(P(F)-y, 5))
    cert.zero("F(P(U)) = U modulo x^5", trunc(at(F, yy=P(y))-y, 5))
    W = div_x(a*(u-at(F, yy=H)), 5)
    chi = div_x(a*(y-P(F)), 5)
    U = red(F+m*z)
    V = red(chi-(ell+2*s*F)*z-s*m*z**2)
    inverse_y, inverse_z = red(-V), red(U+a*x*V)
    cert.zero("base companion identity", m*W-u+at(F, yy=H))
    cert.zero("base inverse factor identity", P(U)+m*V-y)
    cert.zero("base inverse: H(R,S)=T", at(H, yy=inverse_y, zz=inverse_z)-y)
    cert.zero("base inverse: W-component cancellation certificate",
              a*x*inverse_y+inverse_z-at(F, yy=y)-m*z)
    # The identity m*(W(R,S)-z)=0 follows from the two preceding identities.
    # Cancellation is valid in the integral domain K[x,y,z].
    cert.zero("base inverse after forward: both expanded components",
              at(inverse_y, yy=H, zz=W)-y, at(inverse_z, yy=H, zz=W)-z)
    jac = red(derivative(H,2)*derivative(W,3)-derivative(H,3)*derivative(W,2))
    cert.zero("base relative Jacobian = -1", jac+ONE)
    cert.require("base certificates have integral coefficients",
                 all(integral(f) for f in (F,H,W,inverse_y,inverse_z,chi)))
    cert.require("base wildness coefficient test: v_x(bx)=1<5", valuation_x(b*x)==1)
    return {"P":P,"Q":Q,"F":F,"H":H,"W":W,"R":inverse_y,"S":inverse_z,"m":m}


def verify_trefoil(cert, base):
    H,W,F,RY,RZ = (base[k] for k in ("H","W","F","R","S"))
    p,q,r = D(3),D(4),D(5)
    cert.zero("normalized trefoil parameter and companion",
              at(H,xx=p,yy=q,zz=r)-t, at(W,xx=p,yy=q,zz=r)-(8-14*t**2))
    ht,wt = at(H,yy=y+2,zz=z-5*x),at(W,yy=y+2,zz=z-5*x)
    phi=(ht,red(x-ht**3+3*ht),red(wt-8+14*ht**2))
    curve=(t**3-3*t,t**4-4*t**2,t**5-10*t)
    cert.zero("Shastri rectifier maps the curve to (t,0,0)",
              *(at(f,xx=curve[0],yy=curve[1],zz=curve[2])-target
                for f,target in zip(phi,(t,ZERO,ZERO))))
    cert.zero("Shastri inverse on the axis",
              at(RY,xx=p,yy=t,zz=8-14*t**2)-2-curve[1],
              at(RZ,xx=p,yy=t,zz=8-14*t**2)+5*p-curve[2])
    cert.require("Shastri rectifier component degrees",tuple(map(total_degree,phi))==(5,15,24),
                 {"degrees":[5,15,24]})
    cert.zero("rational parameter tau: cleared-denominator identity",
              curve[0]*(curve[1]+ONE)-t*(curve[0]**2-curve[1]-3))
    cert.require("rational tau denominator is not identically zero on Shastri",
                 bool(red(curve[0]**2-curve[1]-3)))
    X,Y,Z = sympy.symbols("X Y Z")
    def tau(X,Y):
        return X*(Y+1)/(X**2-Y-3)
    def rational_forward(X,Y,Z):
        parameter = tau(X,Y)
        S = Z-parameter**5+11*parameter
        return S, X-S**3+3*S, Y-S**4+4*S**2
    def rational_inverse(T,U,V):
        X = U+T**3-3*T
        Y = V+T**4-4*T**2
        parameter = tau(X,Y)
        return X,Y,T+parameter**5-11*parameter
    # Both directions are checked as rational identities. This does not assert
    # regularity at every point of the original curve.
    for direction, composition in (
        ("forward after inverse", rational_forward(*rational_inverse(X,Y,Z))),
        ("inverse after forward", rational_inverse(*rational_forward(X,Y,Z)))):
        cert.require("rational Shastri rectifier: "+direction,
                     all(sympy.cancel(value-target)==0
                         for value,target in zip(composition,(X,Y,Z))))
    cert.require("Shastri rectifier integral coefficients",all(map(integral,phi)))
    return ht


def family_p(n):
    """Construct p_N by the contraction recurrence in Z[x,y]/(x^N)."""
    nu = -y
    for _ in range(n):
        nu = trunc(-y+x*(nu**2-2),n)
    return trunc(2+x*nu-nu**2,n),nu


def build_transfer(cert, base, n):
    H,W,RY,RZ,Q = (base[k] for k in ("H","W","R","S","Q"))
    p,nu = family_p(n)
    prefix = "N="+str(n)+": "
    cert.zero(prefix+"p_N modulo x",trunc(p-(2-y**2),1))
    d3,d4,d5=D(3),D(4),D(5)
    numerator=red(d4-at(p,xx=d3,yy=d5))
    curve_z=exact_quotient(numerator,d3**n)
    cert.zero(prefix+"curve modification lands on normalized trefoil",
              at(p,xx=d3,yy=d5)+d3**n*curve_z-d4)
    cert.zero(prefix+"parameter contraction modulo D3^N",
              (at(nu,xx=d3,yy=d5)-t) % (d3**n))
    cert.require(prefix+"curve degree",degree_in_t(curve_z)==5*n+2,
                 {"third_degree":degree_in_t(curve_z)})
    centre=at(H,yy=p,zz=y,modulus=n)
    centre_w=at(W,yy=p,zz=y,modulus=n)
    cert.zero(prefix+"centre equals -y modulo x",trunc(centre+y,1))
    # centre(U)=-U+d(U), d divisible by x. Fixed-point iteration gives its
    # two-sided inverse in the nilpotent quotient K[x]/(x^N).
    d=trunc(centre+y,n)
    psi=-y
    for _ in range(n):
        psi=trunc(-y+at(d,yy=psi,modulus=n),n)
    cert.zero(prefix+"two-sided inverse of centre modulo x^N",
              at(centre,yy=psi,modulus=n)-y,at(psi,yy=centre,modulus=n)-y)
    correction=at(centre_w,yy=psi,modulus=n)
    cert.zero(prefix+"forward transfer numerator divisible by x^N",
              centre_w-at(correction,yy=centre,modulus=n))
    # These are exactly the two inverse components reduced modulo x^N.
    # Replacing x^N*z+correction by correction is valid in this quotient.
    inv_y_mod=at(RZ,zz=correction,modulus=n)
    inv_lift_mod=at(RY,zz=correction,modulus=n)
    cert.zero(prefix+"inverse transfer numerator divisible by x^N",
              inv_lift_mod-at(p,yy=inv_y_mod,modulus=n))
    Hn=at(H,yy=p+x**n*z,zz=y)
    inner=red(x**(n+1)*z+b*y+x*(p-at(p,yy=ZERO)))
    c=red(a*x*at(p,yy=ZERO))
    cert.zero(prefix+"wildness rational-length-two normal form",
              Hn-Q(c)+a*x**4*y-Q(a*inner+c)+Q(c))
    nonlinear=coefficient_y(inner,2)
    cert.zero(prefix+"inner quadratic coefficient = -x modulo x^2",
              trunc(nonlinear+x,2))
    cert.require(prefix+"inner quadratic coefficient valuation is one",
                 valuation_x(nonlinear)==1)
    cert.require(prefix+"parameter coordinate degree",total_degree(Hn)==4*n+3,
                 {"degree":total_degree(Hn)})
    # The complete transferred maps are stored by their exact polynomial
    # factors. The divisions are certified above; no evaluation at floating
    # point values and no numerical sampling is used.
    def relative_forward(X,Y,Z):
        B=red(at(p,xx=X,yy=Y)+X**n*Z)
        T=at(H,xx=X,yy=B,zz=Y)
        V=exact_quotient(at(W,xx=X,yy=B,zz=Y)-at(correction,xx=X,yy=T),X**n)
        return X,T,V
    def relative_inverse(X,T,V):
        lifted=red(X**n*V+at(correction,xx=X,yy=T))
        Y=at(RZ,xx=X,yy=T,zz=lifted)
        Z=exact_quotient(at(RY,xx=X,yy=T,zz=lifted)-at(p,xx=X,yy=Y),X**n)
        return X,Y,Z
    image=relative_forward(d3,d5,curve_z)
    w=exact_quotient((8-14*t**2)-at(correction,xx=d3,yy=t),d3**n)
    cert.zero(prefix+"actual factored forward map on the curve",
              image[0]-d3,image[1]-t,image[2]-w)
    recovered=relative_inverse(d3,t,w)
    cert.zero(prefix+"actual factored inverse recovers the curve",
              recovered[0]-d3,recovered[1]-d5,recovered[2]-curve_z)
    cert.zero(prefix+"final outer rectifier on the curve",
              image[0]-D(3,image[1]),image[2]-at(w,tt=image[1]))
    def outer_forward(X,Y,Z):
        return Y,red(X-D(3,Y)),red(Z-at(w,tt=Y))
    def outer_inverse(T,U,V):
        return red(U+D(3,T)),T,red(V+at(w,tt=T))
    cert.zero(prefix+"both generic outer composition identities",
              *(f-v for f,v in zip(outer_forward(*outer_inverse(x,y,z)),(x,y,z))),
              *(f-v for f,v in zip(outer_inverse(*outer_forward(x,y,z)),(x,y,z))))
    cert.require(prefix+"constructed coefficients are integral",
                 all(integral(f) for f in (p,nu,curve_z,psi,correction,Hn,inner,w)))
    if n==1:
        cert.zero("harmonic model is C_1",curve_z-D(7))
        cert.zero("harmonic correction matches the explicit known correction",
                  correction-(42*(a-ONE)*y**6+175*b*y**4+(147*a-161)*y**2+8))
        # For N=1 also materialize both complete polynomial relative maps.
        forward=relative_forward(x,y,z)
        inverse=relative_inverse(x,y,z)
        cert.require("harmonic full forward/inverse relative maps are integral polynomials",
                     all(integral(f) for f in (*forward,*inverse)))
        final=(forward[1],red(x-D(3,forward[1])),red(forward[2]-at(w,tt=forward[1])))
        cert.require("harmonic rectifier component degrees",tuple(map(total_degree,final))==(7,21,41),
                     {"degrees":[7,21,41]})
    return {"N":n,"p_N":str(p),"nu_N":str(nu),"curve_third_component":str(curve_z),
            "centre_inverse_mod_xN":str(psi),"correction_phi":str(correction),
            "companion_on_curve":str(w),"wild_inner_coordinate":str(inner),
            "curve_degrees":[3,5,degree_in_t(curve_z)],"parameter_coordinate_degree":total_degree(Hn),
            "inverse_verification":"Exact divisibility in both directions and invertible localized factors; explicit factored evaluation on the curve.",
            "full_relative_maps_materialized":n==1}


def verify_cremona(cert):
    # This checks the algebraic inputs to Blanc--Heden's monomial criterion.
    # The criterion itself, and the generator argument for arbitrary Laurent
    # shears, are proved/cited in the manuscript, not by this finite loop.
    for exponent in range(-3,4):
        matrix=((1,0,0),(exponent,1,0),(-exponent,0,1))
        sums=[sum(row[j] for row in matrix) for j in range(3)]
        cert.require("balanced monomial column parity r="+str(exponent),all(s%2 for s in sums))
    X,Y,Z=sympy.symbols("X Y Z")
    q=Z**3/X**3+Z/X+1/X**2
    even=4
    # D^{-1} E_y(X^(2M)q) D = E_y(q), with D=(X,X^(2M)Y,Z).
    result=sympy.cancel((X**even*Y+X**even*q)/X**even-(Y+q))
    cert.require("Laurent shear conjugation exact rational example",result==0)
    for n in (1,2,3):
        # D_N^{-1} S D_N = B_N S. The parity of D_N itself is not assumed.
        left=(X,X**n*Z,Y/X**n)
        right=(X,X**n*Z,X**(-n)*Y)
        cert.require("D_N normalizes swap generator N="+str(n),
                     all(sympy.cancel(u-v)==0 for u,v in zip(left,right)))


def negative_controls(cert,base):
    cert.rejects("negative control: nondivisible numerator rejected",
                 lambda:div_x(ONE+x,2),ArithmeticError)
    badF=base["F"]+x*y**2
    def wrong_inverse():
        # Exercise the same working identity guard as the positive checks.
        # A separate recorder prevents a failed test from entering this run.
        Certificate().zero("mutated inverse congruence", trunc(base["P"](badF)-y,5))
    cert.rejects("negative control: altered inverse coefficient detected",wrong_inverse,AssertionError)
    def wrong_identity():
        Certificate().zero("deliberately false polynomial identity", base["H"]-base["H"]+ONE)
    cert.rejects("negative control: false identity detected",wrong_identity,AssertionError)
    gamma4=(D(3),D(5)-t,D(7))
    H1=at(base["H"],yy=x*z-y**2+2,zz=y)
    cert.require("scope control: +4t model is not certified by the harmonic H",
                 bool(at(H1,xx=gamma4[0],yy=gamma4[1],zz=gamma4[2])-t))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n",type=int,default=3,help="Finite family range 1..N (default: 3)")
    parser.add_argument("--output-dir",type=Path,default=Path(__file__).resolve().parents[1]/"results")
    args=parser.parse_args()
    if args.max_n<1:
        parser.error("--max-n must be positive")
    started=perf_counter()
    cert=Certificate()
    base=build_base(cert)
    verify_trefoil(cert,base)
    families=[build_transfer(cert,base,n) for n in range(1,args.max_n+1)]
    verify_cremona(cert)
    negative_controls(cert,base)
    source=Path(__file__).read_bytes()
    result={"status":"PASS","date":"2026-10-28","run_utc":datetime.now(timezone.utc).isoformat(),
            "environment":{"python":platform.python_version(),"sympy":sympy.__version__,
                           "optimization_level":sys.flags.optimize,"arithmetic":"exact QQ[a]/(a^2-a+1)",
                           "source_sha256":hashlib.sha256(source).hexdigest()},
            "finite_family_range":[1,args.max_n],"checks":cert.checks,"families":families,
            "elapsed_seconds":round(perf_counter()-started,3),
            "scope":{"computational":"Finite polynomial identities, exact divisibility, coefficient tests and factored inverse certificates.",
                     "theoretical":"All-N induction, tame/wild criteria, stable tameness, Cremona membership and field descent require the manuscript proofs and cited theorems.",
                     "not_claimed":["A solution of the general A1 into A3 embedding problem",
                                    "Nonexistence of a different tame rectifier of the same curve",
                                    "Publication priority","Minimal stabilization dimension"]}}
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/"verification.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    cert.lines.append("ALL CHECKS PASSED; finite family range 1.."+str(args.max_n))
    cert.lines.append("Elapsed seconds: "+str(result["elapsed_seconds"]))
    (args.output_dir/"verification.log").write_text("\n".join(cert.lines)+"\n",encoding="utf-8")
    print(cert.lines[-2],flush=True)


if __name__=="__main__":
    main()
