#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Check selected parameter polynomials and the uniform no-cancellation degree calculation.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Exact finite audits of the uniform naive-Euler obstruction."""
import json
from pathlib import Path
import sympy as s

x,y,z,u=s.symbols('x y z u')
V=(x,y,z)
def C(n,v):
    a,b=s.Integer(2),v
    if n==0:return a
    for _ in range(1,n):a,b=b,s.expand(v*b-a)
    return b
def leading(poly):
    p=s.Poly(poly,*V); d=p.total_degree()
    return s.Add(*(c*x**a*y**b*z**e for (a,b,e),c in p.terms() if a+b+e==d))

P5=y*z-C(5,x)
P4=x**3*z+x**3-x**2*y*z-x*y**2-2*x*z-x+y**3+2*y*z-2*y
cases=[]
for name,P in [('H378_P5',P5),('H378_P4',P4)]:
    g=[C(j,u) for j in (3,7,8)]
    assert s.expand(P.subs(dict(zip(V,g)),simultaneous=True)-u)==0
    terms=[s.expand(s.diff(f,u).subs(u,P)*s.diff(P,v)) for f,v in zip(g,V)]
    S=s.expand(sum(terms))
    expected=-8*x**35*y if name.endswith('P5') else 8*x**16*z**7*(x-y)**8
    assert s.expand(leading(S)-expected)==0
    degrees=[s.Poly(term,*V).total_degree() for term in terms]
    assert degrees==([14,31,36] if name.endswith('P5') else [11,27,31])
    # Direct differentiation independently recovers 3-S.
    direct=sum(s.diff(v-f.subs(u,P),v) for v,f in zip(V,g))
    assert s.expand(direct-(3-S))==0
    restricted=sum(s.diff(f,u)*s.diff(P,v).subs(dict(zip(V,g)),simultaneous=True) for v,f in zip(V,g))
    assert s.expand(restricted-1)==0
    cases.append({'case':name,'P':str(P),'summand_degrees':degrees,'degree_S':max(degrees),
                  'leading_S':str(s.expand(expected)),'minimum_additive_correction_degree':max(degrees)+1,'status':'PASS'})
    print(name,'PASS',flush=True)

uniform=[]
for n in range(1,9):
    a,b,c=3,3*n+1,3*n+2
    P=y*z-C(2*n+1,x)
    assert s.expand(P.subs({x:C(a,u),y:C(b,u),z:C(c,u)},simultaneous=True)-u)==0
    r=s.Poly(P,*V).total_degree()
    # Exact input degrees and leading parts suffice for the no-cancellation audit.
    assert r==2*n+1 and leading(P)==-x**r
    degrees=[2*r+r-1,(b-1)*r+1,(c-1)*r+1]
    assert degrees[2]>max(degrees[:2])
    expected=(3*n+2)*(-1)**(n+1)*x**((2*n+1)*(3*n+1))*y
    actual=s.diff(C(c,u),u).as_poly(u).LC()*leading(P)**(c-1)*y
    assert s.expand(actual-expected)==0
    uniform.append({'n':n,'summand_degrees':degrees,'degree_S':6*n*n+5*n+2,'leading_S':str(expected),'status':'PASS'})
    print('uniform',n,'PASS',flush=True)

out={'arithmetic':'exact rational','status':'PASS','H378':cases,'uniform_cases':uniform,
     'scope':'Finite audits only; unbounded statements are proved in PROOF.md.'}
Path(__file__).with_name('naive_euler_certificates.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('ALL EXACT NAIVE-EULER CHECKS PASSED')
