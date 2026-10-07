# Input Tax Credit (ITC)

> Snapshot written October 2026. ITC conditions and the blocked-credit list are set by the CGST
> Act (notably sections 16 and 17) and amended by notification. Confirm the current position on
> CBIC (https://www.cbic-gst.gov.in) before concluding on any claim.

ITC lets a registered business set the GST paid on its purchases ("inputs") against the GST it
collects on sales. Most real GST questions are ITC questions, so get the conditions right.

## All of these must be true to claim ITC

1. The buyer has a **valid tax invoice** (or debit note / prescribed document).
2. The buyer has **actually received** the goods or services.
3. The supplier has **paid the tax** to the government and **reported the invoice**, so it appears
   in the buyer's **GSTR-2B**.
4. The buyer has **filed the relevant return** (GSTR-3B) claiming it.
5. If the supplier isn't paid within the **prescribed period** (commonly 180 days), the credit is
   reversed and re-claimed when paid.

The practical consequence of condition 3: **if it isn't in your GSTR-2B, you generally can't claim
it** — chase the supplier to upload/file rather than claiming unmatched credit.

## Blocked credits (not available even if the conditions above are met)

Section 17(5) blocks ITC on certain categories regardless. These typically include (confirm the
current list):

- Motor vehicles for personal transport (with specified exceptions, e.g. further supply, transport
  of passengers, driving schools).
- Food and beverages, outdoor catering, beauty, health services, club/fitness memberships (unless
  used to make an outward taxable supply of the same category, or where obligatory under law).
- Works contract and construction of immovable property on own account (with exceptions).
- Goods/services used for **personal consumption**.
- Goods lost, stolen, destroyed, written off, or given as gifts/free samples.

## Apportionment when you make both taxable and exempt supplies

If inputs are used partly for taxable and partly for exempt (or personal) supplies, ITC must be
**apportioned** — only the taxable-use portion is creditable (the Rule 42/43 mechanism). Flag this
whenever a business has a mix of exempt and taxable output.

## 2B reconciliation workflow

When reconciling a purchase register against GSTR-2B, classify each mismatch:

| Symptom | Likely cause | Action |
|---|---|---|
| In books, not in 2B | Supplier hasn't filed / filed late / wrong GSTIN | Chase supplier; don't claim yet |
| In 2B, not in books | Missed entry, or not actually your invoice | Book it, or query the supplier |
| Amount/rate differs | Rate error, or amendment in a later period | Match to the amended invoice |
| GSTIN mismatch | Typo in your records or theirs | Correct the register / ask for amendment |

## Reversals to remember

- Non-payment to supplier within the prescribed period.
- Inputs attributable to exempt supplies (apportionment).
- Goods written off, lost, or given free.

## Official sources

- CBIC-GST (Act, rules, section 16 and 17): https://www.cbic-gst.gov.in
- GST portal (GSTR-2B, filing): https://www.gst.gov.in
