#!/usr/bin/env python3
# Consolidated candidate-identification audit; exact formulas remain unchanged.
# Read AUDIT_RU.md for the distinction between a parameter lift and a coordinate.
"""Verify the original Shastri parameter and van den Essen--van Rossum slice.

These exact identities identify the candidate in Conjectures 5.1--5.3.
They do not prove that its kernel is polynomial: that conclusion additionally
uses the complete rectifier and its polynomial inverse, as explained in
AUDIT_RU.md. A parameter lift alone is not a coordinate certificate.
"""
from pathlib import Path
import json
import sympy as sp

t, u, x, y, z = sp.symbols("t u x y z")
variables = (x, y, z)
curve = (u**3 - 3*u, u**4 - 4*u**2, u**5 - 10*u)
parameter = y*z - x**3 - 5*x*y + 2*z - 7*x
substitution = dict(zip(variables, curve))
checks = []


def check(name, condition):
    """Raise explicitly, including when Python is run with -O."""
    if not condition:
        raise AssertionError(name)
    checks.append(name)


def derivation(polynomial):
    """Apply D=t*d/du+gamma'(u)*d/dX in the five original variables."""
    return sp.expand(t*sp.diff(polynomial, u) + sum(
        sp.diff(fi, u)*sp.diff(polynomial, xi)
        for fi, xi in zip(curve, variables)
    ))


check("parameter_restricts_to_u", sp.expand(parameter.subs(substitution, simultaneous=True)) == u)
invariants = tuple(fi - t*xi for fi, xi in zip(curve, variables))
for index, polynomial in enumerate(invariants):
    check(f"invariant_{index + 1}", derivation(polynomial) == 0)

numerator = sp.expand(u - parameter.subs(dict(zip(variables, invariants)), simultaneous=True))
quotient, remainder = sp.div(sp.Poly(numerator, t, u, x, y, z), sp.Poly(t, t, u, x, y, z))
check("slice_division_is_exact", remainder.is_zero)
original_slice = quotient.as_expr()
check("original_slice_derivative_is_one", derivation(original_slice) == 1)

# The ambient three-variable parameter is not a coordinate: its gradient
# vanishes at the two displayed points. This does not contradict the fact
# that its associated five-variable slice becomes a coordinate after the
# independent rectifier has established polynomiality of the kernel.
gradient = tuple(sp.diff(parameter, variable) for variable in variables)
critical_points = ((1, -2, 5), (-1, -2, -5))
for index, point in enumerate(critical_points):
    point_substitution = dict(zip(variables, point))
    check(f"critical_point_{index + 1}", all(value.subs(point_substitution) == 0 for value in gradient))

# Distinguish the harmonic figure-eight from Shastri's other example.
harmonic_middle = u**5 - 5*u**3 + 5*u
shastri_figure_eight_middle = u*(u**2 - 1)*(u**2 - 4)
check("figure_eight_middle_components_differ_by_u",
      sp.expand(harmonic_middle - shastri_figure_eight_middle) == u)

output = {
    "date": "2026-10-28",
    "status": "PASS",
    "arithmetic": "exact rational",
    "sympy_version": sp.__version__,
    "checks": checks,
    "original_parameter": str(parameter),
    "original_slice": str(original_slice),
    "slice_total_degree": int(sp.Poly(original_slice, t, u, x, y, z).total_degree()),
    "scope": "Candidate identification and exact slice identities only; kernel polynomiality requires the complete rectifier proof.",
}
path = Path(__file__).with_name("original_slice_verification.json")
path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"PASS: {len(checks)} exact candidate-identification checks")
