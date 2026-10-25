#!/usr/bin/env python3
"""Deliberately break isolated copies and require exact verification to fail.

Run: python verification/run_negative_controls.py
Requires SymPy. All original sources remain unchanged. Logs are written to
verification/negative_control_logs, or to the directory supplied by --output.
"""
from pathlib import Path
import argparse
import ast
import json
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]


def internal_case(case):
    # Load the actual arithmetic/check functions, before either construction.
    tree = ast.parse((ROOT/'verify.py').read_text(encoding='utf-8'))
    prefix = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == 'started'
                for target in node.targets):
            break
        prefix.append(node)
    namespace = {}
    exec(compile(ast.Module(body=prefix, type_ignores=[]), 'verify.py', 'exec'), namespace)
    if case == 'false_identity':
        namespace['check']('deliberately false identity', namespace['one'])
    elif case == 'nondivisible_numerator':
        namespace['div_x'](namespace['one'], 1)
    else:
        raise ValueError(case)
    raise RuntimeError('A deliberately false certificate was incorrectly accepted')


def copy_minimal_repository(destination):
    (destination/'paper').mkdir(parents=True)
    for name in ['verify.py','verify_printed_formulas.py']:
        shutil.copy2(ROOT/name, destination/name)
    for name in ['trefoil_explicit.tex','harmonic_explicit.tex']:
        shutil.copy2(ROOT/'paper'/name, destination/'paper'/name)
    shutil.copytree(ROOT/'verification', destination/'verification',
                    ignore=shutil.ignore_patterns('__pycache__','negative_control_logs','*.log'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=ROOT/'verification/negative_control_logs')
    parser.add_argument('--internal-case', choices=['false_identity','nondivisible_numerator'],
                        help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.internal_case:
        internal_case(args.internal_case)
        return
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    rows = []

    def run(label, argv, expected, marker):
        start = time.perf_counter()
        result = subprocess.run([sys.executable, *argv], text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (output/(label+'.log')).write_text(result.stdout, encoding='utf-8')
        row = dict(label=label, exit_code=result.returncode, expected_exit=expected,
                   marker_present=marker in result.stdout,
                   seconds=round(time.perf_counter()-start,3))
        rows.append(row)
        if result.returncode != expected or marker not in result.stdout:
            raise RuntimeError(row)
        print('PASS',label,'exit',result.returncode)

    script = str(Path(__file__).resolve())
    run('false_identity_optimized', ['-O',script,'--internal-case','false_identity'],1,
        'AssertionError: deliberately false identity')
    run('nondivisible_numerator_optimized', ['-O',script,'--internal-case','nondivisible_numerator'],1,
        'ArithmeticError: The numerator is not divisible')
    # These positive checks exercise token consumption and guards under -O.
    for curve in ['trefoil','harmonic']:
        auditor = 'audit_trefoil.py' if curve == 'trefoil' else 'audit_harmonic_independent.py'
        marker = 'PASS all six literal components equal compact formulas after 0 in-memory changes' if curve == 'trefoil' else 'inverse3 difference (inverse x,y,z = X,U,V): 0'
        run('positive_'+curve+'_optimized', ['-O',str(ROOT/'verification'/auditor),
            '--repository',str(ROOT),'--expect-correct'],0,marker)

    for curve in ['trefoil','harmonic']:
        with tempfile.TemporaryDirectory(prefix='rectification_negative_') as temp:
            altered = Path(temp)/'repository'
            copy_minimal_repository(altered)
            tex = altered/'paper'/f'{curve}_explicit.tex'
            text = tex.read_text(encoding='utf-8')
            if curve == 'trefoil':
                correct, wrong = '- 21350 a - 1302', '- 21350 a + 1302'
            else:
                patch = json.loads((ROOT/'verification/harmonic_corrections.json').read_text())[0]
                correct, wrong = patch['new'], patch['old']
            if text.count(correct) != 1:
                raise RuntimeError(('The control mutation is not unique',curve))
            tex.write_text(text.replace(correct,wrong,1),encoding='utf-8')
            marker = 'FAIL: printed formulas differ' if curve == 'trefoil' else 'TOTAL 1 unequal of 6'
            run('negative_'+curve+'_wrapper', ['-O',str(altered/'verify_printed_formulas.py')],1,marker)
            if curve == 'harmonic':
                run('negative_harmonic_standalone_optimized', ['-O',str(altered/'verification/audit_harmonic.py'),
                    '--repo',str(altered),'--output',str(Path(temp)/'results')],1,marker)
    (output/'results.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
    print('ALL NEGATIVE CONTROLS REJECTED; OPTIMIZED POSITIVE CHECKS PASSED')


if __name__ == '__main__':
    main()
