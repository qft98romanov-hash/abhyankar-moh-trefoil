#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Independently verify binary identities, products and Groebner reductions for iterated modifications.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
from pathlib import Path
import sys, json
try:
    import sympy as S
except ModuleNotFoundError:
    sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"python_deps"))
    import sympy as S
x,p=S.symbols('x p')
checks=[]
for ell in range(1,6):
    vv=S.symbols('v0:'+str(ell+1))
    order=lambda exponent: (sum((2**j)*a for j,a in enumerate(exponent)),exponent)
    rel=[vv[j]**2-x*vv[j+1]+(p if j==0 else vv[j-1]) for j in range(ell)]
    G=S.groebner(rel,*vv,domain=S.QQ.poly_ring(x,p),order=order)
    assert len(G.polys)==ell
    assert {S.expand(g.as_expr()) for g in G.polys}==set(rel)
    graded_rel=[vv[j]**2-x*vv[j+1] for j in range(ell)]
    GG=S.groebner(graded_rel,*vv,domain=S.QQ.poly_ring(x,p),order=order)
    E=lambda n:sum(n//(2**j) for j in range(1,ell+1))
    def monomial(n):
        q,r=divmod(n,2**ell)
        return vv[ell]**q*S.prod(vv[j]**((r>>j)&1) for j in range(ell))
    for n in range(65):
        q,r=divmod(n,2**ell)
        assert E(n)==q*(2**ell-1)+r-r.bit_count()
    for i in range(9):
        for j in range(9):
            exponent=E(i+j)-E(i)-E(j)
            assert exponent>=0
            expr=monomial(i)*monomial(j)-x**exponent*monomial(i+j)
            assert GG.reduce(S.expand(expr))[1]==0
    checks.append({'l':ell,'groebner':'PASS','binary_identities':65,'product_identities':81})
first=[]
for n in range(17):
    a3=3*n-n//2-n//4-n//8
    axd2=3*n-n//2-n//4
    first.append({'n':n,'D3':a3,'xD2':axd2})
assert next(row['n'] for row in first if row['D3']!=row['xD2'])==8
assert first[8]=={'n':8,'D3':17,'xD2':18}
result={'status':'PASS','cases':checks,'comparison_D3_xD2':first}
target=Path(__file__).with_name('iterated_independent_checks.json')
target.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','cases':len(checks),'binary_and_product_identities':5*(65+81),'certificate':str(target)}))
