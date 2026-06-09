# Video 13: What is a Computer? Hardware, RAM & Storage

## YouTube Metadata

**Title:** What is a Computer? CPU, RAM & Storage Explained for Programmers | ISM2411
**Description:**
Before you write code that runs efficiently, you need to understand what's happening inside the machine. This video explains the three-layer model every programmer needs: CPU (the chef), RAM (the counter), and storage (the pantry). You'll understand why programs crash, why saving matters, and why a script that processes 5 million rows is slower than one that processes 5,000.

Course page: https://markumreed.github.io/ism2411/pages/week01_lecture.html

**Chapters:**
0:00 — Why programmers need to understand hardware
1:30 — The three layers: CPU, RAM, storage
4:00 — The chef/counter/pantry analogy
6:00 — Files and paths
8:30 — What happens when you run a Python script
10:30 — Why this explains every performance problem
12:30 — Recap

**Applies to:** ISM2411 Module 1

**Tags:** what is a computer, CPU RAM storage, computer hardware basics, python for beginners, ISM2411, USF, programming concepts, how computers work, file system basics, python programming

---

## Script

### INTRO (0:00–1:30)

Most programming courses skip this. They jump straight to `print("Hello world")`. This course doesn't, because the students who understand what's happening inside the machine are the ones who can debug their own problems, reason about performance, and explain to a business stakeholder why a script that worked fine on 1,000 rows is crashing on 1,000,000.

You don't need to be an electrical engineer. You need one mental model. Three layers. Let's build it.

---

### THE THREE LAYERS (1:30–6:00)

Every computer has three components you need to know:

**CPU — Central Processing Unit.** This is the chip that executes instructions. It can do billions of operations per second, but it can only work on what's directly in front of it. Think of it as the chef in a kitchen.

**RAM — Random Access Memory.** This is temporary, fast-access working space. When a program runs, the operating system loads it from storage into RAM, and the CPU works on it there. RAM is extremely fast to read and write, but it's volatile — when you turn off the computer, RAM is cleared. Think of RAM as the kitchen counter. The chef can only work with ingredients that are on the counter.

**Storage — HDD or SSD.** This is where files live permanently — your Python scripts, your CSV data files, your project folders. Storage is slower than RAM but persistent. Turn the computer off, turn it back on — your files are still there. Think of storage as the pantry.

---

### THE ANALOGY (4:00–6:00)

The chef can only cook with ingredients on the counter. To use something from the pantry (storage), you carry it to the counter (load into RAM), and then the chef (CPU) works with it.

When you finish cooking and the kitchen closes (power off), everything on the counter disappears. But the pantry is still stocked.

This is exactly what happens when you run a Python script:
1. Python (on storage) is loaded into RAM
2. Your `.py` file (on storage) is loaded into RAM
3. The CPU executes the instructions one by one
4. Your output appears on screen

When the program finishes, its RAM is cleared. If you saved results to a file — that goes back to storage and persists.

**This explains why "save your work" is not just advice.** Unsaved changes exist only on the counter. Power goes out — counter is cleared — work is gone. Save means "copy from counter to pantry."

---

### FILES AND PATHS (6:00–8:30)

A **file** is a named collection of bytes stored on disk. A **directory** (folder) is a container that holds files and other directories. The file system is a tree — directories nest inside directories.

A **path** is the address of a file — the route from the root of the tree to the file.

```
/Users/markum/Documents/ism2411/module01/hello.py
│       │        │          │        │       │
root  username  folder    course   module   file
```

**Absolute path** — starts from root (`/`). Works from anywhere.
**Relative path** — starts from your current location. Shorter but context-dependent.

When you write a Python script that opens a file:
```python
with open("sales_data.csv") as f:
    ...
```

Python looks for `sales_data.csv` in the **current working directory** — wherever your terminal is when you run the script. If the file isn't there, `FileNotFoundError`. Understanding paths prevents this entire class of error.

---

### WHAT HAPPENS WHEN YOU RUN PYTHON (8:30–10:30)

```bash
python3 hello_business.py
```

Step by step:
1. The shell finds the `python3` program on storage
2. OS loads the Python interpreter into RAM
3. Python reads your `.py` file from storage into RAM
4. Python parses it into bytecode (a more efficient internal format)
5. The CPU executes the bytecode, line by line
6. Output goes to the terminal (also via RAM)
7. When the script finishes, Python's RAM is freed

The CPU never touches your `.py` file directly. Everything goes through RAM. This is why opening a huge CSV file can make a script slow or crash — you're trying to fit a pantry full of groceries onto a small counter.

---

### PERFORMANCE INTUITION (10:30–12:30)

Now you can reason about performance without guessing.

**Why does a script processing 5 million rows run slowly?** Because 5 million rows of data has to fit in RAM. If it doesn't fit, the OS starts "swapping" — moving chunks between RAM and storage — which is thousands of times slower.

**Why does saving a file take time?** Data is being written from RAM (fast) to storage (slower). A large file write takes longer.

**Why does a program "crash"?** Usually: something went wrong in RAM. A variable holds an unexpected value, the program tried to access memory it doesn't own, or it ran out of RAM (MemoryError in Python).

**Why is VS Code slow when you first open it?** It's loading from storage into RAM. Once loaded, it's fast — everything's on the counter.

---

### RECAP (12:30–15:00)

- **CPU** — executes instructions (the chef). Extremely fast.
- **RAM** — working memory (the counter). Fast, temporary, cleared on shutdown.
- **Storage** — permanent files (the pantry). Slower, persistent.
- Programs run in RAM. Files live in storage. The CPU only touches RAM.
- Saving copies from RAM to storage — don't skip it.
- A **path** is the address of a file in the directory tree.
- Absolute paths start from root (`/`). Relative paths start from current location.
- Performance intuition: large data = large RAM requirement = potential slowness or crash.

Next module: the command line — `pwd`, `ls`, `cd`, `mkdir`, `touch`. See you there.
