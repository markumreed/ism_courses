# Video Thumbnails — v2 (punchy, with topic icons)

33 YouTube thumbnails for the two-part course *Python for Business: From First
Line of Code to a Shipped Application*. This is the **punchy** set: a large
accent badge holding a white per-topic vector icon, a bigger headline, and an
accent-tinted background.

For the minimal variant (code motif + sequence number), see [`../thumbnails/`](../thumbnails/).

## Specs
- **Size:** 1280×720 px (YouTube standard), rendered at 2× and downsampled (Lanczos) for crisp edges
- **Background:** dark ink `#14141d`, tinted ~12% toward the topic accent
- **Badge:** rounded accent square with a white icon (vector-drawn, or a bold glyph such as `>_`, `{ }`, `$`)
- **Font:** DejaVu Sans (Bold for headlines, Mono for eyebrow/footer)
- **Naming:** `NN_slug.png`, where `NN` is the video's order in the course (01–33)
- **Accent colors** keyed to topic — green, blue, purple, rose, teal, indigo, gold
- **No course codes** appear on the art; the footer reads `PYTHON FOR BUSINESS · PART 1/2`

## Regenerate
```bash
python3 ppt/_make_thumbnails_v2.py
```
Icons, headlines, accents, and the icon→video mapping all live in the `VIDEOS`
table in [`../_make_thumbnails_v2.py`](../_make_thumbnails_v2.py). To add an icon,
add a branch to `draw_icon()`. Output overwrites this folder.

## Contents
| # | File | Headline | Topic | Accent | Part | Icon |
|---|---|---|---|---|---|---|
| 01 | `01_variables_data_types.png` | Variables & Data Types | PYTHON / FOUNDATIONS | green | 1 | `braces` |
| 02 | `02_python_operators.png` | Python Operators | PYTHON / OPERATORS | blue | 1 | `ops` |
| 03 | `03_fstrings_formatting.png` | f-strings & Formatting | PYTHON / OUTPUT | blue | 1 | `fmt` |
| 04 | `04_if_elif_else.png` | if / elif / else | PYTHON / LOGIC | blue | 1 | `branch` |
| 05 | `05_for_loops.png` | Python for Loops | PYTHON / ITERATION | green | 1 | `loop` |
| 06 | `06_dictionaries.png` | Python Dictionaries | PYTHON / DATA | purple | 1 | `braces` |
| 07 | `07_functions.png` | Python Functions | PYTHON / FUNCTIONS | green | 1 | `func` |
| 08 | `08_reading_tracebacks.png` | Reading Tracebacks | PYTHON / DEBUGGING | rose | 1 | `bug` |
| 09 | `09_terminal_basics.png` | Terminal Basics | COMMAND LINE | teal | 1 | `prompt` |
| 10 | `10_git_basics.png` | Git Basics | VERSION CONTROL | teal | 1 | `git` |
| 11 | `11_github_workflow.png` | GitHub Workflow | VERSION CONTROL | teal | 1 | `git` |
| 12 | `12_coding_with_ai.png` | Coding with AI | AI / BEST PRACTICES | gold | 1 | `ai` |
| 13 | `13_cpu_ram_storage.png` | CPU, RAM & Storage | HOW CODE RUNS | indigo | 1 | `chip` |
| 14 | `14_python_setup.png` | Python Setup | ENVIRONMENT | teal | 1 | `gear` |
| 15 | `15_lists_tuples.png` | Lists & Tuples | PYTHON / DATA | purple | 1 | `brackets` |
| 16 | `16_csv_file_io.png` | CSV File I/O | DATA PIPELINES | blue | 1 | `table` |
| 17 | `17_pandas_basics.png` | pandas Basics | DATA ANALYSIS | gold | 1 | `chart` |
| 18 | `18_data_cleaning.png` | Data Cleaning | DATA ANALYSIS | gold | 1 | `funnel` |
| 19 | `19_groupby_charts.png` | groupby & Charts | DATA ANALYSIS | gold | 1 | `chart` |
| 20 | `20_data_project.png` | Data Analysis Project | CAPSTONE | gold | 1 | `flag` |
| 21 | `21_dev_environment.png` | Dev Environment | SETUP | teal | 2 | `gear` |
| 22 | `22_advanced_shell.png` | Advanced Shell Tools | COMMAND LINE | teal | 2 | `prompt` |
| 23 | `23_virtual_environments.png` | Virtual Environments | WORKFLOW | teal | 2 | `cube` |
| 24 | `24_code_checklist.png` | Code Checklist | WORKFLOW | indigo | 2 | `check` |
| 25 | `25_while_loops.png` | while Loops | CONTROL FLOW | blue | 2 | `loop` |
| 26 | `26_testing_pytest.png` | Testing with pytest | TESTING | indigo | 2 | `check` |
| 27 | `27_classes_oop.png` | Classes & OOP | OOP / PART 1 | rose | 2 | `blueprint` |
| 28 | `28_composition_inheritance.png` | Composition & Inheritance | OOP / PART 2 | rose | 2 | `blueprint` |
| 29 | `29_oop_design.png` | OOP Design | OOP / PART 3 | rose | 2 | `blueprint` |
| 30 | `30_sql_sqlite.png` | SQL & SQLite | DATABASES | teal | 2 | `database` |
| 31 | `31_python_sqlite.png` | Python + SQLite | DATABASES | teal | 2 | `database` |
| 32 | `32_streamlit_app.png` | Streamlit Web App | WEB UI | indigo | 2 | `browser` |
| 33 | `33_ai_feature.png` | AI Feature | GENERATIVE AI | gold | 2 | `ai` |

> Videos 01–20 make up **Part 1** (Python foundations & data analysis); 21–33 make up **Part 2** (building business applications). The 12 shared foundational videos are sequenced into Part 1.
