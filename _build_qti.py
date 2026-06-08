#!/usr/bin/env python3
"""Parse ISM2411 reading-page quizzes and emit Canvas-compatible QTI 1.2 ZIP files.

Output: quiz_exam_fa26/
  ism2411_quiz_w01.zip  …  ism2411_quiz_w15.zip   (14 module quizzes)
  ism2411_midterm.zip                              (modules 1–8 combined)
"""

import html
import io
import re
import zipfile
from html.parser import HTMLParser
from pathlib import Path

PAGES   = Path("/home/markumreed/Documents/ism_courses/ism2411/pages")
OUT     = Path("/home/markumreed/Documents/ism_courses/quiz_exam_fa26")
MODULES = [1,2,3,4,5,6,7,8,10,11,12,13,14,15]


# ── HTML parser ───────────────────────────────────────────────────────────────

class QuizParser(HTMLParser):
    """Extract quiz items from an ISM2411 reading page."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.items = []
        self._in_quiz   = False   # inside .quiz-item
        self._in_type   = False   # inside .quiz-q
        self._in_qtext  = False   # inside .quiz-question
        self._in_pre    = False   # inside <pre> at quiz-item level (code trace blocks)
        self._in_opt    = False   # inside .quiz-options li
        self._in_ans    = False   # inside .quiz-answer details div (after summary)
        self._skip_summary = False
        self._cur = None          # current item dict

    # helpers
    def _classes(self, attrs):
        return set(dict(attrs).get("class", "").split())

    def handle_starttag(self, tag, attrs):
        c = self._classes(attrs)

        if tag == "div" and "quiz-item" in c:
            self._in_quiz = True
            self._cur = {"type_label": "", "question": "", "options": [], "answer": ""}

        if not self._in_quiz or self._cur is None:
            return

        if tag == "div" and c == {"quiz-q"}:
            self._in_type = True
        if tag == "div" and "quiz-question" in c:
            self._in_qtext = True
        if tag == "li" and self._in_quiz:
            opt_ul = False  # li might be outside quiz-options — only track inside quiz-item
            self._in_opt = True
            self._cur["options"].append("")
        if tag == "details" and "quiz-answer" in c:
            self._in_ans = True
        if tag == "summary" and self._in_ans:
            self._skip_summary = True
        if tag == "pre" and self._in_quiz and not self._in_ans:
            self._in_pre = True
            self._cur["question"] += "<pre>"
        if tag == "code" and (self._in_qtext or self._in_pre):
            self._cur["question"] += "<code>"

    def handle_endtag(self, tag):
        if not self._in_quiz or self._cur is None:
            return

        if tag == "div":
            if self._in_type:
                self._in_type = False
            elif self._in_qtext:
                self._in_qtext = False
            elif self._in_ans:
                self._in_ans = False
                self.items.append(self._cur)
                self._cur = None
                self._in_quiz = False
        if tag == "li":
            self._in_opt = False
        if tag == "summary":
            self._skip_summary = False
        if tag == "pre" and self._in_pre:
            self._in_pre = False
            self._cur["question"] += "</pre>"
        if tag == "code" and (self._in_qtext or self._in_pre or self._cur is not None):
            if self._cur is not None:
                self._cur["question"] += "</code>"

    def handle_data(self, data):
        if not self._in_quiz or self._cur is None:
            return
        if self._skip_summary:
            return
        if self._in_type:
            self._cur["type_label"] += data
        elif self._in_qtext or self._in_pre:
            self._cur["question"] += data
        elif self._in_opt:
            self._cur["options"][-1] += data
        elif self._in_ans:
            self._cur["answer"] += data


def parse_quiz(path: Path) -> list[dict]:
    p = QuizParser()
    p.feed(path.read_text(encoding="utf-8"))
    return p.items


# ── answer matching ───────────────────────────────────────────────────────────

def _strip_explanation(text: str) -> str:
    """Remove '— explanation' suffixes Canvas adds as feedback in the HTML."""
    # strip leading/trailing whitespace, then cut at first " — " or " – "
    t = text.strip()
    for sep in [" — ", " -- ", " - "]:
        if sep in t:
            t = t[:t.index(sep)].strip()
            break
    return t


def _opt_text(raw: str) -> str:
    """Strip 'a) ' / 'b) ' etc. prefix from an option string."""
    return re.sub(r"^[a-dA-D]\)\s*", "", raw.strip())


def find_correct_ident(options: list[str], answer_raw: str) -> str | None:
    """Return the response_label ident ('A','B','C','D') for the correct option."""
    answer_clean = _strip_explanation(answer_raw).lower()
    labels = ["A", "B", "C", "D"]
    # exact match first
    for i, opt in enumerate(options):
        if _opt_text(opt).lower() == answer_clean:
            return labels[i]
    # partial / contains match
    for i, opt in enumerate(options):
        ot = _opt_text(opt).lower()
        if ot and (ot in answer_clean or answer_clean in ot):
            return labels[i]
    return None


# ── QTI XML builders ──────────────────────────────────────────────────────────

def _e(text: str) -> str:
    """XML-escape text for attribute / element content."""
    return html.escape(str(text), quote=True)


def _qtype(type_label: str) -> str:
    tl = type_label.lower()
    if "multiple choice" in tl:
        return "multiple_choice_question"
    if "true" in tl or "false" in tl:
        return "true_false_question"
    return "essay_question"


def item_xml(item: dict, idx: int, quiz_ident: str) -> str:
    qtype     = _qtype(item["type_label"])
    item_id   = f"{quiz_ident}_q{idx}"
    q_html    = item["question"].strip()
    answer    = item["answer"].strip()
    options   = item["options"]

    meta = f"""    <item ident="{item_id}" title="Q{idx}">
      <itemmetadata><qtimetadata>
        <qtimetadatafield><fieldlabel>question_type</fieldlabel>
          <fieldentry>{qtype}</fieldentry></qtimetadatafield>
        <qtimetadatafield><fieldlabel>points_possible</fieldlabel>
          <fieldentry>1</fieldentry></qtimetadatafield>
      </qtimetadata></itemmetadata>"""

    # ── presentation ──
    if qtype == "multiple_choice_question":
        labels  = ["A", "B", "C", "D"]
        choices = "\n".join(
            f'        <response_label ident="{labels[i]}">'
            f'<material><mattext texttype="text/html">{_e(_opt_text(o))}'
            f'</mattext></material></response_label>'
            for i, o in enumerate(options)
        )
        correct = find_correct_ident(options, answer) or "A"
        pres = f"""      <presentation>
        <material><mattext texttype="text/html">{_e(q_html)}</mattext></material>
        <response_lid ident="response1" rcardinality="Single">
          <render_choice>{choices}
          </render_choice>
        </response_lid>
      </presentation>
      <resprocessing>
        <outcomes><decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/></outcomes>
        <respcondition continue="No">
          <conditionvar><varequal respident="response1">{correct}</varequal></conditionvar>
          <setvar action="Set" varname="SCORE">100</setvar>
        </respcondition>
      </resprocessing>"""

    elif qtype == "true_false_question":
        ans_lower  = _strip_explanation(answer).lower()
        correct_tf = "true_choice" if "true" in ans_lower and "false" not in ans_lower[:4] else "false_choice"
        pres = f"""      <presentation>
        <material><mattext texttype="text/html">{_e(q_html)}</mattext></material>
        <response_lid ident="response1" rcardinality="Single">
          <render_choice>
            <response_label ident="true_choice"><material><mattext>True</mattext></material></response_label>
            <response_label ident="false_choice"><material><mattext>False</mattext></material></response_label>
          </render_choice>
        </response_lid>
      </presentation>
      <resprocessing>
        <outcomes><decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/></outcomes>
        <respcondition continue="No">
          <conditionvar><varequal respident="response1">{correct_tf}</varequal></conditionvar>
          <setvar action="Set" varname="SCORE">100</setvar>
        </respcondition>
      </resprocessing>"""

    else:  # essay_question (Short Answer / Code Trace)
        model_ans = _e(answer)
        pres = f"""      <presentation>
        <material><mattext texttype="text/html">{_e(q_html)}</mattext></material>
        <response_str ident="response1" rcardinality="Single">
          <render_fib><response_label ident="answer1" rshuffle="No"/></render_fib>
        </response_str>
      </presentation>
      <itemfeedback ident="general_fb" view="All">
        <flow_mat><material>
          <mattext texttype="text/html">Model answer: {model_ans}</mattext>
        </material></flow_mat>
      </itemfeedback>"""

    return f"{meta}\n{pres}\n    </item>"


def assessment_xml(ident: str, title: str, items: list[dict]) -> str:
    body = "\n".join(item_xml(it, i + 1, ident) for i, it in enumerate(items))
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2">
  <assessment ident="{ident}" title="{_e(title)}">
    <qtimetadata>
      <qtimetadatafield><fieldlabel>cc_maxattempts</fieldlabel>
        <fieldentry>1</fieldentry></qtimetadatafield>
    </qtimetadata>
    <section ident="root_section">
{body}
    </section>
  </assessment>
</questestinterop>"""


def manifest_xml(ident: str, filename: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="man_{ident}"
  xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1
    http://www.imsglobal.org/profile/cc/ccv1p1/ccv1p1_imscp_v1p2_v1p0.xsd">
  <metadata>
    <schema>IMS Content</schema>
    <schemaversion>1.1.3</schemaversion>
  </metadata>
  <organizations/>
  <resources>
    <resource identifier="{ident}" type="imsqti_xmlv1p2">
      <file href="{filename}"/>
    </resource>
  </resources>
</manifest>"""


def write_zip(out_path: Path, ident: str, title: str, items: list[dict]):
    assess = assessment_xml(ident, title, items)
    manif  = manifest_xml(ident, f"{ident}.xml")
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("imsmanifest.xml", manif)
        zf.writestr(f"{ident}.xml", assess)
    print(f"  {out_path.name}  ({len(items)} questions)")


# ── main ──────────────────────────────────────────────────────────────────────

# Module title map (for ISM2411)
MODULE_TITLES = {
    1:  "Computers, Files & the Python Environment",
    2:  "The Command Line & Your Environment",
    3:  "Variables, Data Types & F-Strings",
    4:  "Operators & Expressions",
    5:  "Conditionals",
    6:  "Loops",
    7:  "Functions & Debugging",
    8:  "Git, GitHub & the Submission Workflow",
    10: "Lists & Tuples",
    11: "Dictionaries",
    12: "Working with Files & CSVs",
    13: "Introduction to pandas",
    14: "Data Cleaning & Descriptive Statistics",
    15: "Aggregation, Grouping & Charts",
}

print("Building ISM2411 QTI files → quiz_exam_fa26/\n")

all_quiz_items = {}

for mod in MODULES:
    path  = PAGES / f"week{mod:02d}_reading.html"
    items = parse_quiz(path)
    all_quiz_items[mod] = items

    ident = f"ism2411_quiz_w{mod:02d}"
    title = f"ISM2411 Module {mod:02d} Quiz — {MODULE_TITLES[mod]}"
    write_zip(OUT / f"{ident}.zip", ident, title, items)

# Midterm: modules 1–8
midterm_items = []
for mod in [1,2,3,4,5,6,7,8]:
    for item in all_quiz_items[mod]:
        midterm_items.append(item)

write_zip(
    OUT / "ism2411_midterm.zip",
    "ism2411_midterm",
    "ISM2411 Midterm Exam — Modules 1–8",
    midterm_items,
)

print(f"\n  {len(MODULES)} ISM2411 module quizzes + 1 midterm")
print(f"  Midterm total: {len(midterm_items)} questions")

# ── ISM3232 ───────────────────────────────────────────────────────────────────

ISM3232_PAGES   = Path("/home/markumreed/Documents/ism_courses/ism3232/docs")
ISM3232_MODULES = [1,2,3,4,5,6,7,8,10,11,12,13,14,15,16]

ISM3232_TITLES = {
    1:  "Developer Mindset & First Setup",
    2:  "zsh Navigation & File Operations",
    3:  "Virtual Environments & Shell Customisation",
    4:  "Search Tools, the Submission Ritual & Git",
    5:  "Variables, Data Types & Operators",
    6:  "Conditionals, Loops & Dictionaries",
    7:  "Functions, Modules & pytest",
    8:  "Debugging, AI Literacy & Midterm Review",
    10: "OOP I — Classes & Objects",
    11: "OOP II — Composition, Inheritance & SQL Mapping",
    12: "OOP III — Applied Practice & Design",
    13: "Capstone Design & SQL Foundations",
    14: "Python + SQL Integration",
    15: "Streamlit Business Interface",
    16: "GenAI Feature & Final Demo",
}

print("\nBuilding ISM3232 QTI files → quiz_exam_fa26/\n")

ism3232_items = {}

for mod in ISM3232_MODULES:
    path  = ISM3232_PAGES / f"week{mod:02d}_reading.html"
    items = parse_quiz(path)
    ism3232_items[mod] = items

    ident = f"ism3232_quiz_w{mod:02d}"
    title = f"ISM3232 Module {mod:02d} Quiz — {ISM3232_TITLES[mod]}"
    write_zip(OUT / f"{ident}.zip", ident, title, items)

# ISM3232 midterm: modules 1–8
ism3232_mid = []
for mod in [1,2,3,4,5,6,7,8]:
    ism3232_mid.extend(ism3232_items[mod])

write_zip(
    OUT / "ism3232_midterm.zip",
    "ism3232_midterm",
    "ISM3232 Midterm Exam — Modules 1–8",
    ism3232_mid,
)

print(f"\n  {len(ISM3232_MODULES)} ISM3232 module quizzes + 1 midterm")
print(f"  Midterm total: {len(ism3232_mid)} questions")
print(f"\nDone. All QTI files written to quiz_exam_fa26/")
