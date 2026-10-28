#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Check exact jet-separating lower bounds and explicit upper slices in all supplied certificates.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Independent exact verifier. Python standard library only.

Checks the separating jet functionals on every possible retraction monomial;
then constructs each upper slice in five variables and literally applies D.
The theorem in PROOF.md justifies why these finite tests exclude ALL slices.
"""
from fractions import Fraction as Q
from math import prod
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent

# Dense one-variable polynomials, independent of the search implementation.
def trim(a):
    a=list(a)
    while len(a)>1 and not a[-1]: a.pop()
    return a

def plus(a,b):
    return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])

def times(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return trim(c)

def cn(n):
    a,b=[2],[0,1]
    if n==0:return a
    for _ in range(1,n):a,b=b,plus([0]+b,[-v for v in a])
    return b

def tuples(length,total):
    if length==0:
        if total==0:yield ()
        return
    for i in range(total+1):
        for tail in tuples(length-1,total-i):yield (i,)+tail

def bounded_monomials(n,d):
    return [a for total in range(d+1) for a in tuples(n,total)]

def verify_lower(path):
    data=json.loads(path.read_text())
    assert data['status']=='infeasible'
    d=data['slice_degree_bound'];mu=data.get('multiplicity',1);r=(d+mu)//(mu+1)
    assert r==data['parameter_degree_bound']
    witness=[(tuple(e['alpha']),e['u_degree'],Q(e['weight'])) for e in data['dual_witness']]
    assert all(len(a)==3 and min(a)>=0 and j>=0 for a,j,w in witness)
    assert all(not sum(a) or j>d-(mu+1)*sum(a)+mu for a,j,w in witness)
    assert sum(w for a,j,w in witness if a==(0,0,0) and j==1)==1
    cs=[cn(n) for n in data['triple']]
    powers=[]
    for c in cs:
        ps=[[1]]
        for _ in range(r):ps.append(times(ps[-1],c))
        powers.append(ps)
    count=0
    for beta in bounded_monomials(3,r):
        result=Q(0)
        for alpha,j,w in witness:
            if any(a>b for a,b in zip(alpha,beta)):continue
            factor=prod(prod(range(b-a+1,b+1)) for a,b in zip(alpha,beta))
            value=times(times(powers[0][beta[0]-alpha[0]],powers[1][beta[1]-alpha[1]]),powers[2][beta[2]-alpha[2]])
            if j<len(value):result+=w*factor*value[j]
        assert not result,(data['triple'],d,beta,result)
        count+=1
    assert count==data['columns']
    return {'triple':data['triple'],'multiplicity':mu,'excluded_slice_degree':d,'retraction_columns_checked':count,'dual_nonzero_weights':len(witness)}

# Sparse five-variable polynomials (T,U,X,Y,Z), distinct from search data.
Z=(0,0,0,0,0)
ONE={Z:Q(1)}
def var(i):
    a=[0]*5;a[i]=1
    return {tuple(a):Q(1)}
T,U,X,Y,Zv=[var(i) for i in range(5)]
def pplus(*polys):
    result={}
    for p in polys:
        for a,c in p.items():result[a]=result.get(a,Q(0))+c
    return {a:c for a,c in result.items() if c}
def pscale(p,c):return {a:v*c for a,v in p.items() if v*c}
def ptimes(p,q):
    result={}
    for a,c in p.items():
        for b,d in q.items():
            e=tuple(i+j for i,j in zip(a,b))
            result[e]=result.get(e,Q(0))+c*d
    return {a:c for a,c in result.items() if c}
def ppow(p,n):
    result=ONE
    for _ in range(n):result=ptimes(result,p)
    return result
def pdiff(p,i):
    result={}
    for a,c in p.items():
        if a[i]:
            b=list(a);b[i]-=1
            result[tuple(b)]=c*a[i]
    return result
def in_u(c):return {(0,j,0,0,0):Q(v) for j,v in enumerate(c) if v}

def retraction(triple):
    a,b,c=triple
    if c-b==1 and (b+c)%a==0:
        m=(b+c)//a
        out={(j,0,0):Q(-coef) for j,coef in enumerate(cn(m)) if coef}
        out[(0,1,1)]=Q(1)
        return out
    if triple==(3,5,7):return {(2,0,1):Q(1),(1,2,0):Q(-1),(1,0,0):Q(2),(0,0,1):Q(-1)}
    if triple==(4,5,7):return {(2,0,1):Q(1),(0,3,0):Q(-1),(0,1,0):Q(3),(0,0,1):Q(-2)}
    raise ValueError(triple)

def evaluate(P,vs):
    out={}
    for a,c in P.items():
        term=pscale(ONE,c)
        for v,n in zip(vs,a):term=ptimes(term,ppow(v,n))
        out=pplus(out,term)
    return out

def verify_upper(triple,expected,mu=1,P=None):
    gamma=[in_u(cn(n)) for n in triple]
    P=P or retraction(triple)
    assert evaluate(P,gamma)==U
    coefficient=ppow(T,mu)
    vs=[pplus(f,pscale(ptimes(coefficient,x),-1)) for f,x in zip(gamma,(X,Y,Zv))]
    numerator=pplus(U,pscale(evaluate(P,vs),-1))
    sigma={}
    for a,c in numerator.items():
        assert a[0]>=mu
        b=list(a);b[0]-=mu;sigma[tuple(b)]=c
    ds=ptimes(coefficient,pdiff(sigma,1))
    for i,f in enumerate(gamma):ds=pplus(ds,ptimes(pdiff(f,1),pdiff(sigma,i+2)))
    assert ds==ONE
    degree=max(map(sum,sigma))
    assert degree==expected,(triple,degree,expected)
    return {'triple':list(triple),'multiplicity':mu,'slice_degree':degree,'slice_terms':len(sigma),'retraction_degree':max(map(sum,P)),
            'retraction':[{'monomial':list(a),'coefficient':str(c)} for a,c in sorted(P.items())],
            'slice':[{'monomial':list(a),'coefficient':str(c)} for a,c in sorted(sigma.items())]}

if __name__=='__main__':
    cases=[((3,4,5),7),((3,5,7),11),((4,5,7),12),((3,7,8),13),((3,10,11),19),((3,13,14),25),((5,7,8),11),((7,10,11),15)]
    results=[]
    for triple,degree in cases:
        path=HERE/('jet_'+''.join(map(str,triple))+'_d'+str(degree-1)+'.json')
        if not path.exists():
            raise FileNotFoundError(path)
        lower=verify_lower(path)
        upper=verify_upper(triple,degree)
        results.append({'minimum_slice_degree':degree,'lower':lower,'upper':upper})
        print('CERTIFIED',triple,'minimum slice degree',degree,'dual weights',lower['dual_nonzero_weights'],'monomials',lower['retraction_columns_checked'],'slice terms',upper['slice_terms'],flush=True)
    p4={(3,0,1):Q(1),(3,0,0):Q(1),(2,1,1):Q(-1),(1,2,0):Q(-1),(1,0,1):Q(-2),(1,0,0):Q(-1),(0,3,0):Q(1),(0,1,1):Q(2),(0,1,0):Q(-2)}
    for mu,degree in [(2,13),(3,17),(4,21),(5,22),(6,23),(7,25)]:
        path=HERE/('jet_378_mu'+str(mu)+'_d'+str(degree-1)+'.json')
        if not path.exists():raise FileNotFoundError(path)
        lower=verify_lower(path)
        upper=verify_upper((3,7,8),degree,mu,p4 if mu>=5 else None)
        results.append({'minimum_slice_degree':degree,'lower':lower,'upper':upper})
        print('CERTIFIED',(3,7,8),'multiplicity',mu,'minimum slice degree',degree,'dual weights',lower['dual_nonzero_weights'],'monomials',lower['retraction_columns_checked'],flush=True)
    assert len(results)==14
    (HERE/'verified_results.json').write_text(json.dumps({'arithmetic':'fractions.Fraction; no third-party packages','scope':'ALL polynomial slices over every characteristic-zero field, by the jet reduction theorem','results':results},indent=2)+'\n')
    print('ALL 14 EXACT CERTIFICATES PASSED',flush=True)
