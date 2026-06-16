#!/usr/bin/env python3
"""
Download all Adrenalyn XL WC2026 card images (1..630) from Central da Copa's
Firebase Storage. Clean, predictable URLs — one high-quality JPEG per card.

Run locally: python3 download_cards.py
Requires: pip install requests
"""
import time, requests
from pathlib import Path

OUT_DIR = Path(__file__).parent / "images" / "cards"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BASE = ("https://firebasestorage.googleapis.com/v0/b/"
        "centralcopa-prod.firebasestorage.app/o/"
        "public%2Fstickers%2FWC2026_ADRENALYNXL%2F")
MAX_CARD = 630

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "image/jpeg,image/*,*/*;q=0.8",
})

failed = []
for i in range(1, MAX_CARD + 1):
    num = str(i).zfill(3)
    out_file = OUT_DIR / f"{num}.jpeg"
    if out_file.exists() and out_file.stat().st_size > 1000:
        print(f"  skip #{num} (already downloaded)")
        continue
    url = f"{BASE}{i}.jpeg?alt=media"
    try:
        r = session.get(url, timeout=20)
        if r.status_code == 200 and r.headers.get("content-type", "").startswith("image") and len(r.content) > 1000:
            out_file.write_bytes(r.content)
            print(f"  OK #{num} ({len(r.content)//1024}KB)")
        else:
            print(f"  FAIL #{num} — HTTP {r.status_code}, {len(r.content)}B")
            failed.append(i)
    except Exception as e:
        print(f"  FAIL #{num} — {e}")
        failed.append(i)
    time.sleep(0.1)

on_disk = sorted(int(f.stem) for f in OUT_DIR.glob("*.jpeg"))
print(f"\nDone. On disk: {len(on_disk)}/{MAX_CARD}")
if failed:
    print(f"Failed: {failed}")
