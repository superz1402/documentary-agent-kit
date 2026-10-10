#!/usr/bin/env python3
"""Mixkit free-stock-video fetcher: scrape category pages, download best-res MP4s.

Mixkit License: free for commercial use, no attribution required.
Usage: python3 mixkit_fetch.py OUTDIR [category ...] [limit_per_cat]
Writes OUTDIR/manifest.json
"""
import json
import os
import re
import subprocess
import sys

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"
BASE = "https://mixkit.co/free-stock-video/{cat}/"
LICENSE = "Mixkit License - free for commercial use, no attribution required (https://mixkit.co/license/)"


def fetch(url, timeout=30):
    r = subprocess.run(["curl", "-sL", "--max-time", str(timeout), "-A", UA, url],
                       capture_output=True, text=True, timeout=timeout + 10)
    return r.stdout


def page_videos(cat):
    html = fetch(BASE.format(cat=cat))
    ids = {}
    for m in re.finditer(r"https://assets\.mixkit\.co/videos/(\d+)/\1-(\d+)\.mp4", html):
        vid, h = int(m.group(1)), int(m.group(2))
        ids.setdefault(vid, set()).add(h)
    out = []
    for vid, hs in ids.items():
        best = max(hs)
        out.append({"id": vid, "height": best,
                    "url": f"https://assets.mixkit.co/videos/{vid}/{vid}-{best}.mp4"})
    return out, len(html)


def download(items, outdir, limit):
    os.makedirs(outdir, exist_ok=True)
    manifest = []
    for it in items[:limit]:
        dest = os.path.join(outdir, f"mixkit_{it['id']}_{it['height']}.mp4")
        if not os.path.exists(dest):
            r = subprocess.run(["curl", "-sL", "--max-time", "120", "-A", UA,
                                "-o", dest, it["url"]], timeout=150)
            if r.returncode != 0 or not os.path.exists(dest) or os.path.getsize(dest) < 50000:
                if os.path.exists(dest):
                    os.remove(dest)
                it["error"] = "download_failed"
                continue
        it["file"] = dest
        it["size"] = os.path.getsize(dest)
        it["license"] = LICENSE
        manifest.append(it)
    return manifest


if __name__ == "__main__":
    outdir = sys.argv[1]
    args = [a for a in sys.argv[2:] if not a.isdigit()]
    limit = int(sys.argv[-1]) if sys.argv[-1].isdigit() else 4
    cats = args or ["concert", "stage", "crowd", "city-night", "neon", "dance", "microphone"]
    allm = []
    for cat in cats:
        vids, hsz = page_videos(cat)
        print(f"[{cat}] page {hsz//1024}KB, {len(vids)} unique videos")
        m = download(vids, outdir, limit)
        for x in m:
            x["category"] = cat
        allm += m
        print(f"  downloaded {len(m)}")
    mf = os.path.join(outdir, "manifest.json")
    existing = []
    if os.path.exists(mf):
        existing = json.load(open(mf))
    have = {e["id"] for e in existing}
    existing += [x for x in allm if x["id"] not in have]
    json.dump(existing, open(mf, "w"), indent=1)
    total = sum(x["size"] for x in existing) / 1e6
    print(f"MANIFEST {mf}: {len(existing)} clips, {total:.0f} MB total")
