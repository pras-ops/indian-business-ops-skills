#!/usr/bin/env bash
# Rebuild the one-click .skill packages in dist/ from the skills/ folders.
#
# A .skill file is just a zip of a skill directory with its SKILL.md at the root,
# which Claude.ai / Claude apps accept as a one-step install. This script needs
# no special tooling — just zip.
#
# Usage:  bash scripts/build-skills.sh
set -euo pipefail
cd "$(dirname "$0")/.."

mkdir -p dist
rm -f dist/*.skill

for dir in skills/*/; do
  name="$(basename "$dir")"
  # Each skill must have exactly one SKILL.md at its root.
  if [ ! -f "$dir/SKILL.md" ]; then
    echo "skip $name (no SKILL.md)"; continue
  fi
  ( cd skills && zip -q -r -X "../dist/$name.skill" "$name" \
      -x '*/__pycache__/*' '*.pyc' '*/.DS_Store' )
  echo "built dist/$name.skill"
done

echo "Done. $(ls -1 dist/*.skill | wc -l) packages in dist/."
