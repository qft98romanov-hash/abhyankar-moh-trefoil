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
import re
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
    elif case == 'explicit_times':
        # Exercise the actual independent parser without running its CLI or
        # loading the large coordinate polynomials. The first case distinguishes
        # multiplication by a negative operand from subtraction.
        parser_source = ROOT/'verification/audit_harmonic_independent.py'
        parser_tree = ast.parse(parser_source.read_text(encoding='utf-8'))
        declarations = [node for node in parser_tree.body if
                        (isinstance(node, (ast.FunctionDef, ast.ClassDef)) and
                         node.name in {'require', 'TexParser'}) or
                        (isinstance(node, ast.Assign) and any(
                         isinstance(target, ast.Name) and target.id == 'COMMANDS'
                         for target in node.targets))]
        namespace['re'] = re
        exec(compile(ast.Module(body=declarations, type_ignores=[]),
                     str(parser_source), 'exec'), namespace)
        x, y, z = (namespace[name] for name in ('x', 'y', 'z'))
        cases = [(r'x\times-y', -x*y),
                 (r'(x+y)\times(-z)', -(x+y)*z),
                 (r'2\times3', namespace['ring'](6))]
        for formula, expected in cases:
            if namespace['TexParser'](formula).parse() != expected:
                raise AssertionError(('Explicit multiplication parser mismatch', formula))
        print('PASS explicit multiplication parser: 3 cases')
        return
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


def replace_unique(path, correct, wrong):
    text = path.read_text(encoding='utf-8')
    if text.count(correct) != 1:
        raise RuntimeError(('The control mutation is not unique', path.name, correct))
    path.write_text(text.replace(correct, wrong, 1), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=ROOT/'verification/negative_control_logs')
    parser.add_argument('--internal-case', choices=['false_identity','nondivisible_numerator',
                                                   'explicit_times'],
                        help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.internal_case:
        internal_case(args.internal_case)
        return
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    rows = []
    suite_start = time.perf_counter()

    def run(label, argv, expected, markers):
        if isinstance(markers, str):
            markers = (markers,)
        start = time.perf_counter()
        result = subprocess.run([sys.executable, *argv], text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (output/(label+'.log')).write_text(result.stdout, encoding='utf-8')
        row = dict(label=label, command=[sys.executable, *argv],
                   exit_code=result.returncode, expected_exit=expected,
                   markers=list(markers),
                   marker_present=all(marker in result.stdout for marker in markers),
                   seconds=round(time.perf_counter()-start,3))
        rows.append(row)
        # Preserve completed evidence even when a later control fails.
        (output/'results.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
        if result.returncode != expected or not row['marker_present']:
            raise RuntimeError(row)
        print('PASS',label,'exit',result.returncode,flush=True)

    script = str(Path(__file__).resolve())
    run('false_identity_optimized', ['-O',script,'--internal-case','false_identity'],1,
        'AssertionError: deliberately false identity')
    run('nondivisible_numerator_optimized', ['-O',script,'--internal-case','nondivisible_numerator'],1,
        'ArithmeticError: The numerator is not divisible')
    run('positive_explicit_times_optimized', ['-O',script,'--internal-case','explicit_times'],0,
        'PASS explicit multiplication parser: 3 cases')
    run('positive_core_optimized', ['-O','-u',str(ROOT/'verify.py')],0,
        ('PASS: the trefoil inverse callable matches the proved factorization',
         'PASS: the figure-eight inverse callable matches the proved factorization',
         'BOTH RECTIFICATIONS VERIFIED'))
    # These positive checks exercise token consumption and guards under -O.
    for curve in ['trefoil','harmonic']:
        auditor = 'audit_trefoil.py' if curve == 'trefoil' else 'audit_harmonic_independent.py'
        marker = 'PASS all six literal components equal compact formulas after 0 in-memory changes' if curve == 'trefoil' else 'inverse3 difference (inverse x,y,z = X,U,V): 0'
        run('positive_'+curve+'_optimized', ['-O',str(ROOT/'verification'/auditor),
            '--repository',str(ROOT),'--expect-correct'],0,marker)
    with tempfile.TemporaryDirectory(prefix='rectification_positive_') as temp:
        run('positive_harmonic_standalone_optimized',
            ['-O',str(ROOT/'verification/audit_harmonic.py'),
             '--repo',str(ROOT),'--output',temp],0,'TOTAL 0 unequal of 6')

    for curve in ['trefoil','harmonic']:
        with tempfile.TemporaryDirectory(prefix='rectification_negative_') as temp:
            altered = Path(temp)/'repository'
            copy_minimal_repository(altered)
            tex = altered/'paper'/f'{curve}_explicit.tex'
            if curve == 'trefoil':
                correct, wrong = '- 21350 a - 1302', '- 21350 a + 1302'
            else:
                patch = json.loads((ROOT/'verification/harmonic_corrections.json').read_text())[0]
                correct, wrong = patch['new'], patch['old']
            replace_unique(tex,correct,wrong)
            marker = 'FAIL: printed formulas differ' if curve == 'trefoil' else 'TOTAL 1 unequal of 6'
            run('negative_'+curve+'_wrapper', ['-O',str(altered/'verify_printed_formulas.py')],1,marker)
            if curve == 'harmonic':
                run('negative_harmonic_standalone_optimized', ['-O',str(altered/'verification/audit_harmonic.py'),
                    '--repo',str(altered),'--output',str(Path(temp)/'results')],1,marker)

    # A missing TeX exponent brace and a wrong argument order must be rejected
    # by every parser that reads the affected appendix, even under -O.
    for curve, symbol, variable in [('trefoil','T','z'),('harmonic','H','y')]:
        for mutation in ['unbraced_exponent','component_label']:
            with tempfile.TemporaryDirectory(prefix='rectification_syntax_') as temp:
                altered = Path(temp)/'repository'
                copy_minimal_repository(altered)
                tex = altered/'paper'/f'{curve}_explicit.tex'
                if mutation == 'unbraced_exponent':
                    correct, wrong = f'- 14 a {variable}^{{10}}', f'- 14 a {variable}^10'
                    marker = 'AssertionError: Unbraced TeX exponent must be a single digit'
                else:
                    correct = rf'(\Phi_{symbol})_1(x,y,z)'
                    wrong = rf'(\Phi_{symbol})_1(y,x,z)'
                    marker = 'Unexpected component label or argument order'
                replace_unique(tex,correct,wrong)
                auditor = 'audit_trefoil.py' if curve == 'trefoil' else 'audit_harmonic_independent.py'
                run(f'negative_{curve}_{mutation}_optimized',
                    ['-O',str(altered/'verification'/auditor),
                     '--repository',str(altered),'--expect-correct'],1,marker)
                if curve == 'harmonic':
                    run(f'negative_harmonic_{mutation}_standalone_optimized',
                        ['-O',str(altered/'verification/audit_harmonic.py'),
                         '--repo',str(altered),'--output',str(Path(temp)/'results')],1,marker)

    # U = X^3-3X+Y and the original Y must stay distinct. This mutation was
    # formerly invisible to the independent auditor's textual compression.
    with tempfile.TemporaryDirectory(prefix='rectification_coordinate_') as temp:
        altered = Path(temp)/'repository'
        copy_minimal_repository(altered)
        replace_unique(altered/'paper/harmonic_explicit.tex',
                       r'&{}+(X^3-3X+Y)\Bigl[X^{2} - 2\Bigr]',
                       r'&{}+Y\Bigl[X^{2} - 2\Bigr]')
        run('negative_harmonic_u_to_y_independent_optimized',
            ['-O',str(altered/'verification/audit_harmonic_independent.py'),
             '--repository',str(altered),'--expect-correct'],1,
            ('inverse2 difference (inverse x,y,z = X,U,V): -x**5 + 5*x**3 - 6*x',
             'FAIL: printed formulas differ'))
        run('negative_harmonic_u_to_y_standalone_optimized',
            ['-O',str(altered/'verification/audit_harmonic.py'),
             '--repo',str(altered),'--output',str(Path(temp)/'results')],1,
            'TOTAL 1 unequal of 6')

    # This incorrect inverse still agrees on the axis Y=0; the all-variable
    # callable binding must reject it, rather than relying on curve samples.
    with tempfile.TemporaryDirectory(prefix='rectification_callable_') as temp:
        altered = Path(temp)/'repository'
        copy_minimal_repository(altered)
        replace_unique(altered/'verify.py',
                       '            at(inverse_y, xx=X**3-3*X+Y, yy=X,\n'
                       '               zz=Z+(1-a)*(42*X**3-49*X)),',
                       '            red(at(inverse_y, xx=X**3-3*X+Y, yy=X,\n'
                       '               zz=Z+(1-a)*(42*X**3-49*X))+Y),')
        run('negative_harmonic_inverse_callable_optimized',
            ['-O','-u',str(altered/'verify.py')],1,
            'AssertionError: the figure-eight inverse callable matches the proved factorization')

    summary = dict(positive_cases=sum(row['expected_exit']==0 for row in rows),
                   negative_cases=sum(row['expected_exit']!=0 for row in rows),
                   total_cases=len(rows), seconds=round(time.perf_counter()-suite_start,3))
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print('ALL NEGATIVE CONTROLS REJECTED; OPTIMIZED POSITIVE CHECKS PASSED',summary)


if __name__ == '__main__':
    main()
