#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Independently verify exact dual witnesses, complete affine families and rational rank certificates.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Independent verifier of exact bounded normal-field certificates.

No import from the search program and no solution of its feasibility system.
"""
from pathlib import Path
import json,sys
import sympy as s
x,y,z,u=s.symbols('x y z u'); V=(x,y,z)
G=(u**3-3*u,u**7-7*u**5+14*u**3-7*u,
   u**8-8*u**6+20*u**4-16*u**2+2)
vel=tuple(s.diff(f,u) for f in G)
ROOT=Path(__file__).resolve().parent
PRIME=1000003
assert s.isprime(PRIME)
def modular_rank(matrix):
    """A modular rank is a rigorous lower bound for rational rank."""
    rows=[[int(c.p)%PRIME*pow(int(c.q)%PRIME,-1,PRIME)%PRIME for c in row]
          for row in matrix.tolist()]
    if not rows:return 0
    pivot=0
    for col in range(len(rows[0])):
        pos=next((j for j in range(pivot,len(rows)) if rows[j][col]),None)
        if pos is None:continue
        rows[pivot],rows[pos]=rows[pos],rows[pivot]
        inv=pow(rows[pivot][col],-1,PRIME)
        rows[pivot]=[(v*inv)%PRIME for v in rows[pivot]]
        for j in range(pivot+1,len(rows)):
            if rows[j][col]:
                c=rows[j][col]
                rows[j]=[(a-c*b)%PRIME for a,b in zip(rows[j],rows[pivot])]
        pivot+=1
        if pivot==len(rows):break
    return pivot
def decode(terms):
    return s.expand(sum(s.Rational(t['coefficient'])*s.prod(v**e for v,e in zip(V,t['exp'])) for t in terms))
def exponents(d):
    return [(i,j,k) for i in range(d+1) for j in range(d+1-i) for k in range(d+1-i-j)]
def homogeneous_matrix(basis,d,with_divergence):
    """Independent fixed-row construction; no search-program import."""
    columns=[]; div_exps=exponents(d-1)
    for component in range(3):
        for polynomial in basis:
            derivatives=[s.expand(s.diff(polynomial,v).subs(dict(zip(V,G)),simultaneous=True)) for v in V]
            column=[]
            for i in range(3):
                for j in range(i+1,3):
                    for k in range(3):
                        p=s.Poly(vel[i]*derivatives[k]*int(component==j)-vel[j]*derivatives[k]*int(component==i),u)
                        column.extend(p.nth(power) for power in range(8*d+1))
            if with_divergence:
                p=s.Poly(s.diff(polynomial,V[component]),*V)
                column.extend(p.coeff_monomial(s.prod(v**e for v,e in zip(V,exp))) for exp in div_exps)
            columns.append(column)
    return s.Matrix.hstack(*(s.Matrix(c) for c in columns))
def check(path):
    data=json.loads(path.read_text()); d=data['degree_bound']; basis=[decode(p) for p in data['basis']]
    mons=exponents(d)
    images=[s.Poly(s.prod(f**e for f,e in zip(G,exp)),u) for exp in mons]
    ev=s.Matrix([[p.nth(j) for p in images] for j in range(8*d+1)])
    # Exact kernel containment below gives the matching upper bound.
    assert modular_rank(ev)==len(mons)-len(basis)
    if basis:
        coeff=s.Matrix([[s.Poly(p,*V).coeff_monomial(s.prod(v**e for v,e in zip(V,exp))) for p in basis] for exp in mons])
        assert modular_rank(coeff)==len(basis)
    for p in basis:
        assert s.Poly(p,*V).total_degree()<=d
        assert s.expand(p.subs(dict(zip(V,G)),simultaneous=True))==0
    if data['status']=='INFEASIBLE':
        weights=[(tuple(t['row']),s.Rational(t['weight'])) for t in data['dual']]
        value_b=s.Integer(0)
        for key,weight in weights:
            if key[0]=='normal':
                _,i,j,k,power=key
                b=s.Poly(vel[i]*int(j==k)-vel[j]*int(i==k),u).nth(power)
            else:
                b=2 if key[1:]==(0,0,0) else 0
            value_b+=weight*b
        assert value_b==1
        for comp in range(3):
            for p in basis:
                derivatives=[s.Poly(s.expand(s.diff(p,v).subs(dict(zip(V,G)),simultaneous=True)),u) for v in V]
                divergence=s.Poly(s.diff(p,V[comp]),*V)
                value=s.Integer(0)
                for key,weight in weights:
                    if key[0]=='normal':
                        _,i,j,k,power=key
                        factor=vel[i] if comp==j else (-vel[j] if comp==i else 0)
                        a=s.Poly(factor*derivatives[k].as_expr(),u).nth(power)
                    else:
                        a=divergence.coeff_monomial(s.prod(v**e for v,e in zip(V,key[1:])))
                    value+=weight*a
                assert value==0
        outcome='INFEASIBILITY_CERTIFICATE_PASS'
    elif data['status']=='FEASIBLE_NECESSARY_CONDITIONS_ONLY':
        with_divergence='divergence_two' in data.get('constraints',['divergence_two'])
        a=[decode(p) for p in data['field']]
        assert all(s.Poly(p,*V).total_degree()<=d for p in a)
        assert all(s.expand(p.subs(dict(zip(V,G)),simultaneous=True))==0 for p in a)
        if with_divergence:assert s.expand(sum(s.diff(p,v) for p,v in zip(a,V)))==2
        M=s.Matrix(a).jacobian(V).subs(dict(zip(V,G)),simultaneous=True)-s.eye(3)
        for i in range(3):
            for j in range(i+1,3):
                for k in range(3):assert s.expand(vel[i]*M[j,k]-vel[j]*M[i,k])==0
        outcome='NECESSARY_CONDITIONS_CANDIDATE_PASS'
        if 'homogeneous_basis_coefficients' in data:
            vectors=data['homogeneous_basis_coefficients'];N=s.zeros(3*len(basis),len(vectors))
            for j,vector in enumerate(vectors):
                for entry in vector:N[entry['index'],j]=s.Rational(entry['coefficient'])
            A=homogeneous_matrix(basis,d,with_divergence)
            assert (A.to_DM()*N.to_DM()).is_zero_matrix
            assert modular_rank(N)==N.cols
            assert modular_rank(A)+N.cols==A.cols
            assert N.cols==data['solution_affine_dimension']
            outcome+='; EXACT_AFFINE_DIMENSION_'+str(N.cols)+'_PASS'
    else:raise AssertionError(data['status'])
    print(path.name,outcome,flush=True)
    return {'degree':d,'status':outcome,'ideal_dimension':len(basis)}

if __name__=='__main__':
    paths=[Path(p) for p in sys.argv[1:]] if len(sys.argv)>1 else sorted(ROOT.glob('normal_degree_*.json'))
    assert paths,'No certificates'
    results=[check(path) for path in paths]
    (ROOT/'verification.json').write_text(json.dumps({'arithmetic':'exact rational','results':results,'status':'PASS'},ensure_ascii=False,indent=2)+'\n')
    print('ALL NORMAL-FIELD CERTIFICATES PASSED')
