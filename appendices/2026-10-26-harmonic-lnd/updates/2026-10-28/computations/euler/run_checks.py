#!/usr/bin/env python3
# Consolidated verification copy, 28 October 2026.
# Purpose: Run the local exact certificate suite and record per-program execution statuses.
# Arithmetic and executable statements are preserved from the archived source.
# Use run_all_checks.py from the computations root; do not disable assertions.
# The provenance audit compares Python ASTs after removing documentation strings.
"""Run the bundled exact checks from any working directory.

Only the standard library is used by this runner. Individual symbolic checks
require the version of SymPy recorded in requirements.txt. A failed check does
not prevent the remaining checks from running.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
CHECKS = (
    ("theory", "verify_theory.py", (), ("theory_checks.json",)),
    ("divergence_controls", "verify_divergence_controls.py", (), ("divergence_controls.json",)),
    ("h457_naive", "h457/verify_euler_obstruction.py", (), ("euler_obstruction_certificate.json",)),
    ("h457_normal_family", "h457/normal_search/verify_normal_family.py", (),
     ("independent_verification.json", "family_axis_test.json")),
    ("h378_naive", "h378/verify_naive_euler.py", (), ("naive_euler_certificates.json",)),
    ("h378_normal_family", "h378/normal_search/verify_normal_certificates.py",
     tuple(f"normal_degree_{d}.json" for d in range(3, 9)) + ("normal_only_degree_7.json",),
     ("verification.json",)),
    ("h378_axis_obstruction", "h378/normal_search/verify_degree8_axis_obstruction.py", (),
     ("degree8_axis_obstruction.json", "degree8_family_axis_test.json")),
)


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def local_path(path):
    return path.relative_to(ROOT).as_posix()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="List checks without running them.")
    parser.add_argument("--only", nargs="+", choices=[row[0] for row in CHECKS],
                        help="Run only the named checks, in the standard order.")
    args = parser.parse_args()
    selected = [row for row in CHECKS if args.only is None or row[0] in args.only]
    if args.list:
        for name, script, arguments, _ in selected:
            print(f"{name}: {script}" + (" " + " ".join(arguments) if arguments else ""))
        return 0

    started = utc_now()
    try:
        sympy_version = importlib.metadata.version("sympy")
    except importlib.metadata.PackageNotFoundError:
        sympy_version = None
    log_dir = ROOT / "check_logs"
    log_dir.mkdir(exist_ok=True)
    aggregate_path = ROOT / "aggregate_checks.log"
    result_path = ROOT / "aggregate_checks.json"
    records = []
    interrupted = False
    environment = os.environ.copy()
    # Every verifier uses assertions: never inherit an optimized Python mode.
    environment["PYTHONOPTIMIZE"] = "0"
    environment["PYTHONUNBUFFERED"] = "1"
    environment["PYTHONIOENCODING"] = "utf-8"

    with aggregate_path.open("w", encoding="utf-8") as aggregate:
        aggregate.write(f"Started UTC: {started}\nPython: {platform.python_version()}\n")
        aggregate.write(f"SymPy: {sympy_version or 'NOT INSTALLED'}\n")
        for number, (name, relative_script, arguments, outputs) in enumerate(selected, 1):
            script = ROOT / relative_script
            log_path = log_dir / f"{number:02d}_{name}.log"
            record = {"name": name, "script": relative_script,
                      "working_directory": local_path(script.parent),
                      "arguments": list(arguments), "log": local_path(log_path),
                      "expected_outputs": [local_path(script.parent / p) for p in outputs]}
            if interrupted:
                record.update(status="NOT_RUN", reason="Previous check interrupted by user.")
                records.append(record)
                continue
            start_time = time.monotonic()
            header = f"[{number}/{len(selected)}] {name}: {relative_script}\n"
            print(header.rstrip(), flush=True)
            aggregate.write("\n" + header)
            aggregate.flush()
            process = None
            try:
                if not script.is_file():
                    raise FileNotFoundError(f"Missing script: {relative_script}")
                with log_path.open("w", encoding="utf-8") as individual:
                    process = subprocess.Popen(
                        [sys.executable, "-u", script.name, *arguments],
                        cwd=script.parent, env=environment, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace",
                    )
                    for line in process.stdout:
                        # Keep the distributed logs portable and independent of the extraction path.
                        line = line.replace(str(ROOT) + os.sep, "")
                        individual.write(line)
                        aggregate.write(line)
                        individual.flush()
                        aggregate.flush()
                    return_code = process.wait()
                record["return_code"] = return_code
                if return_code:
                    record.update(status="FAIL", reason="Verifier returned a nonzero exit code.")
                else:
                    # A successful script must also have left a readable JSON certificate.
                    for output in outputs:
                        output_path = script.parent / output
                        with output_path.open(encoding="utf-8") as handle:
                            json.load(handle)
                    record["status"] = "PASS"
            except KeyboardInterrupt:
                interrupted = True
                if process is not None and process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()
                record.update(status="INTERRUPTED", reason="Interrupted by user.")
            except Exception as exc:
                reason = f"{type(exc).__name__}: {exc}".replace(str(ROOT) + os.sep, "")
                record.update(status="FAIL", reason=reason)
                with log_path.open("a", encoding="utf-8") as individual:
                    individual.write(reason + "\n")
                aggregate.write(reason + "\n")
            record["elapsed_seconds"] = round(time.monotonic() - start_time, 3)
            records.append(record)
            summary = f"{name}: {record['status']} ({record['elapsed_seconds']} s)\n"
            print(summary.rstrip(), flush=True)
            aggregate.write(summary)
            aggregate.flush()

    overall = "PASS" if all(row["status"] == "PASS" for row in records) else "FAIL"
    report = {"started_utc": started, "finished_utc": utc_now(),
              "python_version": platform.python_version(), "sympy_version": sympy_version,
              "tested_environment": {"python": "3.12", "sympy": "1.14.0"},
              "scope": "Exact bundled checks; universal assertions require the written proofs.",
              "checks": records, "status": overall}
    result_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Overall: {overall}. Logs: aggregate_checks.log; aggregate_checks.json; check_logs/", flush=True)
    return 130 if interrupted else (0 if overall == "PASS" else 1)


if __name__ == "__main__":
    raise SystemExit(main())
