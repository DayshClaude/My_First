# Start here

This is the Beadwell Bracelets & Crafts showcase site — a proof of concept
built in a Claude Code cloud session. Work has moved to a **local** Claude Code
session on Shaun's PC (`C:\Users\shaun\Documents\Islas_Website`), because the
cloud session couldn't see local files and GitHub push access was blocked.

**If you are a Claude session picking this up: read this file first, then
`README.md`.** No GitHub access is needed for anything below.

---

## Pick up here (as of 27 Aug)

The site is finished and working. The only thing outstanding is getting the
owner's photos into `images/` on their machine.

**What went wrong last session:** their local clone went stale — `git pull`
silently never landed, so they were opening a days-old `index.html` that
referenced different filenames and still had the photo bug. Their GitHub
account (`shaundaysh-blip`) has read-only access to this repo, so they cannot
push or upload either. Nothing they did wrong; the routes were just blocked.

**The one-step fix — download the current site as a zip, no git involved:**

https://github.com/DayshClaude/My_First/archive/refs/heads/claude/what-do-i-do-5w1e91.zip

Then, in the extracted folder:

1. Copy their five contact sheets (`Bracelets 1-5`, `Crochet 1-2`,
   `Jewellry 1-2`) and their logo into `images/`.
2. Open `split-images.html`, drag **all nine sheets in at once** (doing them
   one at a time restarts the numbering — this is what bit them), check the
   summary reads 20 bracelets / 19 crochet / 17 jewellery, download the zip
   and unzip it into `images/`.
3. Rename the logo to `images/logo.png`.
4. Open `index.html`.

Work from that fresh folder and discard the old `Islas_Website` one.

---

## Where things stand

**Done:**

- Four static pages, no build step, no dependencies:
  `index.html` (hero, three category cards, About, commissions, enquiry form),
  `bracelets.html` (25), `crochet.html` (19), `jewellery.html` (12),
  plus `thanks.html`.
- All 56 products are already catalogued and written up, based on nine contact
  sheets the owner supplied. Each card already points at the filename the
  splitter will produce, so crops drop in with no rewiring.
- Enquiry flow: no checkout anywhere. Each page carries its own Netlify form;
  *Enquire* on a piece scrolls to it with the piece prefilled. The form is
  repeated per page on purpose — Netlify only detects forms present in the
  static HTML.
- Placeholder artwork: every card draws a crochet-stitch or bead-strand texture
  on canvas, seeded from the piece name, so nothing looks broken before photos
  exist. A real photo at the matching filename covers it automatically.
- Logo support is wired but untested with real artwork (see below).
- Copy is written for a small team ("we", not "I").

**Not done — the next jobs:**

1. **Split the contact sheets.** The originals are in the owner's
   `images/` folder (named `Bracelets 1.png` … `Jewellry 2.png`).

   Easiest route, nothing to install: open **`split-images.html`** in a browser,
   drag the sheets in, check the numbered boxes look right, click download.
   It produces `beadwell-images.zip`; unzip it into `images/`.

   Or, if Python and Pillow are available, move the sheets into
   `images/source/` and run `python3 tools/split_all.py` — same algorithm,
   same output names, and it skips `Bracelets 5` which duplicates
   `Bracelets 4`.

   **Then look at every crop.** Detection splits on white gutters between
   products; the bottom rows of the crochet sheets have tiles that butt close
   together and may merge. For any sheet that splits badly, use
   `tools/split_sheets.py <file> --grid RxC` to force an even cut, or
   `--dry-run` to see boundaries before writing.

   The sheets are ~1.7MB PNGs holding up to ten products, so crops land around
   400–500px wide. The splitter warns when a crop is too small to look sharp.
   Workable, not crisp — worth asking whether larger originals exist.

2. **Check the logo.** It should be at `images/logo.png` or `images/logo.svg`.
   The mechanism: `assets/app.js` probes for it and swaps out the text wordmark
   only once a file genuinely loads, so a missing logo degrades to text rather
   than a broken image. It has been tested with a stand-in but never with the
   real artwork — check the header at desktop and phone width, and check dark
   mode. **The site has a dark theme**, so a logo with dark lettering will
   vanish on a dark background; if so, add a light version as
   `images/logo-dark.png` and it gets used automatically.

3. **Bulk edits to the pieces** go in the catalogue at the top of
   `tools/build_pages.py`, then `python3 tools/build_pages.py` regenerates the
   three category pages. That **overwrites** them — for small edits, change the
   HTML directly.

---

## Things the owner should know

- The product photos are studio-style catalogue images, not photographs of
  pieces actually made. The owner knows, and has said this is a proof of
  concept that won't be shared until real photos replace them. The site's whole
  mechanism is someone enquiring about a specific item, so they do need
  swapping before anyone sees it.
- Search `index.html` for `hello@beadwellbracelets.co.uk` — a placeholder,
  appears in the enquiry section and footer of every page, marked `<!-- EDIT -->`.
  Same for the Instagram link.
- **Netlify Forms only start working once deployed**, and only send email after
  someone ticks the box: Netlify → Forms → Settings → Add email notification.
  Without that, notes are captured but nobody is told. It's the one step that
  matters most.

## Deploying without GitHub

Drag the whole folder onto https://app.netlify.com/drop. Live in about ten
seconds. To update, drag it again. `netlify.toml` already sets the publish
directory, caching and security headers — no build command needed.

## Viewing it locally

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>. Opening `index.html` by double-clicking
mostly works, but some browsers are fussy about local files.
