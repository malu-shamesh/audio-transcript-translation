import pytest

from src.audio_input import find_audio_files, validate_audio_file


def test_find_audio_files_filters_by_supported_extension(tmp_path):
    (tmp_path / "a.mp3").write_bytes(b"")
    (tmp_path / "b.wav").write_bytes(b"")
    (tmp_path / "c.txt").write_bytes(b"")
    (tmp_path / "sub").mkdir()

    files = find_audio_files(tmp_path)

    assert [f.name for f in files] == ["a.mp3", "b.wav"]


def test_find_audio_files_returns_sorted_results(tmp_path):
    (tmp_path / "z.mp3").write_bytes(b"")
    (tmp_path / "a.mp3").write_bytes(b"")

    files = find_audio_files(tmp_path)

    assert [f.name for f in files] == ["a.mp3", "z.mp3"]


def test_validate_audio_file_raises_for_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        validate_audio_file(tmp_path / "missing.mp3")


def test_validate_audio_file_raises_for_unsupported_extension(tmp_path):
    bad_file = tmp_path / "notes.txt"
    bad_file.write_text("not audio")

    with pytest.raises(ValueError):
        validate_audio_file(bad_file)


def test_validate_audio_file_passes_for_supported_extension(tmp_path):
    audio_file = tmp_path / "clip.wav"
    audio_file.write_bytes(b"")

    validate_audio_file(audio_file)  # should not raise
