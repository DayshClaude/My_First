#!/usr/bin/env python3
"""
Generate the category pages from one catalogue of pieces.

The site itself stays plain static HTML with no build step — this just saves
hand-editing fifty-odd near-identical cards. For a small change (fixing a
name, reordering), edit the .html directly. For a bulk change, edit CATALOGUE
below and re-run:

    python3 tools/build_pages.py
"""

import os

# ── The catalogue ────────────────────────────────────────────────────────
# (image stem, name, description, materials, detail)
# The image stem matches what tools/split_sheets.py produces from the
# contact sheets in images/source/.

BRACELETS = [
    ("bracelet-01", "Amethyst Tree of Life",
     "Faceted amethyst and clear quartz linked on hand-coiled copper wire, closed with a toggle.",
     "Amethyst, quartz, copper", "Tree-of-life heart charm"),
    ("bracelet-02", "Ocean Starfish",
     "Teal and aqua crystal separated by silver filigree caps, finished with a hanging starfish.",
     "Crystal, agate, silver plate", "Starfish charm"),
    ("bracelet-03", "Peridot Leaf",
     "Spring-green faceted glass with silver spacers, light enough to wear all day.",
     "Glass, silver plate", "Leaf charm"),
    ("bracelet-04", "Rose Blossom",
     "Rose quartz and pink crystal on copper links, with a five-petal flower at the clasp.",
     "Rose quartz, crystal, copper", "Copper flower charm"),
    ("bracelet-05", "Midnight Tree",
     "Navy agate and cobalt crystal, cool-toned and heavier than it looks.",
     "Agate, crystal, silver plate", "Open tree-of-life disc"),
    ("bracelet-06", "Blush Open Heart",
     "Pale pink crystal and rose quartz on rose-gold links, with a small open heart.",
     "Rose quartz, crystal, rose gold plate", "Open heart charm"),
    ("bracelet-07", "Aquamarine Starfish",
     "Pale blue and deep teal crystal wired individually so each bead sits square.",
     "Crystal, silver plate", "Starfish charm"),
    ("bracelet-08", "Olive Grove Leaf",
     "Olive jade and green crystal on copper, with a veined copper leaf.",
     "Jade, crystal, copper", "Copper leaf charm"),
    ("bracelet-09", "Amethyst Filigree Heart",
     "Deep purple crystal and lilac crackle glass on antique brass.",
     "Crystal, crackle glass, antique brass", "Filigree heart charm"),
    ("bracelet-10", "Pearl Tree of Life",
     "Cream glass pearls and clear crystal on a fine silver chain — the quietest of the set.",
     "Glass pearl, crystal, silver plate", "Tree-of-life disc"),
    ("bracelet-11", "Moss Agate Leaf",
     "Moss and jade agate with a hand-formed copper hook clasp.",
     "Moss agate, jade, copper", "Copper leaf charm"),
    ("bracelet-12", "Sapphire Star",
     "Cobalt and sky-blue agate either side of a single faceted teal centre bead.",
     "Agate, crystal, silver plate", "Star charm"),
    ("bracelet-13", "Peach Blossom Heart",
     "Peach crystal and rose quartz on gold links, closed with a heart-shaped clasp.",
     "Rose quartz, crystal, gold plate", "Open heart charm and clasp"),
    ("bracelet-14", "Lilac Tree of Life",
     "Graded lilac to deep purple, with a hand-bent silver hook.",
     "Amethyst, crystal, silver plate", "Tree-of-life disc"),
    ("bracelet-15", "Ember Butterfly",
     "Copper pearl and red-orange crystal around a filigree copper centre bead.",
     "Glass pearl, crystal, copper", "Brass butterfly charm"),
    ("bracelet-16", "Spring Meadow Trio",
     "Peridot green glass with three charms grouped at the front rather than one.",
     "Glass, silver plate", "Leaf, teardrop and flower charms"),
    ("bracelet-17", "Rockpool Trio",
     "Teal and midnight crystal on copper, hung with three seaside charms.",
     "Crystal, agate, copper", "Starfish, seahorse and shell"),
    ("bracelet-18", "Amethyst Drop",
     "Soft purple agate and clear crystal with a faceted teardrop beside the disc.",
     "Amethyst, agate, silver plate", "Tree-of-life disc and teardrop"),
    ("bracelet-19", "Rainbow Feather",
     "A full spectrum of faceted beads, warm through to cool, running right round the wrist.",
     "Crystal, agate, silver plate", "Heart, teardrop and feather"),
    ("bracelet-20", "Pearl and Blush",
     "Cream pearls alternating with blush crystal on gold, with a pearl beside the heart.",
     "Glass pearl, crystal, gold plate", "Open heart and pearl drop"),
    ("jewellery-05", "Aquamarine and Pearl",
     "Pale aquamarine rounds between freshwater pearls, with an adjustable extension chain.",
     "Aquamarine, freshwater pearl, silver", "Filigree heart charm"),
    ("jewellery-06", "Turquoise Leather Wrap",
     "Turquoise and jasper stitched onto brown leather, wrapping three times.",
     "Turquoise, jasper, leather", "Tree-of-life button fastening"),
    ("jewellery-10", "Amethyst Toggle",
     "Small amethyst rounds spaced along silver wire, with an adjustable toggle.",
     "Amethyst, silver plate", "Filigree heart charm"),
    ("jewellery-13", "Amethyst Leather Wrap",
     "Deep amethyst rounds on brown leather, wrapping twice.",
     "Amethyst, leather, silver", "Medallion button fastening"),
    ("jewellery-16", "Rose Quartz Wrap",
     "Rose quartz on blush leather with silver beads at the join.",
     "Rose quartz, leather, silver", "Lotus charm"),
]

CROCHET = [
    ("crochet-01", "Koala",
     "Worked in soft grey cotton with a cream belly and generously stuffed ears.",
     "Cotton yarn, safety eyes", "Sits unaided, about 20 cm"),
    ("crochet-02", "Sloth",
     "Long arms with separately worked fingers, so it hangs off a cot rail or a hand.",
     "Cotton yarn, safety eyes", "Hanging arms, about 25 cm"),
    ("crochet-03", "Teddy Bear",
     "A classic jointed-look bear in warm brown, wearing a sage scarf.",
     "Cotton yarn, safety eyes", "Removable scarf"),
    ("crochet-04", "Giraffe",
     "Golden yellow with hand-placed brown patches and small stubby horns.",
     "Cotton yarn, safety eyes", "About 22 cm seated"),
    ("crochet-05", "Elephant",
     "Lilac with wide floppy ears and a small flower stitched behind one.",
     "Cotton yarn, safety eyes", "Flower detail"),
    ("crochet-06", "Puppy Drawstring Bag",
     "A lined drawstring bag with floppy ears and a stitched nose, closed with wooden beads.",
     "Cotton yarn, wooden beads", "Lined, drawstring top"),
    ("crochet-07", "Woodland Cot Mobile",
     "Bear, elephant and fox hanging from a beech ring between crocheted clouds and leaves.",
     "Cotton yarn, beech ring", "Nursery mobile"),
    ("crochet-08", "Bunny Storage Basket",
     "A firm-sided basket with a bunny looking over the rim and a leaf on the front.",
     "Cotton yarn", "Holds its shape when empty"),
    ("crochet-09", "Lamb Comforter",
     "A soft square comforter with a sleeping lamb's head, worked in an open shell stitch.",
     "Cotton yarn", "Comforter, about 30 cm square"),
    ("crochet-10", "Frog Shoulder Bag",
     "Bright green with a wide smile, pink cheeks and a long strap for small shoulders.",
     "Cotton yarn, safety eyes", "Long shoulder strap"),
    ("crochet-11", "Grey Elephant",
     "The plainest of the animals — grey with pale toes and nothing else.",
     "Cotton yarn, safety eyes", "About 20 cm seated"),
    ("crochet-12", "Bunny with Bow",
     "Sand-coloured with tall ears and a lilac satin ribbon.",
     "Cotton yarn, satin ribbon", "Ribbon can be left off"),
    ("crochet-13", "Lion",
     "A golden body ringed by a mane worked in loops rather than fringe.",
     "Cotton yarn, safety eyes", "Looped mane"),
    ("crochet-14", "Fox",
     "Rust orange with a cream chest and a white-tipped tail that curls round.",
     "Cotton yarn, safety eyes", "Curled tail"),
    ("crochet-15", "Dinosaur",
     "Sage green with a row of mustard spines down the back and tail.",
     "Cotton yarn, safety eyes", "Sewn-on spines"),
    ("crochet-16", "Star Cot Mobile",
     "Elephant and giraffe with stars and clouds, balanced so it hangs level.",
     "Cotton yarn, beech ring", "Nursery mobile"),
    ("crochet-17", "Drawstring Pouch",
     "Undyed cotton with tasselled ties — for toys, wash things or a gift.",
     "Undyed cotton yarn", "Tasselled drawstring"),
    ("crochet-18", "Ring Rattles",
     "Elephant, lion and bunny on beech teething rings, sold singly or as three.",
     "Cotton yarn, beech ring", "Set of three or singly"),
    ("crochet-19", "Bunting Basket",
     "A cream basket with pastel bunting stitched round the rim and small side handles.",
     "Cotton yarn", "Side handles"),
]

JEWELLERY = [
    ("jewellery-01", "Amethyst Tree of Life Pendant",
     "Silver wire woven into a tree, with amethyst chips wired on as the leaves.",
     "Amethyst, silver-plated wire", "On a silver chain"),
    ("jewellery-02", "Amethyst Hoop Drops",
     "Hammered silver hoops with a faceted amethyst teardrop hanging below each.",
     "Amethyst, sterling ear wires", "About 5 cm drop"),
    ("jewellery-03", "Turquoise Copper Ring",
     "Copper wire coiled into spirals either side of a single turquoise round.",
     "Turquoise, copper wire", "Made to finger size"),
    ("jewellery-04", "Labradorite Pendant",
     "An oval labradorite caught in woven copper, with a small leaf at the bail.",
     "Labradorite, copper wire", "Copper chain and leaf charm"),
    ("jewellery-07", "Blue Cascade Earrings",
     "Fine silver chains hung with blue and clear beads, ending in a faceted topaz drop.",
     "Glass, quartz, silver", "About 7 cm drop"),
    ("jewellery-08", "Rainbow Tree of Life Pendant",
     "The same woven tree, with the leaves graded right through the spectrum.",
     "Mixed gemstone chips, silver-plated wire", "On a silver chain"),
    ("jewellery-09", "Copper Spiral Earrings",
     "Concentric copper coils inside a teardrop frame, weighted by a green jade bead.",
     "Jade, copper wire", "About 5 cm drop"),
    ("jewellery-11", "Labradorite Teardrop Pendant",
     "A large teardrop labradorite in a close copper weave that follows the stone's flash.",
     "Labradorite, copper wire", "Copper chain"),
    ("jewellery-12", "Silver Heart Earrings",
     "Silver wire bent by hand into open hearts, each with an amethyst bead at the point.",
     "Amethyst, silver-plated wire", "About 4 cm drop"),
    ("jewellery-14", "Sea Glass Pendant",
     "A piece of aqua sea glass held in a spiral of silver wire, no two the same shape.",
     "Sea glass, silver-plated wire", "On a silver chain"),
    ("jewellery-15", "Pearl and Aqua Cascade",
     "Freshwater pearls and pale aqua beads on silver chain, finished with a blue topaz drop.",
     "Freshwater pearl, glass, silver", "About 7 cm drop"),
    ("jewellery-17", "Turquoise Statement Ring",
     "A large oval turquoise in a rope-edged silver setting with bead detail.",
     "Turquoise, silver", "Made to finger size"),
]

PAGES = {
    "bracelets": {
        "title": "Bracelets",
        "file": "bracelets.html",
        "texture": "bead",
        "heading": "Bracelets and wraps",
        "intro": "Beaded, wire-linked and leather-wrapped, from single-charm everyday "
                 "pieces to full-spectrum statement bracelets. Most can be remade in "
                 "different colours or to a different wrist size.",
        "items": BRACELETS,
    },
    "crochet": {
        "title": "Crochet",
        "file": "crochet.html",
        "texture": "stitch",
        "heading": "Crochet and nursery",
        "intro": "Amigurumi animals, cot mobiles, baskets and bags, worked in cotton yarn. "
                 "Everything here is stuffed firmly enough to keep its shape and made to "
                 "survive being loved hard.",
        "items": CROCHET,
    },
    "jewellery": {
        "title": "Jewellery",
        "file": "jewellery.html",
        "texture": "bead",
        "heading": "Necklaces, earrings and rings",
        "intro": "Wire-wrapped stones, woven tree pendants and hand-formed silver. "
                 "Each stone is different, so no two of these come out identical even "
                 "when the design is the same.",
        "items": JEWELLERY,
    },
}

RATIOS = ["ratio-45", "ratio-11", "ratio-34"]


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def head(title, description, css_extra=""):
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="theme-color" content="#EEF0EE">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='15' fill='%236E3552'/%3E%3Ccircle cx='16' cy='16' r='6.5' fill='none' stroke='%23EEF0EE' stroke-width='2.4'/%3E%3Ccircle cx='16' cy='5.5' r='2.6' fill='%23EEF0EE'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:SOFT,WONK,opsz,wght@0..100,0..1,9..144,300..700&family=Karla:wght@300..700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="assets/style.css">{css_extra}
</head>
<body>

<a class="skip" href="#main">Skip to the main content</a>
"""


def header(active=""):
    def link(href, label, key):
        current = ' aria-current="page"' if key == active else ""
        return f'    <a href="{href}"{current}>{label}</a>'

    return f"""
<header class="site-head">
  <a class="wordmark" href="index.html">
    <!-- The logo replaces the text below as soon as images/logo.svg or
         images/logo.png exists. Until then the text shows. -->
    <img class="wordmark__logo" alt="Beadwell Bracelets &amp; Crafts" hidden>
    <span class="wordmark__text">
      <span class="wordmark__main">Beadwell</span>
      <span class="wordmark__sub">Bracelets &amp; Crafts</span>
    </span>
  </a>
  <nav class="site-nav" aria-label="Main">
{link("bracelets.html", "Bracelets", "bracelets")}
{link("crochet.html", "Crochet", "crochet")}
{link("jewellery.html", "Jewellery", "jewellery")}
{link("index.html#about", "About", "about")}
    <a href="#enquire" class="nav-cta">Enquire</a>
  </nav>
</header>
"""


def card(stem, name, desc, materials, detail, ref, texture, ratio):
    alt = esc(name)
    return f"""        <article class="piece">
          <div class="piece__media {ratio}">
            <canvas class="texture" data-texture="{texture}" data-seed="{stem}"></canvas>
            <img class="photo" src="images/{stem}.jpg" alt="{alt}" loading="lazy" decoding="async">
            <span class="filehint">Photo goes here &middot; {stem}.jpg</span>
          </div>
          <div class="piece__body">
            <h3>{esc(name)}</h3>
            <p>{esc(desc)}</p>
            <dl class="spec">
              <div><dt>Ref</dt><dd>{ref}</dd></div>
              <div><dt>Materials</dt><dd>{esc(materials)}</dd></div>
              <div><dt>Detail</dt><dd>{esc(detail)}</dd></div>
            </dl>
            <button type="button" class="enquire-btn" data-piece="{esc(name)}" data-ref="{ref}">Enquire about this piece</button>
          </div>
        </article>
"""


def enquire_section():
    return """
  <section id="enquire" class="section section--alt">
    <div class="spine" aria-hidden="true"><span>Enquire</span></div>
    <div class="section__body enquire">
      <div class="enquire__intro">
        <h2>Send a note</h2>
        <p>This goes straight to our inbox. There's no payment on the site — no card
          details, no checkout — just a message, and we'll reply to you directly.</p>
        <p class="fineprint">Prefer email? Write to
          <!-- EDIT: swap this for your real address. -->
          <a href="mailto:hello@beadwellbracelets.co.uk">hello@beadwellbracelets.co.uk</a>.</p>
      </div>

      <form class="form" name="enquiry" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="/thanks.html">
        <input type="hidden" name="form-name" value="enquiry">
        <p class="hp"><label>Leave this empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>

        <div class="field-row" id="about-piece" hidden>
          <p class="about-piece__label">
            Enquiring about <strong id="about-piece__name"></strong>
            <span class="mono" id="about-piece__ref"></span>
            <button type="button" class="linkish" id="clear-piece">clear</button>
          </p>
          <input type="hidden" name="piece" id="piece-field" value="">
        </div>

        <div class="field-row two">
          <p class="field">
            <label for="name">Your name</label>
            <input id="name" name="name" type="text" autocomplete="name" required>
          </p>
          <p class="field">
            <label for="email">Email</label>
            <input id="email" name="email" type="email" autocomplete="email" required>
          </p>
        </div>

        <p class="field">
          <label for="message">What would you like to know?</label>
          <textarea id="message" name="message" rows="6" required></textarea>
        </p>

        <div class="form__foot">
          <button type="submit" class="btn btn--solid">Send the note</button>
          <span class="fineprint">We'll reply within a day or two.</span>
        </div>
        <p class="form__status" id="form-status" role="status" hidden></p>
      </form>
    </div>
  </section>
"""


def footer():
    return """
<footer class="site-foot">
  <div class="site-foot__brand">
    <img class="foot-logo" alt="Beadwell Bracelets &amp; Crafts" hidden>
    <span class="wordmark__main foot-mark">Beadwell</span>
    <p>Crochet and hand-strung beaded jewellery, made one at a time.</p>
  </div>
  <nav class="site-foot__links" aria-label="Footer">
    <a href="bracelets.html">Bracelets</a>
    <a href="crochet.html">Crochet</a>
    <a href="jewellery.html">Jewellery</a>
    <!-- EDIT: point this at your real Instagram handle, or delete the line. -->
    <a href="https://instagram.com/" rel="me noopener" target="_blank">Instagram</a>
    <a href="mailto:hello@beadwellbracelets.co.uk">hello@beadwellbracelets.co.uk</a>
  </nav>
  <p class="site-foot__legal">© <span id="year">2026</span> Beadwell Bracelets &amp; Crafts. Every piece made by hand.</p>
</footer>

<script src="assets/app.js"></script>
</body>
</html>
"""


def build_category(key, page):
    prefix = {"bracelets": "BR", "crochet": "CR", "jewellery": "JW"}[key]
    cards = "".join(
        card(stem, name, desc, materials, detail,
             f"{prefix}·{n:02d}", page["texture"], RATIOS[(n - 1) % len(RATIOS)])
        for n, (stem, name, desc, materials, detail) in enumerate(page["items"], 1)
    )

    count = len(page["items"])
    html = head(f"{page['title']} — Beadwell Bracelets & Crafts", page["intro"])
    html += header(key)
    html += f"""
<main id="main">

  <section class="section page-head">
    <div class="spine" aria-hidden="true"><span>{esc(page['title'])}</span></div>
    <div class="section__body">
      <p class="eyebrow">{count} pieces</p>
      <h1>{esc(page['heading'])}</h1>
      <p class="lede">{esc(page['intro'])}</p>
      <p class="note">Nothing is sold through the site. Use <strong>Enquire</strong> on any
        piece and we'll come back to you with sizing, colours and price.</p>
    </div>
  </section>

  <section class="section">
    <div class="spine" aria-hidden="true"><span>The pieces</span></div>
    <div class="section__body">
      <div class="grid">
{cards}      </div>
    </div>
  </section>
{enquire_section()}
</main>
{footer()}"""
    return html


def build_index():
    featured = [
        ("bracelets.html", "Bracelets", BRACELETS[0][0], "bead",
         f"{len(BRACELETS)} pieces",
         "Beaded, wire-linked and leather-wrapped, with a charm at the clasp."),
        ("crochet.html", "Crochet", CROCHET[2][0], "stitch",
         f"{len(CROCHET)} pieces",
         "Amigurumi animals, cot mobiles, baskets and bags in cotton yarn."),
        ("jewellery.html", "Jewellery", JEWELLERY[0][0], "bead",
         f"{len(JEWELLERY)} pieces",
         "Wire-wrapped stones, woven tree pendants and hand-formed silver."),
    ]

    cards = ""
    for href, title, stem, texture, count, blurb in featured:
        cards += f"""        <a class="cat" href="{href}">
          <div class="piece__media ratio-45">
            <canvas class="texture" data-texture="{texture}" data-seed="cat-{title.lower()}"></canvas>
            <img class="photo" src="images/{stem}.jpg" alt="" loading="lazy" decoding="async">
          </div>
          <div class="cat__body">
            <p class="eyebrow">{count}</p>
            <h3>{title}</h3>
            <p>{blurb}</p>
            <span class="cat__go">View the {title.lower()} &rarr;</span>
          </div>
        </a>
"""

    html = head("Beadwell Bracelets & Crafts",
                "A small workshop making crochet pieces and hand-strung beaded jewellery, "
                "one at a time. Browse the collection and send a note about anything that "
                "catches your eye.")
    html += header("home")
    html += f"""
<main id="main">

  <section class="hero">
    <div class="hero__text">
      <p class="eyebrow reveal">Handmade · One of a kind</p>
      <h1 class="reveal">Every stitch counted, every bead strung by hand.</h1>
      <p class="lede reveal">Beadwell is a small team making crochet pieces and beaded jewellery in
        small numbers. Nothing here is mass-made, and nothing comes out quite the same
        way twice.</p>
      <div class="hero__actions reveal">
        <a class="btn btn--solid" href="bracelets.html">See the bracelets</a>
        <a class="btn btn--ghost" href="#enquire">Ask about a piece</a>
      </div>
    </div>
    <figure class="hero__swatch reveal" aria-hidden="true">
      <canvas class="texture" data-texture="stitch" data-seed="beadwell-hero"></canvas>
    </figure>
  </section>

  <section id="collection" class="section">
    <div class="spine" aria-hidden="true"><span>The Collection</span></div>
    <div class="section__body">
      <header class="section__head">
        <h2>Three things we make</h2>
        <p class="note">There's no checkout here — this is a place to look rather than buy.
          If something catches your eye, use <strong>Enquire</strong> and we'll come back
          to you with sizing, colours and price.</p>
      </header>
      <div class="cats">
{cards}      </div>
    </div>
  </section>

  <section id="about" class="section section--alt">
    <div class="spine" aria-hidden="true"><span>About</span></div>
    <div class="section__body about">
      <div class="about__text">
        <h2>Made slowly, on purpose</h2>
        <p>Between us we've been crocheting and beading for most of our lives. What
          started as something to do with our hands in the evening turned into more
          pieces than the house can reasonably hold, which is how this page came about.</p>
        <p>Everything is made by hand, at home, from materials we pick ourselves —
          natural fibres where we can, glass and real stone rather than plastic, and
          proper findings so a clasp doesn't give out after a fortnight. A bracelet takes
          an evening. A blanket takes considerably longer.</p>
        <p>Colours are the part we enjoy most. If you like a piece but not its palette,
          that's an easy thing to change — most of what you see here can be remade in
          whatever suits you.</p>
        <p>We're not a shop and don't want to be one. If something here appeals, send a
          note and we'll work it out between us.</p>
      </div>
      <figure class="about__swatch" aria-hidden="true">
        <div class="piece__media ratio-45">
          <canvas class="texture" data-texture="stitch" data-seed="workbench"></canvas>
          <img class="photo" src="images/workspace.jpg" alt="" loading="lazy" decoding="async">
          <span class="filehint">Photo goes here &middot; workspace.jpg</span>
        </div>
      </figure>
    </div>
  </section>

  <section id="commissions" class="section">
    <div class="spine" aria-hidden="true"><span>Commissions</span></div>
    <div class="section__body">
      <header class="section__head">
        <h2>How a commission works</h2>
        <p class="note">Three steps, and no money changes hands until the second one.</p>
      </header>
      <ol class="steps">
        <li>
          <span class="steps__num">01</span>
          <h3>Send a note</h3>
          <p>Tell us what you're after — a piece from the collection in different colours,
            or something entirely your own. Photos of what you like are genuinely useful.</p>
        </li>
        <li>
          <span class="steps__num">02</span>
          <h3>We settle the details</h3>
          <p>We'll come back with materials, colours, sizing, a price and a rough timescale.
            Nothing starts until you're happy with all of it.</p>
        </li>
        <li>
          <span class="steps__num">03</span>
          <h3>It gets made</h3>
          <p>We'll send a photo or two along the way. Small pieces take a week or so; larger
            crochet work takes longer and we'll always say so up front.</p>
        </li>
      </ol>
    </div>
  </section>
{enquire_section()}
</main>
{footer()}"""
    return html


def main():
    root = os.path.join(os.path.dirname(__file__), "..")
    written = []

    with open(os.path.join(root, "index.html"), "w") as f:
        f.write(build_index())
    written.append(("index.html", 3))

    for key, page in PAGES.items():
        with open(os.path.join(root, page["file"]), "w") as f:
            f.write(build_category(key, page))
        written.append((page["file"], len(page["items"])))

    for name, count in written:
        print(f"  {name:<18} {count} items")
    total = sum(len(p["items"]) for p in PAGES.values())
    print(f"\n{total} pieces across three category pages.")


if __name__ == "__main__":
    main()
