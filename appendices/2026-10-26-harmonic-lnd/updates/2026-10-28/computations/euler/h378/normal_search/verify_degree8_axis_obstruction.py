#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Verify the invariant-axis certificate excluding the chosen H(3,7,8) representative.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Exact invariant-axis obstruction for the displayed degree-eight field.

This is an all-iterations proof, not a finite iteration experiment.
It makes no assertion about other members of the affine solution space.
"""
from pathlib import Path
import json
import sympy as s

ROOT=Path(__file__).resolve().parent
x,y,z=s.symbols('x y z'); V=(x,y,z)
data=json.loads((ROOT/'normal_degree_8.json').read_text())
field=[s.expand(sum(s.Rational(t['coefficient'])*s.prod(v**e for v,e in zip(V,t['exp']))
                   for t in terms)) for terms in data['field']]
axis=[s.expand(p.subs({x:0,y:0})) for p in field]
assert axis[0]==axis[1]==0
a=s.Poly(axis[2],z); degree=a.degree(); leading=a.LC()
assert degree==6 and leading==s.Rational(15301939053253624082,123929566826253428317)
assert a.eval(2)==0 and s.diff(a.as_expr(),z).subs(z,2)==1
# On the invariant quotient Q[z], D=a(z)*d/dz. If deg f=m>=1,
# deg Df=m+5, and LC(Df)=m*leading*LC(f). Induction is exact.
certificate={
 'status':'EXACT_INVARIANT_AXIS_OBSTRUCTION_PASS',
 'field_certificate':'normal_degree_8.json',
 'invariant_ideal':['x','y'],
 'quotient_field':str(s.factor(a.as_expr())),
 'degree':degree,'leading_coefficient':str(leading),
 'all_iteration_formula':{'degree_Dn_z':'1+5*n',
   'leading_coefficient_Dn_z':'leading_coefficient**n * product(1+5*j, j=0..n-1)'},
 'conclusion':'The displayed particular field is not locally finite; its homogeneous E is not locally nilpotent.',
 'scope':'No conclusion about other fields in the 24-dimensional affine solution space or about rectifiability.'}
(ROOT/'degree8_axis_obstruction.json').write_text(json.dumps(certificate,ensure_ascii=False,indent=2)+'\n')
print(certificate['status'])
print('deg(D^n z)=1+5n for every integer n>=0; hence not locally finite.')

# A separate scope check: the full affine family need not preserve the axis.
if 'homogeneous_basis_coefficients' in data:
    count=len(data['basis'])
    basis_axis=[sum(s.Rational(t['coefficient'])*z**t['exp'][2] for t in terms
                    if t['exp'][0]==t['exp'][1]==0) for terms in data['basis']]
    witnesses=[]
    for j,vector in enumerate(data['homogeneous_basis_coefficients']):
        restricted=[s.Integer(0)]*3
        for entry in vector:
            i=entry['index']
            restricted[i//count]+=s.Rational(entry['coefficient'])*basis_axis[i%count]
        restricted=[s.factor(p) for p in restricted]
        if restricted[0]!=0 or restricted[1]!=0:
            witnesses.append({'direction':j,'axis_x':str(restricted[0]),'axis_y':str(restricted[1])})
    assert len(witnesses)==13
    family={'status':'EXACT_AXIS_FAMILY_TEST_PASS','all_directions_preserve_axis':False,
      'directions_not_preserving_axis':len(witnesses),'total_directions':len(data['homogeneous_basis_coefficients']),
      'first_witness':witnesses[0],
      'scope':'The invariant-axis obstruction for the displayed particular solution does not apply to the full affine family.'}
    (ROOT/'degree8_family_axis_test.json').write_text(json.dumps(family,indent=2)+'\n')
    print('EXACT_AXIS_FAMILY_TEST_PASS: 13 of 24 displayed directions fail to preserve (x,y).')
