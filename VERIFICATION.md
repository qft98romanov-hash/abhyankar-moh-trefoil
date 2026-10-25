# Verification and reproducibility

The core constructions are unchanged. The expanded LaTeX formulas contain the
52 sign corrections documented in [ERRATA_2026-10-25.md](ERRATA_2026-10-25.md).
The implementations and the corrected printed formulas were independently
reread and rerun. All coefficient arithmetic is exact, over
`Q[a]/(a^2-a+1)` or its exact cyclotomic realization.

## Recorded results

| Implementation | Observed version | Result | Evidence |
|---|---|---|---|
| Python / SymPy | Python 3.12.14 / SymPy 1.14.0 | 19 checks passed, including symbolic inverse-callable bindings | [log](verification.log) |
| Literal LaTeX audit | SymPy 1.14.0 | All 12 printed components agree; component labels and argument order checked | [complete log](verification/printed_rerun.log) |
| Independent harmonic LaTeX audit | SymPy 1.14.0 | All 6 harmonic components agree after an invertible coordinate substitution | [log](verification/independent_harmonic_rerun.log) |
| GAP | 4.12.1 | 48 core checks and 6 additional Chebyshev checks passed | [log](gap/gap_run.log) |
| Macaulay2 | 1.22 | 27 core checks and 3 additional Chebyshev checks passed | [core log](macaulay2/verification_macaulay2.log), [Chebyshev log](macaulay2/chebyshev_macaulay2.log) |

The GAP count includes the two conjugate choices of the coefficient `a`.
Macaulay2 works in the abstract quadratic field. Counts describe assertions,
not independent theorems. These are the versions actually run; a run in GAP
4.16 is not claimed.

## Python

From the repository root:

```bash
python -m pip install -r requirements.txt
python -u verify.py
python -u verify_printed_formulas.py
python verification/audit_harmonic_independent.py --repository . --expect-correct
python verification/run_negative_controls.py
```

No FLINT installation is required. The [recorded control results](verification/negative_control_logs/results.json) contain five successful optimized cases and fourteen correctly rejected invalid inputs. The runner checks exit status and the intended diagnostic, including false identities, non-exact divisions, restored sign errors, changed component labels, unbraced multidigit exponents, a corrupted inverse-coordinate expression, and an altered inverse callable. It mutates temporary copies only. Parser validation remains active under `-O`, and the wrapper passes its optimization setting to its child interpreters.

The previous auditor wrapper already rejected discrepant harmonic results,
but its standalone child did not return a failure exit status. Several parser
assertions also consumed tokens and were affected by `-O`; these were replaced
by explicit guards. The 26 October hardening adds two symbolic checks to
`verify.py`; its polynomial construction formulas are unchanged. The independent
harmonic reader now uses an invertible coordinate substitution rather than
textual compression. See [the implementation audit](verification/PYTHON_AUDIT.md)
and [the combined audit corrections](verification/HARDENING_2026-10-26.md).

## GAP

From the `gap` directory:

```text
gap -q --quitonbreak --norepl verify_rectification.g
gap -q --quitonbreak --norepl negative_identity.g
gap -q --quitonbreak --norepl negative_division.g
```

The first command must exit 0; the last two must exit nonzero. They did so in
the recorded run, with the expected failure messages. The [GAP guide](gap/README.md)
also gives interactive Windows instructions.

## Macaulay2

From the `macaulay2` directory:

```text
M2 --script verify_rectification.m2
M2 --script verify_chebyshev.m2
M2 --script negative_identity.m2
M2 --script negative_division.m2
```

The first two commands must exit 0; the last two must fail with their intended
`EXTERNAL NEGATIVE CONTROL` diagnostics after the successful core certificate.
Each additional script loads the core certificate relative to its own file,
so it can also be launched by path from another directory. See the
[Macaulay2 guide](macaulay2/README.md).

## Mathematical scope

All three CAS implementations reconstruct the compact polynomial maps.
They check exact polynomial division, finite inverse certificates, the curve
and axis restrictions, degrees and Jacobians. The base inverse certificates
give both compositions by cancellation in a polynomial domain. The harmonic
factorization is invertible after adjoining `1/x`; polynomiality in both
directions and injective localization prove the identities globally,
including `x=0`. The Jacobian is an additional check, not the invertibility
criterion. The paper and MECHANISM.md give these deductions explicitly.

The literal LaTeX audit is a separate necessary presentation check. GAP and
Macaulay2 do not read LaTeX. Two parsing paths and deliberately corrupted
inputs help test the auditors themselves.

The current [run manifest](verification/current_verification.json) records
commands, versions, source hashes, log hashes, exit codes and expected markers.
Older logs and `environment_and_inputs.json` remain historical evidence of the
25 October checks. In particular, `printed_formulas_corrected.log` and
`hardened_printed.log` are incomplete historical captures and are not used as
evidence for the current twelve-component result.

The checks establish the two specified constructions and the stated affine
Chebyshev normalization. They do not prove a theorem for all Chebyshev knots,
the general embedding conjecture, minimal degrees or bibliographical novelty.
The project is not a full Lean formalization. Earlier partial Lean material
and Aristotle prompts remain in the separate independent-check package;
no new Lean or Aristotle result is claimed by this update.
