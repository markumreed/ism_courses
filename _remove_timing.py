#!/usr/bin/env python3
"""Remove 'Suggested class timing' sections from all ISM3232 docs pages.

Removes per file:
  - Optional <!-- ... Timing ... --> comment line preceding the section
  - The section-divider div with label "Suggested class timing"
  - The timing-bar div and all timing-block children
  - CSS lines for .timing-bar and .timing-block* from inline <style> blocks
"""

import glob
import os

BASE = '/home/markumreed/Documents/ism_courses/ism3232/docs'

DIVIDER = '<div class="section-divider"><div class="line"></div><div class="label">Suggested class timing</div><div class="line"></div></div>'
BAR_OPEN = '<div class="timing-bar">'


def find_div_end(text, pos):
    """Return index right after the closing </div> matching an already-open div.

    pos should be the index immediately after the opening tag (depth=1).
    """
    depth = 1
    while pos < len(text) and depth > 0:
        next_open = text.find('<div', pos)
        next_close = text.find('</div>', pos)
        if next_close == -1:
            break
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            pos = next_close + 6
    return pos


def remove_timing_html(content):
    while True:
        divider_pos = content.find(DIVIDER)
        if divider_pos == -1:
            break

        section_start = divider_pos

        # Find start of the line that contains the divider
        line_start = content.rfind('\n', 0, divider_pos)
        line_start = 0 if line_start == -1 else line_start + 1

        pre = content[line_start:divider_pos]

        if not pre.strip():
            # Divider is at the start of its own line — check the preceding line
            # for a Timing comment and include it in the removal.
            prev_nl = content.rfind('\n', 0, line_start - 1) if line_start > 0 else -1
            prev_line = content[prev_nl + 1:line_start - 1] if prev_nl >= 0 else content[:line_start - 1]
            if '<!--' in prev_line and 'iming' in prev_line:
                section_start = prev_nl + 1  # include from start of comment line

        # Find end of timing-bar div
        bar_pos = content.find(BAR_OPEN, divider_pos + len(DIVIDER))
        if bar_pos != -1:
            section_end = find_div_end(content, bar_pos + len(BAR_OPEN))
        else:
            section_end = divider_pos + len(DIVIDER)

        # Consume one trailing newline (multiline format leaves a blank line)
        if section_end < len(content) and content[section_end] == '\n':
            section_end += 1

        content = content[:section_start] + content[section_end:]

    return content


def remove_timing_css(content):
    """Strip .timing-bar and .timing-block* CSS lines from inline <style>."""
    lines = content.split('\n')
    out = []
    for line in lines:
        s = line.strip()
        if s.startswith('.timing-bar') or s.startswith('.timing-block'):
            continue
        out.append(line)
    return '\n'.join(out)


def process(filepath):
    with open(filepath, encoding='utf-8') as f:
        original = f.read()

    updated = remove_timing_html(original)
    updated = remove_timing_css(updated)

    if updated != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated)
        return 'ok'
    return 'skip'


def main():
    files = sorted(glob.glob(f'{BASE}/*.html'))
    ok = skip = 0
    print(f'Processing {len(files)} files in {BASE}...\n')
    for fp in files:
        r = process(fp)
        if r == 'ok':
            ok += 1
            print(f'  ✓ {os.path.basename(fp)}')
        else:
            skip += 1
    print(f'\nDone — {ok} updated, {skip} no timing section.')


if __name__ == '__main__':
    main()
