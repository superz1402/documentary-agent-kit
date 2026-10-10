#!/usr/bin/env python3
"""CI artifact validator: every stage artifact present must be valid per its contract."""
import glob
import json
import os
import sys

FAILS = []


def check_json(path, required=()):
    try:
        d = json.load(open(path))
    except Exception as e:  # noqa: BLE001
        FAILS.append(f"{path}: invalid JSON ({e})")
        return None
    for k in required:
        if k not in d:
            FAILS.append(f"{path}: missing key '{k}'")
    return d


def main():
    eps = sorted(glob.glob("production/*/"))
    if not eps:
        print("no episodes found — nothing to validate")
        return
    for ep in eps:
        slug = os.path.basename(ep.rstrip("/"))
        print(f"== {slug} ==")
        brief = check_json(ep + "00_brief.json", ("slug", "request"))
        script = check_json(ep + "03_script.json", ("blocks",))
        if script and isinstance(script.get("blocks"), list):
            n = len(script["blocks"])
            words = sum(len(b.get("text", "").split()) for b in script["blocks"])
            print(f"   script: {n} blocks, {words} words")
        check_json(ep + "04_media_manifest.json", ("assets",))
        check_json(ep + "05_voice/timing.json", ("blocks",))
        check_json(ep + "06_timeline.json", ("scenes",))
        check_json(ep + "07_metadata.json", ("title", "description"))
        check_json(ep + "08_qc_report.json", ("checks",))
        check_json(ep + "09_publish.json", ("targets",))
        # captions + thumbnail existence when claimed
        if os.path.exists(ep + "07_metadata.json"):
            for f in ("captions.ass", "thumbnail.png"):
                p = ep + f
                if os.path.exists(p) and os.path.getsize(p) < 500:
                    FAILS.append(f"{p}: suspiciously small")
    if FAILS:
        print("\nFAILURES:")
        for f in FAILS:
            print("  -", f)
        sys.exit(1)
    print("\nALL ARTIFACTS VALID")


if __name__ == "__main__":
    main()
