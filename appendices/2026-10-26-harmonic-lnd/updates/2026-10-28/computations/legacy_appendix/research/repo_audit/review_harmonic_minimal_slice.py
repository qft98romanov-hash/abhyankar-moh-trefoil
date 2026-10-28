# Consolidated verification copy, 28 October 2026.
# Purpose: Independently check the degree-ten exclusion functional and harmonic upper slice.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Independent harmonic slice minimum11 certificate check.
No symbolic algebra library or imported source verifier is used.
All monomials of totaldegree<=10 are checked, not just a weight subspace.
"""
from fractions import Fraction
from itertools import product
from math import comb
from pathlib import Path
import hashlib
import json

folder=Path(__file__).resolve().parents[1]/'lnd_certificate'
witness_file=folder/'no_harmonic_slice_degree10_certificate.json'
upper_file=folder/'harmonic_slice_search.json'
certificate=json.loads(witness_file.read_text())
slice_data=json.loads(upper_file.read_text())
names=['B','u','x','y','z']
assert certificate['variables']==slice_data['variables']==names
zero=(0,)*5
weights={tuple(row['monomial']):Fraction(row['coefficient']) for row in certificate['dual_witness']}
assert len(weights)==len(certificate['dual_witness'])==117
assert all(len(mon)==5 and min(mon)>=0 for mon in weights)
assert weights[zero]==1

# Independently hand-differentiated C3,C5,C7.
generator_images=(
 {},
 {(1,0,0,0,0):1},
 {(0,2,0,0,0):3, zero:-3},
 {(0,4,0,0,0):5, (0,2,0,0,0):-15, zero:5},
 {(0,6,0,0,0):7, (0,4,0,0,0):-35, (0,2,0,0,0):42, zero:-7},
)
def derivative_monomial(mon):
    result={}
    for variable,exponent in enumerate(mon):
        if not exponent: continue
        shortened=list(mon); shortened[variable]-=1
        for dmon,coefficient in generator_images[variable].items():
            new=tuple(a+b for a,b in zip(shortened,dmon))
            result[new]=result.get(new,0)+exponent*coefficient
    return {mon:coef for mon,coef in result.items() if coef}

inputs=[m for m in product(range(11),repeat=5) if sum(m)<=10]
assert len(inputs)==comb(15,5)==3003
weight_count=sum(m[0]-sum(m[2:])==-1 for m in inputs)
assert weight_count==240==certificate['weight_reduced_input_count']
output_support=set()
max_image_degree=0
for mon in inputs:
    image=derivative_monomial(mon)
    output_support.update(image)
    max_image_degree=max(max_image_degree,max(map(sum,image),default=0))
    value=sum(Fraction(coef)*weights.get(term,0) for term,coef in image.items())
    if value: raise AssertionError((mon,value))
assert max_image_degree==15

upper={tuple(row['monomial']):Fraction(row['coefficient']) for row in slice_data['coefficients']}
assert len(upper)==len(slice_data['coefficients'])==27
assert max(map(sum,upper))==11
upper_image={}
for mon,coef in upper.items():
    for term,dcoef in derivative_monomial(mon).items():
        upper_image[term]=upper_image.get(term,0)+coef*dcoef
upper_image={m:c for m,c in upper_image.items() if c}
assert upper_image=={zero:Fraction(1)}

result={
 'input_monomials':len(inputs),
 'weight_minus_one_input_monomials':weight_count,
 'output_monomials':len(output_support),
 'max_output_degree':max_image_degree,
 'dual_support':len(weights),
 'dual_value_on_one':str(weights[zero]),
 'all_dual_values_on_images_zero':True,
 'upper_slice_terms':len(upper),
 'upper_slice_degree':11,
 'upper_derivative_is_one':True,
 'minimal_total_degree':11,
 'valid_over':'Every characteristic-zero field, including C',
 'witness_sha256':hashlib.sha256(witness_file.read_bytes()).hexdigest(),
 'upper_sha256':hashlib.sha256(upper_file.read_bytes()).hexdigest(),
}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
print('INDEPENDENT HARMONIC MINIMAL-SLICE CERTIFICATE REVIEW PASSED')
