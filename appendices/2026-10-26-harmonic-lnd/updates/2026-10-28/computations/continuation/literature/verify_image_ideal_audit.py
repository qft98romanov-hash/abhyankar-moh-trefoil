# Consolidated verification copy, 28 October 2026.
# Purpose: Independently check explicit preimages used by the image-ideal formula.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Independent exact stress checks for the image-ideal formula.

These checks certify selected explicit preimages, not the universal theorem.
Run from any directory: python verify_image_ideal_audit.py
"""
from pathlib import Path
import json
import math
import sympy as s

x, y, z = s.symbols("x y z")


def iterate(h, f, n):
    for _ in range(n):
        f = s.expand(s.diff(h, z) * s.diff(f, y) - s.diff(h, y) * s.diff(f, z))
    return f


checks = []

# Nontrivial content g=x^2, multiplicity E=3, reduction degree e=3.
h = x**2*y**3 + x**5*z
for n in range(13):
    j, i = divmod(n, 3)
    f = y**i*z**j
    expected = (-1)**j * math.factorial(n) * x**(5*n-3*j)
    assert s.expand(iterate(h, f, n)-expected) == 0
    assert iterate(h, f, n+1) == 0
    checks.append({"case": "content_and_repeated_prime", "n": n, "passed": True})

# Nilpotent high-degree coefficients: reduction degree 2 although p has degree 3.
h = y**2 + x*y**3 + x**2*z
v = y**4 + (x*y-1)*z
assert s.expand(y**2 + x*h*y - h - x**2*v) == 0
for n in range(13):
    j, i = divmod(n, 2)
    f = y**i*v**j
    expected = math.factorial(n) * x**(2*(n-j))
    assert s.expand(iterate(h, f, n)-expected) == 0
    assert iterate(h, f, n+1) == 0
    checks.append({"case": "monic_lift_with_nilpotent_terms", "n": n, "passed": True})

# Mixed bad/good primes: x bad of multiplicity 2; x-1 good of multiplicity 3.
# An exact slice-like element q has Dq=x^2, and a Bezout combination produces
# a preimage of x^2 under D^2 globally, avoiding inversion of x-1.
a = x-1
m = x**2*a**3
h = y + a*y**2 + m*z
numerator = s.Poly(s.expand(y-h+a*h**2-2*a**2*h**3), z, y, x)
q, remainder = s.div(numerator, s.Poly(a**3, z, y, x))
assert remainder.is_zero
q = q.as_expr()
assert s.expand(iterate(h, q, 1)-x**2) == 0
A, B, gcd = s.gcdex(x**2, a**4, x)
assert gcd == 1
f2 = s.expand((A*q**2-B*z)/2)
assert s.expand(iterate(h, f2, 2)-x**2) == 0
assert iterate(h, f2, 3) == 0
checks.append({"case": "mixed_primes_global_preimage_n1", "passed": True})
checks.append({"case": "mixed_primes_global_preimage_n2", "passed": True})

result = {
    "date": "2026-10-26",
    "status": "exact_checks_passed_universal_theorem_requires_proof",
    "checks": checks,
    "number_checks": len(checks),
    "mixed_case_bezout": {"A": str(A), "B": str(B)},
}
output = Path(__file__).with_name("image_ideal_audit_checks.json")
output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
print(json.dumps({"passed": len(checks), "output": str(output)}))
