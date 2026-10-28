#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Explore the explicitly bounded search constant mixed projection search space; failure does not prove global nonexistence.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Explore the quadratic mixed projection L=C7+a*C8.

This is a finite search only. Search coefficient M whose roots are supported
at the two roots of v=a*(x^2-1)-x, with bounded multiplicities.
No failed case is used to infer nonrectifiability.
"""
from pathlib import Path
import json
import sys
try:
    import sympy as S
except ModuleNotFoundError:
    sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"python_deps"))
    import sympy as S
x,r=S.symbols("x r")
K=S.QQ.frac_field(r)
a=r/(r*r-1)
k=x*x-1
delta=x**4-3*x*x+1
u=k-a*x
v=a*k-x
h=S.Poly(u**3-3*u*v*v-x*v**3,x,domain=K)
vp=S.Poly(v,x,domain=K)
d=S.Poly(delta,x,domain=K)
excluded=S.Poly(r*(r*r-1)*(r**4-3*r*r+1),r)
results=[]
for total in range(4,11):
    for e in range(total+1):
        f=total-e
        rem=(S.Poly((x-r)**e*(x+1/r)**f,x,domain=K)*d).rem(h)
        equations=[]
        # v+c*rem=0 for a nonzero scalar c requires all coefficients
        # of degree>=3 to vanish and proportionality to v below that.
        for j in range(3,7):
            equations.append(rem.nth(j))
        for j in (0,1):
            equations.append(rem.nth(j)*vp.nth(2)-rem.nth(2)*vp.nth(j))
        gcd=None
        for expression in equations:
            num=S.cancel(expression).as_numer_denom()[0]
            p=S.Poly(num,r)
            if p.is_zero:
                continue
            gcd=p.monic() if gcd is None else S.gcd(gcd,p).monic()
            if gcd.degree()==0:
                break
        if gcd is None:
            raise RuntimeError("all parameter equations vanish identically")
        raw=str(S.factor(gcd.as_expr()))
        while True:
            g=S.gcd(gcd,excluded)
            if g.degree()==0:break
            gcd=gcd.exquo(g).monic()
        result={"e":e,"f":f,"raw_parameter_gcd":raw,"remaining_parameter_polynomial":str(S.factor(gcd.as_expr()))}
        results.append(result)
        print(result,flush=True)
        Path(__file__).with_name("constant_mixed_projection_search.json").write_text(json.dumps(results,indent=2)+"\n")
