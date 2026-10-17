#!/usr/bin/env bash
# Re-run every Bayside app capture. Start the server first, on the CPU only:
#   CUDA_VISIBLE_DEVICES=-1 ollama serve
# PY must point to a Python with ollama, streamlit and pytest installed.
# Run from the repository root. The terminal runs use a scratch copy of the
# app, so no bayside.db lands in the repo.
set -u
PY=${PY:?set PY to a Python that has ollama and streamlit}
RUNS=$PWD/reference/ism3232/runs/bayside_app
COPY=$("$PY" -B -c "import sys; sys.path.insert(0,'reference/ism3232/builders'); from pagekit import folder_at; print(folder_at('HEAD', 'reference/ism3232/bayside_app'))")

# Week 14: the terminal program, run twice against the same bayside.db.
(cd "$COPY" && printf '%s\n' "hello" "Where is order A104?" "Is the fleece vest in stock?" "Please change the address on order A102 to 9 Pine Street, Tampa" "What happened to request 1?" "quit" "no" | "$PY" -B main.py > "$RUNS/main_first_run.txt" 2>&1)
(cd "$COPY" && printf '%s\n' "What happened to request 1?" "quit" | "$PY" -B main.py > "$RUNS/main_second_run.txt" 2>&1)

# Week 15: the app with the course model, driven by Streamlit's AppTest.
"$PY" -B reference/ism3232/runs/bayside_app/app_session.py > "$RUNS/app_session.txt" 2>&1

# Prompt size of a long chat, trimmed and untrimmed.
"$PY" -B reference/ism3232/runs/bayside_app/prompt_size.py > "$RUNS/prompt_size.txt" 2>&1

# Week 16: the evaluation table (a few minutes on the CPU).
(cd "$COPY" && "$PY" -B evaluation.py > "$RUNS/evaluation.txt" 2>&1)

# The app with Ollama switched off (the keyword fallback answers).
pkill -x ollama; pkill -x llama-server; sleep 2
"$PY" -B reference/ism3232/runs/bayside_app/app_session.py > "$RUNS/app_session_ollama_off.txt" 2>&1
