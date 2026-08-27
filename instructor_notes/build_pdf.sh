#!/bin/bash
# Build one or all instructor-guide PDFs from their Markdown source.
# Usage:
#   ./build_pdf.sh ism2411/lab_w04.md        # build a single guide
#   ./build_pdf.sh                            # build every lab_w*.md in ism2411/ and ism3232/
set -euo pipefail
cd "$(dirname "$0")"

build_one() {
  local md="$1"
  local pdf="${md%.md}.pdf"
  echo "Building $pdf ..."
  pandoc "$md" -o "$pdf" --pdf-engine=xelatex --syntax-highlighting=tango \
    --include-in-header="$(dirname "$0")/style_header.tex"
}

if [ "$#" -ge 1 ]; then
  for md in "$@"; do
    build_one "$md"
  done
else
  for md in ism2411/lab_w*.md ism3232/lab_w*.md; do
    [ -f "$md" ] && build_one "$md"
  done
fi
echo "Done."
