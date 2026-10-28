# English translation audit

Date: **28 October 2026**. Scope: the full English research text corresponding
to the Russian appendix of the same date.

The translation retains all sixteen sections, mathematical proofs, status
tables, limitations and fifteen references. A separate internal prose review
found no omitted proofs, reversed implications, lost hypotheses or stronger
claims. This review was AI-assisted and is not independent external peer review.

Run the portable check from any working directory:

```sh
python verify_translation.py
```

The script locates both source trees relative to itself, compares all six
section files, and writes `translation_audit.json`. The delivered result is
**PASS**, covering **833 mathematical fragments**, the section counts,
environment sequences, labels and citation keys.

The check compares formula multisets after removing whitespace and short
translated prose labels inside `\text{...}`. Two pairs of inline formulas in
the continuation proof change order to fit English syntax. The Russian prose
specifies the *degree* of M but places only `M>10` in math mode; the English
version writes `\deg M>10` explicitly. This notational clarification preserves
the stated degree restriction and is the only normalized symbolic difference.
These normalization rules are explicit in the checker and are not substitutes
for reading the proofs.

The front matter and bibliography were reviewed separately. The abstract uses
the precise term “affine spaces of candidates”, consistently with the theorem
and the corresponding Russian body text. Both versions retain the status
“under verification”, author Ivan Dorofeev and the date 28 October 2026.

The Russian PDF and source, all programs in `computations/`, their certificates
and logs are byte-identical to the previous delivered release. The existing
35/35 computation result is retained; translation does not claim a new run.
