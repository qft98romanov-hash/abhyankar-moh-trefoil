#!/usr/bin/env python3
"""Check formula and structural parity of the complete English translation.

This mechanical check complements a prose review; it does not prove that a
translation is semantically correct. Text labels inside formulas are ignored,
and one explicitly documented notational clarification is normalized below.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

BASE = Path(__file__).resolve().parents[2]
RUSSIAN = BASE / "overleaf" / "sections"
ENGLISH = BASE / "overleaf_en" / "sections"
MATH = re.compile(
    r"(?<!\\)\\\[(.*?)\\\]|(?<!\\)\\\((.*?)\\\)|"
    r"(?<!\\)\$(?!\$)(.*?)(?<!\\)\$|"
    r"\\begin\{equation\}(.*?)\\end\{equation\}", re.S
)


def formulas(text, filename):
    values = []
    for match in MATH.finditer(text):
        value = next(group for group in match.groups() if group is not None)
        # Short prose labels such as "for" and "where" are translated.
        value = re.sub(r"\\text\{[^{}]*\}", r"TEXT_LABEL", value)
        value = re.sub(r"\s+", "", value)
        # The Russian prose already specifies the degree of M here.
        if filename == "03_continuation.tex" and value == "M>10":
            value = r"\degM>10"
        values.append(value)
    return Counter(values)


records = []
for source in sorted(RUSSIAN.glob("*.tex")):
    target = ENGLISH / source.name
    ru = source.read_text(encoding="utf-8")
    en = target.read_text(encoding="utf-8")
    ru_math, en_math = formulas(ru, source.name), formulas(en, source.name)
    checks = {
        "formula_multisets_equal": ru_math == en_math,
        "section_count_equal": len(re.findall(r"\\section\{", ru)) == len(re.findall(r"\\section\{", en)),
        "labels_equal": re.findall(r"\\label\{[^}]*\}", ru) == re.findall(r"\\label\{[^}]*\}", en),
        "citation_keys_equal": re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]*)\}", ru) == re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]*)\}", en),
        "environment_sequences_equal": re.findall(r"\\(begin|end)\{([^}]*)\}", ru) == re.findall(r"\\(begin|end)\{([^}]*)\}", en),
        "no_cyrillic_in_english": re.search(r"[\u0400-\u04ff]", en) is None,
    }
    records.append({
        "file": source.name,
        "russian_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "english_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "mathematical_fragments": sum(ru_math.values()),
        "checks": checks,
        "missing_formulas": list((ru_math - en_math).elements()),
        "extra_formulas": list((en_math - ru_math).elements()),
    })

passed = all(all(record["checks"].values()) for record in records)
result = {
    "date": "2026-10-28",
    "status": "PASS" if passed else "FAIL",
    "translated_section_files": len(records),
    "mathematical_fragments": sum(record["mathematical_fragments"] for record in records),
    "normalization": [
        "Whitespace and translated prose labels inside math are ignored.",
        "Formula multisets allow harmless inline reorderings required by English syntax.",
        "In 03_continuation, M>10 is clarified as deg M>10, as already specified by Russian prose.",
    ],
    "semantic_review": "A separate internal prose review found no omitted proofs, lost hypotheses or stronger claims; this is not external peer review.",
    "computations": "Original 35-program computation run is unchanged and was not repeated for translation.",
    "records": records,
}
(Path(__file__).parent / "translation_audit.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(f"{result['status']}: {len(records)} section files, {result['mathematical_fragments']} mathematical fragments")
if not passed:
    for record in records:
        if not all(record["checks"].values()):
            print(json.dumps(record, indent=2))
sys.exit(0 if passed else 1)
