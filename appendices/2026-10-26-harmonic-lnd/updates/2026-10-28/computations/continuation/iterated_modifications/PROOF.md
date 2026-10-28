# Exact degree modules for iterated quadratic modifications

Date: 26 October 2026. Working result under verification. No literature novelty is asserted.

Let k have characteristic zero, A=k[x,y,z], r_{-1}=z, r_0=y and

    r_j=x r_{j-2}-r_{j-1}^2  (j>=1).

Fix l>=1 and set p=r_l, w=r_{l-1}. Define

    D_l=(-1)^l Jac_{y,z}(p, .).

Then D_l(w)=x^l. These are the iterated quadratic modifications appearing in the candidate of Dasgupta--Gaifullin, On locally nilpotent derivations of polynomial algebra in three variables, Sb. Math. 216 (2025), Remark 4.20 and Question 4.21. Composition of coordinate-ring automorphisms and composition of point maps have opposite conventions; the recurrence above fixes our convention unambiguously.

## Kernel and irreducibility

The determinant recurrence is Jac(r_j,r_{j-1})=-x Jac(r_{j-1},r_{j-2}), hence Jac(p,w)=(-x)^l. After inverting x, the recurrence reconstructs y,z from p,w, so

    A_x=k[x,x^{-1},p,w],  D_l=x^l partial_w.

This proves local nilpotence on A_x, and hence on its D_l-stable subring A. The kernel is

    B=ker D_l=k[x,p].

Indeed, p mod x=-y^{2^l}; thus the homomorphism k[p] -> k[y,z] obtained at x=0 is injective. If an element of A intersect k[x,x^{-1},p] had an x-denominator of minimal positive order, its numerator would contradict this injectivity modulo x.

Any common divisor of p_y,p_z divides Jac(p,w)=(-x)^l. But p_y mod x=-2^l y^{2^l-1} is nonzero. Thus D_l is irreducible.

## A basis adapted to the derivation

Write v_j=r_{l-1-j} for 0<=j<=l; in particular v_0=w and v_l=z. Put v_{-1}=p. The relations are

    v_j^2=x v_{j+1}-v_{j-1},  0<=j<l.

They present A as a B-algebra: eliminating successively v_{l-2},...,v_0,p recovers exactly k[x,v_{l-1},v_l]=k[x,y,z]. They also give a monic Groebner basis with leading monomials v_j^2: use weights 2^j on v_j, with the tie-breaking order v_0>v_1>...>v_l. The leading monomials are pairwise coprime. Thus A is a free B-module with basis

    s_n=(product_{j=0}^{l-1} v_j^{epsilon_j}) v_l^q,
    n=sum_{j=0}^{l-1} epsilon_j 2^j+q 2^l,
    epsilon_j in {0,1}, q>=0.

Equivalently, generation follows by the same monic reductions and independence follows from the distinct degrees in w over k(x,p).

The backward recurrence v_{j+1}=(v_j^2+v_{j-1})/x gives

    deg_w(v_j)=2^j,
    leading_coefficient_w(v_j)=x^{-(2^j-1)}.

Consequently deg_{D_l}(s_n)=n, and its leading w-coefficient is

    x^{-E_l(n)},  E_l(n)=sum_{j=1}^l floor(n/2^j).

No cancellation of the largest D-degree is possible in a B-linear combination of distinct s_n. Therefore, for F_n=ker D_l^{n+1},

    F_n=direct_sum_{i=0}^n B s_i,
    D_l^n(F_n)=x^{a_l(n)} B,
    a_l(n)=l n-sum_{j=1}^l floor(n/2^j).

The irrelevant factor n! is a unit in k. This is a complete exact description of the filtration and all its leading-coefficient ideals, not only its first term.

In particular, the plinth ideal is (x^l). For l=3 the exponents a_3(n), n=0,...,8, are

    0,3,5,8,9,12,14,17,17.

The first three local polynomial generators are w=r_2, v_1=r_1 and v_2=y, with D-degrees 1,2,4; z has D-degree 8. The exponent pattern records all three successive divisions by x.

## Scope

This calculation supplies exact invariants for the candidate in Question 4.21. It does NOT prove c((beta theta)^3)=3: a lower bound for that complexity must compare all permitted factorizations and coordinate changes. A visible three-step presentation alone is not such a lower bound.

Once the independently audited one-transfer filtration formula is available, these exponents exclude a one-transfer presentation of D_l (up to a k[x]-automorphism and multiplication by a nonzero scalar) for l>=2. Such a presentation for an irreducible derivation with plinth (x^l) would have first two exponents l and either l or 2l, whereas here they are l and 2l-1. This conditional comparison concerns the explicitly defined one-transfer class, not arbitrary Cremona factorizations or universal level.

## Reproduction

Run verify_iterated_filtration.py. It checks the determinant, primitive gradients, backward coordinate recovery, and the full displayed formula for the basis elements with l=1,...,3 and n=0,...,16, in exact arithmetic. The proof for arbitrary l,n is the algebraic argument above.
