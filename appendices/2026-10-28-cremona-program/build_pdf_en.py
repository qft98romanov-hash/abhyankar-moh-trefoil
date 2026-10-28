#!/usr/bin/env python3
"""Build the English Appendix 2 preprint with standard pdfLaTeX packages."""
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent


def main():
    """Run two passes and reject missing glyphs, unresolved links or overflow."""
    engine = shutil.which("pdflatex")
    if engine is None:
        raise SystemExit("pdfLaTeX is required. Install TeX Live or MiKTeX, or use Overleaf.")
    for _ in range(2):
        subprocess.run(
            [engine, "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
            cwd=ROOT / "latex_en", check=True,
        )
    log = (ROOT / "latex_en/main.log").read_text(encoding="utf-8", errors="replace")
    forbidden = ("Missing character:", "There were undefined references",
                 "There were undefined citations", "Overfull ")
    if any(message in log for message in forbidden):
        raise SystemExit("Review the LaTeX log: unresolved or overflowing content remains.")
    destination = ROOT / "appendix2_cremona_program_en.pdf"
    shutil.copyfile(ROOT / "latex_en/main.pdf", destination)
    print(destination)


if __name__ == "__main__":
    main()
