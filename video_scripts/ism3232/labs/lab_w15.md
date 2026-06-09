# ISM3232 Lab W15: Streamlit Business Interface

## YouTube Metadata

**Title:** Streamlit Business Interface — Lab Walkthrough | ISM3232 Lab 15
**Description:**
Walkthrough of ISM3232 Module 15 Lab. We build a complete five-tab Streamlit application wired to the database.py functions from Lab 14: Submit, View, Filter, Update, and Report tabs. Then adapt the UI to the student's capstone domain.

Course page: https://markumreed.github.io/ism3232/docs/week15_lab.html

**Chapters:**
0:00 — What we're building
0:45 — Install Streamlit and confirm the hello-world run
2:00 — Five-tab structure: st.tabs() overview
3:00 — Tab 1: Submit form with st.form and st.selectbox
5:00 — Tab 2: View all records as a dataframe
5:45 — Tab 3: Filter by status
6:30 — Tab 4: Update status
7:30 — Tab 5: Status report with metrics
8:45 — Adapting to your capstone domain
9:30 — Submission checklist

**Applies to:** ISM3232 Module 15

**Tags:** python streamlit tutorial, streamlit tabs, streamlit forms, streamlit dataframe, ISM3232, USF, python web app, streamlit business app

---

## Script

### INTRO (0:00–0:45)

Lab 15 — Streamlit Business Interface. We wire the five database functions from Lab 14 to a browser UI. Every feature must be connected to a real function from `database.py` — no mock data, no hardcoded lists. By the end of today, you will have a working full-stack Python application.

---

### INSTALL AND FIRST RUN (0:45–2:00)

```bash
cd ~/ism3232/module07_final_project
pip install streamlit
pip freeze > requirements.txt
touch app.py && code app.py
```

Start with a hello-world to confirm the environment:

```python
# app.py — hello world first
import streamlit as st
from database import create_table

create_table()
st.title("My Business Request Tracker")
st.write("Database connected.")
```

Run it:
```bash
streamlit run app.py
```

A browser tab opens at `http://localhost:8501`. Confirm you see the title.

Screenshot 1: browser showing the Streamlit hello page.

---

### FIVE-TAB STRUCTURE (2:00–3:00)

Replace `app.py` with the full application. `st.tabs()` takes a list of labels and returns one context manager per tab.

```python
import streamlit as st
import pandas as pd
from database import create_table, add_record, get_all_records, update_status, get_status_report

create_table()

st.title("Business Request Tracker")
st.caption("Module 7 Capstone — ISM3232")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Submit", "View", "Filter", "Update", "Report"])
```

Everything from here is inside one of those five `with tab` blocks.

---

### TAB 1: SUBMIT (3:00–5:00)

```python
with tab1:
    st.subheader("Submit a Request")
    with st.form("submit_form"):
        requester = st.text_input("Requester name")
        category  = st.selectbox("Category", ["Travel", "Software", "Equipment", "Training", "Other"])
        amount    = st.number_input("Amount ($)", min_value=0.01, step=0.01)
        notes     = st.text_area("Notes (optional)", height=80)
        submitted = st.form_submit_button("Submit Request")

    if submitted:
        if requester and amount > 0:
            add_record(requester, category, amount, notes)
            st.success(f"Request submitted for {requester} — ${amount:,.2f} [{category}]")
        else:
            st.error("Requester name and amount are required.")
```

`st.form()` batches all the inputs together so the app doesn't re-run on every keystroke — it only re-runs when the form submit button is pressed.

---

### TAB 2: VIEW (5:00–5:45)

```python
with tab2:
    st.subheader("All Requests")
    records = get_all_records()
    if records:
        df = pd.DataFrame(records)
        st.dataframe(df, use_container_width=True)
        st.caption(f"{len(records)} total requests")
    else:
        st.info("No requests yet.")
```

---

### TAB 3: FILTER (5:45–6:30)

```python
with tab3:
    st.subheader("Filter by Status")
    status_filter = st.selectbox("Show:", ["All", "Pending", "Approved", "Rejected"])
    records = get_all_records()
    if status_filter != "All":
        records = [r for r in records if r["status"] == status_filter]
    if records:
        st.dataframe(pd.DataFrame(records), use_container_width=True)
        st.caption(f"{len(records)} matching requests")
    else:
        st.info(f"No {status_filter} requests.")
```

---

### TAB 4: UPDATE STATUS (6:30–7:30)

```python
with tab4:
    st.subheader("Update Request Status")
    records = get_all_records()
    if records:
        options = {f"#{r['id']} — {r['requester']} ${r['amount']:,.2f} [{r['status']}]": r['id']
                   for r in records}
        selected_label = st.selectbox("Select request:", list(options.keys()))
        new_status = st.selectbox("New status:", ["Pending", "Approved", "Rejected"])
        if st.button("Update Status"):
            update_status(options[selected_label], new_status)
            st.success(f"Status updated to {new_status}.")
            st.rerun()
    else:
        st.info("No requests yet.")
```

`st.rerun()` forces the app to refresh — otherwise the old status stays visible in the selectbox after the update.

---

### TAB 5: REPORT (7:30–8:45)

```python
with tab5:
    st.subheader("Status Report")
    report = get_status_report()
    if report:
        cols = st.columns(len(report))
        for col, row in zip(cols, report):
            col.metric(
                label=row["status"],
                value=f"{row['count']} requests",
                delta=f"${row['total']:,.2f}"
            )
        st.divider()
        df_report = pd.DataFrame(report)
        st.dataframe(df_report, use_container_width=True)
    else:
        st.info("No data yet.")
```

---

### TESTING EVERY TAB (8:45–9:30)

Run `streamlit run app.py` and test in order:

1. **Tab 1**: Submit three records — one under $500, one $500–$2000, one over $2000. Confirm the success message appears.
2. **Tab 2**: Confirm all three records appear.
3. **Tab 3**: Filter by "Pending" — count should be 3. Filter by "Approved" — should show 0.
4. **Tab 4**: Select the first record, change to "Approved". Switch to Tab 3, filter "Approved" — should show 1.
5. **Tab 5**: Confirm metrics show correct counts and totals for each status.

Screenshot 2: Tab 1 after a successful submission.
Screenshot 3: Tab 4 after updating a status.
Screenshot 4: Tab 5 showing metrics with real data.

---

### ADAPT TO YOUR CAPSTONE DOMAIN (9:30–10:00)

Update these four things to match your proposal:
- `st.title()` — change to your system name
- Category selectbox options — change to your domain categories
- Column display names in Tab 2 — ensure they match your schema
- Status options in Tabs 3 and 4 — change if your system uses different statuses

Stop Streamlit (`Ctrl+C`), save changes, run again to confirm.

---

### SUBMISSION CHECKLIST (10:00–11:00)

Ritual:
```bash
ruff format . && ruff check .
git add . && git commit -m 'lab 15: Streamlit five-feature interface' && git push
```

- All five tabs working end-to-end with real database calls
- Categories and title adapted to capstone domain
- `requirements.txt` updated (`pip freeze > requirements.txt`)
- Screenshot 1: browser showing the hello page (early)
- Screenshot 2: Tab 1 after a successful submission
- Screenshot 3: Tab 4 after updating a status
- Screenshot 4: Tab 5 showing status metrics with real data
- Commit includes "lab 15", GitHub URL to Canvas
