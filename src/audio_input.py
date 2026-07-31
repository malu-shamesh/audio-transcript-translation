"""Locate and validate audio files for transcription.

Whisper (via ffmpeg) decodes far more formats than this list, but restricting
to a known-good set catches an unsupported/mistyped file before spending time
loading the model, rather than failing deep inside ffmpeg with a less legible error.
"""

from pathlib import Path

SUPPORTED_EXTENSIONS = {".mp3", ".wav", ".m4a", ".flac", ".ogg", ".mp4", ".webm"}


def find_audio_files(input_dir: Path) -> list[Path]:
    """Return all supported audio files directly under input_dir, sorted by name."""
    return sorted(
        path for path in input_dir.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def validate_audio_file(path: Path) -> None:
    """Raise a clear error if path doesn't look like a usable audio file."""
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {path}")
    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported audio format '{path.suffix}'. Supported: {sorted(SUPPORTED_EXTENSIONS)}"
        )
