# Responsive Design Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a hamburger nav (≤768px), tablet CSS rules, and index-page tablet tweaks to both ISM2411 and ISM3232 static course sites.

**Architecture:** Hamburger CSS and tablet layout rules go into each course's shared `site.css` (loaded by every page). Hamburger HTML and toggle JS go into `site.js` (which injects the nav at runtime). Index pages get their existing `max-width:640px` media query widened to `768px`.

**Tech Stack:** Vanilla CSS, vanilla JS (IIFE pattern), static HTML. No build step. Changes are per-file edits; test by opening in a browser and resizing.

---

## File Map

| File | Change |
|---|---|
| `ism2411/assets/css/site.css` | Append hamburger CSS + `.nav-mobile-panel` + `@media(max-width:768px)` tablet block |
| `ism2411/assets/js/site.js` | Add hamburger button to nav HTML; inject mobile panel; add hamburger + panel JS; update `setTheme` |
| `ism2411/index.html` | Change `max-width:640px` → `768px`; add `.sec-count{display:none}` |
| `ism3232/site.css` | Same CSS additions as ISM2411 |
| `ism3232/site.js` | Same JS additions as ISM2411 (different nav links and `ism3232-` storage keys) |
| `ism3232/index.html` | Change `max-width:640px` → `768px` (`.sec-count` rule already present) |

---

## Task 1: ISM2411 — Hamburger CSS + Tablet Rules

**Files:** `ism2411/assets/css/site.css`

- [ ] **Step 1: Append hamburger + panel + tablet CSS block**

Open `ism2411/assets/css/site.css`. At the very end of the file, after the existing `:focus-visible` block, append:

```css
/* ── Hamburger button (hidden on desktop) ────────────────────────────── */
.nav-hamburger {
  display: none;
  background: none; border: 1px solid rgba(255,255,255,.12);
  color: #cfcfd9; cursor: pointer;
  width: 34px; height: 34px; border-radius: 6px;
  font-size: 18px; align-items: center; justify-content: center;
  flex-shrink: 0;
  transition: background .15s;
}
[data-theme="light"] .nav-hamburger { color: #2a2a35; border-color: rgba(0,0,0,.12); }
.nav-hamburger:hover { background: rgba(255,255,255,.08); }
[data-theme="light"] .nav-hamburger:hover { background: rgba(0,0,0,.05); }

/* ── Mobile nav panel ────────────────────────────────────────────────── */
.nav-mobile-panel {
  display: none; position: fixed;
  top: 49px; left: 0; right: 0;
  background: #1a1a26;
  border-bottom: 1px solid rgba(255,255,255,.1);
  padding: 16px 20px 24px; z-index: 99;
  box-shadow: 0 12px 40px rgba(0,0,0,.5);
  max-height: calc(100vh - 49px);
  overflow-y: auto;
}
[data-theme="light"] .nav-mobile-panel {
  background: #fff;
  border-bottom-color: rgba(0,0,0,.1);
  box-shadow: 0 12px 40px rgba(0,0,0,.15);
}
.nav-mobile-panel.open { display: block; }

.mob-section { margin-bottom: 16px; }
.mob-section-label {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 10px; letter-spacing: .18em;
  color: #6e6e80; text-transform: uppercase;
  padding: 0 0 6px; margin-bottom: 4px;
  border-bottom: 1px solid rgba(255,255,255,.06);
}
[data-theme="light"] .mob-section-label { color: #8a8a9c; border-bottom-color: rgba(0,0,0,.08); }
.mob-section a {
  display: block; padding: 7px 4px;
  color: #cfcfd9; text-decoration: none;
  font-size: 13px; border-radius: 4px;
  transition: background .12s;
}
[data-theme="light"] .mob-section a { color: #2a2a35; }
.mob-section a:hover { background: rgba(255,255,255,.06); }
[data-theme="light"] .mob-section a:hover { background: rgba(0,0,0,.05); }

.mob-tools {
  display: flex; gap: 8px; align-items: center;
  padding-top: 12px; margin-top: 4px;
  border-top: 1px solid rgba(255,255,255,.08);
}
[data-theme="light"] .mob-tools { border-top-color: rgba(0,0,0,.08); }
.mob-tools .tool-btn { width: 36px; height: 36px; font-size: 14px; }

/* ── ≤768px: show hamburger, hide desktop nav items ─────────────────── */
@media (max-width: 768px) {
  .nav-hamburger { display: inline-flex; }
  .ism-nav .nav-dd,
  .ism-nav .nav-tools { display: none; }
}

/* ── ≤768px: tablet layout rules ────────────────────────────────────── */
@media (max-width: 768px) {
  pre, code { overflow-x: auto; max-width: 100%; }
  img { max-width: 100%; height: auto; }
  .two-col { grid-template-columns: 1fr !important; }
}
```

- [ ] **Step 2: Verify CSS file ends correctly**

Run:
```bash
tail -10 /home/markumreed/Documents/ism_courses/ism2411/assets/css/site.css
```
Expected: last lines show the `@media (max-width: 768px)` tablet block closing `}`.

---

## Task 2: ISM2411 — Hamburger HTML + JS in site.js

**Files:** `ism2411/assets/js/site.js`

The nav IIFE has three sections to update: `setTheme`, the nav `innerHTML` template, and the event listener block at the bottom.

- [ ] **Step 1: Update `setTheme` to sync mobile theme button**

Find this block (lines ~17–22):
```javascript
  function setTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    localStorage.setItem('ism2411-theme', t);
    const btn = document.getElementById('ism-theme-btn');
    if (btn) btn.textContent = t === 'dark' ? '☀' : '☾';
  }
```

Replace it with:
```javascript
  function setTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    localStorage.setItem('ism2411-theme', t);
    const icon = t === 'dark' ? '☀' : '☾';
    const btn = document.getElementById('ism-theme-btn');
    if (btn) btn.textContent = icon;
    const mobBtn = document.getElementById('ism-mob-theme-btn');
    if (mobBtn) mobBtn.textContent = icon;
  }
```

- [ ] **Step 2: Add hamburger button to nav HTML template**

Inside the `nav.innerHTML = \`...\`` template, after the closing `</div>` of `.nav-tools`, add:
```html
    <button class="nav-hamburger" id="ism-hamburger" aria-label="Open navigation" aria-expanded="false">☰</button>
```

The end of the nav innerHTML should look like:
```html
    <div class="nav-tools">
      <button id="ism-font-down" class="tool-btn" aria-label="Decrease font size" title="Smaller text">A−</button>
      <button id="ism-font-up" class="tool-btn" aria-label="Increase font size" title="Larger text">A+</button>
      <button id="ism-theme-btn" class="tool-btn" aria-label="Toggle theme" title="Light / dark">${initialTheme === 'dark' ? '☀' : '☾'}</button>
    </div>
    <button class="nav-hamburger" id="ism-hamburger" aria-label="Open navigation" aria-expanded="false">☰</button>
  `;
```

- [ ] **Step 3: Inject mobile panel after the nav**

Find this block (after the nav innerHTML assignment, around the insert section):
```javascript
  document.body.prepend(nav);
  document.body.prepend(skip);
```

Replace with:
```javascript
  // ── mobile nav panel ──────────────────────────────────────────────────
  const panel = document.createElement('div');
  panel.className = 'nav-mobile-panel';
  panel.id = 'nav-mobile-panel';
  panel.innerHTML = `
    <div class="mob-section">
      <div class="mob-section-label">Start Here</div>
      <a href="${pg}precourse.html">Pre-course Setup</a>
      <a href="${pg}syllabus.html">Syllabus</a>
      <a href="${pg}unit_all_overview.html">All Units Overview</a>
    </div>
    <div class="mob-section">
      <div class="mob-section-label">Unit 1 · Foundations</div>
      <a href="${pg}unit_1_overview.html">Overview</a>
      <a href="${pg}unit_1_cheatsheet.html">Cheat Sheet</a>
      <a href="${pg}week01_reading.html">Module 1 · What is a Computer?</a>
      <a href="${pg}week02_reading.html">Module 2 · The Command Line</a>
      <a href="${pg}week03_reading.html">Module 3 · Variables &amp; Data Types</a>
      <a href="${pg}week04_reading.html">Module 4 · Operators</a>
      <a href="${pg}week05_reading.html">Module 5 · Conditionals</a>
    </div>
    <div class="mob-section">
      <div class="mob-section-label">Unit 2 · Control Flow</div>
      <a href="${pg}unit_2_overview.html">Overview</a>
      <a href="${pg}unit_2_cheatsheet.html">Cheat Sheet</a>
      <a href="${pg}week06_reading.html">Module 6 · Loops</a>
      <a href="${pg}week07_reading.html">Module 7 · Functions &amp; AI Literacy</a>
      <a href="${pg}week08_reading.html">Module 8 · Git &amp; GitHub</a>
      <a href="${pg}week09_midterm.html">Module 9 · Midterm</a>
    </div>
    <div class="mob-section">
      <div class="mob-section-label">Unit 3 · Data Structures</div>
      <a href="${pg}unit_3_overview.html">Overview</a>
      <a href="${pg}unit_3_cheatsheet.html">Cheat Sheet</a>
      <a href="${pg}week10_reading.html">Module 10 · Lists &amp; Tuples</a>
      <a href="${pg}week11_reading.html">Module 11 · Dictionaries</a>
      <a href="${pg}week12_reading.html">Module 12 · Files &amp; CSVs</a>
    </div>
    <div class="mob-section">
      <div class="mob-section-label">Unit 4 · pandas</div>
      <a href="${pg}unit_4_overview.html">Overview</a>
      <a href="${pg}unit_4_cheatsheet.html">Cheat Sheet</a>
      <a href="${pg}week13_reading.html">Module 13 · Intro to pandas</a>
      <a href="${pg}week14_reading.html">Module 14 · Cleaning &amp; Stats</a>
      <a href="${pg}week15_reading.html">Module 15 · Grouping &amp; Charts</a>
    </div>
    <div class="mob-section">
      <div class="mob-section-label">Unit 5 · Capstone</div>
      <a href="${pg}unit_5_overview.html">Overview</a>
      <a href="${pg}week16_capstone.html">Module 16 · Capstone Build</a>
    </div>
    <div class="mob-tools">
      <button id="ism-mob-font-down" class="tool-btn" aria-label="Decrease font size" title="Smaller text">A−</button>
      <button id="ism-mob-font-up" class="tool-btn" aria-label="Increase font size" title="Larger text">A+</button>
      <button id="ism-mob-theme-btn" class="tool-btn" aria-label="Toggle theme" title="Light / dark">${initialTheme === 'dark' ? '☀' : '☾'}</button>
    </div>
  `;

  document.body.prepend(nav);
  document.body.prepend(skip);
  nav.after(panel);
```

- [ ] **Step 4: Add hamburger toggle JS at the bottom of the IIFE**

After the existing `// ── font buttons` block and before the closing `})();`, append:

```javascript
  // ── hamburger / mobile panel ─────────────────────────────────────────
  const hamburger = document.getElementById('ism-hamburger');

  function openPanel() {
    panel.classList.add('open');
    hamburger.textContent = '✕';
    hamburger.setAttribute('aria-expanded', 'true');
    hamburger.setAttribute('aria-label', 'Close navigation');
  }
  function closePanel() {
    panel.classList.remove('open');
    hamburger.textContent = '☰';
    hamburger.setAttribute('aria-expanded', 'false');
    hamburger.setAttribute('aria-label', 'Open navigation');
  }

  hamburger.addEventListener('click', e => {
    e.stopPropagation();
    panel.classList.contains('open') ? closePanel() : openPanel();
  });
  document.addEventListener('click', e => {
    if (panel.classList.contains('open') && !nav.contains(e.target) && !panel.contains(e.target)) {
      closePanel();
    }
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && panel.classList.contains('open')) closePanel();
  });
  panel.querySelectorAll('a').forEach(a => a.addEventListener('click', closePanel));
  window.addEventListener('resize', () => {
    if (window.innerWidth > 768 && panel.classList.contains('open')) closePanel();
  });

  // ── mobile tool buttons ──────────────────────────────────────────────
  document.getElementById('ism-mob-theme-btn').addEventListener('click', () => {
    const cur = document.documentElement.getAttribute('data-theme');
    setTheme(cur === 'dark' ? 'light' : 'dark');
  });
  document.getElementById('ism-mob-font-up').addEventListener('click', () => {
    if (fontIdx < fontSizes.length - 1) { fontIdx++; applyFont(); }
  });
  document.getElementById('ism-mob-font-down').addEventListener('click', () => {
    if (fontIdx > 0) { fontIdx--; applyFont(); }
  });
```

Note: `panel`, `nav`, `hamburger`, `fontIdx`, `fontSizes`, `applyFont`, and `setTheme` are all in scope because they are declared in the same IIFE.

- [ ] **Step 5: Verify site.js structure**

Run:
```bash
grep -n 'nav-hamburger\|nav-mobile-panel\|ism-mob-theme\|closePanel\|openPanel' /home/markumreed/Documents/ism_courses/ism2411/assets/js/site.js
```
Expected: lines matching each of those identifiers.

---

## Task 3: ISM2411 — index.html tablet media query

**Files:** `ism2411/index.html`

- [ ] **Step 1: Widen mobile media query and add `.sec-count` rule**

Find:
```css
@media (max-width: 640px) {
  .precourse-card { grid-template-columns: 1fr; text-align: center; }
  .pc-arrow { display: none; }
  .unit-head { flex-wrap: wrap; }
}
```

Replace with:
```css
@media (max-width: 768px) {
  .precourse-card { grid-template-columns: 1fr; text-align: center; }
  .pc-arrow { display: none; }
  .unit-head { flex-wrap: wrap; }
  .sec-count { display: none; }
}
```

- [ ] **Step 2: Verify change**

Run:
```bash
grep -n 'max-width' /home/markumreed/Documents/ism_courses/ism2411/index.html
```
Expected: one line showing `max-width: 768px` (not 640px).

---

## Task 4: Commit ISM2411

- [ ] **Step 1: Stage and commit**

```bash
cd /home/markumreed/Documents/ism_courses/ism2411
git add assets/css/site.css assets/js/site.js index.html
git commit -m "Add hamburger nav (≤768px), tablet CSS rules, and index breakpoint

- Hamburger at ≤768px hides desktop nav, shows slide-down panel with all links + tools
- Tablet @media(max-width:768px) in site.css: pre overflow, img max-width, .two-col stack
- index.html: widen media query from 640px to 768px, add .sec-count hide rule

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

Expected: commit succeeds, shows 3 files changed.

---

## Task 5: ISM3232 — Hamburger CSS + Tablet Rules

**Files:** `ism3232/site.css`

- [ ] **Step 1: Append hamburger + panel + tablet CSS block**

Open `ism3232/site.css`. At the very end of the file (after the `.weekjump-link.current` and `.wk-deck` and `.wrap` and `.lede` blocks), append:

```css
/* ── Hamburger button (hidden on desktop) ────────────────────────────── */
.nav-hamburger {
  display: none;
  background: none; border: 1px solid rgba(255,255,255,.12);
  color: #cfcfd9; cursor: pointer;
  width: 34px; height: 34px; border-radius: 6px;
  font-size: 18px; align-items: center; justify-content: center;
  flex-shrink: 0;
  transition: background .15s;
}
[data-theme="light"] .nav-hamburger { color: #2a2a35; border-color: rgba(0,0,0,.12); }
.nav-hamburger:hover { background: rgba(255,255,255,.08); }
[data-theme="light"] .nav-hamburger:hover { background: rgba(0,0,0,.05); }

/* ── Mobile nav panel ────────────────────────────────────────────────── */
.nav-mobile-panel {
  display: none; position: fixed;
  top: 49px; left: 0; right: 0;
  background: #1a1a26;
  border-bottom: 1px solid rgba(255,255,255,.1);
  padding: 16px 20px 24px; z-index: 99;
  box-shadow: 0 12px 40px rgba(0,0,0,.5);
  max-height: calc(100vh - 49px);
  overflow-y: auto;
}
[data-theme="light"] .nav-mobile-panel {
  background: #fff;
  border-bottom-color: rgba(0,0,0,.1);
  box-shadow: 0 12px 40px rgba(0,0,0,.15);
}
.nav-mobile-panel.open { display: block; }

.mob-section { margin-bottom: 16px; }
.mob-section-label {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 10px; letter-spacing: .18em;
  color: #6e6e80; text-transform: uppercase;
  padding: 0 0 6px; margin-bottom: 4px;
  border-bottom: 1px solid rgba(255,255,255,.06);
}
[data-theme="light"] .mob-section-label { color: #8a8a9c; border-bottom-color: rgba(0,0,0,.08); }
.mob-section a {
  display: block; padding: 7px 4px;
  color: #cfcfd9; text-decoration: none;
  font-size: 13px; border-radius: 4px;
  transition: background .12s;
}
[data-theme="light"] .mob-section a { color: #2a2a35; }
.mob-section a:hover { background: rgba(255,255,255,.06); }
[data-theme="light"] .mob-section a:hover { background: rgba(0,0,0,.05); }

.mob-tools {
  display: flex; gap: 8px; align-items: center;
  padding-top: 12px; margin-top: 4px;
  border-top: 1px solid rgba(255,255,255,.08);
}
[data-theme="light"] .mob-tools { border-top-color: rgba(0,0,0,.08); }
.mob-tools .tool-btn { width: 36px; height: 36px; font-size: 14px; }

/* ── ≤768px: show hamburger, hide desktop nav items ─────────────────── */
@media (max-width: 768px) {
  .nav-hamburger { display: inline-flex; }
  .ism-nav .nav-dd,
  .ism-nav .nav-tools { display: none; }
}

/* ── ≤768px: tablet layout rules ────────────────────────────────────── */
@media (max-width: 768px) {
  pre, code { overflow-x: auto; max-width: 100%; }
  img { max-width: 100%; height: auto; }
  .two-col { grid-template-columns: 1fr !important; }
}
```

- [ ] **Step 2: Verify**

```bash
tail -10 /home/markumreed/Documents/ism_courses/ism3232/site.css
```
Expected: ends with the `@media (max-width: 768px)` tablet block.

---

## Task 6: ISM3232 — Hamburger HTML + JS in site.js

**Files:** `ism3232/site.js`

- [ ] **Step 1: Update `setTheme` to sync mobile theme button**

Find:
```javascript
  function setTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    localStorage.setItem('ism3232-theme', t);
    const btn = document.getElementById('ism-theme-btn');
    if (btn) btn.textContent = t === 'dark' ? '☀' : '☾';
  }
```

Replace with:
```javascript
  function setTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    localStorage.setItem('ism3232-theme', t);
    const icon = t === 'dark' ? '☀' : '☾';
    const btn = document.getElementById('ism-theme-btn');
    if (btn) btn.textContent = icon;
    const mobBtn = document.getElementById('ism-mob-theme-btn');
    if (mobBtn) mobBtn.textContent = icon;
  }
```

- [ ] **Step 2: Add hamburger button to nav HTML template**

Inside the `nav.innerHTML = \`...\`` template in `ism3232/site.js`, add the hamburger button after the closing `</div>` of `.nav-tools`:

```html
    <div class="nav-tools">
      <button id="ism-font-down"   class="tool-btn" aria-label="Decrease font size" title="Smaller text">A−</button>
      <button id="ism-font-up"     class="tool-btn" aria-label="Increase font size" title="Larger text">A+</button>
      <button id="ism-theme-btn"   class="tool-btn" aria-label="Toggle theme" title="Light / dark">${initialTheme === 'dark' ? '☀' : '☾'}</button>
    </div>
    <button class="nav-hamburger" id="ism-hamburger" aria-label="Open navigation" aria-expanded="false">☰</button>
  `;
```

- [ ] **Step 3: Inject mobile panel after the nav**

Find:
```javascript
  document.body.prepend(nav);
  document.body.prepend(skip);
```

Replace with:
```javascript
  // ── mobile nav panel ──────────────────────────────────────────────────
  const panel = document.createElement('div');
  panel.className = 'nav-mobile-panel';
  panel.id = 'nav-mobile-panel';
  panel.innerHTML = `
    <div class="mob-section">
      <div class="mob-section-label">Start Here</div>
      <a href="${pg}precourse.html">Pre-Course Setup</a>
      <a href="${pg}syllabus.html">Syllabus</a>
      <a href="${pg}course_map.html">Course Map</a>
      <a href="${pg}unit_all_overview.html">All Units Overview</a>
    </div>
    <div class="mob-section">
      <div class="mob-section-label">Reference</div>
      <a href="${pg}unit_1_cheatsheet.html">Cheat Sheets</a>
      <a href="${pg}glossary.html">Glossary</a>
      <a href="${pg}troubleshooting.html">Help / Troubleshooting</a>
      <a href="${pg}capstone_rubric.html">Capstone Rubric</a>
      <a href="${pg}expectations.html">Expectations</a>
      <a href="${pg}slos.html">SLOs</a>
      <a href="${pg}slo_mindmap.html">SLO Mind Map</a>
    </div>
    <div class="mob-section">
      <div class="mob-section-label">Unit 1 · Developer Foundations</div>
      <a href="${pg}unit_1_overview.html">Overview</a>
      <a href="${pg}unit_1_cheatsheet.html">Cheat Sheet</a>
      <a href="${pg}week01_reading.html">Module 1 · Developer Mindset &amp; Setup</a>
      <a href="${pg}week02_reading.html">Module 2 · zsh Navigation &amp; File Ops</a>
      <a href="${pg}week03_reading.html">Module 3 · Virtual Environments &amp; .zshrc</a>
      <a href="${pg}week04_reading.html">Module 4 · Search Tools, Ritual &amp; Git</a>
    </div>
    <div class="mob-section">
      <div class="mob-section-label">Unit 2 · Python Foundations</div>
      <a href="${pg}unit_2_overview.html">Overview</a>
      <a href="${pg}unit_2_cheatsheet.html">Cheat Sheet</a>
      <a href="${pg}week05_reading.html">Module 5 · Variables, Types &amp; Operators</a>
      <a href="${pg}week06_reading.html">Module 6 · Conditionals, Loops &amp; Dicts</a>
      <a href="${pg}week07_reading.html">Module 7 · Functions, Modules &amp; pytest</a>
      <a href="${pg}week08_reading.html">Module 8 · Debugging &amp; AI Literacy</a>
      <a href="${pg}week09_reading.html">Module 9 · Midterm Review</a>
    </div>
    <div class="mob-section">
      <div class="mob-section-label">Unit 3 · Object-Oriented Design</div>
      <a href="${pg}unit_3_overview.html">Overview</a>
      <a href="${pg}unit_3_cheatsheet.html">Cheat Sheet</a>
      <a href="${pg}week10_reading.html">Module 10 · OOP I — Classes &amp; Objects</a>
      <a href="${pg}week11_reading.html">Module 11 · OOP II — Composition &amp; Inheritance</a>
      <a href="${pg}week12_reading.html">Module 12 · OOP III — Design &amp; Practice</a>
    </div>
    <div class="mob-section">
      <div class="mob-section-label">Unit 4 · Capstone Build</div>
      <a href="${pg}unit_4_overview.html">Overview</a>
      <a href="${pg}unit_4_cheatsheet.html">Cheat Sheet</a>
      <a href="${pg}week13_reading.html">Module 13 · Capstone Design &amp; SQL</a>
      <a href="${pg}week14_reading.html">Module 14 · Python + SQL Integration</a>
      <a href="${pg}week15_reading.html">Module 15 · Streamlit Interface</a>
      <a href="${pg}week16_reading.html">Module 16 · GenAI Feature &amp; Final Demo</a>
    </div>
    <div class="mob-tools">
      <button id="ism-mob-font-down" class="tool-btn" aria-label="Decrease font size" title="Smaller text">A−</button>
      <button id="ism-mob-font-up"   class="tool-btn" aria-label="Increase font size" title="Larger text">A+</button>
      <button id="ism-mob-theme-btn" class="tool-btn" aria-label="Toggle theme" title="Light / dark">${initialTheme === 'dark' ? '☀' : '☾'}</button>
    </div>
  `;

  document.body.prepend(nav);
  document.body.prepend(skip);
  nav.after(panel);
```

- [ ] **Step 4: Add hamburger toggle JS at bottom of IIFE**

After the existing `// ── font buttons` block and before the closing `})();`, append:

```javascript
  // ── hamburger / mobile panel ─────────────────────────────────────────
  const hamburger = document.getElementById('ism-hamburger');

  function openPanel() {
    panel.classList.add('open');
    hamburger.textContent = '✕';
    hamburger.setAttribute('aria-expanded', 'true');
    hamburger.setAttribute('aria-label', 'Close navigation');
  }
  function closePanel() {
    panel.classList.remove('open');
    hamburger.textContent = '☰';
    hamburger.setAttribute('aria-expanded', 'false');
    hamburger.setAttribute('aria-label', 'Open navigation');
  }

  hamburger.addEventListener('click', e => {
    e.stopPropagation();
    panel.classList.contains('open') ? closePanel() : openPanel();
  });
  document.addEventListener('click', e => {
    if (panel.classList.contains('open') && !nav.contains(e.target) && !panel.contains(e.target)) {
      closePanel();
    }
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && panel.classList.contains('open')) closePanel();
  });
  panel.querySelectorAll('a').forEach(a => a.addEventListener('click', closePanel));
  window.addEventListener('resize', () => {
    if (window.innerWidth > 768 && panel.classList.contains('open')) closePanel();
  });

  // ── mobile tool buttons ──────────────────────────────────────────────
  document.getElementById('ism-mob-theme-btn').addEventListener('click', () => {
    const cur = document.documentElement.getAttribute('data-theme');
    setTheme(cur === 'dark' ? 'light' : 'dark');
  });
  document.getElementById('ism-mob-font-up').addEventListener('click', () => {
    if (fontIdx < fontSizes.length - 1) { fontIdx++; applyFont(); }
  });
  document.getElementById('ism-mob-font-down').addEventListener('click', () => {
    if (fontIdx > 0) { fontIdx--; applyFont(); }
  });
```

- [ ] **Step 5: Verify site.js structure**

```bash
grep -n 'nav-hamburger\|nav-mobile-panel\|ism-mob-theme\|closePanel\|openPanel' /home/markumreed/Documents/ism_courses/ism3232/site.js
```
Expected: lines matching each identifier.

---

## Task 7: ISM3232 — index.html tablet media query

**Files:** `ism3232/index.html`

- [ ] **Step 1: Widen mobile media query to 768px**

Find:
```css
@media (max-width: 640px) {
  .hero { padding: 48px 20px 40px; }
  .main { padding: 0 16px 60px; }
  .unit-head { flex-wrap: wrap; }
  .precourse-card { grid-template-columns: 1fr; }
  .pre-arrow { display: none; }
  .sec-count { display: none; }
}
```

Replace with:
```css
@media (max-width: 768px) {
  .hero { padding: 48px 20px 40px; }
  .main { padding: 0 16px 60px; }
  .unit-head { flex-wrap: wrap; }
  .precourse-card { grid-template-columns: 1fr; }
  .pre-arrow { display: none; }
  .sec-count { display: none; }
}
```

- [ ] **Step 2: Verify**

```bash
grep -n 'max-width' /home/markumreed/Documents/ism_courses/ism3232/index.html
```
Expected: lines show `768px` (not `640px`) for the responsive block.

---

## Task 8: Commit ISM3232

- [ ] **Step 1: Stage and commit**

```bash
cd /home/markumreed/Documents/ism_courses/ism3232
git add site.css site.js index.html
git commit -m "Add hamburger nav (≤768px), tablet CSS rules, and index breakpoint

- Hamburger at ≤768px hides desktop nav, shows slide-down panel with all links + tools
- Tablet @media(max-width:768px) in site.css: pre overflow, img max-width, .two-col stack
- index.html: widen media query from 640px to 768px

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

Expected: commit succeeds, shows 3 files changed.

---

## Task 9: Update Parent Repo + Commit

- [ ] **Step 1: Commit submodule pointer updates and plan file**

```bash
cd /home/markumreed/Documents/ism_courses
git add ism2411 ism3232 docs/superpowers/plans/2026-05-29-responsive-design.md
git commit -m "Update submodule pointers — responsive nav + tablet CSS

Both courses: hamburger nav (≤768px), tablet layout rules in site.css,
index media query widened to 768px.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

- [ ] **Step 2: Push all three repos**

```bash
cd /home/markumreed/Documents/ism_courses/ism2411 && git push
cd /home/markumreed/Documents/ism_courses/ism3232 && git push
cd /home/markumreed/Documents/ism_courses && git push
```

Expected: all three push cleanly to origin/main.

---

## Manual Verification Checklist

After Task 9, open the following in a browser and resize to 768px or use DevTools mobile emulation:

- [ ] `ism2411/index.html` — hamburger appears, tapping opens panel with all unit links, `.sec-count` hidden
- [ ] `ism2411/pages/week01_lecture.html` — hamburger works, `pre` blocks scroll horizontally, `.two-col` stacks
- [ ] `ism3232/index.html` — hamburger appears, panel includes Reference section
- [ ] `ism3232/docs/week01_lecture.html` — hamburger works, `pre` blocks scroll, `.two-col` stacks
- [ ] Both sites at desktop (>768px) — hamburger is hidden, desktop nav works as before
- [ ] Dark mode + light mode — panel renders correctly in both themes
- [ ] Escape key closes panel
- [ ] Theme toggle and font size buttons in panel work
