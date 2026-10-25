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

## Method in brief

Work over $K=\mathbb Q[a]/(a^2-a+1)\simeq\mathbb Q(\sqrt{-3})$.

1. **Start with a verified relative automorphism**
   $A=(x,H,W)$ and its explicit polynomial inverse.
2. **Transfer the coordinate** through
   $\beta(x,y,z)=(x,p(x,y)+m(x)z,y)$, where $m\ne0$.
   Modulo $m$, require the centre $H(x,p(x,y),y)$ to have an invertible linear
   coefficient and nilpotent higher coefficients. Finite inversion of this
   centre produces a polynomial correction $\varphi(x,T)$.
3. **Correct and divide exactly:**

   $$
   \mathcal A(x,y,z)=\left(
   x,\ H\circ\beta,\
   \frac{W\circ\beta-\varphi(x,H\circ\beta)}{m(x)}
   \right).
   $$

   Both this quotient and the corresponding inverse quotient are polynomial,
   including when $m$ has repeated roots.
4. **Pass from local to global identities.** After inverting $m$, the factors
   are explicitly reversible. Polynomiality in both directions and injectivity
   of localization give a global polynomial automorphism, including the fibres
   where $m=0$.
5. **Straighten the curve.** If
   $\mathcal A(\gamma(t))=(b(t),t,w(t))$, apply
   $(x,T,Q)\mapsto(T,x-b(T),Q-w(T))$ to obtain $(t,0,0)$.

The trefoil supplies the explicit base construction. For the harmonic model,
the transfer uses $m=x$ and $p=2-y^2$; the centre is $-y$ at $x=0$.
The full paper gives the formulas, both inverse maps, and the proof of each step.

The general lifting principle has classical antecedents; no novelty claim is
made for it. The paper explains the precise connections and cites the relevant
propositions.

## The verified curves

$$
\gamma_T(t)=(t^3-3t,\ t^4-4t^2,\ t^5-10t),
$$

$$
\gamma_H(t)=(t^3-3t,\ t^5-5t^3+5t,\ t^7-7t^5+14t^3-7t).
$$

The displayed rectifiers have component degrees $(5,15,24)$ and $(7,21,41)$,
respectively; minimality is not asserted. The harmonic model has **$+5t$** in
its second component. These are rectifications over $K$, hence over $\mathbb C$.

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
$\mathbb A^1_{\mathbb C}\hookrightarrow\mathbb A^3_{\mathbb C}$.

## Literature

- Original curves: [Shastri (1992), §3](https://doi.org/10.2748/tmj/1178227371); [Koseleff–Pecker (2011), Introduction](https://arxiv.org/abs/0909.3281).
- Plane theorem: [Abhyankar–Moh (1975)](https://doi.org/10.1515/crll.1975.276.148) and [Suzuki (1974)](https://doi.org/10.2969/jmsj/02620241).
- Spatial problem and coordinate lifts: [Craighero (1985), Introduction and Proposition 3](https://www.numdam.org/item/RSMUP_1985__74__115_0.pdf), including the precise locations of Abhyankar's Kyoto 1977 conjectures.
- Affine modifications: [Kaliman–Zaidenberg (1999), Proposition 2.1](https://arxiv.org/abs/math/9801076).
- Quotient inversion and exact division: [Edo–Vénéreau (2001)](https://doi.org/10.4064/ap76-1-6); [Edo–van den Essen–Maubach (2009), Lemma 1.1](https://arxiv.org/abs/0809.0767).
- Residual coordinates: [Bhatwadekar–Dutta (1993)](https://doi.org/10.1080/00927879308824585).

The paper contains the full bibliography and explains which result supplies
each connection.
