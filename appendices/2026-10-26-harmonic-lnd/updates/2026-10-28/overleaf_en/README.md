# Full English research appendix — 28 October 2026

Author: **Ivan Dorofeev**, Independent Researcher.

This is the complete English counterpart of the Russian research appendix,
including all sixteen sections, mathematical proofs, formulas, status tables,
open questions and fifteen references. **All material remains under verification.**

## Overleaf

1. Choose **New Project → Upload Project** and upload the English Overleaf ZIP.
2. Set **Main document** to `main.tex` and **Compiler** to **XeLaTeX**.
3. Recompile twice to resolve the table of contents and cross-references.

The project is self-contained and uses standard DejaVu and Latin Modern fonts.
It requires no shell escape, bibliography service, private font or external image.
The article class, margins, theorem style and headers follow the preprint layout.

Official upload instructions:
https://docs.overleaf.com/managing-projects-and-files/uploading-a-project

## Local compilation

```sh
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

The full repository update ZIP includes both language versions and the common
computations with English code comments. The mathematical certificates are shared
between the two texts; translation does not introduce additional experimental results.

The Russian source remains in the sibling `overleaf/` directory in the full package.
This English project is in `overleaf_en/`. The source-only Overleaf ZIP contains no
precompiled `main.pdf`, so its displayed PDF is generated from the uploaded source.
