#!/usr/bin/env python3
"""Generate and inject Module Quiz sections into all ISM3232 reading pages.

Adds quiz CSS to site.css, then injects HTML before <!-- prev-next --> in each
reading page (weeks 1-8 and 10-16; week 9 is the midterm, skipped).

Question types:
  mc   — Multiple Choice (4 options, one correct)
  tf   — True / False
  sa   — Short Answer
  ct   — Code Trace (code block lives in 'code' key)
"""

from pathlib import Path

DOCS    = Path("/home/markumreed/Documents/ism_courses/ism3232/docs")
CSS     = Path("/home/markumreed/Documents/ism_courses/ism3232/site.css")
ANCHOR  = "<!-- prev-next -->"

# ── quiz data ─────────────────────────────────────────────────────────────────
# Each question: {type, q, options:[a,b,c,d], correct (text), answer (explanation), code}

QUIZZES = {

1: {
  "title": "Developer Mindset & First Setup",
  "midterm": True,
  "questions": [
    {"type":"mc","q":"What does a shell do?",
     "options":["Renders web pages","Reads and executes typed commands","Stores files on disk","Compiles Python to machine code"],
     "correct":"Reads and executes typed commands",
     "answer":"The shell (zsh in ISM3232) interprets what you type and tells the OS what to do."},
    {"type":"mc","q":"Which prompt character confirms you are running zsh?",
     "options":["$","#","%",">"],
     "correct":"%",
     "answer":"A dollar sign means bash; a percent sign means zsh. Fix this before continuing."},
    {"type":"mc","q":"What does a path starting with / represent?",
     "options":["A relative path from your home directory","An absolute path from the filesystem root","A temporary directory","A Python module path"],
     "correct":"An absolute path from the filesystem root",
     "answer":"All absolute paths start at /, the root of the directory tree."},
    {"type":"mc","q":"What does ~ represent in a file path?",
     "options":["The parent directory","The current directory","Your home directory","A hidden file"],
     "correct":"Your home directory",
     "answer":"cd ~ takes you home from anywhere, regardless of where you currently are."},
    {"type":"mc","q":"Which command verifies your Python version in ISM3232?",
     "options":["python --version","python3 --version","py --version","check python"],
     "correct":"python3 --version",
     "answer":"Always use python3, not python. The plain python command may point to Python 2 on some systems."},
    {"type":"mc","q":"What does .. (dot dot) refer to in a path?",
     "options":["The current directory","The home directory","The parent directory","A hidden directory"],
     "correct":"The parent directory",
     "answer":"cd .. moves you up one level in the directory tree."},
    {"type":"tf","q":"A directory can contain both files and other directories.",
     "answer":"True — Directories contain files and/or other directories. This is the fundamental structure of every filesystem."},
    {"type":"tf","q":"The terminal and the shell are the same program.",
     "answer":"False — The terminal is the window you type in; the shell (zsh) is the program inside it that reads your commands."},
    {"type":"sa","q":"What are the six verification commands you must run successfully in Week 1, and what does each confirm?",
     "answer":"echo $SHELL (shell is zsh), zsh --version (5.x+), python3 --version (3.10+), git --version (2.x), pwd (shows home dir), ls (lists home contents). All six must run without errors before continuing."},
  ]
},

2: {
  "title": "zsh Navigation & File Operations",
  "midterm": True,
  "questions": [
    {"type":"mc","q":"What does pwd print?",
     "options":["The number of files in the current directory","Your absolute path from the root","Your username","The last command you ran"],
     "correct":"Your absolute path from the root",
     "answer":"pwd stands for 'print working directory'; it always shows an absolute path starting with /."},
    {"type":"mc","q":"Which command lists all files including hidden ones with permissions and sizes?",
     "options":["ls","ls -l","ls -la","ls -a"],
     "correct":"ls -la",
     "answer":"-l adds long format (permissions, size, date); -a adds hidden files (those starting with .)."},
    {"type":"mc","q":"What does mkdir -p a/b/c do?",
     "options":["Creates only directory c","Creates only directory a","Creates a, b, and c as nested directories","Prints the directory tree"],
     "correct":"Creates a, b, and c as nested directories",
     "answer":"The -p flag creates all intermediate directories as needed."},
    {"type":"mc","q":"Which command renames old.py to new.py?",
     "options":["cp old.py new.py","mv old.py new.py","rename old.py new.py","rn old.py new.py"],
     "correct":"mv old.py new.py",
     "answer":"mv moves or renames files. Within the same directory it renames; across directories it moves."},
    {"type":"mc","q":"What is the LAST step of the rm safety ritual before deleting a file?",
     "options":["Run ls to visually confirm the exact filename","Open the file in VS Code","Make a backup copy first","Run git status"],
     "correct":"Run ls to visually confirm the exact filename",
     "answer":"Before rm, always ls to confirm the exact filename. rm has no trash and no undo."},
    {"type":"mc","q":"What does touch filename.py do if the file does not yet exist?",
     "options":["Raises an error","Runs the file","Creates an empty file","Copies the file from a template"],
     "correct":"Creates an empty file",
     "answer":"touch creates an empty file. If the file already exists it updates its timestamp instead."},
    {"type":"tf","q":"rm moves files to a trash folder where they can be recovered.",
     "answer":"False — rm permanently deletes files immediately. There is no trash, no undo, and no recovery. Always double-check with ls before running rm."},
    {"type":"tf","q":"cd .. always takes you to your home directory.",
     "answer":"False — cd .. moves you one level up to the parent directory. cd ~ (tilde) takes you to your home directory from anywhere."},
    {"type":"sa","q":"What does code . do, and when would you use it?",
     "answer":"code . opens the current directory as a workspace in VS Code. Use it after navigating to your project folder so VS Code's file explorer, integrated terminal, and editor all start in the right place."},
  ]
},

3: {
  "title": "Virtual Environments & Shell Customisation",
  "midterm": True,
  "questions": [
    {"type":"mc","q":"What is the primary purpose of a virtual environment?",
     "options":["To speed up Python","To isolate project dependencies so different projects do not conflict","To run Python faster","To share packages with teammates automatically"],
     "correct":"To isolate project dependencies so different projects do not conflict",
     "answer":"Without venv, installing a package for one project can break another project that requires a different version of the same package."},
    {"type":"mc","q":"Which command creates a virtual environment named .venv?",
     "options":["python3 -m venv .venv","virtualenv .venv","venv create .venv","pip install venv"],
     "correct":"python3 -m venv .venv",
     "answer":"The -m flag runs the venv module. .venv is the convention; the leading dot makes it hidden."},
    {"type":"mc","q":"Which command activates the virtual environment on macOS/Linux?",
     "options":["activate .venv",".venv activate","source .venv/bin/activate","venv on"],
     "correct":"source .venv/bin/activate",
     "answer":"source runs the activate script in your current shell. The prompt gains (.venv) when activation succeeds."},
    {"type":"mc","q":"What does pip freeze > requirements.txt do?",
     "options":["Runs all tests","Deletes installed packages","Saves a snapshot of all installed packages to requirements.txt","Updates all packages"],
     "correct":"Saves a snapshot of all installed packages to requirements.txt",
     "answer":"This snapshot lets teammates recreate your exact environment with pip install -r requirements.txt."},
    {"type":"mc","q":"Where must .venv/ always be listed?",
     "options":["requirements.txt","README.md",".gitignore","site.py"],
     "correct":".gitignore",
     "answer":"The .venv folder can contain thousands of files. It must never be committed to git; .gitignore prevents that."},
    {"type":"mc","q":"Where does the .zshrc file live?",
     "options":["/etc/zsh/","~/.zshrc","~/.config/zsh/","/usr/local/share/zsh/"],
     "correct":"~/.zshrc",
     "answer":"~ is your home directory. .zshrc is a hidden file (starts with .) that zsh reads automatically on startup."},
    {"type":"tf","q":"After you run deactivate, pip install still installs packages into the virtual environment.",
     "answer":"False — After deactivate, pip targets the system Python. Run source .venv/bin/activate again to return to the venv."},
    {"type":"tf","q":"An alias defined in .zshrc must be re-entered every time you open a new terminal.",
     "answer":"False — .zshrc is read automatically when a new shell starts. Aliases defined there persist across all future sessions without re-entry."},
    {"type":"sa","q":"What is the difference between pip install requests and pip install -r requirements.txt?",
     "answer":"pip install requests installs one named package. pip install -r requirements.txt reads a file and installs every package listed in it, recreating an environment from a saved snapshot. Use the -r form when cloning a teammate's repo."},
  ]
},

4: {
  "title": "Search Tools, the Submission Ritual & Git",
  "midterm": True,
  "questions": [
    {"type":"mc","q":"Which command searches for the text 'def approve' across all files recursively?",
     "options":["find . -name 'def approve'","grep 'def approve' *.py","rg 'def approve'","search 'def approve' ."],
     "correct":"rg 'def approve'",
     "answer":"ripgrep (rg) searches recursively by default, is faster than grep, and respects .gitignore automatically."},
    {"type":"mc","q":"What does git add . do?",
     "options":["Creates a new repository","Stages all changed files in the current directory for the next commit","Pushes commits to GitHub","Shows recent commits"],
     "correct":"Stages all changed files in the current directory for the next commit",
     "answer":"Staging selects changes for the next commit. git add . stages everything; git add filename.py stages one file."},
    {"type":"mc","q":"What is the correct order of the three core git commands for submitting an assignment?",
     "options":["commit → add → push","push → add → commit","add → commit → push","commit → push → add"],
     "correct":"add → commit → push",
     "answer":"You must stage (add) before you can commit, and you must commit before you can push."},
    {"type":"mc","q":"What does ruff format . do?",
     "options":["Runs all tests","Deletes unused imports","Reformats all Python files to a consistent style","Checks for logic errors"],
     "correct":"Reformats all Python files to a consistent style",
     "answer":"ruff format changes whitespace, indentation, and line length — it does not change what the code does."},
    {"type":"mc","q":"What does git log --oneline show?",
     "options":["The full diff of every commit","A one-line summary of each commit in the history","The current status of staged files","Remote repository information"],
     "correct":"A one-line summary of each commit in the history",
     "answer":"--oneline compresses each commit to its short hash and message, giving a fast visual history."},
    {"type":"mc","q":"In the pre-submission ritual, what step comes immediately before git push?",
     "options":["ruff check .","python3 -m pytest","git commit -m '...'","git add ."],
     "correct":"git commit -m '...'",
     "answer":"The ritual order ends with: git add → git commit → git push. commit must always come before push."},
    {"type":"tf","q":"git status shows which files have been changed but not yet staged.",
     "answer":"True — git status shows three categories: untracked new files, unstaged changes (modified but not added), and staged changes (added but not yet committed)."},
    {"type":"tf","q":"You can push to GitHub without first committing.",
     "answer":"False — git push sends existing commits to the remote. If you have not committed, there is nothing to push. The order is always add → commit → push."},
    {"type":"sa","q":"What is the purpose of ruff check . in the submission ritual, and what does it find that ruff format . does not fix?",
     "answer":"ruff check . finds code quality issues: unused imports, undefined variables, shadowed names, and violations that a formatter cannot auto-fix. ruff format changes layout (whitespace, line length) but ignores logic. ruff check catches bugs and bad practices that format misses."},
  ]
},

5: {
  "title": "Variables, Data Types & Operators",
  "midterm": True,
  "questions": [
    {"type":"mc","q":"What does the // operator return in Python?",
     "options":["Floating-point division","The remainder after division","Integer (floor) division","Exponentiation"],
     "correct":"Integer (floor) division",
     "answer":"7 // 2 is 3, not 3.5. The result is always rounded down to the nearest integer."},
    {"type":"mc","q":"What is the output of: type(3.0)?",
     "options":["<class 'int'>","<class 'float'>","<class 'str'>","<class 'num'>"],
     "correct":"<class 'float'>",
     "answer":"The decimal point makes 3.0 a float, even though its value is a whole number."},
    {"type":"mc","q":"Which f-string format specifier displays 1234567.89 as 1,234,567.89?",
     "options":[":.2f",":,.2f",":>2f",":.2d"],
     "correct":":,.2f",
     "answer":"The comma adds thousands separators; .2 sets decimal places; f specifies float formatting."},
    {"type":"mc","q":"Which expression converts the string \"42\" to the integer 42?",
     "options":["str(42)","float(\"42\")","int(\"42\")","bool(\"42\")"],
     "correct":"int(\"42\")",
     "answer":"int() converts a string or float to an integer. str() goes the other direction."},
    {"type":"ct","q":"What is the output?",
     "code":'price = 49.99\nqty = 3\ntotal = price * qty\nprint(f\'Total: ${total:,.2f}\')',
     "answer":"Total: $149.97 — price * qty = 149.97, formatted with comma separator and two decimal places."},
    {"type":"ct","q":"What is printed?",
     "code":'x = 17\nprint(x // 5)\nprint(x % 5)',
     "answer":"3\n2 — 17 // 5 = 3 (floor division); 17 % 5 = 2 (remainder)."},
    {"type":"tf","q":"In Python, \"3\" + 3 raises a TypeError.",
     "answer":"True — Python does not auto-convert types. You cannot add a string and an integer. Convert first: int(\"3\") + 3, or \"3\" + str(3)."},
    {"type":"tf","q":"The % operator returns a percentage as a float.",
     "answer":"False — % is the modulus operator; it returns the remainder after integer division. 10 % 3 is 1. To get a percentage you multiply by 100: rate * 100."},
    {"type":"sa","q":"What is the difference between = and == in Python?",
     "answer":"= is assignment — it stores a value in a variable (x = 5). == is comparison — it tests equality and returns True or False (x == 5 → True). Using = where == is expected is one of the most common Python bugs."},
  ]
},

6: {
  "title": "Conditionals, Loops & Dictionaries",
  "midterm": True,
  "questions": [
    {"type":"mc","q":"What does the accumulator pattern do?",
     "options":["Deletes items from a list one by one","Builds up a result across loop iterations using += or .append()","Counts backward from n to 0","Exits a loop when a condition is met"],
     "correct":"Builds up a result across loop iterations using += or .append()",
     "answer":"An accumulator starts at an empty/zero value, then grows with each iteration."},
    {"type":"ct","q":"What is printed?",
     "code":'amounts = [100, 250, 75, 400]\ntotal = 0\nfor a in amounts:\n    total += a\nprint(total)',
     "answer":"825 — The accumulator adds each element: 0+100+250+75+400 = 825."},
    {"type":"mc","q":"Which expression accesses the value for key \"status\" in dict d?",
     "options":["d[\"status\"]","d.status","d->status","d(status)"],
     "correct":"d[\"status\"]",
     "answer":"Square bracket notation is the standard way to access dict values by key."},
    {"type":"ct","q":"What is the output?",
     "code":'record = {"name": "Apex Laptop", "price": 899.00, "qty": 5}\nprint(record["name"])\nprint(record["price"] * record["qty"])',
     "answer":"Apex Laptop\n4495.0 — The first line accesses the \"name\" key; the second multiplies the two numeric values."},
    {"type":"mc","q":"What happens if you access a dict key that doesn't exist using square brackets?",
     "options":["Returns None","Returns an empty string","Raises a KeyError","Creates the key with value None"],
     "correct":"Raises a KeyError",
     "answer":"d[\"missing_key\"] raises KeyError immediately. Use d.get(\"key\") to get None instead of an error."},
    {"type":"mc","q":"In a list-of-dicts, what does each item in the list represent?",
     "options":["A column name","One record (row) of data","A table schema","A database connection"],
     "correct":"One record (row) of data",
     "answer":"This is the standard pattern for tabular data: one list holding many records, each record a dict with the same keys."},
    {"type":"tf","q":"An elif branch runs even if the preceding if condition was True.",
     "answer":"False — elif is skipped entirely if the preceding if (or elif) was True. Only the first matching branch executes."},
    {"type":"tf","q":"list.append() modifies the list in place and returns None.",
     "answer":"True — append() modifies the list in place. It does not return the modified list — it returns None. A common mistake: my_list = my_list.append(x) sets my_list to None."},
    {"type":"sa","q":"What is the difference between a while loop and a for loop, and when would you choose each?",
     "answer":"A for loop iterates over a known sequence a fixed number of times. A while loop repeats as long as a condition is True, with no predetermined count. Use for when you know the iterable; use while when waiting for a condition to change (user input, retry logic, draining a queue)."},
  ]
},

7: {
  "title": "Functions, Modules & pytest",
  "midterm": True,
  "questions": [
    {"type":"mc","q":"What does a return statement do in a function?",
     "options":["Prints the result to the terminal","Ends the function and sends a value back to the caller","Stores the result in a global variable","Calls the function again"],
     "correct":"Ends the function and sends a value back to the caller",
     "answer":"Without return, a function returns None. The returned value can be stored or passed to another function."},
    {"type":"ct","q":"What is printed?",
     "code":"def discount(price, rate=0.10):\n    return price * (1 - rate)\n\nprint(discount(200))\nprint(discount(200, 0.25))",
     "answer":"180.0\n150.0 — First call uses default rate 0.10: 200 * 0.90 = 180.0. Second uses 0.25: 200 * 0.75 = 150.0."},
    {"type":"mc","q":"What is a local variable?",
     "options":["A variable defined at the top of a file","A variable that works in any function","A variable defined inside a function that exists only while that function runs","A variable imported from another module"],
     "correct":"A variable defined inside a function that exists only while that function runs",
     "answer":"Local variables are created when a function is called and destroyed when it returns. They are invisible to code outside the function."},
    {"type":"mc","q":"Which pytest convention must test function names follow?",
     "options":["Must start with check_","Must start with test_","Must end with _test","Can be named anything"],
     "correct":"Must start with test_",
     "answer":"pytest discovers tests by looking for functions beginning with test_. Any other prefix and pytest silently skips them."},
    {"type":"mc","q":"In the ISM3232 project structure, where must all pytest test files live?",
     "options":["In the project root","In a tests/ directory","Inside each source file","In a conftest.py file"],
     "correct":"In a tests/ directory",
     "answer":"The required structure is: models.py (source), tests/test_models.py (tests). Tests must be in a dedicated tests/ folder."},
    {"type":"mc","q":"What does assert req.status == 'Pending' do in a pytest test?",
     "options":["Prints the status","Sets the status to 'Pending'","Fails the test if req.status is not 'Pending'","Skips the test if the condition is False"],
     "correct":"Fails the test if req.status is not 'Pending'",
     "answer":"If the assertion fails, pytest marks the test FAILED and shows the actual vs. expected values."},
    {"type":"tf","q":"A function with no return statement returns 0 by default.",
     "answer":"False — A function with no return statement returns None, not 0. Returning None when a value is expected is a common bug."},
    {"type":"tf","q":"You can import a function from another .py file using: from filename import function_name.",
     "answer":"True — For example, from models import BusinessRequest imports the class from models.py in the same directory."},
    {"type":"sa","q":"What is a default parameter value in a function, and why is it useful? Give a one-line example.",
     "answer":"A default parameter gives a fallback value used when the caller does not pass that argument. It makes a parameter optional. Example: def tax(price, rate=0.07): return price * rate — calling tax(100) uses 0.07; tax(100, 0.15) overrides it."},
  ]
},

8: {
  "title": "Debugging, AI Literacy & Midterm Review",
  "midterm": True,
  "questions": [
    {"type":"mc","q":"When reading a Python traceback, where should you start?",
     "options":["The first line","The middle","The last line — the error type and message","The function name in the middle"],
     "correct":"The last line — the error type and message",
     "answer":"The last line names the error type (e.g., TypeError) and explains what went wrong. Read it first, then work up the call stack."},
    {"type":"mc","q":"What does a NameError usually mean?",
     "options":["A function was called with the wrong number of arguments","A variable was used before it was defined","A list index was out of range","Two incompatible types were combined"],
     "correct":"A variable was used before it was defined",
     "answer":"Python raises NameError when it encounters a name it has never seen. Common causes: typo in a variable name, or using a variable before assigning it."},
    {"type":"mc","q":"What is the correct systematic debugging approach in ISM3232?",
     "options":["Ask AI immediately","Try five random fixes","Read the traceback, add print() statements to trace values, form a hypothesis, then test it","Restart the kernel and rerun everything"],
     "correct":"Read the traceback, add print() statements to trace values, form a hypothesis, then test it",
     "answer":"Systematic debugging: read the error, locate it, trace the values, understand what's wrong, fix it."},
    {"type":"mc","q":"What does a TypeError typically indicate?",
     "options":["A variable name was misspelled","An operation was applied to the wrong data type","A file was not found","A list was indexed out of bounds"],
     "correct":"An operation was applied to the wrong data type",
     "answer":"For example: adding a str and int, calling a non-callable, or passing too many arguments to a function."},
    {"type":"ct","q":"What error does this raise, and why?",
     "code":"def total(prices):\n    return sum(prices)\n\nresult = total(\"49.99\")\nprint(result)",
     "answer":"TypeError — sum() expects an iterable of numbers. \"49.99\" is a string; iterating over it gives characters ('4','9','.',…), not numbers. Fix: pass a list of floats."},
    {"type":"mc","q":"What is the 'Debug First, Then Ask' rule in ISM3232?",
     "options":["Never use AI tools","Read the error and attempt at least one fix yourself before asking AI","Ask AI first, then verify its output","Debug for one full hour before giving up"],
     "correct":"Read the error and attempt at least one fix yourself before asking AI",
     "answer":"You must read the traceback, form a hypothesis, and try a fix before using AI. This is a required, graded activity."},
    {"type":"tf","q":"The line number in a traceback always points to the exact line that caused the bug.",
     "answer":"False — The line number shows where Python detected the problem, which is often a consequence of the actual bug earlier in the code."},
    {"type":"tf","q":"When asking AI for debugging help, you should include the full traceback and the relevant code.",
     "answer":"True — AI tools produce much better answers with the exact error message and the code around it. Vague descriptions like 'it doesn't work' lead to generic and often wrong suggestions."},
    {"type":"sa","q":"Name four Python error types and give one distinguishing example for each.",
     "answer":"NameError (print(x) before x is assigned), TypeError (\"3\" + 3 — adding str and int), KeyError (d[\"missing\"] — key does not exist), IndexError ([1,2,3][5] — index out of range). Each name describes exactly which constraint was violated."},
  ]
},

10: {
  "title": "OOP I — Classes & Objects",
  "midterm": False,
  "questions": [
    {"type":"mc","q":"What is the purpose of __init__ in a Python class?",
     "options":["It runs when the class is deleted","It initialises a new instance's attributes when the object is created","It defines class-level constants","It is called every time a method is invoked"],
     "correct":"It initialises a new instance's attributes when the object is created",
     "answer":"__init__ is called automatically when you write obj = ClassName(…). Its job is to store the starting values for all instance attributes."},
    {"type":"mc","q":"What does self refer to inside a method?",
     "options":["The class itself","The specific instance the method was called on","The parent class","The last argument passed to the method"],
     "correct":"The specific instance the method was called on",
     "answer":"self.status refers to the status of the particular object, not all objects of that class. Every instance method must have self as its first parameter."},
    {"type":"ct","q":"What is printed?",
     "code":"class Item:\n    def __init__(self, name, price):\n        self.name = name\n        self.price = price\n\na = Item('Pen', 1.50)\nb = Item('Notebook', 4.99)\nprint(a.name)\nprint(b.price)",
     "answer":"Pen\n4.99 — a and b are independent instances. a.name is 'Pen'; b.price is 4.99."},
    {"type":"mc","q":"What is encapsulation?",
     "options":["Inheriting behaviour from a parent class","Running tests automatically","Bundling data (attributes) and the functions that operate on it (methods) into a single object","Converting one data type to another"],
     "correct":"Bundling data (attributes) and the functions that operate on it (methods) into a single object",
     "answer":"Encapsulation keeps related data and behaviour together and hides implementation details from outside code."},
    {"type":"mc","q":"What is the purpose of __repr__ in a class?",
     "options":["It defines how the object is compared with ==","It initialises attributes","It provides a readable string representation for debugging and the REPL","It destroys the object when it goes out of scope"],
     "correct":"It provides a readable string representation for debugging and the REPL",
     "answer":"Without __repr__, printing an object shows <__main__.BusinessRequest object at 0x…>. With it, you see a readable summary."},
    {"type":"ct","q":"What is printed?",
     "code":"class Counter:\n    def __init__(self):\n        self.count = 0\n\n    def increment(self):\n        self.count += 1\n\nc = Counter()\nc.increment()\nc.increment()\nprint(c.count)",
     "answer":"2 — Each increment() call adds 1 to self.count. Starting at 0, after two calls count is 2."},
    {"type":"tf","q":"Two instances of the same class always share the same attribute values.",
     "answer":"False — Each instance has its own copy of instance attributes. req1.status and req2.status are independent; changing one has no effect on the other."},
    {"type":"tf","q":"A class can have multiple methods in addition to __init__.",
     "answer":"True — Classes can have as many methods as needed. In ISM3232 you write approve(), reject(), __repr__, and others alongside __init__."},
    {"type":"sa","q":"What is the difference between a class and an instance?",
     "answer":"A class is the blueprint — it defines the attributes and methods. An instance is a specific object created from that blueprint. BusinessRequest is the class; req1 = BusinessRequest(1, 'Taylor', 'Equipment', 1200.00) is one instance. Many independent instances can be created from the same class."},
  ]
},

11: {
  "title": "OOP II — Composition, Inheritance & SQL Mapping",
  "midterm": False,
  "questions": [
    {"type":"mc","q":"What is composition in OOP?",
     "options":["A class that inherits all methods from another class","An object that contains another object as an attribute","Combining two functions into one","Storing class data in a database"],
     "correct":"An object that contains another object as an attribute",
     "answer":"In the manager pattern, RequestManager has a self.requests list of BusinessRequest objects — it 'has' requests, it doesn't 'is' one."},
    {"type":"mc","q":"When is inheritance the appropriate design choice?",
     "options":["When two classes share a name","When one class IS a more specific version of another (is-a relationship)","Whenever you want to reuse code","When one class needs to call a method from another"],
     "correct":"When one class IS a more specific version of another (is-a relationship)",
     "answer":"'A TravelRequest IS A BusinessRequest' is valid. If the is-a sentence sounds wrong, use composition instead."},
    {"type":"ct","q":"What is printed?",
     "code":"class Animal:\n    def __init__(self, name):\n        self.name = name\n    def speak(self):\n        return '...'\n\nclass Dog(Animal):\n    def speak(self):\n        return 'Woof'\n\nd = Dog('Rex')\nprint(d.name)\nprint(d.speak())",
     "answer":"Rex\nWoof — d.name comes from Animal.__init__ (inherited). d.speak() uses Dog's override, not Animal's."},
    {"type":"mc","q":"In OOP-to-SQL mapping, what does a class typically map to?",
     "options":["A SQL function","A database table","A database connection","A SQL query"],
     "correct":"A database table",
     "answer":"The class defines the structure (attributes ↔ columns); each instance maps to one row."},
    {"type":"mc","q":"Why is self.requests = [] placed inside __init__ rather than at the class level in RequestManager?",
     "options":["Python requires it there","It ensures each RequestManager instance has its own independent list","It makes the list read-only","Class-level lists don't support append()"],
     "correct":"It ensures each RequestManager instance has its own independent list",
     "answer":"If requests = [] were at the class level, all instances would share it. A bug in one manager would corrupt all others."},
    {"type":"mc","q":"Which sentence correctly describes the TravelRequest / BusinessRequest relationship?",
     "options":["TravelRequest has a BusinessRequest","TravelRequest is a BusinessRequest","BusinessRequest is a TravelRequest","TravelRequest replaces BusinessRequest"],
     "correct":"TravelRequest is a BusinessRequest",
     "answer":"TravelRequest extends BusinessRequest with a lower approval limit; it is still a BusinessRequest, making inheritance appropriate."},
    {"type":"tf","q":"A subclass automatically inherits all methods from its parent class.",
     "answer":"True — A subclass inherits every method and attribute from its parent. It can override specific methods, but anything not overridden falls through to the parent."},
    {"type":"tf","q":"Composition and inheritance solve the same design problem and are interchangeable.",
     "answer":"False — Composition ('has-a') and inheritance ('is-a') solve different design problems. Composition is often preferred because it is more flexible and avoids tight coupling."},
    {"type":"sa","q":"What are the three OOP-to-SQL mapping rules introduced this week?",
     "answer":"(1) Each class maps to a table. (2) Each instance maps to a row. (3) Each attribute maps to a column. This pattern is the foundation of every ORM and explains why SQL tables look like class definitions."},
  ]
},

12: {
  "title": "OOP III — Applied Practice & Design",
  "midterm": False,
  "questions": [
    {"type":"mc","q":"According to the ISM3232 workflow, what must be completed before creating any .py files?",
     "options":["Install all dependencies","Write all tests first","Write a class design document","Create the database schema"],
     "correct":"Write a class design document",
     "answer":"Design before you type. The design document defines entities, attributes, methods, and relationships. Code files come after."},
    {"type":"mc","q":"What is the first of the four OOP mistakes to catch this week?",
     "options":["Using inheritance instead of composition","Missing the self parameter on an instance method","Forgetting __repr__","Hardcoding values as literals"],
     "correct":"Missing the self parameter on an instance method",
     "answer":"def approve(): raises TypeError on call; def approve(self): is correct. Every instance method needs self as its first parameter."},
    {"type":"ct","q":"What mistake is in this code, and what error will it raise?",
     "code":"class Product:\n    def __init__(self, name, price):\n        self.name = name\n        self.price = price\n\n    def apply_discount(rate):\n        self.price = self.price * (1 - rate)",
     "answer":"Missing self in apply_discount — def apply_discount(rate): should be def apply_discount(self, rate):. Calling p.apply_discount(0.1) raises: TypeError: apply_discount() takes 1 positional argument but 2 were given."},
    {"type":"mc","q":"What does writing tests before the implementation (TDD-style) help you do?",
     "options":["Skip the design document","Clarify what the class must do before deciding how it does it","Generate test data automatically","Avoid writing __init__"],
     "correct":"Clarify what the class must do before deciding how it does it",
     "answer":"Tests define the expected behaviour first. You then write code to satisfy them. This catches design problems early."},
    {"type":"mc","q":"A class design document should define which of the following?",
     "options":["Only the __init__ signature","Entity name, attributes with types, methods with purpose, and relationships to other classes","Only the SQL schema","Only the test cases"],
     "correct":"Entity name, attributes with types, methods with purpose, and relationships to other classes",
     "answer":"The design document is your contract. Code and tests are written from it."},
    {"type":"mc","q":"What does 'minimum five tests' mean for the Week 12 assignment?",
     "options":["Five test files","Five test functions, each testing a distinct behaviour","Five lines of assert statements","Five runs of pytest"],
     "correct":"Five test functions, each testing a distinct behaviour",
     "answer":"Each test_ function is one test. The minimum is five distinct behaviours: init, method 1, method 2, edge case, error case."},
    {"type":"tf","q":"It is acceptable in ISM3232 to add attributes to an object outside of __init__.",
     "answer":"False (by course convention) — All instance attributes must be defined in __init__. Attributes added elsewhere are invisible to readers of __init__ and make the class harder to understand and test."},
    {"type":"tf","q":"A design document is only useful for large, complex systems.",
     "answer":"False — Even for a two-class system, a design document prevents the most common beginner mistake: discovering structural problems after writing code. Five minutes of design saves thirty minutes of refactoring."},
    {"type":"sa","q":"Why should a class method do one thing rather than multiple things?",
     "answer":"Methods that do one thing are easier to name, test, and reuse. If approve() also sends a notification and logs to a file, you must mock two systems just to test the approval logic. One responsibility per method means one assert per test."},
  ]
},

13: {
  "title": "Capstone Design & SQL Foundations",
  "midterm": False,
  "questions": [
    {"type":"mc","q":"In the sqlite3 shell, which command lists all tables in the database?",
     "options":["SHOW TABLES;","LIST TABLES;",".tables","SELECT * FROM tables;"],
     "correct":".tables",
     "answer":"sqlite3 dot commands start with . and are not SQL. .tables lists tables; .schema tablename shows the CREATE TABLE statement."},
    {"type":"mc","q":"What does PRIMARY KEY AUTOINCREMENT do on a column?",
     "options":["Requires a value to be manually supplied","Automatically assigns a unique incrementing integer id to each new row","Prevents duplicate rows across all columns","Creates an index on the column"],
     "correct":"Automatically assigns a unique incrementing integer id to each new row",
     "answer":"You never insert the id yourself; SQLite assigns the next available integer automatically."},
    {"type":"ct","q":"What does this SQL statement return?",
     "code":"SELECT requester, amount\nFROM requests\nWHERE status = 'Pending'\nORDER BY amount DESC;",
     "answer":"The requester name and amount for all rows where status is 'Pending', sorted with the highest amounts first (descending)."},
    {"type":"mc","q":"Which SQL data type stores decimal numbers like prices?",
     "options":["INTEGER","TEXT","REAL","BLOB"],
     "correct":"REAL",
     "answer":"REAL stores floating-point numbers (e.g., 1250.00). INTEGER stores whole numbers; TEXT stores strings; BLOB stores binary data."},
    {"type":"mc","q":"What does NOT NULL mean in a column definition?",
     "options":["The column stores only zero values","The column cannot be left empty — a value must be provided","The column stores text, not numbers","The column is a foreign key"],
     "correct":"The column cannot be left empty — a value must be provided",
     "answer":"An INSERT without a value for a NOT NULL column raises an error. Omitting it allows NULL (missing) values, which can cause unexpected bugs."},
    {"type":"mc","q":"How many required fields does the ISM3232 project proposal have?",
     "options":["5","8","10","12"],
     "correct":"10",
     "answer":"All 10 fields are required: project name, business problem, primary user, records stored, key operations, Python entities, SQL tables, success criterion, stretch goal, and tech stack confirmation."},
    {"type":"tf","q":"In SQL, an UPDATE statement without a WHERE clause modifies every row in the table.",
     "answer":"True — UPDATE requests SET status = 'Approved'; changes every row. Always add WHERE id = ? or another specific condition to target only the intended row."},
    {"type":"tf","q":"The sqlite3 shell .mode column and .headers on settings are saved permanently to the database.",
     "answer":"False — These dot commands configure the current session's display only. They are not stored. Add them to ~/.sqliterc to make them permanent."},
    {"type":"sa","q":"What is the difference between CREATE TABLE and CREATE TABLE IF NOT EXISTS?",
     "answer":"CREATE TABLE raises an error if the table already exists. CREATE TABLE IF NOT EXISTS checks first and silently skips creation if the table is there. Always use IF NOT EXISTS in create_table() functions so they are safe to call multiple times, including in tests."},
  ]
},

14: {
  "title": "Python + SQL Integration",
  "midterm": False,
  "questions": [
    {"type":"mc","q":"What is the purpose of using ? placeholders in a sqlite3 query?",
     "options":["To mark optional columns","To prevent SQL injection by separating SQL structure from user-supplied values","To match column types automatically","To create indexes"],
     "correct":"To prevent SQL injection by separating SQL structure from user-supplied values",
     "answer":"Never build SQL with f-strings. conn.execute('INSERT INTO t VALUES (?)', (value,)) is safe; f'INSERT INTO t VALUES ({value})' is a SQL injection vulnerability."},
    {"type":"mc","q":"What does with sqlite3.connect(db_file) as conn: ensure?",
     "options":["The database is always created fresh","The connection is committed and closed automatically when the block exits","All queries run in read-only mode","The database is locked for the test"],
     "correct":"The connection is committed and closed automatically when the block exits",
     "answer":"The context manager handles cleanup. If an exception is raised, changes are rolled back. This prevents connection leaks."},
    {"type":"ct","q":"What does this function return for a new, empty database?",
     "code":"def get_all_records(db_file=DB_FILE):\n    with sqlite3.connect(db_file) as conn:\n        rows = conn.execute('SELECT * FROM requests').fetchall()\n    return rows",
     "answer":"An empty list [] — fetchall() returns all matching rows as a list of tuples. If the table has no rows, it returns an empty list."},
    {"type":"mc","q":"Why do ISM3232 database functions accept a db_file parameter with a default value?",
     "options":["To switch between MySQL and SQLite","To let tests use a temporary database instead of the production file","To set the connection timeout","To specify the SQL dialect"],
     "correct":"To let tests use a temporary database instead of the production file",
     "answer":"Tests pass tmp_path / 'test.db' as db_file, keeping test data completely separate from the real database."},
    {"type":"mc","q":"What does tmp_path provide in a pytest test?",
     "options":["A mock of the database connection","A temporary directory unique to the test, cleaned up after the test runs","A pre-populated test database","A path to the production database"],
     "correct":"A temporary directory unique to the test, cleaned up after the test runs",
     "answer":"Using tmp_path / 'test.db' as db_file ensures each test gets a fresh, isolated database with no leftover data from other tests."},
    {"type":"mc","q":"What does conn.execute() return for an INSERT statement?",
     "options":["The inserted row as a dict","A cursor object (use .lastrowid to get the new id)","The total number of rows in the table","True if successful, False if not"],
     "correct":"A cursor object (use .lastrowid to get the new id)",
     "answer":"The cursor has useful properties: .lastrowid (id of the just-inserted row) and .rowcount (number of rows affected)."},
    {"type":"tf","q":"You should build SQL query strings using f-strings when values come from user input.",
     "answer":"False — Building SQL with f-strings is a SQL injection vulnerability. Always use parameterised queries with ? placeholders: conn.execute('SELECT * FROM t WHERE id = ?', (id,))."},
    {"type":"tf","q":"fetchone() raises an exception if no rows match the query.",
     "answer":"False — fetchone() returns None if no rows match. Always check for None before accessing fields, or you will get TypeError: 'NoneType' object is not subscriptable."},
    {"type":"sa","q":"What are the five required database functions in the ISM3232 capstone, and what does each one do?",
     "answer":"create_table (creates the table if not exists), add_record (INSERT a new row, return new id), get_all_records (SELECT * and return all rows), update_status (UPDATE a specific row's status by id), get_status_report (SELECT grouped by status and return counts or totals). Each is tested separately."},
  ]
},

15: {
  "title": "Streamlit Business Interface",
  "midterm": False,
  "questions": [
    {"type":"mc","q":"What happens every time a user interacts with a Streamlit widget?",
     "options":["Only the widget's callback runs","The entire app.py script re-runs from top to bottom","Only the changed section re-renders","The database connection is reset"],
     "correct":"The entire app.py script re-runs from top to bottom",
     "answer":"This is the Streamlit execution model. Every widget interaction triggers a full rerun. Understanding this prevents bugs like re-initialising data on every click."},
    {"type":"mc","q":"What must st.set_page_config() always be?",
     "options":["The last line of app.py","Called inside a function","The first Streamlit call in the script, before any other st.* calls","Inside the main tab block"],
     "correct":"The first Streamlit call in the script, before any other st.* calls",
     "answer":"If anything else runs first, Streamlit raises StreamlitAPIException. It must be called before any output."},
    {"type":"mc","q":"Which Streamlit function creates a multi-tab layout?",
     "options":["st.sidebar()","st.columns()","st.tabs()","st.container()"],
     "correct":"st.tabs()",
     "answer":"tab1, tab2 = st.tabs(['New Request', 'All Requests']) creates two tabs. Content inside with tab1: appears on the first tab."},
    {"type":"mc","q":"What does st.session_state allow you to do?",
     "options":["Store values that persist across reruns within the same user session","Connect to a database","Cache expensive computations permanently","Share data between different users"],
     "correct":"Store values that persist across reruns within the same user session",
     "answer":"Normal Python variables reset on every rerun. session_state survives reruns, making it essential for counters and form state."},
    {"type":"mc","q":"What does st.success('Done!') display?",
     "options":["A red error banner","A yellow warning","A green success banner","A modal dialog"],
     "correct":"A green success banner",
     "answer":"Streamlit has st.success() (green), st.error() (red), st.warning() (yellow), and st.info() (blue) for user feedback."},
    {"type":"ct","q":"What does this code display when the text box is empty and the button is clicked?",
     "code":"name = st.text_input('Your name')\nif st.button('Submit'):\n    if name:\n        st.success(f'Hello, {name}!')\n    else:\n        st.warning('Please enter your name.')",
     "answer":"A yellow warning: 'Please enter your name.' — When name is empty (falsy), the else branch runs and st.warning() displays a yellow banner."},
    {"type":"tf","q":"Streamlit reruns the entire script even when only one widget changes.",
     "answer":"True — Streamlit reruns everything on every interaction. This makes state management simple; the trade-off is that expensive operations run on every click unless cached with @st.cache_data."},
    {"type":"tf","q":"st.dataframe() can display a list of dicts directly.",
     "answer":"True — st.dataframe() accepts a list of dicts, a pandas DataFrame, or any sequence that can be converted to a table. It renders an interactive, sortable table automatically."},
    {"type":"sa","q":"What are the five required features every ISM3232 Streamlit capstone app must include?",
     "answer":"(1) New request form with inputs and a submit button; (2) All requests view displaying a dataframe of all database records; (3) Update status tab to change a record's status by id; (4) Status report showing counts or totals per status; (5) st.set_page_config() at the top with a descriptive title and wide layout."},
  ]
},

16: {
  "title": "GenAI Feature & Final Demo",
  "midterm": False,
  "questions": [
    {"type":"mc","q":"What is the primary privacy concern when passing data to an external AI API?",
     "options":["The API might be slow","Sensitive or identifying data may be stored or logged by the provider","The API might return incorrect JSON","The API call increases the database file size"],
     "correct":"Sensitive or identifying data may be stored or logged by the provider",
     "answer":"ISM3232 requires sending only non-identifying fields (category, description) to the API, never names, IDs, or financial totals."},
    {"type":"mc","q":"What does the ISM3232 AI disclosure control require?",
     "options":["A pop-up warning before the page loads","A visible label or banner whenever AI-generated content is displayed","A log file recording every API call","An admin approval for each AI response"],
     "correct":"A visible label or banner whenever AI-generated content is displayed",
     "answer":"Users must always know when they are reading AI-generated text. Use st.info() or an explicit 'AI-generated summary' label."},
    {"type":"mc","q":"What is mocking in the context of testing an AI feature?",
     "options":["Writing fake test data for the database","Replacing the real API call with a controlled fake that returns a predictable response","Running the AI in offline mode","Testing only the UI, not the function"],
     "correct":"Replacing the real API call with a controlled fake that returns a predictable response",
     "answer":"unittest.mock.patch replaces the Anthropic client during tests so tests make no real API calls, incur no cost, and do not fail due to network issues."},
    {"type":"ct","q":"What does this test verify?",
     "code":"def test_summarise_returns_text():\n    fake = MagicMock()\n    fake.text = 'A one-sentence summary.'\n    with patch('ai_feature.anthropic.Anthropic') as mock_client:\n        mock_client.return_value.messages.create.return_value.content = [fake]\n        result = summarise_request('Equipment', 'Laptop for dev work')\n    assert isinstance(result, str)",
     "answer":"That summarise_request() returns a string — The test mocks out the Anthropic client (no real API call), then asserts the return type is str. It does not test the content, only the return type."},
    {"type":"mc","q":"Which Anthropic API parameter caps the length of the AI response?",
     "options":["temperature","max_tokens","model","top_p"],
     "correct":"max_tokens",
     "answer":"max_tokens limits how many tokens the model generates. Setting it low (e.g., 100) for a one-sentence summary prevents runaway responses and controls cost."},
    {"type":"mc","q":"What is the required input control before sending user data to the AI?",
     "options":["Strip whitespace only","Validate and limit input: check non-empty, cap length, allow only expected values","Encrypt the input","Convert all text to uppercase"],
     "correct":"Validate and limit input: check non-empty, cap length, allow only expected values",
     "answer":"Control 2 of the six required controls. Always validate before the API call: reject empty input, enforce length limits, restrict to expected categories."},
    {"type":"tf","q":"The Anthropic client should be created inside the function that calls the API, not at the module level.",
     "answer":"True (by ISM3232 convention) — Creating the client inside the function makes it easier to mock in tests. A module-level client requires more complex patching to replace during testing."},
    {"type":"tf","q":"AI-generated output may be displayed to users without any label or disclosure.",
     "answer":"False — ISM3232 requires an AI disclosure label whenever AI-generated content is shown. Users must always know what was written by a human and what was generated by AI."},
    {"type":"sa","q":"What are the six required AI controls in the ISM3232 GenAI feature, and why does each matter?",
     "answer":"(1) Disclosure — users see a label on AI output (honesty); (2) Input validation — reject empty or too-long input before the call (safety); (3) Input scoping — send only non-identifying fields (privacy); (4) Output guardrail — validate or trim AI output before display (reliability); (5) max_tokens limit — prevent runaway responses (cost and UX); (6) Error handling — show a user-friendly message on API failure, not a traceback (resilience)."},
  ]
},

} # end QUIZZES


# ── HTML generation ───────────────────────────────────────────────────────────

def _esc(text: str) -> str:
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&#x27;"))


def question_html(idx: int, q: dict) -> str:
    n   = idx + 1
    typ = q["type"]
    qtext = _esc(q["q"])
    ans   = q["answer"]

    # split answer into main answer + explanation (split on first " — ")
    if " — " in ans:
        ans_main, ans_expl = ans.split(" — ", 1)
    else:
        ans_main, ans_expl = ans, ""

    if typ == "mc":
        opts = q["options"]
        correct = _esc(q["correct"])
        type_label = "Multiple Choice"
        opts_html = "\n".join(f'<li>{chr(97+i)}) {_esc(o)}</li>' for i, o in enumerate(opts))
        opts_block = f'<ul class="quiz-options">\n{opts_html}\n</ul>\n'
        expl_span = f' <span style="color:var(--muted);">— {_esc(ans_expl)}</span>' if ans_expl else ""
        answer_block = (f'<details class="quiz-answer"><summary>Answer</summary>'
                        f'<div style="margin-top:8px;">{_esc(ans_main)}{expl_span}</div></details>')

    elif typ == "tf":
        type_label = "True / False"
        opts_block = ""
        expl_span = f' <span style="color:var(--muted);">— {_esc(ans_expl)}</span>' if ans_expl else ""
        answer_block = (f'<details class="quiz-answer"><summary>Answer</summary>'
                        f'<div style="margin-top:8px;">{_esc(ans_main)}{expl_span}</div></details>')

    elif typ == "sa":
        type_label = "Short Answer"
        opts_block = ""
        answer_block = (f'<details class="quiz-answer"><summary>Answer</summary>'
                        f'<div style="margin-top:8px;">{_esc(ans)}</div></details>')

    else:  # ct — code trace
        type_label = "Code Trace"
        opts_block = f'<pre><code>{_esc(q["code"])}</code></pre>\n'
        expl_span = f' <span style="color:var(--muted);">— {_esc(ans_expl)}</span>' if ans_expl else ""
        answer_block = (f'<details class="quiz-answer"><summary>Answer</summary>'
                        f'<div style="margin-top:8px;">{_esc(ans_main)}{expl_span}</div></details>')

    return (f'<div class="quiz-item">\n'
            f'<div class="quiz-q">Q{n} · {type_label}</div>\n'
            f'<div class="quiz-question">{qtext}</div>\n'
            f'{opts_block}'
            f'{answer_block}\n'
            f'</div>\n')


def quiz_section(week: int, data: dict) -> str:
    mid_badge = (
        " <span style=\"font-family:'JetBrains Mono',ui-monospace,monospace;font-size:11px;font-weight:400;"
        "color:var(--accent);letter-spacing:.12em;margin-left:10px;\">&#9733; Midterm-Eligible</span>"
        if data["midterm"] else ""
    )
    lede = ("Quiz questions repeat on the exam verbatim or with minor variation. Click each answer to reveal it."
            if data["midterm"]
            else "Test your understanding before moving on. Click each answer to reveal it.")
    qs_html = "".join(question_html(i, q) for i, q in enumerate(data["questions"]))
    return (f'\n<h2 id="quiz">Module Quiz{mid_badge}</h2>\n'
            f'<p class="lede" style="font-size:14.5px;">{lede}</p>\n\n'
            f'{qs_html}')


# ── CSS to add to site.css ────────────────────────────────────────────────────

_MONO = "'JetBrains Mono', ui-monospace, monospace"

QUIZ_CSS = f"""
/* ── module quiz ─────────────────────────────────────────────────── */
.quiz-item {{
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 10px; padding: 16px 20px; margin: 14px 0;
}}
.quiz-q {{
  font-family: {_MONO}; font-size: 11px; letter-spacing: .12em;
  text-transform: uppercase; color: var(--accent); margin-bottom: 8px;
}}
.quiz-question {{ font-weight: 600; margin-bottom: 10px; }}
.quiz-item > pre {{ margin: 8px 0 10px; font-size: 12.5px; }}
.quiz-options {{
  list-style: none; padding: 0; margin: 8px 0;
  font-family: {_MONO}; font-size: 13px;
}}
.quiz-options li {{ padding: 3px 0; color: var(--muted); }}
.quiz-answer {{ margin-top: 10px; font-size: 13.5px; }}
.quiz-answer summary {{
  cursor: pointer; color: var(--muted);
  font-family: {_MONO}; font-size: 11px;
  letter-spacing: .08em; text-transform: uppercase; list-style: none;
}}
.quiz-answer summary::-webkit-details-marker {{ display: none; }}
.quiz-answer summary::before {{ content: '▸ '; }}
.quiz-answer[open] summary::before {{ content: '▾ '; }}
"""

# ── main ──────────────────────────────────────────────────────────────────────

# 1. Add quiz CSS to site.css
css_content = CSS.read_text(encoding="utf-8")
if ".quiz-item" not in css_content:
    CSS.write_text(css_content + QUIZ_CSS, encoding="utf-8")
    print("✓ Added quiz CSS to site.css")
else:
    print("  quiz CSS already in site.css — skipped")

# 2. Inject quiz sections into reading pages
for week, data in QUIZZES.items():
    path = DOCS / f"week{week:02d}_reading.html"
    content = path.read_text(encoding="utf-8")
    if 'id="quiz"' in content:
        print(f"  week{week:02d}: quiz already present — skipped")
        continue
    section = quiz_section(week, data)
    if ANCHOR not in content:
        print(f"  week{week:02d}: WARNING — anchor not found, skipping")
        continue
    content = content.replace(ANCHOR, section + "\n" + ANCHOR)
    path.write_text(content, encoding="utf-8")
    print(f"✓ week{week:02d}: injected {len(data['questions'])} questions ({data['title']})")

print("\nDone.")
