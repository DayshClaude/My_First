#!/usr/bin/env python3
"""
Find every contact sheet and split the lot in one go.

    python3 tools/split_all.py

Looks in images/source/ and images/ for files whose name contains "bracelet",
"crochet" or "jewel" and a number — so "Bracelets 1.png", "bracelets-1.jpg"
and "Jewellry 2.PNG" are all picked up without renaming anything. Identical
sheets uploaded twice are detected and skipped.

Crops are numbered continuously within each category, so the four bracelet
sheets produce bracelet-01 through bracelet-20.
"""

import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEARCH_DIRS = ["images/source", "images"]
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

# Category name -> the words that identify it in a filename. "jewel" catches
# jewellery, jewelry and the common misspelling jewellry.
CATEGORIES = {
    "bracelet": ["bracelet"],
    "crochet": ["crochet"],
    "jewellery": ["jewel"],
}


def sheet_number(name):
    """Pull the trailing number out of a filename, for ordering."""
    found = re.findall(r"(\d+)", name)
    return int(found[-1]) if found else 0


def find_sheets():
    """Group every image found into its category, in sheet order."""
    sheets = {key: [] for key in CATEGORIES}
    # Duplicate detection is per category — two different categories could in
    # principle share a sheet, and dropping one silently would lose products.
    seen = {key: set() for key in CATEGORIES}

    for folder in SEARCH_DIRS:
        full = os.path.join(ROOT, folder)
        if not os.path.isdir(full):
            continue
        for entry in sorted(os.listdir(full)):
            path = os.path.join(full, entry)
            if not os.path.isfile(path) or os.path.splitext(entry)[1].lower() not in EXTENSIONS:
                continue

            lowered = entry.lower()
            category = next((key for key, words in CATEGORIES.items()
                             if any(w in lowered for w in words)), None)
            if category is None:
                continue

            # Skip a sheet we have already seen under another name.
            digest = hashlib.md5(open(path, "rb").read()).hexdigest()
            if digest in seen[category]:
                print(f"  skipping {entry} — identical to a {category} sheet already queued")
                continue
            seen[category].add(digest)

            sheets[category].append((sheet_number(entry), path))

    for key in sheets:
        sheets[key].sort()
    return sheets


def main():
    os.chdir(ROOT)
    sheets = find_sheets()
    total = sum(len(v) for v in sheets.values())

    if not total:
        sys.exit("No contact sheets found. Put them in images/source/ — names "
                 "just need to contain 'bracelet', 'crochet' or 'jewel'.")

    print(f"Found {total} sheet(s).\n")
    for category, found in sheets.items():
        if not found:
            print(f"{category}: none found\n")
            continue

        # Each sheet's crops carry on numbering from where the last one stopped.
        next_number = 1
        for _, path in found:
            print(f"{os.path.relpath(path, ROOT)} -> {category}-{next_number:02d} onwards")
            result = subprocess.run(
                [sys.executable, "tools/split_sheets.py", path,
                 "--prefix", category, "--start", str(next_number)],
                capture_output=True, text=True)
            print(result.stdout.rstrip())
            if result.returncode:
                print(result.stderr.rstrip(), file=sys.stderr)
                sys.exit(f"Splitting {path} failed.")
            # Count how many crops that sheet produced.
            next_number += sum(1 for line in result.stdout.splitlines()
                               if line.strip().startswith(category))
        print()

    print("Done. Check images/, then tell Claude and it'll wire them in.")


if __name__ == "__main__":
    main()
