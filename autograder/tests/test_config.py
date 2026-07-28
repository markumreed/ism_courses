import pytest

from autograder_common.config import ConfigError, load_assignment_config, load_course_config


def test_load_course_config_reads_fields(tmp_path, monkeypatch):
    monkeypatch.setenv("CANVAS_API_TOKEN", "secret-token")
    path = tmp_path / "course.yaml"
    path.write_text("canvas_base_url: 'https://example.instructure.com/'\ncanvas_course_id: 123\n")

    config = load_course_config(path)

    assert config == {
        "canvas_base_url": "https://example.instructure.com",
        "canvas_course_id": 123,
        "canvas_token": "secret-token",
    }


def test_load_course_config_missing_field_raises(tmp_path, monkeypatch):
    monkeypatch.setenv("CANVAS_API_TOKEN", "secret-token")
    path = tmp_path / "course.yaml"
    path.write_text("canvas_base_url: 'https://example.instructure.com/'\n")

    with pytest.raises(ConfigError, match="canvas_course_id"):
        load_course_config(path)


def test_load_course_config_missing_token_raises(tmp_path, monkeypatch):
    monkeypatch.delenv("CANVAS_API_TOKEN", raising=False)
    path = tmp_path / "course.yaml"
    path.write_text("canvas_base_url: 'https://example.instructure.com/'\ncanvas_course_id: 123\n")

    with pytest.raises(ConfigError, match="CANVAS_API_TOKEN"):
        load_course_config(path)


def test_load_assignment_config_reads_fields(tmp_path):
    path = tmp_path / "week03_lab.yaml"
    path.write_text(
        "course: ism2411\nkey: week03_lab\nsubmission_type: canvas_upload\n"
        "rubric:\n  submission:\n    points: 1\n    source: mechanical\n    check: file_present\n"
    )

    config = load_assignment_config(path)

    assert config["course"] == "ism2411"
    assert config["submission_type"] == "canvas_upload"
    assert config["rubric"]["submission"]["points"] == 1


def test_load_assignment_config_bad_submission_type_raises(tmp_path):
    path = tmp_path / "bad.yaml"
    path.write_text(
        "course: ism2411\nkey: bad\nsubmission_type: carrier_pigeon\nrubric: {}\n"
    )

    with pytest.raises(ConfigError, match="submission_type"):
        load_assignment_config(path)


def test_load_assignment_config_missing_field_raises(tmp_path):
    path = tmp_path / "bad.yaml"
    path.write_text("course: ism2411\n")

    with pytest.raises(ConfigError, match="missing required field"):
        load_assignment_config(path)
