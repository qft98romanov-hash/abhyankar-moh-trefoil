# Changes in this update

- Correct the 52 sign errors in the expanded appendices: 8 trefoil and 44 harmonic figure-eight. Preserve the compact polynomial constructions.
- Audit all twelve actual LaTeX components and add independent parsing checks and reproducible one-sign negative controls.
- Keep parser validation active with Python `-O`; make the standalone harmonic auditor report failure by a nonzero exit status.
- Include independently rerun GAP and Macaulay2 certificates, negative controls, English instructions, versions and logs.
- Add explicit Chebyshev normalization checks and a concluding section explaining `(C3,C4,C5)`, `(C3,C5,C7)` and the scope of the transfer.
- Add acknowledgements to Alexei Kanel-Belov and Alexander Frolov.
- Rebuild the paper as a 30-page PDF. The result date remains 24 October 2026; the expanded-formula corrections are identified in the article and errata.

See VERIFICATION.md for what was executed. A full Lean formalization and a theorem for arbitrary embeddings are not claimed.
