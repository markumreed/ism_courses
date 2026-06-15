#!/usr/bin/env python3
"""Generate 1280x720 YouTube thumbnails for all 33 lecture videos.

Dark house style matching the course infographics: ink background, a
topic-colored accent, a short bold headline, a topic eyebrow, a faint
code motif, a giant faint sequence number, and a Part footer.

Output: ppt/thumbnails/NN_slug.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

S = 2  # supersample
W, H = 1280 * S, 720 * S
BG, PANEL, INK, MUTED, GHOST = "#14141d", "#1c1c28", "#ffffff", "#9a9ab0", "#22222f"
DJ = "/usr/share/fonts/truetype/dejavu"
OUT = os.path.join(os.path.dirname(__file__), "thumbnails")

# topic accents (drawn from both courses' color tokens)
GREEN, BLUE, PURPLE, ROSE, TEAL, INDIGO, GOLD = (
    "#34d399", "#60a5fa", "#c084fc", "#fb7185", "#00c9a7", "#818cf8", "#fbbf24")


def f(name, size):
    return ImageFont.truetype(f"{DJ}/{name}.ttf", size * S)


F_EYE = f("DejaVuSansMono-Bold", 26)
F_FOOT = f("DejaVuSansMono", 24)
F_CODE = f("DejaVuSansMono", 30)
F_NUM = f("DejaVuSans-Bold", 300)

# (seq#, slug, headline lines, eyebrow, accent, part, code-motif lines)
VIDEOS = [
    (1, "variables_data_types", ["Variables &", "Data Types"], "PYTHON · FOUNDATIONS", GREEN, 1,
     ["price = 19.99", "qty = 20", "in_stock = True"]),
    (2, "python_operators", ["Python", "Operators"], "PYTHON · OPERATORS", BLUE, 1,
     ["total = price * qty", "if total > 100:", "    discount = 0.1"]),
    (3, "fstrings_formatting", ["f-strings &", "Formatting"], "PYTHON · OUTPUT", BLUE, 1,
     ['f"${total:,.2f}"', 'f"{rate:.1%}"']),
    (4, "if_elif_else", ["if / elif", "/ else"], "PYTHON · LOGIC", BLUE, 1,
     ["if x > 100:", "elif x > 50:", "else:"]),
    (5, "for_loops", ["Python", "for Loops"], "PYTHON · ITERATION", GREEN, 1,
     ["for row in data:", "    total += row"]),
    (6, "dictionaries", ["Python", "Dictionaries"], "PYTHON · DATA", PURPLE, 1,
     ['rec = {"name": ..}', 'rec["price"]']),
    (7, "functions", ["Python", "Functions"], "PYTHON · FUNCTIONS", GREEN, 1,
     ["def total(p, q):", "    return p * q"]),
    (8, "reading_tracebacks", ["Reading", "Tracebacks"], "PYTHON · DEBUGGING", ROSE, 1,
     ["Traceback ...", "TypeError: ...", "  line 12"]),
    (9, "terminal_basics", ["Terminal", "Basics"], "COMMAND LINE", TEAL, 1,
     ["pwd", "ls  ·  cd", "mkdir  ·  touch"]),
    (10, "git_basics", ["Git", "Basics"], "VERSION CONTROL", TEAL, 1,
     ["git add .", 'git commit -m', "git push"]),
    (11, "github_workflow", ["GitHub", "Workflow"], "VERSION CONTROL", TEAL, 1,
     ["git clone ...", "git push origin"]),
    (12, "coding_with_ai", ["Coding", "with AI"], "AI · BEST PRACTICES", GOLD, 1,
     ["# AI-assisted", "# reviewed", "# disclosed"]),
    (13, "cpu_ram_storage", ["CPU, RAM", "& Storage"], "HOW CODE RUNS", INDIGO, 1,
     ["CPU", "RAM", "DISK"]),
    (14, "python_setup", ["Python", "Setup"], "ENVIRONMENT", TEAL, 1,
     ["python3 --version", "code .", "git --version"]),
    (15, "lists_tuples", ["Lists &", "Tuples"], "PYTHON · DATA", PURPLE, 1,
     ["sales = [120, 95]", "(a, b) = row"]),
    (16, "csv_file_io", ["CSV", "File I/O"], "DATA PIPELINES", BLUE, 1,
     ['open("data.csv")', "csv.DictReader(f)"]),
    (17, "pandas_basics", ["pandas", "Basics"], "DATA ANALYSIS", GOLD, 1,
     ["pd.read_csv(..)", "df.describe()"]),
    (18, "data_cleaning", ["Data", "Cleaning"], "DATA ANALYSIS", GOLD, 1,
     ["pd.to_numeric(..)", ".str.strip()", ".dropna()"]),
    (19, "groupby_charts", ["groupby &", "Charts"], "DATA ANALYSIS", GOLD, 1,
     ['df.groupby("reg")', "plt.bar(...)"]),
    (20, "data_project", ["Data Analysis", "Project"], "CAPSTONE", GOLD, 1,
     ["load → clean", "analyze → chart"]),
    (21, "dev_environment", ["Dev", "Environment"], "SETUP", TEAL, 2,
     ["code .", "python3 -V", "git --version"]),
    (22, "advanced_shell", ["Advanced", "Shell Tools"], "COMMAND LINE", TEAL, 2,
     ["grep -rn ...", "fd · fzf · zoxide"]),
    (23, "virtual_environments", ["Virtual", "Environments"], "WORKFLOW", TEAL, 2,
     ["python3 -m venv", "pip freeze"]),
    (24, "code_checklist", ["Code", "Checklist"], "WORKFLOW", INDIGO, 2,
     ["pytest -v", "ruff · black", "git push"]),
    (25, "while_loops", ["while", "Loops"], "CONTROL FLOW", BLUE, 2,
     ["while True:", "    if done:", "        break"]),
    (26, "testing_pytest", ["Testing", "with pytest"], "TESTING", INDIGO, 2,
     ["def test_total():", "    assert ..."]),
    (27, "classes_oop", ["Classes", "& OOP"], "OOP · PART 1", ROSE, 2,
     ["class Request:", "  def __init__(self):"]),
    (28, "composition_inheritance", ["Composition", "& Inheritance"], "OOP · PART 2", ROSE, 2,
     ["class Urgent(Req):", "  super().__init__()"]),
    (29, "oop_design", ["OOP", "Design"], "OOP · PART 3", ROSE, 2,
     ["# find the nouns", "# one job each"]),
    (30, "sql_sqlite", ["SQL &", "SQLite"], "DATABASES", TEAL, 2,
     ["CREATE TABLE ...", "INSERT · SELECT"]),
    (31, "python_sqlite", ["Python", "+ SQLite"], "DATABASES", TEAL, 2,
     ["sqlite3.connect(..)", "cur.execute(?, ..)"]),
    (32, "streamlit_app", ["Streamlit", "Web App"], "WEB UI", INDIGO, 2,
     ["st.dataframe(df)", 'st.button("Save")']),
    (33, "ai_feature", ["AI", "Feature"], "GENERATIVE AI", GOLD, 2,
     ["client.messages", "  .create(...)", "max_tokens=300"]),
]


def fit_headline(draw, lines, max_w):
    """Largest bold font (<=104px) where every line fits in max_w."""
    for size in range(104, 48, -2):
        fnt = f("DejaVuSans-Bold", size)
        if all(draw.textlength(ln, font=fnt) <= max_w * S for ln in lines):
            return fnt, size
    return f("DejaVuSans-Bold", 48), 48


def make(seq, slug, lines, eyebrow, accent, part, code):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # giant faint sequence number, bottom-right
    d.text((W - 70 * S, H - 30 * S), f"{seq:02d}", font=F_NUM, fill=GHOST, anchor="rs")
    # faint code motif, top-right
    for i, ln in enumerate(code):
        d.text((W - 60 * S, (95 + i * 46) * S), ln, font=F_CODE, fill="#262634", anchor="ra")
    # left accent bar
    d.rectangle([0, 0, 18 * S, H], fill=accent)
    # eyebrow
    d.text((90 * S, 112 * S), eyebrow, font=F_EYE, fill=accent, anchor="ls")
    # headline (auto-fit)
    fnt, size = fit_headline(d, lines, 1010)
    y = 235
    for ln in lines:
        d.text((86 * S, y * S), ln, font=fnt, fill=INK, anchor="ls")
        y += int(size * 1.18)
    # accent underline under headline
    uy = y - int(size * 0.55)
    d.rectangle([90 * S, uy * S, 330 * S, (uy + 8) * S], fill=accent)
    # footer
    d.text((90 * S, H - 70 * S), f"PYTHON FOR BUSINESS  ·  PART {part}",
           font=F_FOOT, fill=MUTED, anchor="ls")
    img = img.resize((1280, 720), Image.LANCZOS)
    img.save(os.path.join(OUT, f"{seq:02d}_{slug}.png"))


def main():
    os.makedirs(OUT, exist_ok=True)
    for v in VIDEOS:
        make(*v)
    print(f"Generated {len(VIDEOS)} thumbnails in {OUT}")


if __name__ == "__main__":
    main()
