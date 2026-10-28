# Exact computation certificates for Appendix 2

All scripts and comments are in English. They run offline and use exact
rational polynomial arithmetic in `QQ[a,x,y,z,t]/(a^2-a+1)`. They do not use
floating point arithmetic, random sampling, external coefficient files, or
network downloads.

## Reproduce the recorded verification

Use Python 3.10 or newer and install SymPy 1.14.0 (the version used for the
recorded run). From the Appendix 2 directory:

```bash
python -m pip install sympy==1.14.0
python computations/run_all.py --max-n 3
```

The runner launches the verifier normally and with `python -O`. It compares
the exact polynomial outputs and all check records. Both runs include
negative controls. Explicit exceptions keep checks active with optimization
enabled; the implementation does not rely on Python's removable `assert`
statement.

For a single run, or a larger finite family range:

```bash
python computations/verify_appendix2.py --max-n 4 --output-dir results/custom
```

Increasing the bound may substantially increase execution time and polynomial
sizes. `--max-n N` always means a finite check of indices `1,...,N`.

## What is checked

1. The base polynomial coordinate, its companion, and its inverse. Both
   inverse congruences modulo `x^5`, exact divisions, the nontrivial inverse
   identities, the Jacobian sign, and integral coefficients are checked.
   One composition direction is expanded for both nontrivial components;
   the other uses an explicit nonzero-factor cancellation certificate for
   the companion component. This is the same algebraic implication proved
   in the manuscript, not an appeal to the Jacobian conjecture.
2. The original Shastri parametrization and its normalization. The actual
   polynomial rectifier maps the curve to the axis, and the inverse factors
   recover it. The component degrees are checked. The rational rectifier is
   checked in both composition directions as a rational map; the code does
   not assert that it is regular at every point of the curve.
3. For each tested `N`, construction of `p_N`, the curve `C_N`, and the
   inverse of the central polynomial modulo `x^N`. The forward and inverse
   transfer numerators are tested for divisibility by the **full** `x^N`.
   The correction polynomial, inverse-centre polynomial, curve components,
   and companion restricted to the curve are written into JSON.
4. The transferred maps are evaluated through their actual factors on `C_N`
   and on its image. Both generic outer polynomial compositions are checked.
   Both full relative maps are also materialized as polynomials for `N=1`,
   confirming the harmonic model and its component degrees.
5. The exact rational-length-two normal form and the valuation-one
   nonlinear coefficient used in the wildness proof. The computer checks
   their algebraic inputs for the finite range; the cited mathematical
   criteria and the all-`N` proof are not replaced by this test.
6. Algebraic examples of the Cremona generator conjugations and parity of
   the balanced monomial matrices. General membership uses the proof and
   Blanc--Heden's theorem; a finite sample is not a group-membership oracle.
7. Integrality of the constructed certificate polynomials. The proof of
   specialization to any field with a root of `a^2-a+1` uses these universal
   identities. Wildness is claimed only in characteristic zero.

## How the transfer certifies the exceptional fibre

The script proves that the two numerator polynomials vanish modulo `x^N`.
Their quotients by `x^N` are therefore polynomials. After inverting `x`, the
maps are compositions of the explicit modification, the already verified
base automorphism, and a correction shear/scaling. Their inverse factors
are supplied. Since localization of the polynomial ring is injective,
the composition identities also hold on the exceptional fibre `x=0`.

For general `N`, enormous complete composition expansions are intentionally
not produced. The exact modular certificates and factored inverse identities
are the computational certificate. The local Python evaluation functions
perform division after substitution and require their first polynomial
argument to be nonzero. To evaluate at a numerical point on `x=0`, first
materialize the polynomial quotient and then substitute the point. A
zero denominator in a factored evaluation is not a singularity of the
certified polynomial map.

## Negative and scope controls

The following invalid inputs must be rejected in both execution modes:

- a numerator that is not divisible by the claimed power of `x`;
- a changed coefficient of the inverse polynomial modulo `x^5`;
- a false polynomial identity.

The script also checks that the harmonic parameter coordinate does not
certify the different parametrization whose middle component has `+4t`
in place of `+5t`. This is a limitation of that particular formula, not a
proof of nonrectifiability of the changed curve.

## Limits

The calculations do not establish publication priority, universal
rectifiability, impossibility of a different tame rectifier, minimal
stabilization dimension, or a classification of the Cremona group. The
all-`N` statements, stable tameness, arithmetic obstruction over real
fields, and the implications of the tame/wild criteria are mathematical
arguments in the manuscript. All Appendix 2 material remains under review.
