---
name: tds-compliance
description: >-
  Help with Indian TDS and TCS (tax deducted/collected at source) under the Income-tax Act:
  deciding which section applies to a payment (192 salary, 194C contractors, 194J professional/
  technical fees, 194H commission, 194I rent, 194Q purchase of goods, 194O e-commerce, etc.),
  the deduction rate and threshold, higher rates for missing PAN or non-filers, depositing TDS by
  challan, filing quarterly returns (24Q, 26Q, 27Q, 27EQ) and issuing Form 16 / 16A / 16B. Use
  this whenever the user mentions TDS, TCS, a 194-series section, Form 16, Form 26Q/24Q, a TDS
  challan, deducting tax on a vendor or salary payment, Form 26AS or AIS, or a TDS notice/default
  in India — even if they just describe it ("how much tax do we hold back on this consultant's
  bill").
---

# TDS / TCS compliance (India)

TDS (Tax Deducted at Source) makes the **payer** withhold a slice of certain payments and deposit
it with the government against the payee's tax. TCS (Tax Collected at Source) is the mirror for
certain sales. This skill helps a business deduct the right amount, deposit it on time, file the
quarterly returns and issue the certificates.

> [!IMPORTANT]
> Section rates, thresholds and due dates are set by the Income-tax Act and the annual Finance Act
> and change most years. Never assert a current rate or threshold from memory. Confirm it on the
> Income Tax Department site (https://www.incometax.gov.in) or the TRACES portal
> (https://www.tdscpc.gov.in). The reference files here are dated snapshots.
>
> **Section renumbering:** a new Income-tax Act, 2025 is reported to replace the 1961 Act and
> change section numbers. The 192 / 194-series numbers used below are the long-standing ones and
> may no longer be current — identify the payment type first (salary, contract, professional fee,
> rent, …) and confirm the *present* section and rate on the portal rather than relying on the
> number itself.

## The four questions, in order

For any payment, work through these:

1. **Is TDS attracted at all?** Depends on the nature of the payment and whether it crosses the
   section's threshold (per transaction and/or per year). Below the threshold, no deduction.
2. **Which section?** The nature of the payment decides it — salary, contract, professional fees,
   rent, commission, purchase of goods, and so on. Read
   [`references/sections-and-thresholds.md`](references/sections-and-thresholds.md) to match the
   payment to a section and find the current rate/threshold to confirm.
3. **What rate?** The section's rate — but **higher** if the payee has no valid PAN (section 206AA)
   or is a non-filer (section 206AB). Resident vs non-resident changes everything (non-resident
   payments often fall under section 195 with different rules and possible treaty relief).
4. **When to deduct?** Usually at the **earlier of credit or payment** (for salary, at payment).

## Deposit and returns

Deducting is only half the job. Read
[`references/deposit-and-returns.md`](references/deposit-and-returns.md) for:

- Depositing TDS by **challan** (and the monthly due date).
- The **quarterly returns** — 24Q (salary), 26Q (other resident payments), 27Q (non-resident),
  27EQ (TCS) — and how they're prepared and validated.
- Issuing **Form 16** (salary, annual) and **Form 16A** (non-salary, quarterly), downloaded from
  TRACES, and Form 16B (property).

## How to help, concretely

- **"Do we deduct, and how much?"** — Identify the section, confirm the live rate and threshold on
  the portal, check PAN availability and residency, then show the computation as an illustration
  the user can verify.
- **Preparing a quarterly return** — help assemble the deductee-wise data (PAN, section, amount
  paid, tax deducted, challan details) into a clean sheet that maps to the return utility's fields,
  and sanity-check that challan totals tie to the deductions.
- **A default or notice** (short deduction, late deduction, late deposit, PAN errors) — explain the
  mechanism (interest under 201(1A), late-filing fee under 234E, PAN-error demands on TRACES),
  identify the likely cause, and point to the correction process; recommend a professional for
  anything contested.
- **Reconciliation** — match what was deducted and deposited to the payee's **Form 26AS / AIS** so
  credits actually show up for them.

## Guardrails

- Residency matters: resident payments use the 192/194 series; payments to non-residents usually
  fall under **section 195** with different rates, surcharge/cess, and potential DTAA treaty
  benefits (Form 15CA/15CB). Don't apply a resident 194-rate to a non-resident.
- PAN and filing status change the rate — always check both before concluding.
- State the structure confidently; mark every specific rate, threshold and date as "verify on the
  portal". Present tax amounts as illustrations, not advice.
