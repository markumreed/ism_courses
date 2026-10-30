#!/usr/bin/env bash
# Re-capture the Week 15 browser session from the Bayside Week 15 checkpoint.
# Start the server first, on the CPU only:  CUDA_VISIBLE_DEVICES=-1 ollama serve
# PY must point to a Python with streamlit, ollama and websockets. Run from the repository root.
set -eu
PY=${PY:?set PY to a Python that has streamlit, ollama and websockets}
ollama list | grep -q 'granite4.1:3b' || { echo "Ollama is not running, or granite4.1:3b is not pulled"; exit 1; }
COPY=$("$PY" -B -c "import sys; sys.path.insert(0,'reference/ism3232/builders'); from pagekit import folder_at; print(folder_at('8b1b491', 'reference/ism3232/bayside_app'))")
mkdir -p ism3232/assets/img/week15
"$PY" -B reference/ism3232/runs/week15/session.py "$COPY" reference/ism3232/runs/week15/session.txt ism3232/assets/img/week15
ollama ps | grep -q 'granite4.1:3b' || { echo "The course model was not loaded: the keyword rules may have answered"; exit 1; }
