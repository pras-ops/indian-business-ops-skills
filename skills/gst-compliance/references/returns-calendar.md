# GST returns — the form map

> Snapshot written October 2026. Due dates and thresholds change; confirm the live value on the
> GST portal (https://www.gst.gov.in) before relying on any date here. The portal's own compliance
> calendar is the source of truth.

## The main returns

| Return | Who / what | Frequency | Notes |
|---|---|---|---|
| **GSTR-1** | Outward supplies (sales), invoice-wise | Monthly, or quarterly under QRMP | Feeds the buyer's GSTR-2B |
| **IFF** (Invoice Furnishing Facility) | B2B invoices for months 1 and 2 of a quarter | Optional, QRMP only | Lets QRMP sellers pass credit to buyers mid-quarter |
| **GSTR-3B** | Summary of outward tax, ITC, net cash payable | Monthly, or quarterly under QRMP | This is where tax is actually paid |
| **GSTR-2B** | Auto-drafted statement of ITC available | Monthly (static) | Read-only; reconcile your purchases against it |
| **GSTR-9** | Annual return | Yearly | Mandatory above a turnover threshold |
| **GSTR-9C** | Reconciliation statement | Yearly | Above a higher turnover threshold |
| **CMP-08** | Composition dealer quarterly statement-cum-challan | Quarterly | Composition scheme only |
| **GSTR-4** | Composition annual return | Yearly | Composition scheme only |
| **GSTR-5 / 5A** | Non-resident / OIDAR | As applicable | Specialised |
| **GSTR-6** | Input Service Distributor | Monthly | ISD only |
| **GSTR-7 / 8** | TDS (GST) / TCS (e-commerce operators) | Monthly | Different from income-tax TDS |

## Monthly vs quarterly (QRMP)

The **QRMP scheme** (Quarterly Return, Monthly Payment) is available to taxpayers whose aggregate
turnover is at or below a turnover limit (confirm the current limit on the portal). Under QRMP:

- GSTR-1 and GSTR-3B are filed **quarterly**.
- Tax is still **paid monthly** for the first two months via a challan (PMT-06).
- B2B invoices can optionally be uploaded monthly through **IFF** so buyers get their credit without
  waiting for the quarter.

Above the limit, or by choice, a taxpayer files **monthly** GSTR-1 and GSTR-3B.

## Due-date shape (verify each one on the portal)

As an orientation only — the portal's calendar governs, and dates shift for holidays, extensions and
QRMP state categories:

- Monthly **GSTR-1**: around the 11th of the following month.
- Monthly **GSTR-3B**: around the 20th of the following month.
- Quarterly **GSTR-3B** under QRMP: around the 22nd or 24th of the month after the quarter,
  depending on the taxpayer's state category.
- **IFF**: around the 13th of the following month.
- **GSTR-9 / 9C**: typically by 31 December following the financial year.

Always reconfirm, because late filing attracts late fee and interest, and the figure depends on the
exact delay.

## Practical checks before filing

- Do GSTR-1 outward totals reconcile to the GSTR-3B summary and to the books?
- Is every B2B invoice carrying the correct buyer GSTIN (a single wrong digit blocks the buyer's
  credit)?
- Are credit notes and debit notes included in the right period?
- Are reverse-charge (RCM) liabilities captured in 3B?
- Has ITC claimed in 3B been reconciled against the static GSTR-2B?

## Official sources

- GST portal (filing, calendar, rate finder): https://www.gst.gov.in
- CBIC-GST (law, notifications, circulars): https://www.cbic-gst.gov.in
