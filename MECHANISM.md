# Polynomial rectification by exact division and transfer of coordinates

This document explains the algebra behind `verify.py`. It gives explicit polynomial automorphisms and polynomial inverses for the two parametrizations

$$
\gamma_T(t)=(t^3-3t,\ t^4-4t^2,\ t^5-10t)
$$

and

$$
\gamma_H(t)=(t^3-3t,\ t^5-5t^3+5t,\ t^7-7t^5+14t^3-7t).
$$

The second component of the harmonic model contains **$5t$**. Replacing it by $4t$ changes the curve and is outside the result verified here.

The document also proves a sufficient general transfer principle that explains the passage from the first construction to the second. It gives an explicit implementation within the established theory of affine modifications and residual coordinates; see the sources below. That principle has specific input hypotheses; it is not a solution of the rectification problem for arbitrary embeddings of the affine line into affine three-space.

## 1. Coefficient field and the meaning of verification

Let

$$
K=\mathbb Q[a]/(a^2-a+1).
$$

The quadratic polynomial is irreducible over $\mathbb Q$, so $K$ is a field. It embeds into $\mathbb C$ by choosing

$$
a=\frac{1+i\sqrt3}{2}.
$$

Every coefficient calculation can be performed by reducing powers of $a$ using $a^2=a-1$. In particular,

$$
a(1-a)=1.
$$

The code works with rational coefficients and this exact relation. It does not approximate complex numbers. The variable $t$ is also symbolic, so substituting a parametrization checks a polynomial identity in $K[t]$.

We call a map a **polynomial automorphism** only when it has a polynomial inverse. The proof below uses both composition identities. The Jacobian computations are additional checks, not the criterion used to infer invertibility.

All auxiliary polynomials introduced below are explicitly defined. The letters $(X,Y,Z)$ denote the input coordinates of the final inverse maps.

## 2. The common polynomial automorphism

Define

$$
\begin{aligned}
H(x,y,z)={}&ax^3y^2+2x^2yz+(1-a)xz^2\\
&+\bigl((a-1)x^3-ax\bigr)y
  +(-1+ax^2-ax^4)z\\
&-2x^5+(6-2a)x^3-2(1-a)x,
\end{aligned}
$$

and the polynomial in two arguments

$$
\begin{aligned}
f(x,T)={}&-T+x\bigl((1-a)T^2+2a-2\bigr)\\
&+x^2(2aT^3-5aT)
  +x^3(-5T^4+15T^2-2a)\\
&+x^4\bigl(14(1-a)T^5+50(a-1)T^3+(29-24a)T\bigr).
\end{aligned}
$$

Set

$$
W(x,y,z)=\frac{a\bigl(axy+z-f(x,H(x,y,z))\bigr)}{x^5}.
$$

This is a polynomial: the numerator is exactly divisible by $x^5$ in $K[x,y,z]$. The script checks this before constructing the quotient. This displayed division is an algebraic definition by exact polynomial division, not a pointwise evaluation of a rational expression at $x=0$.

The inverse is also explicit. First define

$$
\chi(x,T)=\frac{a\bigl(T-H(x,0,f(x,T))\bigr)}{x^5},
$$

whose numerator is again exactly divisible by $x^5$. Then put

$$
\begin{aligned}
R(x,T,V)={}&-\chi(x,T)\\
&+\bigl(-1+ax^2-ax^4+2(1-a)xf(x,T)\bigr)V\\
&+(1-a)^2x^6V^2,
\end{aligned}
$$

$$
S(x,T,V)=f(x,T)+(1-a)x^5V-axR(x,T,V).
$$

The resulting maps are

$$
A_0(x,y,z)=(x,H(x,y,z),W(x,y,z)),
$$

$$
A_0^{-1}(x,T,V)=(x,R(x,T,V),S(x,T,V)).
$$

### A finite certificate for both composition identities

The exact calculations check

$$
x^5W(x,y,z)=a\bigl(axy+z-f(x,H(x,y,z))\bigr),
\tag{1}
$$

$$
H(x,R(x,T,V),S(x,T,V))=T,
\tag{2}
$$

$$
axR(x,T,V)+S(x,T,V)-f(x,T)=(1-a)x^5V,
\tag{3}
$$

and

$$
R(x,H(x,y,z),W(x,y,z))=y,
\tag{4}
$$

$$
S(x,H(x,y,z),W(x,y,z))=z.
\tag{5}
$$

Substitution of $R,S$ into (1), followed by (2) and (3), gives

$$
x^5W(x,R,S)=a(1-a)x^5V=x^5V.
$$

Cancellation of $x^5$ in the integral domain $K[x,T,V]$ proves $W(x,R,S)=V$. Together with (2), this proves $A_0\circ A_0^{-1}=\mathrm{id}$. Equations (4) and (5) prove $A_0^{-1}\circ A_0=\mathrm{id}$.

Thus the large third component of one composition need not be expanded separately. Its value follows from a checked polynomial certificate and cancellation in a polynomial ring. No fibre has been deleted.

In the script, `f`, `R`, and `S` use the names `y,z` for their second and third arguments; a call to `at` performs the simultaneous substitution corresponding to the displayed arguments $T,V$.

## 3. Rectifying the trefoil parametrization

The affine normalization

$$
M(x,y,z)=(x,y+2,z-5x),\qquad
M^{-1}(x,y,z)=(x,y-2,z+5x)
$$

maps the original parametrization to

$$
M(\gamma_T(t))=(t^3-3t,\ t^4-4t^2+2,\ t^5-5t^3+5t).
$$

Define

$$
h_T(x,y,z)=H(x,y+2,z-5x),\qquad
w_T(x,y,z)=W(x,y+2,z-5x).
$$

Exact substitution gives

$$
h_T(\gamma_T(t))=t,\qquad
w_T(\gamma_T(t))=8-14t^2.
$$

Consequently the final rectifier is

$$
\Phi_T(x,y,z)=
\bigl(h_T(x,y,z),\ x-h_T(x,y,z)^3+3h_T(x,y,z),\
w_T(x,y,z)-8+14h_T(x,y,z)^2\bigr).
$$

Its inverse is

$$
\begin{aligned}
(\Phi_T^{-1})_1(X,Y,Z)&=X^3-3X+Y,\\
(\Phi_T^{-1})_2(X,Y,Z)&=
R(X^3-3X+Y,X,Z+8-14X^2)-2,\\
(\Phi_T^{-1})_3(X,Y,Z)&=
S(X^3-3X+Y,X,Z+8-14X^2)+5(X^3-3X+Y).
\end{aligned}
$$

To see both compositions without expanding unnecessarily large expressions, write

$$
L_T(x,T,V)=(T,x-T^3+3T,V-8+14T^2).
$$

Then

$$
L_T^{-1}(X,Y,Z)=(X^3-3X+Y,X,Z+8-14X^2),
$$

and

$$
\Phi_T=L_T\circ A_0\circ M,\qquad
\Phi_T^{-1}=M^{-1}\circ A_0^{-1}\circ L_T^{-1}.
$$

Every factor here is a global polynomial automorphism. Therefore

$$
\Phi_T(\gamma_T(t))=(t,0,0).
$$

The verified component degrees are $(5,15,24)$, and the determinant of the final Jacobian is $+1$. These are the degrees of the displayed construction; minimality is not asserted.

## 4. Transferring the construction to the harmonic model

Consider the polynomial modification

$$
\beta(x,y,z)=(x,xz-y^2+2,y).
$$

It has the inverse

$$
\beta^{-1}(x,Y,Z)=\left(x,Z,\frac{Y+Z^2-2}{x}\right)
$$

after $x$ has been inverted. The map $\beta$ itself is not an automorphism of the whole affine space. The purpose of the next correction is to make the **complete composite** and its inverse polynomial.

The parametrizations satisfy the exact identity

$$
\beta(\gamma_H(t))=M(\gamma_T(t)).
$$

Define the correction

$$
\varphi(T)=42(a-1)T^6+175(1-a)T^4+(147a-161)T^2+8.
$$

Set

$$
h_H(x,y,z)=H(x,xz-y^2+2,y),
$$

$$
q_H(x,y,z)=
\frac{W(x,xz-y^2+2,y)-\varphi(h_H(x,y,z))}{x}.
$$

The second formula is a polynomial because its entire numerator is divisible by $x$. The script verifies that divisibility coefficient by coefficient.

The proposed inverse of $(x,h_H,q_H)$ is

$$
\left(
x,\ S(x,T,xQ+\varphi(T)),\
\frac{R(x,T,xQ+\varphi(T))+S(x,T,xQ+\varphi(T))^2-2}{x}
\right).
\tag{6}
$$

The numerator in (6) is also exactly divisible by $x$. This second divisibility is essential: proving polynomiality in only one direction would not establish a polynomial automorphism.

### Why the identities include the fibre $x=0$

After adjoining $1/x$, introduce

$$
C(x,T,V)=\left(x,T,\frac{V-\varphi(T)}x\right),\qquad
C^{-1}(x,T,Q)=(x,T,xQ+\varphi(T)).
$$

The relative harmonic map is exactly

$$
(x,h_H,q_H)=C\circ A_0\circ\beta.
$$

Formula (6) is exactly $\beta^{-1}\circ A_0^{-1}\circ C^{-1}$. The two maps therefore have both composition identities over $K[x,1/x]$.

Their components have already been proved polynomial. The map

$$
K[x,y,z]\longrightarrow K[x,1/x,y,z]
$$

is injective. Hence both composition identities hold in $K[x,y,z]$ itself. They hold on the fibre $x=0$ as well. This argument does not evaluate $1/x$ at zero: it proves equalities between polynomials by an injective ring homomorphism.

### The final harmonic rectifier and its inverse

Exact curve substitution gives

$$
h_H(\gamma_H(t))=t,\qquad
q_H(\gamma_H(t))=(1-a)(42t^3-49t).
$$

Thus

$$
\begin{aligned}
\Phi_H(x,y,z)=\bigl(&h_H(x,y,z),\
x-h_H(x,y,z)^3+3h_H(x,y,z),\\
&q_H(x,y,z)-(1-a)(42h_H(x,y,z)^3-49h_H(x,y,z))\bigr)
\end{aligned}
$$

satisfies $\Phi_H(\gamma_H(t))=(t,0,0)$.

For an explicit inverse, denote the second and third polynomial components of (6) by $R_H(x,T,Q)$ and $S_H(x,T,Q)$. These names refer to the complete formulas in (6), including its verified exact division. Then

$$
\begin{aligned}
(\Phi_H^{-1})_1(X,Y,Z)&=X^3-3X+Y,\\
(\Phi_H^{-1})_2(X,Y,Z)&=
R_H\bigl(X^3-3X+Y,X,Z+(1-a)(42X^3-49X)\bigr),\\
(\Phi_H^{-1})_3(X,Y,Z)&=
S_H\bigl(X^3-3X+Y,X,Z+(1-a)(42X^3-49X)\bigr).
\end{aligned}
$$

The last step is the polynomial automorphism

$$
L_H(x,T,Q)=(T,x-T^3+3T,Q-(1-a)(42T^3-49T)),
$$

with the explicitly substituted inverse appearing above. Therefore it preserves the already proved two-sided invertibility.

The verified component degrees of $\Phi_H$ are $(7,21,41)$. The relative map $(x,h_H,q_H)$ has Jacobian determinant $+1$; the final permutation of its first two coordinates changes the determinant to $-1$.

## 5. A sufficient general transfer principle

This section states the algebraic principle independently of the particular formulas above. Let $k$ be a field of characteristic zero; in the applications $k=K$. Suppose that an automorphism and its inverse are given:

$$
A(x,y,z)=(x,H(x,y,z),W(x,y,z)),\qquad
A^{-1}(x,T,V)=(x,R(x,T,V),S(x,T,V)).
$$

Let $0\ne m(x)\in k[x]$ and $p(x,y)\in k[x,y]$. Assume first that $\deg m>0$. Work in the finite ring

$$
B=k[x]/(m(x)),
$$

and write the centre polynomial as

$$
c(y)=H(x,p(x,y),y)=c_0+c_1y+\sum_{j=2}^d c_jy^j\quad\text{in }B[y].
$$

**Sufficient hypothesis.** The coefficient $c_1$ is a unit in $B$, and every coefficient $c_j$ with $j\ge2$ is nilpotent in $B$.

Equivalently, after extending the field to an algebraic closure, the polynomial $H(r,p(r,y),y)$ has degree exactly one for every root $r$ of $m$. The statement in terms of $B$ allows the construction over the original coefficient field, without choosing or numerically computing these roots.

Under this hypothesis, $H(x,p(x,y)+m(x)z,y)$ extends to a polynomial automorphism preserving $x$, and both that automorphism and its inverse can be constructed by finite polynomial operations.

### Finite construction of the correction

Let $J=(c_2,\ldots,c_d)\subseteq B$. Choose a positive integer $e$ with $J^e=0$. Such an integer exists. For example, factor $m$ into distinct irreducibles over $k$ and take the largest exponent occurring in that factorization; the nilradical of $B$ has vanishing $e$th power.

In $B[T]$, define

$$
\psi_0(T)=c_1^{-1}(T-c_0),
$$

$$
\psi_{j+1}(T)=c_1^{-1}
\left(T-c_0-\sum_{\ell=2}^d c_\ell\psi_j(T)^\ell\right),
\qquad 0\le j<e.
$$

Every step is finite; coefficients can be reduced modulo the **full polynomial $m$** after each step.

The difference $\psi_{j+1}-\psi_j$ belongs to $J^{j+1}[T]$. This follows inductively because a difference of powers is divisible by the difference of its arguments and every nonlinear coefficient belongs to $J$. Thus the sequence has stabilized by the stated number of steps, and its fixed-point equation gives

$$
c(\psi_e(T))=T.
$$

It also gives $\psi_e(c(y))=y$. Indeed, $c(v)-c(y)$ is $v-y$ times a polynomial of the form $c_1+n$, with $n\in J B[y,v]$. After substitution of $v=\psi_e(c(y))$, this factor is a unit: its inverse is a finite geometric sum because $J$ is nilpotent. Cancellation of that unit proves the other identity.

Choose any polynomial representative $\varphi(x,T)\in k[x,T]$ of the class

$$
W\bigl(x,p(x,\psi_e(T)),\psi_e(T)\bigr)\quad\text{in }B[T].
$$

For example, take the remainder of degree less than $\deg m$ in $x$.

### The two polynomial maps

The transferred map is

$$
\mathcal A(x,y,z)=\left(
x,\ H(x,p(x,y)+m(x)z,y),\
\frac{W(x,p(x,y)+m(x)z,y)
-\varphi(x,H(x,p(x,y)+m(x)z,y))}{m(x)}
\right).
\tag{7}
$$

Its inverse is

$$
\mathcal A^{-1}(x,T,Q)=\left(
x,\ S(x,T,m(x)Q+\varphi(x,T)),\
\frac{R(x,T,m(x)Q+\varphi(x,T))
-p(x,S(x,T,m(x)Q+\varphi(x,T)))}{m(x)}
\right).
\tag{8}
$$

Both quotients are exact polynomial divisions.

For (7), the identities for $c$ and $\psi_e$ imply, modulo $m$,

$$
\varphi(x,H(x,p(x,y),y))=W(x,p(x,y),y).
$$

Replacing $p(x,y)$ by $p(x,y)+m(x)z$ does not change this congruence. The numerator in (7) is therefore divisible by $m$.

For (8), apply the given inverse $A^{-1}$ to the pair

$$
\bigl(H(x,p(x,\psi_e(T)),\psi_e(T)),
W(x,p(x,\psi_e(T)),\psi_e(T))\bigr)
=\bigl(T,\varphi(x,T)\bigr)
$$

in $B[T]$. This gives

$$
R(x,T,\varphi(x,T))=p(x,\psi_e(T)),\qquad
S(x,T,\varphi(x,T))=\psi_e(T).
$$

The congruences remain valid when $\varphi(x,T)$ is replaced by $m(x)Q+\varphi(x,T)$. The numerator in (8) is consequently divisible by the full $m$, including all multiplicities.

After inverting $m$, (7) is the composition

$$
(x,y,z)\mapsto(x,p(x,y)+m(x)z,y)
\mapsto A(x,p(x,y)+m(x)z,y)
\mapsto\left(x,T,\frac{V-\varphi(x,T)}{m(x)}\right).
$$

Formula (8) reverses these steps. Hence both compositions are identities after localization. Their components are polynomial by the two divisibility arguments, and the injectivity

$$
k[x,y,z]\hookrightarrow k[x,1/m,y,z]
$$

proves the identities globally.

If $m$ is a nonzero constant, take $\varphi=0$: the modification is already a polynomial automorphism and both quotients in (7) and (8) are divisions by a scalar. This treats the remaining case.

Changing the lift $\varphi$ to $\varphi+mD(x,T)$ changes the new third component by $-D(x,\mathcal A_2)$. This is a polynomial shear, so the choice of representative does not affect the existence of the transferred automorphism.

### How the harmonic example fits the principle

Take $A=A_0$, $m(x)=x$ and $p(x,y)=2-y^2$. Since

$$
H(0,y,z)=-z,
$$

the centre polynomial is $H(0,2-y^2,y)=-y$. It has the inverse $\psi(T)=-T$. The correction used in Section 4 is the exact remainder

$$
\varphi(T)=W(0,2-T^2,-T).
$$

Thus this example satisfies the sufficient condition on its exceptional fibre. The two divisibility checks in `verify.py` verify the resulting forward and inverse formulas directly.

More generally, for this same base coordinate $H$, every choice $m=x^N$ with $N\ge1$ and every $p\in K[x,y]$ satisfies the condition: reduction modulo the nilradical gives the same centre $-y$. The general theorem therefore supplies a transferred coordinate in these cases. It does not assert that an arbitrary curve can be placed into this form while retaining its parameter.

## 6. From a relative coordinate to a straight line

The last step used in both examples has a simple general form. Suppose

$$
A=(x,H,W),\qquad A^{-1}=(x,R,S)
$$

are polynomial inverses, and a parametrized curve

$$
\gamma(t)=(b(t),c(t),d(t))
$$

satisfies $H(\gamma(t))=t$. Define the one-variable polynomial $w(t)=W(\gamma(t))$. Then

$$
\Phi(x,y,z)=\bigl(H(x,y,z),\ x-b(H(x,y,z)),\ W(x,y,z)-w(H(x,y,z))\bigr)
$$

has the inverse

$$
\Phi^{-1}(X,Y,Z)=\bigl(
Y+b(X),\ R(Y+b(X),X,Z+w(X)),\ S(Y+b(X),X,Z+w(X))
\bigr).
$$

These are a coordinate permutation and polynomial shears composed with the given automorphism. Substitution proves $\Phi(\gamma(t))=(t,0,0)$. The hypothesis that $H$ belongs to an already verified automorphism is essential; an arbitrary polynomial satisfying only $H(\gamma(t))=t$ would not justify this step.

## 7. What the executable checks establish

`verify.py` performs the following exact operations:

1. It constructs $W$ and $\chi$ by division on monomials, rejecting a nonzero remainder after reduction by $a^2-a+1$.
2. It checks (1)–(5), which prove both inverse identities of the base map by the cancellation argument above.
3. It checks the affine normalization and final shears for the trefoil.
4. It checks exact divisibility of both harmonic formulas. Their explicit factorization, together with the proved base inverse and injective localization, proves both harmonic composition identities.
5. It substitutes each parametrization into its final rectifier and checks all three resulting components against $(t,0,0)$.
6. It substitutes $(t,0,0)$ into each inverse and checks the resulting parametrization.
7. It checks the stated component degrees and relative Jacobian determinants.

The general transfer proof in Section 5 is a mathematical argument. Running two concrete examples does not replace that proof. Likewise, the executable uses finite certificates and composition factorizations; it does not literally expand every component of both high-degree final compositions in one step.

The result is an exact computer-assisted verification supported by the algebraic deductions written here. It has not been formalized in Lean. It depends on the correctness of the stated formulas, the checking code, and the exact polynomial arithmetic implementation.

## 8. Scope

The two displayed maps rectify the specified curves over $K$, hence over $\mathbb C$. Their coefficients are not all real, so these formulas do not provide rectification by real polynomial automorphisms. No assertion about the real knot type is inferred from the complex rectification.

This repository does not claim a general solution for all embeddings $\mathbb A^1_{\mathbb C}\hookrightarrow\mathbb A^3_{\mathbb C}$, a new orbit under the full automorphism group, literature priority, minimal degrees, or a classification of these automorphisms as tame or wild. Its concrete output is the pair of explicit polynomial rectifiers, their polynomial inverses, and reproducible exact certificates for the stated identities.


## 9. Sources and prior constructions

The source of the trefoil is [Shastri (1992), §3, Example 1](https://doi.org/10.2748/tmj/1178227371). The harmonic model is the scaled Chebyshev curve $H(3,5,7)$ described by [Koseleff–Pecker (2011)](https://arxiv.org/abs/0909.3281):

$$
\gamma_H(t)=\bigl(2T_3(t/2),2T_5(t/2),2T_7(t/2)\bigr).
$$

The transfer in Section 5 is an explicit application of the lifting principle for affine modifications in [Kaliman–Zaidenberg, Proposition 2.1](https://arxiv.org/abs/math/9801076). For the quotient-ring construction, see [Edo–Vénéreau, Proposition 1 and Theorem 4](https://doi.org/10.4064/ap76-1-6), and [Edo–van den Essen–Maubach, Lemma 1.1](https://arxiv.org/abs/0809.0767). Existence of a companion also follows from the [Bhatwadekar–Dutta residual-variable theorem](https://doi.org/10.1080/00927879308824585).

The paper's Methods section explains these connections, states the embedding problem with its historical sources, and provides the full bibliography. The general lifting principle is not claimed as new.


## Chebyshev parametrizations

Use the normalized Chebyshev polynomials $C_n(t)=2T_n(t/2)$, where $T_n(\cos\theta)=\cos(n\theta)$. Then

$$
C_3=t^3-3t,\quad C_4=t^4-4t^2+2,\quad
C_5=t^5-5t^3+5t,\quad C_7=t^7-7t^5+14t^3-7t.
$$

The normalized Chebyshev trefoil $(C_3,C_4,C_5)$ is already covered by this repository: it is the image of the Shastri parametrization under the affine automorphism

$$
M(x,y,z)=(x,y+2,z-5x),\qquad M^{-1}(x,y,z)=(x,y-2,z+5x).
$$

Its rectifier is $\Psi=\Phi_T\circ M^{-1}$, with inverse $\Psi^{-1}=M\circ\Phi_T^{-1}$. Thus $\Psi(C_3(t),C_4(t),C_5(t))=(t,0,0)$ over $\mathbb Q(\sqrt{-3})$.

The harmonic figure-eight treated here is exactly $(C_3,C_5,C_7)$. The identity

$$
C_3C_7-C_5^2+2=C_4
$$

explains the modification $(x,y,z)\mapsto(x,xz-y^2+2,y)$ used in its construction. The transfer argument verifies polynomiality in both directions, including the exceptional fibre $x=0$.

For the real knot identifications $H(3,4,5)$ and $H(3,5,7)$, see Koseleff and Pecker, [*Chebyshev diagrams for two-bridge knots*](https://arxiv.org/abs/0909.3281), Introduction and Definition 1.2 ([journal DOI](https://doi.org/10.1007/s10711-010-9514-7)). The normalization above changes the parameter and ambient coordinates linearly.

**Scope.** These cases do not prove rectifiability of all Chebyshev or harmonic parametrizations. Further applications must verify that the complex parametrization is a closed embedding, find a coordinate restricting to the parameter, and meet the transfer theorem's hypotheses. Determining which further Chebyshev models admit this construction remains open here. Their real knot classification alone does not establish polynomial equivalence over $\mathbb C$.


## Acknowledgements

The author expresses his sincere gratitude to Alexei Kanel-Belov and Alexander Frolov.
