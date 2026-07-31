"""Transcribe or translate audio using OpenAI's open-source Whisper model, run locally.

Whisper supports two task modes for the same model call:
- "transcribe": output text in the audio's own spoken language
- "translate": output English text regardless of the spoken language

The "translate" mode is Whisper's built-in translation path - it does not
require a separate translation model or API call, and only ever translates
to English (that's a Whisper model limitation, not a choice made here).
"""

from pathlib import Path
from typing import Literal

import whisper

DEFAULT_MODEL_SIZE = "base"
TaskMode = Literal["transcribe", "translate"]

_model_cache: dict[str, "whisper.Whisper"] = {}


def load_model(model_size: str = DEFAULT_MODEL_SIZE):
    """Load (and cache) a Whisper model by size, so repeated calls don't reload weights."""
    if model_size not in _model_cache:
        _model_cache[model_size] = whisper.load_model(model_size)
    return _model_cache[model_size]


def run_whisper(audio_path: Path, task: TaskMode = "transcribe", model_size: str = DEFAULT_MODEL_SIZE) -> dict:
    """Run Whisper on audio_path and return its raw result dict (text, segments, detected language)."""
    model = load_model(model_size)
    return model.transcribe(str(audio_path), task=task)
