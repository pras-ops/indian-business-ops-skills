"""Put each skill's scripts/ directory on sys.path so the tests can import the helpers."""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
for rel in (
    "skills/gst-compliance/scripts",
    "skills/business-registrations-licenses/scripts",
):
    sys.path.insert(0, str(ROOT / rel))
