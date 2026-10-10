---
name: s1-research-facts
description: Build or reuse the fact dossier (02_facts.md) - the verified research layer every narration claim must come from. Use after S0 before scripting.
---

# S1 — Research & Facts

Produce `production/<slug>/02_facts.md`: a confidence-tagged dossier that is the ONLY source narration may cite.

## Inputs
- `00_brief.json`
- Optionally a pre-made dossier (e.g. `examples/ahyeon-dossier.md`) — reuse instead of re-researching when it exists and passes review.

## Steps
1. Collect candidate facts from primary + reputable secondary sources (official press, Wikipedia with citations, major outlets). Web search agents may fan out here (see `.claude/agents/fact-researcher.md`).
2. Tag every fact: `[WIKI]`, `[NEWS]`, `[OFFICIAL]`, `[FANSITE]`, `[UNVERIFIED]`.
3. Build the verified timeline (dated rows, numbers exact). Documentary spine = timeline.
4. List `[UNVERIFIED]` items explicitly — they are FORBIDDEN in narration.
5. Attach a beat outline (cold open → chapters → outro) with per-beat archival search keywords.

## Guardrails
- Dates + numbers are receipts: write them exactly as sourced.
- Conflicting sources → keep the stronger tag, note the conflict.
- Facts gate (enforced in S2): narration may only reference facts present here.
