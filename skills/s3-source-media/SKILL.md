---
name: s3-source-media
description: Source license-clean media (04_media_manifest.json) - Commons photos, Mixkit B-roll, music; every asset with a recorded license. Use after S2.
---

# S3 — Source Media

Produce `production/<slug>/04_media_manifest.json`:

```json
{"assets":[{"id":"ph01","kind":"photo","file":"...","source":"wikimedia-commons",
            "license":"CC BY-SA 4.0","artist":"...","source_url":"...","credit":"..."}]}
```

## Keyless-safe sources (default stack)
| Source | What | License |
|---|---|---|
| Wikimedia Commons API | subject photos, archival | CC BY / CC BY-SA / CC0 / PD — per-file credit required |
| Mixkit | B-roll (concert/stage/crowd/city/neon) | Mixkit License, free commercial, no credit |
| Incompetech | score | CC BY 4.0 — Kevin MacLeod, credit required |
| Pexels/Pixabay (optional keys) | extra B-roll | free commercial |

## Steps
1. Search per script chapter (keywords from S1 beat outline).
2. Download best resolution; probe with ffprobe/PIL; reject corrupt/small assets.
3. Record license + artist + source URL for EVERY asset. No license string → asset cannot enter the timeline (license gate).
4. Strip embedded audio from all downloaded video assets (`-an` or replace in S7 mix).
5. Subject footage (K-pop MVs etc.): short fair-use clips only (3-6s, narration over, original audio stripped, graded). If unavailable, photo+motion substitution.

## Failure modes
- YouTube yt-dlp bot-walls datacenter IPs → fall back to photos + motion graphics (deterministic, license-clean).
- Rate limits: Commons via curl with descriptive UA; respect 429s with backoff.
