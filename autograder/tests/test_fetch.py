from unittest.mock import patch

import pytest

from autograder_common.fetch import FetchError, fetch_canvas_upload, fetch_github_url, fetch_submission


class FakeCanvasClient:
    def __init__(self):
        self.downloaded = []

    def download_attachment(self, attachment, dest_path):
        self.downloaded.append((attachment, dest_path))
        dest_path.write_text("fake content")


def test_fetch_canvas_upload_downloads_each_attachment(tmp_path):
    client = FakeCanvasClient()
    submission = {"attachments": [{"filename": "pricer.py", "url": "http://x/pricer.py"}]}
    dest_dir = tmp_path / "student"

    paths = fetch_canvas_upload(submission, client, dest_dir)

    assert paths == [dest_dir / "pricer.py"]
    assert (dest_dir / "pricer.py").read_text() == "fake content"


def test_fetch_canvas_upload_no_attachments_raises(tmp_path):
    client = FakeCanvasClient()
    submission = {"attachments": []}

    with pytest.raises(FetchError, match="no attachments"):
        fetch_canvas_upload(submission, client, tmp_path / "student")


def test_fetch_github_url_invalid_url_raises(tmp_path):
    submission = {"url": "https://not-github.example.com/foo/bar"}

    with pytest.raises(FetchError, match="does not look like a GitHub link"):
        fetch_github_url(submission, tmp_path / "student")


def test_fetch_github_url_no_url_raises(tmp_path):
    with pytest.raises(FetchError, match="no URL"):
        fetch_github_url({}, tmp_path / "student")


def test_fetch_github_url_clones_with_correct_url(tmp_path):
    submission = {"url": "https://github.com/janedoe/ism3232-week07"}
    dest_dir = tmp_path / "student"

    with patch("autograder_common.fetch.subprocess.run") as fake_run:
        fake_run.return_value.returncode = 0
        result = fetch_github_url(submission, dest_dir)

    assert result == dest_dir
    args = fake_run.call_args[0][0]
    assert args[:2] == ["git", "clone"]
    assert args[-2] == "https://github.com/janedoe/ism3232-week07.git"
    assert args[-1] == str(dest_dir)


def test_fetch_github_url_removes_existing_dest_before_cloning(tmp_path):
    dest_dir = tmp_path / "student"
    dest_dir.mkdir()
    (dest_dir / "stale_file.txt").write_text("old content")
    submission = {"url": "https://github.com/janedoe/ism3232-week07"}

    with patch("autograder_common.fetch.subprocess.run") as fake_run:
        fake_run.return_value.returncode = 0
        fetch_github_url(submission, dest_dir)

    assert not (dest_dir / "stale_file.txt").exists()


def test_fetch_github_url_clone_failure_raises(tmp_path):
    submission = {"url": "https://github.com/janedoe/private-repo"}

    with patch("autograder_common.fetch.subprocess.run") as fake_run:
        fake_run.return_value.returncode = 128
        fake_run.return_value.stderr = "repository not found"
        with pytest.raises(FetchError, match="repository not found"):
            fetch_github_url(submission, tmp_path / "student")


def test_fetch_submission_dispatches_to_canvas_upload(tmp_path):
    client = FakeCanvasClient()
    submission = {"attachments": [{"filename": "pricer.py", "url": "http://x/pricer.py"}]}
    assignment_config = {"submission_type": "canvas_upload"}

    fetch_submission(submission, assignment_config, client, tmp_path / "student")

    assert (tmp_path / "student" / "pricer.py").exists()


def test_fetch_submission_dispatches_to_github_url(tmp_path):
    submission = {"url": "https://github.com/janedoe/ism3232-week07"}
    assignment_config = {"submission_type": "github_url"}

    with patch("autograder_common.fetch.subprocess.run") as fake_run:
        fake_run.return_value.returncode = 0
        fetch_submission(submission, assignment_config, None, tmp_path / "student")

    fake_run.assert_called_once()


def test_fetch_submission_unknown_type_raises(tmp_path):
    with pytest.raises(FetchError, match="unknown submission_type"):
        fetch_submission({}, {"submission_type": "carrier_pigeon"}, None, tmp_path / "student")
