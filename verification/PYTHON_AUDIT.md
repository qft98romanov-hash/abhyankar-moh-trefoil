# Python verification: scope and implementation audit

Updated 26 October 2026. Two symbolic inverse-callable checks and the parser
corrections below have been added. The polynomial construction formulas are
unchanged. See [HARDENING_2026-10-26.md](HARDENING_2026-10-26.md).

The compact construction in `verify.py` was read and rerun independently. Its
coefficient arithmetic is exact over
`Q[a]/(a^2-a+1)`, with `x,y,z,t` polynomial indeterminates. No floating-point
evaluation, random sampling, or numerical tolerance is used.

## Why the compact certificates suffice

The base map is `(x,H,W)` and its candidate inverse is `(x,R,S)`.
The program expands `H(x,R,S)=y`, `R(x,H,W)=y`, and `S(x,H,W)=z`.
It also checks the defining identity for `W` and

```text
a*x*R + S - f = (1-a)*x^5*z.
```

Substitution in the defining identity for `W`, together with `a*(1-a)=1`, gives
`x^5*(W(x,R,S)-z)=0`. The coefficient ring is a field because
`a^2-a+1` is irreducible over Q; its polynomial ring is an integral domain.
Cancellation therefore establishes the missing component. Thus both base
composition identities hold as polynomial identities.

For the trefoil, the remaining maps are displayed affine and triangular
automorphisms with checked inverses. Their composition gives the claimed
global inverse. Curve substitution and the inverse on the axis are separately
checked, as are component degrees and a Jacobian identity.

For the harmonic figure-eight, the relative construction is the composition
of three explicit invertible maps after adjoining `1/x`: a modification,
the base automorphism, and an output modification. The proposed inverse is
their inverse composition in reverse order. `div_x` checks every coefficient
of each required numerator and rejects any non-divisible monomial. The forward
and inverse expressions are therefore polynomials. The injective localization
map from the polynomial ring to its localization implies that both composition
identities remain true on `x=0`, as well as off that fiber. The final triangular
map has its inverse checked separately.

This is a finite exact certificate. The script does not expand all six final
composition components at once. A nonzero constant Jacobian is only an
additional consistency check here; it is not being used as a substitute for
an inverse.

## Displayed formulas

`verify_printed_formulas.py` compares all twelve actual LaTeX right-hand sides
with the compact construction. The trefoil parser has an independent second
parsing route. A separately supplied harmonic checker uses two parsing routes
and separate coefficient normalization. All twelve corrected components are
checked; the earlier successful compact checks alone did not check LaTeX.

Each reader now validates component labels and argument order and rejects
multidigit exponents without braces. The independent harmonic reader parses
the actual inverse RHS with the invertible substitution
`X=x, Y=y-x^3+3*x, Z=z-(1-a)*(42*x^3-49*x)` in both parsing routes.
It no longer textually identifies `X^3-3*X+Y` with the original symbol `Y`.
Its multiplication handling retains the meaning of `\times`.

## Small implementation repairs

The following repairs were made on 25 October, when `verify.py` was unchanged:

1. Replace parser `assert` statements by explicit `require` calls. Several
   assertions consumed a closing token as a side effect, so Python's `-O`
   option could change the parser rather than merely disable diagnostics.
   Explicit guards retain all validation and token consumption under `-O`.
2. Make standalone `audit_harmonic.py` exit nonzero when any component differs.
   The previous wrapper already enforced this using the JSON results, but the
   standalone auditor used to write discrepancies and still exit successfully.
3. Correct its default repository location, and correct the independent
   harmonic auditor's command example and construction-loading comment.

The 26 October update additionally binds the actual `trefoil_inverse` and
`harmonic_inverse` callables to their proved factorizations by polynomial
identities in three independent variables. It corrects the independent
harmonic coordinate-substitution defect and the parser issues above, and
propagates `-O` from the wrapper to its child interpreters. None of these
changes alters the polynomial construction formulas.

## Reproducibility and negative controls

Fresh runs and their actual exit codes are recorded in the accompanying logs.
The control runner checks valid sources and deliberately invalid isolated
copies. It retains the historical sign mutations and tests changed labels,
unbraced multidigit exponents, the harmonic `U -> Y` corruption and an
off-axis change to `harmonic_inverse`. It requires both the expected exit code
and the intended diagnostic. A missing dependency or input is not an accepted
negative-test result. Temporary mutations never touch the actual paper.

This audit concerns the two concrete constructions and their presentation.
It is not a proof of rectifiability for every polynomial embedding, nor a full
Lean formalization, nor a general-purpose LaTeX verification system.

## Executed results

Runtime: Python 3.12.14; SymPy 1.14.0; pure Python coefficient arithmetic.

- Compact verifier with two inverse-callable bindings: exit 0, 19 PASS messages.
- Corrected literal LaTeX wrapper: exit 0, all twelve components match.
- Separate harmonic auditor: exit 0, all six components match.
- Hardened auditor wrapper: exit 0, all twelve components match.
- Expanded portable control runner: exit 0; five optimized positive cases pass and all fourteen deliberately invalid cases are rejected with exit 1 and the intended diagnostics.

`environment_and_inputs.json` records historical versions and input/source
hashes from 25 October, not hashes of current output logs.
[current_verification.json](current_verification.json) records the current
source and output-log hashes, versions and complete runs.
[negative_control_logs/results.json](negative_control_logs/results.json)
records each control's exit code, expected markers and duration.
