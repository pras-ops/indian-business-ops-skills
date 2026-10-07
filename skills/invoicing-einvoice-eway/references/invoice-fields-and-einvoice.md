# Invoice fields, e-invoice and e-way bill

> Snapshot written October 2026. Field rules and thresholds are set by the CGST Rules and changed
> by notification. **Confirm on https://www.gst.gov.in, https://einvoice.gst.gov.in and
> https://ewaybillgst.gov.in before relying on any threshold.**

## Tax invoice — mandatory fields

1. Supplier's **name, address and GSTIN**.
2. A **consecutive serial number**, unique within a series, for the financial year (letters/numbers/
   "/" and "-" allowed).
3. **Date** of issue.
4. Recipient's **name, address and GSTIN** (if registered). For B2C above a value, name/address and
   place of supply.
5. **HSN code** (goods) / **SAC** (services) — digit count per turnover.
6. Description, quantity (with unit), total **value**.
7. **Taxable value** (after discount).
8. **Rate and amount** of tax, split as **CGST + SGST/UTGST** (intra-state) or **IGST**
   (inter-state); cess if any.
9. **Place of supply** (and the state) for inter-state supplies.
10. Whether tax is payable on **reverse charge**.
11. Address of delivery where different from place of supply.
12. **Signature / digital signature** of the supplier or authorised person.

Export invoices carry an endorsement ("SUPPLY MEANT FOR EXPORT ... ON PAYMENT OF IGST" or "... UNDER
LUT WITHOUT PAYMENT OF IGST") and buyer details per the shipping docs.

## Document types

| Document | When |
|---|---|
| **Tax invoice** | Taxable supply by a regular registered supplier |
| **Bill of supply** | Exempt supply, or a **composition** dealer (no tax charged) |
| **Receipt voucher** | On receiving an advance |
| **Refund voucher** | Refunding an advance where no supply happened |
| **Credit note** | Reduce value/tax of an earlier invoice (report in GSTR-1) |
| **Debit note** | Increase value/tax of an earlier invoice (report in GSTR-1) |
| **Payment voucher** | For RCM payments to an unregistered supplier |
| **Delivery challan** | Movement without a tax invoice (job work, etc.) |

## Numbering discipline

- Consecutive and unique within a series per financial year; no gaps or duplicates.
- Multiple series are allowed (e.g. per branch) if each is internally consecutive.
- Breaks and repeats are a common audit flag and can block the buyer's ITC.

## E-invoice (IRN + QR)

- **Trigger:** supplier's **aggregate turnover** crossing the notified limit (lowered in stages —
  verify the current figure and whether the business is covered).
- **Scope:** B2B invoices, exports, and credit/debit notes. **B2C is excluded** (though a covered
  supplier may need a **dynamic QR** on B2C — verify).
- **Process:** report the invoice JSON to the **IRP**; it returns a signed **IRN** and a **QR code**
  to print on the invoice. This is your invoice, registered — not a separate document.
- **Consequence:** for a covered supplier, an invoice **without a valid IRN** is not a valid tax
  invoice; the buyer's ITC is at risk.
- **Time limit:** large taxpayers may have a limited window to report older invoices to the IRP —
  check the current rule.

## E-way bill

- **Trigger:** movement of **goods** where the consignment value crosses the threshold. Thresholds
  and some exemptions (short distance, specific goods, intra-state rules) **vary by state** —
  verify for the origin/destination states.
- **Parts:** **Part A** (GSTIN, invoice, value, HSN, place) and **Part B** (transporter ID / vehicle
  number). Part B can be updated when the vehicle is known.
- **Validity:** tied to distance; a bill expires and must be extended for long hauls.
- Generated on https://ewaybillgst.gov.in (or via API / the e-invoice flow, which can create it
  together with the IRN).

## Official sources

- GST portal: https://www.gst.gov.in
- E-invoice (IRP): https://einvoice.gst.gov.in
- E-way bill: https://ewaybillgst.gov.in
