import json

import pytest

from src.output_writer import format_srt_timestamp, to_json, to_srt, to_text, write_output


def _sample_result() -> dict:
    return {
        "text": "  Hello world. This is a test.  ",
        "language": "en",
        "segments": [
            {"start": 0.0, "end": 1.5, "text": " Hello world."},
            {"start": 1.5, "end": 3.25, "text": " This is a test."},
        ],
    }


def test_format_srt_timestamp_formats_hours_minutes_seconds_millis():
    assert format_srt_timestamp(3725.123) == "01:02:05,123"


def test_format_srt_timestamp_clamps_negative_to_zero():
    assert format_srt_timestamp(-5) == "00:00:00,000"


def test_to_text_strips_whitespace():
    assert to_text(_sample_result()) == "Hello world. This is a test."


def test_to_srt_produces_numbered_cues_with_timestamps():
    srt = to_srt(_sample_result())

    assert "1\n00:00:00,000 --> 00:00:01,500\nHello world." in srt
    assert "2\n00:00:01,500 --> 00:00:03,250\nThis is a test." in srt


def test_to_json_produces_valid_json_with_expected_keys():
    data = json.loads(to_json(_sample_result()))

    assert data["language"] == "en"
    assert data["text"] == "Hello world. This is a test."
    assert len(data["segments"]) == 2
    assert data["segments"][0]["text"] == "Hello world."


def test_write_output_rejects_unsupported_format(tmp_path):
    with pytest.raises(ValueError):
        write_output(_sample_result(), tmp_path / "out.xml", "xml")


def test_write_output_writes_txt_file(tmp_path):
    output_path = tmp_path / "out.txt"
    write_output(_sample_result(), output_path, "txt")

    assert output_path.read_text(encoding="utf-8") == "Hello world. This is a test."
