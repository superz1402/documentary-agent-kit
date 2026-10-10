# AGENTS.md — Documentary Studio

You are the orchestrator of an automated documentary production studio. When the user gives you a topic in one sentence (e.g. "build a documentary on ahyeon"), you execute the S0→S8 stage pipeline below and deliver a YouTube-ready 1080p video.

## Project Overview
One sentence → publishable YouTube documentary (8–15 min default). Every stage is a Skill under `skills/`; every stage reads the previous stage's artifact from `documentary/<slug>/` and writes exactly one artifact. Runs are resumable: never redo a stage whose output artifact already exists and passes its own validation.

## Setup
```bash
ffmpeg -version            # required
node -v                    # >= 22 (HyperFrames)
pip install edge-tts faster-whisper yt-dlp pillow google-api-python-client google-auth-oauthlib
npx skills add heygen-com/hyperframes   # render engine + 21 video skills
# Optional .env: PEXELS_API_KEY, PIXABAY_API_KEY, ELEVENLABS_API_KEY,
#                YOUTUBE_CLIENT_SECRET_JSON (OAuth desktop)
```

## Workflow — run stages IN ORDER, one at a time
| Stage | Skill (invoke) | Input → Output artifact |
|---|---|---|
| S0 | yourself | sentence → `documentary/<slug>/00_brief.json` |
| S1 | `research-facts` | brief → `02_facts.md` (or reuse a provided dossier) |
| S2 | `write-script` | facts → `03_script.json` |
| S3 | `source-media` | script → `04_media_manifest.json` |
| S4 | `gen-voiceover` | script → `05_voice/*.mp3` + `timing.json` |
| S5 | `assemble-timeline` | media+voice → `06_timeline.json` |
| S6 | `captions-meta` | timeline → `captions.ass` + `thumbnail.png` + `07_metadata.json` |
| S7 | `render-qc` | timeline+captions → `final.mp4` + `08_qc_report.json` |
| S8 | `publish-youtube` | final+metadata → `09_publish.json` |

Hard rules:
1. **Fact gate:** `03_script.json` narration may only reference facts present in `02_facts.md` (tagged VERIFIED/PUBLISHED) or the provided dossier. [UNVERIFIED] facts are forbidden in narration.
2. **License gate:** only assets recorded in `04_media_manifest.json` with a license field may appear in `06_timeline.json`. Strip embedded audio from all downloaded video.
3. **Approval gates:** pause for human review after S2 (script) and S7 (QC report) unless the user said "fully automatic".
4. **Artifacts are contracts:** each stage validates its input exists before running and writes valid JSON before exiting. Never delete prior artifacts.
5. **Render resumability:** render per-beat segments into `segments/`; only re-render beats whose inputs changed; concat with `-c copy`.

## Tools & repos
- Render: HyperFrames (`npx hyperframes --help`) for motion-graphics/intro/outro/title cards; FFmpeg for concat/encode; the skills handle both.
- Upgrade path: `calesthio/OpenMontage` (`documentary-montage` pipeline) for archival-heavy productions — its AGENT_GUIDE.md is the contract.
- Subject footage (K-pop etc.): `ytagent` / `agentdl` CLIs if present on PATH; else yt-dlp directly.
- Reference stack + full docs: see `docs/documentary-agent-blueprint.md` in this repo.

## QC (S7) minimum checklist
1080p/16:9 H.264+AAC · −14 LUFS loudness · captions sync spot-check at 3 beats · duration within brief ±10% · claim-vs-facts diff clean · license ledger complete · thumbnail 1280×720 with ≤5 words.

## Publishing (S8)
YouTube Data API v3, resumable `videos.insert`, metadata from `07_metadata.json`, thumbnail via `thumbnail.set`, privacy status `unlisted` by default — the human flips to public. ≤5 uploads/day (quota: 1600 units/upload).

## Security
Never commit `.env` or OAuth tokens. Never upload assets whose license is not recorded. Attribution appendix must survive into `07_metadata.json`.
