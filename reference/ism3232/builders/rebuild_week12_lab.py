"""Rebuild module06_agents from the Week 11 baseline by following the built
Week 12 lab page, then compare with the reference folder and run the check.

    python reference/ism3232/builders/rebuild_week12_lab.py
"""

import filecmp
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parents[1] / "tools"))

import week12_common as w
from check import check
from pagekit import DOCS, folder_at

BASELINE = "81ee233"  # Task 1: the Week 11 end state, rebuilt from the Week 11 lab
DASH = " — "


def steps(page):
    """Yield ('part', label) and ('code', label, code) in page order."""
    text = (DOCS / page).read_text()
    pattern = re.compile(
        r'<div class="section-divider">.*?<div class="label">(.*?)</div>'
        r'|<div class="code-block"><div class="cb-label">(.*?)</div><pre>(.*?)</pre></div>',
        re.DOTALL,
    )
    for match in pattern.finditer(text):
        if match.group(1) is not None:
            yield ("part", html.unescape(match.group(1)))
        else:
            label = html.unescape(match.group(2))
            code = html.unescape(re.sub(r"<[^>]+>", "", match.group(3)))
            yield ("code", label, code)


def replace_def(text, name, new):
    indent = "    " if new.startswith("    def ") else ""
    pattern = (
        rf"^{indent}def {name}\(.*?(?=^{indent}def |^\S|\Z)"
        if indent
        else rf"^def {name}\(.*?(?=^\S|\Z)"
    )
    match = re.search(pattern, text, re.DOTALL | re.MULTILINE)
    if match is None:
        raise ValueError(f"no def {name} to replace")
    tail = "\n\n" if indent else "\n\n\n"
    rest = text[match.end() :]
    return text[: match.start()] + new.rstrip("\n") + (tail if rest else "\n") + rest


def apply(folder, label, code):
    """Apply one listing; return a short description, or None if it is not a file step."""
    name, _, action = label.partition(DASH)
    path = folder / name
    if not name.endswith(".py"):
        return None
    if not action:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(code.rstrip("\n") + "\n")
        return f"write {name}"
    text = path.read_text()
    if action == "add this method to the class":
        text = text.rstrip("\n") + "\n\n" + code.rstrip("\n") + "\n"
    elif action.startswith("replace "):
        text = replace_def(text, action.removeprefix("replace "), code)
    elif action == "add at the bottom":
        text = text.rstrip("\n") + "\n\n\n" + code.rstrip("\n") + "\n"
    elif action == "add this import below the fake_model import":
        anchor = "from fake_model import FakeModel\n"
        text = text.replace(anchor, anchor + code.rstrip("\n") + "\n", 1)
    else:
        return None
    path.write_text(text)
    return f"{action} in {name}"


def differences(built, reference):
    """The .py files that differ between two folders (either side)."""
    names = {p.relative_to(built) for p in built.rglob("*.py")} | {
        p.relative_to(reference) for p in reference.rglob("*.py")
    }
    bad = []
    for name in sorted(names):
        a, b = built / name, reference / name
        if not (a.exists() and b.exists() and filecmp.cmp(a, b, shallow=False)):
            bad.append(str(name))
    return bad


def main():
    folder = folder_at(BASELINE)
    failures = 0
    checkpoint_done = False
    for step in steps("week12_lab.html"):
        if step[0] == "part" and step[1].startswith("Part 7") and not checkpoint_done:
            checkpoint_done = True
            diff = differences(folder, folder_at(w.GUIDED))
            print("after Part 6, differs from guided commit:", diff)
            failures += len(diff)
            failures += check(folder) != 0
        elif step[0] == "code":
            done = apply(folder, step[1], step[2])
            if done:
                print(" ", done)
    diff = differences(folder, w.FOLDER)
    print("after the exercises and mini-project, differs from reference:", diff)
    failures += len(diff)
    failures += check(folder) != 0
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
