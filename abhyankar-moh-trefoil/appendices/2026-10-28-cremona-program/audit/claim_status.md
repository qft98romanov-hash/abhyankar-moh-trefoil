# Appendix 2: claim and literature audit

Date: 28 October 2026. Status: research branch, UNDER VERIFICATION.

Repository baseline: `b954f3609e900761fddc9c8ff03d8301e9604cab`.
This document separates logical consequences of the supplied formulas from
novelty, external review and universal conjectures. It is not an external
peer-review report.

## Claims that the displayed constructions address

| Claim | Mathematical support | Limit |
| --- | --- | --- |
| Rectifiability of the specified Shastri curve over Q(sqrt(-3)) and C | A polynomial map and its polynomial inverse, with the curve identity. Existing main manuscript and root certificates. | Does not settle all A1 embeddings in A3. Does not establish priority. |
| Rectifiability of the harmonic model and C_N | Exact coordinate transfer and its inverse; general induction in the text, finite implementation checks. | The +4t variation is not the +5t harmonic model. Finite N checks alone do not prove all N. |
| Wildness of the selected trefoil rectifier | Edo–Vénéreau 2001, Proposition 2: bx^5 does not divide the nonlinear coefficient bx. Umirbaev–Yu 2004 transfers relative wildness to ambient wildness. | Does not rule out another tame rectifier of the same curve. |
| Wildness of the selected harmonic and C_N rectifiers | Edo 2013, Theorem 8(1), reduced-quadruple uniqueness (Proposition 2), and the companion calculation in the proof of 8(3). The reduced inner coordinate has y^2 coefficient -x modulo x^2, not divisible by x^(N+1). Then Umirbaev–Yu. | This is an application to these formulas, not a theorem of the cited article mentioning these knots. |
| Membership in C3=<PGL4,sigma3> | Laurent shears, balanced monomial maps, Blanc–Hedén monomial parity criterion, and normalization by D_N. | For odd N, do not claim D_N itself lies in C3. Its normalizer action is sufficient. |
| Stable tameness of all selected rectifiers | Berson–van den Essen–Wright 2012, Corollary 4.9. Add three identity variables to get a tame automorphism of A6. | The number three is an upper bound, not a proved minimum. The general stable tameness conjecture is not solved. |
| Minimal degree of a number-field rectification field is two | Real knot obstruction excludes every real embedding; the explicit quadratic-field formula supplies the upper bound. | Does not establish uniqueness of Q(sqrt(-3)); absence of a root of a^2-a+1 only blocks this coefficient formula. |

## Named conjectural candidates

1. **Shastri's specific complex trefoil candidate.** The 1992 primary article
   proposes real knot embeddings as candidates for complex nonrectifiability
   and writes the exact curve. It does not contain a separately numbered
   conjecture asserting nonrectifiability of this particular formula. Later
   works call it Shastri's conjecture. The safe manuscript wording is that the
   explicit rectifier excludes this specified historical candidate.
2. **van den Essen–van Rossum 2002, Conjectures 5.1–5.3.** These consequences
   already appear in Appendix 1. Their mechanism was checked directly from
   its polynomial coordinate changes: the five-variable LND becomes a
   coordinate derivation; its kernel, the stated slice quotient and the
   extended Rees algebra are polynomial. Appendix 2 recalls this implication
   and does not present it as a new Cremona theorem.
3. **Conjecture E and the Oda preprint.** arXiv:1201.4198 was withdrawn on
   9 May 2020 with the comment "This is an incorrect part". It is excluded
   from the proof chain. Its historical statement of Conjecture E is not
   evidence for the validity of its attempted solution.

For a rectifier F=(P,Q,R) with inverse G, let V=gamma(u)-tX. The map

    (t,u,X) -> (t, P(V), Q(V)/t, R(V)/t, (u-P(V))/t)

has polynomial inverse

    u=p+t*s,  X=(gamma(p+t*s)-G(p,t*q,t*r))/t.

Both divisions follow from the axis identities. This explicitly proves that
the corresponding kernel is k[t,p,q,r]. Any other slice differs from s by
a kernel element, so its zero quotient is polynomial. Finally
k[x,y,z][t,I_gamma/t]=k[t,P,Q/t,R/t]. These arguments hold already over
the coefficient field K and remain valid after base change to C.

## Existing literature, with exact roles

- A. R. Shastri, *Polynomial representations of knots*, Tohoku Math. J.
  44 (1992), 11–17, DOI <https://doi.org/10.2748/tmj/1178227371>.
  Primary PDF <https://www.jstage.jst.go.jp/article/tmj1949/44/1/44_1_11/_pdf>:
  section 1 and section 3, Example 1. The introduction already links
  rectifiable spatial lines to candidates for non-tame automorphisms.
- A. van den Essen and P. van Rossum, *Triangular derivations related to
  problems on affine n-space*, Proc. Amer. Math. Soc. 130 (2002), 1311–1322,
  DOI <https://doi.org/10.1090/S0002-9939-01-06212-8>.
  Theorem 4.1, Corollary 4.2 and section 5 are the locations recorded and
  transcribed in Appendix 1. **Access note for this audit:** publisher
  bibliographic metadata was retrieved afresh; the full AMS PDF returned
  HTTP 403. Numbering of 5.1–5.3 is retained from the existing Appendix 1,
  not represented as a newly successful PDF retrieval. The algebraic
  implication above was checked independently of that retrieval.
- A. van den Essen and P. van Rossum, *Coordinates in two variables over a
  Q-algebra*, Trans. Amer. Math. Soc. 356 (2004), 1691–1703,
  DOI <https://doi.org/10.1090/S0002-9947-04-03492-0>.
  Page 1702 explicitly refers to the complex nonrectifiability claim as
  Shastri's conjecture. The publisher PDF was unavailable to this fresh
  retrieval; searchable paper text exposed the passage. We therefore do
  not rely on that passage as the sole basis for a new attribution.
- M. Mella and E. Polastri, *Equivalent birational embeddings*, Bull.
  London Math. Soc. 41 (2009), 89–93, DOI
  <https://doi.org/10.1112/blms/bdn107>,
  <https://arxiv.org/abs/0906.4858>. Introduction and Theorem 1:
  direct Cremona/Abhyankar–Moh predecessor; codimension at least two.
- E. Edo and S. Vénéreau, *Length 2 variables of A[x,y] and transfer*,
  Ann. Polon. Math. 76 (2001), 67–76, DOI
  <https://doi.org/10.4064/ap76-1-6>.
  Proposition 2 for length-one tameness; transfer constructions in later sections.
- E. Edo, *Coordinates of R[x,y]: Constructions and classifications*,
  Comm. Algebra 41 (2013), 4694–4710,
  <https://arxiv.org/abs/1206.5876>. Proposition 2 and Theorem 8.
- U. U. Umirbaev and J.-T. Yu, *The strong Nagata conjecture*, PNAS 101
  (2004), 4352–4355, DOI <https://doi.org/10.1073/pnas.0308157101>.
  Main Theorem: relative wild coordinates are ambient wild coordinates.
- D. Lewis, *A unified approach to embeddings of a line in 3-space*,
  Comm. Algebra 52 (2024), 189–200, DOI
  <https://doi.org/10.1080/00927872.2023.2239344>,
  <https://arxiv.org/abs/2203.08178>. Lemma 1, Theorems 2 and 12:
  direct predecessor for the coordinate lift and denominator-removal strategy.
- J. Blanc and I. Hedén, *The group of Cremona transformations generated
  by linear maps and the standard involution*, Ann. Inst. Fourier 65
  (2015), 2641–2680, DOI <https://doi.org/10.5802/aif.2999>.
  Theorem 1.1 (monomial criterion), Proposition 6.5 (tame inclusion),
  Proposition 6.8 (Nagata already belongs to C3).
- J. Berson, A. van den Essen and D. Wright, *Stable tameness of
  two-dimensional polynomial automorphisms over a regular ring*, Adv.
  Math. 230 (2012), 2176–2197, DOI
  <https://doi.org/10.1016/j.aim.2012.04.017>,
  <https://arxiv.org/abs/0707.3151>. Corollary 4.9.
- Withdrawn record: <https://arxiv.org/abs/1201.4198> (not a proof source).

## Open or not established here

- General rectification of A1 in A3 over C; the historical existential
  nonrectifiability conjecture and its universal opposite are not decided.
- Necessity/completeness of the fixed-x relative construction.
- Tame rectifiability of a curve as opposed to tameness of our chosen map.
- Minimum degrees, minimum stabilization dimension, classification of
  all rectification fields and all descended maps.
- Full description of Cr3 or proof that every polynomial automorphism
  belongs to C3. Do not conflate C3 with larger linear-plus-Jonquieres groups.
- General cancellation, general linearization and general stable tameness.
- First-publication priority. Targeted searches did not locate an earlier
  full Shastri rectifier, but a negative search is not a priority proof.

## Review boundary

The Appendix 1 claims about all harmonic-index classes and minimal slice
degrees are not re-proved or re-certified by this Appendix 2 audit. They
should remain attributed to their existing appendix, with its stated
verification status. The new computations certify finite identities;
literature theorems and general induction arguments remain mathematical
proof obligations, not properties a finite CAS run decides.
