"""Read the transcripts that tools/count_runs.py writes, so pages can quote
counts computed from the saved runs instead of numbers typed by hand."""

import ast
import re

from pagekit import REF


def load(week, name):
    """Return the list of runs in runs/<week>/<name>. Each run is a dict with
    'turns' [(you, reply)], 'tools' [(name, arguments, result)], 'queued' [dict]."""
    text = (REF / "runs" / week / name).read_text()
    runs = []
    for chunk in re.split(r"^--- run \d+\n", text, flags=re.MULTILINE)[1:]:
        run = {"turns": [], "tools": [], "queued": []}
        you = None
        for line in chunk.split("\n"):
            if line.startswith("You: "):
                you = line[5:]
            elif line.startswith("Sunny: "):
                run["turns"].append((you, line[7:]))
            elif line.startswith("  tool "):
                match = re.match(r"  tool (\w+) (\{.*?\}) -> (.*)", line)
                run["tools"].append(
                    (match.group(1), ast.literal_eval(match.group(2)), match.group(3))
                )
            elif line.startswith("  queued "):
                run["queued"].append(ast.literal_eval(line[9:]))
        runs.append(run)
    return runs


def count(runs, test):
    """How many runs pass `test`, and how many runs there were."""
    return sum(1 for run in runs if test(run)), len(runs)


def repeated_lookup(run):
    """True if the same tool was asked for twice in a row with the same arguments."""
    calls = [(name, arguments) for name, arguments, _ in run["tools"]]
    return any(calls[i] == calls[i + 1] for i in range(len(calls) - 1))


def refused(run):
    """True if the toolbox refused at least one request in this run."""
    return any("has not given" in result for _, _, result in run["tools"])


def words(n):
    """Spell small counts the way the pages do: 'five', '0' stays a word too."""
    names = [
        "none",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
    ]
    return names[n] if 0 <= n < len(names) else str(n)
