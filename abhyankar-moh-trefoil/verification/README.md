# Audit of the displayed formulas

From the repository root, run `python verify_printed_formulas.py`.
This reads all twelve actual LaTeX components and checks them against the
compact construction. `python verification/run_negative_controls.py` tests
the checkers on deliberately false identities, inexact divisions, temporary
sign/label/exponent/coordinate mutations and an altered inverse callable.

An additional independent harmonic reader can be run using
`python verification/audit_harmonic_independent.py --repository . --expect-correct`.

See [VERIFICATION.md](../VERIFICATION.md), [PYTHON_AUDIT.md](PYTHON_AUDIT.md)
and [HARDENING_2026-10-26.md](HARDENING_2026-10-26.md) for the precise scope
and new runs. [current_verification.json](current_verification.json) records
current source and output hashes.
Logs marked `original_audit` and the correction manifests document the previous
52 sign errors. `printed_rerun.log` is the complete current twelve-component
log. The old `printed_formulas_corrected.log` and `hardened_printed.log` are
incomplete historical captures, not complete current certificates. Arithmetic
is exact. The historical `environment_and_inputs.json` describes its original
input files; it is not a current-source manifest after these checker updates.
