#!/usr/bin/env python3
"""Run normal and optimized exact certificates and compare their results."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from time import perf_counter


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=3)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    verifier = root / "computations" / "verify_appendix2.py"
    results = root / "results"
    started = perf_counter()
    summaries = []
    documents = []
    for name, options in (("normal", []), ("optimized", ["-O"])):
        destination = results / name
        destination.mkdir(parents=True, exist_ok=True)
        command = [sys.executable, *options, str(verifier), "--max-n", str(args.max_n),
                   "--output-dir", str(destination)]
        with (destination / "process.log").open("w", encoding="utf-8") as log:
            result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT,
                                    check=False, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"{name} run failed; inspect {destination / 'process.log'}")
        document = json.loads((destination / "verification.json").read_text(encoding="utf-8"))
        if document["status"] != "PASS":
            raise RuntimeError(f"{name} did not report PASS")
        documents.append(document)
        summaries.append({"mode": name, "returncode": result.returncode,
                          "number_of_checks": len(document["checks"]),
                          "elapsed_seconds": document["elapsed_seconds"]})
        print(f"PASS: {name}: {len(document['checks'])} checks", flush=True)
    # Ignore only run metadata. The polynomial data and every check must agree.
    for field in ("checks", "families", "finite_family_range", "scope"):
        if documents[0][field] != documents[1][field]:
            raise AssertionError(f"Normal and optimized runs disagree on {field}")
    summary = {"status": "PASS", "normal_optimized_results_identical": True,
               "finite_family_range": [1, args.max_n], "runs": summaries,
               "source_sha256": hashlib.sha256(verifier.read_bytes()).hexdigest(),
               "elapsed_seconds": round(perf_counter()-started, 3)}
    (results / "run_summary.json").write_text(json.dumps(summary, indent=2)+"\n", encoding="utf-8")
    (results / "run_summary.log").write_text(
        "PASS: normal and optimized exact polynomial results agree.\n"
        "The negative controls were detected in both modes.\n"
        "Finite tests do not replace the manuscript proofs for all N.\n", encoding="utf-8")
    print("PASS: normal and optimized exact results agree", flush=True)


if __name__ == "__main__":
    main()
