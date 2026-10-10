# documentary-agent-kit

One sentence → a publishable YouTube documentary.
`build a documentary on ahyeon` → a 29-minute, 1080p, fact-checked, license-clean video.

An agent-native video production studio: **AGENTS.md** orchestrator contract + **Agent Skills** per stage + a deterministic S0→S8 pipeline that runs locally *or* on GitHub Actions.

![status](https://img.shields.io/badge/pipeline-S0%E2%86%92S8-blue) ![license](https://img.shields.io/badge/license-MIT-green)

## Stage pipeline

| Stage | Skill | Input → Output artifact |
|---|---|---|
| S0 | intent | sentence → `00_brief.json` |
| S1 | research-facts | brief → `02_facts.md` (or reuse a provided dossier) |
| S2 | write-script | facts → `03_script.json` |
| S3 | source-media | script → `04_media_manifest.json` (license ledger) |
| S4 | gen-voiceover | script → `05_voice/*.mp3` + `timing.json` |
| S5 | assemble-timeline | media+voice → `06_timeline.json` |
| S6 | captions-meta | timeline → `captions.ass` + `thumbnail.png` + `07_metadata.json` |
| S7 | render-qc | timeline+captions → `final.mp4` + `08_qc_report.json` |
| S8 | publish | final+metadata → `09_publish.json` |

Hard rules (enforced by `AGENTS.md`): facts gate (narration may only use VERIFIED dossier facts), license gate (every timeline asset must have a recorded license), per-stage artifacts as resumable contracts, segment render + `-c copy` concat.

## Quickstart (local)

```bash
ffmpeg -version   # required
pip install -r requirements.txt
python scripts/run_stage.py all production/ahyeon     # full pipeline
python scripts/run_stage.py s4-voice production/ahyeon  # or any single stage
```

## Run on GitHub Actions

`Actions → pipeline → Run workflow` — pick a stage (`s3-media`, `s4-voice`, `s7-render`), set `publish_release: true` on `s7-render` to attach `final.mp4` to a GitHub release automatically.

Secrets (repo → Settings → Secrets → Actions):
- `NIM_API_KEY` — optional NVIDIA NIM key for script QC / metadata generation.
- No keys are required for the default footage-first pipeline (edge-tts is free, Commons/Mixkit/Incompetech are keyless).

## Production example: `production/ahyeon/`

**Jung Ahyeon (정아현) — Worth the Wait** — 29:00 documentary built from this kit:
facts dossier (`examples/ahyeon-dossier.md`) → 9-chapter script → 23 Wikimedia Commons photos (CC) + Mixkit B-roll + Incompetech score → edge-tts narration (word-timed) → motion-graphic cards + Ken Burns → ASS captions → loudnorm −14 LUFS → QC gate → release.

## Media licenses (default stack, monetization-safe)

| Source | License | Attribution |
|---|---|---|
| Wikimedia Commons photos | CC BY / CC BY-SA / CC0 / PD | per-file, in description credits |
| Mixkit B-roll | Mixkit License (free commercial) | not required |
| Incompetech music | CC BY 4.0 — Kevin MacLeod | required, in description credits |

## Layout

```
AGENTS.md            orchestrator contract (drop into any agent that reads AGENTS.md)
skills/              one Agent Skill per stage (SKILL.md format)
.claude/agents/      optional subagents (fact-researcher, media-scout)
scripts/             deterministic pipeline implementation (S0–S8)
production/<slug>/   episode artifacts (00–09 stage contracts)
examples/            ready-made fact dossiers (ahyeon)
docs/                blueprint + license matrix
.github/workflows/   ci.yml · pipeline.yml · publish.yml
```

## Security

Never commit `.env`, OAuth tokens or raw API keys. Uploads default to **unlisted**; a human flips to public. YouTube upload uses quota 1600 units per video (default 10k/day ≈ 6 uploads).

## License

MIT — see [LICENSE](LICENSE).
