# ISM2411 Interactive Course Map — Design Spec
**Date:** 2026-06-09
**Status:** Approved

---

## Goal

Add an interactive course map page to ISM2411 (Python for Business) that matches the visual pattern established by the ISM3232 course map, while fully integrating with ISM2411's existing design system (light/dark theme, JetBrains Mono font, site nav).

---

## Architecture

**File:** `ism2411/pages/course_map.html`

**External dependencies (same pattern as other ISM2411 pages):**
- `../assets/css/site.css` — nav styles and unit color variables (`--u1` through `--u5`)
- `../assets/js/site.js` — injects sticky nav and theme toggle

**Self-contained map CSS** inside `<style>` block — all layout, card, animation, and detail-panel styles live in the file. Theme overrides via `[data-theme="light"]` selectors.

**Nav integration:** One `<a>` added to the "Start Here" dropdown in `site.js`:
```
<a href="${pg}course_map.html">Course Map</a>
```
Positioned after "All Units Overview" in the Start Here menu.

---

## Layout

**Grid:** `grid-template-columns: 1fr 22px 1fr 22px 1fr 22px 1fr 22px 1fr`
- 5 unit cards alternating with 4 animated arrow columns
- `overflow: hidden` on the shell; cards fill available viewport height

**Unit card anatomy (per card):**
1. Left-edge accent bar (unit color, animates on hover/active)
2. Unit number badge — `UNIT 0N · Weeks X–Y` in monospace
3. Unit title — bold display text
4. Subtitle — week/module range tagline
5. Topic list — bullet dots, highlights in unit color
6. Unit note — italic, bottom of card

**Detail panel:** Slides open below the grid on click (same `max-height` transition as ISM3232). Four columns inside, each with a label and 4 bullet items. Border color matches active unit.

**Keyboard nav:** Keys `1`–`5` activate units; `Escape` closes.

**Animated arrows:** Shaft + arrowhead animate into view for all arrows preceding the active unit (visualises prerequisite chain).

---

## Theme

Dark (default):
- `--bg: #0a0a0f`, `--bg2: #111118`, `--text: #e8e8f0`, `--muted: #6b6b80`
- Unit colors from `site.css` `--u1` through `--u5`

Light override via `[data-theme="light"]`:
- `--bg: #f8f8fc`, `--bg2: #ffffff`, `--text: #1a1a2e`, `--muted: #5a5a70`
- Borders, shadows, and glow adjusted for legibility on light backgrounds

---

## Content

### Unit 1 — Foundations · Weeks 1–5 · Color: `--u1` (green)
**Topics (highlights starred):** \*command line\*, file system & paths, \*variables & data types\*, operators & expressions, \*conditionals\*, print() & input(), scripts & running Python

**Unit note:** "Unit 1 is not about code. It is about learning to think like a computer — and talk to one."

**Detail panel columns:**
- Hardware & OS: CPU/RAM/storage, file system tree, absolute vs relative paths, what Python actually is
- Command Line: cd · ls · mkdir · pwd, creating files, running scripts, .zshrc basics
- Python Basics: variables, str/int/float/bool, print() · input(), f-strings
- Logic: if · elif · else, comparison operators, logical ops (and/or/not), truth values

### Unit 2 — Control Flow & Structure · Weeks 6–8 + W9 · Color: `--u2` (blue)
**Topics (highlights starred):** \*for loops\*, while loops, \*functions & return\*, parameters & arguments, \*debugging & tracebacks\*, AI literacy framework, \*Git & GitHub\*

**Unit note:** "Week 9: midterm. Weeks 1–8 content. Open notes."

**Detail panel columns:**
- Loops: for loop anatomy, range(), while loops, accumulator pattern, loop + list
- Functions: def · parameters · return, type hints, scope & NameError, reusing logic
- Debugging: reading tracebacks, print() debugging, "Debug First Then Ask" framework, common error types
- Git & GitHub: git init/add/commit/push, meaningful messages, GitHub repo, 9-step ritual

### Unit 3 — Data Structures · Weeks 10–12 · Color: `--u3` (purple)
**Topics (highlights starred):** \*lists & indexing\*, slicing & methods, \*dictionaries\*, nested structures, \*CSV files\*, file paths, tuples

**Unit note:** "Lists become DataFrames in Unit 4. Dicts become the rows. The connection is direct."

**Detail panel columns:**
- Lists: create/index/slice, append/remove/sort, list comprehensions, len() · in
- Tuples: immutable sequences, when to use vs list, tuple unpacking, enumerate()
- Dictionaries: key-value pairs, .get() · .keys() · .values(), nested dicts, dict patterns
- Files & CSVs: open() · read/write modes, csv.reader / csv.writer, relative paths, with statement

### Unit 4 — pandas & Analysis · Weeks 13–15 · Color: `--u4` (gold)
**Topics (highlights starred):** \*DataFrames\*, .head()/.info()/.describe(), \*cleaning & dtypes\*, boolean indexing, \*groupby()\*, \*bar/line/histogram charts\*, matplotlib & Seaborn

**Unit note:** "pandas is the single most-used Python library in business analytics. Knowing it well is a job-market skill on its own."

**Detail panel columns:**
- DataFrames: pd.read_csv(), .head()/.tail()/.info(), column selection, .describe()
- Cleaning: missing values (.isna()), fillna()/dropna(), fix dtypes, rename columns, drop duplicates
- Aggregation: boolean indexing, .groupby() + .agg(), .sort_values(), .value_counts()
- Visualization: plt.show(), bar charts, line charts, histograms, Seaborn heatmaps, axis labels

### Unit 5 — Capstone · Week 16 · Color: `--u5` (pink)
**Topics (highlights starred):** \*retail sales dataset\*, \*3 business questions\*, \*end-to-end analysis\*, clean + explore + visualize + present, portfolio deliverable

**Unit note:** "There are no new concepts in Unit 5 — only integration. This is the deliverable you add to your portfolio."

**Detail panel columns:**
- Dataset: 5,000-row retail CSV, load & inspect, identify issues, cleaning plan
- Analysis: formulate business questions, filter/group/aggregate, answer with numbers
- Visuals: one chart per question, labeled axes, chart type matches question type
- Delivery: written findings with business context, 7-min presentation, GitHub portfolio

---

## Footer Thread Bar

Five segments, each with its unit color dot:

| Dot color | Text |
|-----------|------|
| `--u1` green | data types — every variable |
| `--u2` blue | control flow — every decision |
| `--u3` purple | data structures — every collection |
| `--u4` gold | pandas — the job-market skill |
| `--u5` pink | git log — your visible workflow |

---

## Files to Create / Modify

| Action | File |
|--------|------|
| Create | `ism2411/pages/course_map.html` |
| Modify | `ism2411/assets/js/site.js` — add Course Map link to Start Here dropdown |
