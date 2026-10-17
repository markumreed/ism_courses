# ISM3232 reference builds

Working copies of the code that the ISM3232 pages teach. Pages are generated
from these files, so a listing on the site always matches code that ran.

- `module06_agents/`: the Weeks 10–12 lab folder. Its git history holds each
  checkpoint (Week 11 end, Week 12 guided parts, Week 12 with exercises and
  mini-project).
- `bayside_app/`: the Bayside Outfitters reference app that the Week 13–16
  pages quote. It is laid out exactly like a student's capstone repository.
  Checkpoint commits (page builders read each week's listings from these):
  - Week 13 `04bc8c9`: `schema.sql`
  - Week 14 `d44a23b`: `database.py`, `tools.py`, `agent.py`, `settings.py`,
    `main.py`, the four model files, `tests/`
  - Week 15 `8b1b491`: `app.py`
  - Week 16 `172d6ad`: `evaluation.py` (the whole app)
  (The first Week 14–16 checkpoints, `835cc6f`, `ce25ab8` and `637468a`, came
  before the final-review fixes and must not be used for pages.)
- `bayside_dev_tests/`: Streamlit `AppTest` and evaluation checks for the app.
  They live beside the app, not inside it, so `pytest` in `bayside_app/` (and
  the autograder) never collects them. Run with
  `python -m pytest -q reference/ism3232/bayside_dev_tests`.
- `tools/streamlit_shots.py`: screenshots both tabs of a running Streamlit app.
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
