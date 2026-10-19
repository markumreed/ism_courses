#!/usr/bin/env bash
# Re-capture the Week 14 terminal runs from the Bayside Week 14 checkpoint.
# Start the server first, on the CPU only:  CUDA_VISIBLE_DEVICES=-1 ollama serve
# PY must point to a Python with the ollama package. Run from the repository root.
set -eu
PY=${PY:?set PY to a Python that has the ollama package}
RUNS=$PWD/reference/ism3232/runs/week14
COPY=$("$PY" -B -c "import sys; sys.path.insert(0,'reference/ism3232/builders'); from pagekit import folder_at; print(folder_at('d44a23b', 'reference/ism3232/bayside_app'))")
(cd "$COPY" && printf '%s\n' "hello" "Where is order A104?" "Is the fleece vest in stock?" "Please change the address on order A102 to 9 Pine Street, Tampa" "What happened to request 1?" "quit" "no" | "$PY" -B main.py >| "$RUNS/main_first_run.txt" 2>&1)
(cd "$COPY" && printf '%s\n' "What happened to request 1?" "quit" | "$PY" -B main.py >| "$RUNS/main_second_run.txt" 2>&1)
