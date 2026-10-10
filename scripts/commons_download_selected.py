#!/usr/bin/env python3
"""Download a curated selection of Commons files (by exact title) + build manifest."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commons_search import download  # noqa: E402

SELECTED = [
    # hero + solo Ahyeon
    "File:Adidas Orchard Ignition Event X Babymonster - Ahyeon 30082026.jpg",
    "File:Ahyeon 20260905 Manila.jpg",
    "File:Ahyeon 20260905 Manila 2.jpg",
    "File:Ahyeon Summer Sonic 2026.jpg",
    "File:Signature of Ahyeon.png",
    # group / era shots
    "File:Babymonster at Incheon Airport.jpg",
    "File:Babymonster with Doosan Bear Players for Adidas.png",
    "File:Babymonster Seattle.jpg",
    "File:BABYMONSTER in Seattle.jpg",
    "File:Adidas Orchard Ignition Event X Babymonster - Asa 30082026.jpg",
    "File:Adidas Orchard Ignition Event X Babymonster - Chiquita 30082026.jpg",
    "File:Adidas Orchard Ignition Event X Babymonster - Pharita 30082026.jpg",
    "File:Adidas Orchard Ignition Event X Babymonster - Rora 30082026.jpg",
    "File:Adidas Orchard Ignition Event X Babymonster - Ruka 30082026.jpg",
    "File:Babymonster Sep'24.png",
    "File:BabyMonster at SBS Radio on 20240428.jpg",
    "File:BabyMonster Promoting drip on 2024112.png",
    "File:BabyMonster batter up era.jpg",
    "File:BabyMonster Logo (2023).jpg",
    "File:Babymonster Exhibition at The SameE Myeongdong.jpg",
    "File:BABYMONSTER ASA BANILA CO.png",
    # Seoul b-roll with name resonance
    "File:Seoul-metro-242-Ahyeon-station-sign-20181121-075034.jpg",
    "File:Seoul-metro-242-Ahyeon-station-platform-20181121-075130.jpg",
]

OUTDIR = "/home/z/my-project/production/media/commons"
RESEARCH = "/home/z/my-project/research"


def main():
    pool = {}
    for jf in ["commons_ahyeon.json", "commons_babymonster.json"]:
        p = os.path.join(RESEARCH, jf)
        if os.path.exists(p):
            for it in json.load(open(p)):
                pool[it["title"]] = it
    items = []
    missing = []
    for t in SELECTED:
        if t in pool:
            items.append(pool[t])
        else:
            missing.append(t)
    print(f"selected {len(items)}, missing {len(missing)}")
    for m in missing:
        print("  MISSING:", m)
    items = download(items, OUTDIR)
    ok = [it for it in items if it.get("file")]
    json.dump(ok, open(os.path.join(OUTDIR, "manifest.json"), "w"), ensure_ascii=False, indent=1)
    total = sum(os.path.getsize(it["file"]) for it in ok) / 1e6
    print(f"DOWNLOADED {len(ok)}/{len(SELECTED)} files, {total:.0f} MB -> {OUTDIR}")
    for it in ok:
        print(f"  ok [{it['license']}] {it['title']}")


if __name__ == "__main__":
    main()
