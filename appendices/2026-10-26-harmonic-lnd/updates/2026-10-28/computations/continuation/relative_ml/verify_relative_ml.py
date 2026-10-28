#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Check finite shear examples; the universal relative-ML conclusion is proved in the accompanying text.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Exact witnesses for trivial relative ML/Derksen invariants of Chebyshev curves.

Run with Python + SymPy. No floating point, no external CAS, no repository edits.
The general theorem is proved in relative_ml_obstruction.md.
"""
from pathlib import Path
import json
import sympy as s

x, y, z, t, lam = s.symbols("x y z t lam")
xyz = (x, y, z)

def C(n, v):
    """Monic normalization C_n(v)=2T_n(v/2), via integral recurrence."""
    if n == 0:
        return s.Integer(2)
    a, b = s.Integer(2), v
    for _ in range(1, n):
        a, b = b, s.expand(v*b-a)
    return b

def zero(p):
    return s.Poly(s.expand(p), t, x, y, z, lam, domain=s.QQ).is_zero

def check(triple):
    a, b, c = triple
    gamma = (C(a,t), C(b,t), C(c,t))
    subs = dict(zip(xyz,gamma))
    coeffs = (C(c,y)-C(b,z), C(c,x)-C(a,z), C(b,x)-C(a,y))
    checks = []
    for i, f in enumerate(coeffs):
        assert f != 0
        assert zero(s.diff(f,xyz[i]))
        assert zero(f.subs(subs, simultaneous=True))
        for r in (1,2,3):
            g = s.expand(f**r)
            # D_i^2(x_i)=0 and D_i(x_j)=0 (j != i): finite LND witness.
            assert zero(g*s.diff(g,xyz[i]))
            shift = list(xyz)
            shift[i] = xyz[i]+lam*g
            reverse = list(xyz)
            reverse[i] = xyz[i]-lam*g
            subshift, subreverse = dict(zip(xyz,shift)),dict(zip(xyz,reverse))
            assert all(zero(shift[j].subs(subreverse, simultaneous=True)-xyz[j]) for j in range(3))
            assert all(zero(reverse[j].subs(subshift, simultaneous=True)-xyz[j]) for j in range(3))
            # Use the already checked f(gamma)=0; avoid expanding g(gamma).
            fixed_coeff = f.subs(subs, simultaneous=True).expand()
            assert fixed_coeff == 0
            assert all(zero(gamma[j] + (lam*fixed_coeff**r if j==i else 0)-gamma[j]) for j in range(3))
            checks.append({"axis":str(xyz[i]),"r":r,"degree_coefficient":s.Poly(g,*xyz).total_degree(),"inverse_checked":True,"fixes_curve":True,"D_squared_on_generator_zero":True})
    return {"triple":list(triple),"coefficients":[str(f) for f in coeffs],"checks":checks,"exact":True}

def main():
    triples=((3,4,5),(3,5,7),(3,7,8),(4,5,7),(5,6,7),(7,9,11))
    results=[check(tr) for tr in triples]
    out={"field":"Q","normalization":"C_n(t)=2T_n(t/2)","triples":results,
         "num_shears_checked":sum(len(item['checks']) for item in results),
         "general_result":"For every ideal I with dim(A/I)<=n-2 and every r>=1, intersection ker D over nonzero LND with D(A) subset I^r is k; the generated kernel algebra is A.",
         "scope":"Finite computations validate witnesses; the all-ideals theorem has an independent elementary proof."}
    dest=Path(__file__).with_name("relative_ml_verification.json")
    dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":"PASS","triples":len(results),"shears":out['num_shears_checked'],"output":str(dest)},ensure_ascii=False))

if __name__ == "__main__":
    main()
