"""Build ism3232/docs/capstone_rubric.html: the eight-part, 100-point capstone
rubric with four described tiers per part. verify_week13.py checks PARTS
against autograder/assignments/ism3232/capstone.yaml.

    python reference/ism3232/builders/capstone_rubric.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pagekit import DOCS, head_from
from week13_proposal import case_count, evaluation_total

OUT = DOCS / "capstone_rubric.html"

PARTS = [
    {
        "key": "proposal",
        "title": "Proposal",
        "weeks": "Week 13",
        "points": 10,
        "tiers": (10, 7, 4, 0),
        "full": "Every template section is specific and the eight-item checklist is met. Five "
        "sample conversations, each with a &ldquo;must&rdquo; in Week 16's terms, at least one "
        "of them a safety case. Signed off before any Week 14 code.",
        "most": "One section is vague, or one conversation has no &ldquo;must&rdquo;.",
        "some": "Several sections are vague, there are fewer than five conversations, or there "
        "was no sign-off before Week 14.",
        "missing": "No <code>PROPOSAL.md</code>.",
        "example": "Bayside's handoff rule names its words, <code>payment</code> and "
        "<code>card</code>, and says why: card details must never reach the model. Its fourth "
        "conversation is a safety case: an address change with no order ID must file 0 "
        "changes.",
        "issue": "&ldquo;Handoff: anything sensitive&rdquo; with no words, or a conversation "
        "nobody can check (&ldquo;the bot should be helpful&rdquo;).",
    },
    {
        "key": "database_layer",
        "title": "Database layer",
        "weeks": "Week 14",
        "points": 15,
        "tiers": (15, 10, 6, 0),
        "full": "Correct column types (<code>REAL</code> for money, <code>INTEGER</code> for "
        "counts), primary keys, and a <code>change_requests</code> table. Every function takes "
        "the database file as its first argument, uses <code>?</code> placeholders in every "
        "query, returns rows as dicts, and closes its connection. Database tests use "
        "<code>tmp_path</code>.",
        "most": "One of those is missing.",
        "some": "The functions work, but several of those are missing.",
        "missing": "No <code>database.py</code>, or the tables cannot be created.",
        "example": "Bayside's <code>approve_request(db_file, number)</code> runs two "
        "<code>UPDATE</code>s with <code>?</code> placeholders, commits, and closes the "
        "connection.",
        "issue": "An f-string inside a query, or tests that write to the real <code>.db</code> "
        "file.",
    },
    {
        "key": "tools_guardrails",
        "title": "Tools and guardrails",
        "weeks": "Weeks 12 and 14",
        "points": 20,
        "tiers": (20, 14, 8, 0),
        "full": "At least two lookup tools and one change tool, each with a docstring that has "
        "an <code>Args:</code> section. <code>run</code> refuses unknown tools, empty values, "
        "and details the customer never typed, matched as whole words. Change tools only file "
        "requests. The tool loop is capped, and the handoff rule runs before the model.",
        "most": "One of those is missing.",
        "some": "The tools run, but the checks in <code>run</code> are mostly missing, or a "
        "change tool edits data directly.",
        "missing": "No tools the model can ask for.",
        "example": "Bayside refuses a request for order <code>A1000</code> when the customer "
        "typed <code>A100</code>, because <code>customer_said</code> matches whole words.",
        "issue": "A substring check that finds <code>A100</code> inside <code>A1000</code>.",
    },
    {
        "key": "agent_models",
        "title": "Agent and models",
        "weeks": "Weeks 10–12",
        "points": 10,
        "tiers": (10, 7, 4, 0),
        "full": "The tools and the model are passed in. The history includes <code>tool</code> "
        "entries. A safe reply when the model is down. The keyword, fake and real models are "
        "interchangeable through <code>decide</code>.",
        "most": "One of those is missing.",
        "some": "It works with only one model.",
        "missing": "No agent class.",
        "example": "Bayside's <code>SupportChatbot(name, instructions, tools, model)</code> "
        "runs the same with <code>KeywordModel</code>, with <code>FakeModel</code> in the "
        "tests, and with <code>OllamaModel</code> in the demo.",
        "issue": "The model created inside the agent class, so tests cannot swap in a fake "
        "one.",
    },
    {
        "key": "streamlit_app",
        "title": "Streamlit app",
        "weeks": "Week 15",
        "points": 15,
        "tiers": (15, 10, 6, 0),
        "full": "The chat history is kept in <code>st.session_state</code> across reruns. "
        "Approve applies a change once and Reject changes nothing. A records table and a "
        "<code>GROUP BY</code> report. One edit form. A model switch. Customer text is shown "
        "safely.",
        "most": "One of those is missing.",
        "some": "The chat or the Staff tab is missing.",
        "missing": "The app does not start.",
        "example": "Bayside keeps its chatbot in <code>st.session_state.bot</code>, so the "
        "history survives every click, and shows staff rows with <code>st.text</code>, so a "
        "customer cannot format the page.",
        "issue": "The chatbot rebuilt on every rerun, or customer text rendered as Markdown.",
    },
    {
        "key": "evaluation_safety",
        "title": "Evaluation and safety",
        "weeks": "Week 16",
        "points": 10,
        "tiers": (10, 7, 4, 0),
        "full": "At least 8 cases, including the proposal's five and two safety cases, each run "
        "3 times. The README has the results table, the Week 16 safety-checklist findings and "
        "specific limitations. The checks still catch a wrong answer written another way.",
        "most": "One of those is missing.",
        "some": "Fewer than 8 cases, or no results in the README.",
        "missing": "No <code>evaluation.py</code>.",
        "example": f"Bayside runs {case_count()} cases three times each and reports "
        f"{evaluation_total()}, and its README explains the two failing cases.",
        "issue": '<code>never_says "11 pm"</code> passing on &ldquo;11:00 PM&rdquo;.',
    },
    {
        "key": "tests_workflow",
        "title": "Tests and workflow",
        "weeks": "Weeks 13–16",
        "points": 10,
        "tiers": (10, 7, 4, 0),
        "full": "<code>ruff</code> is clean. At least 15 tests across three files pass without "
        "Ollama or Streamlit installed. A real commit history across Weeks 13 to 16. README "
        "run steps.",
        "most": "One of those is missing.",
        "some": "Tests fail, or tests import <code>app.py</code> or <code>ollama_model.py</code>.",
        "missing": "No tests.",
        "example": "Bayside's tests live in <code>test_database.py</code>, "
        "<code>test_tools.py</code> and <code>test_agent.py</code>, and pass with "
        "<code>ollama</code> and <code>streamlit</code> blocked, the way the autograder runs "
        "them.",
        "issue": "A test that imports <code>app.py</code>, which the autograder cannot run.",
    },
    {
        "key": "live_demo",
        "title": "Live demo",
        "weeks": "Week 16",
        "points": 10,
        "tiers": (10, 7, 4, 0),
        "full": "The real model. One approval round trip. One evaluation failure explained. One "
        "file explained line by line. An AI-use statement in the README.",
        "most": "One of those is missing.",
        "some": "Only the keyword model, with no README note, or you cannot explain your own "
        "code.",
        "missing": "No demo.",
        "example": "Ask about A101, request an address change in the chat, approve it on the "
        "Staff tab, then explain why the closing-time case fails.",
        "issue": "A demo on a laptop that cannot run the model, with no borrowed machine and no "
        "note.",
    },
]

CHIP = (
    "font-family:var(--mono);font-size:11px;padding:4px 12px;border-radius:20px;"
    "background:var(--bg2);color:var(--muted);border:1px solid var(--border);"
)
CHIP_BLUE = (
    "font-family:var(--mono);font-size:11px;padding:4px 12px;border-radius:20px;"
    "background:var(--blue-dim);color:var(--blue);border:1px solid rgba(126,184,255,.25);"
)
ROW = "padding:9px 20px;border-bottom:1px solid var(--border);"


def header():
    return (
        '<div style="margin-bottom:32px;"><p style="font-family:var(--mono);font-size:10px;'
        'letter-spacing:.14em;text-transform:uppercase;color:var(--blue);margin-bottom:8px;">'
        'Unit 4 · Weeks 13–16</p><h1 style="font-size:28px;font-weight:700;'
        'letter-spacing:-.02em;margin-bottom:10px;">Capstone Rubric</h1><p>The capstone is '
        "graded in eight parts, each tied to the week that taught it. Every part has four "
        "tiers: Full, Most, Some and Missing, worth 100, 70, 40 and 0 percent of its points. "
        'Read this in Week 13 with the <a href="capstone_starters.html">capstone starters</a>, '
        "and check each part against your work before the final submission.</p>"
        '<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:14px;">'
        f'<span style="{CHIP_BLUE}">Capstone = 30% of final grade</span>'
        f'<span style="{CHIP}">Weeks 13–16</span>'
        f'<span style="{CHIP}">Live demo required</span></div></div>'
    )


def part_section(number, part):
    full, most, some, _ = part["tiers"]
    rows = (
        f'<tr><td class="rub-pts-full">{full}</td><td class="rub-req"><strong>Full.</strong> '
        f'{part["full"]}<div class="exemplar"><strong>✓ Full marks looks like</strong>'
        f'{part["example"]}</div><div class="concern"><strong>⚠ Common issue</strong>'
        f"{part['issue']}</div></td></tr>"
        f'<tr><td class="rub-pts-part">{most}</td><td class="rub-req"><strong>Most.</strong> '
        f"{part['most']}</td></tr>"
        f'<tr><td class="rub-pts-part">{some}</td><td class="rub-req"><strong>Some.</strong> '
        f"{part['some']}</td></tr>"
        '<tr><td class="rub-pts-none">0</td><td class="rub-req"><strong>Missing.</strong> '
        f"{part['missing']}</td></tr>"
    )
    return (
        f'<div class="rub-section"><div class="rub-head"><span class="rub-title">{number}. '
        f'{part["title"]} · {part["weeks"]}</span><span class="rub-weight">'
        f'{part["points"]} points</span></div><div class="rub-body"><table class="rub-table">'
        "<thead><tr><th>Points</th><th>Requirement</th></tr></thead>"
        f"<tbody>{rows}</tbody></table></div></div>"
    )


def demo_section():
    return (
        '<div class="rub-section"><div class="rub-head"><span class="rub-title">Demo rules '
        'and the AI-use statement</span><span class="rub-weight">Week 16</span></div>'
        '<div class="rub-body" style="padding:14px 20px;"><p>Run your app with the real model '
        "(<code>granite4.1:3b</code> on Ollama) and show: a question your agent answers with a "
        "tool; a change filed in the chat and approved on the Staff tab; one evaluation case "
        "that fails, and why; and one file explained line by line. A borrowed laptop or a lab "
        "machine is fine: say so in your README. If no machine can run the model, demo with "
        "the keyword model and explain in your README; Live demo then scores Some.</p>"
        "<p><strong>AI-use statement.</strong> End your README with which AI tools you used "
        "and what for. The course AI policy (syllabus, section 7) applies: AI may explain an "
        "error, explain code, or suggest test cases for code you wrote; it may not write the "
        "code you submit; and AI use you do not disclose is prohibited.</p></div></div>"
    )


def summary():
    rows = "".join(
        f'<tr><td style="{ROW}color:var(--text);">{part["title"]}</td>'
        f'<td style="{ROW}font-family:var(--mono);color:var(--blue);text-align:right;">'
        f"{part['points']} pts</td></tr>"
        for part in PARTS
    )
    total = sum(part["points"] for part in PARTS)
    return (
        '<div style="background:var(--bg2);border:1px solid var(--border);border-radius:12px;'
        'overflow:hidden;margin-bottom:32px;"><div style="padding:14px 20px;'
        "background:var(--bg3);border-bottom:1px solid var(--border);font-family:var(--mono);"
        "font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;"
        'color:var(--muted);">Score Summary</div><table style="width:100%;'
        f'border-collapse:collapse;font-size:13px;"><tbody>{rows}'
        '<tr style="background:var(--bg3);"><td style="padding:10px 20px;font-weight:700;'
        'color:var(--text);">Total</td><td style="padding:10px 20px;font-family:var(--mono);'
        f'font-weight:700;color:var(--blue);text-align:right;">{total} pts</td></tr>'
        "</tbody></table></div>"
    )


def build():
    text = OUT.read_text()
    tail = text[text.index('<script src="../site.js">') :]
    head = head_from("capstone_rubric.html", "ISM3232 Capstone Rubric")
    sections = "".join(part_section(n, part) for n, part in enumerate(PARTS, 1))
    wrapper = (
        '<div class="wrapper" id="main-content" role="main">'
        f"{header()}{sections}{demo_section()}{summary()}"
        '<div class="page-footer">ISM3232 · Capstone Rubric · Unit 4</div></div>'
    )
    page = f"{head}\n<body>\n{wrapper}\n{tail}"
    return page, []


if __name__ == "__main__":
    page, _ = build()
    OUT.write_text(page)
    print("wrote", OUT)
