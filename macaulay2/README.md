# Macaulay2 verification

This directory contains a standalone exact-arithmetic implementation of the compact rectification certificates. It calls neither Python nor SymPy. The implementation was rerun successfully with **Macaulay2 1.22**. It checks the two specific parametrizations

\[
\gamma_T(t)=(t^3-3t,\ t^4-4t^2,\ t^5-10t),
\qquad
\gamma_H(t)=(t^3-3t,\ t^5-5t^3+5t,\ t^7-7t^5+14t^3-7t).
\]

The harmonic parametrization has **+5t**, not +4t, in its second component.

## Run

Run these commands from this directory:

```bash
M2 --version
M2 --script verify_rectification.m2
M2 --script verify_chebyshev.m2
```

The first certificate must exit with status 0 and finish with

```text
BOTH RECTIFICATIONS VERIFIED (Macaulay2 certificates)
```

It prints **27 PASS lines**. The Chebyshev script first runs those 27 checks, then adds **3 further PASS lines**, and finishes with `THREE ADDITIONAL CHEBYSHEV CHECKS VERIFIED`. The recorded logs are `verification_macaulay2.log` and `chebyshev_macaulay2.log`.

Two external negative controls are also supplied:

```bash
M2 --script negative_division.m2
M2 --script negative_identity.m2
```

**Both are expected to fail with a nonzero exit status.** They first load the successful main certificate. Then the first calls its actual exact-division function on `(1+x)/x`, and the second calls its actual assertion function on a parameter lift perturbed by 1. The recorded runs both exited with status 1 and reported their corresponding `EXTERNAL NEGATIVE CONTROL` failure. These deliberate failures are not failures of the rectifications.

## Why these checks establish polynomial inverses

All calculations take place in

\[
K=\mathbb Q[a]/(a^2-a+1),\qquad P=K[x,y,z,t].
\]

The discriminant is -3, so the quadratic is irreducible over the rationals. Thus K is a field and P is an integral domain. Macaulay2's `toField` declares this mathematically justified fact; it is not itself an irreducibility proof. Working in this abstract field covers both complex embeddings of K. There is no floating-point root approximation.

`at` uses a ring map and substitutes all variables simultaneously. `exactDivX` computes a quotient inside P and then explicitly checks both its parent ring and the identity `p-x^n*q=0`. Polynomiality is never inferred from formal cancellation in a rational-function expression.

For the base maps `A=(x,H,W)` and `B=(x,R,S)`, the program directly checks

\[
H(x,R,S)=y,\qquad R(x,H,W)=y,\qquad S(x,H,W)=z.
\]

The fourth identity follows from two checked polynomial certificates:

\[
x^5W=a(axy+z-f(x,H)),\qquad
axR+S-f(x,y)=(1-a)x^5z.
\]

Substituting `(R,S)` into the first and using the second gives
`x^5 W(x,R,S)=a(1-a)x^5 z=x^5 z`. Since P is an integral domain, cancellation gives `W(x,R,S)=z` **globally, including x=0**. This proves both compositions without expanding the expensive fourth expression in full.

For the harmonic transfer, after inverting x the map is the composition

\[
(x,y,z)\mapsto(x,xz-y^2+2,y)
\mapsto(x,H,W)
\mapsto\left(x,H,\frac{W-\operatorname{corr}(H)}x\right).
\]

The inverse is obtained by reversing these three factors. The script verifies the exact divisions proving that the resulting forward and inverse maps both belong to P. The injection `P -> P[x^(-1)]` then brings the two composition identities back to P. In addition, both compositions are directly checked on x=0. There is no unverified exceptional fibre.

The remaining changes of variables have displayed elementary inverses; their identities are checked. The program also verifies the restrictions of the rectifiers to the parametrized curves, the inverses on the target axis, the forward degrees `(5,15,24)` and `(7,21,41)`, and the Jacobians. **The Jacobian checks are not used as a substitute for polynomial inverses.**

## Chebyshev normalization

Define `C_0(t)=2`, `C_1(t)=t`, and `C_{n+1}(t)=t*C_n(t)-C_{n-1}(t)`. Equivalently, `C_n(t)=2*T_n(t/2)` for the usual Chebyshev polynomial T_n.

The additional script checks

\[
M\circ\gamma_T=(C_3,C_4,C_5),\qquad
M(x,y,z)=(x,y+2,z-5x),
\]

\[
M^{-1}(x,y,z)=(x,y-2,z+5x),\qquad
\gamma_H=(C_3,C_5,C_7).
\]

Both affine inverse identities are checked. In particular, a rectifier of the normalized Chebyshev trefoil is `Phi_T o M^(-1)`, with inverse `M o Psi_T`. This does not assert rectifiability for arbitrary Chebyshev degree triples.

## Scope and optional computations

This package verifies the **compact polynomial constructions**. It does not parse the coordinate-only LaTeX appendices. Those are checked separately by the repository's `verify_printed_formulas.py`; that distinction matters because earlier printed formulas contained sign errors.

The executable certificates above use exact division, cancellation and injective localization. A single expansion of all final compositions is not needed for the proof and is not claimed by these run logs.

This verification does not establish the general embedding conjecture, minimal degrees, or literary priority. It is not a full Lean formalization. The executable lines of the core certificate are unchanged from the prior implementation; only its comments were translated into English. The added scripts supply the external negative controls and the three Chebyshev checks.

For installation, use the project's official instructions: <https://macaulay2.com/Downloads/>. On Windows, Macaulay2's official Windows page describes the WSL route: <https://macaulay2.com/Downloads/Microsoft-Windows/index.html>.
