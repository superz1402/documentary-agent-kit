---
name: s4-gen-voiceover
description: Generate the narration voiceover (05_voice/*.mp3 + timing.json) with word-level timestamps via edge-tts. Use after S2 script is locked.
---

# S4 — Generate Voiceover

Produce `production/<slug>/05_voice/b###.mp3` + `05_voice/timing.json`.

## Steps
1. For each script block, synthesize with edge-tts:
   - `en-US-AndrewNeural` — calm-authoritative male (Cold Fusion register), default rate -4% for longform.
   - Stream `WordBoundary` events → word-level offsets; store in `timing.json`:
     `{"blocks":[{"id":"b001","file":"b001.mp3","duration_s":24.3,"words":[{"w":"...", "t0":0.12,"t1":0.44}]}]}`
2. Retry (3x, backoff) per block; a failed block must fail loudly, not silently truncate.
3. Normalize nothing yet — loudness pass happens in S7 over the final mix.
4. Duration check: sum(durations) vs script plan; if drift > 5%, return to S2 for extension/trim (duration enforcer).

## Fallbacks
- edge-tts network blocked → `piper-tts` offline (approximate word timing from characters-per-second).
- Premium: ElevenLabs `eleven_multilingual_v2` (~$0.10/1k chars) for hero narration.

## Guardrails
- One voice for the whole episode. No per-chapter voice changes.
- Keep MP3 48kHz mono — stereo mix-up happens in S7.
