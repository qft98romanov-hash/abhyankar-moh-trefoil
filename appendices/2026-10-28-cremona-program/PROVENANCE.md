# Provenance and review boundary

Date: **28 October 2026** (Europe/Moscow).

Author: **Ivan Dorofeev**, as identified by the existing repository manuscript.

Baseline repository:
https://github.com/qft98romanov-hash/abhyankar-moh-trefoil

Pinned baseline commit:
`b954f3609e900761fddc9c8ff03d8301e9604cab`.

The original manuscript, compact verifier, printed-formula verifier and first
appendix were read from that revision. They are not rewritten by Appendix 2.
The root README, changelog and root checksum manifest receive integration
updates; all mathematical additions are isolated in this second appendix.

This is an AI-assisted working research document. The algebraic checks,
literature comparisons and cross-checks were performed within that workflow.
They are not external independent peer review. All statements remain under
verification, and publication priority is not asserted.

## Evidence categories

- **Baseline constructions:** existing polynomial rectifiers and inverses.
- **New exact reruns:** compact baseline and all twelve printed components.
- **Appendix 2 exact calculations:** the standalone normal and optimized runs,
  with explicit finite family range and negative controls.
- **Written mathematical arguments:** all-index induction, the inner-coordinate
  lemma, Cremona subgroup membership and arithmetic consequences.
- **Published inputs:** the cited relative-coordinate, wildness, Cremona and
  stable-tameness theorems. No formal verification of these theorems is claimed.
- **Inherited Appendix 1 consequences:** the explicit kernel, slice quotient
  and extended Rees ring attached to the Shastri curve. Their algebraic
  mechanism is displayed again; not every old computation was rerun.
- **Open questions:** completeness, other tame rectifiers, minimal degrees and
  other coefficient fields. A failed bounded search is not an obstruction to
  every polynomial automorphism.

See `audit/claim_status.md` for the source-access boundary of the literature
check and `computations/README.md` for the exact computational coverage.

## Archive contents

The full downloadable archive contains the repository snapshot plus Appendix 2,
including the source manuscript, English-commented code, fresh logs, previous
certificates and checksums. It excludes `.git`, interpreter caches and temporary
TeX compilation products. The separate Overleaf ZIP contains a standalone
`main.tex`, all included sections, the bibliography and bundled font files.

Bundled URW font files are unchanged; their copyright and licence notice is
included under `latex/fonts/LICENSE-URW.txt`.
