# Beadwell Bracelets & Crafts

A showcase site for crochet work and hand-strung beaded jewellery. There's no
shop and no checkout — visitors browse the pieces and send a note about
anything they like, which arrives as an email.

Plain HTML, CSS and JavaScript. No build step, no framework, no dependencies to
install. What's in this folder is exactly what gets served.

```
index.html          the whole site — all the text lives here
thanks.html         where someone lands after sending a note
assets/style.css    every colour, font and spacing rule
assets/app.js       filtering, the enquire flow, the swatch textures
images/             your photos go here (see images/README.md)
netlify.toml        Netlify settings — you shouldn't need to touch this
```

---

## Getting it online

### The quick way — drag and drop

1. Go to [app.netlify.com/drop](https://app.netlify.com/drop).
2. Drag this whole folder onto the page.
3. It's live in about ten seconds, on an address like
   `random-words-123.netlify.app`.

Good for a first look. To update it you drag the folder over again.

### The better way — connect it to GitHub

Netlify then rebuilds automatically every time a change is pushed, and you get a
history you can roll back.

1. In Netlify: **Add new site → Import an existing project → GitHub**.
2. Pick this repository.
3. Leave **build command** empty and set **publish directory** to `.` —
   `netlify.toml` already says this, so the fields should fill themselves in.
4. **Deploy**.

### Giving it a proper name

Free, and worth doing straight away: **Site configuration → Change site name**
gets you `beadwellbracelets.netlify.app` instead of the random words.

For a real domain (`beadwellbracelets.co.uk`, roughly £10–15/year from any
registrar), go to **Domain management → Add a domain** and follow the
instructions. Netlify sorts out the HTTPS certificate itself.

---

## Turning on the enquiry emails

**This is the one step that matters — without it, notes are captured but nobody
is told about them.**

The form is already wired up for Netlify Forms. It only starts working once the
site is deployed to Netlify (it does nothing when you open `index.html` off your
own computer — that's normal).

After the first deploy:

1. Netlify dashboard → **Forms**. You should see a form called **enquiry**.
2. **Settings → Form notifications → Add notification → Email notification**.
3. Put in the address that should receive enquiries. Done.

Every submission is also kept in the Forms tab as a backup, so nothing is lost
if an email goes astray. The free tier covers 100 submissions a month, which is
plenty. A hidden honeypot field already filters out most spam bots.

If the Forms tab is empty after deploying, it's almost always because the
`<input type="hidden" name="form-name" value="enquiry">` line got deleted from
the form — Netlify needs it.

---

## Changing things

### Text

All of it is in `index.html`. Open it in any text editor, find the words on the
page, change them, save. Nothing else needs to happen.

### Photos

See **`images/README.md`** — save a photo with the right filename and it appears
by itself. Until then each card draws its own woven or beaded swatch, so the
site never looks half-finished.

### Adding a new piece

Copy one `<article class="piece">…</article>` block in `index.html` and edit it.
Four things to change:

- `data-cat="bracelets"` — one of `crochet`, `bracelets` or `jewellery`
- `--img:url('images/your-photo.jpg')` and the `<span class="filehint">` under it
- `data-texture="bead"` or `"stitch"`, and give `data-seed` any unique word
  (that's what makes each swatch look different)
- `data-piece` and `data-ref` on the Enquire button — these are what gets
  emailed to you

### Colours

Top of `assets/style.css`. Change a value in the `:root` block and it updates
everywhere, including the generated swatches. The block below it does the same
for people whose phone or laptop is set to dark mode.

### Before you go live

Search `index.html` for `hello@beadwellbracelets.co.uk` and swap in your real
address — it appears twice, in the enquiry section and the footer. Same for the
Instagram link in the footer. Both are marked with `<!-- EDIT -->` comments.

---

## Looking at it on your own computer

Double-clicking `index.html` mostly works. Some browsers are fussy about local
files, so if anything looks off, run a tiny local server from this folder:

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>.
