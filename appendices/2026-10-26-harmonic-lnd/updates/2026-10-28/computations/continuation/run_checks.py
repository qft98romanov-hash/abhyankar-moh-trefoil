#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Run the local exact certificate suite and record per-program execution statuses.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Run final exact verifiers, never the expensive exploratory searches.

The driver uses the Python standard library.  Most child programs need SymPy.
Each child runs in its own source directory with bytecode writing disabled.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
# Units describe the actual finite computations, not counts of new theorems.
CHECKS = [
    ("jet", "embedding_lnd/verify_jet_certificates.py", False,
     "14 paired lower/upper certificates: 8 models at mu=1 and 6 further multiplicities for H378"),
    ("formal_frames", "embedding_lnd/verify_formal_frames.py", False,
     "8 explicit normal frames; universal formal-triviality theorem is proved in prose"),
    ("h457_multiplicity", "embedding_lnd/verify_h457_multiplicity.py", False,
     "1 determinant certificate and 14 upper slices; all-mu minimality uses the written proof"),
    ("h378_linear", "h378/verify_linear_coordinate_obstruction.py", True,
     "13 named algebraic identities, plus sign values; not 13 independent nonexistence theorems"),
    ("h378_uniform", "h378/verify_uniform_obstructions.py", True,
     "20 model indices and 160 polynomial checks; the universal statement needs its proof"),
    ("h457_degree4", "h457/verify_degree4.py", True,
     "35 named exact assertions for one degree-four obstruction"),
    ("h457_independent", "relative_ml/review_457_checks.py", True,
     "Independent rank minors, elimination, resultant and Bezout check; overlaps h457_degree4"),
    ("jet_independent", "relative_ml/review_jet_checks.py", True,
     "27 explicit slices plus 1 uniqueness minor; overlaps the jet certificates"),
    ("relative_ml", "relative_ml/verify_relative_ml.py", True,
     "54 shears = 6 triples x 3 axes x 3 powers; general theorem is proved separately"),
    ("transfer", "relative_lnd/verify_transfer_filtration.py", True,
     "16 finite model cases with several identities per case; not a universal computer proof"),
    ("image_ideal_audit", "literature/verify_image_ideal_audit.py", True,
     "28 selected explicit preimage checks; does not alone prove the general image-ideal formula"),
    ("iterated", "iterated_modifications/verify_iterated_filtration.py", True,
     "3 modification lengths, each with n=0,...,16; universal result uses the written proof"),
    ("iterated_independent", "h378/verify_iterated_review.py", True,
     "5 lengths, 65 binary identities and 81 product identities each, plus Groebner checks"),
    ("mixed_projection_audit", "h457/review_h378_checks.py", True,
     "56 bounded multiplicity pairs and exceptional-parameter checks; not an unbounded search"),
]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stdlib-only", action="store_true", help="Run the first three verifiers, requiring no SymPy")
    parser.add_argument("--only", nargs="+", choices=[c[0] for c in CHECKS], help="Run selected verifier IDs")
    parser.add_argument("--sympy-path", type=Path, help="Existing external directory containing SymPy; no dependency files are copied")
    parser.add_argument("--timeout", type=int, default=600, help="Per-verifier timeout in seconds (default: 600)")
    args = parser.parse_args()
    if sys.flags.optimize:
        parser.error("Do not run with -O or -OO: the verifiers use assert.")
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    selected = [c for c in CHECKS if (not args.stdlib_only or not c[2]) and (not args.only or c[0] in args.only)]
    if not selected:
        parser.error("The selected options leave no verifiers to run.")
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONUNBUFFERED"] = "1"
    env.pop("PYTHONOPTIMIZE", None)
    if args.sympy_path:
        dep = str(args.sympy_path.resolve())
        env["PYTHONPATH"] = dep + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    sympy_version = None
    if any(c[2] for c in selected):
        probe = subprocess.run([sys.executable, "-B", "-c", "import sympy; print(sympy.__version__)"],
                               env=env, text=True, capture_output=True)
        if probe.returncode:
            parser.error("SymPy is unavailable. Install sympy==1.14.0 in this Python environment, pass --sympy-path, or use --stdlib-only.")
        sympy_version = probe.stdout.strip()
    logs = ROOT / "logs"
    logs.mkdir(exist_ok=True)
    results = []
    started = datetime.now(timezone.utc).isoformat()
    for ident, rel, requires_sympy, meaning in selected:
        source = ROOT / rel
        command = [sys.executable, "-B", source.name]
        log = logs / (ident + ".log")
        begin = time.perf_counter()
        print("RUN", ident, flush=True)
        status, returncode = "FAIL", None
        with log.open("w", encoding="utf-8") as stream:
            stream.write("Working directory: " + str(source.parent) + "\n")
            stream.write("Command: " + " ".join(command) + "\n\n")
            stream.flush()
            try:
                completed = subprocess.run(command, cwd=source.parent, env=env, stdout=stream,
                                           stderr=subprocess.STDOUT, timeout=args.timeout)
                returncode = completed.returncode
                status = "PASS" if returncode == 0 else "FAIL"
            except subprocess.TimeoutExpired:
                status = "TIMEOUT"
                stream.write("\nTIMEOUT: " + str(args.timeout) + " seconds\n")
        elapsed = round(time.perf_counter() - begin, 3)
        record = {"id": ident, "script": rel, "working_directory": str(Path(rel).parent),
                  "status": status, "returncode": returncode, "seconds": elapsed,
                  "requires_sympy": requires_sympy, "counting_unit": meaning,
                  "script_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                  "log": str(log.relative_to(ROOT))}
        results.append(record)
        print(status, ident, "(" + str(elapsed) + " s)", flush=True)
    passed = sum(r["status"] == "PASS" for r in results)
    summary = {"started_utc": started, "finished_utc": datetime.now(timezone.utc).isoformat(),
               "status": "PASS" if passed == len(selected) else "FAIL",
               "scope": "full_final_verifier_suite" if len(selected) == len(CHECKS) else "selected_verifiers_only",
               "python_version": sys.version.split()[0], "sympy_version": sympy_version,
               "scripts_selected": len(selected), "scripts_passed": passed,
               "counting_note": "Script counts are not theorem counts. Mathematical check counts overlap and are deliberately not summed.",
               "excluded_searches": ["embedding_lnd/jet_slice_search.py", "h378/search_constant_mixed_projection.py"],
               "results": results}
    target = ROOT / "aggregate_checks.json"
    target.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("RESULT", summary["status"], str(passed) + "/" + str(len(selected)), "scripts;", target, flush=True)
    return 0 if summary["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
