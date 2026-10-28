#!/usr/bin/env python3
"""Run the self-contained exact certificate suite without downloading sources.

The default runs certificates and bounded controls, not expensive discovery.
Use --full to add fresh bounded searches in isolated copies. Search failures
are never interpreted as nonrectifiability. Every subprocess has assertions
enabled, a deterministic working directory, an execution timeout and its own
log. A failed subprocess is recorded and does not suppress subsequent checks.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent

# Each item names a finite verification unit, not a new mathematical theorem.
CHECKS = [
    ('source_comments', 'verify_comment_only_edits.py', (), '63 source files: exact provenance and documentation-only edits'),
    ('original_candidate_identification', 'audit_checks/verify_original_slice.py', (), 'Nine exact identities identifying the original parameter and slice in Conjectures 5.1--5.3'),
    ('base_rectifiers', 'baseline/verify.py', (), 'Two compact rectifications, exact divisions and polynomial inverse certificates'),
    ('printed_components', 'baseline/verify_printed_formulas.py', (), 'All twelve printed components against the compact source'),
    ('shastri_slice_minimum', 'legacy_appendix/research/lnd_certificate/verify_minimal_slice.py', (), 'Degree-six exclusion and degree-seven upper slice'),
    ('shastri_slice_review', 'legacy_appendix/research/repo_audit/review_minimal_slice.py', (), 'Separate implementation of the Shastri degree bound'),
    ('harmonic_slice_minimum', 'legacy_appendix/research/lnd_certificate/verify_harmonic_minimal_slice.py', (), 'Degree-ten exclusion and degree-eleven upper slice'),
    ('harmonic_slice_review', 'legacy_appendix/research/repo_audit/review_harmonic_minimal_slice.py', (), 'Separate implementation of the harmonic degree bound'),
    ('base_lnd', 'legacy_appendix/research/repo_audit/independent_base_lnd.py', (), 'Base Jacobian LND and exact slice numerator identities'),
    ('kernel_coordinates', 'legacy_appendix/research/lnd_certificate/verify_lnd.py', (), 'Factored kernel-coordinate certificate with universal coefficient B'),
    ('periodic_shears', 'legacy_appendix/research/harmonic_literature/periodic_shears.py', (), 'Finite exact controls for the periodic Chebyshev shear formulas'),
    ('repeated_factor_transfer', 'legacy_appendix/research/cremona_lnd/verify_example.py', (), 'Exact transfer across the repeated factor x squared'),
    ('legacy_parameter_obstructions', 'legacy_appendix/research/harmonic_compute/verify_new_results.py', (), 'Specified finite parameter and relative-coordinate calculations'),
    ('bounded_harmonic_reductions', 'legacy_appendix/research/harmonic_compute/reduction_scan.py', (), 'All specified decreasing paths for pairwise-coprime triples up to 100'),
]

CONTINUATION = [
    ('jet', 'embedding_lnd/verify_jet_certificates.py', '14 paired certificates, including eight models at multiplicity one'),
    ('formal_frames', 'embedding_lnd/verify_formal_frames.py', 'Eight explicit normal frames; universal formal triviality requires the proof'),
    ('h457_multiplicity', 'embedding_lnd/verify_h457_multiplicity.py', 'Determinant witness and fourteen upper slices supporting the all-multiplicity argument'),
    ('h378_linear', 'h378/verify_linear_coordinate_obstruction.py', 'Relative linear-coordinate obstruction identities'),
    ('h378_uniform', 'h378/verify_uniform_obstructions.py', 'Twenty model indices and 160 finite identities; unbounded claim uses the proof'),
    ('h457_degree4', 'h457/verify_degree4.py', 'Degree-four parameter and relative-coordinate obstruction'),
    ('h457_review', 'relative_ml/review_457_checks.py', 'Separate rank, resultant and Bezout controls'),
    ('jet_review', 'relative_ml/review_jet_checks.py', 'Twenty-seven explicit slices and a uniqueness minor'),
    ('relative_ml', 'relative_ml/verify_relative_ml.py', 'Fifty-four shear controls; the universal theorem is not inferred from their count'),
    ('transfer_filtration', 'relative_lnd/verify_transfer_filtration.py', 'Sixteen finite kernel, plinth and image-ideal model cases'),
    ('image_ideal_review', 'literature/verify_image_ideal_audit.py', 'Twenty-eight selected exact preimages'),
    ('iterated_filtration', 'iterated_modifications/verify_iterated_filtration.py', 'Three lengths and orders zero through sixteen'),
    ('iterated_review', 'h378/verify_iterated_review.py', 'Separate binary, product and Groebner checks'),
    ('mixed_projection_review', 'h457/review_h378_checks.py', 'Fifty-six bounded multiplicity pairs and exceptional parameters'),
]
CHECKS += [('continuation_' + name, 'continuation/' + path, (), scope)
           for name, path, scope in CONTINUATION]
CHECKS += [
    ('euler_theory', 'euler/verify_theory.py', (), 'Positive finite-closure example and negative normal-field controls'),
    ('euler_divergence', 'euler/verify_divergence_controls.py', (), 'Divergence and fixed-ideal counterexamples'),
    ('euler_h457_naive', 'euler/h457/verify_euler_obstruction.py', (), 'Exact naive-field controls for three harmonic models'),
    ('euler_h457_family', 'euler/h457/normal_search/verify_normal_family.py', (), 'Degree-six obstruction, complete 19-dimensional family and particular-point non-LF certificate'),
    ('euler_h378_naive', 'euler/h378/verify_naive_euler.py', (), 'Parameter and leading-degree controls for the naive-field obstruction'),
    ('euler_h378_family', 'euler/h378/normal_search/verify_normal_certificates.py',
     tuple('normal_degree_' + str(d) + '.json' for d in range(3, 9)) + ('normal_only_degree_7.json',),
     'Exact degree bounds, full 24-dimensional family and the 11-dimensional normal-only control'),
    ('euler_h378_axis', 'euler/h378/normal_search/verify_degree8_axis_obstruction.py', (), 'Particular-point non-LF certificate and limits of the axis argument'),
]

# Full-mode discovery is isolated so it cannot destroy the distributed certificates.
SEARCHES = [
    ('parameter_search', 'legacy_appendix/research/harmonic_compute', 'parameter_search.py', (),
     'Regenerate the specified finite search for low-degree parameter lifts'),
    ('h457_normal_search', 'euler/h457/normal_search', 'search_normal_fields.py', ('6', '7'),
     'Regenerate degree-six and degree-seven normal-field systems'),
    ('h378_normal_search', 'euler/h378/normal_search', 'search_normal_fields.py', ('7', '8'),
     'Regenerate degree-seven and degree-eight normal-field systems'),
]


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def run_one(name, script, arguments, scope, log_folder, timeout, env, kind='certificate'):
    """Run one exact check and return its status without converting failures to PASS."""
    start = time.monotonic()
    log = log_folder / (name + '.log')
    print('RUN', name, flush=True)
    record = {'id': name, 'script': script.relative_to(ROOT).as_posix(),
              'arguments': list(arguments), 'scope': scope, 'kind': kind,
              'source_sha256': hashlib.sha256(script.read_bytes()).hexdigest(),
              'log': log.relative_to(ROOT).as_posix(), 'status': 'FAIL'}
    with log.open('w', encoding='utf-8') as stream:
        stream.write('Working directory (relative): ' + script.parent.relative_to(ROOT).as_posix() + '\n')
        stream.write('Scope: ' + scope + '\n\n')
        stream.flush()
        try:
            completed = subprocess.run([sys.executable, '-B', '-u', script.name, *arguments],
                                       cwd=script.parent, env=env, stdout=stream,
                                       stderr=subprocess.STDOUT, timeout=timeout)
            record['returncode'] = completed.returncode
            record['status'] = 'PASS' if completed.returncode == 0 else 'FAIL'
        except subprocess.TimeoutExpired:
            record['status'] = 'TIMEOUT'
            stream.write('\nTIMEOUT: ' + str(timeout) + ' seconds. This is not a mathematical obstruction.\n')
    record['elapsed_seconds'] = round(time.monotonic() - start, 3)
    print(record['status'], name, record['elapsed_seconds'], 's', flush=True)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list', action='store_true', help='List the selected checks without running them')
    parser.add_argument('--only', nargs='+', choices=[c[0] for c in CHECKS], help='Run selected certificate IDs')
    parser.add_argument('--full', action='store_true', help='Also regenerate the documented bounded searches in isolated copies')
    parser.add_argument('--timeout', type=int, default=900, help='Per-certificate timeout in seconds')
    parser.add_argument('--search-timeout', type=int, default=1800, help='Per-search timeout in full mode')
    args = parser.parse_args()
    if sys.flags.optimize:
        parser.error('Do not use -O or -OO. Exact verifiers contain assertions.')
    if args.timeout <= 0 or args.search_timeout <= 0:
        parser.error('Timeouts must be positive.')
    if args.only and args.full:
        parser.error('--only and --full are mutually exclusive.')
    selected = [c for c in CHECKS if args.only is None or c[0] in args.only]
    if args.list:
        for name, path, arguments, scope in selected:
            print(name + ': ' + path + ' — ' + scope)
        if args.full:
            for name, directory, script, arguments, scope in SEARCHES:
                print(name + ': ' + directory + '/' + script + ' — ' + scope)
        return 0
    env = os.environ.copy()
    env['PYTHONOPTIMIZE'] = '0'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTHONUNBUFFERED'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'
    logs = ROOT / 'verification_logs'
    logs.mkdir(exist_ok=True)
    started = now()
    results = []
    for name, path, arguments, scope in selected:
        results.append(run_one(name, ROOT / path, arguments, scope, logs, args.timeout, env))
    if args.full:
        runs = ROOT / 'full_search_runs'
        runs.mkdir(exist_ok=True)
        for name, directory, script, arguments, scope in SEARCHES:
            destination = runs / name
            shutil.copytree(ROOT / directory, destination, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            results.append(run_one(name, destination / script, arguments, scope,
                                   logs, args.search_timeout, env, kind='bounded_discovery'))
    try:
        sympy_version = importlib.metadata.version('sympy')
    except importlib.metadata.PackageNotFoundError:
        sympy_version = None
    report = {'started_utc': started, 'finished_utc': now(),
              'mode': 'full_with_bounded_discovery' if args.full else ('selected_certificates' if args.only else 'all_certificates'),
              'python': platform.python_version(), 'sympy': sympy_version,
              'status': 'PASS' if all(r['status'] == 'PASS' for r in results) else 'FAIL',
              'passed': sum(r['status'] == 'PASS' for r in results), 'selected': len(results),
              'counting_note': 'Program counts are not theorem counts; many checks overlap.',
              'optional_interpreters': {'GAP': 'NOT_RUN_BY_THIS_DRIVER', 'Macaulay2': 'NOT_RUN_BY_THIS_DRIVER'},
              'results': results}
    (ROOT / 'verification_summary.json').write_text(json.dumps(report, indent=2) + '\n')
    print('RESULT:', report['status'], str(report['passed']) + '/' + str(report['selected']), flush=True)
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
