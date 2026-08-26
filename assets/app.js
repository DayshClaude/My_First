/* ============================================================
   Beadwell — site behaviour
   1. Generated stitch / bead textures (placeholders for photos)
   2. Collection filtering
   3. "Enquire about this piece" → prefills the form
   4. Scroll reveals
   ============================================================ */

document.documentElement.classList.add('js');

var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ── 1. Textures ───────────────────────────────────────────
   Each card draws a woven or beaded swatch instead of sitting
   empty. The pattern is seeded from the piece name, so a given
   piece always looks the same but no two pieces match.
   A real photo in images/ covers this up automatically.
   ------------------------------------------------------- */

// Turn a string into a number, so each seed gives a repeatable pattern.
function hashSeed(str) {
  var h = 2166136261;
  for (var i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

// Small deterministic random number generator (mulberry32).
function rng(seed) {
  var a = seed;
  return function () {
    a |= 0; a = a + 0x6D2B79F5 | 0;
    var t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

function readPalette() {
  var s = getComputedStyle(document.documentElement);
  return {
    ground: s.getPropertyValue('--paper-2').trim() || '#E4E8E5',
    thread: s.getPropertyValue('--accent').trim() || '#6E3552',
    brass:  s.getPropertyValue('--brass').trim() || '#A8813F',
    ink:    s.getPropertyValue('--ink').trim() || '#22262A'
  };
}

// Colours to draw bands in. The brand colours appear more often than the
// neutral, so a swatch reads as damson-and-brass rather than mostly grey.
function weave(pal) {
  return [pal.thread, pal.thread, pal.thread, pal.brass, pal.brass, pal.ink];
}

// Crochet: rows of chained V-stitches, offset row to row.
function drawStitch(ctx, w, h, rand, pal) {
  // Aim for a stitch about 34px across whatever the card's width, so the
  // texture keeps the same scale on a phone as on a desktop.
  var cols = Math.max(5, Math.round(w / 34));
  var step = w / cols;
  var rowH = step * 0.78;
  var rows = Math.ceil(h / rowH) + 1;
  var hues = weave(pal);

  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';
  ctx.lineWidth = Math.max(1.4, step * 0.13);

  for (var r = 0; r < rows; r++) {
    // Bands of colour, a few rows deep, like a striped blanket.
    var band = hues[Math.floor(rand() * hues.length)];
    var bandRows = 1 + Math.floor(rand() * 3);
    var alpha = 0.16 + rand() * 0.24;

    for (var b = 0; b < bandRows && r < rows; b++, r++) {
      var y = r * rowH;
      var offset = (r % 2) * step * 0.5;
      ctx.strokeStyle = band;
      ctx.globalAlpha = alpha;

      for (var c = -1; c <= cols; c++) {
        var x = c * step + offset;
        var jx = (rand() - 0.5) * step * 0.09;
        var jy = (rand() - 0.5) * rowH * 0.09;
        ctx.beginPath();
        ctx.moveTo(x + jx, y + jy);
        ctx.lineTo(x + step * 0.5 + jx, y + rowH * 0.72 + jy);
        ctx.lineTo(x + step + jx, y + jy);
        ctx.stroke();
      }
    }
    r--; // the inner loop already advanced r
  }
  ctx.globalAlpha = 1;
}

// Beadwork: strands of round beads with a highlight on each.
function drawBead(ctx, w, h, rand, pal) {
  // Same idea as the stitches: a bead stays roughly 30px across at any size.
  var perRow = Math.max(5, Math.round(w / 30));
  var d = w / perRow;
  var rows = Math.ceil(h / (d * 0.92)) + 1;
  var hues = weave(pal);

  for (var r = 0; r < rows; r++) {
    var y = r * d * 0.92 + d * 0.5;
    var offset = (r % 2) * d * 0.5;
    var band = hues[Math.floor(rand() * hues.length)];
    var alpha = 0.18 + rand() * 0.26;

    // The thread the beads sit on.
    ctx.strokeStyle = pal.ink;
    ctx.globalAlpha = alpha * 0.35;
    ctx.lineWidth = Math.max(0.8, d * 0.045);
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(w, y);
    ctx.stroke();

    for (var c = -1; c <= perRow; c++) {
      var x = c * d + offset + d * 0.5;
      var rad = d * (0.3 + rand() * 0.1);
      ctx.globalAlpha = alpha;
      ctx.fillStyle = band;
      ctx.beginPath();
      ctx.arc(x, y, rad, 0, Math.PI * 2);
      ctx.fill();

      // Glass catches the light on the upper left of each bead.
      ctx.globalAlpha = alpha * 0.5;
      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(x - rad * 0.3, y - rad * 0.3, rad * 0.26, 0, Math.PI * 2);
      ctx.fill();
    }
  }
  ctx.globalAlpha = 1;
}

function paint(canvas) {
  var rect = canvas.getBoundingClientRect();
  if (!rect.width || !rect.height) return;

  var dpr = Math.min(window.devicePixelRatio || 1, 2);
  canvas.width = Math.round(rect.width * dpr);
  canvas.height = Math.round(rect.height * dpr);

  var ctx = canvas.getContext('2d');
  if (!ctx) return;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

  var pal = readPalette();
  var rand = rng(hashSeed(canvas.dataset.seed || 'beadwell'));

  ctx.fillStyle = pal.ground;
  ctx.fillRect(0, 0, rect.width, rect.height);

  if (canvas.dataset.texture === 'bead') {
    drawBead(ctx, rect.width, rect.height, rand, pal);
  } else {
    drawStitch(ctx, rect.width, rect.height, rand, pal);
  }
}

var canvases = Array.prototype.slice.call(document.querySelectorAll('canvas.texture'));

function paintAll() { canvases.forEach(paint); }

// Repaint on resize (debounced) and when the colour scheme flips.
var resizeTimer;
window.addEventListener('resize', function () {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(paintAll, 150);
});

var darkQuery = window.matchMedia('(prefers-color-scheme: dark)');
if (darkQuery.addEventListener) darkQuery.addEventListener('change', paintAll);

// Web fonts don't affect the canvas, but layout settling does.
if (document.fonts && document.fonts.ready) document.fonts.ready.then(paintAll);
paintAll();

/* ── 2. Filtering ──────────────────────────────────────── */

var chips = Array.prototype.slice.call(document.querySelectorAll('.chip'));
var pieces = Array.prototype.slice.call(document.querySelectorAll('.piece'));
var emptyMsg = document.getElementById('empty');

function applyFilter(cat) {
  var shown = 0;
  pieces.forEach(function (piece) {
    var match = cat === 'all' || piece.dataset.cat === cat;
    piece.hidden = !match;
    if (match) shown++;
  });

  chips.forEach(function (chip) {
    var active = chip.dataset.filter === cat;
    chip.classList.toggle('is-active', active);
    chip.setAttribute('aria-pressed', active ? 'true' : 'false');
  });

  if (emptyMsg) emptyMsg.hidden = shown > 0;
  // Columns reflow, so the canvases need redrawing at their new sizes.
  requestAnimationFrame(paintAll);
}

chips.forEach(function (chip) {
  chip.addEventListener('click', function () { applyFilter(chip.dataset.filter); });
});

document.querySelectorAll('.empty .linkish').forEach(function (btn) {
  btn.addEventListener('click', function () { applyFilter(btn.dataset.filter); });
});

/* ── 3. Enquire → prefill the form ─────────────────────── */

var aboutPiece = document.getElementById('about-piece');
var aboutName = document.getElementById('about-piece__name');
var aboutRef = document.getElementById('about-piece__ref');
var pieceField = document.getElementById('piece-field');
var messageField = document.getElementById('message');
var nameField = document.getElementById('name');

function setPiece(name, ref) {
  if (!aboutPiece) return;
  aboutName.textContent = name;
  aboutRef.textContent = ref;
  pieceField.value = name + ' (' + ref + ')';
  aboutPiece.hidden = false;

  // Only write a suggested message into an empty box — never
  // overwrite something the visitor has already typed.
  if (messageField && !messageField.value.trim()) {
    messageField.value = 'Hello — I’d love to know more about the ' + name + '. ';
  }
}

function clearPiece() {
  if (!aboutPiece) return;
  aboutPiece.hidden = true;
  pieceField.value = '';
  aboutName.textContent = '';
  aboutRef.textContent = '';
}

document.querySelectorAll('.enquire-btn').forEach(function (btn) {
  btn.addEventListener('click', function () {
    setPiece(btn.dataset.piece, btn.dataset.ref);
    document.getElementById('enquire').scrollIntoView({
      behavior: reduceMotion ? 'auto' : 'smooth',
      block: 'start'
    });
    // Wait for the scroll before taking focus, or the browser jumps.
    setTimeout(function () { if (nameField) nameField.focus({ preventScroll: true }); }, reduceMotion ? 0 : 600);
  });
});

var clearBtn = document.getElementById('clear-piece');
if (clearBtn) clearBtn.addEventListener('click', clearPiece);

/* Preview builds have no Netlify behind them, so show what would
   happen instead of navigating to a page that isn't there. */
if (document.documentElement.hasAttribute('data-preview')) {
  var form = document.querySelector('form.form');
  var status = document.getElementById('form-status');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!status) return;
    status.hidden = false;
    status.textContent = 'This is a preview, so nothing was sent. On the live site this note goes '
      + 'straight to the workshop inbox and the visitor lands on a thank-you page.';
  });
}

/* ── 4. Reveals + the year in the footer ───────────────── */

var yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = String(new Date().getFullYear());

if (!reduceMotion && 'IntersectionObserver' in window) {
  pieces.forEach(function (p) { p.classList.add('will-reveal'); });

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-in');
      observer.unobserve(entry.target);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });

  document.querySelectorAll('.reveal, .piece').forEach(function (el, i) {
    el.style.transitionDelay = Math.min(i, 6) * 60 + 'ms';
    observer.observe(el);
  });
} else {
  document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('is-in'); });
}
