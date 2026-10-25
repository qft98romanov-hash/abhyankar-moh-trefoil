# Polynomial rectification of the trefoil and a harmonic figure-eight

**Ivan Dorofeev** · Independent Researcher  
[qft98romanov@gmail.com](mailto:qft98romanov@gmail.com)

The results were obtained on **24 October 2026** through interactive work with
**GPT Astra**. The main polynomial identities and both explicit rectifications
have been checked by exact symbolic computation; a reproducible computational
certificate is included.

[Full paper](paper/rectification.pdf) · [LaTeX source](paper/main.tex) ·
[Detailed mechanism](MECHANISM.md) · [Certificate](verify.py) ·
[Run log](verification.log)

The paper is organized as **methods → trefoil → harmonic figure-eight**.

## Acknowledgements

The author expresses his sincere gratitude to Alexei Kanel-Belov and Alexander Frolov.

## Correction and literal-formula audit: 25 October 2026

The previous coordinate-only TeX formulas contained 52 sign errors: 8 in the
trefoil formulas and 44 in the harmonic figure-eight formulas. The compact
construction in `verify.py` is unchanged and its exact certificate passed again.
The displayed formulas have now been corrected and are checked by reading their
actual LaTeX right-hand sides. See [the errata](ERRATA_2026-10-25.md).

Run both the construction certificate and the literal-document check:

```bash
python -u verify.py
python -u verify_printed_formulas.py
```

The second command fails if any of the twelve printed forward/inverse components
differs from the corresponding compact polynomial.

## Method in brief

Work over

```math
K=\mathbb{Q}[a]/(a^2-a+1)\simeq\mathbb{Q}(\sqrt{-3}).
```

1. **Start with a verified relative automorphism**
   $`A=(x,H,W)`$ and its explicit polynomial inverse.
2. **Transfer the coordinate** through
   $`\beta(x,y,z)=(x,p(x,y)+m(x)z,y)`$, where $`m\ne0`$.
   Modulo $`m`$, require the centre $`H(x,p(x,y),y)`$ to have an invertible linear
   coefficient and nilpotent higher coefficients. Finite inversion of this
   centre produces a polynomial correction $`\varphi(x,T)`$.
3. **Correct and divide exactly:**

   ```math
   \mathcal A(x,y,z)=\left(
   x,\ H\circ\beta,
   \frac{W\circ\beta-\varphi(x,H\circ\beta)}{m(x)}
   \right).
   ```

   Both this quotient and the corresponding inverse quotient are polynomial,
   including when $`m`$ has repeated roots.
4. **Pass from local to global identities.** After inverting $`m`$, the factors
   are explicitly reversible. Polynomiality in both directions and injectivity
   of localization give a global polynomial automorphism, including the fibres
   where $`m=0`$.
5. **Straighten the curve.** If
   $`\mathcal A(\gamma(t))=(b(t),t,w(t))`$, apply
   $`(x,T,Q)\mapsto(T,x-b(T),Q-w(T))`$ to obtain $`(t,0,0)`$.

The trefoil supplies the explicit base construction. For the harmonic model,
the transfer uses $`m=x`$ and $`p=2-y^2`$; the centre is $`-y`$ at $`x=0`$.
The full paper gives the formulas, both inverse maps, and the proof of each step.

The general lifting principle has classical antecedents; no novelty claim is
made for it. The paper explains the precise connections and cites the relevant
propositions.

## The verified curves

```math
\gamma_T(t)=(t^3-3t,\ t^4-4t^2,\ t^5-10t),
```

```math
\gamma_H(t)=(t^3-3t,\ t^5-5t^3+5t,\ t^7-7t^5+14t^3-7t).
```

The displayed rectifiers have component degrees $`(5,15,24)`$ and $`(7,21,41)`$,
respectively; minimality is not asserted. The harmonic model has **$`+5t`$** in
its second component. These are rectifications over $`K`$, hence over $`\mathbb C`$.

## Run the certificate

```bash
python -m pip install -r requirements.txt
python -u verify.py
```

The script uses exact SymPy arithmetic and requires no FLINT installation.
It checks polynomial divisions, inverse-composition certificates, curve
substitutions, degrees, and Jacobian determinants. Cancellation and localization
justify the final inverse identities as explained in the paper. A successful run
ends with `BOTH RECTIFICATIONS VERIFIED`.

The general transfer theorem is a sufficient construction under its stated
hypotheses; it does not settle rectification of arbitrary embeddings
$`\mathbb A^1_{\mathbb C}\hookrightarrow\mathbb A^3_{\mathbb C}`$.

## Independent verification

The exact checks are provided in three computer algebra systems. The Python
LaTeX audit additionally reads the actual twelve displayed components.

```bash
python -u verify.py
python -u verify_printed_formulas.py
gap -q --quitonbreak --norepl gap/verify_rectification.g
M2 --script macaulay2/verify_rectification.m2
```

See [VERIFICATION.md](VERIFICATION.md) for the tested versions, successful
run logs, negative controls and precise scope of the certificates; the
[GAP guide](gap/README.md) and [Macaulay2 guide](macaulay2/README.md)
give system-specific instructions. Neither CAS certificate substitutes
for checking the printed LaTeX formulas.

## Literature

- Original curves: [Shastri (1992), §3](https://doi.org/10.2748/tmj/1178227371); [Koseleff–Pecker (2011), Introduction](https://arxiv.org/abs/0909.3281).
- Plane theorem: [Abhyankar–Moh (1975)](https://doi.org/10.1515/crll.1975.276.148) and [Suzuki (1974)](https://doi.org/10.2969/jmsj/02620241).
- Spatial problem and coordinate lifts: [Craighero (1985), Introduction and Proposition 3](https://www.numdam.org/item/RSMUP_1985__74__115_0.pdf), including the precise locations of Abhyankar's Kyoto 1977 conjectures.
- Affine modifications: [Kaliman–Zaidenberg (1999), Proposition 2.1](https://arxiv.org/abs/math/9801076).
- Quotient inversion and exact division: [Edo–Vénéreau (2001)](https://doi.org/10.4064/ap76-1-6); [Edo–van den Essen–Maubach (2009), Lemma 1.1](https://arxiv.org/abs/0809.0767).
- Residual coordinates: [Bhatwadekar–Dutta (1993)](https://doi.org/10.1080/00927879308824585).

The paper contains the full bibliography and explains which result supplies
each connection.


## Chebyshev parametrizations

Use the normalized Chebyshev polynomials $`C_n(t)=2T_n(t/2)`$, where $`T_n(\cos\theta)=\cos(n\theta)`$. Then

```math
\begin{aligned}
C_3(t)&=t^3-3t,\\
C_4(t)&=t^4-4t^2+2,\\
C_5(t)&=t^5-5t^3+5t,\\
C_7(t)&=t^7-7t^5+14t^3-7t.
\end{aligned}
```

The normalized Chebyshev trefoil $`(C_3,C_4,C_5)`$ is already covered by this repository: it is the image of the Shastri parametrization under the affine automorphism

```math
\begin{aligned}
M(x,y,z)&=(x,y+2,z-5x),\\
M^{-1}(x,y,z)&=(x,y-2,z+5x).
\end{aligned}
```

Its rectifier is $`\Psi=\Phi_T\circ M^{-1}`$, with inverse $`\Psi^{-1}=M\circ\Phi_T^{-1}`$. Thus $`\Psi(C_3(t),C_4(t),C_5(t))=(t,0,0)`$ over $`\mathbb Q(\sqrt{-3})`$.

The harmonic figure-eight treated here is exactly $`(C_3,C_5,C_7)`$. The identity

```math
C_3C_7-C_5^2+2=C_4
```

explains the modification $`(x,y,z)\mapsto(x,xz-y^2+2,y)`$ used in its construction. The transfer argument verifies polynomiality in both directions, including the exceptional fibre $`x=0`$.

For the real knot identifications $`H(3,4,5)`$ and $`H(3,5,7)`$, see Koseleff and Pecker, [*Chebyshev diagrams for two-bridge knots*](https://arxiv.org/abs/0909.3281), Introduction and Definition 1.2 ([journal DOI](https://doi.org/10.1007/s10711-010-9514-7)). The normalization above changes the parameter and ambient coordinates linearly.

**Scope.** These cases do not prove rectifiability of all Chebyshev or harmonic parametrizations. Further applications must verify that the complex parametrization is a closed embedding, find a coordinate restricting to the parameter, and meet the transfer theorem's hypotheses. Determining which further Chebyshev models admit this construction remains open here. Their real knot classification alone does not establish polynomial equivalence over $`\mathbb C`$.
