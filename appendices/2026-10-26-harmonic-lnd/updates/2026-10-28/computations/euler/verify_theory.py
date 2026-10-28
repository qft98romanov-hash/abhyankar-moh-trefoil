#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Check explicit positive and negative examples of the normal locally-finite-field criterion.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Exact finite checks accompanying theory.md, not a proof of universal statements."""
from pathlib import Path
import json
import sympy as s

x,y,z,u=s.symbols('x y z u')
Y=(x,y,z)
checks=[]
def check(name, value):
    assert value, name
    checks.append(name)
def D(coef,F):
    return s.expand(sum(a*s.diff(F,v) for a,v in zip(coef,Y)))
def iterate(coef,F,n):
    for _ in range(n): F=D(coef,F)
    return F
def proj(coef,F,j,L):
    for i in range(L+1):
        if i!=j: F=s.expand((D(coef,F)-i*F)/s.Rational(j-i))
    return F
def C(n,v):
    if n==0:return s.Integer(2)
    a,b=s.Integer(2),v
    for _ in range(1,n):a,b=b,s.expand(v*b-a)
    return b

# A nontrivial polynomial coordinate system and its normal Euler field.
r=z-x*x
q=y-r*r
p=x-q*q
coef=(2*q*q,q+2*r*r,r+4*x*q*q)
coef=tuple(map(s.expand,coef))
check('positive_delta_p_zero',D(coef,p)==0)
check('positive_delta_q_weight_one',D(coef,q)==q.expand())
check('positive_delta_r_weight_one',D(coef,r)==r)
check('positive_divergence_two',s.expand(sum(s.diff(a,v) for a,v in zip(coef,Y)))==2)
gamma=(u,0,u*u)
check('positive_parameter',s.expand(p.subs(dict(zip(Y,gamma)),simultaneous=True))==u)
check('positive_normal_q',s.expand(q.subs(dict(zip(Y,gamma)),simultaneous=True))==0)
check('positive_normal_r',s.expand(r.subs(dict(zip(Y,gamma)),simultaneous=True))==0)

# A finite closure certificate, stronger than a finite string of successful numerical tests.
vec=[s.Integer(1)]
for f in Y:
    vec.extend(iterate(coef,f,n) for n in range(5))
nextvec=[iterate(coef,f,5) for f in Y]
monoms=sorted(set().union(*(set(s.Poly(f,*Y).monoms()) for f in vec+nextvec)))
def col(f):
    dd=s.Poly(f,*Y).as_dict()
    return s.Matrix([dd.get(m,0) for m in monoms])
M=s.Matrix.hstack(*(col(f) for f in vec))
rank=M.rank()
check('positive_exact_finite_closure',s.Matrix.hstack(M,*(col(f) for f in nextvec)).rank()==rank)
check('positive_projector_recovers_p',proj(coef,x,0,4)==p.expand())
check('positive_projector_recovers_q',proj(coef,y,1,4)==q.expand())
check('positive_projector_recovers_r',proj(coef,r,1,4)==r)
pp,qq,rr=s.symbols('p q r')
inverse=(pp+qq**2,qq+rr**2,rr+(pp+qq**2)**2)
check('positive_inverse',all(s.expand(f.subs(dict(zip(Y,inverse)),simultaneous=True)-v)==0 for f,v in zip((p,q,r),(pp,qq,rr))))

# This field passes divergence and fixed-scheme tests but has unbounded iteration degree.
bad=(y*z,y,z+y*y*x)
check('negative_divergence_two',sum(s.diff(a,v) for a,v in zip(bad,Y))==2)
check('negative_normal_y',bad[1]-y==0)
check('negative_normal_z',s.rem(s.Poly(bad[2]-z,y),s.Poly(y*y,y))==0)
gb=s.groebner(bad,x,y,z)
check('negative_fixed_ideal_exact',set(map(s.expand,gb.polys_to_expr()))=={y,z} if hasattr(gb,'polys_to_expr') else set(s.expand(f.as_expr()) for f in gb.polys)=={y,z})
growth=[]
for n in range(1,7):
    F=iterate(bad,x,2*n)
    coeff=s.Poly(F,*Y).coeff_monomial(x*y**(3*n))
    check('negative_nonzero_growth_'+str(n),coeff>0)
    growth.append({'n':n,'iterations':2*n,'degree':int(s.Poly(F,*Y).total_degree()),'witness_monomial':str(x*y**(3*n)),'witness_coefficient':str(coeff)})

# Check the divergence obstruction on important explicit parameter polynomials.
naive=[]
models=[((3,4,5),y*z-x**3+3*x),((3,7,8),y*z-C(5,x)),((4,5,7),(x*x-2)*z-y**3+3*y)]
for indices,P in models:
    curve=[C(i,u) for i in indices]
    check('naive_parameter_'+str(indices),s.expand(P.subs(dict(zip(Y,curve)),simultaneous=True))==u)
    coeff=[s.expand(v-C(i,P)) for v,i in zip(Y,indices)]
    div=s.expand(sum(s.diff(a,v) for a,v in zip(coeff,Y)))
    check('naive_nonconstant_divergence_'+str(indices),s.Poly(div,*Y).total_degree()>0)
    naive.append({'indices':indices,'parameter_degree':int(s.Poly(P,*Y).total_degree()),'divergence_degree':int(s.Poly(div,*Y).total_degree())})

out={'status':'PASS','arithmetic':'exact rational','sympy':s.__version__,'checks':checks,'positive_closure_dimension':rank,'negative_growth':growth,'naive_divergence':naive,'scope':'Finite examples verify formulas. Universal statements require theory.md.'}
target=Path(__file__).with_name('theory_checks.json')
target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS',len(checks),'exact named checks; finite stable space dimension',rank)
print(target)
