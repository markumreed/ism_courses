# Technical guide: Colab, GitHub, pandas, and AI in ISM 2411

All programming in this course happens in **Google Colab**: Jupyter notebooks that run in your web browser, with nothing to install. You save your work from Colab into your own public **GitHub** repository and submit a **GitHub URL** in Canvas.

## 1. One-time setup

**Before the first class** (about 15 minutes):

1. **GitHub account.** Create a free account at [github.com](https://github.com) if you do not have one, and verify your email address. If GitHub asks you to turn on two-factor authentication, use an authenticator app and save the recovery codes somewhere safe.
2. **Privacy.** Everything in your repository is public. Your GitHub username does not have to be your real name, and you can leave your profile's Name and photo blank; Canvas already knows which submission is yours. Every save from Colab shows your profile name in the repository's history, so set it before Lab 1 (your picture → **Settings** → **Public profile**).
3. **Your course repository.** On GitHub, select **New repository**. Name it `ism2411`, choose **Public**, and check **Add a README file**. (Colab can save only into a repository that already has a file in it.)
4. **Google account.** Sign in to [Google Colab](https://colab.research.google.com) with a Google account. If one Google account won't open Colab, try another, such as a personal Gmail account.

**In the first class (Lab 1):**

5. **Connect Colab to GitHub.** Open Lab 1 from its Canvas link and choose **File → Save a copy in GitHub**. The first time, Colab asks you to authorize it with GitHub; accept. (If nothing appears, allow pop-ups for colab.research.google.com.) Pick `ism2411`, set the file path to `labs/lab01_setup.ipynb`, and select **OK**.

You never paste a password or token into a notebook. **Never put passwords, API keys, tokens, or personal information in your repository.**

## 2. How the course runs each week

- **One meeting a week**, in a large lecture hall. From Week 3 on, each meeting opens with a closed-book check on the previous week's material. Then come live coding, a short prediction game, and a code-along start on that week's lab.
- **In class, you answer polls and ask questions from your phone or laptop** in Poll Everywhere, at `pollev.com/[presenter name]`, signed in with your USF account. Your answers record your attendance and count toward participation (10% of the grade), for answering, not for being right. Questions go to the class Q&A, where a TA answers them; the most-upvoted ones go to the instructor.
- **Attendance:** missing more than four class meetings, for any reason, including illness, results in automatic failure of the course. Absences are logged from your Poll Everywhere sign-in; you do not need to report or explain them, and there are no exceptions. If you expect to miss four or more meetings, drop the course.
- **Everything is due Sunday at 11:59 p.m. Eastern Time** of its week: the lab, the DataCamp chapters and reading for the next meeting, and any case or checkpoint. The portfolio is the one exception: Monday, May 3.
- **Late work** receives a 25% grade reduction (25% of the possible points) for each calendar day it is late, subject to approved accommodations.
- **Labs** carry no points. A lab is **Complete** when you have run every cell and honestly tried every exercise, prediction, and written answer. A ✓ on every check is not required.
- **Checks** take about 15 minutes. Each covers the previous week's lecture, lab, and DataCamp chapters, and one question is a variant of an exercise in that week's lab. There are 12 checks, on Weeks 2–13; Week 14 has none.
- **Cases** are individual and graded. Each brief gives its release date, checkpoint (Case 1), and due date.

## 3. Working in Colab, step by step

| Step | What to do |
| --- | --- |
| Open | Click the **Open in Colab** link in Canvas. This opens the course's copy; nothing is yours until you save it. |
| Save right away | **File → Save a copy in GitHub** → `ism2411` → the path from section 4. Now you have your own copy. |
| Work | Run a cell with **Shift + Enter**. Save to GitHub again (same menu, same path) at the end of each session. Each save is a commit. |
| Come back later | Open **your** copy, not the Canvas link: **File → Open notebook → GitHub** → `ism2411` → your file. |
| Undo a bad save | On GitHub, open the file and select **History**. Copy the commit ID of the version you want, open `https://colab.research.google.com/github/<you>/ism2411/blob/<commit ID>/<path>`, and save it to the same path. Lab 5 practices this. |
| Finish | **Runtime → Restart session and run all**. Fix anything that fails, then save to GitHub one last time. |
| Submit | Paste the GitHub URL in Canvas (section 5). |

**Careful:** **Ctrl + S** (**Cmd + S** on a Mac) and **File → Save** save to Google Drive, not GitHub. Your grader sees only what is in GitHub.

**Keep outputs on.** Leave **Edit → Notebook settings → Omit code cell output** turned off, so your saved notebook shows that it ran.

## 4. Where each file goes in `ism2411`

| Work | Path in your repository |
| --- | --- |
| Labs | `labs/lab02_values_lists_dicts.ipynb` and so on (each lab gives its file name at the top) |
| Case notebook | `case1_sales/analysis.ipynb`, `case2_marketing/analysis.ipynb`, … |
| Case README | `case1_sales/README.md`, … (create it on GitHub; section 11) |

## 5. Submitting a GitHub URL

- **Labs:** after you save, Colab opens your notebook on GitHub in a new tab. Copy that page's address, for example `https://github.com/<you>/ism2411/blob/main/labs/lab02_values_lists_dicts.ipynb`.
- **Cases:** open `analysis.ipynb` on GitHub, select **⋯ → Copy permalink**, and submit that. A permalink includes your commit ID, so it points to exactly the version you submitted; later portfolio revisions don't change it. Create your case README *before* you copy the permalink.

Before submitting, open the URL in a private (incognito) browser window. If you can't see the file there, neither can your grader: check that the repository is public.

## 6. Loading data

Notebooks that use data set its location for you in the first code cell. The data lives in the course repository, so there is nothing to upload:

```python
import pandas as pd
DATA = "https://raw.githubusercontent.com/…"     # already filled in
df = pd.read_csv(f"{DATA}/sales_transactions.csv")
df.shape
```

If you get `HTTPError: 404`, the address was probably changed. Open the original Canvas link again and copy its setup cell.

## 7. Inspect before you analyze

These lines answer the first item on the verification checklist. Run them before you change anything.

```python
df.shape                      # rows, columns
df.info()                     # column names, types, non-missing counts
df.head(10)                   # first rows
df.isna().sum()               # missing values per column
df.duplicated().sum()         # exact duplicate rows
df["some_column"].value_counts(dropna=False)   # every distinct value, with counts
df.describe()                 # min, max, mean of numeric columns: look for impossible values
```

Every time you filter, clean, or join, print the row count before and after, and record the step in your notebook's cleaning table.

## 8. Use AI with CRIT

Every case requires Geoff Woods's CRIT process: **C**ontext, **R**ole, **I**nterview, **T**ask. Do the four steps in order, in one conversation.

| Step | What you write | Example |
| --- | --- | --- |
| **Context** | The business situation, the data (column names and types from `df.info()`, plus a few rows from `df.head()`), the constraints, and the outcome you need. | "Mangrove Outfitters is deciding … The data has these columns … The decision is limited to … I need a notebook that …" |
| **Role** | The expert you want the AI to act as. | "Act as a retail analytics manager who reviews analyst work before it goes to executives." |
| **Interview** | Ask the AI to ask you questions first, one at a time. | "Before writing any code, ask me up to five clarifying questions, one at a time. Wait for my answer each time." |
| **Task** | The specific analysis or code you want. | "Write pandas code that … Explain each step in a comment." |

- Paste the column information and a few rows, not the whole file.
- Ask the AI to explain any line you do not understand. You must be able to explain your code.
- When the AI suggests a cleaning step, ask what it changes and how many rows it affects, then check the count yourself.
- Keep notes as you go for the decision record: what you asked, accepted, corrected, and rejected.

A second AI answer is not verification. Section 10 lists checks that count.

## 9. Charts

```python
import seaborn as sns
import matplotlib.pyplot as plt

ax = sns.barplot(data=summary, x="category", y="value", errorbar=None)
ax.set_title("A title that states the finding")
ax.set_xlabel("Category")
ax.set_ylabel("Value (units)")
plt.xticks(rotation=30, ha="right")
plt.show()
```

- Seaborn's bar and line charts draw error bars by default. This course is descriptive, so turn them off with `errorbar=None`.
- Bar charts start at zero. Label both axes with units. A title should say what the chart shows, not just name the topic.

## 10. Verify independently

The checklist asks you to confirm at least three records and one aggregate *outside Python*:

1. Get the data: open the course repository's [cases folder](../), then your case's `data` folder. Click the CSV and select **Download raw file** (the download icon).
2. Open it in Google Sheets or Excel. Filter to the rows, then use `SUM`, `COUNTIF`, or a pivot table. For a single record, a hand calculation such as quantity × unit price also works.
3. In the checklist, put the record IDs, the outside value, and the notebook value side by side.

## 11. Your case README

On GitHub, open your `ism2411` repository and select **Add file → Create new file**. Name it `case1_sales/README.md` (use your case's folder). Copy in the [README template](README_template.md), fill it in, and select **Commit changes**.

For the **Open in Colab** badge, use this line with your GitHub username in place of `<you>` and your case's folder in place of `case1_sales`:

```markdown
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/<you>/ism2411/blob/main/case1_sales/analysis.ipynb)
```
