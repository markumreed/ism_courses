# Video 12: AI Literacy — Using AI Tools Responsibly in Development

## YouTube Metadata

**Title:** AI Literacy for Programmers — When to Use AI & When Not To | ISM2411 / ISM3232
**Description:**
AI coding tools are powerful and widely used in industry — but using them wrong in a learning context stunts your growth and can compromise your academic integrity. This video gives you a clear framework for when AI helps, when it hurts, and how to use it in a way that builds real skills while staying within course policy.

Course pages: https://markumreed.github.io/ism2411/pages/week07_lecture.html · https://markumreed.github.io/ism3232/docs/week08_lecture.html

**Chapters:**
0:00 — AI tools are real, not going away
1:30 — Three modes: Explainer, Debugger, Generator
4:00 — When AI helps your learning
7:00 — When AI hurts your learning
9:30 — Disclosure requirements
11:30 — The one rule that protects you
13:00 — Recap

**Applies to:** ISM2411 Module 7 · ISM3232 Module 8

**Tags:** AI coding tools, AI literacy, ChatGPT programming, GitHub Copilot students, responsible AI use, AI academic integrity, ISM2411, ISM3232, python AI tools, AI for learning, coding with AI

---

## Script

### INTRO (0:00–1:30)

AI coding tools — ChatGPT, GitHub Copilot, Claude — are used by professional developers every day. They're not going away. In fact, knowing how to use them effectively is now a marketable skill. But in a learning environment, the same tools that accelerate an expert can short-circuit a beginner.

The difference is not the tool — it's the mode you're using it in. This video gives you a clear framework: three modes of AI use, which ones build skills, which ones destroy them, and what you need to disclose when you use AI in your coursework.

---

### THREE MODES (1:30–4:00)

Think of AI in three modes: **Explainer**, **Debugger**, and **Generator**.

**Mode 1 — Explainer.** You wrote code, or you read code, and you don't understand part of it. You ask the AI to explain it.

"Explain what `enumerate()` does in this loop."

This is almost always fine. You're using AI as an interactive textbook. Your understanding goes up.

**Mode 2 — Debugger.** Your code is broken. You've tried to fix it yourself for a reasonable amount of time and you're stuck. You show the AI your error and ask what's wrong.

"Here's my code and the traceback I'm getting. What's causing this TypeError?"

This is usually fine, with one important condition: **you must read and understand the fix before applying it.** If you paste the fix without understanding why it works, you learned nothing and will face the same bug again.

**Mode 3 — Generator.** You have an assignment prompt. You ask AI to write the solution for you.

"Write a Python function that calculates a tiered discount."

This is the dangerous mode in a learning context. The output might be correct. But you didn't build the skill. And when the exam asks you to write a tiered discount function from scratch — and it will — you'll have nothing.

---

### WHEN AI HELPS (4:00–7:00)

AI genuinely accelerates learning when used for these purposes:

**Understanding error messages.** Paste your traceback and ask "what does this mean?" The AI explains the error type, common causes, and what to look for. Then you go fix it yourself.

**Clarifying syntax.** "What's the difference between `=` and `==` in Python?" Faster than a web search, with context.

**Seeing alternative approaches.** After you've written your solution, ask "how might an experienced Python developer approach this differently?" You learn patterns. You don't replace your work — you compare.

**Code review.** "Here's my function. What would make it more readable or efficient?" This is how professionals use AI — to improve existing code, not to generate from nothing.

**Learning new APIs.** "Show me a minimal example of reading a CSV with pandas." Boilerplate is a reasonable thing to generate — understanding it is still your job.

---

### WHEN AI HURTS (7:00–9:30)

Avoid these patterns:

**Generating solutions before attempting them yourself.** The struggle of writing code that doesn't work — and debugging it — is where learning happens. Skip the struggle, skip the learning. Every assignment in this course is designed to be doable with the material covered. Try it first. Spend at least 20 minutes genuinely trying before you reach for AI.

**Accepting AI output without reading it.** AI makes mistakes. Subtle logic errors, deprecated syntax, code that "looks right" but doesn't handle edge cases. If you don't understand the output, you can't catch these mistakes. And your name is on the submission.

**Using AI in ways that prevent spaced repetition.** You need to see the same concept multiple times, at increasing difficulty, to truly learn it. If AI always supplies the answer the first time, you never build the retrieval practice that makes knowledge stick. The exam doesn't have an AI.

**Generating explanations to paste into reflection assignments.** If the assignment asks you to explain your approach, the explanation should come from your understanding — not from a prompt.

---

### DISCLOSURE (9:30–11:30)

Both ISM2411 and ISM3232 require disclosure when you use AI assistance.

What to disclose:
- Which tool you used (ChatGPT, Copilot, Claude, etc.)
- What you asked it for (explanation, debugging help, code review)
- How you used its output (understood and adapted it, or used it directly)

Where to disclose: in a comment at the top of your file, or in the Canvas submission notes.

```python
# AI assistance: Used ChatGPT to explain the TypeError on line 14.
# Understood the fix (needed int() conversion) and applied it myself.
```

What does NOT require disclosure: using AI as a dictionary or syntax reference — "what's the syntax for a for loop?" is equivalent to googling it.

What DOES require disclosure: getting code written or debugged by AI, even partially.

Non-disclosure of AI use when it materially affected your submission is an academic integrity violation. The disclosure requirement protects you — it keeps AI a legitimate tool instead of a secret one.

---

### THE ONE RULE (11:30–13:00)

Here's the rule that covers every edge case: **you must be able to explain every line of code you submit.**

If AI wrote 5 lines and you can explain all 5 — what they do, why they work, what would break if you changed them — then you've actually learned from the interaction. Disclose it and submit with confidence.

If AI wrote 5 lines and you're not sure what they do — don't submit them. Go back, research until you understand, then submit.

This rule also protects you from submitting AI-generated bugs. If you can't read the code, you can't catch the errors.

---

### RECAP (13:00–15:00)

- AI tools are legitimate and widely used professionally — learn to use them well
- **Explainer mode:** understand concepts and errors — almost always fine
- **Debugger mode:** get help when genuinely stuck — fine with disclosure and understanding
- **Generator mode:** write your code for you — avoid for learning assignments
- Always try yourself first — the struggle is the learning
- Never submit code you can't explain line by line
- Disclose AI use clearly and specifically when it affected your work

The goal isn't to avoid AI. The goal is to use it in ways that make you more capable — not less.
