#!/usr/bin/env python3
"""Check that every reference file carries a recent `last_verified` date.

Indian tax and company law changes often, so each skills/*/references/*.md must declare when it
was last checked against the official source, as an HTML comment on any line:

    <!-- last_verified: YYYY-MM-DD -->

Exit status:
  1  a reference file is missing the marker, or the date is unparseable  (hard failure)
  0  otherwise  — but files older than --max-age-days are printed as warnings to review

Usage:
  python scripts/check_freshness.py [--max-age-days 90]
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

MARKER = re.compile(r"<!--\s*last_verified:\s*(\d{4}-\d{2}-\d{2})\s*-->")
ROOT = Path(__file__).parent.parent


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-age-days", type=int, default=90)
    args = ap.parse_args()

    today = dt.date.today()
    refs = sorted(ROOT.glob("skills/*/references/*.md"))
    missing, stale, ok = [], [], []
    for f in refs:
        m = MARKER.search(f.read_text())
        rel = f.relative_to(ROOT)
        if not m:
            missing.append(rel)
            continue
        try:
            d = dt.date.fromisoformat(m.group(1))
        except ValueError:
            missing.append(rel)
            continue
        age = (today - d).days
        (stale if age > args.max_age_days else ok).append((rel, age))

    for rel, age in ok:
        print(f"ok      {rel} ({age}d)")
    for rel, age in stale:
        print(f"REVIEW  {rel} — {age}d old (> {args.max_age_days}d); re-verify against the portal")
    for rel in missing:
        print(f"MISSING {rel} — add <!-- last_verified: YYYY-MM-DD -->")

    if missing:
        print(f"\n{len(missing)} file(s) missing a valid last_verified marker.")
        return 1
    if stale:
        print(f"\n{len(stale)} file(s) are older than {args.max_age_days} days — review them.")
    else:
        print(f"\nAll {len(refs)} reference files are marked and within {args.max_age_days} days.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
