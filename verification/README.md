# Audit of the displayed formulas

From the repository root, run `python verify_printed_formulas.py`.
This reads all twelve actual LaTeX components and checks them against the
compact construction. `python verification/run_negative_controls.py` tests
the checkers on deliberately false inputs and temporary one-sign mutations.

An additional independent harmonic reader can be run using
`python verification/audit_harmonic_independent.py --repository . --expect-correct`.

See ../VERIFICATION.md and PYTHON_AUDIT.md for the precise scope and new runs.
Logs marked `original_audit` and the correction manifests document the previous
52 sign errors. The corrected-paper logs show agreement. Arithmetic is exact.
