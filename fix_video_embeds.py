#!/usr/bin/env python3
"""Neutralize unrecorded-video placeholders so pages never load a broken
YouTube embed (src="https://www.youtube.com/embed/PLACEHOLDER_V07" etc).

Run this AFTER update_video_ids.py on every pass:
    python update_video_ids.py
    python fix_video_embeds.py

For any iframe/tile whose video ID still contains "PLACEHOLDER", the real
src/onclick attribute is swapped for data-embed-src/data-embed-title (so the
browser never requests youtube.com/embed/PLACEHOLDER_*) and a "coming soon"
placeholder is rendered instead. The placeholder token is preserved in the
data attribute, so update_video_ids.py can still find and replace it later.

This script is idempotent: on a later run, once update_video_ids.py has
turned a data-embed-src value into a real ID, re-running this script
"promotes" that tile/block back into a normal, clickable, playable embed.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIRS = [ROOT / "ism2411" / "pages", ROOT / "ism3232" / "docs"]

EMBED_PREFIX = "https://www.youtube.com/embed/"


def is_placeholder(video_id):
    return "PLACEHOLDER" in video_id


def find_block(html, start):
    """Return (start, end) of the <div ...> block starting at `start`,
    matching on div-tag depth."""
    depth = 0
    for m in re.finditer(r"<div\b|</div>", html[start:]):
        if m.group() == "<div" or m.group().startswith("<div"):
            depth += 1
        else:
            depth -= 1
        if depth == 0:
            return start, start + m.end()
    raise ValueError("unbalanced div block")


def coming_soon_box(indent, title=None, label="Video coming soon"):
    i = " " * indent
    title_span = (
        f'\n{i}    <span style="font-size:13px;color:var(--dim,#888);max-width:85%;">{title}</span>'
        if title
        else ""
    )
    return (
        f'{i}<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;'
        f'border-radius:10px;border:1px dashed var(--border,rgba(255,255,255,.15));'
        f'background:var(--bg2,rgba(255,255,255,.03));">\n'
        f'{i}  <div style="position:absolute;top:0;left:0;width:100%;height:100%;'
        f"display:flex;flex-direction:column;align-items:center;justify-content:center;"
        f'text-align:center;padding:16px;box-sizing:border-box;gap:6px;">\n'
        f'{i}    <span style="font-family:var(--mono,monospace);font-size:11px;'
        f'letter-spacing:.15em;text-transform:uppercase;color:var(--dim,#888);">'
        f"{label}</span>{title_span}\n"
        f"{i}  </div>\n"
        f"{i}</div>"
    )


def real_iframe_block(indent, src, title):
    i = " " * indent
    return (
        f'{i}<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;'
        f'border-radius:10px;border:1px solid var(--border,rgba(255,255,255,.08));">\n'
        f"{i}  <iframe\n"
        f'{i}    style="position:absolute;top:0;left:0;width:100%;height:100%;"\n'
        f'{i}    src="{src}"\n'
        f'{i}    title="{title}"\n'
        f'{i}    frameborder="0"\n'
        f'{i}    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"\n'
        f"{i}    allowfullscreen>\n"
        f"{i}  </iframe>\n"
        f"{i}</div>"
    )

VIDEO_EMBED_RE = re.compile(
    r'<iframe\s+style="[^"]*"\s+src="([^"]*)"\s+title="([^"]*)"\s+frameborder="0"'
    r'\s+allow="([^"]*)"\s+allowfullscreen>\s*</iframe>',
    re.DOTALL,
)

# Matches either a live iframe-bearing stage/single block, OR an already
# "demoted" coming-soon block carrying data-embed-src/data-embed-title.
DEMOTED_SINGLE_RE = re.compile(
    r'data-embed-src="([^"]*)"(?:\s+data-embed-title="([^"]*)")?'
)

TILE_LIVE_RE = re.compile(
    r'<div class="vpl-tile( vpl-active)?"\s+onclick="vplSwitch\(this,\'([^\']*)\',\'([^\']*)\'\)">'
    r'\s*<span class="vpl-num">([^<]*)</span>\s*<span class="vpl-title">(.*?)</span>\s*</div>',
    re.DOTALL,
)

TILE_DEMOTED_RE = re.compile(
    r'<div class="vpl-tile"\s+data-embed-src="([^"]*)"\s+data-embed-title="([^"]*)"'
    r'\s+style="opacity:\.45;cursor:default;">\s*<span class="vpl-num">([^<]*)</span>'
    r'\s*<span class="vpl-title">(.*?)</span>\s*</div>',
    re.DOTALL,
)

TILE_ANY_RE = re.compile(
    r'<div class="vpl-tile".*?</div>\s*</div>',
    re.DOTALL,
)


def strip_coming_soon_suffix(title):
    return title[: -len(" — coming soon")] if title.endswith(" — coming soon") else title


def parse_tiles(tiles_html):
    """Split the vpl-tiles inner HTML into a list of tile dicts, preserving order."""
    tiles = []
    pos = 0
    tile_open_re = re.compile(r'<div class="vpl-tile\b')
    matches = list(tile_open_re.finditer(tiles_html))
    for i, m in enumerate(matches):
        start = m.start()
        s, e = find_block(tiles_html, start)
        block = tiles_html[s:e]
        live = TILE_LIVE_RE.match(block)
        demoted = TILE_DEMOTED_RE.match(block)
        if live:
            active, src, title, num, title_span = live.groups()
            tiles.append(
                {
                    "src": src,
                    "title": title,
                    "num": num,
                    "display_title": title_span,
                    "was_active": bool(active),
                }
            )
        elif demoted:
            src, title, num, title_span = demoted.groups()
            tiles.append(
                {
                    "src": src,
                    "title": title,
                    "num": num,
                    "display_title": strip_coming_soon_suffix(title_span),
                    "was_active": False,
                }
            )
        else:
            raise ValueError(f"unrecognized tile markup: {block[:200]}")
    return tiles


def render_tile(tile, is_active):
    vid = tile["src"].rsplit("/", 1)[-1]
    if is_placeholder(vid):
        return (
            f'    <div class="vpl-tile" data-embed-src="{tile["src"]}" '
            f'data-embed-title="{tile["title"]}" style="opacity:.45;cursor:default;">\n'
            f'      <span class="vpl-num">{tile["num"]}</span>\n'
            f'      <span class="vpl-title">{tile["display_title"]} — coming soon</span>\n'
            "    </div>"
        )
    active_class = " vpl-active" if is_active else ""
    return (
        f'    <div class="vpl-tile{active_class}" '
        f"onclick=\"vplSwitch(this,'{tile['src']}','{tile['title']}')\">\n"
        f'      <span class="vpl-num">{tile["num"]}</span>\n'
        f'      <span class="vpl-title">{tile["display_title"]}</span>\n'
        "    </div>"
    )


def fix_single_video_embed(block):
    live = VIDEO_EMBED_RE.search(block)
    if live:
        src, title, allow = live.groups()
        vid = src.rsplit("/", 1)[-1]
        if not is_placeholder(vid):
            return None  # already correct, leave untouched
        # demote
        prefix = block[: live.start()]
        # coming_soon_box() below is a full self-closing replacement for the
        # old aspect-ratio div; only the outer video-embed div's own closing
        # tag still needs to follow it (not the old aspect-div's closing tag).
        suffix = "\n</div>"
        opening_tag_re = re.compile(r'(<div class="video-embed")([^>]*)(>)')
        m = opening_tag_re.search(prefix)
        new_prefix = (
            prefix[: m.start()]
            + f'{m.group(1)} data-embed-src="{src}" data-embed-title="{title}"{m.group(2)}{m.group(3)}'
            + prefix[m.end() :]
        )
        new_middle = coming_soon_box(indent=2, title=title)
        # replace the wrapping aspect-ratio div + iframe entirely, including
        # its leading indentation (coming_soon_box supplies its own)
        div_idx = new_prefix.rfind("<div")
        line_start = new_prefix.rfind("\n", 0, div_idx) + 1
        new_prefix2 = new_prefix[:line_start]
        return new_prefix2 + new_middle + suffix

    demoted = DEMOTED_SINGLE_RE.search(block)
    if demoted:
        src, title = demoted.groups()
        vid = src.rsplit("/", 1)[-1]
        if is_placeholder(vid):
            return None  # still not recorded, leave as-is
        # promote back to a real iframe
        wrap = real_iframe_block(indent=2, src=src, title=title or "")
        opening_tag_re = re.compile(
            r'(<div class="video-embed")\s+data-embed-src="[^"]*"(?:\s+data-embed-title="[^"]*")?([^>]*)(>)'
        )
        m = opening_tag_re.search(block)
        new_opening = f"{m.group(1)}{m.group(2)}{m.group(3)}"
        return block[: m.start()] + new_opening + "\n" + wrap + "\n</div>"

    return None  # not a recognized video-embed block


def fix_vid_playlist(block):
    if "PLACEHOLDER" not in block and "data-embed-src" not in block:
        return None  # nothing to promote/demote, leave byte-identical

    tiles_m = re.search(r'<div class="vpl-tiles">', block)
    if not tiles_m:
        return None
    tiles_start, tiles_end = find_block(block, tiles_m.start())
    tiles_inner = block[tiles_m.end() : tiles_end - len("</div>")]
    tiles = parse_tiles(tiles_inner)

    real_tiles = [t for t in tiles if not is_placeholder(t["src"].rsplit("/", 1)[-1])]
    default_tile = real_tiles[0] if real_tiles else None

    new_tiles_html = "\n".join(
        render_tile(t, is_active=(default_tile is not None and t is default_tile))
        for t in tiles
    )

    stage_m = re.search(r'<div class="vpl-stage">', block)
    stage_start, stage_end = find_block(block, stage_m.start())
    if default_tile is not None:
        stage_inner = real_iframe_block(indent=4, src=default_tile["src"], title=default_tile["title"])
    else:
        stage_inner = coming_soon_box(indent=4, label="Videos coming soon")
    new_stage = f'<div class="vpl-stage">\n{stage_inner}\n  </div>'

    new_block = (
        block[: stage_m.start()]
        + new_stage
        + block[stage_end : tiles_m.start()]
        + '<div class="vpl-tiles">\n'
        + new_tiles_html
        + "\n  </div>"
        + block[tiles_end:]
    )
    if new_block == block:
        return None
    return new_block


def process_file(path):
    html = path.read_text(encoding="utf-8")
    original = html

    replacements = []  # (start, end, new_text), applied back-to-front

    for m in re.finditer(r'<div class="video-embed"', html):
        s, e = find_block(html, m.start())
        new = fix_single_video_embed(html[s:e])
        if new is not None:
            replacements.append((s, e, new))

    for m in re.finditer(r'<div class="vid-playlist"', html):
        s, e = find_block(html, m.start())
        new = fix_vid_playlist(html[s:e])
        if new is not None:
            replacements.append((s, e, new))

    for s, e, new in sorted(replacements, key=lambda r: r[0], reverse=True):
        html = html[:s] + new + html[e:]

    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main():
    changed = []
    for d in DIRS:
        for path in sorted(d.glob("*.html")):
            if process_file(path):
                changed.append(path)
    for path in changed:
        print(f"  fixed: {path.relative_to(ROOT)}")
    print(f"Done. {len(changed)} file(s) updated.")


if __name__ == "__main__":
    main()
