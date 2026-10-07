# Architecture and design doctrine

This repo is one layer of a larger pattern for "AI that helps run an Indian business." Knowing
which layer it is — and which it deliberately isn't — keeps it useful and honest.

## The four layers

```
┌──────────────────────────────────────────────┐
│  1. AI agent        Claude / other LLM agent  │   decides WHAT to do, explains, prioritises
└───────────────────────┬──────────────────────┘
                        │
┌───────────────────────▼──────────────────────┐
│  2. Skills / RAG    ◀── THIS REPO             │   domain workflow, checks, where to look
│     GST · TDS · payroll · ROC · …             │
└───────────────────────┬──────────────────────┘
                        │
┌───────────────────────▼──────────────────────┐
│  3. Deterministic engines  ◀── THIS REPO too  │   exact math, validation, reconciliation
│     gst_calc.py · pan.py · …                  │
└───────────────────────┬──────────────────────┘
                        │
┌───────────────────────▼──────────────────────┐
│  4. Action layer    MCP servers / portal APIs │   read books, file returns, move money
│     Tally · GST portal · banking · MCA        │
└──────────────────────────────────────────────┘
```

This repo owns **layers 2 and 3**: the skills that carry the workflow, and the small deterministic
helpers they call for anything that must be exact. It does **not** own layer 4 — it never files a
return, moves money, or logs into a portal. That line is intentional; see "What this repo is not".

## The one rule that matters

> **The language model decides what to do. Code decides the numbers.**

An LLM is excellent at "which section applies, what order to do things in, what to check." It is a
poor calculator and a worse source of a current tax rate. So:

- Exact work — a GSTIN check digit, a CGST/SGST split, a PAN's entity type — goes to a **script**
  (`skills/*/scripts/*.py`), tested in [`tests/`](tests). The skills tell the agent to call it.
- Volatile law — rates, slabs, thresholds, due dates — is **never hardcoded as fact**. A rate is
  supplied to the calculator by the agent after confirming it on the official portal. The skills
  and dated reference files route to CBIC, incometax.gov.in, MCA, EPFO, ESIC and so on.
- Judgement and explanation stay with the model and the skill prose.

This is the same split the stronger projects in this space settled on, and it's what makes the
output trustworthy: the parts that can be wrong in a damaging way are the parts handled by code and
by a trip to the source of truth, not by a guess.

## What this repo is not

- **Not an action layer.** It prepares and checks; a human (or a separate, clearly-scoped MCP/API
  integration) files. If you add an action layer, keep it a distinct component with its own
  authorisation and audit trail — don't fold "file it" into a skill.
- **Not professional advice.** See [DISCLAIMER.md](DISCLAIMER.md). It assists a user and their CA/CS;
  it does not replace them.
- **Not a frozen copy of the law.** It is built to send the agent to the current source, because the
  law moves faster than any file.

## Where it could grow

Natural extensions that stay on the right side of the design rule:

- More deterministic helpers (interest/late-fee day-count that takes the rate as input; an
  invoice-numbering gap checker; a 2B-vs-purchase-register reconciler).
- A thin, clearly-scoped **action layer** (e.g. an MCP server) as a *separate* component that these
  skills can drive — not merged into them.
- Per-state reference notes (Professional Tax, Shops & Establishments) under each skill's
  `references/`.
