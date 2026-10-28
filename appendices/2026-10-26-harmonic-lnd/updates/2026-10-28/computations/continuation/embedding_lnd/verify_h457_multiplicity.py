#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Check the determinant witness and upper slices supporting the all-multiplicity argument.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Exact elementary certificate for the all-multiplicities H(4,5,7) formula.

Checks injectivity of restriction on polynomials of degree <=3 by a
nonzero 20x20 integer minor, and literally verifies selected upper slices.
The proof for all multiplicities is in PROOF.md, section 7.1.
"""
from pathlib import Path
import json
from verify_jet_certificates import cn, times, verify_upper

HERE=Path(__file__).resolve().parent
cs=[cn(n) for n in (4,5,7)]
mons=[(i,j,k) for i in range(4) for j in range(4-i) for k in range(4-i-j)]
polys=[]
for alpha in mons:
    p=[1]
    for f,n in zip(cs,alpha):
        for _ in range(n):p=times(p,f)
    polys.append(p)
matrix=[[int(p[i]) if i<len(p) else 0 for p in polys] for i in range(20)]
a=[row[:] for row in matrix]
prev=1;sign=1
for k in range(19):
    row=next(i for i in range(k,20) if a[i][k])
    if row!=k:a[k],a[row]=a[row],a[k];sign=-sign
    pivot=a[k][k]
    for i in range(k+1,20):
        for j in range(k+1,20):
            num=a[i][j]*pivot-a[i][k]*a[k][j]
            assert num%prev==0
            a[i][j]=num//prev
        a[i][k]=0
    prev=pivot
det=sign*a[-1][-1]
assert det==267386
print('CERTIFIED H457: degree <=3 restriction minor determinant = 267386')
for mu in list(range(1,13))+[25,100]:
    upper=verify_upper((4,5,7),max(12,mu+9,2*mu+3),mu)
    assert upper['retraction_degree']==3
    print('UPPER VERIFIED mu =',mu,'degree =',upper['slice_degree'])
(HERE/'h457_unique_cubic_parameter.json').write_text(json.dumps({'triple':[4,5,7],'degree_bound':3,'row_u_degrees':list(range(20)),'columns_monomials':mons,'matrix':matrix,'determinant':det,'unique_parameter':'(x^2-2)*z-y^3+3*y','minimum_slice_degree_all_mu':'max(12,mu+9,2*mu+3)','proof':'PROOF.md section 7.1'},indent=2)+'\n')
print('ALL H457 MULTIPLICITY CHECKS PASSED')
