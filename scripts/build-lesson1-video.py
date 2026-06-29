#!/usr/bin/env python3
"""
Build lesson 1 MP4 video from Marp slides and Gemini TTS WAV blocks.

The video is synchronized by blocks:

    slides 01-05 -> leccion-01-bloque-01-algieba.wav
    slides 06-10 -> leccion-01-bloque-02-algieba.wav
    slides 11-15 -> leccion-01-bloque-03-algieba.wav
    slides 16-20 -> leccion-01-bloque-04-algieba.wav
    slides 21-25 -> leccion-01-bloque-05-algieba.wav
    slides 26-29 -> leccion-01-bloque-06-algieba.wav

Usage from the repository root:

    python scripts/build-lesson1-video.py

Output:

    slides/leccion-01/media/final/leccion-01.mp4
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import wave


REPO_ROOT = Path(__file__).resolve().parents[1]
LESSON_DIR = REPO_ROOT / "slides" / "leccion-01"
MARP_MD = LESSON_DIR / "leccion-01.md"
THEME_CSS = LESSON_DIR / "theme.css"
AUDIO_DIR = LESSON_DIR / "tts" / "audio"
MEDIA_DIR = LESSON_DIR / "media"
WORK_DIR = MEDIA_DIR / "work"
SLIDES_DIR = WORK_DIR / "slides"
BLOCKS_DIR = WORK_DIR / "blocks"
FINAL_DIR = MEDIA_DIR / "final"
FINAL_MP4 = FINAL_DIR / "leccion-01.mp4"


BLOCKS = [
    ("01", 1, 5),
    ("02", 6, 10),
    ("03", 11, 15),
    ("04", 16, 20),
    ("05", 21, 25),
    ("06", 26, 29),
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def run(command: list[str], cwd: Path = REPO_ROOT) -> None:
    print("+ " + " ".join(str(part) for part in command))
    subprocess.run(command, cwd=str(cwd), check=True)


def find_ffmpeg() -> str:
    found = shutil.which("ffmpeg")
    if found:
        return found

    local_app_data = os.environ.get("LOCALAPPDATA")
    candidates: list[Path] = []
    if local_app_data:
        winget_packages = Path(local_app_data) / "Microsoft" / "WinGet" / "Packages"
        if winget_packages.exists():
            candidates.extend(winget_packages.glob("**/ffmpeg.exe"))

    extra_roots = [
        Path("C:/ffmpeg"),
        Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "ffmpeg",
        Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "GyanD",
    ]
    for root in extra_roots:
        if root.exists():
            candidates.extend(root.glob("**/ffmpeg.exe"))

    if candidates:
        return str(sorted(candidates)[0])

    fail(
        "ffmpeg was not found. Install it with: "
        "winget install --id Gyan.FFmpeg -e --source winget"
    )


def find_npx() -> str:
    found = shutil.which("npx") or shutil.which("npx.cmd")
    if found:
        return found
    fail("npx was not found. Install Node.js or ensure npx is available in PATH.")


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as wav_file:
        return wav_file.getnframes() / wav_file.getframerate()


def image_path(slide_number: int) -> Path:
    return SLIDES_DIR / f"slide.{slide_number:03d}.png"


def quote_for_concat(path: Path) -> str:
    # ffmpeg concat file list accepts forward slashes on Windows.
    return str(path.resolve()).replace("\\", "/").replace("'", "'\\''")


def ensure_inputs() -> None:
    if not MARP_MD.exists():
        fail(f"Slides Markdown not found: {MARP_MD}")
    if not THEME_CSS.exists():
        fail(f"Theme CSS not found: {THEME_CSS}")

    missing = []
    for block, _start, _end in BLOCKS:
        audio = AUDIO_DIR / f"leccion-01-bloque-{block}-algieba.wav"
        if not audio.exists():
            missing.append(audio)
    if missing:
        print("Missing audio files:")
        for path in missing:
            print(f"  - {path}")
        fail("Generate missing TTS audio before building the video.")


def export_slide_images(npx: str, force: bool) -> None:
    SLIDES_DIR.mkdir(parents=True, exist_ok=True)
    existing = sorted(SLIDES_DIR.glob("slide.*.png"))
    if existing and not force:
        print(f"[skip] Found {len(existing)} existing slide PNG files")
        return

    if SLIDES_DIR.exists():
        shutil.rmtree(SLIDES_DIR)
    SLIDES_DIR.mkdir(parents=True, exist_ok=True)

    run(
        [
            npx,
            "@marp-team/marp-cli",
            str(MARP_MD.relative_to(REPO_ROOT)),
            "--theme",
            str(THEME_CSS.relative_to(REPO_ROOT)),
            "--images",
            "png",
            "--image-scale",
            "1",
            "--allow-local-files",
            "--output",
            str((SLIDES_DIR / "slide.png").relative_to(REPO_ROOT)),
        ]
    )

    count = len(list(SLIDES_DIR.glob("slide.*.png")))
    if count != 29:
        fail(f"Expected 29 slide images, found {count}")


def build_block_video(ffmpeg: str, block: str, start: int, end: int, force: bool) -> Path:
    output = BLOCKS_DIR / f"leccion-01-bloque-{block}.mp4"
    if output.exists() and not force:
        print(f"[skip] {output.name} already exists")
        return output

    BLOCKS_DIR.mkdir(parents=True, exist_ok=True)
    audio = AUDIO_DIR / f"leccion-01-bloque-{block}-algieba.wav"
    duration = wav_duration(audio)
    slide_numbers = list(range(start, end + 1))
    seconds_per_slide = duration / len(slide_numbers)

    concat_file = BLOCKS_DIR / f"leccion-01-bloque-{block}-images.txt"
    print(
        f"Block {block}: slides {start}-{end}, "
        f"audio {duration:.1f}s, {seconds_per_slide:.1f}s/slide"
    )

    command = [ffmpeg, "-y"]
    for slide in slide_numbers:
        img = image_path(slide)
        if not img.exists():
            fail(f"Missing slide image: {img}")
        command.extend(
            [
                "-loop",
                "1",
                "-t",
                f"{seconds_per_slide:.6f}",
                "-i",
                str(img),
            ]
        )
    command.extend(["-i", str(audio)])

    filter_parts = []
    concat_inputs = []
    for idx, _slide in enumerate(slide_numbers):
        filter_parts.append(
            f"[{idx}:v]fps=30,format=yuv420p,setsar=1,setpts=PTS-STARTPTS[v{idx}]"
        )
        concat_inputs.append(f"[v{idx}]")
    filter_parts.append(
        f"{''.join(concat_inputs)}concat=n={len(slide_numbers)}:v=1:a=0[v]"
    )
    filter_complex = ";".join(filter_parts)
    audio_index = len(slide_numbers)

    command.extend(
        [
            "-filter_complex",
            filter_complex,
            "-map",
            "[v]",
            "-map",
            f"{audio_index}:a",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "20",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            "-movflags",
            "+faststart",
            str(output),
        ]
    )

    run(
        command
    )

    return output


def concat_blocks(ffmpeg: str, block_videos: list[Path], force: bool) -> None:
    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    if FINAL_MP4.exists() and not force:
        print(f"[skip] Final video already exists: {FINAL_MP4}")
        return

    concat_file = WORK_DIR / "lesson-01-blocks.txt"
    with concat_file.open("w", encoding="utf-8") as handle:
        for video in block_videos:
            handle.write(f"file '{quote_for_concat(video)}'\n")

    run(
        [
            ffmpeg,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-vf",
            "fps=30,format=yuv420p",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "20",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            str(FINAL_MP4),
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate slide images, block videos, and final MP4.",
    )
    parser.add_argument(
        "--keep-work",
        action="store_true",
        help="Keep intermediate work files.",
    )
    args = parser.parse_args()

    ensure_inputs()
    ffmpeg = find_ffmpeg()
    npx = find_npx()
    print(f"ffmpeg: {ffmpeg}")
    print(f"npx: {npx}")

    WORK_DIR.mkdir(parents=True, exist_ok=True)
    export_slide_images(npx=npx, force=args.force)

    block_videos = [
        build_block_video(ffmpeg, block, start, end, force=args.force)
        for block, start, end in BLOCKS
    ]
    concat_blocks(ffmpeg, block_videos, force=args.force)

    print()
    print(f"Final video: {FINAL_MP4}")
    print(f"Size: {FINAL_MP4.stat().st_size / 1024 / 1024:.1f} MB")

    if not args.keep_work:
        print("Keeping work files for now. Delete slides/leccion-01/media/work manually if needed.")


if __name__ == "__main__":
    main()
