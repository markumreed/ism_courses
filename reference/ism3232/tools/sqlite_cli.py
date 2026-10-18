"""Run the sqlite3 command-line tool the way students see it.

The Week 13 pages show sqlite3 3.45.1, the version `sudo apt install sqlite3`
installs on Ubuntu 24.04 (WSL). Other versions space `.mode column` output
differently, so `fetch` downloads exactly that package with apt, checks its
SHA-256 against the value in apt's signed index, and unpacks it.

    python reference/ism3232/tools/sqlite_cli.py DIR   # prints the checked sqlite3
"""

import hashlib
import os
import subprocess
import sys
from pathlib import Path

PACKAGE = "sqlite3=3.45.1-1ubuntu2.8"
DEB = "sqlite3_3.45.1-1ubuntu2.8_amd64.deb"
SHA256 = "78493e56909614ec1d588c9fae1739a704d9e1a6ff65509b1f06c3e4d53ed0c3"
VERSION = "3.45.1"


def verify_sha256(path, expected):
    """Raise ValueError unless the file's SHA-256 is `expected`."""
    digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if digest != expected:
        raise ValueError(f"{path}: SHA-256 is {digest}, expected {expected}")


def check_version(cli):
    """Return the `--version` line, or raise ValueError if it is not 3.45.1."""
    line = subprocess.run(
        [str(cli), "--version"], capture_output=True, text=True, check=True
    ).stdout.rstrip("\n")
    if not line.startswith(VERSION + " "):
        raise ValueError(f"{cli} prints {line!r}, expected version {VERSION}")
    return line


def fetch(target):
    """Download, check, and unpack the package into `target`; return sqlite3's path."""
    target = Path(target)
    target.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["apt-get", "download", PACKAGE], cwd=target, check=True, capture_output=True
    )
    verify_sha256(target / DEB, SHA256)
    subprocess.run(["dpkg-deb", "-x", DEB, "unpacked"], cwd=target, check=True)
    cli = target / "unpacked" / "usr" / "bin" / "sqlite3"
    check_version(cli)
    return cli


def cli_from_env():
    """The checked sqlite3 that $SQLITE3_CLI names."""
    cli = os.environ.get("SQLITE3_CLI")
    if not cli:
        raise SystemExit(
            "set SQLITE3_CLI: python reference/ism3232/tools/sqlite_cli.py DIR"
        )
    check_version(cli)
    return Path(cli)


def transcript(cli, folder, lines, db="bayside.db"):
    """What a student sees after typing `lines` into `sqlite3 db` inside `folder`:
    the banner, then 'sqlite> ' and each typed line, then what it printed."""
    result = subprocess.run(
        [str(cli), "-interactive", db],
        cwd=folder,
        input="\n".join(lines) + "\n",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    text = result.stdout.rstrip("\n")
    if text.endswith("sqlite> "):
        text = text[: -len("sqlite> ")].rstrip("\n")
    return text


if __name__ == "__main__":
    print(fetch(sys.argv[1]))
