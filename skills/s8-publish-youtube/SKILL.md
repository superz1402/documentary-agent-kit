---
name: s8-publish-youtube
description: Publish the finished episode - GitHub release (permanent) and/or YouTube upload (unlisted by default), plus 09_publish.json record. Use after S7 QC passes.
---

# S8 — Publish

## Targets
1. **GitHub Release** (default, permanent): `gh release create <tag> final.mp4` + attach `captions.ass`, `thumbnail.png`, `07_metadata.json`. Files >2GB must be split or re-encoded to ≤2GB.
2. **YouTube Data API v3** (optional): resumable `videos.insert` with `07_metadata.json`, `thumbnail.set`, `privacy_status=unlisted` (human flips public). Quota: 1600 units/upload, 10k/day ≈ 6 uploads.
3. **Free file mirrors** (optional): storage.to REST API (`POST /upload/init` → presigned `PUT` → `POST /upload/confirm`; anonymous files expire in 3 days — mirrors only).

## Output
`09_publish.json`:
```json
{"targets":[{"type":"github-release","url":"...","tag":"..."},
            {"type":"storage.to","url":"...","expires":"..."}],
 "metadata_used":"07_metadata.json","sha256":"<final.mp4 digest>"}
```

## Guardrails
- Never publish a video whose `08_qc_report.json` has failing checks.
- Never publish metadata without the credits appendix.
- Log every URL + file hash into `09_publish.json` (provenance).
