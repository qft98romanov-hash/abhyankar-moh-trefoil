#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Independently differentiate the explicit slices and check the uniqueness minor.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Independent SymPy audit: explicit slices, direct derivatives, degree profiles.

Does not import either the jet search or its Fraction verifier.
"""
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "python_deps"))
import sympy as s

t, u, X, Y, Z = s.symbols("t u X Y Z")
x, y, z = s.symbols("x y z")
ambient = (t, u, X, Y, Z)
parameters = (x, y, z)
normal = (X, Y, Z)

def C(n, arg):
    return s.expand(2 * s.chebyshevt(n, arg / 2))

def evaluate(P, values):
    return s.expand(P.subs(dict(zip(parameters, values)), simultaneous=True))

def jet_degree(P, gamma, mu):
    r = s.Poly(P, *parameters).total_degree()
    terms = []
    for a in range(r + 1):
        for b in range(r + 1 - a):
            for c in range(r + 1 - a - b):
                q = a + b + c
                if not q:
                    continue
                derivative = s.diff(P, x, a, y, b, z, c)
                value = evaluate(derivative, gamma)
                if value != 0:
                    terms.append(s.degree(value, u) + (mu + 1) * q - mu)
    return int(max(terms))

P457 = (x*x - 2)*z - y**3 + 3*y
P378_5 = y*z - C(5, x)
P378_4 = x**3*z + x**3 - x*x*y*z - x*y*y - 2*x*z - x + y**3 + 2*y*z - 2*y
results = []

for name, triple, P in [
    ("H457_P3", (4, 5, 7), P457),
    ("H378_P5", (3, 7, 8), P378_5),
    ("H378_P4", (3, 7, 8), P378_4),
]:
    gamma = tuple(C(n, u) for n in triple)
    f, g, h = gamma
    assert evaluate(P, gamma) == u
    profiles = []
    for mu in range(1, 10):
        numerator = s.Poly(u - evaluate(P, [v - t**mu * w for v, w in zip(gamma, normal)]), *ambient)
        assert all(monomial[0] >= mu for monomial, coeff in numerator.terms())
        S = s.Poly.from_dict({(a-mu, b, c, d, e): coeff
                             for (a, b, c, d, e), coeff in numerator.terms()}, ambient).as_expr()
        DS = t**mu*s.diff(S, u) + sum(s.diff(v, u)*s.diff(S, w) for v, w in zip(gamma, normal))
        assert s.expand(DS) == 1
        degree = s.Poly(S, *ambient).total_degree()
        assert degree == jet_degree(P, gamma, mu)
        if name == "H457_P3":
            explicit = (2*f*h)*X + (3-3*g*g)*Y + (f*f-2)*Z + t**mu*(-h*X*X-2*f*X*Z+3*g*Y*Y) + t**(2*mu)*(X*X*Z-Y**3)
            assert s.expand(S - explicit) == 0
        if name == "H378_P5":
            explicit = h*Y + g*Z - t**mu*Y*Z
            explicit += sum((-1)**q/s.factorial(q)*t**(mu*(q-1))*s.diff(C(5, x), x, q).subs(x, f)*X**q for q in range(1, 6))
            assert s.expand(S - explicit) == 0
        profiles.append({"mu": mu, "degree": int(degree), "terms": len(s.Poly(S, *ambient).terms())})
        if mu == 1:
            (HERE / (name + "_expanded_slice.txt")).write_text(str(s.expand(S)) + "\n")
    results.append({"case": name, "parameter_degree": int(s.Poly(P, *parameters).total_degree()), "profile": profiles})

assert [e["degree"] for e in results[0]["profile"]] == [12,12,12,13,14,15,17,19,21]
assert [e["degree"] for e in results[1]["profile"]] == [13,13,17,21,25,29,33,37,41]
assert [e["degree"] for e in results[2]["profile"]] == [19,19,20,21,22,23,25,28,31]
assert results[0]["profile"][0]["terms"] == results[1]["profile"][0]["terms"] == 29

# An independent certificate that P457 is the ONLY parameter polynomial of
# degree at most three.  Lower degree is impossible since its top u-degrees
# are distinct and all nonconstant ones exceed one.
monomials = [(i, j, k) for i in range(4) for j in range(4-i) for k in range(4-i-j)]
gamma457 = tuple(C(n, u) for n in (4, 5, 7))
values = [s.Poly(s.prod(v**a for v, a in zip(gamma457, beta)), u) for beta in monomials]
evaluation_minor = s.Matrix([[p.nth(j) for p in values] for j in range(20)])
assert evaluation_minor.det() == 267386
lower_top_degrees = sorted(4*i+5*j+7*k for i, j, k in monomials if i+j+k <= 2)
assert lower_top_degrees == [0,4,5,7,8,9,10,11,12,14]

out = {"status": "PASS", "independence": "SymPy chebyshevt, substitution, and differentiation; no imports from searched or reviewed implementation", "slices_checked": 27, "results": results,
       "H457_unique_degree_three_parameter_certificate": {
           "monomial_order": [list(a) for a in monomials],
           "minor_u_degrees": list(range(20)), "determinant": "267386",
           "degree_at_most_two_distinct_top_u_degrees": lower_top_degrees},
       "H457_all_multiplicities_consequence": "m(mu)=max(12,mu+9,2*mu+3), mu>=1; proof in review_jet.md"}
(HERE / "review_jet_checks.json").write_text(json.dumps(out, indent=2) + "\n")
print("PASS: 27 exact slices; DS=1, Taylor jet degree, and explicit H457/H378 formulas independently checked.")
