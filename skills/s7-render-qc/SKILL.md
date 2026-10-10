---
name: s7-render-qc
description: Render the final 1080p video (segmented, resumable) and run the QC gate (duration, loudness -14 LUFS, black frames, sync). Use after S6.
---

# S7 — Render & QC

## Render (segmented + resumable)
1. Render each scene to `segments/<id>.mp4` (silent video): Ken Burns via zoompan, cards via fades, b-roll trimmed+graded. Parallelize across cores; only re-render scenes whose inputs changed.
2. Concat with `-c copy` → `S7_render/video_master.mp4`.
3. Audio: build voice track from block offsets; music bed (CC) ducked ~-13 dB under narration; mix → `loudnorm=I=-14:TP=-1.5:LRA=11`.
4. Final pass: burn `captions.ass`, mux audio → `S7_render/final.mp4` (H.264 high, yuv420p, AAC 192k, 25fps).

## QC gate (`08_qc_report.json`) — fail the run on
- duration outside brief ±3%
- loudness not -14 ±1 LUFS (measure with ebur128)
- blackdetect: intro/outro black segments only
- resolution/fps mismatch; audio channel mismatch
- caption sync spot-check failure at 3 beats
- fact-vs-dossier diff not clean; license ledger incomplete
- freezedetect: no frozen frames > 4s (except intentional holds)

Deliver `final.mp4` only if every check passes; else emit the failing report and stop.
