#!/usr/bin/env python3
"""
Download all 630 Adrenalyn XL WC2026 card images from Coleka.
Run this locally: python3 download_cards.py
Requires: pip install requests
"""
import os, time, sys, requests
from pathlib import Path

OUT_DIR = Path(__file__).parent / "images" / "cards"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BASE = "https://www.coleka.com/media/item"
SLUG = "adrenalyn-xl-fifa-world-cup-2026-carte-n-1"

# All known/likely upload date paths to try (most recent first)
DATE_PATHS = [
    "202603/18", "202603/19", "202603/17", "202603/20",
    "202603/21", "202603/22", "202603/25", "202603/26",
    "202603/27", "202603/28", "202604/01", "202604/02",
    "202603/24", "202603/23", "202603/15", "202603/16",
    "202603/14", "202603/10", "202603/11", "202603/12",
]

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Referer": "https://www.coleka.com/en/collection/adrenalyn-xl-fifa-world-cup-2026/",
    "sec-fetch-dest": "image",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-origin",
})

# Warm up session with a page visit first
print("Visiting Coleka to warm up session...")
try:
    session.get("https://www.coleka.com/en/collection/adrenalyn-xl-fifa-world-cup-2026/", timeout=15)
    time.sleep(1)
except Exception as e:
    print(f"Warning: warm-up failed ({e}), continuing anyway...")

failed = []

for i in range(1, 631):
    num = str(i).zfill(3)
    out_file = OUT_DIR / f"{num}.webp"

    if out_file.exists():
        print(f"  skip #{num} (already downloaded)")
        continue

    downloaded = False
    for date_path in DATE_PATHS:
        url = f"{BASE}/{date_path}/{SLUG}-{num}-001.webp"
        try:
            r = session.get(url, timeout=10)
            if r.status_code == 200 and len(r.content) > 500:
                out_file.write_bytes(r.content)
                print(f"  OK #{num} from {date_path}  ({len(r.content)//1024}KB)")
                downloaded = True
                break
        except Exception:
            continue
        time.sleep(0.05)

    if not downloaded:
        print(f"  FAIL #{num} — not found in any date path")
        failed.append(i)

    time.sleep(0.2)  # be polite

print(f"\nDone. Downloaded: {630 - len(failed)}/630")
if failed:
    print(f"Failed: {failed}")
    print("\nFor failed cards, try visiting Coleka manually and inspecting the image URL.")
