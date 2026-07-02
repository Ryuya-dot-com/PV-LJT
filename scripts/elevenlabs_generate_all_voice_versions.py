#!/usr/bin/env python3
"""Generate or dry-run all PV-LJT audio sets for male and female voices."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "elevenlabs_generate_audio.py"

TASKS = [
    {
        "label": "ljt_v4",
        "recording_script": ROOT / "materials" / "audio_recording_script_ljt_v4_pre_audio.tsv",
    },
    {
        "label": "audio_decision_v2",
        "recording_script": ROOT / "materials" / "audio_recording_script_audio_decision_v2.tsv",
    },
    {
        "label": "practice_v1",
        "recording_script": ROOT / "materials" / "audio_recording_script_practice_v1.tsv",
    },
]

VOICES = [
    {
        "label": "male",
        "env": "ELEVENLABS_MALE_VOICE_ID",
    },
    {
        "label": "female",
        "env": "ELEVENLABS_FEMALE_VOICE_ID",
    },
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true", help="Call the API")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dotenv", default=str(ROOT / ".env"))
    parser.add_argument("--output-root", default=str(ROOT / "audio" / "raw" / "elevenlabs"))
    parser.add_argument("--manifest-dir", default=str(ROOT / "materials"))
    parser.add_argument("--stability", type=float, default=0.75)
    parser.add_argument("--similarity-boost", type=float, default=0.75)
    parser.add_argument("--style", type=float, default=0.0)
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=20260701)
    args = parser.parse_args()

    output_root = Path(args.output_root)
    manifest_dir = Path(args.manifest_dir)

    for voice in VOICES:
        for task in TASKS:
            out_dir = output_root / voice["label"] / task["label"]
            manifest = (
                manifest_dir
                / f"elevenlabs_generation_manifest_{voice['label']}_{task['label']}.tsv"
            )
            cmd = [
                sys.executable,
                str(GENERATOR),
                "--dotenv",
                args.dotenv,
                "--recording-script",
                str(task["recording_script"]),
                "--out-dir",
                str(out_dir),
                "--manifest",
                str(manifest),
                "--voice-id-env",
                voice["env"],
                "--voice-label",
                voice["label"],
                "--stability",
                str(args.stability),
                "--similarity-boost",
                str(args.similarity_boost),
                "--style",
                str(args.style),
                "--speed",
                str(args.speed),
                "--seed",
                str(args.seed),
            ]
            if args.limit is not None:
                cmd.extend(["--limit", str(args.limit)])
            if args.overwrite:
                cmd.append("--overwrite")
            if args.generate:
                cmd.append("--generate")

            print(f"Running {voice['label']} / {task['label']}", flush=True)
            subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
