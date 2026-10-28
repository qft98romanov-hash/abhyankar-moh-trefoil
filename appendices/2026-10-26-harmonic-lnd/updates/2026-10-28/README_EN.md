# Research appendix — 28 October 2026

**Researchers: Ivan Dorofeev and Alexander Frolov. All material remains under verification.**

**Ivan Dorofeev** — Independent Researcher.  
**Alexander Frolov** — Higher School of Modern Mathematics, MIPT.

This research branch continues the study of consequences of the certified
rectifications and their connections with the Abhyankar–Moh embedding problem,
locally nilpotent derivations, the Makar-Limanov invariant and affine geometry.
The authors share interim proofs and computations before verification is
complete, hope that this direction will develop into a broader research
programme, and invite all interested readers to check and contribute to it.

The material was prepared with AI assistance. Checks within that process do
not constitute independent external peer review. No claim of priority is made.

**Acknowledgements.** The authors express their sincere gratitude to Professor
Alexei Kanel-Belov and Professor Alexander Gasnikov.

## Full texts and source projects

| Item | File |
| --- | --- |
| Complete English research text | [English PDF](abhyankar_moh_research_appendix_2026-10-28_en.pdf) |
| Complete Russian research text | [Russian PDF](abhyankar_moh_research_appendix_2026-10-28_ru.pdf) |
| English Overleaf / XeLaTeX source | [overleaf_en/main.tex](overleaf_en/main.tex) |
| Russian Overleaf / XeLaTeX source | [overleaf/main.tex](overleaf/main.tex) |
| All computations and exact certificates | [computations/README_EN.md](computations/README_EN.md) |
| Recorded full verification run | [computations/verification_summary.json](computations/verification_summary.json) |
| Internal audit records | [audits/README.md](audits/README.md) |
| Snapshot integrity | [SHA256SUMS.txt](SHA256SUMS.txt), [verify_delivery.py](verify_delivery.py) |
| Translation verification | [audits/translation/translation_audit.json](audits/translation/translation_audit.json) |

The English version translates all sixteen sections, proofs, formulas, status
tables, open problems and fifteen references. It is not an abridged summary.
Both versions use the same computational evidence. Their pagination may differ.

## Established results and open questions

1. The original Shastri and H(3,5,7) rectifiers over Q(sqrt(-3)) are supported
   by exact composition certificates. The Shastri rectifier yields polynomiality
   of the specified kernel and extended Rees algebra and makes the original
   slice a coordinate. Consequently, Conjectures 5.1–5.3 of van den Essen–van
   Rossum are refuted for this particular candidate over C.
2. The continuation includes two infinite harmonic families, eight minimum
   slice degrees, two formulas for all multiplicities, formal coordinates,
   filtrations for classes of LNDs, and a rectification criterion through a
   normal locally finite vector field. General statements have written proofs;
   finite computations verify particular certificates.
3. The proposed relative ML invariant of the embedded pair is always trivial
   in the stated codimension and does not supply the envisaged obstruction.
4. **No complex rectification of H(3,7,8) or H(4,5,7) is established here.**
   Complete affine spaces of normal fields with divergence two have dimensions
   24 and 19. It remains unknown here whether they contain a locally finite
   field. The full ML invariant of the associated new kernels is also unresolved.
5. The general harmonic classification, general spatial embedding and
   cancellation problems, and Question 4.21 of Dasgupta–Gaifullin remain
   unresolved by this work. Questions Q.1–Q.2 in Shastri's 1992 paper were
   already answered by Shastri and are not attributed to this project.

## Reproduction

Tested mathematical package: Python 3.12, SymPy 1.14.0. From `computations/`:

```sh
python -m pip install -r requirements.txt
python run_all_checks.py
```

The recorded full run dated 28 October 2026 is **PASS 35/35**. Program counts
are not theorem counts. Runnable code has English comments. The archive
preserves 292 original inputs; documentation-only edits were checked in
56 Python programs and seven GAP/Macaulay2 source files. GAP/Macaulay2 source
and historical logs are included, but no fresh run of those interpreters is
claimed. The optional `--full` discovery mode was not part of the 35/35 run.

The English addition changes no mathematical code, certificate or computation
log. It does not claim a new execution of the same 35 programs. Before running
programs that regenerate results, verify the delivered snapshot from this directory:

```sh
python verify_delivery.py
```

## Overleaf

Upload the separate English source ZIP using **New Project → Upload Project**.
Select `main.tex` as the main document and **XeLaTeX** as the compiler.
Alternatively, import the contents of `overleaf_en/` from the complete update.
The Russian project remains separately available in `overleaf/`.

## Repository installation

The inspected upstream baseline is
`b954f3609e900761fddc9c8ff03d8301e9604cab`.
The complete ZIP uses repository-relative paths beginning with `appendices/`.
Copy that directory into the local repository root, previously supplied by the author:

```text
C:\Users\comp\Documents\GitHub\abhyankar-moh-trefoil
```

The research update is under:

```text
appendices/2026-10-26-harmonic-lnd/updates/2026-10-28/
```

All 75 files of the appendix dated 26 October and the original manuscript remain
unchanged. If the earlier Russian-only update of 28 October is already installed,
the English addition introduces new English files and refreshes only its pointer,
README, provenance, delivery status and manifest. See
[ENGLISH_ADDITION.md](ENGLISH_ADDITION.md) for the exact scope. Preserve any
subsequent edits you made before replacing those metadata files.

Review the additions in GitHub Desktop, commit them and push through an account
with write permission. Preparing or downloading this ZIP does not publish a commit.
