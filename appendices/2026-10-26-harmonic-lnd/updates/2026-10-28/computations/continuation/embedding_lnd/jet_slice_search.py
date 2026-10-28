#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Explore the explicitly bounded jet slice search search space; failure does not prove global nonexistence.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Exact finite jet systems for minimal slices of embedding derivations.

SymPy is used only to solve a small selected rational linear system.
All generated certificates can be checked by verify_jet_certificates.py
using the standard library only.
"""
from fractions import Fraction
from itertools import product
from math import factorial
from pathlib import Path
import json, sys, time

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/'python_deps'))
import sympy as S

def add(p,q):
    out=p.copy()
    for i,c in q.items(): out[i]=out.get(i,0)+c
    return {i:c for i,c in out.items() if c}

def mul(p,q):
    out={}
    for i,c in p.items():
        for j,d in q.items(): out[i+j]=out.get(i+j,0)+c*d
    return {i:c for i,c in out.items() if c}

def scale(p,c): return {i:c*v for i,v in p.items() if c*v}

def cheb(n):
    cs=[{0:2},{1:1}]
    for j in range(2,n+1): cs.append(add(mul({1:1},cs[-1]),scale(cs[-2],-1)))
    return cs[n]

def mons(n,r):
    return sorted((a for a in product(range(r+1),repeat=n) if sum(a)<=r),key=lambda a:(sum(a),a))

def jet_system(triple,d,mu=1):
    r=(d+mu)//(mu+1)
    ms=mons(3,r)
    cs=[cheb(n) for n in triple]
    values={(0,0,0):{0:1}}
    for beta in ms[1:]:
        j=next(i for i,b in enumerate(beta) if b)
        a=list(beta);a[j]-=1
        values[beta]=mul(values[tuple(a)],cs[j])
    rows={}
    for col,beta in enumerate(ms):
        for alpha in product(*(range(b+1) for b in beta)):
            order=sum(alpha)
            coeff=1
            for b,a in zip(beta,alpha):coeff*=factorial(b)//factorial(b-a)
            poly=values[tuple(b-a for b,a in zip(beta,alpha))]
            for j,c in poly.items():
                if order and j<=d-(mu+1)*order+mu:continue
                rows.setdefault((alpha,j),{})[col]=coeff*c
    # Put the jet bounds first and the retraction equations last.
    keys=sorted(rows,key=lambda a:(sum(a[0])==0,-sum(a[0]),-a[1],a[0]))
    target=((0,0,0),1)
    if target not in rows:rows[target]={};keys.append(target)
    return ms,[(key,rows[key],int(key==target)) for key in keys]

def independent_rows(rows,n,prime=1000003):
    basis={};selected=[]
    for key,row,b in rows:
        work={j:c%prime for j,c in row.items() if c%prime}
        if b:work[n]=b
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

def solve(triple,d,mu=1):
    start=time.time()
    ms,rows=jet_system(triple,d,mu)
    selected,conflict=independent_rows(rows,len(ms))
    print('SYSTEM',triple,d,len(ms),len(rows),'selected',len(selected),'conflict',conflict,flush=True)
    mat=S.MutableSparseMatrix(len(selected),len(ms)+1,{(i,j):c for i,(_,row,b) in enumerate(selected) for j,c in list(row.items())+([(len(ms),b)] if b else [])})
    result={'triple':list(triple),'multiplicity':mu,'slice_degree_bound':d,'parameter_degree_bound':(d+mu)//(mu+1),'columns':len(ms),'rows':len(rows),'selected_rows':len(selected)}
    if conflict:
        rhs=S.zeros(len(ms)+1,1);rhs[-1]=1
        weights,free=mat.T.gauss_jordan_solve(rhs)
        assert not list(free)
        # Verify exactly against the original selected rows.
        assert mat.T*weights==rhs
        result['status']='infeasible'
        result['dual_witness']=[{'alpha':list(key[0]),'u_degree':key[1],'weight':str(weights[i])} for i,(key,row,b) in enumerate(selected) if weights[i]]
    else:
        coeffs,free=mat[:,:-1].gauss_jordan_solve(mat[:,-1])
        coeffs=coeffs.subs({p:0 for p in free})
        for key,row,b in rows:
            assert sum(coeffs[j]*c for j,c in row.items())==b,(key,'missed exact equation')
        result['status']='feasible'
        result['retraction']=[{'monomial':list(a),'coefficient':str(coeffs[j])} for j,a in enumerate(ms) if coeffs[j]]
        x,y,z=S.symbols('x y z')
        result['retraction_text']=str(S.Add(*(coeffs[j]*x**a[0]*y**a[1]*z**a[2] for j,a in enumerate(ms))))
        print('RETRACTION',result['retraction_text'],flush=True)
    result['seconds']=time.time()-start
    fn=HERE/('jet_'+''.join(map(str,triple))+('' if mu==1 else '_mu'+str(mu))+'_d'+str(d)+'.json')
    fn.write_text(json.dumps(result,indent=2)+'\n')
    print('RESULT',result['status'],'certificate',len(result.get('dual_witness',[])),'seconds',result['seconds'],flush=True)
    return result

if __name__=='__main__':
    if len(sys.argv) in (5,6):
        solve(tuple(map(int,sys.argv[1:4])),int(sys.argv[4]),int(sys.argv[5]) if len(sys.argv)==6 else 1)
    else:
        for triple,d in [((3,4,5),6),((3,5,7),10),((4,5,7),11),((4,5,7),12),((3,7,8),18),((3,7,8),19)]: solve(triple,d)
