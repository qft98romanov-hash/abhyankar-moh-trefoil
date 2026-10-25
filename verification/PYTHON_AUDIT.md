# Python verification: scope and implementation audit

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

## Small implementation repairs

The compact formulas and `verify.py` were left unchanged.

1. Replace parser `assert` statements by explicit `require` calls. Several
   assertions consumed a closing token as a side effect, so Python's `-O`
   option could change the parser rather than merely disable diagnostics.
   Explicit guards retain all validation and token consumption under `-O`.
2. Make standalone `audit_harmonic.py` exit nonzero when any component differs.
   The previous wrapper already enforced this using the JSON results, but the
   standalone auditor used to write discrepancies and still exit successfully.
3. Correct its default repository location, and correct the independent
   harmonic auditor's command example and construction-loading comment.

## Reproducibility and negative controls

Fresh runs and their actual exit codes are recorded in the accompanying logs.
The control runner first checks the corrected sources, then restores exactly
one previous sign error in an isolated temporary copy of each appendix.
The wrapper must reject both altered copies with exit code 1. The standalone
harmonic checker is also required to reject its altered copy under `python -O`.
Temporary mutations never touch the actual paper.

This audit concerns the two concrete constructions and their presentation.
It is not a proof of rectifiability for every polynomial embedding, nor a full
Lean formalization, nor a general-purpose LaTeX verification system.

## Executed results

Runtime: Python 3.12.14; SymPy 1.14.0; pure Python coefficient arithmetic.

- Unchanged compact verifier: exit 0, 17 PASS messages.
- Corrected literal LaTeX wrapper: exit 0, all twelve components match.
- Separate harmonic auditor: exit 0, all six components match.
- Hardened auditor wrapper: exit 0, all twelve components match.
- Final portable control runner: exit 0; two positive audits under `-O` pass, and all five intended failures are rejected with exit 1. The five controls are a false compact identity, a nondivisible numerator, a trefoil sign error through the wrapper, a harmonic sign error through the wrapper, and the same harmonic error through the standalone auditor under `-O`.

`environment_and_inputs.json` records versions and input/output SHA256 hashes.
`portable_control_logs/results.json` records each exit code, expected output marker, and duration.
