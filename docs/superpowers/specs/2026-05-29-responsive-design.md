# Responsive Design — ISM2411 & ISM3232
**Date:** 2026-05-29  
**Status:** Approved

---

## Context

Both course sites are static HTML with a shared design system. Mobile breakpoints (600px) were injected into all inner pages via `_add_mobile.py`. This spec covers the remaining responsive work: hamburger nav (≤768px), tablet CSS in shared `site.css`, and index page tablet tweaks.

---

## Breakpoint System

| Range | Label | Trigger |
|---|---|---|
| ≤ 600px | Mobile | Injected sentinel (done) |
| ≤ 768px | Tablet / hamburger | This spec |
| 769px+ | Desktop | No changes needed |

---

## Section 1 — Nav Hamburger (≤ 768px)

### Files
- `ism2411/assets/css/site.css`
- `ism2411/assets/js/site.js`
- `ism3232/site.css`
- `ism3232/site.js`

### Behavior
- At `≤768px`: hide all `.nav-dd` buttons and `.nav-tools` group; show a `☰` hamburger button (right side of nav).
- Clicking `☰` toggles a full-width slide-down panel below the sticky nav bar.
- Panel contains: all unit/page navigation links (same links as the desktop dropdowns) + theme toggle + font size buttons.
- Panel closes on: button re-click, outside click, `Escape` key, or clicking any link inside the panel.
- At `>768px`: hamburger hidden, desktop nav unchanged.

### CSS additions to `site.css`
```css
/* hamburger button — hidden on desktop */
.nav-hamburger {
  display: none;
  background: none; border: 1px solid rgba(255,255,255,.12);
  color: #cfcfd9; cursor: pointer;
  width: 34px; height: 34px; border-radius: 6px;
  font-size: 16px; align-items: center; justify-content: center;
  transition: background .15s;
}
[data-theme="light"] .nav-hamburger { color: #2a2a35; border-color: rgba(0,0,0,.12); }
.nav-hamburger:hover { background: rgba(255,255,255,.08); }

/* mobile nav panel */
.nav-mobile-panel {
  display: none; position: fixed;
  top: 49px; left: 0; right: 0;  /* 49px = nav padding (10+10) + button height (28px) + border (1px) */
  background: #1a1a26; border-bottom: 1px solid rgba(255,255,255,.1);
  padding: 12px 16px 20px; z-index: 99;
  box-shadow: 0 12px 40px rgba(0,0,0,.5);
}
[data-theme="light"] .nav-mobile-panel {
  background: #fff; border-bottom-color: rgba(0,0,0,.1);
}
.nav-mobile-panel.open { display: block; }

@media (max-width: 768px) {
  .nav-hamburger { display: inline-flex; }
  .ism-nav .nav-dd,
  .ism-nav .nav-tools { display: none; }
}
```

### JS additions to `site.js`
- Inject `.nav-hamburger` button into nav HTML.
- On click: toggle `.nav-mobile-panel.open`; update `aria-expanded`; swap `☰` ↔ `✕`.
- `document.addEventListener('click')` — close if click target is outside nav + panel.
- `document.addEventListener('keydown')` — close on `Escape`.
- Panel link clicks — close panel.
- On resize past 768px — close panel if open.

---

## Section 2 — Tablet Rules in `site.css`

One `@media(max-width:768px)` block added to both `site.css` files covering classes that appear across inner pages.

```css
@media (max-width: 768px) {
  /* code blocks — scroll horizontally rather than break page layout */
  pre, code { overflow-x: auto; max-width: 100%; }

  /* images never overflow their container */
  img { max-width: 100%; height: auto; }

  /* two-column grids stack before columns get too narrow */
  .two-col { grid-template-columns: 1fr !important; }
}
```

**Note:** YouTube iframes are already wrapped in a responsive `position:relative; padding-bottom:56.25%` container via inline styles on each lecture page — no additional CSS needed. `.wrap` uses `clamp()` — no tablet change needed. `.pn`, `.vpl-tile`, `.concept-grid` are covered by the 600px mobile sentinel.

---

## Section 3 — Index Page Tablet Tweaks

**Files:** `ism2411/index.html`, `ism3232/index.html`

Extend existing `@media(max-width:640px)` to `@media(max-width:768px)` and add:
- `.sec-count { display: none }` — already done at 640px, extend to 768px
- `.unit-head { flex-wrap: wrap }` — already done at 640px

The auto-fit grids (`.ov-grid`, `.week-grid`) handle tablet column count naturally via `minmax()` — no changes needed.

---

## Out of Scope

- Specialty pages (course_map, slo_mindmap, troubleshooting) — unique layouts, deferred.
- 404.html — trivial, not a content page.
- Print stylesheets — not requested.

---

## Implementation Order

1. `site.css` (ISM2411) — hamburger CSS + tablet block
2. `site.js` (ISM2411) — hamburger HTML + JS
3. `site.css` (ISM3232) — hamburger CSS + tablet block
4. `site.js` (ISM3232) — hamburger HTML + JS
5. `ism2411/index.html` — extend media query to 768px
6. `ism3232/index.html` — extend media query to 768px
7. Commit ISM2411, commit ISM3232, update parent pointers
