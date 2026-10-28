# Exact kernels, plinth ideals, and the full LND filtration of a coordinate transfer

Date: 26 October 2026. Working mathematical note, under verification.

This note proves an explicit result inside the coordinate-transfer class used in
the repository. It does not assert a new classification of all locally nilpotent
derivations, and it does not assert priority for the general mechanisms. No
motivic, K-theoretic, or homological-algebraic argument is used.

## 1. Setup and statement

Let k be a field of characteristic zero, R=k[x], A=R[y,z]. Let

    (H(Y,Z), W(Y,Z)) in Aut_R R[Y,Z],
    d = H_Y W_Z - H_Z W_Y in k*,
    beta(y,z) = (p(y)+m z, y),  p in R[y], 0 != m in R.

Write h=H(beta), w=W(beta), and

    D = h_z partial_y - h_y partial_z.

Take c=h(x,0,0), and let g in R be the monic greatest common divisor of the
coefficients of all nonconstant monomials in y,z in h. Define

    h0=(h-c)/g,   D0=(h0)_z partial_y - (h0)_y partial_z.

Then D=g D0. Both derivations are nonzero and locally nilpotent.

**Theorem.** The following hold.

1. g divides m in R. Put m1=m/g. Then

       ker D = ker D0 = B := R[h0].

2. For every monic irreducible pi dividing m1, let

       E_pi = ord_pi(m1),  kappa_pi = R/(pi),
       G_pi(y) = h0 mod pi.

   This reduction is independent of z and is a nonconstant polynomial in y.
   Let e_pi=deg_y G_pi >=1.

3. For n>=0 set F_n=ker(D^(n+1))=ker(D0^(n+1)). Then

       D^n(F_n) = a_n B,

       a_n = g^n product_{pi | m1} pi^[ E_pi ( n - floor(n/e_pi) ) ].

   Generators are understood up to nonzero constants in k. In particular,

       plinth(D) := D(A) intersect ker D
                   = (g q0) B,

       q0 = product_{e_pi >=2} pi^E_pi.

4. There are b_n in A, n>=0, with b_0=1, D-degree(b_n)=n and
   D^n(b_n)=a_n. They form a B-basis of A, and

       F_n = B b_0 direct_sum ... direct_sum B b_n.

   Here D-degree means max{j: D^j(f)!=0}, NOT the ordinary total degree of f.

5. A minimal local slice b_1 can be constructed by finite univariate inversion
   modulo the part of m1 supported on the primes with e_pi=1. Explicitly, if
   r is that monic part and q=m1/r, choose phi(T) in R[T] satisfying

       w == phi(h0) mod r.

   Then S=(w-phi(h0))/r belongs to A and

       D(S)=d g q,
       ker D^2 = B direct_sum B S.

   The scalar difference between q and the monic q0 does not affect the ideal.

The result includes nonreduced exceptional divisors and the cases in which the
original h fails to be primitive. All exponents E_pi are retained.

## 2. Generic coordinate, normalization, and saturation

Over K=k(x), beta is an automorphism. Consequently (h,w) is a coordinate system
of K[y,z], D is a nonzero invariant multiple of partial_w, and

    D(w)=d m,  D0(w)=d m1.

Since D=g D0 and D(w)=d m, the polynomial g divides m. Local nilpotence follows
over K[y,z] and descends to A by injectivity of A -> K[y,z]. Also

    ker(D on K[y,z]) = K[h] = K[h0].

By the definition of g, for every irreducible pi in R the polynomial h0 mod pi
is nonconstant in kappa_pi[y,z]. Hence the map

    (R/(pi))[T] -> A/(pi),   T |-> h0 mod pi

is injective: a nonconstant polynomial in a polynomial ring over a field is
transcendental over that field. Thus R[h0] is pi-saturated inside A:

    R[h0] intersect pi A = pi R[h0].

For f in A intersect K[h0], clear a denominator in R and cancel its irreducible
factors one at a time using this saturation. This proves

    A intersect K[h0] = R[h0],

and hence the kernel statement. This proof avoids assuming that the original
h itself generates the kernel.

The derivative identity

    (h0)_z = m1 H_Y(beta)

shows that modulo every divisor of m1, h0 is independent of z. Here division
by the positive integer exponents of z is legitimate since k has characteristic
zero. The same holds for w because w_z=m W_Y(beta).

Let G(y)=h0(x,y,0) and J(y)=w(x,y,0). If (P(T,V),Q(T,V)) is the inverse of
(H,W), then the exact polynomial identity

    Q(c+g G(y), J(y)) = y

holds already over R. In particular,

    R[G,J]=R[y],

and after any base change the pair (G,J) still generates the polynomial ring.
This is the key condition that rules out accidental rational dependence of J on
a nonlinear G in the plinth calculation.

## 3. The normalized one-step modification

Define

    F(T,V)=P(T,V)-p(Q(T,V)),
    N(T,V)=F(c+g T,V)/g.

We first justify that N is polynomial.

Modulo g, the identity H(p(y),y)=c+gG(y) gives H(p(y),y)=c. Inverting (H,W)
gives Q(c,J(y))=y. Thus J defines a polynomial automorphism of (R/(g))[y]:
over every residue field it has degree one with nonzero slope, its higher
coefficients are nilpotent, and its linear coefficient is a unit. Since
F(c,J(y))=0 modulo g and substitution by J is invertible, F(c,V)=0 modulo g.
The difference F(c+gT,V)-F(c,V) is also divisible by g. Therefore N is in R[T,V].
If g is a unit this argument is unnecessary and N is immediately polynomial.

Next, N does not vanish identically modulo any irreducible pi dividing m1.
If pi does not divide g, this follows from the invertible affine substitution
T |-> c+gT and the fact that F is an R-coordinate.
If pi divides g, then over kappa_pi the coordinate H-c vanishes on the graph
Y=p(Z). Both H-c and Y-p(Z) are irreducible, so

    H-c = u (Y-p(Z)),  u in kappa_pi*.

After the inverse coordinate change, F(T,V)=u^(-1)(T-c) modulo pi. Since

    N_T(T,V)=F_T(c+gT,V),

we get N_T=u^(-1) modulo pi, so N mod pi is not zero. Hence gcd(m1,N)=1.

The map

    R[T,V,Z0]/(m1 Z0-N(T,V)) -> A,
    T |-> h0, V |-> w, Z0 |-> z

is surjective: y=Q(c+g h0,w) lies in its image. It becomes an isomorphism over
K. The defining polynomial is primitive and irreducible, since it is linear
in Z0 and gcd(m1,N)=1. Its quotient is a domain and injects into its
localization over K. Therefore the displayed map is an isomorphism.

This normalization step is important: simply replacing h by h0 without
justifying N/g would leave a gap.

## 4. Local monic normal form at one exceptional prime

Fix pi|m1, put E=ord_pi(m1), O=R_(pi), and write m1=u pi^E with u a unit
of O. Localize ONLY R here: the coefficient ring is O[T], not the localization
of R[T] at its height-one prime (pi). Thus points with additional conditions
on T are retained.

Let C=O/(pi^E). The normalized presentation of Section 3 and the independence
of h0,w from z modulo pi^E give

    C[T,V]/(N)  ~=  C[y],   T |-> G(y), V |-> J(y).

For precision, after adjoining the same variable z on both sides this is the
reduction of the isomorphism in Section 3. That isomorphism fixes z. Taking
the quotient by the ideal generated by z on both sides gives the asserted
isomorphism before adjoining z.

Put e=deg(G mod pi). Then C[y] is free of rank e over C[G], with basis
1,y,...,y^(e-1), and C[G] is naturally C[T]. This can be proved without a
formal Weierstrass theorem:

* Modulo pi, ordinary division by the degree-e polynomial G-T proves spanning.
* Lift that reduction and apply it to the remaining pi-multiple. After E
  iterations the remainder vanishes, proving spanning over C.
* For linear independence, suppose a relation has a nonzero coefficient and
  let r<E be the minimum pi-order among all its coefficients. Lift the
  relation to O, divide the lifted equality by pi^r, and reduce modulo pi.
  This gives a nonzero relation among 1,y,...,y^(e-1) over
  kappa_pi[G_pi], a contradiction. Equivalently one can induct on E using
  lifts modulo pi^(E-r). No cancellation of a zero divisor inside C is used.

The identity Q(c+gG,J)=y shows that J generates C[y] as a C[T]-algebra. Let
P_pi(T,V) be the characteristic polynomial of multiplication by J on the free
rank-e C[T]-module C[y]. It is monic of V-degree e. Cayley-Hamilton and the
generation statement give a surjection

    C[T,V]/(P_pi) -> C[y]

between free rank-e C[T]-modules. Such a surjection is an isomorphism (its
matrix has a right inverse, so its determinant is a unit). Thus the two
principal ideals (N) and (P_pi) agree in C[T,V].

Choose any monic lift P_pi to O[T,V], still of V-degree e. There are
polynomials a,b,c1,d1 over O[T,V] such that

    P_pi = a N + pi^E b,
    N    = c1 P_pi + pi^E d1.

These TWO identities, rather than inversion of a polynomial unit only modulo
pi^E, imply equality of the modification subalgebras:

    A tensor_R O
      = O[h0,w,N(h0,w)/pi^E]
      = O[h0,w,P_pi(h0,w)/pi^E].

Write v=P_pi(h0,w)/pi^E. Thus the local algebra has the exact presentation

    O[T,V,U]/(P_pi(T,V)-pi^E U).

Since P_pi is monic of V-degree e, this algebra is free over O[T] with basis

    V^i U^j,  0<=i<e, j>=0.

## 5. Local filtration and exact image ideals

Over K[h0,w], D0=d m1 partial_w. For n=ej+i with 0<=i<e,

    w^i v^j = pi^(-Ej) w^n + lower w-degree terms.

Consequently this basis element has D0-degree exactly n and

    D0^n(w^i v^j) = n! (d u)^n pi^[E(n-j)].

The basis elements have distinct D-degrees. Therefore there can be no
cancellation of their highest D-degree terms when the coefficients lie in
O[h0]. It follows that the local nth filtration term is precisely the span
of the basis elements with i+ej<=n and

    D0^n(ker D0^(n+1)) tensor_R O
      = pi^[E(n-floor(n/e))] O[h0].

At a prime pi not dividing m1, A tensor_R O=O[h0,w] and D0(w)=d m1 is a unit.
The corresponding image ideal is the whole O[h0].

Kernels and images here commute with localization because D0 is R-linear.
Equality of two R-submodules is detected after localization at every maximal
ideal of R. In particular, all the local equalities above imply the global
formula for D0. This argument preserves possible codimension-two support in
Spec R[h0]; it does not replace O[h0] by a field in h0.

Finally D^n=g^n D0^n and the kernels of their powers agree. This proves the
formula for D and all n>=0.

## 6. Global basis and an explicit minimal local slice

The B-linear map D^n:F_n->B has kernel F_(n-1) and image a_n B. Choose
b_n in F_n with D^n(b_n)=a_n. Since a_n is nonzero,

    F_n=F_(n-1) direct_sum B b_n.

Induction, followed by the union of the filtration, proves the free B-basis
claim. Existence of such a basis for rank-at-most-two LNDs has known precedents;
the explicit a_n is what is being computed in this transfer presentation.

For n=1 the general formula gives the plinth ideal. It also has a direct
constructive proof. Let r be the part of m1 supported on the primes with
e_pi=1. In (R/(r))[y], the reduction of G is an automorphism: its linear
coefficient is a unit, all higher coefficients are nilpotent. Compute its
inverse L(T) by finite nilpotent iteration, and set

    phi(T)=J(L(T)) mod r.

Then w-phi(h0) is divisible by r in A, and

    S=(w-phi(h0))/r,   D(S)=d g (m1/r).

If r=1 take phi=0. Dividing S by a suitable nonzero constant gives b_1.
The identity ker D^2=B direct_sum B S follows by subtracting a B-multiple
of S from any element whose D-image lies in B.

The lower bound can be checked directly at a bad prime without the whole
filtration. If D0(f)=P(h0), and ord_pi P=e0<E, write P=pi^e0 P0. Then

    pi^(E-e0) f - P0(h0) w/(d u) in O[h0].

Reduction modulo pi implies J_pi is rational in G_pi. But
kappa_pi[G_pi,J_pi]=kappa_pi[y], so this would give
kappa_pi(G_pi)=kappa_pi(y), contradicting deg G_pi>=2. Thus pi^E divides
every P in the plinth ideal. This independently explains the full
multiplicity retained at every bad prime.

## 7. Geometric interpretation

For the primitive quotient map (x,h0), over pi|m1 the boundary equation is

    G_pi(y)=lambda,

with z free. Over an algebraic closure and for lambda outside the finite
critical-value set, this fiber is the disjoint union of e_pi affine lines.
The field-extension degree is e_pi. Thus e_pi=1 is exactly the good boundary
condition in this class. The multiplicity E_pi controls the additional
valuation cost in higher derivative images.

The factor g records a different phenomenon: scaling a primitive LND by a
base polynomial. It multiplies the nth image ideal by g^n even when the
primitive quotient has a good fiber. Kernel geometry and scaling of the
vector field should therefore be kept separate.

The derivation D0 is irreducible: any common factor of (h0)_y and (h0)_z
divides D0(w)=d m1, hence is a factor in R. Such a prime would make h0
constant modulo that prime, contradicting primitiveness. This verifies the
irreducibility hypothesis appearing in several general plinth theorems.

### Intrinsic extraction of the boundary degrees

For a bad prime pi the valuation sequence of the image ideals is

    ord_pi I_n(D0)=E_pi(n-floor(n/e_pi)).

Thus E_pi=ord_pi I_1(D0), and e_pi is the smallest n>=2 for which
ord_pi I_n(D0)<n ord_pi I_1(D0). The boundary degree is therefore recoverable
from the LND filtration, rather than being an auxiliary choice of transfer.

For example, the derivations

    D_(M,e)=x^M partial_y-e y^(e-1) partial_z,  M>=1, e>=2,

have kernel k[x,y^e+x^M z] and plinth ideal (x^M). Their nth image ideals
are (x^[M(n-floor(n/e))]). For fixed M these derivations are pairwise
nonconjugate under polynomial automorphisms: e is exactly the first n for
which I_n(D) strictly contains plinth(D)^n, an intrinsic property preserved
under conjugacy. The integer M is also preserved, as the multiplicity of
the unique prime factor of the plinth ideal in the polynomial kernel.
Consequently distinct pairs (M,e) give nonconjugate derivations in this family.
This is an explicit consequence in a classical family, not a claim that these
invariants classify arbitrary LNDs.

For any nonzero a in B, the invariant multiple aD has the same kernel and
filtration and I_n(aD)=a^n I_n(D). Thus the formula also covers these replicas.

## 8. Explicit higher-order example

Take

    h=y^2+x y^3+x^2 z,
    D=x^2 partial_y-(2y+3x y^2) partial_z.

Here g=1, m=x^2, e_x=2. A monic relation modulo x^2 is

    P(T,V)=V^2+x T V-T.

The polynomial

    v=P(h,y)/x^2 = y^4+x y z-z

satisfies

    D(v)=2y+x h,   D^2(v)=2x^2.

The inverse expression is polynomial:

    z=-(1+xy)v+h y^2.

Thus A is free over k[x,h] with basis

    1, y, v, yv, v^2, yv^2, ...,

and the successive image ideals have generators

    1, x^2, x^2, x^4, x^4, x^6, x^6, ... .

The higher term x y^3 increases the ordinary degree of h, but it does not
increase the residue degree e_x. This illustrates why a generic-degree-only
analysis misses the relevant filtration structure.

For H(4,5,7), the familiar parameter polynomial

    h=(x^2-2)z-y^3+3y

has g=1 and e_pi=3 at both geometric roots of x^2-2. Hence

    ker D = k[x,h],
    plinth(D)=(x^2-2) k[x,h],
    D^n(F_n)=(x^2-2)^[n-floor(n/3)] k[x,h].

This describes that specific LND. It is not an obstruction to every possible
coordinate lift of the harmonic curve.

## 9. Relation to the literature and limits

The general coordinate/slice criterion is classical: see van den Essen and
van Rossum, Coordinates in two variables over a Q-algebra (2004), and its
reproduction as Theorem 3.2 in Edo--van den Essen--Maubach, arXiv:0809.0767.

Daigle--Freudenburg's work on LNDs over UFDs and the rank-two theory provide
the broader context for polynomial kernels. Freeness over the kernel in
rank at most two has been studied independently; this note supplies a direct
proof for the present transfer class and explicitly computes its image ideals.

Masuda, Factorial affine Ga-varieties with principal plinth ideals,
arXiv:2312.05455, and the 2025 work arXiv:2512.06687 relate affine
modifications, plinth divisors and the field degrees of boundary quotients.
The degree e_pi above is the concrete field degree in this presentation.
No claim of new general geometric criterion is made.

The theorem is not a classification of all harmonic embeddings, and failure
of the good-boundary condition for one transfer does not imply that a curve
is nonrectifiable. The theorem concerns the displayed D, its kernel and its
filtration exactly.

The script verify_transfer_filtration.py creates certificates.json using
exact rational arithmetic. It verifies examples with a good repeated prime,
a bad repeated prime, mixed good/bad primes, nonprimitive h, nonlinear input
automorphisms, an irreducible quadratic prime, and varying residue degrees.
Its tests support the implementation; the general theorem rests on the
proof above, not on a finite sample.
