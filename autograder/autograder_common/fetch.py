"""Resolve a Canvas submission (file upload or GitHub URL) into a local
directory containing the student's code."""
import re
import shutil
import subprocess
from pathlib import Path

GITHUB_URL_RE = re.compile(r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/\s]+?)(?:\.git)?(?:/|$)")


class FetchError(Exception):
    pass


def fetch_canvas_upload(submission, canvas_client, dest_dir):
    """submission: a Canvas submission dict with 'attachments' (list of file
    dicts with 'filename' and 'url'). Downloads every attachment into
    dest_dir. Returns the list of downloaded file paths."""
    dest_dir = Path(dest_dir)
    attachments = submission.get("attachments") or []
    if not attachments:
        raise FetchError("no attachments on this submission")
    dest_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for att in attachments:
        dest = dest_dir / att["filename"]
        canvas_client.download_attachment(att, dest)
        paths.append(dest)
    return paths


def fetch_github_url(submission, dest_dir):
    """submission: a Canvas submission dict with 'url' (the GitHub link the
    student pasted into Canvas). Clones the repo (full history, needed for
    git-log-based checks) into dest_dir, replacing any existing directory
    there. Returns dest_dir."""
    url = submission.get("url")
    if not url:
        raise FetchError("no URL on this submission")
    match = GITHUB_URL_RE.search(url)
    if not match:
        raise FetchError(f"URL does not look like a GitHub link: {url}")
    clone_url = f"https://github.com/{match.group('owner')}/{match.group('repo')}.git"
    dest_dir = Path(dest_dir)
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    result = subprocess.run(
        ["git", "clone", clone_url, str(dest_dir)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise FetchError(f"clone of {clone_url} failed: {result.stderr.strip()}")
    return dest_dir


def fetch_submission(submission, assignment_config, canvas_client, dest_dir):
    """Dispatch to fetch_canvas_upload or fetch_github_url based on
    assignment_config['submission_type']."""
    submission_type = assignment_config["submission_type"]
    if submission_type == "canvas_upload":
        return fetch_canvas_upload(submission, canvas_client, dest_dir)
    if submission_type == "github_url":
        return fetch_github_url(submission, dest_dir)
    raise FetchError(f"unknown submission_type: {submission_type!r}")
