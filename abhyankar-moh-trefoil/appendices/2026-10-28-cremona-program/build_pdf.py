#!/usr/bin/env python3
"""Build the Appendix 2 preprint with a portable XeLaTeX source tree."""
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent


def main():
    """Use two passes for references; fail immediately on a TeX error."""
    engine = shutil.which("xelatex")
    if engine is None:
        raise SystemExit("XeLaTeX is required. Install TeX Live or use Overleaf.")
    for _ in range(2):
        subprocess.run(
            [engine, "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
            cwd=ROOT / "latex", check=True,
        )
    log = (ROOT / "latex/main.log").read_text(encoding="utf-8", errors="replace")
    forbidden = ("Missing character:", "There were undefined references",
                 "There were undefined citations", "Overfull ")
    if any(message in log for message in forbidden):
        raise SystemExit("Review the LaTeX log: unresolved or overflowing content remains.")
    destination = ROOT / "appendix2_cremona_program_ru.pdf"
    shutil.copyfile(ROOT / "latex/main.pdf", destination)
    print(destination)


if __name__ == "__main__":
    main()
