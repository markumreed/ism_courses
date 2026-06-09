# Video 24: The Submission Ritual

## YouTube Metadata

**Title:** The ISM3232 Submission Ritual — 9 Steps Every Assignment | ISM3232
**Description:**
The submission ritual is a fixed 9-step sequence you run before submitting every assignment in ISM3232. It's not bureaucracy — it's the professional pre-flight checklist that catches bugs, enforces clean code standards, ensures your tests pass, and guarantees your submission is visible on GitHub. Learn it once, run it every time.

Course page: https://markumreed.github.io/ism3232/docs/week04_lecture.html

**Chapters:**
0:00 — Why a ritual?
1:30 — Step 1: Activate venv
2:30 — Step 2: Run your script
3:30 — Step 3: Run pytest
5:00 — Step 4: Run ruff (linting)
7:00 — Step 5: Run black (formatting)
8:30 — Step 6: Verify output
9:30 — Step 7: git add, commit, push
11:00 — Step 8: Verify on GitHub
12:00 — Step 9: Submit Canvas URL
13:00 — Automating with a shell function
14:30 — Recap

**Applies to:** ISM3232 Module 4

**Tags:** ISM3232 submission ritual, python project workflow, git commit push, pytest, ruff linting, black formatter, python submission checklist, ISM3232, developer workflow, python professional workflow

---

## Script

### INTRO (0:00–1:30)

Every pilot runs the same pre-flight checklist before every flight. Not because they forgot how to fly — because a checklist catches the things that slip through when you're tired, rushed, or confident. The ISM3232 submission ritual is your pre-flight checklist.

Nine steps. Same order every time. Run them before every submission. They take about 3 minutes and will save you from submitting broken code, style violations, or a push that never made it to GitHub.

---

### STEP 1: ACTIVATE venv (1:30–2:30)

```bash
cd ~/ism3232/module_name
source .venv/bin/activate
```

Prompt shows `(.venv)`. You're in the right environment. If you skip this, pytest might not find your packages and ruff might not be available.

---

### STEP 2: RUN YOUR SCRIPT (2:30–3:30)

Run your main Python file from scratch — not from VS Code's run button, from the terminal:

```bash
python3 main.py
```

Read the output. Does it match the expected output in the assignment? Does it crash? Fix any issues before continuing.

If your script requires input, test it now. Catch runtime errors before they become submission errors.

---

### STEP 3: pytest (3:30–5:00)

If the assignment has tests (any assignment from Module 7 onward does):

```bash
pytest -v
```

The `-v` flag shows each test name and its result.

Output when all pass:
```
========================= test session starts ==========================
collected 5 items

tests/test_functions.py::test_calculate_tax PASSED             [ 20%]
tests/test_functions.py::test_apply_discount PASSED            [ 40%]
tests/test_functions.py::test_process_order PASSED             [ 60%]
tests/test_functions.py::test_edge_cases PASSED                [ 80%]
tests/test_functions.py::test_type_validation PASSED           [100%]

========================== 5 passed in 0.12s ===========================
```

If any test fails, fix the code — do not submit with failing tests.

```bash
pytest -v --tb=short   # shorter traceback for faster scanning
```

---

### STEP 4: ruff (5:00–7:00)

`ruff` is a fast Python linter — it checks for style issues, undefined names, unused imports, and common bugs.

```bash
ruff check .
```

If there are no issues:
```
All checks passed!
```

If there are issues:
```
main.py:14:5: F841 Local variable 'x' is assigned to but never used
main.py:22:1: E501 Line too long (102 > 88 characters)
```

Fix each issue. Then run `ruff check .` again until it's clean.

Auto-fix what ruff can fix automatically:
```bash
ruff check --fix .
```

Some issues ruff can fix; others (like logic errors) require your judgment.

---

### STEP 5: black (7:00–8:30)

`black` auto-formats your Python code to a consistent style. It handles indentation, line length, quotes, and spacing — so you don't have to think about formatting.

```bash
black .
```

Output:
```
reformatted main.py
reformatted tests/test_main.py
2 files reformatted.
```

Or if already formatted:
```
1 file left unchanged.
```

After `black` reformats, run `ruff check .` again — black sometimes resolves ruff issues and occasionally surfaces new ones.

---

### STEP 6: VERIFY OUTPUT (8:30–9:30)

Run your script one more time after formatting:

```bash
python3 main.py
```

Check that the output still matches expectations. Formatting shouldn't change logic, but verify anyway.

If the assignment has a specific expected output, compare line by line.

---

### STEP 7: git add, commit, push (9:30–11:00)

```bash
git status        # see what changed
git add .
git commit -m "Complete Module 4 — submission ritual and git/github"
git push
```

Write a descriptive commit message — not "final" or "done". Say what the commit contains.

If `git push` is rejected:
```bash
git pull --rebase
git push
```

---

### STEP 8: VERIFY ON GITHUB (11:00–12:00)

Open a browser. Go to your repository on github.com. Verify:

1. Your latest files are visible (click on `main.py`, read the code)
2. The commit message matches what you wrote
3. Tests directory is present if required
4. `requirements.txt` is present
5. `.venv/` is NOT present (it should be in `.gitignore`)

If anything is missing — the push didn't work. Go back to Step 7.

---

### STEP 9: CANVAS SUBMISSION (12:00–13:00)

Copy the full URL of your repository from your browser's address bar:
```
https://github.com/yourusername/ism3232-module04
```

Paste it in the Canvas assignment submission box. Submit.

After submitting, load the Canvas submission and click the URL to verify it works. A broken link is an unsubmitted assignment.

---

### AUTOMATING WITH A SHELL FUNCTION (13:00–14:30)

Add this to your `~/.zshrc` to run steps 3–6 with one command:

```bash
ritual() {
    echo "=== Step 1: Running tests ==="
    pytest -v
    echo ""
    echo "=== Step 2: Linting with ruff ==="
    ruff check .
    echo ""
    echo "=== Step 3: Formatting with black ==="
    black .
    echo ""
    echo "=== Step 4: Re-checking after format ==="
    ruff check .
    echo ""
    echo "=== Ritual complete. Review output above. ==="
}
```

After `source ~/.zshrc`, run `ritual` from any project directory. It runs all four checks in sequence.

---

### RECAP (14:30–15:00)

The 9-step ritual:

1. `source .venv/bin/activate`
2. `python3 main.py` — verify output
3. `pytest -v` — all tests pass
4. `ruff check .` — no lint errors
5. `black .` — auto-format
6. `python3 main.py` — verify again
7. `git add . && git commit -m "message" && git push`
8. Verify files on github.com
9. Paste GitHub URL in Canvas, submit

Run this every time. No exceptions. The checklist is the professionalism.
