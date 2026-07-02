#!/usr/bin/env python3
"""List available ElevenLabs voices without printing the API key."""

from __future__ import annotations

import argparse
import csv
import json
import os
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "materials" / "elevenlabs_voices_available.tsv"
API_URL = "https://api.elevenlabs.io/v2/voices"


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dotenv", default=str(ROOT / ".env"))
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    parser.add_argument("--limit", type=int, default=200)
    args = parser.parse_args()

    load_dotenv(Path(args.dotenv))
    api_key = os.environ.get("ELEVENLABS_API_KEY", "")
    headers = {}
    if api_key:
        headers["xi-api-key"] = api_key
    req = urllib.request.Request(API_URL, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))

    voices = payload.get("voices", [])[: args.limit]
    rows = []
    for voice in voices:
        labels = voice.get("labels") or {}
        settings = voice.get("settings") or {}
        rows.append(
            {
                "voice_id": str(voice.get("voice_id", "")),
                "name": str(voice.get("name", "")),
                "category": str(voice.get("category", "")),
                "description": str(voice.get("description", "")).replace("\n", " "),
                "accent": str(labels.get("accent", "")),
                "gender": str(labels.get("gender", "")),
                "age": str(labels.get("age", "")),
                "use_case": str(labels.get("use case", labels.get("use_case", ""))),
                "preview_url": str(voice.get("preview_url", "")),
                "stability": str(settings.get("stability", "")),
                "similarity_boost": str(settings.get("similarity_boost", "")),
                "style": str(settings.get("style", "")),
                "speed": str(settings.get("speed", "")),
            }
        )

    fields = [
        "voice_id",
        "name",
        "category",
        "description",
        "accent",
        "gender",
        "age",
        "use_case",
        "preview_url",
        "stability",
        "similarity_boost",
        "style",
        "speed",
    ]
    out = Path(args.out)
    write_tsv(out, rows, fields)
    print(f"Wrote {out} with {len(rows)} voices")
    print("API key was not printed.")


if __name__ == "__main__":
    main()
