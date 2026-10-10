#!/usr/bin/env python3
"""Stage dispatcher: python scripts/run_stage.py <stage> <episode_dir>

Stages: s0-intent s1-facts s2-script s3-media s4-voice s5-timeline
        s6-captions s7-render s8-publish | all
Each stage script lives in scripts/ and exposes run(episode_dir) -> artifact path(s).
Stages are resumable: a stage whose output artifact already exists is skipped.
"""
import importlib
import os
import sys

ORDER = [
    ("s0-intent", "s0_intent", "00_brief.json"),
    ("s1-facts", "s1_facts", "02_facts.md"),
    ("s2-script", "s2_script", "03_script.json"),
    ("s3-media", "s3_media", "04_media_manifest.json"),
    ("s4-voice", "s4_voice", "05_voice/timing.json"),
    ("s5-timeline", "s5_timeline", "06_timeline.json"),
    ("s6-captions", "s6_captions", "07_metadata.json"),
    ("s7-render", "s7_render", "S7_render/final.mp4"),
    ("s8-publish", "s8_publish", "09_publish.json"),
]


def main():
    stage, ep = sys.argv[1], sys.argv[2]
    wanted = [s for s in ORDER if s[0] == stage or stage == "all"]
    if not wanted:
        print(f"unknown stage {stage}; choose from {[s[0] for s in ORDER]} or 'all'")
        sys.exit(2)
    for sid, mod, artifact in wanted:
        out = os.path.join(ep, artifact)
        if os.path.exists(out) and stage != "all":
            print(f"[{sid}] artifact exists, rerunning anyway (explicit stage)")
        elif os.path.exists(out):
            print(f"[{sid}] artifact exists — skip (resumable)")
            continue
        try:
            m = importlib.import_module(mod)
        except ModuleNotFoundError:
            print(f"[{sid}] module scripts/{mod}.py not present — skipping")
            continue
        print(f"[{sid}] running...")
        m.run(ep)
    print("done")


if __name__ == "__main__":
    main()
