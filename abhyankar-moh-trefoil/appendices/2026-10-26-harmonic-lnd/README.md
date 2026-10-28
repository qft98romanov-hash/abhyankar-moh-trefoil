# Research appendix: harmonic embeddings, Cremona constructions and LNDs

**Date: 26 October 2026.**  
**Status: preliminary research appendix — UNDER VERIFICATION.**

**Дата: 26 октября 2026 года. Статус: дополнительное исследовательское приложение, НА СТАДИИ ПРОВЕРКИ.**

This separate appendix records additional arguments, computations and exact
certificates. Its mathematical claims remain subject to further checking.
The computational checks and alternative implementations were produced within
the same AI-assisted research process; external independent peer review and
literature priority are not asserted. This appendix does not amend or replace
the existing manuscript, formulas, verification scripts or verification logs.

The fixed source baseline is commit
[`3cf41be3fb3b1108e1ec91dd23dff7bfcf59569e`](https://github.com/qft98romanov-hash/abhyankar-moh-trefoil/tree/3cf41be3fb3b1108e1ec91dd23dff7bfcf59569e).

## Read the appendix

- [Detailed Russian report (PDF)](harmonic_knots_lnd_research_ru.pdf).
- [LaTeX source](latex/harmonic_knots_lnd_research_ru.tex).
- [Russian reproduction instructions](README.txt).
- [Provenance and verification scope](PROVENANCE.md).
- [Exact upstream input manifest](research/source_manifest.json).
- [Checksums of the files in this appendix](SHA256SUMS.txt).

## Results submitted for verification

Write $C_n(t)=2T_n(t/2)$ and $K=\mathbb Q(\sqrt{-3})$.

| Topic | Statement and scope | Proof / computation |
| --- | --- | --- |
| Harmonic index changes | If $\gcd(a,b)=1$ and $c'\equiv\varepsilon_a c\pmod{2a}$, $c'\equiv\varepsilon_b c\pmod{2b}$, then $C_{c'}-\varepsilon_a\varepsilon_b C_c\in\mathbb Q[C_a,C_b]$. This supplies polynomial shears. | [Proof](latex/sections/harmonic.tex), [exact checks](research/harmonic_literature/periodic_shears.py) |
| Two infinite families | Rectifiability over $K$ of $H(3,4,c)$ with $\gcd(c,12)=1$ and $H(3,5,c)$ with $\gcd(c,15)=1$, using the baseline rectifiers. These are infinite families of parametrizations, not infinitely many distinct real knot types. | [Proof and residue classes](latex/sections/harmonic.tex) |
| Relative transfer and LND | Within the stated transfer construction, the quotient-ring centre criterion, a relative coordinate, a slice and geometric absence of fixed points are equivalent. Repeated factors of the denominator are included. | [Proof](latex/sections/cremona.tex), [base identities](research/repo_audit/independent_base_lnd.py) |
| van den Essen–van Rossum | Explicit coordinates of the kernel of the specific derivation in Conjecture 5.1, and consequences for the related Conjectures 5.2 and 5.3, follow from the baseline rectifier. This is not a solution of general cancellation or linearization problems. | [Proof with polynomial inverse](latex/sections/van_den_essen.tex), [factored certificate](research/lnd_certificate/verify_lnd.py) |
| Minimum slice degrees | Ordinary total-degree minima 7 (Shastri curve) and 11 ($H(3,5,7)$), in the specified original five variables. These lower bounds have separate exact rational witnesses and do not depend on the baseline rectifiers. | [Degree 7 proof](latex/sections/minimum_slice.tex), [degree 11 proof](latex/sections/harmonic_minimum_slice.tex), witnesses below |
| Bounded reductions | 44,142 pairwise-coprime triples $2\le a<b<c\le100$ were scanned through all strictly decreasing elementary paths. 3,209 reach index 1; 237 additional triples reach a verified base model; 40,696 remain undecided by this algorithm. | [Code](research/harmonic_compute/reduction_scan.py), [results](research/harmonic_compute/reduction_scan.json) |
| Remaining cases | Specific transfer and low-degree parameter-coordinate obstructions for $H(3,7,8)$ and $H(4,5,7)$. Neither rectifiability nor nonrectifiability of these two cases is established here. | [Proofs and exact computations](latex/sections/computations.tex) |

No general rectification theorem for all harmonic embeddings is claimed.
Motivic methods, K-theory and homological algebra are not used.

## Exact rational certificates

The lower-bound witnesses are
[degree 6 exclusion](research/lnd_certificate/no_slice_degree6_certificate.json)
and [degree 10 exclusion](research/lnd_certificate/no_harmonic_slice_degree10_certificate.json).
They annihilate the derivation images of all 462 and 3,003 source monomials,
respectively, without truncating the image support, and take value 1 on the
constant polynomial. The included upper slices have degrees 7 and 11.

Run all commands below **from this appendix directory**. Use Python 3.10+
(tested with Python 3.12), without `-O`; several research scripts use `assert`.
Some verifiers regenerate JSON result files beside themselves.

The following four verifiers require only the Python standard library:

```bash
python research/lnd_certificate/verify_minimal_slice.py
python research/repo_audit/review_minimal_slice.py
python research/lnd_certificate/verify_harmonic_minimal_slice.py
python research/repo_audit/review_harmonic_minimal_slice.py
```

For the remaining computations:

```bash
python -m pip install -r requirements.txt
python bootstrap_source.py
python repo/verify.py
python repo/verify_printed_formulas.py
python research/repo_audit/independent_base_lnd.py
python research/harmonic_literature/periodic_shears.py
python research/lnd_certificate/verify_lnd.py
python research/cremona_lnd/verify_example.py
python research/harmonic_compute/verify_new_results.py
python research/harmonic_compute/reduction_scan.py
```

`bootstrap_source.py` retrieves only the 11 pinned upstream files and checks
their Git blob hashes and byte lengths. It never executes downloaded code and
does not overwrite a differing local file. From a checkout whose original
files still match the pinned commit, the offline alternative is:

```bash
python bootstrap_source.py --from-repo ../..
```

The dependency snapshot is written only to this appendix's ignored `repo/`
directory. The original repository files are not modified.

On Windows, this appendix's `.gitattributes` keeps its text files in LF form,
so its certificate checksums remain stable after checkout. The upstream root
files may still use CRLF in a local checkout. In that case use the default
online `python bootstrap_source.py`, which retrieves the exact pinned Git
bytes; do not disable the hash checks to force the offline copy to pass.

The bounded exploratory searches (`parameter_search.py`, `quadratic_ansatz.py`,
`quadratic_ansatz2.py`, `divisor_ansatz.py`, `matrix_probe.py` and
`degree5_quadratic_observation.py`) are included separately. Their restricted
search spaces are not completeness claims, and some Gröbner searches are costly.

## Build the PDF

Use XeLaTeX, with `fontspec`, `polyglossia`, `unicode-math`, the DejaVu fonts
and Latin Modern Math:

```bash
cd latex
xelatex -interaction=nonstopmode -halt-on-error harmonic_knots_lnd_research_ru.tex
xelatex -interaction=nonstopmode -halt-on-error harmonic_knots_lnd_research_ru.tex
```

The report gives primary literature links and distinguishes the established
background mechanisms, their applications here and the unresolved cases.
