# Build the paper

Researchers: Ivan Dorofeev (Independent Researcher) and Alexander Frolov
(Higher School of Modern Mathematics, MIPT).

Compile `main.tex` twice with pdfLaTeX:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The repository copy of the compiled paper is `rectification.pdf`.
The Overleaf ZIP has the same root layout as the repository. On Overleaf, select `paper/main.tex` as the main document and pdfLaTeX as the compiler.
Keep `trefoil_explicit.tex` and `harmonic_explicit.tex` in the same directory;
they contain the coordinate-only formulas for both maps and their inverses.
Keep `references.tex` alongside them for the linked bibliography.

The reproducible computational certificate is `../verify.py`; its successful
run is recorded in `../verification.log`. The Overleaf archive preserves this repository layout.

Keep `chebyshev_note.tex` and `acknowledgements.tex` alongside `main.tex`. The expanded appendix formulas are checked directly by `../verify_printed_formulas.py`; CAS verification instructions are in `../VERIFICATION.md`.
