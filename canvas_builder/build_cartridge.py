#!/usr/bin/env python3
"""CLI: build a Canvas-importable Common Cartridge from a course manifest.

Usage:
    python build_cartridge.py --manifest ism2411_manifest.yaml --out ism2411_fa26.imscc
"""
from __future__ import annotations

import argparse
import os
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from canvas_builder_common.cartridge_writer import write_cartridge
from canvas_builder_common.manifest_schema import load_manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="Path to the course manifest YAML")
    parser.add_argument("--out", required=True, help="Output .imscc path")
    args = parser.parse_args(argv)

    course = load_manifest(args.manifest)
    write_cartridge(course, args.out)

    expected_weblinks = sum(len(m.items) for m in course.modules)
    expected_assignments = sum(len(m.assignments) for m in course.modules)

    with zipfile.ZipFile(args.out) as zf:
        names = zf.namelist()
        actual_weblinks = sum(1 for n in names if n.startswith("weblinks/"))
        actual_assignments = sum(1 for n in names if n.startswith("assignment_"))

    print(f"Built {args.out}")
    print(f"  Modules:     {len(course.modules)}")
    print(f"  Weblinks:    {actual_weblinks} (expected {expected_weblinks})")
    print(f"  Assignments: {actual_assignments} (expected {expected_assignments})")

    if actual_weblinks != expected_weblinks or actual_assignments != expected_assignments:
        print("MISMATCH — cartridge contents do not match manifest. Do not import.", file=sys.stderr)
        os.remove(args.out)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
