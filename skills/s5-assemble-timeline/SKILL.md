---
name: s5-assemble-timeline
description: Assemble the edit decision list (06_timeline.json) - every scene with exact start/duration/visual parameters, synced to voiceover timings. Use after S4.
---

# S5 — Assemble Timeline

Produce `production/<slug>/06_timeline.json` — the single source of truth for rendering.

## Steps
1. For each script block, compute `start_s` from cumulative voice durations + pad.
2. Assign visuals per block's direction, resolved against `04_media_manifest.json`:
   - `photo` → Ken Burns (zoom/pan direction, seed) — oversample to 2304x1296 for smooth motion.
   - `b-roll` → clip + in-point; trim; strip audio.
   - `card` → static motion-graphic (title/stat/quote/timeline) with fade or slide.
   - `breather` → music-only ambient scene (no narration) — these pads absorb duration drift.
3. Enforce total duration: adjust breather lengths so the timeline lands within ±3% of target.
4. License gate: every scene's asset must exist in the media manifest with a license field, else fail.

## Output shape
```json
{"fps":25,"resolution":[1920,1080],"duration_s":1740.0,
 "scenes":[{"id":"b001","start_s":0.0,"dur_s":24.9,"voice":"05_voice/b001.mp3",
             "visual":{"type":"photo","ref":"ph01","kb":{"zoom":1.18,"pan":"right"}}}]}
```
