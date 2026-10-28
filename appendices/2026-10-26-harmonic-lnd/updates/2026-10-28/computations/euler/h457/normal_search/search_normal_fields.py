#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Explore the explicitly bounded search normal fields search space; failure does not prove global nonexistence.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Exact bounded search for normal fields, with optional divergence=2.

These are necessary conditions for the Euler lift to be LND.  A feasible
answer is not asserted to be locally nilpotent.
"""
from pathlib import Path
from itertools import product
from functools import reduce
import json, sys, time
import sympy as S

HERE=Path(__file__).resolve().parent
x,y,z,u=S.symbols('x y z u')
Y=(x,y,z)

def cheb(n):
    a,b=S.Integer(2),u
    for _ in range(1,n): a,b=b,S.expand(u*b-a)
    return b

def mons(d):
    return sorted((m for m in product(range(d+1),repeat=3) if sum(m)<=d),key=lambda m:(sum(m),m))

def primitive(vec):
    den=S.ilcm(*[a.q for a in vec])
    nums=[int(a*den) for a in vec]
    g=reduce(S.igcd,nums)
    return [int(a//g) for a in nums]

def independent_rows(rows,n,prime=1000003):
    basis={};selected=[]
    for key,row,b in rows:
        work={j:int(c)%prime for j,c in row.items() if int(c)%prime}
        if b:work[n]=int(b)%prime
        while work:
            p=min(work)
            if p not in basis:
                inv=pow(work[p],-1,prime)
                basis[p]={j:c*inv%prime for j,c in work.items()}
                selected.append((key,row,b))
                if p==n:return selected,True
                break
            factor=work[p]
            for j,c in basis[p].items():
                v=(work.get(j,0)-factor*c)%prime
                if v:work[j]=v
                else:work.pop(j,None)
    return selected,False

def build_system(d,divergence=True):
    ms=mons(d); gamma=[cheb(n) for n in (4,5,7)]
    vals={}
    for m in ms:
        vals[m]=S.Poly(S.prod(g**a for g,a in zip(gamma,m)),u)
    ev=S.Matrix([[vals[m].nth(j) for m in ms] for j in range(7*d+1)])
    ns=[primitive(v) for v in ev.nullspace()]
    k=len(ns)
    assert ev*S.Matrix(ns).T==S.zeros(ev.rows,k)
    polynomials=[S.Add(*(c*S.prod(q**a for q,a in zip(Y,m)) for m,c in zip(ms,b) if c)) for b in ns]
    tangent=S.Matrix([S.diff(g,u) for g in gamma])
    cross=[tangent.cross(S.eye(3)[:,i]) for i in range(3)]
    rows={};rhs={}
    def put(key,col,val):
        if val:rows.setdefault(key,{})[col]=int(val)
    for comp in range(3):
        for bidx,b in enumerate(ns):
            col=comp*k+bidx
            for j in range(3):
                dv=S.Poly(0,u)
                for m,c in zip(ms,b):
                    if c and m[j]:
                        lower=list(m);lower[j]-=1
                        dv+=int(c*m[j])*vals[tuple(lower)]
                for a in range(3):
                    cp=S.Poly(cross[comp][a],u)*dv
                    for (power,),coef in cp.terms():put(('normal',j,a,power),col,coef)
            if divergence:
                for m,c in zip(ms,b):
                    if c and m[comp]:
                        lower=list(m);lower[comp]-=1
                        put(('div',*lower),col,c*m[comp])
    for j in range(3):
        for a in range(3):
            for (power,),coef in S.Poly(cross[j][a],u).terms():
                if coef:rhs[('normal',j,a,power)]=int(coef)
    if divergence:rhs[('div',0,0,0)]=2
    for key in rhs:rows.setdefault(key,{})
    # Finite normal conditions first.  Both exact and modular solves are checked.
    keys=sorted(rows,key=lambda key:(key[0]=='div',key))
    return ms,ns,polynomials,[(key,rows[key],rhs.get(key,0)) for key in keys],int(ev.rank())

def solve(d,divergence=True):
    start=time.time()
    ms,ns,polys,rows,rank=build_system(d,divergence)
    n=3*len(ns)
    print('SYSTEM',d,'div',divergence,'I_basis',len(ns),'unknowns',n,'rows',len(rows),flush=True)
    selected,conflict=independent_rows(rows,n)
    mat=S.Matrix([[row.get(j,0) for j in range(n)]+[b] for _,row,b in selected])
    out={'degree_bound':d,'divergence_required':divergence,'triple':[4,5,7],
         'monomials':ms,'ideal_basis_coefficients':ns,'evaluation_rank':rank,
         'unknowns':n,'equations':len(rows),'selected_equations':len(selected)}
    if conflict:
        target=S.zeros(n+1,1);target[-1]=1
        weights,free=mat.T.gauss_jordan_solve(target)
        weights=weights.subs({q:0 for q in free})
        assert mat.T*weights==target
        out['status']='INFEASIBLE'
        out['dual_witness']=[{'equation':list(key),'weight':str(weights[i])}
                             for i,(key,row,b) in enumerate(selected) if weights[i]]
        # Check the final sparse witness against every column with exact rationals.
        sums=[S.Integer(0)]*(n+1)
        for i,(_,row,b) in enumerate(selected):
            for j,c in row.items():sums[j]+=weights[i]*c
            sums[n]+=weights[i]*b
        assert sums==[S.Integer(0)]*n+[S.Integer(1)]
    else:
        general,free=mat[:,:-1].gauss_jordan_solve(mat[:,-1])
        coeffs=general.subs({q:0 for q in free})
        for key,row,b in rows:assert sum(coeffs[j]*c for j,c in row.items())==b,key
        out['status']='FEASIBLE_NOT_TESTED_FOR_LOCAL_NILPOTENCE'
        out['coefficients']=[str(a) for a in coeffs]
        out['affine_dimension']=len(free)
        out['homogeneous_directions']=[]
        for parameter in free:
            direction=general.diff(parameter)
            for key,row,b in rows:assert sum(direction[j]*c for j,c in row.items())==0,key
            out['homogeneous_directions'].append({str(i):str(a) for i,a in enumerate(direction) if a})
        fields=[S.expand(sum(coeffs[i*len(ns)+j]*p for j,p in enumerate(polys))) for i in range(3)]
        out['field']=[str(f) for f in fields]
        print('FEASIBLE_DIMENSION',len(free),'FIELD_TERMS',[len(S.Poly(f,*Y).terms()) for f in fields],flush=True)
    out['seconds']=round(time.time()-start,3)
    target=HERE/f'normal_degree{d}_{"div2" if divergence else "jet_only"}.json'
    target.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print('RESULT',d,divergence,out['status'],'dual',len(out.get('dual_witness',[])),out['seconds'],'s',flush=True)
    return out

if __name__=='__main__':
    for arg in sys.argv[1:] or ['4','5','6']:
        solve(int(arg),True)
