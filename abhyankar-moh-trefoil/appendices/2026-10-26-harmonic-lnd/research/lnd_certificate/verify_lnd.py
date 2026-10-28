#!/usr/bin/env python3
"""Exact factored certificate for the Shastri van-den-Essen LND.

Run: python verify_lnd.py [path/to/repo/verify.py]
Requires SymPy. All arithmetic is in Q[a]/(a^2-a+1).

The high-degree q,r are certified as polynomial arithmetic circuits by
remainder/divisibility and chain-rule certificates; they are not fully expanded.
The slice s and the invariant p are fully expanded and differentiated exactly.
The universal coefficient B can subsequently be replaced by any b(t), including
zero. Source rectification identities are rerun, rather than assumed from logs.
"""
from pathlib import Path
import contextlib
import hashlib
import importlib.util
import json
import sys
from time import perf_counter

SOURCE = (Path(sys.argv[1]) if len(sys.argv) > 1 else
          Path(__file__).resolve().parents[2] / "repo" / "verify.py")
HERE = Path(__file__).resolve().parent
started = perf_counter()
spec = importlib.util.spec_from_file_location("rectification_source", SOURCE)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

from sympy import QQ
from sympy.polys.rings import ring

R, a, B, u, x, y, z = ring("a,B,u,x,y,z", QQ)
rel = a*a-a+1
one, zero = R(1), R(0)

def red(p):
    return p % rel

def check(label, *values):
    for value in values:
        if red(value) != zero:
            raise AssertionError((label, str(value)))
    print("PASS:", label, flush=True)

def deriv(p, index):
    out = {}
    for mon, coeff in p.to_dict().items():
        if mon[index]:
            exponent = mon[index]
            newmon = list(mon)
            newmon[index] -= 1
            out[tuple(newmon)] = coeff * exponent
    return R.from_dict(out)

def substitute_source(p, images):
    # Source variables are (a,x,y,z,t); substitution is simultaneous.
    terms = p.to_dict()
    powers = []
    for j, image in enumerate(images):
        max_degree = max((mon[j] for mon in terms), default=0)
        row = [one]
        for _ in range(max_degree):
            row.append(red(row[-1]*image))
        powers.append(row)
    answer = zero
    for mon, coeff in terms.items():
        term = R(coeff)
        for j, exp in enumerate(mon):
            term = red(term*powers[j][exp])
        answer += term
    return red(answer)

def divide_B(p):
    out = {}
    for mon, coeff in red(p).to_dict().items():
        if mon[1] < 1:
            raise ArithmeticError("Numerator has a nonzero remainder modulo B")
        newmon = list(mon)
        newmon[1] -= 1
        out[tuple(newmon)] = coeff
    return R.from_dict(out)

def det(M):
    return red(M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
               -M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
               +M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))

gamma = (u**3-3*u, u**4-4*u**2, u**5-10*u)
gamma_prime = tuple(deriv(f, 2) for f in gamma)
X = (x,y,z)
V = tuple(f-B*xx for f,xx in zip(gamma,X))

def D(p):
    return red(B*deriv(p,2) + sum(fp*deriv(p,j+3)
                               for j,fp in enumerate(gamma_prime)))

check("D(B)=0 and D(V_i)=0: universal chain-rule certificate",
      D(B), *(D(vi) for vi in V))

Fgamma = tuple(substitute_source(f,(a,*gamma,u)) for f in v.phi_t)
check("literal source F(gamma(u))=(u,0,0)",
      Fgamma[0]-u,Fgamma[1],Fgamma[2])

inverse_axis = v.trefoil_inverse(v.t,v.zero,v.zero)
Gaxis = tuple(substitute_source(g,(a,x,y,z,u)) for g in inverse_axis)
check("literal source F^{-1}(u,0,0)=gamma(u)",
      *(a1-a2 for a1,a2 in zip(Gaxis,gamma)))

# P(V) and its slice are expanded here, independently of the source curve check.
p = substitute_source(v.phi_t[0],(a,*V,u))
s = divide_B(u-p)
check("literal expanded p is D-invariant and s is a slice", D(p),D(s)-one)
check("exact slice numerator division", B*s-u+p)

# For any polynomial F, F(V) modulo B is F(gamma(u)). Therefore these exact
# remainders certify the two large quotients without exponential expansion.
check("q=Q(V)/B and r=R(V)/B have zero polynomial remainder modulo B",
      Fgamma[1],Fgamma[2])
# D(Q(V)) = sum Q_i(V) D(V_i) = 0, and similarly for R. As D(B)=0,
# B*D(q)=B*D(r)=0. The polynomial ring is a domain, hence D(q)=D(r)=0.
check("all premises of the q,r chain-rule and cancellation certificate",
      D(B),*(D(vi) for vi in V))

# Exact first jets: the special fiber B=0 is a linear change over K[u].
J = [[substitute_source(v.derivative(f,j),(a,*gamma,u))
      for j in (1,2,3)] for f in v.phi_t]
check("JF(gamma(u))*gamma'(u)=(1,0,0)",
      *(sum(J[i][j]*gamma_prime[j] for j in range(3))-(one if i==0 else zero)
        for i in range(3)))
check("det JF(gamma(u))=1",det(J)-one)
M = [[-e for e in J[1]],[-e for e in J[2]],J[0]]  # rows q0,r0,s0
check("special-fiber coordinate matrix is unimodular",det(M)-one)
q0,r0,s0 = [red(sum(row[j]*X[j] for j in range(3))) for row in M]
D0 = lambda f: red(sum(fp*deriv(f,j+3) for j,fp in enumerate(gamma_prime)))
check("specialization B=0: D0(q0)=D0(r0)=0, D0(s0)=1",
      D0(q0),D0(r0),D0(s0)-one)

# A low-degree parameter retraction is NOT automatically an ambient coordinate.
F0 = y*z-x**3-5*x*y+2*z-7*x
F0source = v.y*v.z-v.x**3-5*v.x*v.y+2*v.z-7*v.x
check("the low-degree F0 is a parameter retraction",
      substitute_source(F0source,(a,*gamma,u))-u)
simple_slice = divide_B(u-substitute_source(F0source,(a,*V,u)))
simple_slice_formula = (-(3*u**6-13*u**4+7*u**2+7)*x
                       +(u**5-5*u**3+5*u)*y+(u**4-4*u**2+2)*z
                       +B*(3*(u**3-3*u)*x**2+5*x*y-y*z)-B**2*x**3)
check("simple degree-seven slice formula and D(simple_slice)=1",
      simple_slice-simple_slice_formula,D(simple_slice)-one)
for sign in (-1,1):
    critical = (v.ring(sign),v.ring(-2),v.ring(5*sign))
    check("F0 has a critical point at " + str((sign,-2,5*sign)),
          *(substitute_source(v.derivative(F0source,j),(a,*map(lambda q:R(q.as_expr()),critical),u))
            for j in (1,2,3)))

results = {
    "source_sha256":hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "field":"Q[a]/(a^2-a+1)",
    "universal_derivation":"B*d_u + f'(u)*d_x+g'(u)*d_y+h'(u)*d_z",
    "coordinate_order":["B","p","q","r","s"],
    "p_terms":len(p.to_dict()),"s_terms":len(s.to_dict()),
    "p_total_degree":max(sum(mon[1:]) for mon in p.to_dict()),
    "s_total_degree":max(sum(mon[1:]) for mon in s.to_dict()),
    "p_expanded":str(p),"s_expanded":str(s),
    "simple_slice_expanded":str(simple_slice),
    "simple_slice_total_degree":max(sum(mon[1:]) for mon in simple_slice.to_dict()),
    "special_fiber_J":[[str(e) for e in row] for row in J],
    "forward_formulas":{
        "V":"gamma(u)-B*(x,y,z)","p":"P(V)","q":"Q(V)/B",
        "r":"R(V)/B","s":"(u-P(V))/B"},
    "inverse_formulas":{
        "u":"p+B*s","X":"(gamma(p+B*s)-F^{-1}(p,B*q,B*r))/B"},
    "scope":"Exact factored certificate, with p and s fully expanded. q,r polynomiality is checked by their exact remainders modulo B; their invariance uses the chain rule and cancellation. Both full coordinate composition identities follow from the source F/F^{-1} identities after localization, and injectivity of localization.",
    "all_checks_passed":True,
    "elapsed_seconds":round(perf_counter()-started,2)
}
(HERE/"certificate_results.json").write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n")
print("ALL LND CERTIFICATE CHECKS PASSED; elapsed",results["elapsed_seconds"],"s",flush=True)
