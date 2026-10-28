# Research appendix — 28 October 2026

Author: Ivan Dorofeev. Language: Russian. **Research in progress; under verification.**

## Overleaf

1. Choose **New Project → Upload Project** and upload the separate Overleaf ZIP.
2. Set **Main document** to `main.tex` and **Compiler** to **XeLaTeX**.
3. Recompile twice if cross-references or the contents page are not yet resolved.

The project is self-contained. No bibliography service, shell escape, external
image or private font is needed. DejaVu fonts and Latin Modern Math are part of
the normal TeX environment. The article layout follows the source preprint's
article class, geometry and theorem style, with a Unicode font setup for Russian.

Official upload instructions:
https://docs.overleaf.com/managing-projects-and-files/uploading-a-project

## Local compilation

```sh
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

The complete code and certificates are in the separate full update ZIP, under
`computations/`. This source-only ZIP deliberately does not contain a `main.pdf`
that could be mistaken for newly compiled output. All claims remain subject to
checking; the source files contain the exact scope and open questions.
