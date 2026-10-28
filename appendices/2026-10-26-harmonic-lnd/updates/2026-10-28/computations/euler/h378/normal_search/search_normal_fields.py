#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Explore the explicitly bounded search normal fields search space; failure does not prove global nonexistence.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Exact bounded search: fields vanishing on gamma, normal identity, divergence 2.

This checks necessary conditions for the homogeneous Euler-LND strategy.
Feasibility never asserts local nilpotence.
"""
from pathlib import Path
import argparse,json,time
import sympy as s

x,y,z,u=s.symbols('x y z u'); V=(x,y,z)
ROOT=Path(__file__).resolve().parent
def C(n,v):
    a,b=s.Integer(2),v
    if n==0:return a
    for _ in range(1,n):a,b=b,s.expand(v*b-a)
    return b
G=tuple(C(n,u) for n in (3,7,8)); vel=tuple(s.diff(f,u) for f in G)
def qstr(q):return str(q)
def mons(d):return [(i,j,k) for i in range(d+1) for j in range(d+1-i) for k in range(d+1-i-j)]
def mon(e):return s.prod(v**i for v,i in zip(V,e))
def polysparse(p):return [{'exp':list(e),'coefficient':qstr(c)} for e,c in s.Poly(p,*V).terms()]
def normalize_column(col):
    den=s.ilcm(*[q.q for q in col]); vals=[int(q*den) for q in col]
    common=s.igcd(*vals); vals=[v//common for v in vals]
    if next(v for v in vals if v)<0:vals=[-v for v in vals]
    return s.Matrix(vals)

def restriction_basis(d):
    exps=mons(d); images=[s.Poly(s.prod(f**i for f,i in zip(G,e)),u) for e in exps]
    evaluation=s.Matrix([[p.nth(j) for p in images] for j in range(8*d+1)])
    kernels=[normalize_column(c) for c in evaluation.nullspace()]
    basis=[s.expand(sum(a*mon(e) for a,e in zip(c,exps))) for c in kernels]
    assert all(s.expand(p.subs(dict(zip(V,G)),simultaneous=True))==0 for p in basis)
    return exps,evaluation,kernels,basis

def system_from_basis(basis,d):
    rowcols={}; rhs={}; width=3*len(basis)
    def add_poly(kind,extra,pol,col=None):
        gens=(u,) if kind=='normal' else V
        p=s.Poly(s.expand(pol),*gens)
        for exp,c in p.terms():
            if not c:continue
            key=(kind,)+extra+exp
            if col is None:rhs[key]=rhs.get(key,0)+c
            else:rowcols.setdefault(key,{})[col]=rowcols.get(key,{}).get(col,0)+c
    for i in range(3):
        for j in range(i+1,3):
            for k in range(3):
                add_poly('normal',(i,j,k),vel[i]*int(j==k)-vel[j]*int(i==k))
    add_poly('divergence',(),s.Integer(2))
    for component in range(3):
        for bidx,p in enumerate(basis):
            col=component*len(basis)+bidx
            deriv=[s.expand(s.diff(p,v).subs(dict(zip(V,G)),simultaneous=True)) for v in V]
            for i in range(3):
                for j in range(i+1,3):
                    factor=vel[i] if component==j else (-vel[j] if component==i else 0)
                    if factor==0:continue
                    for k in range(3):add_poly('normal',(i,j,k),factor*deriv[k],col)
            add_poly('divergence',(),s.diff(p,V[component]),col)
    keys=sorted(set(rowcols)|set(rhs))
    A=s.zeros(len(keys),width)
    for row,key in enumerate(keys):
        for col,c in rowcols.get(key,{}).items():A[row,col]=c
    b=s.Matrix([rhs.get(key,0) for key in keys])
    return keys,A,b

def solve_with_certificate(A,b):
    if not A.cols:
        j=next(i for i,a in enumerate(b) if a)
        lam=s.zeros(A.rows,1);lam[j]=1/b[j]
        return {'feasible':False,'rank':0,'dual':lam,'independent_rows':[]}
    _,rows=A.T.rref(); rows=list(rows); rank=len(rows)
    A0=A.extract(rows,list(range(A.cols))); b0=b.extract(rows,[0])
    _,cols=A0.rref(); cols=list(cols)
    square=A.extract(rows,cols)
    c=s.zeros(A.cols,1)
    solution=square.inv()*b0
    for j,v in zip(cols,solution):c[j]=v
    residual=A*c-b
    if residual==s.zeros(A.rows,1):
        return {'feasible':True,'rank':rank,'solution':c,'independent_rows':rows}
    j=next(i for i,a in enumerate(residual) if a)
    coeff=square.T.inv()*A.extract([j],cols).T
    discrepancy=b[j]-(coeff.T*b0)[0]
    lam=s.zeros(A.rows,1);lam[j]=1/discrepancy
    for row,value in zip(rows,coeff):lam[row]-=value/discrepancy
    assert lam.T*A==s.zeros(1,A.cols)
    assert (lam.T*b)[0]==1
    return {'feasible':False,'rank':rank,'dual':lam,'independent_rows':rows}

def run(d,normal_only=False):
    begin=time.monotonic();print('START degree',d,flush=True)
    exps,ev,kernels,basis=restriction_basis(d)
    print('ideal dimension',len(basis),'monomials',len(exps),flush=True)
    keys,A,b=system_from_basis(basis,d)
    if normal_only:
        selected=[i for i,key in enumerate(keys) if key[0]=='normal']
        A=A.extract(selected,list(range(A.cols)));b=b.extract(selected,[0]);keys=[keys[i] for i in selected]
    print('linear shape',A.shape,flush=True)
    result=solve_with_certificate(A,b)
    data={'date':'2026-10-28','model':[3,7,8],'degree_bound':d,'monomials':len(exps),
          'restriction_rank':len(exps)-len(basis),'ideal_dimension':len(basis),
          'unknowns':A.cols,'equations':A.rows,'matrix_rank':result['rank'],
          'homogeneous_solution_dimension':A.cols-result['rank'],
          'status':'FEASIBLE_NECESSARY_CONDITIONS_ONLY' if result['feasible'] else 'INFEASIBLE',
          'basis':[polysparse(p) for p in basis],
          'constraints':['vanishing_on_curve','normal_identity']+([] if normal_only else ['divergence_two']),
          'scope':'No assertion of local nilpotence; no assertion of rectifiability or nonrectifiability.'}
    if result['feasible']:
        data['solution_affine_dimension']=A.cols-result['rank']
        c=result['solution'];field=[s.expand(sum(c[i*len(basis)+j]*p for j,p in enumerate(basis))) for i in range(3)]
        if not normal_only:assert sum(s.diff(a,v) for a,v in zip(field,V)).expand()==2
        assert all(s.expand(a.subs(dict(zip(V,G)),simultaneous=True))==0 for a in field)
        J=s.Matrix(field).jacobian(V).subs(dict(zip(V,G)),simultaneous=True)-s.eye(3)
        for i in range(3):
            for j in range(i+1,3):
                for k in range(3):assert s.expand(vel[i]*J[j,k]-vel[j]*J[i,k])==0
        data['field']=[polysparse(p) for p in field]
        data['field_text']=[str(p) for p in field]
        data['solution_coefficients']=[qstr(v) for v in c]
    else:
        data['dual']=[{'row':list(keys[i]),'weight':qstr(v)} for i,v in enumerate(result['dual']) if v]
        data['dual_nonzero']=len(data['dual'])
    data['seconds']=round(time.monotonic()-begin,3)
    prefix='normal_only_degree' if normal_only else 'normal_degree'
    (ROOT/f'{prefix}_{d}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(data['status'],'degree',d,'rank',result['rank'],'seconds',data['seconds'],flush=True)
    return data

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('degrees',type=int,nargs='*',default=[3,4,5,6]);ap.add_argument('--normal-only',action='store_true');args=ap.parse_args()
    for d in args.degrees:run(d,args.normal_only)
