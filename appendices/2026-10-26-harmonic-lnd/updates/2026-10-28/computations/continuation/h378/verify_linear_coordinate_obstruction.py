#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Check the stated relative-coordinate obstruction for the H(3,7,8) model.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Exact identities behind two infinite-class obstructions for H(3,7,8).

The proof of nonexistence for all degrees is in linear_coordinate_obstruction.md.
This script certifies the algebraic identities, including polynomial-factor and
sign certificates. It does not infer nonrectifiability of the curve.
"""
from pathlib import Path
import json
import sys

try:
    import sympy as S
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "python_deps"))
    import sympy as S

x, t = S.symbols("x t")
C = lambda n, variable: S.expand(2 * S.chebyshevt(n, variable / 2))
relation = t**3 - 3*t - x
reduce_t = lambda p: S.rem(S.expand(p), relation, t)
k = x**2 - 1
delta = x**4 - 3*x**2 + 1
E6 = x**6 - 5*x**4 + 6*x**2 - 1
E7 = x**7 - 6*x**5 + 10*x**3 - 4*x
s = t**2 - 2
y = k*t - x*s
z = -x*t + k*s

checks = {}
def check(name, expression):
    reduced = S.expand(expression)
    assert reduced == 0, (name, reduced)
    checks[name] = True

check("C7_module_expression", reduce_t(C(7,t) - y))
check("C8_module_expression", reduce_t(C(8,t) - z))
check("C7_square", reduce_t(y**2 - (2 + x*(2-x**2)*t + delta*s)))
check("C8_square", reduce_t(z**2 - (2 + x*k*(k-2)*t - delta*s)))
check("C7_projection_relation", reduce_t(y**3 - 3*y - C(7,x)))
check("C8_projection_relation", reduce_t(z**3 - 3*z - C(8,x)))
check("first_elimination_coefficient", x**2*(2-x**2) + k*delta - E6)
check("second_elimination_coefficient", x*(k**2*(k-2)-delta) - E7)

f_plus_value = x**3 - x**2 - 2*x + 1
f_minus_value = x**3 + x**2 - 2*x - 1
check("E6_factorization", E6 - f_plus_value*f_minus_value)
check("positive_delta_factor", delta-x-(x+1)*f_plus_value)
check("negative_delta_factor", delta+x-(x-1)*f_minus_value)
endpoint_signs = {
    "f_plus_value_at_1": int(f_plus_value.subs(x,1)),
    "f_plus_value_at_2": int(f_plus_value.subs(x,2)),
    "f_minus_value_at_1": int(f_minus_value.subs(x,1)),
    "f_minus_value_at_2": int(f_minus_value.subs(x,2)),
}
assert endpoint_signs == {
    "f_plus_value_at_1": -1, "f_plus_value_at_2": 1,
    "f_minus_value_at_1": -1, "f_minus_value_at_2": 7,
}

r = S.sqrt(2)
alpha = S.sqrt(2 + S.sqrt(2))
for name, value, target in [("sqrt2", r, -1), ("sqrt_2_plus_sqrt2", alpha, 1)]:
    assert S.simplify(E7.subs(x,value)) == 0
    assert S.simplify(delta.subs(x,value)) != 0
    assert S.simplify((k-target*delta).subs(x,value)) == 0
    checks["second_projection_value_"+name] = True

out = {
    "model": [3,7,8],
    "normalization": "C_n(t)=2*T_n(t/2)",
    "field": "C (hence any characteristic-zero subfield)",
    "checks": checks,
    "first_projection_sign_certificate": endpoint_signs,
    "identities": {
        "first": "U_6(x/2)*A(x) + U_4(x/2)*M(x) = x",
        "second": "U_7(x/2)*A(x) + U_4(x/2)*M(x) = x^2-1",
    },
    "conclusion": "No k[x]-coordinate lifting t has either form Q(x,y)+M(x)z or Q(x,z)+M(x)y, with arbitrary polynomial Q,M.",
    "limitation": "Does not exclude nonlinear dependence on both y,z, changing x, or arbitrary polynomial rectification.",
}
dest = Path(__file__).with_name("linear_coordinate_obstruction.json")
dest.write_text(json.dumps(out, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print(json.dumps({"passed":len(checks), "certificate":str(dest)}, ensure_ascii=False))
