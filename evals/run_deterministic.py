#!/usr/bin/env python3
"""Grade the deterministic (computational) eval items against the bundled helper scripts.

This covers the part of the pack whose correctness is objective — GSTIN validation, PAN decode,
and the CGST/SGST/IGST split — and prints a pass rate. The judgement questions (graded_by "llm")
are not run here; they need the full with-skill vs without-skill benchmark described in README.md.

Usage:  python evals/run_deterministic.py
Exit status is non-zero if any deterministic item fails, so CI can gate on it.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "skills/gst-compliance/scripts"))
sys.path.insert(0, str(ROOT / "skills/business-registrations-licenses/scripts"))

import gst_calc  # noqa: E402
import pan  # noqa: E402


def grade(item: dict) -> tuple[bool, str]:
    cat = item["category"]
    if cat == "gstin":
        got = gst_calc.validate_gstin(item["input"])["valid"]
        return got == item["expect_valid"], f"valid={got}, expected {item['expect_valid']}"
    if cat == "pan":
        r = pan.validate_pan(item["input"])
        if r["valid"] != item["expect_valid"]:
            return False, f"valid={r['valid']}, expected {item['expect_valid']}"
        if item.get("expect_entity") and r.get("entity_type") != item["expect_entity"]:
            return False, f"entity={r.get('entity_type')!r}, expected {item['expect_entity']!r}"
        return True, "ok"
    if cat == "tax_split":
        got = gst_calc.split_tax(item["taxable"], item["rate"], item["intra"])
        for k, v in item["expect"].items():
            if got[k] != v:
                return False, f"{k}={got[k]}, expected {v}"
        return True, "ok"
    return False, f"unknown deterministic category {cat!r}"


def main() -> int:
    data = json.loads((ROOT / "evals/evals.json").read_text())
    items = [e for e in data["evals"] if e.get("graded_by") == "script"]
    passed = 0
    for it in items:
        ok, detail = grade(it)
        passed += ok
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] #{it['id']:<2} {it['category']:<10} {detail}")
    total = len(items)
    pct = 100.0 * passed / total if total else 0.0
    print(f"\nDeterministic eval: {passed}/{total} passed ({pct:.0f}%).")
    llm = sum(1 for e in data["evals"] if e.get("graded_by") == "llm")
    print(f"({llm} judgement questions not run here — see evals/README.md for the full benchmark.)")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
