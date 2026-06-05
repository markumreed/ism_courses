#!/usr/bin/env python3
"""Inject Lab Walkthrough video placeholder into all lab pages.

ISM2411/pages/week*_lab.html  — inserts before <h2>Exercises</h2>
ISM3232/docs/week*_lab.html   — inserts before <div class="time-bar">

Skips pages that already contain the <!-- ism-lab-video --> sentinel.
"""

import glob
import os
import re

BASE = '/home/markumreed/Documents/ism_courses'
SENTINEL = '<!-- ism-lab-video -->'


def ism2411_block(week, title):
    return (
        f'{SENTINEL}\n'
        f'<div style="display:flex;align-items:center;gap:12px;margin:0 0 0;">'
        f'<div style="height:1px;flex:1;background:var(--border);"></div>'
        f'<span style="font-family:var(--mono);font-size:10px;letter-spacing:.2em;'
        f'text-transform:uppercase;color:var(--dim);">Lab Walkthrough</span>'
        f'<div style="height:1px;flex:1;background:var(--border);"></div></div>\n'
        f'<div class="video-embed" style="margin:28px 0 32px;">\n'
        f'  <div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;'
        f'border-radius:10px;border:1px solid var(--border,rgba(255,255,255,.08));">\n'
        f'    <iframe\n'
        f'      style="position:absolute;top:0;left:0;width:100%;height:100%;"\n'
        f'      src="https://www.youtube.com/embed/PLACEHOLDER_LAB_W{week:02d}"\n'
        f'      title="{title}"\n'
        f'      frameborder="0"\n'
        f'      allow="accelerometer; autoplay; clipboard-write; encrypted-media; '
        f'gyroscope; picture-in-picture; web-share"\n'
        f'      allowfullscreen>\n'
        f'    </iframe>\n'
        f'  </div>\n'
        f'</div>\n\n'
    )


def ism3232_block(week, title):
    return (
        f'{SENTINEL}\n'
        f'<div style="display:flex;align-items:center;gap:12px;margin:0 0 10px;">'
        f'<div style="height:1px;flex:1;background:var(--border);"></div>'
        f'<span style="font-family:\'Courier New\',Courier,monospace;font-size:9px;'
        f'letter-spacing:.12em;text-transform:uppercase;color:var(--text-muted);">'
        f'Lab Walkthrough</span>'
        f'<div style="height:1px;flex:1;background:var(--border);"></div></div>\n'
        f'<div class="video-embed" style="margin:28px 0 32px;">\n'
        f'  <div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;'
        f'border-radius:10px;border:1px solid var(--border,rgba(255,255,255,.08));">\n'
        f'    <iframe\n'
        f'      style="position:absolute;top:0;left:0;width:100%;height:100%;"\n'
        f'      src="https://www.youtube.com/embed/PLACEHOLDER_LAB_W{week:02d}"\n'
        f'      title="{title}"\n'
        f'      frameborder="0"\n'
        f'      allow="accelerometer; autoplay; clipboard-write; encrypted-media; '
        f'gyroscope; picture-in-picture; web-share"\n'
        f'      allowfullscreen>\n'
        f'    </iframe>\n'
        f'  </div>\n'
        f'</div>\n'
    )


def get_title_2411(content):
    m = re.search(r'<title>[^·]*·\s*([^—]+)—', content)
    if m:
        return m.group(1).strip()
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
    return m.group(1).strip() if m else 'Lab Walkthrough'


def get_title_3232(content):
    m = re.search(r'<h1[^>]*class="wk-title"[^>]*>([^<]+)</h1>', content)
    if m:
        return m.group(1).strip()
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
    return m.group(1).strip() if m else 'Lab Walkthrough'


def inject(filepath, anchor, block):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    if SENTINEL in content:
        return 'skip'
    if anchor not in content:
        return 'no-anchor'
    content = content.replace(anchor, block + anchor, 1)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return 'ok'


def main():
    ok = skip = 0

    print('ISM2411 lab pages:')
    for fp in sorted(glob.glob(f'{BASE}/ism2411/pages/week*_lab.html')):
        week = int(re.search(r'week(\d+)', os.path.basename(fp)).group(1))
        with open(fp, encoding='utf-8') as f:
            content = f.read()
        title = get_title_2411(content)
        r = inject(fp, '<h2>Exercises</h2>', ism2411_block(week, title))
        print(f'  week{week:02d}: {r}  ({title})')
        if r == 'ok':
            ok += 1
        else:
            skip += 1

    print('\nISM3232 lab pages:')
    for fp in sorted(glob.glob(f'{BASE}/ism3232/docs/week*_lab.html')):
        week = int(re.search(r'week(\d+)', os.path.basename(fp)).group(1))
        with open(fp, encoding='utf-8') as f:
            content = f.read()
        title = get_title_3232(content)
        r = inject(fp, '<div class="time-bar">', ism3232_block(week, title))
        print(f'  week{week:02d}: {r}  ({title})')
        if r == 'ok':
            ok += 1
        else:
            skip += 1

    print(f'\nDone — {ok} updated, {skip} skipped.')


if __name__ == '__main__':
    main()
