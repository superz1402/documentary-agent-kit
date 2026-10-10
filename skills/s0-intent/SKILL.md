---
name: s0-intent
description: Turn a one-sentence request into 00_brief.json - the episode contract (subject, duration, style, gates). Use at the very start of every documentary episode.
---

# S0 — Intent

Turn "build a documentary on X" into a machine-checkable episode contract.

## Output
`production/<slug>/00_brief.json` with at minimum:

```json
{
  "slug": "...", "request": "...", "mode": "fully-automatic|human-gated",
  "deliverable": {"type": "youtube-documentary", "duration_target_s": 1740,
                   "resolution": "1920x1080", "fps": 25, "language": "en",
                   "loudness_lufs": -14},
  "subject": {"name": "...", "group": "...", "born": "..."},
  "title_working": "...", "throughline": "...",
  "style": {"palette": {}, "fonts": {}, "motif": "", "tone": ""},
  "gates": {"facts_gate": "...", "license_gate": "...", "human_approval": false}
}
```

## Steps
1. Parse the request: subject, angle, target length (default 8-15 min; longform 20-30 min only if the dossier supports it).
2. Pick a throughline — one sentence the whole edit serves. No throughline, no episode.
3. Fix style tokens (palette hex, display/body fonts, motif) so every later stage is visually consistent.
4. Record gates. If the user said "fully automatic", set human_approval=false and log it.

## Guardrails
- Duration target is a promise: every later stage enforces it (±3%).
- Never invent facts here; S0 is logistics only.
