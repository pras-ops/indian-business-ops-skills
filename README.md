# Indian Business Ops — Agent Skills

[![CI](https://github.com/pras-ops/indian-business-ops-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/pras-ops/indian-business-ops-skills/actions/workflows/ci.yml)
![Deterministic evals: 17/17](https://img.shields.io/badge/deterministic%20evals-17%2F17-brightgreen.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Jurisdiction: India](https://img.shields.io/badge/jurisdiction-India%20🇮🇳-FF9933.svg)

Agent Skills that help Claude (or any agent that reads the `SKILL.md` format) run the compliance
side of a company in **India** — GST, TDS, payroll, ROC/MCA, registrations, invoicing and Tally.
The model does the judgement; **bundled code does the exact numbers** (GSTIN/PAN validation, the
CGST/SGST/IGST split), and live rates are confirmed on the official portal, never guessed.

## See it work

**You:** We got a bill from a new vendor, GSTIN `27AAPFU0939F1ZX`. Book ₹1,00,000 of consulting at
18% GST — both of us are in Maharashtra.

**Claude, with these skills:**

> I validated the GSTIN first, and it doesn't pass — the check digit is wrong: `27AAPFU0939F1ZX`
> should end in **`V`**, not `X` (a classic typo). A wrong GSTIN silently blocks your input tax
> credit, so confirm it with the vendor before booking the bill.
>
> For ₹1,00,000 at 18%, intra-state (both in Maharashtra) → **CGST + SGST**:
>
> | | Amount |
> |---|---|
> | Taxable | ₹1,00,000 |
> | CGST @ 9% | ₹9,000 |
> | SGST @ 9% | ₹9,000 |
> | **Invoice total** | **₹1,18,000** |
>
> (I took the rate as 18% — confirm the item's current rate on the GST portal; slabs changed in
> Sept 2025.)

Those numbers aren't the model doing mental math — they come from the bundled helper, so they're
exact and reproducible:

```bash
$ python skills/gst-compliance/scripts/gst_calc.py validate 27AAPFU0939F1ZX
{ "valid": false, "reason": "Check digit mismatch: expected 'V', got 'X' (likely a typo)" }

$ python skills/gst-compliance/scripts/gst_calc.py split --taxable 100000 --rate 18 --intra
{ "cgst": 9000.0, "sgst": 9000.0, "igst": 0.0, "total_tax": 18000.0, "invoice_total": 118000.0 }
```

Without the skills, an agent will often skip the checksum entirely and may invent a GST rate. That
difference — validate, compute exactly, verify the rate — is the whole point of the pack.

## What's in the pack

| Skill | What it helps with |
|---|---|
| [`gst-compliance`](skills/gst-compliance) | GST returns (GSTR-1 / 3B / 9), the slab structure, HSN/SAC classification, input tax credit, + a GSTIN validator and tax-split helper |
| [`tds-compliance`](skills/tds-compliance) | Which TDS section applies, deposit timing, quarterly returns (24Q/26Q/27Q), Form 16/16A |
| [`payroll-statutory`](skills/payroll-statutory) | Salary structure, EPF, ESI, Professional Tax, gratuity, payslips, the monthly ECR |
| [`company-roc-compliance`](skills/company-roc-compliance) | MCA/ROC annual filings (AOC-4, MGT-7/7A), DIR-3 KYC, statutory registers and board meetings |
| [`business-registrations-licenses`](skills/business-registrations-licenses) | Picking an entity type and the registrations/licences it needs (PAN/TAN, GSTIN, Udyam, Shops & Est., IEC, FSSAI), + a PAN validator |
| [`invoicing-einvoice-eway`](skills/invoicing-einvoice-eway) | A legally complete tax invoice, e-invoice (IRN/QR) applicability, and the e-way bill |
| [`tally-operations`](skills/tally-operations) | Moving data in and out of Tally (XML/Excel), voucher structure, reconciling books to returns |

## Install

### One command (Claude Code plugin)

```bash
claude plugin marketplace add pras-ops/indian-business-ops-skills
claude plugin install indian-business-ops@pras-ops
```

> Plugin manifests (`.claude-plugin/`) are a newer Claude Code feature; if your version reports a
> manifest error, use a download or copy below and please open an issue so it can be fixed.

### One-click download (`.skill`)

Pre-built, validated packages are in [`dist/`](dist/). On **Claude.ai / Claude apps**, download a
`.skill` and open it, or upload it under **Settings → Capabilities → Skills**.

| Skill | Download |
|---|---|
| GST | [`gst-compliance.skill`](dist/gst-compliance.skill) |
| TDS / TCS | [`tds-compliance.skill`](dist/tds-compliance.skill) |
| Payroll & statutory | [`payroll-statutory.skill`](dist/payroll-statutory.skill) |
| Company / ROC | [`company-roc-compliance.skill`](dist/company-roc-compliance.skill) |
| Registrations & licences | [`business-registrations-licenses.skill`](dist/business-registrations-licenses.skill) |
| Invoicing / e-invoice / e-way | [`invoicing-einvoice-eway.skill`](dist/invoicing-einvoice-eway.skill) |
| Tally | [`tally-operations.skill`](dist/tally-operations.skill) |

### Copy from source

```bash
cp -r skills/gst-compliance ~/.claude/skills/   # one skill for your account
cp -r skills/* .claude/skills/                  # the whole pack for a project
```

**Any other agent runtime** — the skills are plain Markdown with a small YAML header; point your
loader at the `SKILL.md` files.

## Design doctrine

> **The language model decides what to do. Code decides the numbers.**

Exact computation and validation live in tested Python; volatile law (rates, thresholds, due
dates) is never hardcoded but confirmed on the official portal at run time; judgement and
explanation stay with the model. This is the layer *between* an AI agent and the business's
software and portals — the skills + deterministic-engine layer, not an action layer that files on
its own. See [ARCHITECTURE.md](ARCHITECTURE.md).

## Accuracy

The computational core is tested two ways: unit tests in [`tests/`](tests) and a labelled eval set
in [`evals/`](evals). The deterministic questions (GSTIN validation, PAN decode, tax split) pass
**17 / 17** and run in CI. The judgement questions (which TDS section, e-invoice applicability, …)
are set up for a with-skill vs without-skill benchmark — see [`evals/README.md`](evals/README.md).

## Privacy

GST/TDS work involves PANs, GSTINs and sometimes Aadhaar. Before pasting documents into any AI
tool, **mask identifiers you don't need** (show only the last few characters), and never paste full
Aadhaar numbers. For automatic, on-device redaction before text leaves your machine, see
[RedactKit](https://github.com/pras-ops/redactkit).

## How a skill is built

```
skills/<skill-name>/
├── SKILL.md       # YAML frontmatter (name, description) + the workflow
├── references/    # deeper, volatile detail (each dated), read on demand
└── scripts/       # deterministic helpers the skill calls for exact work
```

## Scope and limits

- **Covers:** the recurring compliance a typical private limited company, LLP or proprietorship
  meets. A map and a checklist, not filled-in forms.
- **Does not cover:** a binding legal opinion, a final tax-liability figure as advice, or
  state-specific rules beyond pointing at the right authority (PT, Shops & Est. and labour rules
  differ by state — the skills say so).
- **Always verify** the live number on the official portal before filing.

## Status, disclaimers and the law

> [!IMPORTANT]
> This is an operations assistant, **not** a substitute for a Chartered Accountant, Company
> Secretary or lawyer. It encodes workflow and checks, not a frozen copy of the law, and routes to
> the official portal for every current rate, threshold and due date. Read [DISCLAIMER.md](DISCLAIMER.md).

> [!WARNING]
> **Content last reviewed: October 2026 — two transitions are under way, so verify specifics.** A
> new **Income-tax Act, 2025** is reported to replace the 1961 Act and **renumber sections**, so
> the TDS section numbers (192, 194C, 194J, …) may have changed — confirm on
> https://www.incometax.gov.in. India's **Labour Codes** are being brought into force and can
> change the statutory definition of *wages* (PF/ESI/gratuity) — confirm on
> https://www.epfindia.gov.in. Each reference file carries a `last_verified` date; CI flags any
> older than 90 days.

## Reviewed by

Looking for practising **CAs / CSs** to review these skills for accuracy and be credited here. If
that's you, open a [review issue](https://github.com/pras-ops/indian-business-ops-skills/issues/new)
or a PR. Spotted something out of date? Use the **Law or rate changed** issue template.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The most valuable contributions are keeping the official
links and dates current, adding state-specific notes, and adding real CA-grade eval questions.

## License

[MIT](LICENSE) — the instructions are free to use and adapt. The law they point to is published by
the Government of India.
