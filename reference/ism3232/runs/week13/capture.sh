#!/usr/bin/env bash
set -eu
# Re-capture every Week 13 sqlite3 transcript with the sqlite3 that Ubuntu 24.04
# installs (3.45.1). DIR is a scratch folder for the downloaded package.
#   PY=<python3.12> reference/ism3232/runs/week13/capture.sh DIR
PY=${PY:?set PY to a Python 3.12}
DIR=${1:?give a scratch folder for the sqlite3 package}
cd "$(dirname "$0")/../../../.."
SQLITE3_CLI=$("$PY" -B reference/ism3232/tools/sqlite_cli.py "$DIR")
export SQLITE3_CLI
"$PY" -B reference/ism3232/builders/week13_capture.py
