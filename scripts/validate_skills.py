#!/usr/bin/env python3
"""Fail if any skill is missing a SKILL.md or a name/description in its YAML frontmatter.

A standalone check (no external skill tooling needed) so CI can gate the pack.
"""

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent


def problems_for(skill_md: Path) -> list[str]:
    """Return a list of problems with one skill's SKILL.md (empty means valid)."""
    folder = skill_md.parent.name
    text = skill_md.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return ["no YAML frontmatter"]
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        return [f"invalid YAML ({e})"]
    found = []
    name = str(fm.get("name", "")).strip()
    if name != folder:
        found.append(f"name '{name}' must equal the folder name '{folder}'")
    if not str(fm.get("description", "")).strip():
        found.append("missing description")
    return found


def main() -> int:
    skills = sorted(ROOT.glob("skills/*/SKILL.md"))
    all_ok = True
    for skill_md in skills:
        folder = skill_md.parent.name
        issues = problems_for(skill_md)
        if issues:
            all_ok = False
            for issue in issues:
                print(f"FAIL {folder}: {issue}")
        else:
            print(f"ok   {folder}")
    print("\nAll skills valid." if all_ok else "\nValidation failed.")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
