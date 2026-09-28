#!/bin/bash
# Build one or all instructor projection decks from their Markdown lab guide.
# Usage:
#   ./build_slides.sh ism2411/lab_w04.md     # build a single deck
#   ./build_slides.sh                         # build every lab_w*.md in ism2411/ and ism3232/
# Output: slides_wNN.html next to each lab_wNN.md. Open in a browser; press S for speaker notes.
set -euo pipefail
cd "$(dirname "$0")"
exec python3 build_slides.py "$@"
