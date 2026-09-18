# ISM3232 Lab W15: Streamlit Business Interface

## YouTube Metadata

**Title:** Streamlit Business Interface — Full Lab Walkthrough | ISM3232 Lab 15
**Description:**
Step-by-step, test-as-you-go walkthrough of ISM3232 Module 15 Lab. Install Streamlit, confirm a hello-world app runs, build all five required tabs — Submit, View, Filter, Update, Report — wired to the Week 14 database.py functions, test every tab with real submitted data, then adapt it to your own capstone domain and push.

Course page: https://markumreed.github.io/ism3232/docs/week15_lab.html

**Chapters:**
0:00 — What this lab covers — five tabs, one database
0:40 — Step 1: install streamlit and freeze requirements
1:20 — Step 2: write and run the hello-world app
2:20 — Screenshot 1 checkpoint
2:40 — Step 3: page config, imports, and the five tabs
3:40 — Step 4: build Tab 1 — Submit
5:00 — Step 5: build Tab 2 — View
5:50 — Step 6: build Tab 3 — Filter
7:00 — Step 7: build Tab 4 — Update
8:40 — Step 8: build Tab 5 — Report
9:50 — Step 9: run the full app for the first time
10:20 — Step 10: submit three test records on Tab 1
11:40 — Screenshot 2 checkpoint
12:00 — Step 11: verify Tab 2 and Tab 3
13:00 — Step 12: update a status on Tab 4, confirm on Tab 3
14:00 — Screenshot 3 checkpoint
14:20 — Step 13: verify Tab 5's metrics
15:00 — Screenshot 4 checkpoint
15:20 — Step 14: adapt the app to your own capstone domain
16:20 — Step 15: stop Streamlit and run the ritual
17:00 — Submission checklist

**Applies to:** ISM3232 Module 15

**Tags:** streamlit tutorial python, streamlit tabs dataframe, streamlit sqlite integration, streamlit selectbox button, ISM3232, USF, streamlit business app tutorial

---

## How to Use This Script

**SAY** it, **DO** it, **CHECK** the exact output, **FIX** it if it doesn't match — then move to the next step.

---

## Script

### INTRO (0:00–0:40)

**SAY:** "Lab 15 — the Streamlit business interface. Five required features, five tabs, every one of them wired directly to the `database.py` functions from Week 14 — nothing here talks to the database on its own; it's all going through `create_table`, `add_record`, `get_all_records`, `update_status`, `get_status_report`. One note: the last part of today's class covers FastAPI and REST APIs conceptually — there's no FastAPI deliverable, that lecture is awareness only."

---

### PART 1 — Install Streamlit and First Run (0:40–2:40)

#### Step 1 — Install and freeze

**DO:**
```bash
cd ~/ism3232/module07_final_project
source .venv/bin/activate
pip install streamlit
pip freeze > requirements.txt
touch app.py
code app.py
```

**CHECK:** `requirements.txt` now lists `streamlit` alongside `pytest` and `ruff` from previous weeks.

---

#### Step 2 — Hello-world app

**SAY:** "Before wiring anything to the database, confirm Streamlit itself actually runs."

**DO:**
```python
import streamlit as st

st.title('Hello from Streamlit!')
st.write('Database connected.')
```
```bash
streamlit run app.py
```

**CHECK:** A browser tab opens automatically at `http://localhost:8501`, showing "Hello from Streamlit!" as a large title and "Database connected." underneath.

**FIX:** If the browser doesn't open automatically, copy the `Local URL:` line from the terminal output and paste it into Chrome manually.

---

#### Screenshot 1 checkpoint (2:20–2:40)

**SAY:** "Screenshot 1 — the browser showing the Streamlit hello page."

---

### PART 2 — Build the Complete app.py (2:40–9:50)

#### Step 3 — Imports, page config, and the five tabs

**SAY:** "Replace the hello-world entirely. First: imports, table setup, page config, and the tab structure itself — before any content goes inside them."

**DO:**
```python
import streamlit as st
from database import create_table, add_record, get_all_records, update_status, get_status_report

create_table()
st.set_page_config(page_title='Request Tracker', layout='wide')
st.title('Business Request Tracker')

tab1, tab2, tab3, tab4, tab5 = st.tabs(['Submit', 'View', 'Filter', 'Update', 'Report'])
```

**CHECK:** Read it out loud: "`create_table()` runs every time the app starts — safe, because it's `CREATE TABLE IF NOT EXISTS` under the hood. `st.tabs([...])` returns five separate tab objects — everything for Tab 1 goes inside a `with tab1:` block, Tab 2 inside `with tab2:`, and so on."

---

#### Step 4 — Build Tab 1 — Submit

**SAY:** "A form: text input, a category dropdown, a number input, an optional notes box, and a submit button that validates before writing to the database."

**DO:**
```python
with tab1:
    st.header('Submit a New Request')
    requester = st.text_input('Your name')
    category  = st.selectbox('Category', ['Travel', 'Equipment', 'Software', 'Other'])
    amount    = st.number_input('Amount ($)', min_value=0.0, step=10.0)
    notes     = st.text_area('Notes (optional)')
    if st.button('Submit Request'):
        if requester and amount > 0:
            add_record(requester, category, amount, notes)
            st.success(f'Request submitted for {requester}')
        else:
            st.error('Name and amount are required.')
```

**CHECK:** Say out loud what the validation does: "Clicking Submit with an empty name or a zero amount shows a red error and does **not** call `add_record` — the database only gets written to when both conditions pass."

---

#### Step 5 — Build Tab 2 — View

**SAY:** "The simplest tab — pull every record and display it as a table."

**DO:**
```python
with tab2:
    st.header('All Requests')
    records = get_all_records()
    if records:
        st.dataframe(records, use_container_width=True)
    else:
        st.info('No records yet.')
```

**CHECK:** Note the `if records:` guard — an empty list is falsy in Python, so a brand-new database with zero rows shows a friendly "No records yet." message instead of an empty, confusing table.

---

#### Step 6 — Build Tab 3 — Filter

**SAY:** "Same data as Tab 2, but filtered in Python after it comes back from the database."

**DO:**
```python
with tab3:
    st.header('Filter Requests')
    status_filter = st.selectbox('Filter by status', ['All', 'Pending', 'Approved', 'Rejected'])
    records = get_all_records()
    if status_filter != 'All':
        records = [r for r in records if r['status'] == status_filter]
    st.dataframe(records, use_container_width=True)
    st.caption(f'{len(records)} record(s) shown')
```

**CHECK:** Read the filter line out loud: "This is the exact same list-comprehension filtering pattern from Week 6 and Week 11 — `[r for r in records if r['status'] == status_filter]` — just triggered by a dropdown instead of hardcoded in a script."

---

#### Step 7 — Build Tab 4 — Update

**SAY:** "The trickiest tab — a dropdown needs to show something human-readable, like a name and amount, while still knowing the underlying record `id` to update."

**DO:**
```python
with tab4:
    st.header('Update Request Status')
    records = get_all_records()
    if records:
        options = {f"ID {r['id']}: {r['requester']} - ${r['amount']:,.2f}": r['id'] for r in records}
        selected = st.selectbox('Select request', list(options.keys()))
        new_status = st.selectbox('New status', ['Pending', 'Approved', 'Rejected'])
        if st.button('Update Status'):
            update_status(options[selected], new_status)
            st.success(f'Updated to {new_status}')
    else:
        st.info('No records yet.')
```

**CHECK:** Trace the `options` dict out loud: "It's a dict comprehension — each key is a formatted display string like `'ID 3: Morgan - $3,500.00'`, and each value is the plain integer `id`. The dropdown shows the readable key; when you click Update, `options[selected]` looks up the actual `id` behind whichever label the user picked."

---

#### Step 8 — Build Tab 5 — Report

**SAY:** "Last tab — the aggregate report from `get_status_report()`, rendered as Streamlit metric widgets instead of printed text."

**DO:**
```python
with tab5:
    st.header('Status Report')
    report = get_status_report()
    if report:
        for row in report:
            col1, col2 = st.columns(2)
            col1.metric(row[0], row[1], 'requests')
            col2.metric('Total', f'${row[2]:,.2f}')
    else:
        st.info('No data yet.')
```

**CHECK:** Recall from Week 14 that `get_status_report()` returns plain tuples, not dicts — that's why this loop uses `row[0]`, `row[1]`, `row[2]` (status, count, total) instead of dict keys, unlike Tabs 2 and 3 which use `r['status']` on `get_all_records()`'s dict results.

---

### PART 3 — Test Every Feature (9:50–15:20)

#### Step 9 — Run the full app

**DO:**
```bash
streamlit run app.py
```

**CHECK:** Browser refreshes (or reopens) showing "Business Request Tracker" as the title and five tabs — Submit, View, Filter, Update, Report — across the top.

---

#### Step 10 — Submit three test records

**SAY:** "Three records, deliberately spanning different amount ranges, so later filtering and reporting have something real to show."

**DO:** On Tab 1, submit three requests:
- Name: `Taylor`, Category: `Travel`, Amount: `89` (under $500)
- Name: `Jordan`, Category: `Equipment`, Amount: `1200` (between $500–$2000)
- Name: `Morgan`, Category: `Software`, Amount: `3500` (over $2000)

**CHECK:** After each submission, a green success message appears: "Request submitted for Taylor," then "...for Jordan," then "...for Morgan."

---

#### Screenshot 2 checkpoint (11:40–12:00)

**SAY:** "Screenshot 2 — Tab 1 right after a successful submission."

---

#### Step 11 — Verify Tab 2 and Tab 3

**DO:** Click Tab 2, then Tab 3.

**CHECK:** Tab 2 shows all three records — Taylor, Jordan, Morgan — each with status `Pending`. On Tab 3, select `Pending` from the filter dropdown — the caption reads "3 record(s) shown," since none have been updated yet. Switch back to `All` to restore the full view.

---

#### Step 12 — Update a status on Tab 4

**DO:** On Tab 4, select the first request in the dropdown, choose `Approved` as the new status, click Update Status. Then switch to Tab 3 and filter by `Approved`.

**CHECK:** Tab 4 shows a green "Updated to Approved" message. Back on Tab 3, filtering by `Approved` now shows exactly 1 record, and filtering by `Pending` shows exactly 2 — confirming the update actually persisted to the database rather than just changing something on-screen.

---

#### Screenshot 3 checkpoint (14:00–14:20)

**SAY:** "Screenshot 3 — Tab 4 right after updating a status."

---

#### Step 13 — Verify Tab 5's metrics

**DO:** Click Tab 5.

**CHECK:** Two metric groups appear — one for `Approved` showing a count of 1 and a total matching whichever record you approved, one for `Pending` showing a count of 2 and the combined total of the other two records. Confirm the numbers add up: total approved plus total pending equals the sum of all three amounts you entered in Step 10.

---

#### Screenshot 4 checkpoint (15:00–15:20)

**SAY:** "Screenshot 4 — Tab 5 showing the status report metrics with real data."

---

### PART 4 — Adapt to Your Capstone Domain (15:20–16:20)

#### Step 14 — Customize for your own domain

**SAY:** "Everything above used a generic 'business request' example — now make it yours, matching the proposal from Week 13."

**DO:** Update:
- `st.title(...)` — your system's actual name
- The category `selectbox` options — your domain's real categories, not `Travel`/`Equipment`/`Software`
- Column names shown in the dataframe — must match your own `schema.sql` from Week 13
- The status options — if your system uses different status values than `Pending`/`Approved`/`Rejected`

**CHECK:** Re-run the full Part 3 test sequence — submit, view, filter, update, report — against your *customized* version, end to end, before moving on.

---

### PART 5 — Run the Ritual and Push (16:20–17:00)

#### Step 15 — Stop Streamlit and run the ritual

**SAY:** "Streamlit runs as a live server — stop it before running the ritual, since `ruff` and Git don't need it running."

**DO:** In the terminal running Streamlit, press `Ctrl+C`. Then:
```bash
ruff format . && ruff check .
git add . && git commit -m 'lab 15: Streamlit five-feature interface' && git push
```

**CHECK:** No lint errors, push succeeds, commit message includes "lab 15." (No `pytest` step this week — Streamlit's UI code isn't unit-tested directly; Week 14's `database.py` tests still cover the underlying logic.)

---

### SUBMISSION CHECKLIST (17:00–end)

- [ ] Screenshot 1: Tab 1 (Submit) showing a successful submission
- [ ] Screenshot 2: Tab 4 (Update) after changing a status
- [ ] Screenshot 3: Tab 5 (Report) showing the status metrics with real data
- [ ] All five tabs — Submit, View, Filter, Update, Report — working end to end
- [ ] `app.py` adapted to your own capstone domain (title, categories, columns, statuses)
- [ ] Git commit message includes "lab 15"
- [ ] GitHub repository URL pasted into Canvas
