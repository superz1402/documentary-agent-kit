# One-Sentence Documentary Factory — Master Blueprint
### "Say 'build a documentary on Ahyeon' → get a YouTube-ready video"

Companion files: `github-repos-catalog.md` (all repos) · `ahyeon-documentary-dossier.md` (verified fact pack) · `documentary-agent-kit/` (ready-to-install AGENTS.md + skills)

---

## 1. Executive Summary

You are ~70% of the way there already — you just own the pieces under four different accounts. Your `ai-documentary-studio` (Bilal140202) is a complete 17-agent/14-stage production system that ends at an MP4; `babymonster-documentary-pipeline` (Ansaribilal14) has a proven 47-scene script + narration for this exact subject but is blocked on footage download and final render; `ytagent` (Bilal140202) solves that footage block; `vfactory` (Superz1402) and `youtube-automation-engine` (Hamza140202) prove the topic→video and serverless patterns. What's missing is: (a) a **fact layer** (verified dossier — delivered in `ahyeon-documentary-dossier.md`), (b) a **publish stage** (SEO metadata, thumbnail, YouTube upload), (c) a **single orchestrator contract** (AGENTS.md + skills) that fuses everything, and (d) optionally the strongest open-source production system as an upgrade path: **OpenMontage (65.7k★)** — the only repo covering research→render end-to-end with a real-footage `documentary-montage` pipeline.

**Recommended stack (primary path):**

| Layer | Tool | Why |
|---|---|---|
| Orchestrator | Your coding agent (Claude Code) + the `documentary-agent-kit/` in this folder | AGENTS.md + SKILL.md convention; artifacts on disk; resumable |
| Production system (upgrade) | `calesthio/OpenMontage` — `documentary-montage` pipeline | research→compose w/ quality gates, CLIP footage retrieval, zero-key free tier |
| Render engine | `heygen-com/hyperframes` (+ Remotion via OpenMontage) | deterministic HTML→MP4, 21 agent skills, the engine brag uses |
| Footage (archival) | Pexels · Pixabay · Wikimedia Commons · Internet Archive · NASA (all free APIs) | license-safe b-roll; OpenMontage indexes them via CLIP |
| Footage (K-pop subject) | your `ytagent` + `character-clip-extractor` | only reliable path to stage cuts; pair with fair-use edit distances |
| Voiceover | edge-tts (free, word timestamps) → ElevenLabs (~$1/doc premium) → kokoro (offline fallback) | hi/ko/en coverage; SRT timestamps for free |
| Captions | faster-whisper / whisperX → ASS karaoke burn-in via FFmpeg | word-level sync |
| Music | Pixabay Music / YouTube Audio Library | ⚠ NOT MusicGen (weights are CC-BY-NC — unmonetizable) |
| Publish | YouTube Data API v3 `videos.insert` (resumable) + thumbnail.set | ~6 uploads/day quota; unlisted→public flip |

**Fallback (fastest turnkey):** `harry0703/MoneyPrinterTurbo` (129k★, MIT) — topic→script→footage→VO→subtitles→render→publish in one app — accepting its montage style is "AI shorts", not authored documentary. Use it as your upload-layer reference and for quick one-off videos.

---

## 2. Reference Architecture — 9 Stages (S0–S8)

Each stage is a **Skill** that reads the previous stage's artifact and writes its own. Everything lands in `documentary/<slug>/` so any stage is re-runnable and auditable.

```text
USER SENTENCE: "build a documentary on ahyeon"
        │
        ▼
S0 INTENT          00_brief.json         (subject, angle, length 8–15min, language,
        │                                    chapter seed, style targets)
        ▼
S1 RESEARCH        02_facts.md           (Wikipedia/Wikidata REST + web search;
        │                                    every fact = source URL + confidence tag)
        ▼
S2 SCRIPT          03_script.json        (hook 0–30s, 3–6 acts, narration beats,
        │                                    on-screen text, per-beat visual keywords)
        ▼
S3 MEDIA           04_media_manifest.json (per asset: URL, license, attribution,
        │                                    local path) — Pexels/Pixabay/Commons/
        │                                    IA/NASA + ytagent for subject footage
        ▼
S4 VOICEOVER       05_voice/*.mp3 + timing.json  (edge-tts default — emits SRT;
        │                                    ElevenLabs premium; kokoro offline;
        │                                    faster-whisper word timestamps)
        ▼
S5 ASSEMBLY        06_timeline.json      (EDL: beat starts = voice durations,
        │                                    Ken-Burns on stills, music bed −18 LUFS
        │                                    ducked −6 dB under VO)
        ▼
S6 CAPTIONS+META   07_metadata.json + captions.ass + thumbnail.png
        │                                    (chapters start 00:00; title ≤100 chars;
        │                                    attribution appendix; thumbnail 1280×720)
        ▼
S7 RENDER+QC       08_qc_report.json     (per-beat segments → concat; 1080p H.264;
        │                                    −14 LUFS; ffprobe checks; claim-vs-facts
        │                                    diff before render)
        ▼
S8 PUBLISH         09_publish.json       (resumable videos.insert, thumbnail.set,
                                             unlisted by default → you flip public)
```

**Why stages-as-files:** a 15-minute documentary means a 15–45 minute render and dozens of API calls. With artifact-per-stage, a failed render costs you one stage, not the run; you can hand-edit `03_script.json` and re-run from S4; and the JSON checkpoints mirror what OpenMontage does internally (resumable + decision audit trail).

---

## 3. Tool Matrix (verified costs & auth)

| Tool | Stage | Cost | Auth | Notes |
|---|---|---|---|---|
| Pexels API | S3 | Free, monetization-safe, no attribution | API key | 200 req/hr, 20k/mo |
| Pixabay API (+music) | S3 | Free | API key | 100 req/60s |
| Unsplash API | S3 | Free demo tier | token | 50 req/hr, attribution required |
| Wikimedia Commons | S3 | Free | none | parse `extmetadata` for license |
| Internet Archive | S3 | Free | none | prelinger/newsreels; add retries (flaky) |
| NASA images API | S3 | Free | none | public-domain space footage |
| Openverse API | S3 | Free | none | ~20 req/min anonymous; CC search across Flickr/FMA |
| Freesound | S3 SFX | Free | token | 60 req/min; CC-BY needs credit |
| edge-tts | S4 | Free | none | 400+ voices/90+ languages (incl. hi-IN, ko-KR); emits MP3+SRT |
| Kokoro (kokoro-onnx) | S4 | Free, Apache-2.0 | none | 82M local, CPU-realtime, per-token timing |
| ElevenLabs v2/v2.5 | S4 | ~$0.10/1k chars ≈ $0.40–0.90 per 10-min doc | API key | best quality; Hindi + Korean supported |
| OpenAI TTS | S4 | ~$0.015/min | API key | no word timestamps |
| faster-whisper / whisperX | S4/S6 | Free, local | none | `word_timestamps=True` |
| ASS + libass (FFmpeg) | S6 | Free | — | karaoke `\k` tags → `ffmpeg -vf ass=` |
| HyperFrames | S5/S7 | Free, Apache-2.0 | none | Node 22+ & FFmpeg; deterministic frames |
| Remotion | S5/S7 | Free individuals/small co. | none | OpenMontage default engine |
| YouTube Data API v3 | S8 | Free | OAuth desktop | 1600 units/upload vs 10k/day ≈ 6 uploads/day; `resumable=True`; thumbnail.set needs verified account |

---

## 4. The conventions you asked about (AGENTS.md & Skills)

**AGENTS.md** (agents.md — used by Codex, Cursor, Jules, Aider, goose, opencode, Zed, Warp, Devin, Copilot coding agent, Gemini CLI; Claude Code reads it via CLAUDE.md/symlink) is "a README for agents": a single root Markdown file, no required schema. What matters to agents: project overview, setup commands, the stage workflow contract ("run one stage at a time, write artifacts, exit"), tools/skills catalog, QC instructions, security notes (keys in `.env`, upload quota), output contracts. Nested `AGENTS.md` per subfolder wins over the root file. A ready-to-drop one is in `documentary-agent-kit/AGENTS.md`.

**Agent Skills** (agentskills.io spec, mirrored in anthropics/skills) = a folder with `SKILL.md` carrying YAML frontmatter (`name`, `description`) + optional `scripts/`, `references/`, `assets/`. Agents load only name+description at startup and read the body on match (progressive disclosure). Install/share via `npx skills add owner/repo`; ecosystem lists: ComposioHQ/awesome-claude-skills, VoltAgent/awesome-agent-skills (1000+). brag and HyperFrames (21 skills) are the best-in-class examples of this packaging.

**Subagents** (`.claude/agents/*.md`, frontmatter `name/description/tools/model`) run in their own context with restricted tools — ideal for token-heavy stages (media search fan-out). Two ready ones ship in the kit: `fact-researcher`, `media-scout`. CrewAI/LangGraph are unnecessary here: a linear 9-stage flow with checkpoint files is simplest as orchestrator+skills (LangGraph only if you later need durable graphs/retries).

---

## 5. Gap analysis — your repos vs. the goal

| Capability | ai-documentary-studio | babymonster-doc-pipeline | OpenMontage | Kit (this folder) |
|---|---|---|---|---|
| Research + fact-check | ✅ Truth Agent (≥2 sources, veto) | ✅ sourcing guide | ✅ 15–25 web searches/stage | ✅ research-facts skill + dossier |
| Script/storyboard | ✅ 3–5 acts | ✅ 47 scenes proven | ✅ per-genre directors | ✅ write-script skill |
| Footage acquisition | ✅ yt-dlp + stock | ⚠ blocked (IP) — **ytagent unblocks** | ✅ CLIP retrieval over free archives | ✅ source-media skill |
| Voiceover + timing | ✅ TTS w/ alignment | ✅ 47 edge-tts MP3s done | ✅ 10+ providers | ✅ gen-voiceover skill |
| Edit/assembly + captions | ✅ EDL + HyperFrames + SRT | ⚠ render pending | ✅ + self-review | ✅ assemble-timeline + captions-meta |
| Thumbnail + SEO metadata | ❌ | ❌ | ⚠ partial | ✅ captions-meta skill |
| YouTube upload | ❌ ends at MP4 | ❌ | ❌ | ✅ publish-youtube skill |
| One-sentence trigger | ❌ scripted per topic | ❌ | ⚠ pipeline manifest per run | ✅ AGENTS.md orchestrator |

**Fastest route:** run the kit on your existing repos (kit skills wrap `ai-documentary-studio` stages; `source-media` calls `ytagent`; reuse the 47-scene script for the group doc) → then adopt OpenMontage's `documentary-montage` as the long-form upgrade when you want archival-heavy real-footage docs.

---

## 6. Risks & mitigations (memorize these)

- **Copyright / Content ID** — K-pop MV clips WILL get claimed. Mitigation: record license per asset in `04_media_manifest.json`; strip embedded audio from archival video; prefer short, transformative clips with narration over them; keep an attribution appendix; swap flagged assets and re-render.
- **YouTube "inauthentic content" monetization policy (Jul 2025)** — templated, mass-produced AI narration is ineligible; AI narration alone is fine, sameness is not. Mitigation: original angle per episode (S0 angle param), unique archival sourcing, varied act structures, human review gates at S2 and S7.
- **TTS reliability** — edge-tts is an unofficial protocol (can throttle). Mitigation: kokoro offline fallback; ElevenLabs one-flag upgrade; pronunciation lexicon for proper nouns (e.g., Korean names) in script JSON.
- **Render failures** — 15-min 1080p two-pass encode can take 15–45 min and die mid-way. Mitigation: per-beat segment renders → concat (`-c copy`), EDL so only changed beats re-render, NVENC/QSV when present.
- **API limits** — Pexels 200/hr, Pixabay 100/60s, Openverse 200/day, archive.org flaky. Mitigation: cache all downloads to `assets/` with a local index; exponential backoff; fan out media search across subagents; idempotent stages.
- **Upload quota** — 1600 units/upload vs 10,000/day ≈ 6 uploads/day; OAuth apps in testing mode cap at private/unlisted. Mitigation: upload unlisted → flip public manually; batch ≤5/day.
- **Hallucinated facts about real people** — defamation risk on K-pop docs. Mitigation: hard gate — script beats may only reference facts present in `02_facts.md`; S7 QC runs a claim-vs-facts diff before render. (The dossier already tags [UNVERIFIED] items.)
- **Music licensing** — MusicGen weights are CC-BY-NC (non-commercial). Mitigation: Pixabay Music / YouTube Audio Library only.

---

## 7. Your first run — exact steps

1. `mkdir -p ~/documentary-studio && cp -r documentary-agent-kit/* ~/documentary-studio/`
2. `cd ~/documentary-studio && ln -s AGENTS.md CLAUDE.md` (or just open in any agents.md-compatible tool)
3. Optional keys in `.env`: `PEXELS_API_KEY`, `PIXABAY_API_KEY`, `ELEVENLABS_API_KEY` (none required for a first draft), `YOUTUBE_OAUTH_CLIENT_SECRET_JSON`
4. Install engines once: `node -v` (22+), `ffmpeg`, `pip install edge-tts faster-whisper yt-dlp pillow`, `npx skills add heygen-com/hyperframes`
5. Say: **"build a documentary on ahyeon using examples/ahyeon-dossier.md"** — S0–S8 run with artifacts in `documentary/ahyeon/`; review `03_script.json` at the S2 gate and flip the uploaded video public.
6. Upgrade later: clone `calesthio/OpenMontage`, run its `documentary-montage` pipeline with your dossier as the research seed for archival-heavy productions.
