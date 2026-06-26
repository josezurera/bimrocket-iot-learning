#!/usr/bin/env python3
"""
Generate Gemini TTS audio blocks for lesson 1.

Usage from the repository root:

    $env:GEMINI_API_KEY="YOUR_KEY"
    python scripts/generate_tts_gemini.py

The script reads:

    slides/leccion-01/tts/bloques/bloque-*.txt

And writes:

    slides/leccion-01/tts/audio/leccion-01-bloque-XX-algieba.wav

The API key is read only from the GEMINI_API_KEY environment variable.
Do not commit API keys to the repository.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path
import sys
import time
import urllib.error
import urllib.request
import wave


REPO_ROOT = Path(__file__).resolve().parents[1]
BLOCKS_DIR = REPO_ROOT / "slides" / "leccion-01" / "tts" / "bloques"
AUDIO_DIR = REPO_ROOT / "slides" / "leccion-01" / "tts" / "audio"

API_URL = "https://generativelanguage.googleapis.com/v1beta/interactions"
MODEL = "gemini-3.1-flash-tts-preview"
VOICE = "Algieba"

WAV_CHANNELS = 1
WAV_RATE = 24_000
WAV_SAMPLE_WIDTH = 2


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def write_wav(path: Path, pcm: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wav_file:
        wav_file.setnchannels(WAV_CHANNELS)
        wav_file.setsampwidth(WAV_SAMPLE_WIDTH)
        wav_file.setframerate(WAV_RATE)
        wav_file.writeframes(pcm)


def build_prompt(transcript: str) -> str:
    return (
        "Read the following Spanish course narration in a natural Spanish-from-Spain voice. "
        "Use a calm, clear, professional teaching tone. "
        "Speak only the transcript, not these instructions. "
        "Keep the pace slightly slow and didactic.\n\n"
        "Transcript:\n"
        '"""\n'
        f"{transcript.strip()}\n"
        '"""'
    )


def post_tts(api_key: str, transcript: str) -> dict:
    payload = {
        "model": MODEL,
        "input": build_prompt(transcript),
        "response_format": {"type": "audio"},
        "generation_config": {
            "speech_config": [
                {"voice": VOICE},
            ],
        },
    }
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        fail(f"Gemini API returned HTTP {exc.code}: {body}")
    except urllib.error.URLError as exc:
        fail(f"Could not reach Gemini API: {exc}")


def find_audio_base64(response: dict) -> str:
    candidates = [
        ("output_audio", "data"),
        ("outputAudio", "data"),
    ]
    for keys in candidates:
        cursor = response
        for key in keys:
            if not isinstance(cursor, dict) or key not in cursor:
                break
            cursor = cursor[key]
        else:
            if isinstance(cursor, str) and cursor:
                return cursor

    # Fallback for shape changes in preview APIs.
    def walk(value):
        if isinstance(value, dict):
            if isinstance(value.get("data"), str):
                return value["data"]
            for child in value.values():
                found = walk(child)
                if found:
                    return found
        elif isinstance(value, list):
            for child in value:
                found = walk(child)
                if found:
                    return found
        return None

    found = walk(response)
    if isinstance(found, str) and found:
        return found

    fail(
        "Could not find base64 audio in API response. "
        f"Top-level keys: {', '.join(response.keys())}"
    )


def block_number(path: Path) -> str:
    # bloque-01-slides-01-05.txt -> 01
    parts = path.stem.split("-")
    if len(parts) >= 2 and parts[1].isdigit():
        return parts[1]
    return path.stem


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate existing WAV files.",
    )
    parser.add_argument(
        "--only",
        help="Generate a single block number, e.g. 01 or 06.",
    )
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        fail(
            "GEMINI_API_KEY is not set. In PowerShell run: "
            '$env:GEMINI_API_KEY="YOUR_KEY"'
        )

    if not BLOCKS_DIR.exists():
        fail(f"Blocks directory not found: {BLOCKS_DIR}")

    block_files = sorted(BLOCKS_DIR.glob("bloque-*.txt"))
    if args.only:
        wanted = args.only.zfill(2)
        block_files = [p for p in block_files if block_number(p) == wanted]
        if not block_files:
            fail(f"No block found for --only {wanted}")

    if not block_files:
        fail(f"No block files found in {BLOCKS_DIR}")

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Model: {MODEL}")
    print(f"Voice: {VOICE}")
    print(f"Blocks: {len(block_files)}")
    print()

    for index, block_file in enumerate(block_files, start=1):
        number = block_number(block_file)
        output_file = AUDIO_DIR / f"leccion-01-bloque-{number}-algieba.wav"

        if output_file.exists() and not args.force:
            print(f"[skip] {output_file.name} already exists")
            continue

        transcript = block_file.read_text(encoding="utf-8").strip()
        print(f"[{index}/{len(block_files)}] Generating {output_file.name}...")

        response = post_tts(api_key, transcript)
        audio_b64 = find_audio_base64(response)
        pcm = base64.b64decode(audio_b64)
        write_wav(output_file, pcm)

        duration = len(pcm) / (WAV_RATE * WAV_CHANNELS * WAV_SAMPLE_WIDTH)
        print(f"      saved {output_file} ({duration:.1f}s)")

        # Small pause to be gentle with preview/rate limits.
        time.sleep(1)

    print()
    print("Done.")


if __name__ == "__main__":
    main()
