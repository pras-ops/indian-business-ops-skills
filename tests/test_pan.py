import pan as p
import pytest


@pytest.mark.parametrize(
    ("pan_no", "entity"),
    [
        ("AAPFU0939F", "Firm / LLP"),      # 4th char F
        ("ABCPK1234Q", "Individual"),       # P
        ("AAACI1234A", "Company"),          # C
        ("AAATR4321H", "Trust"),            # T
    ],
)
def test_valid_pan_decodes_entity(pan_no, entity):
    r = p.validate_pan(pan_no)
    assert r["valid"] is True
    assert r["entity_type"] == entity


@pytest.mark.parametrize(
    ("pan_no", "needle"),
    [
        ("AAPFU0939", "10 characters"),     # too short
        ("AAPF00939F", "5 letters"),        # 5th char is a digit
        ("AAPFU093AF", "5 letters"),        # digit block has a letter
        ("AAAXU0939F", "entity-type"),      # 4th char X is not a valid entity code
    ],
)
def test_invalid_pan_rejected(pan_no, needle):
    r = p.validate_pan(pan_no)
    assert r["valid"] is False
    assert needle.lower() in r["reason"].lower()


def test_lowercase_is_normalised():
    assert p.validate_pan("aapfu0939f")["pan"] == "AAPFU0939F"
