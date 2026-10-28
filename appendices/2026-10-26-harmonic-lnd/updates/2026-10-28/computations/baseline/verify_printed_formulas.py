#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Compare all printed LaTeX components with the compact exact construction.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Read the actual LaTeX formulas and check all twelve components exactly.

Run from any directory: python /path/to/repository/verify_printed_formulas.py
Requires the same SymPy dependency as verify.py. No FLINT is required.
"""
from pathlib import Path
import json
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent

def main():
    optimization = ['-' + 'O'*sys.flags.optimize] if sys.flags.optimize else []
    subprocess.run([
        sys.executable, *optimization, '-u', str(ROOT/'verification/audit_trefoil.py'),
        '--repository', str(ROOT), '--expect-correct'
    ], check=True)
    with tempfile.TemporaryDirectory(prefix='rectification_tex_audit_') as tmp:
        subprocess.run([
            sys.executable, *optimization, '-u', str(ROOT/'verification/audit_harmonic.py'),
            '--repo', str(ROOT), '--output', tmp
        ], check=True)
        results = json.loads((Path(tmp)/'results.json').read_text())
        if len(results) != 6 or not all(row['equal'] for row in results):
            raise RuntimeError('The harmonic LaTeX formulas differ from the compact construction')
    print('ALL 12 PRINTED COMPONENTS MATCH THE COMPACT CONSTRUCTION')

if __name__ == '__main__':
    main()
