# Consolidated verification copy, 28 October 2026.
# Purpose: Verify the polynomial Chebyshev shears that transfer the established base rectifications.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Exact certificates for Chebyshev fixed-projection shear equivalence.

C_n(t)=2*T_n(t/2), C_0=2, C_1=t.  This script proves identities
only; it does not claim a general rectification algorithm.
"""
from functools import lru_cache
from math import gcd
import json
from pathlib import Path
import sympy as s

t,x,y=s.symbols('t x y')

@lru_cache(None)
def C(n):
    if n==0: return s.Poly(2,t,domain=s.QQ)
    if n==1: return s.Poly(t,t,domain=s.QQ)
    return s.Poly(t,t)*C(n-1)-C(n-2)

def membership_certificate(a,b,f):
    """Return P and gap remainder with f=P(C_a,C_b)+remainder."""
    ca,cb=C(a),C(b)
    f=s.Poly(f,t,domain=s.QQ)
    out=s.Integer(0); rem=s.Poly(0,t,domain=s.QQ)
    b_inv=pow(b,-1,a)
    while not f.is_zero:
        d=f.degree(); coeff=f.LC()
        j=(d*b_inv)%a; i=(d-b*j)//a
        if i>=0:
            f-=coeff*ca**i*cb**j
            out+=coeff*x**i*y**j
        else:
            term=s.Poly(coeff*t**d,t,domain=s.QQ)
            rem+=term; f-=term
    return s.expand(out),rem

def check(a,b,c,cp,sgn):
    target=C(cp)-sgn*C(c)
    p,rem=membership_certificate(a,b,target)
    assert rem.is_zero,(a,b,c,cp,sgn,rem)
    substitution=s.Poly(p.subs({x:C(a).as_expr(),y:C(b).as_expr()},simultaneous=True),t)
    assert (substitution-target).is_zero
    return p

def signs(a,b,c,cp):
    return [(ea,eb) for ea in (1,-1) for eb in (1,-1)
            if (cp-ea*c)%(2*a)==0 and (cp-eb*c)%(2*b)==0]

def main():
    # A tempting birational reduction and its exact fibre obstruction.
    r=s.symbols('r')
    assert ((C(3)**2-2)*C(8)-C(7)**2+2-C(2)).is_zero
    rem7=s.rem(C(7).as_expr(),C(3).as_expr()-r,t)
    assert s.expand(rem7-(-r*t**2+(r**2-1)*t+2*r))==0
    residue_checks=0
    for n in range(11):
        vn=s.chebyshevu(n,r/2).expand()
        vp=s.chebyshevu(n-1,r/2).expand() if n else s.Integer(0)
        for degree,expected in [(3*n+1,-vp*t**2+vn*t+2*vp),
                                (3*n+2,vn*t**2-vp*t-2*vn)]:
            actual=s.rem(C(degree).as_expr(),C(3).as_expr()-r,t)
            assert s.expand(actual-expected)==0
            residue_checks+=1
    examples=[]
    for a,b,c,cp in [(3,4,1,7),(3,4,5,11),(3,4,5,29),
                     (3,5,1,11),(3,5,4,14),(3,5,7,13),
                     (5,7,3,73),(5,7,11,81),(7,9,11,137)]:
        ea,eb=signs(a,b,c,cp)[0]
        p=check(a,b,c,cp,ea*eb)
        examples.append(dict(a=a,b=b,c=c,cp=cp,sign=ea*eb,P=str(p)))
    count=0
    # All compatible residue classes up to degree 40 for these fixed pairs.
    for a,b in [(2,3),(3,4),(3,5),(4,5),(3,7),(5,7)]:
        for c in range(1,21):
            if gcd(c,a*b)!=1: continue
            for cp in range(c+1,41):
                sig=signs(a,b,c,cp)
                if not sig: continue
                check(a,b,c,cp,sig[0][0]*sig[0][1]); count+=1
    result=dict(normalization='C_n(t)=2*T_n(t/2)',
                verified_residue_shears=count,examples=examples,
                birational_reduction_H378='(C3^2-2)*C8-C7^2+2=C2',
                verified_general_cubic_residues=residue_checks,
                remainder_C7_mod_C3_minus_r=str(rem7),
                graph_center_obstruction='r^2=2 and lambda != 0 imply lambda*r != 0')
    Path(__file__).with_name('periodic_shears_results.json').write_text(
        json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
