#!/usr/bin/env bash
# Split every contact sheet in images/source/ into individual product images.
# Re-runnable: it overwrites previous crops rather than piling up duplicates.
set -euo pipefail
cd "$(dirname "$0")/.."

split() {
  local file="images/source/$1" prefix="$2" start="$3"
  if [ ! -f "$file" ]; then
    echo "skipping $file — not there yet"
    return
  fi
  python3 tools/split_sheets.py "$file" --prefix "$prefix" --start "$start"
}

# --start keeps the numbering running across sheets in the same category,
# so the four bracelet sheets produce bracelet-01 through bracelet-20.
split bracelets-1.jpg  bracelet   1
split bracelets-2.jpg  bracelet   6
split bracelets-3.jpg  bracelet  11
split bracelets-4.jpg  bracelet  16

split crochet-1.jpg    crochet    1
split crochet-2.jpg    crochet   11

split jewellery-1.jpg  jewellery  1
split jewellery-2.jpg  jewellery  8

echo
echo "Done. Check images/ — then tell Claude and it'll wire them into the site."
