---
name: s6-captions-meta
description: Generate burned captions (captions.ass), thumbnail (1280x720), and YouTube metadata (07_metadata.json) with credits. Use after S5.
---

# S6 — Captions, Thumbnail, Metadata

## Captions (`captions.ass`)
1. Group word timings (S4) into cues of 3-5 words / max 2.0s.
2. Style: Inter SemiBold ~52px, white #F2F2F2, thin black outline + soft shadow, bottom-centered, safe margins.
3. Spot-check sync at 3 points (cold open, mid, outro) against word timestamps.

## Thumbnail (`thumbnail.png`, 1280x720)
- ≤5 words. Subject photo (highest-res, licensed) + brand palette + motif. Test legibility at 200px wide.

## Metadata (`07_metadata.json`)
- `title` ≤100 chars, hook-first, no clickbait lies.
- `description`: hook paragraph → chapter list (00:00 format, first at 0:00) → **credits appendix** (every CC asset + artist + license; music credits) → sources.
- `tags`, `category` (22 People & Blogs or 27 Education), `privacy_status` default `unlisted`.
- Chapters must match `06_timeline.json` chapter starts exactly.

## Guardrails
- The credits appendix is part of the license gate — it must survive into publishing.
- Title/description claims must pass the facts gate too.
