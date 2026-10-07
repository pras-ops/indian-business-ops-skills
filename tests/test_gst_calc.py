import gst_calc as g
import pytest

# Structurally valid GSTINs with correct GSTN check digits (used as examples in GST documentation).
VALID_GSTINS = ["27AAPFU0939F1ZV", "07AAGFF2194N1Z1"]


@pytest.mark.parametrize("gstin", VALID_GSTINS)
def test_valid_gstins_pass(gstin):
    assert g.validate_gstin(gstin)["valid"] is True


def test_check_digit_matches_spec():
    # The illustrative "...Z6" GSTIN seen in many tutorials has an incorrect check digit;
    # the correct one for the first 14 chars is 'A'.
    assert g.gstin_check_digit("29GGGGG1314R9Z") == "A"
    assert g.validate_gstin("29GGGGG1314R9ZA")["valid"] is True


@pytest.mark.parametrize(
    ("gstin", "needle"),
    [
        ("29GGGGG1314R9Z6", "Check digit"),   # wrong check digit (common typo)
        ("27AAPFU0939F1ZX", "Check digit"),   # last char corrupted
        ("1234", "15 characters"),            # too short
        ("07AA1FU0939F1ZX", "PAN invalid"),   # PAN segment: 3rd char is a digit
        ("00AAPFU0939F1ZV", "state code"),    # unknown state code 00
    ],
)
def test_invalid_gstins_rejected(gstin, needle):
    r = g.validate_gstin(gstin)
    assert r["valid"] is False
    assert needle.lower() in r["reason"].lower()


def test_parse_exposes_parts():
    r = g.parse_gstin("27AAPFU0939F1ZV")
    assert r["state"] == "Maharashtra"
    assert r["pan"] == "AAPFU0939F"
    assert r["entity_type"] == "Firm / LLP"  # PAN 4th char 'F'


def test_split_intra_state_halves_and_reconciles():
    r = g.split_tax(1000, 18, intra_state=True)
    assert r["cgst"] == 90.0 and r["sgst"] == 90.0 and r["igst"] == 0.0
    assert r["total_tax"] == 180.0 and r["invoice_total"] == 1180.0
    assert round(r["cgst"] + r["sgst"], 2) == r["total_tax"]


def test_split_inter_state_is_igst_only():
    r = g.split_tax(1000, 18, intra_state=False)
    assert r["igst"] == 180.0 and r["cgst"] == 0.0 and r["sgst"] == 0.0


def test_split_rounds_without_losing_a_paisa():
    # An odd taxable value must still have cgst + sgst == total_tax exactly.
    r = g.split_tax(1033.33, 5, intra_state=True)
    assert round(r["cgst"] + r["sgst"], 2) == r["total_tax"]
