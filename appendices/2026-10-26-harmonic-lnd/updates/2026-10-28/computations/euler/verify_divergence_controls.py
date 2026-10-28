#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Check why constant divergence and the fixed-point ideal do not suffice for local finiteness.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Exact controls; all-n proofs are in literature.md. Requires SymPy."""
import json
from pathlib import Path
import sympy as s

x, y, z, t, q, r = s.symbols("x y z t q r")

def apply(coefficients, variables, polynomial):
    return s.expand(sum(a * s.diff(polynomial, v) for a, v in zip(coefficients, variables)))

weak = (0, y + y**2, z - 2*y*z)
strong = (y*z, y, z+y**2*x)
E = (1, q**2, -2*q*r)
checks = []
for name, vector in [("weak", weak), ("strong", strong)]:
    div = sum(s.diff(a, v) for a, v in zip(vector, (x, y, z)))
    assert div == 2
    assert all(s.sympify(a).subs({y: 0, z: 0}) == 0 for a in vector)
    for remainder in (vector[1]-y, vector[2]-z):
        if remainder != 0:
            assert all(sum(m[1:]) >= 2 for m in s.Poly(remainder,x,y,z).monoms())
    checks.append({"field": name, "divergence": str(div), "normal_jet_verified": True})

a, b = y, q
for n in range(1, 11):
    a = apply(weak, (x,y,z), a)
    b = apply(E, (t,q,r), b)
    assert s.degree(a,y) == n+1
    assert s.Poly(a,y).LC() == s.factorial(n)
    assert b == s.factorial(n)*q**(n+1)
    checks.append({"n": n, "weak_iterate_degree": n+1, "weak_leading_coefficient": str(s.factorial(n)), "E_iterate_formula_verified": True})

c = x
strong_rows = []
for n in range(1, 7):
    c = apply(strong, (x,y,z), apply(strong, (x,y,z), c))
    poly = s.Poly(c, x,y,z)
    witness = poly.coeff_monomial(x*y**(3*n))
    assert witness > 0
    assert all(value > 0 for value in poly.coeffs())
    strong_rows.append({"iteration": 2*n, "witness": f"x*y**{3*n}", "witness_coefficient": str(witness), "total_degree": poly.total_degree()})

ideal = s.groebner(strong, x,y,z)
assert list(ideal) == [y,z]
report = {
    "date": "2026-10-28", "arithmetic": "exact over Q",
    "scope": "finite verification; all-n non-local-finiteness is proved separately in literature.md",
    "checks": checks,
    "strong_counterexample": {
        "field": [str(a) for a in strong],
        "coefficient_ideal_reduced_groebner_basis": [str(a) for a in ideal],
        "even_iterates": strong_rows,
    },
}
out = Path(__file__).with_name("divergence_controls.json")
out.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n")
print(f"PASS: divergence/normal jet; ten weak iterates, ten E iterates; six strong even iterates; fixed ideal (y,z). Saved {out.name}.")
