#!/usr/bin/env bash
# Re-capture the Week 16 runs from the Bayside app at HEAD (the Week 16 checkpoint).
# Start the server first, on the CPU only. Ollama 0.34 also reaches the GPU through
# Vulkan, so hide both:
#   CUDA_VISIBLE_DEVICES=-1 GGML_VK_VISIBLE_DEVICES=-1 OLLAMA_VULKAN=0 ollama serve
# PY must point to a Python with the ollama package. Run from the repository root.
# Takes several minutes on the CPU.
set -eu
PY=${PY:?set PY to a Python that has the ollama package}
ollama list | grep -q 'granite4.1:3b' || { echo "Ollama is not running, or granite4.1:3b is not pulled"; exit 1; }
RUNS=$PWD/reference/ism3232/runs/week16
COPY=$("$PY" -B -c "import sys; sys.path.insert(0,'reference/ism3232/builders'); from pagekit import folder_at; print(folder_at('HEAD', 'reference/ism3232/bayside_app'))")
# Load the model once and refuse to go on unless it runs on the CPU.
ollama run granite4.1:3b 'Answer in one word: hello' </dev/null >/dev/null
ollama ps | grep 'granite4.1:3b' | grep -q '100% CPU' || { echo "The model is not on the CPU: restart the server as above"; exit 1; }
(cd "$COPY" && "$PY" -B evaluation.py >| "$RUNS/evaluation.txt")
(cd "$COPY" && "$PY" -B "$RUNS/safety.py" "$COPY" "$RUNS")
ollama ps | grep 'granite4.1:3b' | grep -q '100% CPU' || { echo "The course model was not on the CPU at the end"; exit 1; }
