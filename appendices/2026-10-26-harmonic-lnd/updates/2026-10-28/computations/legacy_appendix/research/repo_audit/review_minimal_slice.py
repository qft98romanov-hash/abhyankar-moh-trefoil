# Consolidated verification copy, 28 October 2026.
# Purpose: Independently check the degree-six exclusion functional and upper slice.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Independent exact review of the supplied dual obstruction and upper slice.
Uses no SymPy, no imported verifier, and no linear-equation solver.
"""
from fractions import Fraction
from itertools import product
from math import comb
from pathlib import Path
import ast
import hashlib
import json

folder=Path(__file__).resolve().parents[1]/'lnd_certificate'
certificate=json.loads((folder/'no_slice_degree6_certificate.json').read_text())
slice_data=json.loads((folder/'minimal_degree_slice.json').read_text())
names=('B','u','x','y','z')
assert certificate['variables']==list(names)
weights={tuple(row['monomial']):Fraction(row['coefficient']) for row in certificate['dual_witness']}
assert len(weights)==len(certificate['dual_witness'])==31
assert all(len(mon)==5 and min(mon)>=0 for mon in weights)
zero=(0,)*5
assert weights[zero]==1

# Construct derivation images by the product rule from the FIVE generator images.
generator_images=(
 {},
 {(1,0,0,0,0):1},
 {(0,2,0,0,0):3, zero:-3},
 {(0,3,0,0,0):4, (0,1,0,0,0):-8},
 {(0,4,0,0,0):5, zero:-10},
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

inputs=[m for m in product(range(7),repeat=5) if sum(m)<=6]
assert len(inputs)==comb(11,5)==462==certificate['input_monomial_count']
output_support=set()
max_image_degree=0
for mon in inputs:
    image=derivative_monomial(mon)
    output_support.update(image)
    max_image_degree=max(max_image_degree,max(map(sum,image),default=0))
    value=sum(Fraction(coef)*weights.get(term,0) for term,coef in image.items())
    if value: raise AssertionError((mon,value))
assert len(output_support)==certificate['output_monomial_count']==812
assert max_image_degree==9

upper={ast.literal_eval(mon):Fraction(coef) for mon,coef in slice_data['coefficients'].items()}
assert max(map(sum,upper))==7
upper_image={}
for mon,coef in upper.items():
    for term,dcoef in derivative_monomial(mon).items():
        upper_image[term]=upper_image.get(term,0)+coef*dcoef
upper_image={m:c for m,c in upper_image.items() if c}
assert upper_image=={zero:Fraction(1)}

result={
 'input_monomials':len(inputs),
 'output_monomials':len(output_support),
 'max_output_degree':max_image_degree,
 'dual_support':len(weights),
 'dual_value_on_one':str(weights[zero]),
 'all_dual_values_on_images_zero':True,
 'upper_slice_terms':len(upper),
 'upper_slice_degree':7,
 'upper_derivative_is_one':True,
 'minimal_total_degree':7,
 'valid_over':'Every characteristic-zero field, including C',
 'witness_sha256':hashlib.sha256((folder/'no_slice_degree6_certificate.json').read_bytes()).hexdigest(),
}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
print('INDEPENDENT MINIMAL-SLICE CERTIFICATE REVIEW PASSED')
