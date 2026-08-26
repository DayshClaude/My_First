# Put the original photos here

This is for **full-size originals** — the contact sheets with several products
per picture, straight off the camera or phone. Nothing in this folder is used
by the website directly; it's the raw material.

`tools/split_sheets.py` reads a sheet from here and writes one cropped,
web-sized image per product into `images/`, which is what the site actually
serves.

Name them by batch so the splitter's output is predictable:

```
bracelets-1.jpg   bracelets-2.jpg   bracelets-3.jpg   bracelets-4.jpg
crochet-1.jpg     crochet-2.jpg
jewellery-1.jpg   jewellery-2.jpg
```

Then, from the top of the project:

```bash
bash tools/split-all.sh
```

Keep the originals in here even after splitting. If a crop needs redoing at a
different size or aspect ratio later, the source is right where you left it.
