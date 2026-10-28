# Explicit trivialization of the Shastri locally nilpotent derivation

Field: `K = Q[a]/(a^2-a+1)`. The construction also works over any characteristic-zero field over which the stated rectifier exists. Source repository snapshot: `3cf41be3fb3b1108e1ec91dd23dff7bfcf59569e`.

This is an explicit application of the rectification criterion of van den Essen–van Rossum, *Triangular derivations related to problems on affine n-space*, Proceedings of the AMS **130** (2002), 1311–1322, DOI [10.1090/S0002-9939-01-06212-8](https://doi.org/10.1090/S0002-9939-01-06212-8), especially Theorem 4.1, Corollary 4.2, and Conjecture 5.1. The general implication is not claimed as new. The new input to the present calculation is the supplied exact rectifier. The source itself numbers the conjecture 5.1; “Conjecture E” is an external designation.

## General construction

Let `gamma(u)=(f(u),g(u),h(u))`, and suppose `F=(P,Q,R)` is an automorphism of `K[x,y,z]` satisfying

\[
F(\gamma(u))=(u,0,0).
\]

Write `G=F^{-1}`. Work first over `K[B]`, treating `B` as an independent variable. On

\[
A=K[B,u,x,y,z]
\]

consider

\[
D=B\partial_u+f'(u)\partial_x+g'(u)\partial_y+h'(u)\partial_z.
\]

It is locally nilpotent: it is triangular, or this follows from the explicit polynomial additive-group action given below.

Put

\[
V=\gamma(u)-B(x,y,z),\qquad
p=P(V),\quad q=\frac{Q(V)}B,\quad r=\frac{R(V)}B,\quad
s=\frac{u-P(V)}B.
\]

All displayed expressions are polynomials. Indeed, modulo `B`, their numerators become respectively `0`, `0`, and `u-P(gamma(u))=0`. This uses polynomial division by the indeterminate `B`, not division on a punctured variety.

Since `D(B)=0` and `D(V)=0`, the chain rule gives `D(p)=D(q)=D(r)=0` and `D(s)=1`. Cancellation of `B` is valid because the polynomial ring is a domain.

The inverse coordinate change is explicitly

\[
u=p+Bs,\qquad
(x,y,z)=\frac{\gamma(p+Bs)-G(p,Bq,Br)}B.
\]

These quotients are also polynomial: setting `B=0` in the numerator gives `gamma(p)-G(p,0,0)=0`. After inverting `B`, the two maps compose to the identity directly from `G F=F G=id`. As both maps are polynomial and localization is injective, the identities hold also on `B=0`.

Consequently

\[
A=K[B,p,q,r,s],\qquad D=\partial_s,\qquad
\ker D=K[B,p,q,r]\simeq K^{[4]}.
\]

Thus the statement is stronger than existence of a slice: it provides a polynomial coordinate system containing a slice and gives generators of the full invariant ring.

## Shastri specialization and Conjecture E

For

\[
\gamma(u)=(u^3-3u,\ u^4-4u^2,\ u^5-10u),
\]

the source rectifier has component degrees `(5,15,24)` and is defined over `K`. Its exact source identities are rerun by `verify_lnd.py`. Therefore the derivation

\[
D=t\partial_u+(3u^2-3)\partial_x+(4u^3-8u)\partial_y+(5u^4-10)\partial_z
\]

on `K[t,u,x,y,z]` has the above explicit polynomial invariant ring. After scalar extension this holds over `C`. Subject to the source rectifier identities, this contradicts Conjecture 5.1 (the assertion called Conjecture E) for this derivation. It does not decide the general Cancellation Problem.

## Arbitrary coefficient b(t), including repeated roots

The construction is an automorphism over `K[B]`. Base change `B -> b(t)` therefore produces a polynomial automorphism over `K[t]` for every polynomial `b(t)`, with no squarefreeness assumption, and conjugates

\[
D_b=b(t)\partial_u+f'(u)\partial_x+g'(u)\partial_y+h'(u)\partial_z
\]

to `partial_s`. This includes `b(t)=0`, provided the formulas are interpreted as specializations of the universal polynomial quotients, not as division by zero. This generalization is a direct consequence of the known rectification principle; no independent novelty claim is made.

## Exact special fiber

At `B=0`, `p=u` and

\[
q_0=-\nabla Q(\gamma(u))\cdot (x,y,z),\quad
r_0=-\nabla R(\gamma(u))\cdot (x,y,z),\quad
s_0=\nabla P(\gamma(u))\cdot (x,y,z).
\]

The matrix with these three coefficient rows is unimodular over `K[u]`: its determinant equals `det JF(gamma(u))=1` for this source rectifier. Differentiating `F gamma=(u,0,0)` gives `JF(gamma(u)) gamma'(u)=(1,0,0)`. The script checks both polynomial identities exactly. Hence

\[
K[u,x,y,z]=K[u,q_0,r_0,s_0],\qquad
D_0=\partial_{s_0},\qquad
\ker D_0=K[u,q_0,r_0].
\]

## A retraction is insufficient to supply a rectifier

The much smaller polynomial

\[
F_0=yz-x^3-5xy+2z-7x
\]

satisfies `F0(gamma(u))=u`, exactly. Nevertheless it is not an ambient polynomial coordinate: all three partial derivatives vanish at `(1,-2,5)` and `(-1,-2,-5)`. A component of a polynomial automorphism cannot have a vanishing gradient, because the full Jacobian matrix is everywhere invertible. The script checks both the retraction identity and these two critical points exactly.

Using `F0` instead of `P` still gives a slice `(u-F0(V))/B`; it does not give a coordinate triple or generators of the invariant ring. Thus existence of this easily computed retraction alone does not prove the claimed trivialization.

## A minimal-degree slice: a separate exact result

For `B=t`, the compact slice from `F0` is

\[
\begin{aligned}
\sigma={}&-(3u^6-13u^4+7u^2+7)x
+(u^5-5u^3+5u)y+(u^4-4u^2+2)z\\
&+t\bigl(3(u^3-3u)x^2+5xy-yz\bigr)-t^2x^3.
\end{aligned}
\]

It has 15 nonzero monomials and ordinary total degree seven in the five variables `(t,u,x,y,z)`. Literal exact differentiation gives `D(sigma)=1`. This formula is independent of the source rectifier.

Moreover, **seven is the minimum total degree of any polynomial slice**, over any characteristic-zero field. A dual certificate proves the lower bound: the 31 rational weights in `no_slice_degree6_certificate.json` define a coefficient-extraction functional `L` with `L(1)=1` and `L(D(m))=0` for all 462 monomials of total degree at most six. Thus `L(D(s))=0` for every polynomial `s` of degree at most six, contradicting `D(s)=1`. Rational weights extend linearly to every characteristic-zero field, so this is not merely a search over rational coefficients.

Run `python verify_minimal_slice.py` in this directory, or invoke it by path. It uses only the Python standard library and exact rational arithmetic. It independently checks every column of the derivation matrix and the degree-seven upper-bound formula. It requires neither SymPy nor the source rectifier nor a linear-system solver. A separate independently written verifier also passed. The Russian TeX section `minimum_slice.tex` includes the complete 31-entry table and proof. No claim of literature novelty is made.

The compact slice may also replace the previously constructed large slice while keeping the invariant generators. Indeed,

\[
\sigma-s=\frac{p-F_0(G(p,Bq,Br))}{B}\in K[B,p,q,r],
\]

where polynomiality follows by setting `B=0`. Hence `(B,p,q,r,sigma)` is again a polynomial coordinate system. The source construction's fully expanded slice `s` has total degree 15, while this replacement has degree seven when `B=t`.

## Additive-group action

The original action is already explicit:

\[
\exp(\lambda D)(B,u,X)=
\left(B,\ u+B\lambda,\ X+\frac{\gamma(u+B\lambda)-\gamma(u)}B\right).
\]

The quotient is polynomial. In the new coordinates it is simply

\[
(B,p,q,r,s)\longmapsto(B,p,q,r,s+\lambda).
\]

## Exact scope of the computational certificate

`verify_lnd.py` reruns the source rectification certificate. It then independently verifies `D(V)=0`, the source restrictions to the curve and axis, expands `p` and `s` and differentiates them literally, verifies the exact zero remainders that certify polynomiality of `q` and `r`, and checks the first-jet matrix, its determinant, its tangent identity, and the two critical points of `F0`.

The high-degree polynomials `q` and `r` are retained as arithmetic circuits. Their invariance uses the exact chain-rule certificate; the two full inverse identities use the displayed polynomial inverse formulas and injectivity of localization. The certificate does not claim to expand all large five-variable compositions. No floating-point calculations, motives, K-theory, or homological algebra are used.
