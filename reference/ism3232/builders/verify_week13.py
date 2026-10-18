"""Check the Week 13 pages and the two capstone pages without changing them.

Each page on disk must be exactly what its builder makes now. Every code block
must appear verbatim in schema.sql, a saved sqlite3 transcript, or text a
builder derived. The lab's expected boxes must be real output. Exercise answers
stay inside the lab's answer keys. The quiz must import cleanly. The rubric
must match the autograder config. Every saved session must print the same
thing when sqlite3 runs it again.

    SQLITE3_CLI=<checked sqlite3> python reference/ism3232/builders/verify_week13.py
"""

import html
import importlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import week13_common as w
from pagekit import DOCS, ROOT, check_listings

PAGES = [
    "week13_reading",
    "week13_lecture",
    "week13_slides",
    "week13_lab",
    "week13_lab_slides",
    "capstone_starters",
    "capstone_rubric",
]
CONFIG = ROOT / "autograder" / "assignments" / "ism3232" / "capstone.yaml"


def plain(text):
    return html.unescape(re.sub(r"<[^>]+>", "", text))


def answer_leaks(name, text, answers=w.ANSWERS):
    """Answers shown where they should not be. The lab may show them only inside
    its click-to-reveal keys; the lab slides may show them anywhere."""
    if name == "week13_lab_slides":
        return []
    if name == "week13_lab":
        text = re.sub(r"<details.*?</details>", "", text, flags=re.DOTALL)
    shown = plain(text)
    return [answer for answer in answers if answer in shown]


def expected_misses(text, pool):
    """Expected-output boxes whose text is in no saved transcript."""
    boxes = re.findall(r'<div class="expected"[^>]*>(.*?)</div>', text, re.DOTALL)
    return [plain(box)[:60] for box in boxes if plain(box) not in pool]


def qti_functions():
    """parse_quiz and find_correct_ident from _build_qti.py, without running the
    part of that script that writes the quiz zips."""
    source = (ROOT / "_build_qti.py").read_text()
    namespace = {"__name__": "qti_definitions", "__file__": str(ROOT / "_build_qti.py")}
    definitions = compile(source[: source.index("# ── main")], "_build_qti.py", "exec")
    exec(definitions, namespace)  # noqa: S102 - the repo's own quiz builder
    return namespace["parse_quiz"], namespace["find_correct_ident"]


def quiz_problems(path, count=10):
    parse_quiz, find_correct_ident = qti_functions()
    items = parse_quiz(Path(path))
    problems = (
        [] if len(items) == count else [f"{len(items)} quiz items, expected {count}"]
    )
    for number, item in enumerate(items, 1):
        label = item["type_label"].lower()
        answer = item["answer"].strip()
        if not answer:
            problems.append(f"Q{number}: no answer")
        elif (
            "multiple choice" in label
            and find_correct_ident(item["options"], answer) is None
        ):
            problems.append(f"Q{number}: the answer matches no option")
        elif "true" in label and not answer.startswith(("True", "False")):
            problems.append(
                f"Q{number}: a true/false answer must start with True or False"
            )
    return problems


def rubric_problems(parts, config):
    """The rubric page's parts against capstone.yaml's rubric section."""
    rubric = config["rubric"]
    problems = []
    if [part["key"] for part in parts] != list(rubric):
        problems.append("part keys differ from capstone.yaml")
    for part in parts:
        key, points = part["key"], part["points"]
        if key in rubric and rubric[key]["points"] != points:
            problems.append(
                f"{key}: {points} points, capstone.yaml says {rubric[key]['points']}"
            )
        if tuple(part["tiers"]) != (points, points * 7 // 10, points * 4 // 10, 0):
            problems.append(
                f"{key}: tiers {tuple(part['tiers'])} do not follow 100/70/40/0"
            )
    if sum(part["points"] for part in parts) != 100:
        problems.append("parts do not add up to 100")
    return problems


def sessions_problems(cli):
    """Every saved session, run again now, must print exactly what was saved."""
    sys.path.insert(0, str(w.REF / "tools"))
    from sqlite_cli import check_version

    problems = []
    if check_version(cli) != w.run_text("version"):
        problems.append("sqlite3 --version differs from runs/week13/version.txt")
    for name in w.SESSIONS:
        if w.run_session(cli, name) != w.run_text(name):
            problems.append(f"session {name} prints something else now")
    return problems


def main():
    sys.path.insert(0, str(w.REF / "tools"))
    import yaml
    from capstone_rubric import PARTS
    from sqlite_cli import cli_from_env

    bad, derived, texts = [], [], {}
    for name in PAGES:
        page, extra = importlib.import_module(name).build()
        derived += extra
        texts[name] = (DOCS / f"{name}.html").read_text()
        if texts[name] != page:
            bad.append(f"{name}.html differs from what its builder makes now")
    sources = [
        w.schema_text(),
        *[p.read_text() for p in sorted(w.RUNS.glob("*.txt"))],
        *derived,
    ]
    pool = "\n".join(sources)
    for name in PAGES:
        bad += [
            f"{name}: in no source: {m}"
            for m in check_listings(DOCS / f"{name}.html", sources)
        ]
        bad += [f"{name}: answer shown: {a}" for a in answer_leaks(name, texts[name])]
    bad += [
        f"week13_lab: not real output: {m}"
        for m in expected_misses(texts["week13_lab"], pool)
    ]
    bad += [f"week13_reading: {p}" for p in quiz_problems(DOCS / "week13_reading.html")]
    config = yaml.safe_load(CONFIG.read_text())
    bad += [f"capstone_rubric: {p}" for p in rubric_problems(PARTS, config)]
    bad += sessions_problems(cli_from_env())
    for line in bad:
        print(line)
    print("verify_week13:", "OK" if not bad else f"{len(bad)} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
