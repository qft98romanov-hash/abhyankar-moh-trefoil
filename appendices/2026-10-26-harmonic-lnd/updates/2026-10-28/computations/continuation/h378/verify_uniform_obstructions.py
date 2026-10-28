#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Check finite Chebyshev identities supporting the uniform restricted-ansatz obstruction.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Exact checks for uniform necessary-condition obstructions, n=1,...,20.

See uniform_obstructions.tex for proofs valid for every n >= 1.
"""
from pathlib import Path
import json
import sys
try:
    import sympy as S
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "python_deps"))
    import sympy as S

x, t, u, v = S.symbols("x t u v")
C = lambda n, variable: S.Poly(2*S.chebyshevt(n,variable/2),variable,domain=S.QQ)
U = lambda n: S.Poly(S.chebyshevu(n,x/2),x,domain=S.QQ) if n>=0 else S.Poly(0,x)
records=[]
for n in range(1,21):
    un,vn=U(n),U(n-1)
    identities={
        "conic": un**2+vn**2-S.Poly(x,x)*un*vn-1,
        "determinant": un**2-vn**2-U(2*n),
        "norm_first": un**3-3*un*vn**2+S.Poly(x,x)*vn**3-U(3*n),
        "norm_second": vn**3-3*vn*un**2+S.Poly(x,x)*un**3-U(3*n+1),
        "ratio_square_first": U(2*n)**2-vn**2-U(3*n)*un,
        "ratio_square_second": U(2*n)**2-un**2-U(3*n+1)*vn,
        "center_coprimality": C(n,x)**2+S.Poly(4-x*x,x)*vn**2-4,
    }
    for name,p in identities.items():
        assert p.is_zero,(n,name,p)
    c3,cb,cc=C(3,t),C(3*n+1,t),C(3*n+2,t)
    cn_c3=C(n,x).as_expr().subs(x,c3.as_expr())
    beta_identity=S.Poly(cn_c3,t)*cc-cb**2+2-C(2,t)
    assert beta_identity.is_zero,(n,"beta")
    # Rational inequalities proving that the two tested roots lie to the
    # right of every admissible root of the height coefficient M.
    assert S.Rational(2,3*n+1)<S.Rational(1,n)
    assert S.Rational(2,3*n+2)<S.Rational(1,n+1)
    records.append({"n":n,"model":[3,3*n+1,3*n+2],"polynomial_checks":8,"passed":True})
result={
    "status":"All exact checks passed; universal claims follow from accompanying proof.",
    "models":records,
    "total_polynomial_checks":sum(r["polynomial_checks"] for r in records),
    "degree_unbounded_obstructions":[
        "No relative parameter coordinate Q(x,y)+M(x)z",
        "No relative parameter coordinate Q(x,z)+M(x)y",
        "No affine center for beta_n=(x,C_n(x)z-y^2+2,y) and any parameter lift on its target",
    ],
    "not_claimed":"Nonrectifiability or classification of all harmonic embeddings",
}
destination=Path(__file__).with_name("uniform_obstructions.json")
destination.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"models":len(records),"checks":result["total_polynomial_checks"],"certificate":str(destination)},ensure_ascii=False))
