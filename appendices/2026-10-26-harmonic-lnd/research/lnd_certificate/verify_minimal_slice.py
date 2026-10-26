#!/usr/bin/env python3
"""Independent exact certificate: minimum total degree of a slice is seven.

Python standard library only. No source rectifier or matrix solver is needed.
The dual certificate is rational, hence remains valid over every char-zero field.
Variable order is (B,u,x,y,z). All exponent tuples are ordinary total degree.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
data = json.loads((HERE/"no_slice_degree6_certificate.json").read_text())
weights = {tuple(e["monomial"]):Fraction(e["coefficient"])
           for e in data["dual_witness"]}
zero = (0,0,0,0,0)

def D_monomial(mon):
    B,u,x,y,z = mon
    result = {}
    def add(key,value):
        result[key] = result.get(key,Fraction(0))+value
    if u:
        add((B+1,u-1,x,y,z),u)
    if x:
        add((B,u+2,x-1,y,z),3*x)
        add((B,u,x-1,y,z),-3*x)
    if y:
        add((B,u+3,x,y-1,z),4*y)
        add((B,u+1,x,y-1,z),-8*y)
    if z:
        add((B,u+4,x,y,z-1),5*z)
        add((B,u,x,y,z-1),-10*z)
    return {k:v for k,v in result.items() if v}

bound = data["input_degree_bound"]
if bound != 6:
    raise AssertionError("The certificate must address all degrees <= 6")
count = 0
for mon in product(range(bound+1),repeat=5):
    if sum(mon)>bound:
        continue
    image = D_monomial(mon)
    value = sum(weights.get(key,Fraction(0))*coefficient
                for key,coefficient in image.items())
    if value != 0:
        raise AssertionError((mon,value))
    count += 1
if count != 462 or weights.get(zero,Fraction(0)) != 1:
    raise AssertionError("Bad basis size or bad normalization")
print("PASS: ell(D(m))=0 for every one of the 462 monomials of degree <= 6")
print("PASS: ell(1)=1; hence no polynomial slice of degree <= 6 exists")

# This explicit sigma is independent of the nonlinear source rectifier.
sigma = {
    (0,6,1,0,0):-3, (0,4,1,0,0):13, (0,2,1,0,0):-7,
    (0,0,1,0,0):-7, (0,5,0,1,0):1, (0,3,0,1,0):-5,
    (0,1,0,1,0):5, (0,4,0,0,1):1, (0,2,0,0,1):-4,
    (0,0,0,0,1):2, (1,3,2,0,0):3, (1,1,2,0,0):-9,
    (1,0,1,1,0):5, (1,0,0,1,1):-1, (2,0,3,0,0):-1,
}
image = {}
for mon,c in sigma.items():
    for out,d in D_monomial(mon).items():
        image[out]=image.get(out,Fraction(0))+c*d
image={k:v for k,v in image.items() if v}
if image != {zero:1}:
    raise AssertionError(image)
degree = max(map(sum,sigma))
if degree != 7:
    raise AssertionError(degree)
print("PASS: the 15-monomial sigma has total degree 7 and D(sigma)=1")
print("CERTIFIED: minimum total degree of a slice is exactly 7")
