#!/usr/bin/env python3
"""
Split a contact sheet (several products photographed on a white background)
into one image per product, sized and padded for the website's cards.

    python3 tools/split_sheets.py images/source/bracelets-1.jpg --prefix bracelet

How it works: the products sit on white with clear gutters between them, so
instead of anything clever we look for the empty rows and columns. Rows of
pure white split the sheet into bands; white columns split each band into
individual products.

Options:
    --grid RxC   skip detection and cut into an even R by C grid
    --ratio W:H  aspect ratio to pad each crop to (default 4:5, matching the cards)
    --out DIR    where to write (default images/)
    --dry-run    report what it found without writing anything
"""

import argparse
import os
import sys

from PIL import Image

# A pixel counts as "content" if it is this much darker than pure white.
# Product shadows are soft, so we need to be reasonably sensitive.
WHITE_TOLERANCE = 14

# A band must be at least this fraction of the sheet to count as a real
# product rather than a speck of dust or a stray shadow.
MIN_BAND_FRACTION = 0.04

# Breathing room left around each product, as a fraction of its size.
PADDING = 0.08


def content_mask(img, axis):
    """Return a list of booleans: does this row (or column) contain any product?"""
    grey = img.convert("L")
    w, h = grey.size
    px = grey.load()

    limit = 255 - WHITE_TOLERANCE
    if axis == "rows":
        return [any(px[x, y] < limit for x in range(0, w, 3)) for y in range(h)]
    return [any(px[x, y] < limit for y in range(0, h, 3)) for x in range(w)]


def find_bands(mask, minimum):
    """Turn a run of True values into (start, end) pairs, dropping tiny ones."""
    bands, start = [], None
    for i, filled in enumerate(mask):
        if filled and start is None:
            start = i
        elif not filled and start is not None:
            if i - start >= minimum:
                bands.append((start, i))
            start = None
    if start is not None and len(mask) - start >= minimum:
        bands.append((start, len(mask)))
    return bands


def detect_cells(img):
    """Find every product on the sheet, returned as crop boxes."""
    w, h = img.size
    boxes = []

    row_bands = find_bands(content_mask(img, "rows"), int(h * MIN_BAND_FRACTION))
    for top, bottom in row_bands:
        strip = img.crop((0, top, w, bottom))
        col_bands = find_bands(content_mask(strip, "cols"), int(w * MIN_BAND_FRACTION))
        for left, right in col_bands:
            boxes.append((left, top, right, bottom))
    return boxes


def grid_cells(img, rows, cols):
    """Cut the sheet into an even grid, for sheets that don't separate cleanly."""
    w, h = img.size
    return [
        (c * w // cols, r * h // rows, (c + 1) * w // cols, (r + 1) * h // rows)
        for r in range(rows)
        for c in range(cols)
    ]


def pad_to_ratio(img, ratio_w, ratio_h, background=(255, 255, 255)):
    """Centre the crop on a white canvas of the card's aspect ratio."""
    w, h = img.size
    target = ratio_w / ratio_h
    if w / h > target:
        new_w, new_h = w, round(w / target)
    else:
        new_w, new_h = round(h * target), h

    canvas = Image.new("RGB", (new_w, new_h), background)
    canvas.paste(img, ((new_w - w) // 2, (new_h - h) // 2))
    return canvas


def save_web_ready(img, path, max_width=1200, budget_bytes=300_000):
    """Resize to a sensible width, then step quality down until it fits."""
    if img.width > max_width:
        height = round(img.height * max_width / img.width)
        img = img.resize((max_width, height), Image.LANCZOS)

    for quality in (86, 80, 74, 68, 62):
        img.save(path, "JPEG", quality=quality, optimize=True, progressive=True)
        if os.path.getsize(path) <= budget_bytes:
            break
    return os.path.getsize(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sheet", help="the contact sheet to split")
    ap.add_argument("--prefix", default="piece", help="filename stem for the crops")
    ap.add_argument("--out", default="images", help="output directory")
    ap.add_argument("--grid", help="force an even grid instead of detecting, e.g. 2x5")
    ap.add_argument("--ratio", default="4:5", help="aspect ratio to pad to")
    ap.add_argument("--start", type=int, default=1, help="first number to use")
    ap.add_argument("--dry-run", action="store_true", help="report without writing")
    args = ap.parse_args()

    if not os.path.exists(args.sheet):
        sys.exit(f"Can't find {args.sheet}")

    img = Image.open(args.sheet).convert("RGB")
    ratio_w, ratio_h = (int(n) for n in args.ratio.split(":"))

    if args.grid:
        rows, cols = (int(n) for n in args.grid.lower().split("x"))
        boxes = grid_cells(img, rows, cols)
    else:
        boxes = detect_cells(img)

    print(f"{args.sheet}: {img.width}x{img.height}, found {len(boxes)} item(s)")
    if not boxes:
        sys.exit("Nothing detected. The background may not be white enough — "
                 "try --grid, e.g. --grid 2x5.")

    os.makedirs(args.out, exist_ok=True)

    for n, (left, top, right, bottom) in enumerate(boxes, start=args.start):
        pad_x = round((right - left) * PADDING)
        pad_y = round((bottom - top) * PADDING)
        box = (max(0, left - pad_x), max(0, top - pad_y),
               min(img.width, right + pad_x), min(img.height, bottom + pad_y))

        crop = img.crop(box)
        name = f"{args.prefix}-{n:02d}.jpg"
        path = os.path.join(args.out, name)

        if args.dry_run:
            print(f"  {name}  from {box}  ({crop.width}x{crop.height})")
            continue

        size = save_web_ready(pad_to_ratio(crop, ratio_w, ratio_h), path)
        flag = "  <- small, may look soft" if crop.width < 500 else ""
        print(f"  {name}  {crop.width}x{crop.height} source  {size // 1024} KB{flag}")


if __name__ == "__main__":
    main()
