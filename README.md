# audio-transcript-translation

Automated multilingual transcription with Whisper.

This repo previously contained no code - only this README. Built out from scratch as a runnable CLI tool rather than a converted notebook (there was nothing to convert).

## What it does

Transcribes or translates audio files using [OpenAI's open-source Whisper model](https://github.com/openai/whisper), run entirely locally:

- **`transcribe`**: outputs text in the audio's own spoken language (multilingual - Whisper supports dozens of languages and auto-detects the spoken one).
- **`translate`**: outputs English text regardless of the spoken language, using Whisper's built-in translation task mode - not a separate translation model or API call. This is a Whisper model limitation as well as its feature: it only ever translates *to* English, not between arbitrary language pairs.

Output can be written as plain text (`.txt`), subtitles (`.srt`), or structured JSON with per-segment timestamps.

## Why Whisper (free, no trial tiers)

`openai-whisper` is the original open-source package - not the paid OpenAI API. Once model weights are downloaded (automatically, on first use, cached locally), everything runs offline with no API key, no per-minute cost, and no usage cap.

## Architecture

```
src/
  audio_input.py    # Finds/validates audio files (extension check before touching Whisper)
  transcriber.py     # Loads (and caches) a Whisper model, runs transcribe/translate
  output_writer.py   # Formats Whisper's result dict as .txt / .srt / .json
main.py              # CLI: validate -> transcribe/translate -> write output
```

## Setup

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**ffmpeg is also required** (Whisper uses it to decode audio) - install via your OS package manager (`brew install ffmpeg`, `apt-get install ffmpeg`, or the [Windows builds](https://www.gyan.dev/ffmpeg/builds/)) and ensure it's on your `PATH`.

## Usage

```bash
# Transcribe in the spoken language, SRT subtitles
python main.py --input audio.mp3 --task transcribe --format srt

# Translate to English, plain text
python main.py --input audio.mp3 --task translate --format txt

# Process every supported file in a directory
python main.py --input-dir audio_samples --task transcribe --format json

# Use a larger, more accurate (but slower) model
python main.py --input audio.mp3 --model-size medium
```

Model sizes (`tiny` to `large`) trade accuracy for speed/memory - `base` is the default. Output files land in `--output-dir` (default `outputs/`), named after the input file with the chosen format's extension.

## Tests

```bash
pytest
```

Covers `audio_input.py` (extension filtering, sorted results, missing/unsupported file errors) and `output_writer.py` (SRT timestamp formatting including negative-time clamping, text/SRT/JSON formatting from a sample Whisper result dict, and the unsupported-format error path) - none of which need Whisper or ffmpeg to run.

## Verification

Unlike several other repos converted this session (`Agentic-document-extraction`'s PaddleOCR, `classify-handwritten-digits`' TensorFlow), **`openai-whisper` and its `torch` dependency install and import cleanly on this environment's Python 3.14** - confirmed directly, not assumed. `src/audio_input.py` and `src/output_writer.py` are fully verified with 12 passing tests.

What could *not* be verified: **ffmpeg is not installed in this environment**, and Whisper requires it unconditionally - even for raw WAV files. `src/transcriber.py`'s model-loading step (`whisper.load_model`) was confirmed to work (downloads and loads real model weights successfully), but running `main.py` against a synthetic test WAV confirmed Whisper's `load_audio` always shells out to the `ffmpeg` binary via `subprocess.run`, with no pure-Python fallback - it fails with `FileNotFoundError: [WinError 2] The system cannot find the file specified` without it. So the actual transcribe/translate call is unverified here, but the failure mode is now confirmed rather than assumed. Install ffmpeg and re-run `main.py` against a real audio file before relying on this tool.
