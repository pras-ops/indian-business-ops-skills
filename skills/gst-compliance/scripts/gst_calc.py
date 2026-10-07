#!/usr/bin/env python3
"""Deterministic GST helpers — validation and arithmetic that an agent should call rather
than compute in its head.

Design rule for this pack: the language model decides *what* to do; code decides the exact
numbers. Nothing here hardcodes a tax rate or slab — the rate is always supplied by the caller
(from the GST portal rate finder), so this file stays correct when rates change.

CLI:
    python gst_calc.py validate 29GGGGG1314R9Z6
    python gst_calc.py parse    29GGGGG1314R9Z6
    python gst_calc.py split    --taxable 1000 --rate 18 --intra
    python gst_calc.py split    --taxable 1000 --rate 18            # inter-state (IGST)

Every command prints JSON.
"""

from __future__ import annotations

import argparse
import json
from decimal import ROUND_HALF_UP, Decimal

# GSTIN check-digit alphabet: digits then A-Z (base 36), per the GSTN specification.
_GSTIN_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# GST state / UT codes (first two characters of a GSTIN).
STATE_CODES = {
    "01": "Jammu and Kashmir", "02": "Himachal Pradesh", "03": "Punjab",
    "04": "Chandigarh", "05": "Uttarakhand", "06": "Haryana", "07": "Delhi",
    "08": "Rajasthan", "09": "Uttar Pradesh", "10": "Bihar", "11": "Sikkim",
    "12": "Arunachal Pradesh", "13": "Nagaland", "14": "Manipur", "15": "Mizoram",
    "16": "Tripura", "17": "Meghalaya", "18": "Assam", "19": "West Bengal",
    "20": "Jharkhand", "21": "Odisha", "22": "Chhattisgarh", "23": "Madhya Pradesh",
    "24": "Gujarat", "25": "Daman and Diu", "26": "Dadra and Nagar Haveli and Daman and Diu",
    "27": "Maharashtra", "28": "Andhra Pradesh (old)", "29": "Karnataka", "30": "Goa",
    "31": "Lakshadweep", "32": "Kerala", "33": "Tamil Nadu", "34": "Puducherry",
    "35": "Andaman and Nicobar Islands", "36": "Telangana", "37": "Andhra Pradesh",
    "38": "Ladakh", "97": "Other Territory", "99": "Centre Jurisdiction",
}

# PAN 4th character → entity type (a GSTIN carries a PAN in positions 3-12).
PAN_ENTITY = {
    "P": "Individual", "C": "Company", "H": "HUF", "F": "Firm / LLP",
    "A": "Association of Persons (AOP)", "T": "Trust", "B": "Body of Individuals (BOI)",
    "L": "Local Authority", "J": "Artificial Juridical Person", "G": "Government",
}


def gstin_check_digit(first14: str) -> str:
    """Return the expected 15th (check) character for the first 14 characters of a GSTIN."""
    mod = len(_GSTIN_ALPHABET)  # 36
    factor = 2
    total = 0
    for ch in reversed(first14.upper()):
        value = _GSTIN_ALPHABET.index(ch)
        addend = factor * value
        factor = 1 if factor == 2 else 2
        addend = (addend // mod) + (addend % mod)
        total += addend
    check = (mod - (total % mod)) % mod
    return _GSTIN_ALPHABET[check]


def validate_gstin(gstin: str) -> dict:
    """Validate a GSTIN's structure, state code and check digit.

    Returns {"valid": bool, "reason": str, ...}. A valid structure with a bad check digit is
    reported as invalid — that catches most typos.
    """
    raw = (gstin or "").strip().upper()
    if len(raw) != 15:
        return {"valid": False, "reason": f"GSTIN must be 15 characters, got {len(raw)}"}
    if not all(c in _GSTIN_ALPHABET for c in raw):
        return {"valid": False, "reason": "GSTIN may contain only digits and A-Z"}
    if raw[:2] not in STATE_CODES:
        return {"valid": False, "reason": f"Unknown state code '{raw[:2]}'"}

    pan = raw[2:12]
    pan_check = validate_pan(pan)
    if not pan_check["valid"]:
        return {"valid": False, "reason": f"Embedded PAN invalid: {pan_check['reason']}"}

    # Position 14 (index 13) is normally 'Z' by default but other letters occur; don't hard-fail.
    expected = gstin_check_digit(raw[:14])
    if raw[14] != expected:
        return {
            "valid": False,
            "reason": f"Check digit mismatch: expected '{expected}', got '{raw[14]}' "
            "(likely a typo)",
        }
    return {
        "valid": True,
        "reason": "ok",
        "gstin": raw,
        "state_code": raw[:2],
        "state": STATE_CODES[raw[:2]],
        "pan": pan,
        "entity_type": PAN_ENTITY.get(pan[3], "Unknown"),
        "entity_number": raw[12],
    }


def parse_gstin(gstin: str) -> dict:
    """Break a GSTIN into its parts (validates first)."""
    return validate_gstin(gstin)


def validate_pan(pan: str) -> dict:
    """Structural validation of a PAN (5 letters, 4 digits, 1 letter) plus entity-type decode.

    PAN has no public checksum, so this checks the published structure only.
    """
    raw = (pan or "").strip().upper()
    if len(raw) != 10:
        return {"valid": False, "reason": f"PAN must be 10 characters, got {len(raw)}"}
    letters, digits, last = raw[:5], raw[5:9], raw[9:]
    if not (letters.isalpha() and digits.isdigit() and last.isalpha()):
        return {"valid": False, "reason": "PAN must be 5 letters, 4 digits, then 1 letter"}
    return {
        "valid": True,
        "reason": "ok",
        "pan": raw,
        "entity_type": PAN_ENTITY.get(raw[3], f"Unknown ('{raw[3]}')"),
    }


def _money(x) -> Decimal:
    return Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def split_tax(taxable, rate, intra_state: bool) -> dict:
    """Split GST on a taxable value at a given rate.

    `rate` is the total GST rate as a percentage (e.g. 18 for 18%). It is supplied by the caller
    from the portal — this function never assumes a slab. Intra-state → CGST + SGST (half each);
    inter-state → IGST.
    """
    taxable_d = _money(taxable)
    rate_d = Decimal(str(rate))
    total_tax = _money(taxable_d * rate_d / Decimal(100))
    result = {
        "taxable_value": float(taxable_d),
        "rate_percent": float(rate_d),
        "intra_state": bool(intra_state),
    }
    if intra_state:
        half = _money(total_tax / 2)
        # Put any rounding remainder on CGST so cgst + sgst == total_tax exactly.
        result["cgst"] = float(_money(total_tax - half))
        result["sgst"] = float(half)
        result["igst"] = 0.0
    else:
        result["cgst"] = 0.0
        result["sgst"] = 0.0
        result["igst"] = float(total_tax)
    result["total_tax"] = float(total_tax)
    result["invoice_total"] = float(_money(taxable_d + total_tax))
    return result


def _main() -> None:
    p = argparse.ArgumentParser(description="Deterministic GST helpers (validation + arithmetic).")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate").add_argument("gstin")
    sub.add_parser("parse").add_argument("gstin")
    sp = sub.add_parser("split")
    sp.add_argument("--taxable", required=True)
    sp.add_argument("--rate", required=True, help="total GST rate %, from the portal")
    sp.add_argument("--intra", action="store_true", help="intra-state (CGST+SGST); omit for IGST")

    args = p.parse_args()
    if args.cmd in ("validate", "parse"):
        print(json.dumps(validate_gstin(args.gstin), indent=2))
    elif args.cmd == "split":
        print(json.dumps(split_tax(args.taxable, args.rate, args.intra), indent=2))


if __name__ == "__main__":
    _main()
