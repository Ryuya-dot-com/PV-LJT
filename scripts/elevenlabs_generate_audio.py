#!/usr/bin/env python3
"""Generate PV-LJT audio files with the ElevenLabs Text-to-Speech API.

The script reads a recording-script TSV and writes audio files plus a manifest.
It never prints the API key. By default it performs a dry run; pass --generate
to call the API and create audio.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCRIPT = ROOT / "materials" / "audio_recording_script_ljt_v4_pre_audio.tsv"
DEFAULT_OUT_DIR = ROOT / "audio" / "raw" / "elevenlabs" / "ljt_v4"
DEFAULT_MANIFEST = ROOT / "materials" / "elevenlabs_generation_manifest_ljt_v4.tsv"

API_BASE = "https://api.elevenlabs.io/v1"


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


def read_tsv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader), list(reader.fieldnames or [])


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def text_column(row: dict[str, str]) -> str:
    for key in ("text_to_record", "stimulus_text", "sentence_text"):
        if key in row and row[key]:
            return row[key]
    raise ValueError("Input row has no text_to_record, stimulus_text, or sentence_text column")


def item_id(row: dict[str, str]) -> str:
    for key in ("item_id", "trial_id", "practice_id", "recording_id"):
        if key in row and row[key]:
            return row[key]
    raise ValueError("Input row has no item_id, trial_id, practice_id, or recording_id column")


def output_extension(output_format: str) -> str:
    if output_format.startswith("mp3"):
        return ".mp3"
    if output_format.startswith("wav"):
        return ".wav"
    if output_format.startswith("pcm"):
        return ".pcm"
    if output_format.startswith("ulaw"):
        return ".ulaw"
    return ".audio"


def normalized_audio_name(row: dict[str, str], output_format: str) -> str:
    name = row.get("audio_file_name", "").strip()
    ext = output_extension(output_format)
    if name:
        return str(Path(name).with_suffix(ext))
    return f"{item_id(row)}{ext}"


def bool_arg(value: str) -> bool:
    lowered = value.lower()
    if lowered in {"1", "true", "yes", "y", "on"}:
        return True
    if lowered in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"Expected true/false, got {value!r}")


def request_tts(
    *,
    api_key: str,
    voice_id: str,
    model_id: str,
    output_format: str,
    text: str,
    stability: float,
    similarity_boost: float,
    style: float,
    speed: float,
    use_speaker_boost: bool,
    seed: int | None,
    timeout: int,
) -> bytes:
    url = f"{API_BASE}/text-to-speech/{voice_id}?output_format={output_format}"
    payload: dict[str, object] = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost,
            "style": style,
            "use_speaker_boost": use_speaker_boost,
            "speed": speed,
        },
    }
    if seed is not None:
        payload["seed"] = seed

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg" if output_format.startswith("mp3") else "audio/wav",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--recording-script", default=str(DEFAULT_SCRIPT))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--dotenv", default=str(ROOT / ".env"))
    parser.add_argument("--voice-id", default=None)
    parser.add_argument(
        "--voice-id-env",
        default="ELEVENLABS_VOICE_ID",
        help="Environment variable containing the voice ID",
    )
    parser.add_argument(
        "--voice-label",
        default="default",
        help="Human-readable voice label for manifests, e.g. male or female",
    )
    parser.add_argument("--model-id", default=None)
    parser.add_argument("--output-format", default=None)
    parser.add_argument("--stability", type=float, default=0.75)
    parser.add_argument("--similarity-boost", type=float, default=0.75)
    parser.add_argument("--style", type=float, default=0.0)
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--use-speaker-boost", type=bool_arg, default=True)
    parser.add_argument("--seed", type=int, default=20260701)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--generate", action="store_true", help="Call the API and write audio files")
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--max-retries", type=int, default=3)
    args = parser.parse_args()

    load_dotenv(Path(args.dotenv))

    api_key = os.environ.get("ELEVENLABS_API_KEY", "")
    voice_id = args.voice_id or os.environ.get(args.voice_id_env, "")
    if not voice_id and args.voice_id_env != "ELEVENLABS_VOICE_ID":
        voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "")
    model_id = args.model_id or os.environ.get("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")
    output_format = args.output_format or os.environ.get(
        "ELEVENLABS_OUTPUT_FORMAT", "mp3_44100_128"
    )

    if args.generate and not api_key:
        raise SystemExit("ELEVENLABS_API_KEY is not set in the environment or .env")
    if not voice_id:
        raise SystemExit(
            f"{args.voice_id_env} is not set. Add it to .env or pass --voice-id."
        )

    recording_script = Path(args.recording_script)
    out_dir = Path(args.out_dir)
    manifest = Path(args.manifest)
    rows, _ = read_tsv(recording_script)
    if args.limit is not None:
        rows = rows[: args.limit]

    out_dir.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    manifest_rows: list[dict[str, str]] = []

    for index, row in enumerate(rows, start=1):
        text = text_column(row)
        current_seed = args.seed + index - 1 if args.seed is not None else None
        audio_name = normalized_audio_name(row, output_format)
        audio_path = out_dir / audio_name
        status = "planned"
        error = ""

        if args.generate:
            if audio_path.exists() and not args.overwrite:
                status = "skipped_exists"
            else:
                for attempt in range(1, args.max_retries + 1):
                    try:
                        audio = request_tts(
                            api_key=api_key,
                            voice_id=voice_id,
                            model_id=model_id,
                            output_format=output_format,
                            text=text,
                            stability=args.stability,
                            similarity_boost=args.similarity_boost,
                            style=args.style,
                            speed=args.speed,
                            use_speaker_boost=args.use_speaker_boost,
                            seed=current_seed,
                            timeout=args.timeout,
                        )
                        audio_path.write_bytes(audio)
                        status = "generated"
                        break
                    except urllib.error.HTTPError as exc:
                        error = f"HTTP {exc.code}"
                        if exc.code in {400, 401, 403, 404}:
                            break
                    except urllib.error.URLError as exc:
                        error = exc.reason.__class__.__name__
                    if attempt < args.max_retries:
                        time.sleep(2 * attempt)
                else:
                    status = "failed"
                if error and status != "failed":
                    status = "failed"

        manifest_rows.append(
            {
                "source_recording_script": str(recording_script),
                "recording_id": row.get("recording_id", ""),
                "item_id": item_id(row),
                "task": row.get("task", ""),
                "pv": row.get("pv", ""),
                "condition": row.get("condition", ""),
                "item_type": row.get("item_type", ""),
                "text_to_record": text,
                "audio_file_name": audio_name,
                "audio_path": str(audio_path),
                "voice_label": args.voice_label,
                "voice_id_env": args.voice_id_env,
                "voice_id": voice_id,
                "model_id": model_id,
                "output_format": output_format,
                "stability": str(args.stability),
                "similarity_boost": str(args.similarity_boost),
                "style": str(args.style),
                "speed": str(args.speed),
                "use_speaker_boost": str(args.use_speaker_boost),
                "seed": "" if current_seed is None else str(current_seed),
                "generated_at_utc": now if args.generate else "",
                "status": status,
                "error": error,
            }
        )
        print(f"{index}/{len(rows)} {status}: {audio_name}")

    fields = [
        "source_recording_script",
        "recording_id",
        "item_id",
        "task",
        "pv",
        "condition",
        "item_type",
        "text_to_record",
        "audio_file_name",
        "audio_path",
        "voice_label",
        "voice_id_env",
        "voice_id",
        "model_id",
        "output_format",
        "stability",
        "similarity_boost",
        "style",
        "speed",
        "use_speaker_boost",
        "seed",
        "generated_at_utc",
        "status",
        "error",
    ]
    write_tsv(manifest, manifest_rows, fields)
    print(f"Wrote {manifest}")
    if not args.generate:
        print("Dry run only. Re-run with --generate to call ElevenLabs.")


if __name__ == "__main__":
    main()
