#!/usr/bin/env python3
"""Inject a mobile media-query block into every inner-page <style> block.

Targets both courses:
  ism2411/pages/*.html
  ism3232/docs/*.html

Skips files that already have the /* ism-mobile */ sentinel.
"""

import glob
import os
import re

BASE = '/home/markumreed/Documents/ism_courses'
SENTINEL = '/* ism-mobile */'

# ── ISM2411 mobile block ──────────────────────────────────────────────────────
# All ISM2411 inner pages share the same template.
# .pn = prev/next 2-col grid (needs to stack)
# .two-col = content 2-col grid (needs to stack)
# .vpl-tile = playlist tiles (min-width causes overflow on narrow screens)
# pre = reduce code font a touch on phones
ISM2411_MOBILE = """\
/* ism-mobile */
@media(max-width:600px){
  .pn{grid-template-columns:1fr}
  .two-col{grid-template-columns:1fr}
  .vpl-tile{min-width:unset;flex:1 1 100%}
  pre{font-size:12px;padding:12px 14px}
  .sched-row{grid-template-columns:80px 1fr;font-size:12.5px}
  .sched-row span:last-child{display:none}
  .concept-grid{grid-template-columns:1fr}
}"""

# ── ISM3232 mobile block ──────────────────────────────────────────────────────
# ISM3232 pages split into two templates:
#   A) body{padding:40px 20px 80px} — older Georgia-font lecture/lab/reading pages
#   B) body{min-height:100vh;width:100%;padding:40px 24px 80px} — newer wrap-based pages
#   C) .wrap via site.css — unit overview / cheatsheet pages
#
# For A+B we override body padding on mobile.
# For all ISM3232 pages: .two-col, .concept-table, pre/code.
ISM3232_MOBILE_BODY = """\
/* ism-mobile */
@media(max-width:600px){
  body{padding:16px 14px 48px!important}
  .wrapper{padding-left:14px!important;padding-right:14px!important}
  .two-col{grid-template-columns:1fr!important}
  .concept-table{display:block;overflow-x:auto}
  .timing-bar{grid-template-columns:1fr 1fr}
  .pn{grid-template-columns:1fr}
  .vpl-tile{min-width:unset;flex:1 1 100%}
  pre,code{font-size:12px}
  .two-pane{flex-direction:column}
}"""

ISM3232_MOBILE_WRAP = """\
/* ism-mobile */
@media(max-width:600px){
  .two-col{grid-template-columns:1fr!important}
  .concept-table{display:block;overflow-x:auto}
  .timing-bar{grid-template-columns:1fr 1fr}
  .pn{grid-template-columns:1fr}
  .vpl-tile{min-width:unset;flex:1 1 100%}
  pre,code{font-size:12px}
  .two-pane{flex-direction:column}
}"""


def has_body_padding(content):
    """Return True if the page sets body padding directly (not via .wrap)."""
    return bool(re.search(r'body\s*\{[^}]*padding:\s*40px', content))


def inject_mobile(filepath, mobile_css):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    if SENTINEL in content:
        return 'skip'

    # Find the first </style> and inject before it
    idx = content.find('</style>')
    if idx == -1:
        return 'no-style'

    new_content = content[:idx] + mobile_css + '\n' + content[idx:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return 'ok'


def main():
    total = skip = ok = 0

    # ── ISM2411 ──────────────────────────────────────────────────────────────
    print('\nism2411/pages:')
    for fp in sorted(glob.glob(f'{BASE}/ism2411/pages/*.html')):
        total += 1
        result = inject_mobile(fp, ISM2411_MOBILE)
        if result == 'ok':
            ok += 1
            print(f'  + {os.path.basename(fp)}')
        elif result == 'skip':
            skip += 1
        # silently ignore no-style (shouldn't happen)

    # ── ISM3232 ──────────────────────────────────────────────────────────────
    print('\nism3232/docs:')
    for fp in sorted(glob.glob(f'{BASE}/ism3232/docs/*.html')):
        total += 1
        with open(fp, encoding='utf-8') as f:
            content = f.read()
        if SENTINEL in content:
            skip += 1
            continue
        mobile_css = ISM3232_MOBILE_BODY if has_body_padding(content) else ISM3232_MOBILE_WRAP
        result = inject_mobile(fp, mobile_css)
        if result == 'ok':
            ok += 1
            print(f'  + {os.path.basename(fp)}')
        elif result == 'skip':
            skip += 1

    print(f'\nDone — {ok} updated, {skip} skipped, {total} total')


if __name__ == '__main__':
    main()
