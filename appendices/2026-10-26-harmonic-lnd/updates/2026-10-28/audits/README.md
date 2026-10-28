# Audit records — 28 October 2026

These are frozen records of the internal, AI-assisted verification process.
They are not independent external peer review and do not establish priority.

- `named_claims/`: identification and scope of the named conjectures.
- `continuation/`: proof audit, 24 structured records, filtration review and
  comparison of the fourteen checked source hashes.
- `euler/`: proof audit, 20 structured records, original-input hashes and
  selected fresh rechecks.
- `upstream_appendix_integrity.json`: all 75 earlier appendix files matched
  their Git blobs at the pinned repository version.
- `upstream_tree.json`: the inspected public repository tree.

The registries overlap and must not be added together as a theorem count.
Their statuses record the audit at its own stage. The consolidated Russian
paper supplies the final formulation, hypotheses and subsequent corrections.
In particular, the Euler audit originally treated the real knot obstruction
conditionally; the final paper additionally checks H(3,7,8)=T(2,5) and
H(4,5,7)=5_2 against Koseleff–Pecker, *Harmonic knots*.

Historical source paths identify where an audit was performed. Reproduction
uses the portable programs in `../computations/` and its unified runner, not
the original workstation paths in these audit records. Duplicate code is
omitted here: the same named-candidate and Euler recheck programs are supplied
in `computations/audit_checks/` and `computations/euler/`.

No claim of a new complex rectifier for H(3,7,8) or H(4,5,7) is supported by
these records. Neither the degree-four relative exclusion nor a failed finite
search is an unrestricted obstruction to rectification.
