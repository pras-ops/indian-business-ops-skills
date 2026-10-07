# Contributing

Thanks for helping keep this accurate. Indian compliance moves fast, so the highest-value
contributions are usually small corrections, not big rewrites.

## Most useful contributions

1. **Fix a stale link or number.** If an official portal moved, or a reference's dated snapshot is
   now wrong, update it and move the snapshot date. Cite the official source in the PR.
2. **Add a state-specific note.** Professional Tax, Shops & Establishments registration and some
   labour rules differ by state. Short per-state notes in a skill's `references/` are welcome.
3. **Add a skill** for another recurring area (for example: Partnership/LLP deeds, MSME delayed-
   payment claims, import-export documentation, or state labour welfare funds).

## Ground rules

- **Don't hardcode volatile law as fact.** Rates, thresholds and due dates belong in a
  `references/` file, dated, with a line telling the agent to confirm the live value on the
  official portal. The `SKILL.md` body should teach the *process*, which changes far less often.
- **Cite official sources** (gst.gov.in, incometax.gov.in, mca.gov.in, etc.) — not blog posts.
- **No advice framing.** Skills help a user prepare and understand; they do not tell a user what
  their liability "is" or replace a CA/CS. Keep the disclaimer intact.
- **Keep each `SKILL.md` focused** (ideally under ~400 lines); push detail into `references/`.

## Skill format

Each skill is a folder with a `SKILL.md`. The frontmatter needs `name` and `description`:

```markdown
---
name: skill-name
description: What it does, and the Indian forms/terms that should make an agent reach for it.
---

# Title

...imperative workflow...
```

Open a PR against `main`. Thank you!
