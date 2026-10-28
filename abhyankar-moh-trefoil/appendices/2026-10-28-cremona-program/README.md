# Appendix 2: Cremona groups and polynomial rectification

**Ivan Dorofeev — 28 October 2026.**

**Research branch: UNDER VERIFICATION. / Исследовательская ветка: НА СТАДИИ ПРОВЕРКИ.**

This appendix continues the study of consequences of the explicit rectifiers
and their connections with the Abhyankar–Moh embedding problem, Cremona groups,
birational geometry and affine geometry. Every statement remains subject to
checking. The author shares these working arguments and reproducible calculations
in the hope that they develop into a useful research programme, and invites
others to verify, correct, discuss and extend them.

The work was prepared in an AI-assisted research process. Internal reruns and
alternative implementations are not external independent peer review. No claim
of publication priority is made. This appendix does not replace the original
paper or Appendix 1.

## Read and build

- [Russian research preprint (PDF)](appendix2_cremona_program_ru.pdf).
- [Overleaf-compatible main source](latex/main.tex), with the complete source
  tree and bundled text fonts under `latex/`.
- [Claim and literature audit](audit/claim_status.md).
- [Computational scope and commands](computations/README.md).
- [Provenance and source version](PROVENANCE.md).
- [Checksums](SHA256SUMS.txt).

The paper uses the existing preprint's `article`/11pt/A4 layout, 24 mm margins,
theorem environments, page headers and linked references. The Unicode text-font
configuration is adapted for Russian and is included in the Overleaf source.

For Overleaf, upload the **separate Overleaf ZIP** as a new project, select
`main.tex` and set **Compiler → XeLaTeX**. No shell escape or external downloads
are needed. From this directory, local compilation is:

```bash
python build_pdf.py
```

This runs XeLaTeX twice and writes `appendix2_cremona_program_ru.pdf`.

## What the appendix claims

Over `K = Q[a]/(a^2-a+1)`, the constructed Shastri, harmonic and `C_N` rectifiers
have working proofs of the following properties:

1. They are polynomial automorphisms with polynomial inverses.
2. They are **wild** in three variables. The assertion concerns these chosen
   maps; another tame rectifier of the same curve is not excluded.
3. They belong to `C_3(K) = <PGL_4(K), sigma_3>`.
4. After extending by three identity coordinates, they belong to `Tame_6(K)`.

The paper gives the group-theoretic literature needed for these inferences and
the proofs that its hypotheses hold. Finite computational tests do not prove
the general assertions for all `N`; induction and the written proofs do.

The specific Shastri curve is therefore excluded as a candidate complex
nonrectifiable line. The related van den Essen–van Rossum candidates already
treated in Appendix 1 are recorded separately. Neither the general spatial
embedding problem, the general cancellation problem, nor the general stable
tameness conjecture is claimed to be solved.

The programme studies the intersection of a birational rectifier's stabilizer
coset with the polynomial automorphism group, with relative coordinates and
control of poles as a constructive approach. Completeness of this approach,
tame rectifiability of the curves themselves, and classification of fields of
rectification remain open within this project.

## Reproduce the new computations

Python 3.10+ is required (tested with Python 3.12 and SymPy 1.14.0):

```bash
python -m pip install -r requirements.txt
python computations/run_all.py --max-n 3
```

The runner performs normal and `python -O` checks and compares their exact
mathematical results. It writes only under this appendix's `results/` directory.
The delivered run contains 90 passing checks per mode for `N = 1, 2, 3`, including
negative controls. Logs and JSON records are included. Code comments and
docstrings are in English; no floating-point arithmetic or network access is
used by the verifier.

The baseline commands `python -u verify.py` and
`python -u verify_printed_formulas.py` were also rerun from the repository root.
Both passed; all twelve printed components matched the compact construction.
Their fresh logs are `results/upstream_compact.log` and
`results/upstream_printed.log`. Other historical logs in the full repository
archive are retained as historical records, not advertised as new executions.

## Scope of the certificate

The proof of polynomial invertibility uses exact division in both directions
and injective localization, with explicitly invertible factors. For generic
`N`, the verifier does not expand every enormous global composition. It checks
the modular divisibility certificates and actual factored curve evaluations;
see `computations/README.md` for the precise distinction. The exceptional
fibre is covered by polynomiality and the localization argument, not omitted.

Deep cited theorems and the all-`N` proof are mathematical arguments, not a
formal proof-assistant certificate. A six-variable elementary factorization
word is not computed: its existence follows from the cited stable-tameness
theorem.

## Repository integration

This directory is the second dated appendix. The proposed update adds links in
the root README, a changelog entry and refreshed checksums, while leaving the
main paper and first appendix unchanged. The source baseline is recorded in
`PROVENANCE.md`; the downloadable update patch can be checked with
`git apply --check appendix2-cremona.patch` before application.

Discussion and corrections are welcome at the existing project repository:
https://github.com/qft98romanov-hash/abhyankar-moh-trefoil
