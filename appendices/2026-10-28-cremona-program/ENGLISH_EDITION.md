# Appendix 2: English research edition

**Ivan Dorofeev and Alexander Frolov — Researchers — 28 October 2026.**

**Alexander Frolov’s affiliation:** Higher School of Modern Mathematics, MIPT.

**Status: research branch, under verification.**

This is the complete English edition of the Russian Appendix 2 dated
28 October 2026. It preserves the mathematical statements, proofs, formulas,
qualifications, literature references and invitation to collaborative research.
It does not claim external independent peer review or publication priority.
The English edition does not modify the original manuscript, Appendix 1,
the Russian Appendix 2, or the computational sources and recorded runs.

- [English research preprint](appendix2_cremona_program_en.pdf).
- [Main LaTeX source](latex_en/main.tex).
- [English edition checksums](SHA256SUMS_EN.txt).
- [Translation and build audit](audit/english_edition_review.json).

## Preprint layout and Overleaf

The preamble follows the original repository preprint: `article`, 11 pt,
A4 paper, 24 mm margins, Latin Modern fonts, AMS mathematical environments,
running page headers, numbered statements, an abstract, a table of contents,
and linked bibliography entries. The authors and date are displayed on the
title page. The research-under-verification declaration is included in full.

Import `appendix2_overleaf_en_2026-10-28.zip` as a new Overleaf project.
Select `main.tex` as the main document and **pdfLaTeX** as the compiler.
The English edition uses standard TeX fonts and needs no external font files,
shell escape, bibliography service or downloaded assets. Run two passes.

From this appendix directory, local compilation is:

```sh
python build_pdf_en.py
```

The generated file is `appendix2_cremona_program_en.pdf`. The build helper
rejects missing characters, unresolved references/citations and overfull boxes.

## Computations and scope

The English manuscript refers to the same exact computational certificates
as the Russian edition. The previously recorded normal and optimized runs
contain 90 passing checks each for N = 1, 2, 3. Their outputs are reused;
the translation itself is not presented as a new computational rerun.
See `computations/README.md`, `PROVENANCE.md` and the existing audit files
for the precise scope and the distinction between finite tests and all-index
mathematical arguments.

## Add this edition using GitHub Desktop on Windows

Extract `appendix2_english_windows_addon_2026-10-28.zip` into a temporary
directory. Copy its `appendices` directory into the existing repository root:

```text
C:\Users\comp\Documents\GitHub\abhyankar-moh-trefoil
```

Merge the directories in File Explorer. The package contains only new
English-edition files at their repository-relative paths. It does not contain
replacement copies of the root README, changelog, root checksum manifest,
Russian manuscript or earlier appendices. In GitHub Desktop, review Changes,
commit with the summary below, and push the commit:

```text
Add English edition of Appendix 2: Cremona research programme
```

The original release checksum manifests still identify their original file
sets. The additional English files have their own `SHA256SUMS_EN.txt`, with
paths relative to this appendix directory. No earlier checksum is rewritten.
