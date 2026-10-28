# Appendix 2: ready-to-review repository update

Author: Ivan Dorofeev. Date: 28 October 2026.
Status: research branch, all statements remain under verification.

This archive contains:

- `abhyankar-moh-trefoil/`: the complete repository snapshot plus Appendix 2;
- `appendix2-cremona.patch`: a binary Git patch against commit `b954f3609e900761fddc9c8ff03d8301e9604cab`;
- `appendix2_overleaf_2026-10-28.zip`: standalone XeLaTeX sources;
- `SHA256SUMS.txt`: checksums for every other file in this archive.

The original manuscript and Appendix 1 are unchanged. All new mathematical
content is under `appendices/2026-10-28-cremona-program/`. Root integration
changes are limited to README.md, CHANGELOG.md and SHA256SUMS.txt.
The connection used for preparation had read access only; no remote push,
pull request, public release or Overleaf project upload was performed.

## Apply the patch

Use a clean local checkout at the recorded baseline. Keep any personal work
on a separate branch or commit before applying an update. From the checkout:

```sh
git switch -c research/appendix-2-cremona
git apply --check /path/to/appendix2-cremona.patch
git apply /path/to/appendix2-cremona.patch
git diff --check
```

If the checkout has newer commits, inspect and resolve differences rather than
forcing the patch. The archive also contains every proposed file directly.
The patch was checked and applied to a disposable checkout of the baseline;
all resulting file hashes matched the packaged repository snapshot.

## Verify

From the snapshot root, `sha256sum -c SHA256SUMS.txt` checks all file hashes.
For computations and PDF build instructions, see the appendix README.
Normal and optimized verification runs contain 90 passing checks each for
N = 1, 2, 3. The baseline compact verifier and all twelve printed formula
components were also rerun successfully. Other historical logs are preserved
as historical records, not claimed as fresh executions.

Overleaf: import the separate ZIP, select main.tex, and choose XeLaTeX.
The extracted ZIP was compiled successfully in a clean local directory.
