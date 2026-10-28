# Consolidated verification copy, 28 October 2026.
# Purpose: Independently check rank minors, resultant and Bezout identities in the H(4,5,7) analysis.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Independent arithmetic audit of the H457 degree-four obstruction.

This verifier reads the proposed basis from the certificate but reconstructs
the evaluation map via an independent integral recurrence, proves its rank
using explicit nonzero minors, and independently recomputes the difficult
quartic-z elimination and its resultant.
"""
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'python_deps'))
import sympy as S

here=Path(__file__).resolve().parent
data=json.loads((here.parent/'h457'/'degree4_certificate.json').read_text())
x,y,z,t,r,w,a,b,L,U=S.symbols('x y z t r w a b L U')

def cheb(n):
    left,right=S.Poly(2,t),S.Poly(t,t)
    for _ in range(1,n):left,right=right,S.Poly(t,t)*right-left
    return right.as_expr() if n else left.as_expr()

gamma=dict(zip((x,y,z),[cheb(n) for n in (4,5,7)]))
K=[S.sympify(q,locals={'x':x,'y':y,'z':z}) for q in data['kernel_degree4_basis']]
F0=(x*x-2)*z-y**3+3*y
assert S.expand(F0.subs(gamma,simultaneous=True)-t)==0
assert all(S.expand(q.subs(gamma,simultaneous=True))==0 for q in K)
exps=[(i,j,k) for i in range(5) for j in range(5-i) for k in range(5-i-j)]
mon=[x**i*y**j*z**k for i,j,k in exps]
cols=[S.Poly(q.subs(gamma,simultaneous=True),t) for q in mon]
E=S.Matrix([[p.nth(j) for p in cols] for j in range(29)])
B=S.Matrix([[S.Poly(q,x,y,z).coeff_monomial(m) for q in K] for m in mon])
assert E*B==S.zeros(29,7)
rank_cols=list(E.rref()[1]); rank_rows=list(E[:,rank_cols].T.rref()[1])
minor=E.extract(rank_rows,rank_cols).det()
kernel_rows=list(B.T.rref()[1]); kernel_minor=B.extract(kernel_rows,list(range(7))).det()
assert len(rank_cols)==len(rank_rows)==28 and minor!=0
assert len(kernel_rows)==7 and kernel_minor!=0

# Recompute the full quartic-z branch from the family.
coeff=[a,-4*w*(r+r**3),w,w*(r**4-6*r*r),b,-4*w*r**3,-w*r**4]
F=S.expand((F0+sum(c*q for c,q in zip(coeff,K))).subs(y,L-r*x))
pxl=S.Poly(F,x,L)
e30=pxl.coeff_monomial(x**3)
e21=pxl.coeff_monomial(x*x*L)
linear=[S.Poly(e,z).coeff_monomial(z) for e in (e30,e21)]
sol=S.solve(linear,[a,b],dict=True)
assert len(sol)==1
Pexpr=S.factor((-3*r*e21-9*e30).subs(sol[0])/w)
assert S.Poly(Pexpr,r)==S.Poly(3*r**6-41*r**4+25*r*r+1,r)
Az=pxl.coeff_monomial(x*x).subs(sol[0])
B2=pxl.coeff_monomial(x*L*L).subs(sol[0])
Qexpr=S.factor(-3*r*r*S.Poly(S.expand(-4*w*Az-B2*B2),z).coeff_monomial(z*z)/(w*w))
assert S.Poly(Qexpr,r)==S.Poly(48*r**8+96*r**6-8*r**4-56*r*r+7,r)
P=S.Poly(3*U**3-41*U*U+25*U+1,U)
Q=S.Poly(48*U**4+96*U**3-8*U*U-56*U+7,U)
res=S.resultant(P,Q,U)
assert res!=0
AA=S.Poly(98443392*U**3+361976832*U*U+422233904*U+148292464,U)
BB=S.Poly(-6152712*U*U+73768936*U+82963001,U)
assert AA*P+BB*Q==S.Poly(729033471,U)

result={
 'status':'PASS',
 'evaluation_rank_lower_bound_minor':{'rows':rank_rows,'columns':rank_cols,'determinant':str(minor)},
 'seven_independent_kernel_vectors_minor':{'rows':kernel_rows,'determinant':str(kernel_minor)},
 'exact_rank':28,
 'quartic_z_linear_elimination':{str(k):str(v) for k,v in sol[0].items()},
 'quartic_z_necessary_polynomials':[str(P.as_expr()),str(Q.as_expr())],
 'quartic_z_resultant':str(res),
 'bezout_constant':729033471,
 'limitations':'Normal-form applicability and branch completeness were separately reviewed mathematically in review_457.md; this is not a nonrectifiability certificate.'
}
(here/'review_457_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
