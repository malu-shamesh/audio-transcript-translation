"""Format Whisper's result dict into plain text, SRT subtitles, or JSON."""

import json
from pathlib import Path


def format_srt_timestamp(seconds: float) -> str:
    """Convert seconds to SRT's HH:MM:SS,mmm timestamp format."""
    if seconds < 0:
        seconds = 0
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    milliseconds = round((secs - int(secs)) * 1000)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(secs):02d},{milliseconds:03d}"


def to_text(result: dict) -> str:
    return result["text"].strip()


def to_srt(result: dict) -> str:
    lines = []
    for i, segment in enumerate(result.get("segments", []), start=1):
        start = format_srt_timestamp(segment["start"])
        end = format_srt_timestamp(segment["end"])
        text = segment["text"].strip()
        lines.append(f"{i}\n{start} --> {end}\n{text}\n")
    return "\n".join(lines)


def to_json(result: dict) -> str:
    payload = {
        "text": result.get("text", "").strip(),
        "language": result.get("language"),
        "segments": [
            {"start": seg["start"], "end": seg["end"], "text": seg["text"].strip()}
            for seg in result.get("segments", [])
        ],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def write_output(result: dict, output_path: Path, fmt: str) -> None:
    writers = {"txt": to_text, "srt": to_srt, "json": to_json}
    if fmt not in writers:
        raise ValueError(f"Unsupported format '{fmt}'. Supported: {sorted(writers)}")

    content = writers[fmt](result)
    output_path.write_text(content, encoding="utf-8")
