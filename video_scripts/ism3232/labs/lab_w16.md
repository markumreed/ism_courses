# ISM3232 Lab W16: GenAI Feature & Final Demo

## YouTube Metadata

**Title:** GenAI Feature & Final Demo — Lab Walkthrough | ISM3232 Lab 16
**Description:**
Walkthrough of ISM3232 Module 16 Lab. We build ai_feature.py with the summarise_request function using the Anthropic SDK, wire it into app.py Tab 1 with a disclosure label and human review button, write two mocked pytest tests, complete the final capstone checklist, and prepare for the 8-topic demo presentation.

Course page: https://markumreed.github.io/ism3232/docs/week16_lab.html

**Chapters:**
0:00 — What this lab covers
0:45 — Six required AI controls and why they exist
2:30 — Building ai_feature.py: summarise_request
5:00 — Wiring the AI feature into Tab 1
7:00 — Two mocked pytest tests for the AI feature
8:30 — README.md AI feature section
9:00 — Final checklist and 8-topic demo preparation
10:00 — Submission

**Applies to:** ISM3232 Module 16

**Tags:** python anthropic SDK, python AI feature, python mock testing, streamlit AI integration, ISM3232, USF, python GenAI, python capstone

---

## Script

### INTRO (0:00–0:45)

Lab 16 — GenAI Feature and Final Demo. We add one AI feature to the Streamlit app, then present the complete system. There are six required AI controls. Missing any one fails the feature on the rubric — not just the AI component, the whole feature.

---

### SIX REQUIRED AI CONTROLS (0:45–2:30)

Every AI feature in a business system needs these six things. This is not ISM3232-specific — this is the industry standard for responsible AI integration:

1. **Disclosure label in the UI** — users must see "AI-generated content" before they can act on it
2. **Human review before save** — the user must click a separate "Save" button after reviewing the AI output
3. **No PII sent to the API** — check that request IDs, names, and dollar amounts don't appear in the prompt
4. **Test with mocked API** — the pytest suite must not make real API calls
5. **Limitations documented in README** — AI can be wrong; you must say so
6. **You can explain every line** — if the AI wrote it, you must annotate it

If you built the feature with AI assistance, add a comment to every line you didn't write yourself explaining what it does and why. This is not optional.

---

### BUILDING AI_FEATURE.PY (2:30–5:00)

```bash
cd ~/ism3232/module07_final_project
pip install anthropic
pip freeze > requirements.txt
touch ai_feature.py && code ai_feature.py
```

```python
# ai_feature.py
import anthropic


def summarise_request(category: str, amount: float, notes: str) -> str:
    """Return a one-sentence AI-generated approval recommendation.

    Args:
        category: The request category (Travel, Software, etc.)
        amount: The dollar amount — used as context, not as PII
        notes: The notes field from the request form

    Returns:
        A one-sentence recommendation string

    Note: No requester name or ID is sent to the API.
    """
    client = anthropic.Anthropic()

    prompt = (
        f"You are a business approval assistant. "
        f"A {category} request for ${amount:,.2f} has these notes: '{notes}'. "
        f"Provide one sentence recommending approval or further review, with a brief reason."
    )

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text
```

Notice what is NOT in the prompt: no requester name, no employee ID. The category and amount are context, not identifying information.

Test manually:
```python
>>> from ai_feature import summarise_request
>>> summarise_request("Travel", 1200, "Annual sales conference in Tampa")
>>> # Should return a one-sentence recommendation
```

Screenshot 1: Python shell showing the AI-generated summary.

---

### WIRING INTO APP.PY TAB 1 (5:00–7:00)

Add the AI feature section inside Tab 1, after the form but before the `if submitted:` block:

```python
with tab1:
    st.subheader("Submit a Request")
    with st.form("submit_form"):
        requester = st.text_input("Requester name")
        category  = st.selectbox("Category", ["Travel", "Software", "Equipment", "Training", "Other"])
        amount    = st.number_input("Amount ($)", min_value=0.01, step=0.01)
        notes     = st.text_area("Notes (optional)", height=80)
        submitted = st.form_submit_button("Submit Request")

    # AI summary feature — outside the form
    st.divider()
    st.subheader("AI Summary (optional)")
    ai_notes = st.text_area("Enter request description for AI review:", height=60, key="ai_notes")
    ai_category = st.selectbox("Category for AI review:", ["Travel", "Software", "Equipment", "Training", "Other"], key="ai_cat")
    ai_amount = st.number_input("Amount for AI review:", min_value=0.01, step=0.01, key="ai_amt")

    if st.button("Generate AI Summary"):
        if ai_notes:
            from ai_feature import summarise_request
            with st.spinner("Generating..."):
                summary = summarise_request(ai_category, ai_amount, ai_notes)

            # Required: disclosure label
            st.info("AI-generated content — review before using.")
            st.session_state["ai_summary"] = summary

    if "ai_summary" in st.session_state:
        st.write(st.session_state["ai_summary"])
        if st.button("Save AI Summary to Last Record"):
            records = get_all_records()
            if records:
                # Append AI summary to notes — human reviews before saving
                # (In a full app, you would re-submit with the summary appended)
                st.success("Reviewed and noted.")
            else:
                st.warning("No records yet — submit a request first.")
```

The critical UX pattern here: the AI output appears first, then a **separate** "Save" button. The user must read the disclosure label and actively choose to save — they cannot accidentally skip the review step.

Screenshot 2: Tab 1 showing AI summary with disclosure label and review button.

---

### TWO MOCKED PYTEST TESTS (7:00–8:30)

The tests must not make real API calls. Use `unittest.mock.patch` to replace the Anthropic client with a fake.

Create `tests/test_ai_feature.py`:

```python
from unittest.mock import MagicMock, patch
from ai_feature import summarise_request


def test_summarise_returns_text():
    with patch("ai_feature.anthropic.Anthropic") as mock_client:
        # Build the mock response chain
        mock_message        = MagicMock()
        mock_content_block  = MagicMock()
        mock_content_block.text = "Recommend approval — amount is within policy."
        mock_message.content    = [mock_content_block]
        mock_client.return_value.messages.create.return_value = mock_message

        result = summarise_request("Travel", 1200, "Annual sales conference")
        assert "Recommend" in result or len(result) > 0


def test_no_pii_in_prompt():
    """Verify that the requester name is NOT sent to the API."""
    with patch("ai_feature.anthropic.Anthropic") as mock_client:
        mock_message        = MagicMock()
        mock_content_block  = MagicMock()
        mock_content_block.text = "Approve."
        mock_message.content    = [mock_content_block]
        mock_client.return_value.messages.create.return_value = mock_message

        result = summarise_request("Travel", 1200, "Conference")

        # Inspect the actual prompt that was sent
        call_args = mock_client.return_value.messages.create.call_args
        messages_sent = call_args[1]["messages"]   # keyword arg
        prompt_text = messages_sent[0]["content"]

        # The requester name "Jordan" should NOT appear — we never pass it
        assert "Jordan" not in prompt_text
```

Run: `pytest -v` — both tests must pass without making any network requests.

Screenshot 3: `pytest -v` with all tests passing (including the two new AI tests).

---

### README.MD AI FEATURE SECTION (8:30–9:00)

Update `README.md` with this required section — fill in your actual limitations:

```markdown
## AI Feature

**What it does:** Generates a one-sentence approval recommendation from request notes.

**Model:** claude-haiku-4-5-20251001

### Required Controls
- AI-generated content is labelled clearly in the UI
- Human review is required before saving
- No PII (requester name, ID) is sent to the API
- Tests use mocked API — no network calls in the test suite
- Category and amount used as context only

### Limitations
- The model may suggest approval for amounts that exceed policy
- Recommendations are not binding — final approval remains with the manager
- AI output quality depends on the notes content; vague notes produce vague recommendations

### AI Use Statement
[Honest account: what AI tools did you use while building this project, and how?
Which parts did you write yourself? Which did you generate and then annotate?]
```

---

### FINAL CHECKLIST AND 8-TOPIC DEMO (9:00–10:30)

Work through every item before the demo:

- All 5 database functions pass tests
- All 5 Streamlit features work end-to-end
- GenAI feature shows disclosure label and human review button
- README.md has AI feature section with limitations
- `requirements.txt` current (`pip freeze > requirements.txt`)
- `.gitignore` includes `.venv/`, `__pycache__/`, `*.db`, `.env`
- `ruff format .` and `ruff check .` pass clean
- All tests pass
- Repository accessible to instructor
- `screenshots/` folder has at least 2 images of the running app
- You can explain every file and every function without reading notes

Final push:
```bash
ruff format . && ruff check . && pytest -v
git add . && git commit -m 'lab 16: GenAI feature + final submission' && git push
```

**8-Topic Demo — what to cover:**

| # | Topic | What to show |
|---|-------|--------------|
| 1 | Business problem + user workflow | Describe the problem, walk through a user session |
| 2 | Developer workflow | Terminal: venv active, ruff passing, pytest green, git log |
| 3 | OOP design | Walk through models.py: classes, attributes, methods |
| 4 | SQL schema + key queries | CREATE TABLE, a filter query, the GROUP BY report |
| 5 | Streamlit demo | Live: submit, view, filter, update, report |
| 6 | GenAI feature | Show disclosure label, review step, explain the prompt |
| 7 | Testing + limitations | pytest passing, name one known limitation |
| 8 | AI use statement | Honest account of what AI tools you used and how |

The instructor will stop you if you skip a topic.

---

### SUBMISSION CHECKLIST (10:30–11:00)

- `ai_feature.py` in repo
- `tests/test_ai_feature.py` in repo — both mocked tests passing
- `README.md` with completed AI feature section
- Screenshot 1: Tab 1 with AI summary, disclosure label, and review button
- Screenshot 2: `pytest -v` all tests green including the two AI tests
- Commit includes "lab 16", GitHub URL to Canvas
