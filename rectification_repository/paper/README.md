# Build the paper

Author: Ivan Dorofeev, Independent Researcher.

Compile `main.tex` twice with pdfLaTeX:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The repository copy of the compiled paper is `rectification.pdf`.
On Overleaf, select `main.tex` as the main document and pdfLaTeX as the compiler.
Keep `trefoil_explicit.tex` and `harmonic_explicit.tex` in the same directory;
they contain the coordinate-only formulas for both maps and their inverses.
Keep `references.tex` alongside them for the linked bibliography.

The reproducible computational certificate is `../verify.py`; its successful
run is recorded in `../verification.log`. In the standalone Overleaf archive,
these files are placed alongside `main.tex`.
