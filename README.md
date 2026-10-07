# Indian Business Ops — Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Agent Skills](https://img.shields.io/badge/format-Agent%20Skills-6E56CF.svg)
![Jurisdiction: India](https://img.shields.io/badge/jurisdiction-India%20🇮🇳-FF9933.svg)

A pack of [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
that teach Claude (or any agent that reads the same `SKILL.md` format) how to help run the
statutory and bookkeeping side of a company in **India** — GST, TDS, payroll, ROC/MCA filings,
registrations, invoicing and Tally.

> [!IMPORTANT]
> These skills encode **workflow, structure and checks** — not a frozen copy of the law. Indian
> tax and company law change often (GST was overhauled in September 2025). Every skill routes the
> agent to the **official portal** for the current rate, threshold or due date rather than
> trusting a number baked into a file. This is an operations assistant, **not** a substitute for a
> Chartered Accountant, Company Secretary or lawyer. Read [DISCLAIMER.md](DISCLAIMER.md).

> [!WARNING]
> **Content last reviewed: October 2026 — two large transitions are under way, so verify before
> relying on any specifics.** A new **Income-tax Act, 2025** is reported to replace the Income-tax
> Act, 1961, which **renumbers sections** — so the section numbers used in the TDS skill (192,
> 194C, 194J, …) may no longer be current; confirm the present section on
> https://www.incometax.gov.in. India's **four Labour Codes** are being brought into force, which
> can change the statutory definition of *wages* and therefore **PF, ESI and gratuity** amounts;
> confirm on https://www.epfindia.gov.in and the relevant code. The skills are built to send the
> agent to these portals for the live position rather than to answer from the files.

---

## What's in the pack

| Skill | What it helps with |
|---|---|
| [`gst-compliance`](skills/gst-compliance) | GST returns (GSTR-1 / 3B / 9), the current slab structure, HSN/SAC classification, input tax credit |
| [`tds-compliance`](skills/tds-compliance) | Which TDS section applies, deposit timing, quarterly returns (24Q/26Q/27Q), Form 16/16A |
| [`payroll-statutory`](skills/payroll-statutory) | Salary structure, EPF, ESI, Professional Tax, gratuity, payslips, the monthly ECR |
| [`company-roc-compliance`](skills/company-roc-compliance) | MCA/ROC annual filings (AOC-4, MGT-7/7A), DIR-3 KYC, statutory registers and board meetings |
| [`business-registrations-licenses`](skills/business-registrations-licenses) | Picking an entity type and the registrations/licences it needs (PAN/TAN, GSTIN, Udyam, Shops & Establishments, IEC, FSSAI) |
| [`invoicing-einvoice-eway`](skills/invoicing-einvoice-eway) | A legally complete tax invoice, e-invoice (IRN/QR) applicability, and the e-way bill |
| [`tally-operations`](skills/tally-operations) | Moving data in and out of Tally (XML/Excel), voucher structure, and reconciling books to returns |

Each skill is a folder with a `SKILL.md` and, where the detail is large or volatile,
a `references/` directory the agent reads only when it needs it.

## Install

### One-click install (`.skill` download)

Pre-built, validated `.skill` packages are in [`dist/`](dist/). On **Claude.ai / Claude apps**,
download a `.skill` file and open it, or upload it under **Settings → Capabilities → Skills**
(where your workspace allows custom skills) — it installs in one step.

| Skill | Download |
|---|---|
| GST | [`dist/gst-compliance.skill`](dist/gst-compliance.skill) |
| TDS / TCS | [`dist/tds-compliance.skill`](dist/tds-compliance.skill) |
| Payroll & statutory | [`dist/payroll-statutory.skill`](dist/payroll-statutory.skill) |
| Company / ROC | [`dist/company-roc-compliance.skill`](dist/company-roc-compliance.skill) |
| Registrations & licences | [`dist/business-registrations-licenses.skill`](dist/business-registrations-licenses.skill) |
| Invoicing / e-invoice / e-way | [`dist/invoicing-einvoice-eway.skill`](dist/invoicing-einvoice-eway.skill) |
| Tally | [`dist/tally-operations.skill`](dist/tally-operations.skill) |

A `.skill` file is just a zip of the skill folder; rebuild them any time with
[`scripts/build-skills.sh`](scripts/build-skills.sh).

### From source (Claude Code)

Copy any skill folder into your skills directory:

```bash
# one skill, for your user account
cp -r skills/gst-compliance ~/.claude/skills/

# or the whole pack for a single project
cp -r skills/* .claude/skills/
```

The skill is picked up on the next run; the agent consults it when a task matches its
`description`.

**Claude.ai / Claude apps** — zip a skill folder and upload it under
**Settings → Capabilities → Skills** (if your workspace allows custom skills).

**Any other agent runtime** — the files are plain Markdown with a small YAML header
(`name`, `description`). Point your loader at the `SKILL.md` files; nothing here is
Claude-specific except the loading convention.

## How a skill is built

```
skills/<skill-name>/
├── SKILL.md            # YAML frontmatter (name, description) + the workflow
└── references/         # deeper, more volatile detail, read on demand
    └── *.md
```

The `description` in the frontmatter is what makes an agent reach for the skill, so it names the
Indian forms and terms a user would actually type ("GSTR-3B", "194J", "Udyam", "e-way bill").

## Scope and limits

- **Covers:** the recurring compliance a typical private limited company, LLP or proprietorship
  runs into. It is a map and a checklist, not filled-in forms.
- **Does not cover:** giving a binding legal opinion, computing someone's exact tax liability as
  advice, or anything state-specific beyond pointing at the right authority. Professional Tax,
  Shops & Establishments and labour rules differ by state — the skills say so and tell the agent
  to check the specific state.
- **Always verify** the live number on the official portal before filing. Links are in each
  skill's references.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The most useful contributions are keeping the official
links current and adding state-specific reference notes.

## License

[MIT](LICENSE) — the instructions are free to use and adapt. The law they point to is published
by the Government of India.
