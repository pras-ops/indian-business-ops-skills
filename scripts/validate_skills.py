#!/usr/bin/env python3
"""Fail if any skill is missing a SKILL.md or a name/description in its YAML frontmatter.

A standalone check (no external skill tooling needed) so CI can gate the pack.
"""

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
ok = True
for skill_md in sorted(ROOT.glob("skills/*/SKILL.md")):
    folder = skill_md.parent.name
    text = skill_md.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        print(f"FAIL {folder}: no YAML frontmatter"); ok = False; continue
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        print(f"FAIL {folder}: invalid YAML ({e})"); ok = False; continue
    name = str(fm.get("name", "")).strip()
    if name != folder:
        print(f"FAIL {folder}: name '{name}' must equal the folder name"); ok = False
    if not str(fm.get("description", "")).strip():
        print(f"FAIL {folder}: missing description"); ok = False
    if ok:
        print(f"ok   {folder}")
print("\nAll skills valid." if ok else "\nValidation failed.")
sys.exit(0 if ok else 1)
