#!/usr/bin/env python3
"""Verify the delivered snapshot without executing any research program."""
import hashlib
from pathlib import Path
import sys

base = Path(__file__).resolve().parent
failures = []
checked = 0
for line in (base / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    expected, relative = line.split("  ", 1)
    target = base / relative
    # The manifest records package-relative paths, never arbitrary system paths.
    if not target.resolve().is_relative_to(base):
        failures.append(f"Unsafe manifest path: {relative}")
        continue
    if not target.is_file():
        failures.append(f"Missing file: {relative}")
        continue
    actual = hashlib.sha256(target.read_bytes()).hexdigest()
    if actual != expected:
        failures.append(f"Hash mismatch: {relative}")
    checked += 1
for failure in failures:
    print(failure)
print(f"{'FAIL' if failures else 'PASS'}: checked {checked} delivered files")
sys.exit(1 if failures else 0)
