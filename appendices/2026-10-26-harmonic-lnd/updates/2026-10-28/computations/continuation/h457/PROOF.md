# H(4,5,7): obstruction through total degree four for every original projection

Date: 26 October 2026. Working result for independent review.

No motives, K-theory, or homological algebra are used. The only structural
input is the classical degree-reduction theorem for polynomial automorphisms
of the affine plane (Jung–van der Kulk). Everything specific to the curve
below is an exact calculation over the rational numbers.

## 1. Statement and limits

Let k be any field of characteristic zero, and use the monic normalization
C_n(t)=2T_n(t/2). Let

    gamma(t) = (C4(t),C5(t),C7(t))
             = (t^4−4t²+2, t^5−5t³+5t, t^7−7t^5+14t³−7t).

For F in k[x,y,z], suppose F(gamma(t))=t and deg(F)≤4, where deg is ordinary
total degree in all three variables.

**Theorem.**

1. If F is a coordinate of k(x)[y,z], then
   F=F0=(x²−2)z−y³+3y.
2. No such F is a coordinate of k(y)[x,z].
3. No such F is a coordinate of k(z)[x,y].
4. Consequently no such F is a relative coordinate over k[x], k[y], or k[z].

Thus any construction that first completes one of the pairs (x,F), (y,F),
(z,F) to a polynomial coordinate system must use deg(F)≥5. This includes
the natural relative-coordinate strategy used for the previously certified
base models, when applied with one of the three *original* coordinates of
H(4,5,7).

This is NOT a proof of nonrectifiability. It does NOT exclude an absolute
coordinate F of degree four whose completion preserves none of x,y,z. It
does NOT exclude a relative-coordinate parameter of degree five or higher.
It also does not make a claim about an arbitrary new affine combination or
nonlinear choice of the preserved coordinate.

The identities remain valid after extending k. Therefore the result holds
over C and every coefficient extension used in the previous constructions.
An affine reparametrization at+b (a≠0) gives the same degree bound, by
replacing F with (F−b)/a.

## 2. The classical low-degree normal form

Let K be a characteristic-zero field. A coordinate f of K[u,v] of degree d
has highest homogeneous part proportional to L^d, with L a linear form.
For d=3, after choosing an independent linear form M, it has the form

    f=P3(L)+c M,        c≠0.

For d=4 there are only the following two possibilities, with translations
absorbed into the displayed univariate polynomials:

    f=P4(L)+c M,        c≠0,
    f=A(M+Q2(L))²+b L+c,    A b≠0, deg Q2=2.

Here a rescaling of M is allowed; it has been absorbed into A and Q2. More
generally choosing another independent M only modifies Q2 by an affine
polynomial and changes the nonzero constants.

**Reason.** Complete f to (f,g), and choose g of minimal degree. The plane
degree-reduction theorem allows repeated replacement of g by g−c f^m
until deg(g)<deg(f). The Division Lemma implies deg(g) divides deg(f).
For d=3 this forces deg(g)=1. For d=4, either deg(g)=1 or deg(g)=2.
In the latter case first subtract a multiple of g² from f, then a multiple
of g if needed; the remaining companion has degree one. Thus g is a
quadratic polynomial in a linear form plus an independent linear form,
and f is a quadratic polynomial in g plus a nonzero multiple of the first
linear form. Completing the square gives the stated formula.

In particular, if the leading term is c u^4, then after writing

    f=A v²+B(u)v+C(u),

the quadratic case requires A∈K*, deg B≤2, and

    C(u)−B(u)²/(4A)

to have degree exactly one. The triangular case A=0 requires B∈K*.
These implications alone suffice below; no sufficiency test is used.

An accessible primary source for the classical ingredients is Nguyen Van
Chau, *A Simple Proof of Jung's Theorem on Polynomial Automorphisms of C²*,
https://arxiv.org/pdf/math/0408077 : Division Lemma in §2 and the degree
reduction in §4. The classical theorem over arbitrary fields is also
recorded there; the proof above applies over K=k(x), k(y), or k(z).

## 3. Complete finite-dimensional family

The parameter polynomial of degree three is

    F0=(x²−2)z−y³+3y.

Every parameter polynomial of total degree at most four is uniquely

    F=F0+c0 K0+c1 K1+c2 K2+c3 K3+c4 K4+c5 K5+c6 K6,

where the ci are constants in k and

    K0=x²z²−x²−xy²+2x−y³z+3yz−z²,
    K1=x²y+xy³−xy²z−2xy+xz−yz²+z³−2z,
    K2=x²yz−xy²+x−y⁴+3y²−2yz+z²−2,
    K3=x³+x²y²−2x²−xz²−x−y²−yz+2,
    K4=x³z−x²z+xy−3xz+y³−yz²−2y+2z,
    K5=x³y+x²z−xy³−xy+xz−y³−y²z+yz²+y−z,
    K6=x⁴+x²y²−5x²+xy²−xyz−xz²−y²−z²+4.

All seven Ki vanish on gamma. There are 35 monomials of degree≤4, and their
evaluation matrix in k[t] has rank 28 over Q. The seven displayed kernel
vectors have rank seven. This proves completeness, including over every
characteristic-zero coefficient extension. The verifier computes all three
ranks and verifies all eight substitution identities exactly.

## 4. Preserving x=C4

Regard F as a polynomial in (y,z) over K=k(x). Its degree-four part is

    −c0 y³z−c2 y⁴.

If this is nonzero and a pure fourth power, c0=0 and c2=w≠0, with leading
direction y. The quartic normal form also forbids z³ and yz², forcing
c1=0 and c4=c5=u. Set c3=v, c6=q. Write F=A z²+B(y)z+C(y). Then

    A=w−x(v+q)−q,
    [y²]B=−u,
    [y⁴]C=−w.

If A≠0, the fourth coefficient of 4AC−B² gives

    −4w A−u²=0.

Since w≠0 is a constant, its x coefficient gives q=−v, so A=w+v.
With this substitution,

    [y]B=v(x−1)+w(x²−2),     [y³]C=−1−ux.

The x² coefficient in [y³](4AC−B²) is 2uw. It must vanish, hence u=0.
The fourth coefficient then implies A=0, a contradiction.

If A=0 at the outset, its coefficients give q=w and v=−w. The triangular
normal form requires B to be independent of y, so u=0; however

    [y]B=w(x²−x−1)≠0.

This excludes every degree-four possibility.

For degree at most three, c0=c2=0. The cubic part is

    (−1+c1 x+c4−c5(x+1))y³
      +(−c1 x−c5)y²z+(−c1−c4+c5)yz²+c1 z³.

If c1≠0 and this is a cube, the constant coefficient of yz² forces the
ratio of its two linear coefficients to be constant. Its y²z coefficient
would then also be constant in x, contradicting −c1 x−c5. Thus c1=0.
A nonzero cube without z³ is proportional to y³, forcing c5=c4=0.
The cubic part is now −y³, so it cannot vanish and the degree cannot fall
to two. Only c3=v,c6=q remain. The coefficient of z² is

    −x(v+q)−q.

The cubic normal form requires this to vanish, hence q=v=0. This leaves
precisely F0, which is a coordinate over k(x) because x²−2 is invertible
there.

It is not a coordinate over k[x]: its derivatives in y,z vanish at
x²=2,y²=1. Indeed its entire gradient vanishes when in addition z=0.
Such geometric zeros persist as an obstruction over any characteristic-
zero field, by scalar extension to an algebraic closure.

## 5. Preserving y=C5

Regard F in (x,z) over k(y). Its quartic part is

    c6 x⁴+c4 x³z+c0 x²z².

The pure-power condition in the quartic case gives c0=c4=0,c6=w≠0,
with leading direction x. Absence of z³ and xz² forces c1=0,c3=−w.
Set c2=a,c5=b. In F=A z²+B(x)z+C(x),

    A=a+by−w,       [x²]B=1+ay+b,       [x⁴]C=w.

Both quartic normal forms imply

    4w A−(1+ay+b)²=0.

The coefficients of y², then y, force a=0,b=0. The constant coefficient
then forces 4w²+1=0, so A=−w≠0. At these values,

    [x³](4AC−B²)=4w²+2wy,

which is nonzero because w≠0. Thus no quartic coordinate exists.

In the cubic case c0=c4=c6=0, and the homogeneous cubic is

    (c3+c5 y)x³+(1+c2 y+c5)x²z−c3 xz²+c1 z³.

If c1=0, the pure-cube condition forces c3=c2=0,c5=−1. The cubic part
is −y x³ and F=F0−K5, whose z² coefficient is −y≠0. This contradicts
the cubic normal form.

If c1≠0, the ratio of the linear coefficients in the cube is constant
because the z³ and xz² coefficients are constant. It follows that
c2=c5=0. Comparing the remaining coefficients gives

    c1=−1/9,       c3=v,       3v²+1=0.

The leading cubic is −(z+3v x)³/9. Put L=z+3v x. In coordinates (x,L),
the x² coefficient of F is

    (2v/3)y²−(4/9)y−5v/3.

It is nonzero because v≠0, contradicting the cubic normal form.
The homogeneous cubic cannot vanish in either branch, so no degree≤2
case has been omitted.

## 6. Preserving z=C7

The quartic part in (x,y) over k(z) is

    c6 x⁴+c5 x³y+(c3+c6)x²y²+(c1−c5)xy³−c2 y⁴.

### 6a. Quartic with nonzero y⁴ coefficient

Write c2=w≠0 and its pure-power form as −w(y+rx)⁴. Its coefficients
force

    c1=−4w(r+r³), c3=w(r⁴−6r²), c5=−4wr³, c6=−wr⁴.

The parameter r is a constant, even though we work over k(z), since it
is recovered from ratios of the constant quartic coefficients. Set c0=a,
c4=b and L=y+rx. The quartic normal forms forbid x³ and x²L. Their
coefficients are

    E30 = ar³z−ar²−br³+bz−5r⁶w+4r⁵wz+5r⁴w
          +4r³wz+r³−3r²w−rwz,
    E21 = −3ar²z+2ar+3br²+14r⁵w−8r⁴wz−4r³w
          −8r²wz−3r²−2rw+wz.

If r=0, [z]E21=w≠0. Thus r≠0. Solving their z coefficients yields

    a=w(1−8r²−8r⁴)/(3r²),
    b=w(2r−4r³−4r⁵)/3.

After substitution, their constant parts satisfy

    −3r E21−9 E30 = w(3r⁶−41r⁴+25r²+1).

Hence P(r²)=0, where P(U)=3U³−41U²+25U+1.

Write F=A x²+B(L)x+C(L). In either quartic normal form the fourth-degree
coefficient relation requires −4w A−([L²]B)²=0. Its z² coefficient is

    −w²(48r⁸+96r⁶−8r⁴−56r²+7)/(3r²).

Thus Q(r²)=0, with Q(U)=48U⁴+96U³−8U²−56U+7. But the following exact
integer identity rules this out in characteristic zero:

    (98443392 U³+361976832 U²+422233904 U+148292464) P(U)
    +(−6152712 U²+73768936 U+82963001) Q(U)
      =729033471.

The verifier checks this Bézout identity by direct expansion.

### 6b. Quartic with leading direction x

If c2=0, pure fourth power forces c1=c5=0,c3=−c6, with c6=w≠0.
Write c0=a,c4=b. Absence of y³ and xy² in the adapted quartic normal
form requires

    b−1−az=0,        w−a=0.

The first equation gives a=0,b=1, and the second gives w=0, contradiction.

### 6c. Cubic and lower degrees

The vanishing of the quartic part gives c1=c2=c3=c5=c6=0. Thus
F=F0+aK0+bK4, with homogeneous cubic

    bz x³−a xy²+(b−1−az)y³.

Its x²y coefficient is zero. A pure cube can therefore involve only x
or only y. The only two possibilities are (a,b)=(0,0) and (0,1).
For the first, F0 has x² coefficient z≠0, although its leading direction
is y. For the second, F0+K4 has mixed coefficient [xy]F=1, although its
leading direction is x. Both contradict the cubic normal form.
There is no degree≤2 branch: the displayed cubic cannot vanish identically.

## 7. Reproduction and exact meaning of the certificate

Run

    python research/continuation_20261026/h457/verify_degree4.py

The script resolves the existing local SymPy dependency automatically,
constructs the full evaluation matrix, verifies the complete 7-dimensional
kernel, and checks 35 exact algebraic assertions supporting every branch.
It writes degree4_certificate.json. It does not infer nonexistence from a
random numerical search or a bounded sample of parameter values.

The normal-form argument and the branch exhaustiveness are mathematical
proof steps recorded above; they should be independently reviewed along
with the machine identities. The result is an improvement of a degree
bound for a specified strategy, not a resolution of the full embedding
problem and not an assertion of novelty relative to all literature.
