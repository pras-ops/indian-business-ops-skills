#!/usr/bin/env python3
"""Deterministic PAN (Permanent Account Number) helper.

The agent should call this to validate a PAN and read its entity type rather than eyeballing it.
PAN has no public checksum, so this validates the published structure (5 letters, 4 digits, 1
letter) and decodes the 4th character, which encodes the holder's entity type.

CLI:
    python pan.py AAPFU0939F
"""

from __future__ import annotations

import argparse
import json

# PAN 4th character → entity type.
PAN_ENTITY = {
    "P": "Individual",
    "C": "Company",
    "H": "HUF (Hindu Undivided Family)",
    "F": "Firm / LLP",
    "A": "Association of Persons (AOP)",
    "T": "Trust",
    "B": "Body of Individuals (BOI)",
    "L": "Local Authority",
    "J": "Artificial Juridical Person",
    "G": "Government",
}


def validate_pan(pan: str) -> dict:
    """Return {"valid": bool, "reason": str, "pan"?, "entity_type"?}."""
    raw = (pan or "").strip().upper()
    if len(raw) != 10:
        return {"valid": False, "reason": f"PAN must be 10 characters, got {len(raw)}"}
    letters, digits, last = raw[:5], raw[5:9], raw[9:]
    if not letters.isalpha() or not digits.isdigit() or not last.isalpha():
        return {"valid": False, "reason": "PAN must be 5 letters, then 4 digits, then 1 letter"}
    entity = PAN_ENTITY.get(raw[3])
    if entity is None:
        return {
            "valid": False,
            "reason": f"4th character '{raw[3]}' is not a recognised entity-type code",
        }
    return {"valid": True, "reason": "ok", "pan": raw, "entity_type": entity}


def _main() -> None:
    p = argparse.ArgumentParser(description="Validate a PAN and decode its entity type.")
    p.add_argument("pan")
    args = p.parse_args()
    print(json.dumps(validate_pan(args.pan), indent=2))


if __name__ == "__main__":
    _main()
