#!/usr/bin/env node
/**
 * interaction_state_probe.js — measured hover / focus-visible audit for kriskrug.co
 *
 * Answers, per route, for every interactive element actually rendered:
 *
 *   1. Does :hover change any visual property?          (measured, not grepped)
 *   2. Does :focus-visible change any visual property?  (measured)
 *   3. If focus does change something, is it the theme's ring or the browser's
 *      UA default ring (outline-style: auto)?
 *   4. Is a focus outline suppressed (outline: none / 0) with no replacement?
 *      -> WCAG 2.4.7 failure candidate.
 *   5. Where a state rule EXISTS in CSS and matches the element but the computed
 *      style does not change, the rule is losing the cascade. That is reported
 *      separately from "no rule at all", because they are different fixes.
 *   6. Real keyboard tab-through: order, reachability, and visible focus at each
 *      stop, driven by actual Tab keypresses.
 *
 * HOW IT WORKS
 * ------------
 * Chromium in this sandbox cannot reach the public internet (the agent HTTPS
 * proxy resets browser connections), but curl can. So the script:
 *
 *   a) mirrors each route's live HTML with curl, plus every stylesheet and
 *      script it links, rewriting those URLs to local relative paths;
 *   b) serves the mirror from 127.0.0.1 so document.styleSheets is same-origin
 *      and cssRules are readable;
 *   c) drives real Chromium against it.
 *
 * Ground truth is therefore the live rendered markup + the live Jetpack Boost
 * CSS bundle + the live theme.json global styles, not the repo's CSS files.
 * That matters: most of this site's markup lives in the WordPress database.
 *
 * State forcing uses CDP `CSS.forcePseudoState`, the same mechanism DevTools'
 * ":hov" toggles use. It is geometry independent, so occluded or off-screen
 * elements are measured exactly like visible ones. The keyboard pass is
 * separate and uses genuine Tab keypresses.
 *
 * USAGE
 * -----
 *   PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers \
 *     node scripts/interaction_state_probe.js --out /tmp/probe
 *
 *   # re-run analysis without re-fetching
 *   node scripts/interaction_state_probe.js --out /tmp/probe --skip-mirror
 *
 *   # a subset of routes
 *   node scripts/interaction_state_probe.js --out /tmp/probe --routes / /contact/
 *
 * Options:
 *   --base <url>       origin to mirror                (default https://kriskrug.co)
 *   --routes <r...>    routes to audit                 (default: the 8 main-nav routes)
 *   --out <dir>        output directory                (required)
 *   --skip-mirror      reuse an existing mirror in <out>/mirror
 *   --port <n>         local server port               (default 8731)
 *   --viewport <wxh>   viewport                        (default 1440x900)
 *   --max-tabs <n>     Tab keypress budget per route   (default 400)
 *   --reduced-motion   emulate prefers-reduced-motion: reduce (default: no-preference)
 *   --json-only        skip the markdown summary
 *
 * Writes <out>/probe.json (full data) and <out>/summary.md (human summary).
 * Read-only: it never writes to WordPress and never touches theme/.
 *
 * REQUIREMENTS
 * ------------
 * Playwright (global install at /opt/node22/lib/node_modules is auto-detected)
 * and a preinstalled Chromium. The script REFUSES to download a browser: if
 * PLAYWRIGHT_BROWSERS_PATH is unset or Chromium is missing it fails loudly,
 * per AURORA-STYLESHEET-REBUILD-PLAN.md section 4.6.
 */

'use strict';

const fs = require('fs');
const path = require('path');
const http = require('http');
const { execFileSync } = require('child_process');

// --------------------------------------------------------------------------
// Playwright resolution — never download, fail loudly (rebuild plan 4.1/4.6)
// --------------------------------------------------------------------------

function loadPlaywright() {
  const candidates = [
    'playwright',
    '/opt/node22/lib/node_modules/playwright',
    '/usr/lib/node_modules/playwright',
    '/usr/local/lib/node_modules/playwright',
  ];
  for (const c of candidates) {
    try {
      return require(c);
    } catch (_) {
      /* next */
    }
  }
  console.error(
    'FATAL: playwright is not resolvable. Install it globally or set NODE_PATH.\n' +
      'Do NOT run `playwright install` — Chromium is preinstalled at /opt/pw-browsers.'
  );
  process.exit(2);
}

function assertBrowsersPath() {
  const p = process.env.PLAYWRIGHT_BROWSERS_PATH;
  if (!p) {
    console.error(
      'FATAL: PLAYWRIGHT_BROWSERS_PATH is unset. Re-run with\n' +
        '  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node scripts/interaction_state_probe.js ...\n' +
        'Refusing to trigger a browser download.'
    );
    process.exit(2);
  }
  if (!fs.existsSync(p)) {
    console.error(`FATAL: PLAYWRIGHT_BROWSERS_PATH=${p} does not exist.`);
    process.exit(2);
  }
}

// --------------------------------------------------------------------------
// CLI
// --------------------------------------------------------------------------

const DEFAULT_ROUTES = [
  '/',
  '/about/',
  '/speaking/',
  '/services/',
  '/work/',
  '/blog/',
  '/photography/',
  '/contact/',
];

function parseArgs(argv) {
  const out = {
    base: 'https://kriskrug.co',
    routes: null,
    out: null,
    skipMirror: false,
    port: 8731,
    viewport: { width: 1440, height: 900 },
    maxTabs: 400,
    jsonOnly: false,
    reducedMotion: false,
  };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--base') out.base = argv[++i];
    else if (a === '--out') out.out = argv[++i];
    else if (a === '--skip-mirror') out.skipMirror = true;
    else if (a === '--json-only') out.jsonOnly = true;
    else if (a === '--reduced-motion') out.reducedMotion = true;
    else if (a === '--port') out.port = Number(argv[++i]);
    else if (a === '--max-tabs') out.maxTabs = Number(argv[++i]);
    else if (a === '--viewport') {
      const [w, h] = argv[++i].split('x').map(Number);
      out.viewport = { width: w, height: h };
    } else if (a === '--routes') {
      out.routes = [];
      while (i + 1 < argv.length && !argv[i + 1].startsWith('--')) out.routes.push(argv[++i]);
    } else if (a === '--help' || a === '-h') {
      console.log(fs.readFileSync(__filename, 'utf8').split('*/')[0]);
      process.exit(0);
    } else {
      console.error(`unknown argument: ${a}`);
      process.exit(2);
    }
  }
  if (!out.routes) out.routes = DEFAULT_ROUTES.slice();
  if (!out.out) {
    console.error('FATAL: --out <dir> is required');
    process.exit(2);
  }
  return out;
}

// --------------------------------------------------------------------------
// Phase 1 — mirror with curl (the browser has no outbound network here)
// --------------------------------------------------------------------------

function curl(url, destFile) {
  execFileSync('curl', ['-sS', '-L', '--fail', '--max-time', '60', '-o', destFile, url], {
    stdio: ['ignore', 'ignore', 'pipe'],
  });
}

function routeSlug(route) {
  const s = route.replace(/^\/|\/$/g, '').replace(/[^a-zA-Z0-9._-]/g, '_');
  return s === '' ? 'home' : s;
}

function mirror(opts) {
  const mdir = path.join(opts.out, 'mirror');
  const adir = path.join(mdir, 'assets');
  fs.mkdirSync(adir, { recursive: true });

  const assetMap = new Map(); // absolute url -> local relative path
  let assetIdx = 0;

  const fetchAsset = (url, ext) => {
    if (assetMap.has(url)) return assetMap.get(url);
    const name = `a${String(assetIdx++).padStart(3, '0')}${ext}`;
    const dest = path.join(adir, name);
    try {
      curl(url, dest);
    } catch (e) {
      process.stderr.write(`  ! asset failed ${url}\n`);
      assetMap.set(url, null);
      return null;
    }
    const rel = `assets/${name}`;
    assetMap.set(url, rel);
    return rel;
  };

  const pages = [];
  for (const route of opts.routes) {
    const slug = routeSlug(route);
    const htmlPath = path.join(mdir, `${slug}.html`);
    const url = opts.base.replace(/\/$/, '') + route;
    process.stderr.write(`mirroring ${url}\n`);
    curl(url, htmlPath);
    let html = fs.readFileSync(htmlPath, 'utf8');

    // Rewrite <link rel=stylesheet href="ABS"> and <script src="ABS">
    html = html.replace(
      /(<link\b[^>]*\brel=['"]?stylesheet['"]?[^>]*\bhref=)(['"])(https?:\/\/[^'"]+)\2/gi,
      (m, pre, q, u) => {
        const rel = fetchAsset(u, '.css');
        return rel ? `${pre}${q}${rel}${q}` : m;
      }
    );
    html = html.replace(/(<script\b[^>]*\bsrc=)(['"])(https?:\/\/[^'"]+)\2/gi, (m, pre, q, u) => {
      const rel = fetchAsset(u, '.js');
      return rel ? `${pre}${q}${rel}${q}` : m;
    });

    fs.writeFileSync(htmlPath, html);
    pages.push({ route, slug, file: `${slug}.html`, bytes: Buffer.byteLength(html) });
  }
  fs.writeFileSync(
    path.join(mdir, '_manifest.json'),
    JSON.stringify({ base: opts.base, capturedAt: new Date().toISOString(), pages }, null, 2)
  );
  return { mdir, pages };
}

// --------------------------------------------------------------------------
// Phase 2 — local static server
// --------------------------------------------------------------------------

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json',
};

function serve(root, port) {
  const srv = http.createServer((req, res) => {
    const rel = decodeURIComponent(req.url.split('?')[0]);
    const file = path.join(root, rel === '/' ? '/home.html' : rel);
    if (!file.startsWith(root)) {
      res.writeHead(403);
      res.end();
      return;
    }
    fs.readFile(file, (err, data) => {
      if (err) {
        res.writeHead(404, { 'content-type': 'text/plain' });
        res.end('not found');
        return;
      }
      res.writeHead(200, { 'content-type': MIME[path.extname(file)] || 'application/octet-stream' });
      res.end(data);
    });
  });
  return new Promise((resolve) => srv.listen(port, '127.0.0.1', () => resolve(srv)));
}

// 1x1 transparent PNG, used to satisfy image requests so layout is not a wall
// of broken-image icons. Dimensions come from attributes/CSS, not the bytes.
const PIXEL = Buffer.from(
  'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==',
  'base64'
);

// --------------------------------------------------------------------------
// In-page collection code (runs inside the browser)
// --------------------------------------------------------------------------

const PAGE_LIB = `
(() => {
  const VISUAL_PROPS = [
    'color','background-color','background-image','background-position','background-size',
    'border-top-color','border-right-color','border-bottom-color','border-left-color',
    'border-top-width','border-right-width','border-bottom-width','border-left-width',
    'border-top-style','border-radius',
    'outline-color','outline-style','outline-width','outline-offset',
    'box-shadow','text-decoration-line','text-decoration-color','text-decoration-thickness',
    'text-underline-offset','opacity','transform','translate','scale','rotate','filter',
    'letter-spacing','font-weight','text-shadow','cursor','visibility'
  ];
  // cursor/visibility are collected for context but never counted as an
  // affordance on their own.
  const NON_AFFORDANCE = new Set(['cursor','visibility']);

  const INTERACTIVE_SEL = [
    'a[href]','button','input:not([type="hidden"])','select','textarea','summary',
    '[tabindex]','[role="button"]','[role="link"]','[role="tab"]','[role="menuitem"]',
    '[contenteditable=""]','[contenteditable="true"]'
  ].join(',');

  // Container shapes the issue names explicitly: cards and pills. Only counted
  // when they actually contain or are an interactive element.
  const CONTAINER_SEL = [
    '[class*="card"]','[class*="pill"]','[class*="chip"]','[class*="tile"]',
    '[class*="btn"]','[class*="button"]','[class*="-item"]','[class*="tag"]'
  ].join(',');

  // WordPress-generated class shapes. These are not design classes, so an
  // element whose entire class list is noise is a template wrapper, not a
  // component: it must not be reported as "a card missing a hover state".
  const WP_NOISE = /^(wp-|has-|is-|alignwide|alignfull|aligncenter|screen-reader|post-\\d|type-|status-|format-|hentry|category-|tag-|entry-|menu-item|page-|postid-)/;

  const WP_NOISE_EXACT = new Set(['post','page','blog','home','archive','search','single','hentry',
    'sticky','attachment','error404','rtl','widget','sidebar','clearfix','group','row','col','container']);

  function themeClasses(el) {
    return Array.from(el.classList).filter(c => !WP_NOISE.test(c) && !WP_NOISE_EXACT.has(c));
  }

  function signature(el) {
    const tc = themeClasses(el);
    return el.tagName.toLowerCase() + (tc.length ? '.' + tc.join('.') : '');
  }

  function category(el) {
    const tag = el.tagName.toLowerCase();
    const cls = (el.className && el.className.baseVal !== undefined ? el.className.baseVal : el.className) || '';
    if (['input','select','textarea'].includes(tag)) return 'field';
    if (tag === 'button' || el.getAttribute('role') === 'button') return 'button';
    if (tag === 'summary') return 'disclosure';
    if (tag === 'a') {
      if (el.closest('nav, header, .wp-block-navigation')) return 'nav-link';
      if (/btn|button|cta/i.test(cls)) return 'link-button';
      if (/pill|chip|tag|badge/i.test(cls)) return 'pill';
      if (/card/i.test(cls)) return 'card-link';
      if (el.closest('footer')) return 'footer-link';
      return 'link';
    }
    if (/card|tile/i.test(cls)) return 'card';
    if (/pill|chip|tag|badge/i.test(cls)) return 'pill';
    return 'other';
  }

  function domPath(el) {
    const parts = [];
    let n = el;
    while (n && n.nodeType === 1 && parts.length < 6) {
      let s = n.tagName.toLowerCase();
      if (n.id) { s += '#' + n.id; parts.unshift(s); break; }
      const tc = themeClasses(n);
      if (tc.length) s += '.' + tc.slice(0, 3).join('.');
      const sibs = n.parentElement ? Array.from(n.parentElement.children).filter(c => c.tagName === n.tagName) : [];
      if (sibs.length > 1) s += ':nth-of-type(' + (sibs.indexOf(n) + 1) + ')';
      parts.unshift(s);
      n = n.parentElement;
    }
    return parts.join(' > ');
  }

  // Several Aurora components put their whole hover affordance on a generated
  // box (".aurora-link:hover::after", ".aurora-related-row:hover::before").
  // Reading only the element would score those as "no hover state".
  const PE_PROPS = ['content','background-color','background-image','transform','translate',
    'scale','opacity','width','height','border-bottom-color','color','box-shadow','inset','filter'];

  function snapshot(el) {
    const s = getComputedStyle(el);
    const o = {};
    for (const p of VISUAL_PROPS) o[p] = s.getPropertyValue(p);
    for (const pe of ['::before', '::after']) {
      const ps = getComputedStyle(el, pe);
      for (const p of PE_PROPS) o[pe + ' ' + p] = ps.getPropertyValue(p);
    }
    return o;
  }

  // A hover affordance often lands on a DESCENDANT (".card:hover .title").
  // Fingerprint the first N descendants so those are not scored as "no hover".
  const SUBTREE_PROPS = ['color','background-color','background-image','text-decoration-line',
    'transform','opacity','box-shadow','border-bottom-color','outline-style','filter','translate','scale'];
  function subtreeFingerprint(el, limit) {
    const out = [];
    const kids = el.querySelectorAll('*');
    const n = Math.min(kids.length, limit || 40);
    for (let i = 0; i < n; i++) {
      const s = getComputedStyle(kids[i]);
      out.push(SUBTREE_PROPS.map(p => s.getPropertyValue(p)).join('|'));
    }
    return out;
  }
  function subtreeDelta(a, b) {
    if (!a || !b) return 0;
    let n = 0;
    for (let i = 0; i < Math.min(a.length, b.length); i++) if (a[i] !== b[i]) n++;
    return n;
  }

  // Resolve what a declared value WOULD compute to on this element, by applying
  // it inline for one frame. This is how we tell "the rule is a no-op because it
  // declares the value the element already has" from "the rule declares a
  // different value but loses the cascade".
  function resolveDeclared(el, prop, value) {
    const prev = el.style.getPropertyValue(prop);
    const prevPrio = el.style.getPropertyPriority(prop);
    let resolved = null;
    try {
      el.style.setProperty(prop, value, 'important');
      resolved = getComputedStyle(el).getPropertyValue(prop);
    } catch (e) {
      resolved = null;
    }
    el.style.removeProperty(prop);
    if (prev) el.style.setProperty(prop, prev, prevPrio);
    return resolved;
  }

  function diff(a, b) {
    const d = {};
    for (const k of Object.keys(a)) if (a[k] !== b[k]) d[k] = [a[k], b[k]];
    return d;
  }

  function affordanceProps(d) {
    return Object.keys(d).filter(k => !NON_AFFORDANCE.has(k));
  }

  // ---- colour helpers, for WCAG contrast on focus rings -------------------
  function parseRGB(v) {
    const m = String(v).match(/rgba?\\(([^)]+)\\)/);
    if (!m) return null;
    const p = m[1].split(/[,\\s\\/]+/).filter(Boolean).map(Number);
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  }
  function lum(c) {
    const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b);
  }
  function contrast(c1, c2) {
    if (!c1 || !c2) return null;
    const l1 = lum(c1), l2 = lum(c2);
    return Math.round(((Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05)) * 100) / 100;
  }
  function effectiveBg(el) {
    let n = el;
    while (n && n.nodeType === 1) {
      const c = parseRGB(getComputedStyle(n).backgroundColor);
      if (c && c.a > 0.5) return c;
      n = n.parentElement;
    }
    return { r: 255, g: 255, b: 255, a: 1 };
  }

  /**
   * WCAG 1.4.11 contrast for a focus ring, measured against the colour the ring
   * is actually drawn on.
   *
   * An outline with a POSITIVE offset is painted in the gap outside the border
   * box, i.e. over the ANCESTOR's background, not the element's own. Measuring
   * a ring around a filled button against that button's own fill produces a
   * false failure (measured: 1.37:1 against the CTA's orange fill vs 4.67:1
   * against the cream page it is actually drawn on). With offset <= 0 the ring
   * overlaps the element edge, so both neighbours count and the worse wins.
   */
  function ringContrast(el) {
    const cs = getComputedStyle(el);
    if (cs.outlineStyle === 'none' || parseFloat(cs.outlineWidth) === 0) return null;
    const ring = parseRGB(cs.outlineColor);
    if (!ring) return null;
    const own = effectiveBg(el);
    const outer = el.parentElement ? effectiveBg(el.parentElement) : own;
    const offset = parseFloat(cs.outlineOffset) || 0;
    const vsOuter = contrast(ring, outer);
    const vsOwn = contrast(ring, own);
    return {
      value: offset > 0 ? vsOuter : Math.min(vsOuter, vsOwn),
      vsOuter, vsOwn, offset,
      outerHex: [outer.r, outer.g, outer.b], ringColor: cs.outlineColor
    };
  }

  // ---- which state rules in the loaded CSS target this element? -----------
  const STATE_RE = /:(hover|focus-visible|focus-within|focus|active)\\b/;

  function collectStateRules() {
    const out = [];
    for (let i = 0; i < document.styleSheets.length; i++) {
      const sheet = document.styleSheets[i];
      let rules;
      try { rules = sheet.cssRules; } catch (e) { out.push({ inaccessible: true, href: sheet.href }); continue; }
      const walk = (list, cond) => {
        for (const r of list) {
          if (r.type === CSSRule.STYLE_RULE) {
            if (!STATE_RE.test(r.selectorText || '')) continue;
            const decls = {};
            for (let j = 0; j < r.style.length; j++) {
              const p = r.style[j];
              decls[p] = { value: r.style.getPropertyValue(p), important: r.style.getPropertyPriority(p) === 'important' };
            }
            out.push({
              sheet: sheet.href ? sheet.href.split('/').pop() : ('inline#' + (sheet.ownerNode && sheet.ownerNode.id || i)),
              selector: r.selectorText,
              condition: cond,
              conditionApplies: cond ? matchMedia(cond).matches : true,
              decls
            });
          } else if (r.cssRules) {
            walk(r.cssRules, r.conditionText || cond);
          }
        }
      };
      walk(rules, null);
    }
    return out;
  }

  /**
   * Split a selector list on TOP-LEVEL commas only. Naive String.split(',')
   * shreds ":where(a, button, input):focus-visible" into invalid fragments --
   * which silently reports the theme's own global focus-ring rule as matching
   * nothing. Same for spaces when finding the subject compound.
   */
  function splitTop(sel, sep) {
    const out = [];
    let depth = 0, cur = '';
    for (let i = 0; i < sel.length; i++) {
      const c = sel[i];
      if (c === '(' || c === '[') depth++;
      else if (c === ')' || c === ']') depth--;
      if (depth === 0 && sep.test(c)) { out.push(cur); cur = ''; continue; }
      cur += c;
    }
    out.push(cur);
    return out.map(s => s.trim()).filter(Boolean);
  }

  function stripState(sel, state) {
    // "a.foo:hover .bar" -> { test: "a.foo .bar", subject: 'ancestor' }
    const res = [];
    for (const part of splitTop(sel, /,/)) {
      if (!part.includes(':' + state)) continue;
      const stripped = part.replace(new RegExp(':' + state + '\\\\b', 'g'), '');
      // ":not(:hover)" collapses to ":not()", which is invalid -- skip those.
      if (/\\(\\s*\\)/.test(stripped)) continue;
      // subject = self when the state pseudo sits on the LAST compound
      const compounds = splitTop(part.replace(/\\s*([>+~])\\s*/g, ' '), /\\s/);
      const last = compounds[compounds.length - 1] || '';
      res.push({
        test: stripped.trim() || '*',
        subject: last.includes(':' + state) ? 'self' : 'ancestor',
        raw: part
      });
    }
    return res;
  }

  window.__probe = {
    VISUAL_PROPS, INTERACTIVE_SEL, CONTAINER_SEL, SUBTREE_PROPS,
    themeClasses, signature, category, domPath, snapshot, diff, affordanceProps,
    subtreeFingerprint, subtreeDelta, resolveDeclared, splitTop,
    parseRGB, contrast, effectiveBg, ringContrast, collectStateRules, stripState, STATE_RE
  };
})();
`;

// --------------------------------------------------------------------------
// Per-route probe
// --------------------------------------------------------------------------

async function probeRoute(ctx, page, cdp, route, url, opts) {
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(1200); // let inline styles + any local JS settle

  // CRITICAL: the theme transitions colour (0.15s) and transform. Reading
  // getComputedStyle immediately after forcing :hover returns the START of the
  // transition, i.e. the rest value -- which silently scores every transitioned
  // hover as "no hover state". Freeze all timing so computed values snap.
  // Verified: without this, .aurora-primary-nav a:hover reads as unchanged;
  // with it (or after a 700ms settle) it reads rgb(181,60,24).
  await page.addStyleTag({
    content:
      '*, *::before, *::after { transition-duration: 0s !important; transition-delay: 0s !important; ' +
      'animation-duration: 0.001s !important; animation-delay: 0s !important; }',
  });
  await page.addScriptTag({ content: PAGE_LIB });
  await page.waitForTimeout(120);

  // 1. Inventory + rest snapshots + which state rules match each element.
  const inventory = await page.evaluate(() => {
    const P = window.__probe;
    const stateRules = P.collectStateRules();
    const accessible = stateRules.filter((r) => !r.inaccessible);
    const inaccessible = stateRules.filter((r) => r.inaccessible);

    const seen = new Set();
    const els = [];
    const push = (el) => {
      if (seen.has(el)) return;
      seen.add(el);
      els.push(el);
    };
    document.querySelectorAll(P.INTERACTIVE_SEL).forEach(push);
    document.querySelectorAll(P.CONTAINER_SEL).forEach((el) => {
      if (el.matches(P.INTERACTIVE_SEL)) return; // already counted
      // A wrapper whose whole class list is WordPress-generated (post-1234,
      // type-post, tag-ai, …) is a template artefact, not a designed card.
      if (P.themeClasses(el).length === 0) return;
      if (el.querySelector(P.INTERACTIVE_SEL)) push(el);
    });

    const items = [];
    els.forEach((el, i) => {
      el.setAttribute('data-probe-id', String(i));
      const cs = getComputedStyle(el);
      const box = el.getBoundingClientRect();
      const rendered =
        cs.display !== 'none' && cs.visibility !== 'hidden' && (box.width > 0 || box.height > 0);

      // Which authored state rules target this element?
      const restCS = getComputedStyle(el);
      const matched = { hover: [], 'focus-visible': [], focus: [], 'focus-within': [], active: [] };
      for (const r of accessible) {
        for (const state of Object.keys(matched)) {
          if (!new RegExp(':' + state + '\\b').test(r.selector)) continue;
          for (const cand of P.stripState(r.selector, state)) {
            // A rule targeting the element's ::before/::after still styles the
            // element visually, so match on the element and remember the fact.
            const peMatch = cand.test.match(/::[a-zA-Z-]+/);
            const testSel = cand.test.replace(/::[a-zA-Z-]+(\\([^)]*\\))?/g, '').trim();
            let ok = false;
            try {
              ok = testSel ? el.matches(testSel) : false;
            } catch (e) {
              ok = false;
            }
            if (!ok) continue;
            // For self-subject rules, work out whether each declaration would
            // actually change anything if it won.
            // Skip for pseudo-element rules: the declaration applies to the
            // generated box, so testing it on the element proves nothing.
            const declared = {};
            if (cand.subject === 'self' && !peMatch) {
              for (const [p, d] of Object.entries(r.decls)) {
                const resolved = P.resolveDeclared(el, p, d.value);
                declared[p] = {
                  value: d.value,
                  important: d.important,
                  resolved,
                  wouldChange: resolved !== null && resolved !== restCS.getPropertyValue(p),
                };
              }
            }
            matched[state].push({
              sheet: r.sheet,
              selector: cand.raw,
              subject: cand.subject,
              condition: r.condition,
              conditionApplies: r.conditionApplies,
              props: Object.keys(r.decls),
              important: Object.values(r.decls).some((d) => d.important),
              declared,
              pseudoElement: peMatch ? peMatch[0] : null,
              wouldChange: Object.values(declared).some((d) => d.wouldChange),
            });
          }
        }
      }

      items.push({
        idx: i,
        tag: el.tagName.toLowerCase(),
        category: P.category(el),
        signature: P.signature(el),
        classes: P.themeClasses(el),
        path: P.domPath(el),
        text: (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 60),
        href: el.getAttribute('href') || null,
        type: el.getAttribute('type') || null,
        rendered,
        inHeader: !!el.closest('header, .wp-block-template-part'),
        inFooter: !!el.closest('footer'),
        tabbable: el.tabIndex >= 0,
        rest: P.snapshot(el),
        restSubtree: P.subtreeFingerprint(el, 40),
        bg: P.effectiveBg(el),
        matched,
      });
    });

    // Second pass: which probed elements are ancestors of which? A card's hover
    // state covers everything inside it, so an inner title with no hover rule of
    // its own is NOT a gap.
    els.forEach((el, i) => {
      const anc = [];
      let n = el.parentElement;
      while (n) {
        const id = n.getAttribute && n.getAttribute('data-probe-id');
        if (id !== null && id !== undefined) anc.push(Number(id));
        n = n.parentElement;
      }
      items[i].ancestorIds = anc;
    });

    // Exact dead-state-rule coverage: how many elements on THIS route does each
    // authored state rule actually match? A ":hover" rule that matches nothing
    // is not interaction coverage, and must not be inventoried as such.
    const ruleCoverage = accessible.map((r) => {
      let matches = 0;
      const states = [];
      for (const state of ['hover', 'focus-visible', 'focus-within', 'focus', 'active']) {
        if (!new RegExp(':' + state + '\\b').test(r.selector)) continue;
        states.push(state);
        for (const cand of P.stripState(r.selector, state)) {
          // querySelectorAll cannot select a pseudo-element; strip it so that
          // ".x:hover::after" is counted against ".x", not reported as dead.
          const test = cand.test.replace(/::[a-zA-Z-]+(\\([^)]*\\))?/g, '').trim();
          if (!test) continue; // e.g. "::-webkit-scrollbar-thumb:hover"
          try {
            matches += document.querySelectorAll(test).length;
          } catch (e) {
            /* unsupported selector */
          }
        }
      }
      return {
        sheet: r.sheet,
        selector: r.selector,
        states,
        condition: r.condition,
        conditionApplies: r.conditionApplies,
        matches,
        props: Object.keys(r.decls),
        important: Object.values(r.decls).some((d) => d.important),
      };
    });

    return {
      items,
      ruleCoverage,
      stateRuleCount: accessible.length,
      inaccessibleSheets: inaccessible.map((r) => r.href),
      sheetCount: document.styleSheets.length,
    };
  });

  // 2. Force :hover then :focus-visible per element via CDP, exactly as
  //    DevTools' ":hov" panel does. Geometry independent.
  const { root } = await cdp.send('DOM.getDocument', { depth: -1 });
  const results = [];
  for (const item of inventory.items) {
    let nodeId = 0;
    try {
      ({ nodeId } = await cdp.send('DOM.querySelector', {
        nodeId: root.nodeId,
        selector: `[data-probe-id="${item.idx}"]`,
      }));
    } catch (e) {
      nodeId = 0;
    }
    const out = {
      ...item,
      hoverState: null,
      focusState: null,
      forced: nodeId !== 0,
    };
    if (nodeId) {
      const read = (id) =>
        page.evaluate((i) => {
          const P = window.__probe;
          const el = document.querySelector(`[data-probe-id="${i}"]`);
          const cs = getComputedStyle(el);
          return {
            style: P.snapshot(el),
            subtree: P.subtreeFingerprint(el, 40),
            ringContrast: P.ringContrast(el),
          };
        }, id);

      await cdp.send('CSS.forcePseudoState', { nodeId, forcedPseudoClasses: ['hover'] });
      await page.evaluate(() => new Promise((r) => requestAnimationFrame(() => r())));
      out.hoverState = await read(item.idx);
      await cdp.send('CSS.forcePseudoState', {
        nodeId,
        forcedPseudoClasses: ['focus', 'focus-visible'],
      });
      await page.evaluate(() => new Promise((r) => requestAnimationFrame(() => r())));
      out.focusState = await read(item.idx);
      await cdp.send('CSS.forcePseudoState', { nodeId, forcedPseudoClasses: [] });
    }
    results.push(out);
  }

  // 3. Genuine keyboard tab-through.
  const tabStops = await (async () => {
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.evaluate(() => document.body.focus());
    const stops = [];
    const seenIdx = new Set();
    for (let i = 0; i < opts.maxTabs; i++) {
      await page.keyboard.press('Tab');
      await page.evaluate(() => new Promise((r) => requestAnimationFrame(() => r())));
      const stop = await page.evaluate(() => {
        const a = document.activeElement;
        if (!a || a === document.body || a === document.documentElement) return null;
        const P = window.__probe;
        const cs = getComputedStyle(a);
        const ring = {
          outlineStyle: cs.outlineStyle,
          outlineWidth: cs.outlineWidth,
          outlineColor: cs.outlineColor,
          outlineOffset: cs.outlineOffset,
          boxShadow: cs.boxShadow,
        };
        const box = a.getBoundingClientRect();
        return {
          probeId: a.getAttribute('data-probe-id'),
          tag: a.tagName.toLowerCase(),
          signature: P.signature(a),
          text: (a.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40),
          focusVisible: a.matches(':focus-visible'),
          ring,
          ringContrast: P.ringContrast(a),
          uaDefaultRing: cs.outlineStyle === 'auto',
          offscreen: box.width === 0 && box.height === 0,
          hidden: cs.visibility === 'hidden' || cs.display === 'none',
        };
      });
      if (!stop) break;
      const key = stop.probeId !== null ? 'p' + stop.probeId : stop.signature + '|' + stop.text;
      if (seenIdx.has(key) && stops.length > 3) break; // wrapped around
      seenIdx.add(key);
      stops.push({ order: stops.length + 1, ...stop });
    }
    return stops;
  })();

  return { route, url, ...inventory, items: results, tabStops };
}

// --------------------------------------------------------------------------
// Classification (runs in node, on the collected data)
// --------------------------------------------------------------------------

const NON_AFFORDANCE = new Set(['cursor', 'visibility']);

/**
 * Cause taxonomy for a missing state, which is the distinction #424's fix has
 * to act on:
 *
 *   rule-missing        no authored rule targets this element in this state
 *   rule-loses-cascade  a rule targets it and WOULD change something, but the
 *                       computed style is unchanged -> it is being outranked
 *   rule-no-op          a rule targets it but declares the value it already has
 *                       (e.g. hover colour == rest colour). Cosmetically this is
 *                       identical to having no rule, but the fix is different:
 *                       change the value, not the specificity.
 */
function classify(item) {
  const diffProps = (a, b) => {
    if (!a || !b) return [];
    return Object.keys(a).filter((k) => a[k] !== b[k] && !NON_AFFORDANCE.has(k));
  };
  const subtreeDelta = (a, b) => {
    if (!a || !b) return 0;
    let n = 0;
    for (let i = 0; i < Math.min(a.length, b.length); i++) if (a[i] !== b[i]) n++;
    return n;
  };

  const hoverStyle = item.hoverState && item.hoverState.style;
  const focusStyle = item.focusState && item.focusState.style;
  const hoverProps = diffProps(item.rest, hoverStyle);
  const focusProps = diffProps(item.rest, focusStyle);
  const hoverSubtree = subtreeDelta(item.restSubtree, item.hoverState && item.hoverState.subtree);
  const focusSubtree = subtreeDelta(item.restSubtree, item.focusState && item.focusState.subtree);

  const off = (s) => s && (s['outline-style'] === 'none' || parseFloat(s['outline-width']) === 0);
  const restOutlineOff = off(item.rest);
  const focusOutlineOff = off(focusStyle);
  const uaRing = focusStyle && focusStyle['outline-style'] === 'auto';

  // Did anything other than the outline change on focus? (an equal-or-better
  // replacement, per WCAG 2.4.7 / the issue's explicit criterion)
  const focusReplacement = focusProps.filter((p) => !p.startsWith('outline'));

  let focusVerdict;
  if (!focusStyle) focusVerdict = 'unmeasured';
  else if (focusOutlineOff && focusReplacement.length === 0 && focusSubtree === 0)
    focusVerdict = 'none';
  else if (focusOutlineOff) focusVerdict = 'replacement-only';
  else if (uaRing) focusVerdict = 'ua-default-ring';
  else focusVerdict = 'theme-ring';

  let hoverVerdict;
  if (!hoverStyle) hoverVerdict = 'unmeasured';
  else if (hoverProps.length) hoverVerdict = 'yes';
  else if (hoverSubtree > 0) hoverVerdict = 'yes-descendant';
  else hoverVerdict = 'no';

  const applicable = (list) =>
    (list || []).filter((r) => r.subject === 'self' && r.conditionApplies !== false);
  const hoverRules = applicable(item.matched && item.matched.hover);
  const fvRules = applicable(item.matched && item.matched['focus-visible']).concat(
    applicable(item.matched && item.matched.focus)
  );

  const cause = (verdictMissing, rules) => {
    if (!verdictMissing) return null;
    if (!rules.length) return 'rule-missing';
    // A pseudo-element rule's declared value cannot be resolved on the element,
    // so it counts as "would change" for cause purposes — the measurement of
    // ::before/::after computed style already proved nothing actually changed.
    return rules.some((r) => r.wouldChange || r.pseudoElement)
      ? 'rule-loses-cascade'
      : 'rule-no-op';
  };

  return {
    hoverVerdict,
    hoverProps,
    hoverSubtree,
    hoverCause: cause(hoverVerdict === 'no', hoverRules),
    hoverRuleCount: hoverRules.length,
    focusVerdict,
    focusProps,
    focusSubtree,
    focusCause: cause(focusVerdict === 'none', fvRules),
    focusRuleCount: fvRules.length,
    focusRing:
      focusStyle && !focusOutlineOff
        ? `${focusStyle['outline-width']} ${focusStyle['outline-style']} ${focusStyle['outline-color']} @${focusStyle['outline-offset']}`
        : null,
    focusRingContrast:
      item.focusState && item.focusState.ringContrast
        ? item.focusState.ringContrast.value
        : null,
    focusRingContrastDetail: item.focusState ? item.focusState.ringContrast : null,
    restOutlineOff,
    focusOutlineOff,
    uaRing,
  };
}

/**
 * Second pass: an element with no hover state of its own is not a gap if a
 * probed ANCESTOR has one — hovering the card lights the card, and the title
 * inside it is part of that affordance. Same for focus-within.
 */
function applyAncestorCoverage(items) {
  const byIdx = new Map(items.map((i) => [i.idx, i]));
  for (const i of items) {
    if (i.verdict.hoverVerdict !== 'no') continue;
    const provider = (i.ancestorIds || [])
      .map((id) => byIdx.get(id))
      .find((a) => a && (a.verdict.hoverVerdict === 'yes' || a.verdict.hoverVerdict === 'yes-descendant'));
    if (provider) {
      i.verdict.hoverVerdict = 'covered-by-ancestor';
      i.verdict.hoverCoveredBy = provider.signature;
      i.verdict.hoverCause = null;
    }
  }
  return items;
}

// --------------------------------------------------------------------------
// Reporting
// --------------------------------------------------------------------------

function summarise(data) {
  const L = [];
  L.push('# Interaction state probe — measured results');
  L.push('');
  L.push(`Captured: ${data.capturedAt}  ·  base: ${data.base}`);
  L.push('');
  L.push('| Route | Interactive (rendered) | hover: no | focus: none | focus: UA ring only | tab stops | stops w/o visible focus |');
  L.push('|---|---:|---:|---:|---:|---:|---:|');
  for (const r of data.routes) {
    const rendered = r.items.filter((i) => i.rendered);
    const noHover = rendered.filter((i) => i.verdict.hoverVerdict === 'no').length;
    const noFocus = rendered.filter((i) => i.verdict.focusVerdict === 'none').length;
    const ua = rendered.filter((i) => i.verdict.focusVerdict === 'ua-default-ring').length;
    const badStops = r.tabStops.filter(
      (s) => s.ring.outlineStyle === 'none' && (!s.ring.boxShadow || s.ring.boxShadow === 'none')
    ).length;
    L.push(
      `| \`${r.route}\` | ${rendered.length} | ${noHover} | ${noFocus} | ${ua} | ${r.tabStops.length} | ${badStops} |`
    );
  }
  L.push('');
  for (const r of data.routes) {
    L.push(`## \`${r.route}\``);
    L.push('');
    L.push('| # | Element | Category | hover | focus | cause | focus ring |');
    L.push('|---:|---|---|---|---|---|---|');
    const rendered = r.items.filter((i) => i.rendered);
    const bySig = new Map();
    for (const i of rendered) {
      if (!bySig.has(i.signature)) bySig.set(i.signature, []);
      bySig.get(i.signature).push(i);
    }
    let n = 0;
    for (const [sig, group] of bySig) {
      const i = group[0];
      const v = i.verdict;
      L.push(
        `| ${++n} | \`${sig}\` ×${group.length} | ${i.category} | ${v.hoverVerdict} | ${v.focusVerdict} | ${
          v.focusCause || v.hoverCause || ''
        } | ${v.focusRing || '—'}${v.focusRingContrast ? ' (' + v.focusRingContrast + ':1)' : ''} |`
      );
    }
    L.push('');
  }
  return L.join('\n');
}

// --------------------------------------------------------------------------
// main
// --------------------------------------------------------------------------

async function main() {
  const opts = parseArgs(process.argv);
  assertBrowsersPath();
  const { chromium } = loadPlaywright();

  fs.mkdirSync(opts.out, { recursive: true });
  const mdir = path.join(opts.out, 'mirror');
  if (!opts.skipMirror) {
    mirror(opts);
  } else if (!fs.existsSync(mdir)) {
    console.error(`FATAL: --skip-mirror given but ${mdir} does not exist`);
    process.exit(2);
  }

  const srv = await serve(mdir, opts.port);
  const browser = await chromium.launch({ args: ['--no-sandbox'] });
  // Default to no-preference: that is what most visitors get, and the theme's
  // prefers-reduced-motion block explicitly cancels transform-based hover
  // affordances (style.css:4380 `.aurora-media-card:hover img { transform: none }`
  // and 14 siblings). Auditing under `reduce` would score those as missing
  // hover for everyone, which is wrong. Use --reduced-motion to measure the
  // reduced-motion experience deliberately.
  const ctx = await browser.newContext({
    viewport: opts.viewport,
    reducedMotion: opts.reducedMotion ? 'reduce' : 'no-preference',
    colorScheme: 'light',
  });
  // Satisfy image/font requests locally so layout is not distorted by broken
  // images; everything else 404s from the mirror, which is fine.
  await ctx.route('**/*', (r) => {
    const t = r.request().resourceType();
    if (t === 'image') return r.fulfill({ status: 200, contentType: 'image/png', body: PIXEL });
    if (t === 'font' || t === 'media') return r.abort();
    return r.continue();
  });

  const page = await ctx.newPage();
  const cdp = await ctx.newCDPSession(page);
  await cdp.send('DOM.enable');
  await cdp.send('CSS.enable');

  const routes = [];
  for (const route of opts.routes) {
    const slug = routeSlug(route);
    process.stderr.write(`probing ${route}\n`);
    const r = await probeRoute(
      ctx,
      page,
      cdp,
      route,
      `http://127.0.0.1:${opts.port}/${slug}.html`,
      opts
    );
    r.items.forEach((i) => {
      i.verdict = classify(i);
    });
    applyAncestorCoverage(r.items);
    routes.push(r);
    process.stderr.write(
      `  ${r.items.filter((i) => i.rendered).length} rendered interactive elements, ` +
        `${r.tabStops.length} tab stops\n`
    );
  }

  await browser.close();
  srv.close();

  const data = {
    capturedAt: new Date().toISOString(),
    base: opts.base,
    viewport: opts.viewport,
    routes,
  };
  fs.writeFileSync(path.join(opts.out, 'probe.json'), JSON.stringify(data, null, 2));
  if (!opts.jsonOnly) fs.writeFileSync(path.join(opts.out, 'summary.md'), summarise(data) + '\n');
  process.stderr.write(`wrote ${path.join(opts.out, 'probe.json')}\n`);
}

if (require.main === module) {
  main().catch((e) => {
    console.error('FATAL:', e && e.stack ? e.stack : e);
    process.exit(1);
  });
}

module.exports = { classify, applyAncestorCoverage, routeSlug, PAGE_LIB };
