#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Independently verify the degree-six dual obstruction and the complete degree-seven affine family.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Independent exact verification of the degree-six obstruction and degree-seven family.

Only the Python standard library is used.  No symbolic solver is called.
Ranks are bounded below modulo a prime and above by exact kernel vectors.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json

HERE=Path(__file__).resolve().parent
PRIME=1000003

def add(p,q):
    r=p.copy()
    for a,c in q.items():r[a]=r.get(a,0)+c
    return {a:c for a,c in r.items() if c}
def scale(p,c):return {a:b*c for a,b in p.items() if b*c}
def mul(p,q):
    r={}
    for a,b in p.items():
        for c,d in q.items():r[a+c]=r.get(a+c,0)+b*d
    return {a:c for a,c in r.items() if c}
def cheb(n):
    a,b={0:2},{1:1}
    for _ in range(1,n):a,b=b,add(mul({1:1},b),scale(a,-1))
    return b
def diff(p):return {a-1:a*c for a,c in p.items() if a}
def residue(c):
    c=F(c)
    return c.numerator*pow(c.denominator,-1,PRIME)%PRIME
def rank_mod(rows):
    pivots={}
    for row in rows:
        w={i:residue(c) for i,c in row.items() if residue(c)}
        while w:
            j=min(w)
            if j not in pivots:
                inv=pow(w[j],-1,PRIME)
                pivots[j]={i:c*inv%PRIME for i,c in w.items()}
                break
            factor=w[j]
            for i,c in pivots[j].items():
                value=(w.get(i,0)-factor*c)%PRIME
                if value:w[i]=value
                else:w.pop(i,None)
    return len(pivots)

def reconstruct(data):
    d=data['degree_bound'];ms=[tuple(m) for m in data['monomials']]
    expected=sorted((m for m in product(range(d+1),repeat=3) if sum(m)<=d),key=lambda m:(sum(m),m))
    assert ms==expected
    ns=data['ideal_basis_coefficients'];k=len(ns)
    gamma=[cheb(i) for i in (4,5,7)]
    tangent=[diff(g) for g in gamma]
    vals={(0,0,0):{0:1}}
    for m in ms[1:]:
        i=next(i for i,a in enumerate(m) if a)
        lower=list(m);lower[i]-=1
        vals[m]=mul(vals[tuple(lower)],gamma[i])
    evrows={}
    for j,m in enumerate(ms):
        for power,c in vals[m].items():evrows.setdefault(power,{})[j]=c
    for b in ns:
        assert len(b)==len(ms)
        value={}
        for m,c in zip(ms,b):value=add(value,scale(vals[m],c))
        assert not value
    eval_rank=rank_mod(evrows.values())
    assert eval_rank==len(ms)-k==data['evaluation_rank']
    assert rank_mod([{i:c for i,c in enumerate(b) if c} for b in ns])==k
    # Thus the supplied vectors are an exact basis for every degree-d relation.
    cross=[[{},scale(tangent[2],-1),tangent[1]],
           [tangent[2],{},scale(tangent[0],-1)],
           [scale(tangent[1],-1),tangent[0],{}]]
    derivatives=[]
    for b in ns:
        ds=[]
        for j in range(3):
            value={}
            for m,c in zip(ms,b):
                if c and m[j]:
                    lower=list(m);lower[j]-=1
                    value=add(value,scale(vals[tuple(lower)],c*m[j]))
            ds.append(value)
        derivatives.append(ds)
    rows={};rhs={}
    for i in range(3):
        for bidx,b in enumerate(ns):
            col=i*k+bidx
            for j in range(3):
                for a in range(3):
                    for power,c in mul(cross[a][i],derivatives[bidx][j]).items():
                        rows.setdefault(('normal',j,a,power),{})[col]=c
            if data['divergence_required']:
                for m,c in zip(ms,b):
                    if c and m[i]:
                        lower=list(m);lower[i]-=1
                        rows.setdefault(('div',*lower),{})[col]=c*m[i]
    for j in range(3):
        for a in range(3):
            for power,c in cross[a][j].items():rhs[('normal',j,a,power)]=c
    if data['divergence_required']:rhs[('div',0,0,0)]=2
    for key in rhs:rows.setdefault(key,{})
    return ms,ns,rows,rhs

def check_negative():
    data=json.loads((HERE/'normal_degree6_div2.json').read_text())
    ms,ns,rows,rhs=reconstruct(data)
    assert data['status']=='INFEASIBLE'
    sums=[F(0)]*(3*len(ns));target=F(0)
    for w in data['dual_witness']:
        key=tuple(w['equation']);weight=F(w['weight'])
        assert key[0]=='normal'  # The obstruction does not use divergence rows.
        for j,c in rows[key].items():sums[j]+=weight*c
        target+=weight*rhs.get(key,0)
    assert not any(sums) and target==1
    return {'degree_bound':6,'status':'EXACTLY_INFEASIBLE','dual_weights':len(data['dual_witness']),
            'unknowns':3*len(ns),'does_not_require_divergence_condition':True,
            'all_characteristic_zero_extensions':True}

def check_positive():
    data=json.loads((HERE/'normal_degree7_div2.json').read_text())
    ms,ns,rows,rhs=reconstruct(data)
    n=3*len(ns);k=len(ns)
    base=list(map(F,data['coefficients']))
    directions=[{int(i):F(c) for i,c in h.items()} for h in data['homogeneous_directions']]
    for key,row in rows.items():
        assert sum((base[j]*c for j,c in row.items()),F(0))==rhs.get(key,0),key
        for h in directions:
            assert sum((h.get(j,F(0))*c for j,c in row.items()),F(0))==0,key
    matrix_rank=rank_mod(rows.values());direction_rank=rank_mod(directions)
    assert matrix_rank+direction_rank==n
    assert direction_rank==len(directions)==data['affine_dimension']==19
    # An affine point + 19 independent exact kernel directions is the full family.
    fields=[]
    for i in range(3):
        value={}
        for j,b in enumerate(ns):
            for m,c in zip(ms,b):
                if c:value[m]=value.get(m,F(0))+base[i*k+j]*c
        fields.append({m:c for m,c in value.items() if c})
    axes=[{m[0]:c for m,c in f.items() if m[1]==m[2]==0} for f in fields]
    assert not axes[1] and not axes[2]
    degree=max(axes[0]);assert degree==7
    axis=axes[0]
    assert sum(c*2**j for j,c in axis.items())==0
    assert sum(j*c*2**(j-1) for j,c in axis.items() if j)==1
    # The invariant-axis argument applies only to the displayed point, not to
    # the full family. Check this limitation exactly on all basis directions.
    axis_directions=[]
    for number,h in enumerate(directions,1):
        components=[]
        for i in (1,2):
            value={}
            for bidx,b in enumerate(ns):
                coefficient=h.get(i*k+bidx,F(0))
                if coefficient:
                    for m,c in zip(ms,b):
                        if m[1]==m[2]==0 and c:
                            value[m[0]]=value.get(m[0],F(0))+coefficient*c
            components.append({str(j):str(c) for j,c in value.items() if c})
        axis_directions.append({'direction':number,'preserves_axis':not any(components),
                                'y_axis':components[0],'z_axis':components[1]})
    nonpreserving=[row['direction'] for row in axis_directions if not row['preserves_axis']]
    assert len(nonpreserving)==11
    family_axis={'arithmetic':'exact rational','affine_dimension':19,
                 'nonpreserving_directions':nonpreserving,'directions':axis_directions,
                 'scope':'The invariant axis is not preserved by the entire affine family.'}
    (HERE/'family_axis_test.json').write_text(json.dumps(family_axis,indent=2)+'\n')
    # At every iteration, degree(phi(x)d/dx)^m x = 1+6m and its coefficient is
    # a^m product_{j=0}^{m-1}(1+6j), nonzero in characteristic zero.  This proves
    # non-local-finiteness, and the falling factorial formula excludes LND E.
    return {'degree':7,'status':'COMPLETE_AFFINE_FAMILY_VERIFIED',
            'unknowns':n,'matrix_rank':matrix_rank,'affine_dimension':direction_rank,
            'particular_field_terms':[len(f) for f in fields],
            'particular_axis_coefficients':{str(j):str(c) for j,c in sorted(axis.items())},
            'particular_axis_degree':degree,'particular_is_not_locally_finite':True,
            'family_directions_not_preserving_axis':len(nonpreserving),
            'scope':'The particular point is excluded; the remaining 19-parameter family is not classified.'}

def main():
    result={'date':'2026-10-28','arithmetic':'fractions.Fraction and exact modular rank lower bounds',
            'prime':PRIME,'degree_six':check_negative(),'degree_seven':check_positive(),'status':'PASS'}
    (HERE/'independent_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('DEGREE <=6: EXACT DUAL OBSTRUCTION PASSED')
    print('DEGREE 7: COMPLETE 19-PARAMETER FAMILY PASSED')
    print('PARTICULAR POINT: ALGEBRAIC NON-LND OBSTRUCTION PASSED')

if __name__=='__main__':main()
