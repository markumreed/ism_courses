# ISM3232 Lab W16: GenAI Feature & Final Demo

## YouTube Metadata

**Title:** GenAI Feature, Testing & Final Demo — Full Lab Walkthrough | ISM3232 Lab 16
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM3232 Module 16 Lab — the final capstone lab. Build a controlled AI summary feature with all six required GenAI controls: disclosure label, human review gate, no PII sent to the API, a mocked pytest test, documented limitations, and full explainability. Wire it into Streamlit, write the mocked tests, complete the README, run the final checklist, and prepare the eight-topic capstone demo.

Course page: https://markumreed.github.io/ism3232/docs/week16_lab.html

**Chapters:**
0:00 — The six required GenAI controls
0:50 — Step 1: install the Anthropic SDK
1:20 — Step 2: write summarise_request()
2:40 — Step 3: test it manually in the Python shell
3:40 — Screenshot 1 checkpoint
4:00 — Step 4: add the AI feature UI to Tab 1
5:40 — Step 5: the disclosure label and review gate, explained
6:30 — Step 6: run the full flow — generate, review, save
7:30 — Screenshot 2 checkpoint
7:50 — Step 7: write the mocked API tests
10:00 — Step 8: why mocking matters here, explained
10:40 — Step 9: run pytest -v and confirm both pass
11:10 — Step 10: complete the README AI feature section
12:10 — Step 11: walk the final checklist, item by item
14:00 — Step 12: the final push
14:30 — Step 13: prepare the eight-topic demo
16:00 — Submission checklist

**Applies to:** ISM3232 Module 16

**Tags:** anthropic api python tutorial, genai responsible ai controls, pytest mock unittest, streamlit ai feature, ISM3232, USF, capstone final demo

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step. This is the final capstone lab — every control here is graded individually, and missing even one fails the feature on the rubric.

---

## Script

### INTRO (0:00–0:50)

**SAY:** "Lab 16 — the GenAI feature and final demo. Six controls are required, and missing any one fails this feature on the capstone rubric. One: a disclosure label in the UI. Two: human review before anything is saved. Three: no personally identifiable information sent to the API. Four: a test using a mocked API call. Five: limitations documented in the README. Six: you personally can explain every line. Let's build all six."

---

### PART 1 — Build ai_feature.py (0:50–3:40)

#### Step 1 — Install the SDK

**DO:**
```bash
cd ~/ism3232/module07_final_project
source .venv/bin/activate
pip install anthropic
pip freeze > requirements.txt
touch ai_feature.py && code ai_feature.py
```

**CHECK:** `requirements.txt` now includes `anthropic` alongside `streamlit`, `pytest`, and `ruff`.

---

#### Step 2 — Write summarise_request()

**SAY:** "Control three starts right here, in the function signature — notice exactly what gets passed in."

**DO:**
```python
import anthropic


def summarise_request(category: str, description: str) -> str:
    """
    Return a one-sentence AI summary of a business request.
    Only category and description are sent -- no names, IDs, or amounts.
    """
    client = anthropic.Anthropic()
    prompt = f'Summarise this {category} business request in one clear sentence:\n{description}'
    message = client.messages.create(
        model='claude-haiku-4-5-20251001',
        max_tokens=150,
        messages=[{'role': 'user', 'content': prompt}]
    )
    return message.content[0].text
```

**CHECK:** Read the docstring's second line out loud and confirm the function signature matches it exactly: "`category` and `description` are the only two parameters — no `requester`, no `record_id`, no dollar `amount`. That's control three, no PII sent to the API, enforced structurally by the function's own signature, not just a promise in a comment."

---

#### Step 3 — Test manually in the Python shell

**DO:**
```bash
python3
```
```python
>>> from ai_feature import summarise_request
>>> result = summarise_request('Travel', 'Flight and hotel for Q4 sales conference')
>>> print(result)
>>> exit()
```

**CHECK:** A one-sentence AI-generated summary prints — something like "This request covers flight and hotel expenses for attending a Q4 sales conference." Exact wording varies each time; confirm it's a single sentence and it's actually about the request you described.

**FIX:** If you get an authentication error, confirm your Anthropic API key is set as an environment variable (`ANTHROPIC_API_KEY`) — never hardcoded into the script itself.

---

#### Screenshot 1 checkpoint (3:40–4:00)

**SAY:** "Screenshot 1 — the Python shell showing the AI-generated summary."

---

### PART 2 — Wire the Feature into app.py (4:00–7:50)

#### Step 4 — Add the AI feature UI to Tab 1

**SAY:** "Now into Streamlit — after the existing form fields on the Submit tab, not replacing them."

**DO:** Append inside `with tab1:` in `app.py`:
```python
    # AI summary feature
    description = st.text_area('Request description (for AI summary)')
    if description:
        if st.button('Generate AI Summary'):
            with st.spinner('Generating summary...'):
                from ai_feature import summarise_request
                ai_summary = summarise_request(category, description)

            # Required: disclosure label
            st.info(f'AI-generated summary (review before saving):\n\n{ai_summary}')
            st.caption('AI output generated by Claude. Review before saving.')

            # Required: human review gate
            if st.button('Looks good -- save with this summary'):
                add_record(requester, category, amount, notes=ai_summary)
                st.success('Record saved with AI summary.')
```

**CHECK:** Count the two required-control comments already in the code: `# Required: disclosure label` and `# Required: human review gate` — both should be present exactly as written, marking controls one and two.

---

#### Step 5 — The disclosure label and review gate, explained

**SAY:** "Two separate button clicks, on purpose. Clicking 'Generate AI Summary' only calls the API and shows the result — it never touches the database. The `st.info(...)` box is explicitly labeled 'AI-generated summary' and 'review before saving' — that's control one, disclosure. Only a *second*, distinct click on 'Looks good — save with this summary' actually calls `add_record`. A user can generate ten summaries, reject all of them, and never save a single AI-authored word — that's control two, human review, enforced by requiring two separate clicks rather than one."

---

#### Step 6 — Run the full flow

**DO:**
```bash
streamlit run app.py
```
On Tab 1: enter a description, click "Generate AI Summary," read the disclosure box, then click "Looks good — save with this summary."

**CHECK:** After Generate: a blue info box shows the AI summary with the disclosure caption underneath. After Save: a green "Record saved with AI summary" message appears. Switch to Tab 2 and confirm the new record's notes field contains the AI-generated text.

---

#### Screenshot 2 checkpoint (7:30–7:50)

**SAY:** "Screenshot 2 — Tab 1 showing the AI-generated summary with the disclosure label and review button visible."

---

### PART 3 — Write the Test and Update README (7:50–12:10)

#### Step 7 — Write the mocked API tests

**SAY:** "Control four: a test that exercises `summarise_request` without ever making a real network call to Anthropic's API."

**DO:** In `tests/test_ai_feature.py`:
```python
from unittest.mock import MagicMock, patch
from ai_feature import summarise_request


def test_summarise_returns_string():
    with patch('ai_feature.anthropic.Anthropic') as mock_client:
        mock_message = MagicMock()
        mock_message.content = [MagicMock(text='AI summary.')]
        mock_client.return_value.messages.create.return_value = mock_message

        result = summarise_request('Travel', 'Flight to Atlanta for client meeting')
        assert isinstance(result, str)
        assert len(result) > 0


def test_prompt_does_not_include_name():
    with patch('ai_feature.anthropic.Anthropic') as mock_client:
        mock_message = MagicMock()
        mock_message.content = [MagicMock(text='Short summary.')]
        mock_client.return_value.messages.create.return_value = mock_message

        result = summarise_request('Software', 'License renewal for design tools')
        assert 'Taylor' not in str(result)
        assert 'Jordan' not in str(result)
```

**CHECK:** Read `patch('ai_feature.anthropic.Anthropic')` out loud: "This replaces the real `anthropic.Anthropic` class, *inside the `ai_feature` module specifically*, with a fake object for the duration of the `with` block. `mock_client.return_value.messages.create.return_value = mock_message` says: whenever the code calls `client.messages.create(...)`, hand back this fake message instead of contacting the real API."

---

#### Step 8 — Why mocking matters here, explained

**SAY:** "Three reasons this test is mocked instead of real: speed — a real API call takes seconds, a mocked one takes milliseconds. Cost — every real call to a paid API costs money; running the test suite shouldn't. And determinism — a real AI response varies every time you ask, which makes `assert result == 'exact text'` impossible to write reliably. Mocking fixes all three at once."

---

#### Step 9 — Run pytest and confirm both pass

**DO:**
```bash
pytest -v
```

**CHECK:**
```
tests/test_ai_feature.py::test_summarise_returns_string PASSED
tests/test_ai_feature.py::test_prompt_does_not_include_name PASSED

======================== 2 passed in 0.02s ========================
```
Confirm this ran fast — well under a second — and that no API key or network access was needed, proof the mock actually intercepted the call.

---

#### Step 10 — Complete the README AI feature section

**SAY:** "Control five: documented limitations, in writing, in the repo."

**DO:** In `README.md`:
```markdown
## AI Feature

**What it does:** [one sentence]

**Controls implemented:**
- AI-generated content is labelled clearly in the UI
- Human review required before any AI output is saved
- No personally identifiable information is sent to the API

**Limitations:**
- [limitation 1]
- [limitation 2]

**AI use during development:**
[Describe honestly what AI tools you used and how]
```

**CHECK:** Write at least two real limitations, not placeholders — for example: "The summary quality depends on how detailed the user's description is" or "The API call adds a few seconds of latency to the submit flow, with no offline fallback."

---

### PART 4 — Final Submission Checklist and Presentations (12:10–16:00)

#### Step 11 — Walk the final checklist, item by item

**SAY:** "Before presenting, go through every single item out loud — skipping one here is how a working capstone loses easy points."

**DO/CHECK:** Confirm each:
- [ ] All 5 database functions pass tests (Week 14's five `pytest` tests)
- [ ] All 5 Streamlit features work end-to-end (Week 15's five tabs)
- [ ] GenAI feature shows disclosure label and human review button
- [ ] README complete with AI feature section and limitations
- [ ] `requirements.txt` current from `pip freeze`
- [ ] `.gitignore` includes `.venv/`, `__pycache__/`, `*.db`, `.env`
- [ ] `ruff format` and `ruff check` pass
- [ ] All tests pass
- [ ] Repository accessible to the instructor
- [ ] `screenshots/` folder has at least 2 images of the running app
- [ ] You can explain every file and every function without reading notes

**FIX:** If `.env` isn't already in `.gitignore`, add it now — that's the file where your real API key lives, and it must never be committed.

---

#### Step 12 — The final push

**DO:**
```bash
ruff format . && ruff check . && pytest -v
git add . && git commit -m 'lab 16: GenAI feature + final submission' && git push
```

**CHECK:** No lint errors, all tests pass (Week 14's five database tests plus these two AI tests, at minimum), push succeeds, commit message includes "lab 16."

---

#### Step 13 — Prepare the eight-topic demo

**SAY:** "Last thing before presenting — walk through all eight required topics once, out loud, right now, so nothing is a surprise in front of the instructor."

**DO/CHECK:** Rehearse each:
1. **Business problem + user workflow** — describe the problem, walk through a user session
2. **Developer workflow** — terminal: venv active, `ruff` passing, `pytest` green, `git log`
3. **OOP design** — walk through `models.py`: classes, attributes, methods
4. **SQL schema + key queries** — `CREATE TABLE`, a filter query, the `GROUP BY` report
5. **Streamlit demo** — live: submit, view, filter, update status, show report
6. **GenAI feature** — show the disclosure label, the review step, explain the prompt
7. **Testing + limitations** — `pytest` passing, name one real limitation
8. **AI use statement** — an honest account of what AI tools you used and how

**CHECK:** Time yourself running through all eight — if any single topic takes more than a minute or two, tighten it; the instructor will stop you if any topic is skipped entirely, so better to under-run than over-run.

---

### SUBMISSION CHECKLIST (16:00–end)

- [ ] Screenshot 1: AI feature in Tab 1 — summary visible with disclosure label and review button
- [ ] Screenshot 2: `pytest -v` showing all tests passing (including the mocked AI tests)
- [ ] `README.md` with the completed AI feature section
- [ ] `ai_feature.py` in the repo
- [ ] `tests/test_ai_feature.py` in the repo
- [ ] Git commit message includes "lab 16"
- [ ] GitHub repository URL pasted into Canvas
