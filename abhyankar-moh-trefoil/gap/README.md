# Independent exact verification in GAP

This directory checks the compact polynomial constructions for

\[
\gamma_T(t)=(t^3-3t,t^4-4t^2,t^5-10t)
\]

and

\[
\gamma_H(t)=(t^3-3t,t^5-5t^3+5t,t^7-7t^5+14t^3-7t).
\]

It also checks the affine passage to the Chebyshev trefoil. No Python,
SymPy, FLINT, network connection, or additional GAP package is used.
All polynomial coefficients are recomputed by GAP.

## Run

From this directory:

```text
gap -q --quitonbreak --norepl verify_rectification.g
```

From an interactive GAP session on Windows, substitute your actual path:

```gap
LogTo("C:/rectification_check/my_gap_run.log");
Read("C:/rectification_check/gap/verify_rectification.g");
LogTo();
```

Do not type the `gap>` prompt. An error or a `brk>` prompt is a failure,
even if earlier checks printed `PASS`. The command-line flags make errors
terminate with a nonzero exit status rather than enter the break loop.

The main script must print two blocks ending in

```text
BOTH RECTIFICATIONS VERIFIED IN GAP
Checks: 24; runtime (CPU ms): ...
```

and two further blocks ending in

```text
CHEBYSHEV NORMALIZATIONS VERIFIED; additional checks: 3
```

The two copies correspond to the conjugate coefficients `a=E(6)` and
`a=1-E(6)`. Thus there are **48 core checks and 6 additional Chebyshev
checks**, not 54 independent mathematical theorems.

## Exact arithmetic and the certificate

The coefficient field is `CyclotomicField(3)`. The exact root of unity
`E(6)` belongs to this field and satisfies `a^2-a+1=0` and `a*(1-a)=1`.
Both identities are checked. Evaluations use simultaneous polynomial
substitution. There are no floating-point calculations or random samples.

`ExactDivX` verifies every coefficient below the required power of `x`,
constructs a polynomial quotient, and checks the product identity. The
four divisions defining `W`, `chi`, and the forward and inverse harmonic
transfer are therefore polynomial divisions, not rational simplifications.

For the base maps `A=(x,H,W)` and `Ainv=(x,R,S)`, the script directly
checks `H(x,R,S)=y`, `R(x,H,W)=y`, and `S(x,H,W)=z`. It also checks

```text
x^5*W = a*(a*x*y+z-f(x,H)),
a*x*R+S-f(x,y) = (1-a)*x^5*z.
```

Substitution and `a*(1-a)=1` give `x^5*(W(x,R,S)-z)=0`. Cancellation in
the polynomial domain proves the fourth inverse identity globally.

The trefoil maps are composites of this certified inverse pair and the
explicit affine and triangular outer maps. The outer inverse identities,
both restrictions to the curve/axis, and forward degrees `(5,15,24)` are
checked.

For the harmonic relative map, invert `x` and factor it as

```text
(x,y,z) -> (x,x*z-y^2+2,y)
        -> (x,H,W)
        -> (x,y,(z-correction(y))/x).
```

The inverse is obtained by reversing these three explicitly invertible
factors. Exact division proves polynomiality of both resulting maps.
Since localization of a polynomial domain is injective, the inverse
identities then hold before localization, including the fibre `x=0`.
The script additionally checks the centre on that fibre, both outer
inverse identities, the curve/axis restrictions, and degrees `(7,21,41)`.

The relative Jacobian checks are consistency checks. They are not used
as a replacement for the inverse certificate.

## Chebyshev normalization

Define `C_0(t)=2`, `C_1(t)=t`, and
`C_(n+1)(t)=t*C_n(t)-C_(n-1)(t)`. Equivalently,
`C_n(t)=2*T_n(t/2)`, in the usual notation for Chebyshev polynomials.
The additional checks verify

```text
M(x,y,z) = (x,y+2,z-5*x),
Minv(x,y,z) = (x,y-2,z+5*x),
M(gamma_T(t)) = (C_3(t),C_4(t),C_5(t)),
gamma_H(t) = (C_3(t),C_5(t),C_7(t)).
```

Thus the Chebyshev trefoil is already covered by the original affine
normalization. Its rectifier is `Phi_T o Minv`, with inverse
`M o Phi_T_inverse`. The script constructs these maps and checks both
curve/axis restrictions. Their global inverse property follows by
composing the two certified inverse pairs.

This does not establish a result for arbitrary triples of Chebyshev
degrees or for every real knot represented by a Chebyshev parametrization.

## Negative controls

Run each separately from this directory:

```text
gap -q --quitonbreak --norepl negative_identity.g
gap -q --quitonbreak --norepl negative_division.g
```

Both must fail with a nonzero exit status. The expected messages are
`FAILED: deliberately false identity 1=0` and
`NOT DIVISIBLE: deliberate 1/x`, respectively. Each first runs the normal
verification, then deliberately passes an invalid input to the checker.

The main script also confirms that its first harmonic coordinate does
not restrict to `t` when the second curve component has `+4t` instead
of `+5t`. This excludes that substitution for these formulas; it proves
nothing about the existence of another rectifier for the `+4t` curve.

## Recorded run and scope

The supplied logs were freshly produced by **GAP 4.12.1**, with exit code
0 for the main script and exit code 1 for each negative control. The
machine-readable `run_results.json` records commands, counts, timings,
and source hashes. No run in GAP 4.16 is claimed.

These checks concern the compact construction. They **do not parse the
printed LaTeX expansions**. Use the repository's separate
`verify_printed_formulas.py` for that purpose. This distinction matters:
the earlier expanded appendices contained sign errors even though the
compact certificate passed.

This is exact computer algebra plus the elementary cancellation and
localization arguments above. It is not a full Lean formalization, a
proof of the general embedding conjecture, a proof of minimal degrees,
or a claim of bibliographical priority.

After an interactive run, the records `RectificationResult`,
`ConjugateResult`, `ChebyshevResult`, and `ConjugateChebyshevResult`
contain the computed polynomial maps.
