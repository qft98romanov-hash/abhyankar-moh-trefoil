#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Check the exact lower-bound witness and degree-eleven harmonic upper slice.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Exact autonomous certificate: harmonic H(3,5,7) LND slices have degree >=11.

Python standard library only. All 3003 monomials of total degree <=10 are
checked, including every weight. The upper slice has 27 terms and degree 11.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
ZERO=(0,0,0,0,0)
ONE={ZERO:Fraction(1)}

def variable(j):
    m=[0]*5;m[j]=1
    return {tuple(m):Fraction(1)}

B,u,x,y,z=[variable(j) for j in range(5)]

def add(*polys):
    out={}
    for p in polys:
        for mon,c in p.items():out[mon]=out.get(mon,Fraction(0))+c
    return {m:c for m,c in out.items() if c}

def scale(p,c):
    return {m:Fraction(c)*v for m,v in p.items() if c*v}

def mul(p,q):
    out={}
    for m,c in p.items():
        for n,d in q.items():
            mn=tuple(i+j for i,j in zip(m,n))
            out[mn]=out.get(mn,Fraction(0))+c*d
    return {m:c for m,c in out.items() if c}

def partial(p,j):
    out={}
    for m,c in p.items():
        if m[j]:
            n=list(m);n[j]-=1
            out[tuple(n)]=c*m[j]
    return out

C=[scale(ONE,2),u]
for n in range(2,8):C.append(add(mul(u,C[-1]),scale(C[-2],-1)))
f,g,h=C[3],C[5],C[7]
fps=[partial(p,1) for p in (f,g,h)]

def D_monomial(mon):
    p={mon:Fraction(1)}
    return add(mul(B,partial(p,1)),
               *(mul(fp,partial(p,j+2)) for j,fp in enumerate(fps)))

certificate=json.loads((HERE/"no_harmonic_slice_degree10_certificate.json").read_text())
if certificate["input_degree_bound"]!=10:
    raise AssertionError("The bound must be ten")
weights={tuple(e["monomial"]):Fraction(e["coefficient"])
         for e in certificate["dual_witness"]}
count=0
for mon in product(range(11),repeat=5):
    if sum(mon)>10:continue
    value=sum(weights.get(m,Fraction(0))*c for m,c in D_monomial(mon).items())
    if value:
        raise AssertionError((mon,value))
    count+=1
if count!=3003 or weights.get(ZERO,Fraction(0))!=1:
    raise AssertionError("Wrong basis size or normalization")
print("PASS: ell(D(m))=0 on all 3003 monomials of total degree <=10")
print("PASS: ell(1)=1; no slice of total degree <=10 exists over any char-zero field")

# Check the compact cubic parameter retraction and its induced slice.
retraction_on_curve=add(mul(mul(f,f),h),scale(mul(f,mul(g,g)),-1),scale(f,2),scale(h,-1))
if retraction_on_curve!=u:
    raise AssertionError("Cubic retraction fails")
sigma=add(
    mul(add(scale(mul(f,h),2),scale(mul(g,g),-1),scale(ONE,2)),x),
    scale(mul(mul(f,g),y),-2),
    mul(add(mul(f,f),scale(ONE,-1)),z),
    mul(B,add(mul(f,mul(y,y)),scale(mul(f,mul(x,z)),-2),
              scale(mul(g,mul(x,y)),2),scale(mul(h,mul(x,x)),-1))),
    mul(mul(B,B),add(mul(mul(x,x),z),scale(mul(x,mul(y,y)),-1)))
)
searched=json.loads((HERE/"harmonic_slice_search.json").read_text())
found={tuple(e["monomial"]):Fraction(e["coefficient"]) for e in searched["coefficients"]}
if sigma!=found:
    raise AssertionError("Compact formula differs from the recorded coefficients")
image=add(*(scale(D_monomial(mon),c) for mon,c in sigma.items()))
if image!=ONE or len(sigma)!=27 or max(map(sum,sigma))!=11:
    raise AssertionError((image,len(sigma),max(map(sum,sigma))))
print("PASS: R_H(gamma(u))=u for R_H=x^2*z-x*y^2+2*x-z")
print("PASS: compact sigma_H matches all 27 recorded coefficients, has degree 11, and D(sigma_H)=1")
print("CERTIFIED: minimum total degree of a harmonic H(3,5,7) slice is exactly 11")
