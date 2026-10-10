---
name: s2-write-script
description: Write the narration script (03_script.json) from the fact dossier - scene blocks with visual directions, duration-enforced. Use after S1.
---

# S2 — Write Script

Produce `production/<slug>/03_script.json`:

```json
{"slug":"...","target_duration_s":1740,"words_total":3960,
 "blocks":[{"id":"b001","chapter":"cold-open","text":"...","words":38,
            "visual":{"type":"b-roll|photo|card|stat|quote|breather","ref":"...",
                       "hint":"slow push-in on stage lights"}}]}
```

## Steps
1. Map dossier beats to chapters; assign each a word budget (narration ≈ 150 wpm; add 8-12% music-only breathers).
2. Write block-by-block. Every block = one narration paragraph + one visual direction.
3. **Facts gate:** every claim must exist in `02_facts.md` with a non-UNVERIFIED tag. Numbers on screen must match the dossier digit-for-digit.
4. Cold open must earn the first 30 seconds: stakes + contradiction, no greetings, no "in this video".
5. Ban list: "little did she know", "in a world where", "but here's the thing", rhetorical-question stacking, "AI slop" cadence. Prefer concrete receipts (dates, numbers) over adjectives.
6. Duration enforcement: sum(words)/150*60 + breather seconds must land within ±3% of target. Extend underweight beats with substance, never filler.
7. End cold open with the title card line; end outro with the throughline callback.

## Approval gate
If `human_approval=true` in the brief: pause and show the script. Otherwise proceed.
