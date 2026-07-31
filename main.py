"""CLI for multilingual audio transcription and translation via local Whisper.

Usage:
    python main.py --input audio.mp3 --task transcribe --format srt
    python main.py --input audio.mp3 --task translate --format txt  # -> English text
    python main.py --input-dir audio_samples --task transcribe --format txt
"""

import argparse
from pathlib import Path

from src.audio_input import find_audio_files, validate_audio_file
from src.output_writer import write_output
from src.transcriber import DEFAULT_MODEL_SIZE, run_whisper


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Local Whisper transcription/translation")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input", type=Path, help="Path to a single audio file.")
    group.add_argument("--input-dir", type=Path, help="Directory of audio files to process.")

    parser.add_argument(
        "--task", choices=["transcribe", "translate"], default="transcribe",
        help="'transcribe' keeps the spoken language; 'translate' outputs English.",
    )
    parser.add_argument(
        "--model-size", default=DEFAULT_MODEL_SIZE,
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size - larger is more accurate but slower and needs more memory.",
    )
    parser.add_argument("--format", choices=["txt", "srt", "json"], default="txt")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def process_file(audio_path: Path, task: str, model_size: str, fmt: str, output_dir: Path) -> None:
    validate_audio_file(audio_path)
    print(f"Processing {audio_path.name} ({task})...")

    result = run_whisper(audio_path, task=task, model_size=model_size)
    detected_language = result.get("language", "unknown")
    print(f"  Detected language: {detected_language}")

    output_path = output_dir / f"{audio_path.stem}.{fmt}"
    write_output(result, output_path, fmt)
    print(f"  Saved to {output_path}")


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    if args.input:
        process_file(args.input, args.task, args.model_size, args.format, args.output_dir)
    else:
        audio_files = find_audio_files(args.input_dir)
        if not audio_files:
            print(f"No supported audio files found in {args.input_dir}")
            return
        print(f"Found {len(audio_files)} audio file(s).")
        for audio_path in audio_files:
            process_file(audio_path, args.task, args.model_size, args.format, args.output_dir)


if __name__ == "__main__":
    main()
