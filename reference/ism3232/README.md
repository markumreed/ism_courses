# ISM3232 reference builds

Working copies of the code that the ISM3232 pages teach. Pages are generated
from these files, so a listing on the site always matches code that ran.

- `module06_agents/`: the Weeks 10–12 lab folder. Its git history holds each
  checkpoint (Week 11 end, Week 12 guided parts, Week 12 with exercises and
  mini-project).
- `tools/check.py`: copies a folder to a temporary directory and runs
  `ruff format --check`, `ruff check` (default rules), and pytest with the
  `ollama` and `streamlit` packages blocked, as the autograder sees it.
- `tools/count_runs.py`: runs one conversation several times against the
  course model and prints every run.
- `runs/weekNN/`: captured real runs that the pages quote.

Real runs use the course model on the CPU only, as on a student laptop
without a usable GPU, with Ollama's default 4k context:

    CUDA_VISIBLE_DEVICES=-1 ollama serve

Do not pin it to a few cores with taskset: llama-server still starts one
thread per physical core, and the oversubscribed threads make each reply
take minutes. Pages never quote timings from these runs.

Use a Python that has ruff, pytest, ollama, and streamlit installed (a
virtual environment outside this repo). Exams and keys never go here.
