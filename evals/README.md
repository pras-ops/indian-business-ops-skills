# Evaluations

Two kinds of check, because the pack has two kinds of claim.

## 1. Deterministic (computational) — run automatically

The parts with an objectively correct answer — GSTIN validation, PAN decode, CGST/SGST/IGST
split — are graded by [`run_deterministic.py`](run_deterministic.py) against the bundled helper
scripts. It's cheap, runs in CI, and gives a hard number:

```bash
python evals/run_deterministic.py
```

Current result: **17 / 17 (100%)** on the computational items in [`evals.json`](evals.json).
These double as regression fixtures — a change that breaks GSTIN checks or tax splits fails here.

## 2. Judgement questions — the with-skill vs without-skill benchmark

The other items in `evals.json` (`graded_by: "llm"`) are judgement questions: picking the right
TDS section, deciding CGST/SGST vs IGST, e-invoice applicability, composition-scheme documents,
and so on. For these the useful measure is **does Claude answer better with these skills than
without them** — the "accuracy went from X% to Y%" comparison.

That benchmark is **not run in CI** because it is expensive: each question is asked to Claude twice
(with the skills loaded, and without), and the answers are graded. To run it yourself:

1. Load the skills in Claude Code (`cp -r skills/* ~/.claude/skills/` or install the plugin).
2. Ask each `graded_by: "llm"` prompt with the skills available; record the answer.
3. Repeat in a session with the skills removed (the baseline).
4. Grade each answer against its `expected` note (a CA's review is the gold standard here).
5. Report both pass rates and the delta.

> The `expected` notes describe the *shape* of a correct answer, not a filing figure. Because rates
> and thresholds change, a model that correctly says "confirm the current rate on the portal" is
> answering well — the benchmark rewards correct process and routing, not a memorised number.

Contributions of more real questions (especially ones a practising CA would pose) are welcome —
see the repo's CONTRIBUTING.md.
