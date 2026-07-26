#!/usr/bin/env python3
"""visual_baseline.py — visual-regression baseline harness for kriskrug.co (issue #473).

Implements step 1 / §4 of docs/current-state/AURORA-STYLESHEET-REBUILD-PLAN.md.
This is the gate for the Aurora stylesheet rebuild (#423): no rebuild step may
land unless a `make visual-diff` run against it is green.

WHAT IT DOES
------------
Captures full-page screenshots of 11 logged-out routes at 3 viewports
(375 / 768 / 1440), with reduced-motion and light color-scheme forced and a
scroll-settle pass, masking the known non-deterministic regions (marquee board,
live dates, Beehiiv embed). It then records a hash manifest — never the pixels —
plus the live-vs-repo md5 identity of every theme CSS file and the Jetpack Boost
bundle hash for the same run.

    make visual-baseline            # freeze a baseline, write manifest-<ts>.json
    make visual-diff BASE=<ts>      # capture a candidate, compare, pass/warn/fail
    make visual-diff-report         # markdown table for the PR body

HOW IT TALKS TO THE SITE
------------------------
Chromium in this sandbox cannot reach kriskrug.co directly — the agent HTTPS
proxy resets browser connections (ERR_CONNECTION_RESET) while curl gets 200.
So every request the browser makes is intercepted by Playwright and fulfilled
from a curl fetch, keyed by URL and cached on disk for the run. The page's own
origin is preserved (we navigate to the real https://kriskrug.co/<route> and
fulfil it), so no URL rewriting is needed and same-origin CSS stays readable.
This is the same constraint scripts/interaction_state_probe.js works around; the
mechanism here is request interception rather than a rewritten local mirror.

Hosts outside the allowlist (kriskrug.co, the Pagely CDN, the Jetpack image CDN)
are fulfilled with an empty 200 rather than fetched. That is deliberate: GTM,
social embeds and third-party widgets are the largest source of run-to-run
nondeterminism, and their layout boxes are declared in markup/CSS, not by the
response body.

WHY THE DIFF RUNS IN CHROMIUM
-----------------------------
Neither `pixelmatch`/`pngjs` (node) nor `Pillow`/`numpy` (python) are installed
here, and a pure-Python PNG decode of a 2880x20000 full-page capture is far too
slow to be a usable gate. Chromium is already a hard dependency and decodes PNG
natively, so the comparison is done in-page over typed arrays using pixelmatch's
YIQ delta at threshold 0.2, strip by strip to bound canvas memory.

STORAGE — issue #318
--------------------
PNGs are NEVER committed. `docs/current-state/reports/visual-baseline/*` is
git-ignored wholesale; only `manifest-*.json`, `diff-*.json` and `report-*.md`
at its top level are un-ignored by name. `visual_baseline.py guard` re-checks
that invariant against the git index after every capture and diff, and the make
targets fail if it trips. See `--help` of the `guard` subcommand.

CHROMIUM
--------
Chromium is preinstalled at /opt/pw-browsers. This script REFUSES to download a
browser: if PLAYWRIGHT_BROWSERS_PATH is unset, missing, or Chromium is not
present under it, preflight exits 2 with a FATAL message. Every node child is
spawned with PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 so even a bug cannot fetch one.

Read-only with respect to WordPress: it issues GETs and nothing else.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "docs" / "current-state" / "reports" / "visual-baseline"
ARTIFACT_ROOT_REL = "docs/current-state/reports/visual-baseline"

BASE_URL = "https://kriskrug.co"

# Hosts whose responses are really fetched. Everything else is fulfilled with an
# empty 200 so third-party widgets cannot make the baseline nondeterministic.
ALLOW_HOSTS = ("kriskrug.co", "s5102.pcdn.co", "i0.wp.com", "i1.wp.com", "i2.wp.com")

# --------------------------------------------------------------------------
# Routes — §4.2. Eleven logged-out routes, chosen to cover distinct templates.
#
# `expect_status` is asserted by preflight before any capture runs: a route that
# starts redirecting or 404ing must break the run loudly, not be captured as a
# silently different page. That is the difference between a gate and theatre.
# --------------------------------------------------------------------------
ROUTES: tuple[dict[str, Any], ...] = (
    {"id": "home", "path": "/", "template": "front-page.html", "expect_status": 200},
    {"id": "about", "path": "/about/", "template": "page.html", "expect_status": 200},
    {
        "id": "services",
        "path": "/generative-ai-services/",
        "template": "page.html",
        "expect_status": 200,
        # §4.2 lists /services/; live 301s it to /generative-ai-services/.
        # Captured at the canonical target so the capture is of a page, not of a
        # redirect. Verified 2026-07-25.
        "note": "canonical target of /services/ (301)",
    },
    {"id": "speaking", "path": "/speaking/", "template": "page.html", "expect_status": 200},
    {"id": "work", "path": "/work/", "template": "page.html", "expect_status": 200},
    {"id": "photography", "path": "/photography/", "template": "page.html", "expect_status": 200},
    {"id": "blog", "path": "/blog/", "template": "index.html", "expect_status": 200},
    {"id": "contact", "path": "/contact/", "template": "page.html", "expect_status": 200},
    {
        "id": "single-post",
        "path": "/2026/07/18/i-am-nomad-ai-film/",
        "template": "single.html",
        "expect_status": 200,
    },
    {
        "id": "not-found",
        "path": "/definitely-not-a-page-404-probe/",
        "template": "404.html",
        "expect_status": 404,
    },
    {
        "id": "category-archive",
        "path": "/category/vancouver-ai-ecosystem/",
        "template": "archive.html",
        "expect_status": 200,
        # §4.2 asks for a marquee board post here (the theme's only inline
        # <style>). kk-marquee-board is repo-side only: /marquee/ returns 404 on
        # live as of 2026-07-25, so there is no board post to capture. The
        # category archive is substituted because archive.html is otherwise
        # uncovered by the other ten. See MARQUEE_ROUTE below — flip it on and
        # drop this one once the plugin is deployed.
        "note": "stands in for the marquee board post; /marquee/ is 404 on live",
    },
)

# Not captured today. Kept here so the substitution above is explicit and
# reversible rather than a silently missing route.
MARQUEE_ROUTE = {
    "id": "marquee-board",
    "path": "/marquee/",
    "template": "single-marquee_board.html",
    "expect_status": 200,
    "enabled": False,
    "note": "kk-marquee-board is not deployed to live; /marquee/ 404s (checked 2026-07-25)",
}

VIEWPORTS: tuple[dict[str, Any], ...] = (
    {"name": "mobile", "width": 375, "height": 812},
    {"name": "tablet", "width": 768, "height": 1024},
    {"name": "desktop", "width": 1440, "height": 900},
)

DEFAULT_DEVICE_SCALE = 2  # §4.3

# --------------------------------------------------------------------------
# Masks — §4.3: "declared in the manifest, not hardcoded". They live here as the
# default declaration, are written into every manifest, and can be overridden
# per run with --masks <file.json>. A selector that matches nothing is not an
# error; the per-capture match counts are recorded so a mask silently ceasing to
# match (a class rename) is visible in the manifest instead of surfacing as a
# mystery diff.
# --------------------------------------------------------------------------
DEFAULT_MASKS: dict[str, list[str]] = {
    "marquee": [
        ".aurora-woven-marquee",
        ".aurora-woven-marquee-track",
        ".kkm",
        ".kkm-board",
        "[class*='marquee']",
    ],
    "dates": [
        "time",
        ".wp-block-post-date",
        ".aurora-article-date",
        ".aurora-masthead-date",
        "[class*='now-showing']",
        "[class*='entry-date']",
        "[class*='posted-on']",
    ],
    "beehiiv": [
        "iframe[src*='beehiiv']",
        "[class*='beehiiv']",
        "[id*='beehiiv']",
        "[data-beehiiv]",
    ],
}
MASK_COLOR = "#FF00FF"

# --------------------------------------------------------------------------
# Reveal end-states.
#
# Aurora gates several components behind JS-added classes and starts them at
# `opacity: 0` (style.css: `.aurora-fade-up`, `.aurora-scale-in`,
# `.is-aurora-lux-reveal`; animations.css: `.aurora-hero-text .word`). A
# full-page screenshot renders content that was never scrolled into view, so
# whether an IntersectionObserver fired is a race — and an element that lost the
# race is captured invisible. Measured on /blog/: reveal-gated cards rendered at
# partial opacity, which is both wrong (no visitor sees that) and unstable.
#
# So after the scroll pass we add the theme's OWN "revealed" class rather than
# overriding opacity/transform in CSS. Driving the theme's end state through its
# own selectors means a real regression in those rules still shows up in the
# pixels; a blanket `opacity: 1 !important` would hide it.
#
# Declared here, written into the manifest, and the per-run match counts are
# recorded — so a class rename surfaces as a count of 0 rather than as a diff
# nobody can explain.
# --------------------------------------------------------------------------
DEFAULT_REVEALS: list[dict[str, str]] = [
    {"selector": ".is-aurora-lux-reveal", "add_class": "is-revealed"},
    {"selector": ".aurora-fade-up", "add_class": "is-visible"},
    {"selector": ".aurora-scale-in", "add_class": "is-visible"},
    {"selector": ".aurora-hero-text", "add_class": "is-visible"},
]

# --------------------------------------------------------------------------
# Tolerance — §4.4
# --------------------------------------------------------------------------
TOLERANCE = {
    "pixel_threshold": 0.2,  # per-pixel YIQ antialias tolerance (pixelmatch default)
    "pass_pct": 0.1,  # <= this share of differing pixels -> pass
    "warn_pct": 1.0,  # <= this -> warn (human review); above -> fail
    "height_delta_pct": 2.0,  # any full-page height change beyond this -> fail
}

# Theme CSS files whose live-vs-repo md5 identity is recorded per run (§4.5/§1.6).
# Includes Aurora 1.5.0 scaffold sheets (#474): 02-tokens.css + 09-late.css.
THEME_CSS_FILES = (
    "style.css",
    "assets/css/02-tokens.css",
    "assets/css/animations.css",
    "assets/css/bleeding-edge.css",
    "assets/css/editor.css",
    "assets/css/09-late.css",
    "assets/css/revive-port.css",
    "assets/css/typography-refined.css",
)
THEME_LIVE_BASE = "/wp-content/themes/kk-aurora/"
THEME_REPO_DIR = REPO_ROOT / "theme" / "kk-aurora"

SETTLE_MS = 900
IMAGE_BUDGET_MS = 25_000  # per-image ceiling in the force-load pass
NAV_TIMEOUT_MS = 90_000

MANIFEST_SCHEMA = "kk-visual-baseline/1"


# ==========================================================================
# small helpers
# ==========================================================================


def fatal(msg: str, code: int = 2) -> None:
    print(f"FATAL: {msg}", file=sys.stderr)
    sys.exit(code)


def info(msg: str) -> None:
    print(msg, file=sys.stderr)


def run_id_now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def png_dimensions(path: Path) -> tuple[int, int]:
    """Width/height from the IHDR chunk. Avoids decoding the image."""
    with path.open("rb") as fh:
        head = fh.read(24)
    if len(head) < 24 or head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"not a PNG: {path}")
    width = int.from_bytes(head[16:20], "big")
    height = int.from_bytes(head[20:24], "big")
    return width, height


def curl_bytes(url: str, timeout: int = 60) -> tuple[int, bytes]:
    """GET a URL with curl. Returns (http_status, body). Never raises on 4xx/5xx."""
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        dest = Path(tf.name)
    try:
        proc = subprocess.run(
            [
                "curl", "-sS", "-L",
                "--max-time", str(timeout),
                "-H", "Cache-Control: no-cache",
                "-H", "Pragma: no-cache",
                "-o", str(dest),
                "-w", "%{http_code}",
                url,
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"curl failed for {url}: {proc.stderr.strip()}")
        status = int((proc.stdout or "0").strip() or 0)
        return status, dest.read_bytes()
    finally:
        dest.unlink(missing_ok=True)


def curl_status(url: str, timeout: int = 45) -> int:
    proc = subprocess.run(
        ["curl", "-sS", "-o", os.devnull, "-w", "%{http_code}", "--max-time", str(timeout), url],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"curl failed for {url}: {proc.stderr.strip()}")
    return int((proc.stdout or "0").strip() or 0)


def git(*args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args], capture_output=True, text=True, check=False
    )
    return proc.stdout


# ==========================================================================
# preflight — Chromium, node, playwright, routes
# ==========================================================================

NODE_CANDIDATES = ("node", "/opt/node22/bin/node")
NODE_PATH_CANDIDATES = (
    "/opt/node22/lib/node_modules",
    "/usr/lib/node_modules",
    "/usr/local/lib/node_modules",
)


def resolve_node() -> str:
    for cand in NODE_CANDIDATES:
        exe = shutil.which(cand) if "/" not in cand else (cand if Path(cand).exists() else None)
        if exe:
            return exe
    fatal(
        "node was not found. Tried: " + ", ".join(NODE_CANDIDATES) + "\n"
        "The capture driver is a Node/Playwright program; there is no pure-Python fallback."
    )
    raise AssertionError  # unreachable


def node_env() -> dict[str, str]:
    env = dict(os.environ)
    env["NODE_PATH"] = os.pathsep.join(
        [p for p in NODE_PATH_CANDIDATES if Path(p).is_dir()] + [env.get("NODE_PATH", "")]
    ).strip(os.pathsep)
    # Belt and braces: even a bug in the driver cannot pull a browser down.
    env["PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD"] = "1"
    env["PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS"] = "1"
    return env


def preflight_browser() -> dict[str, str]:
    """Assert Chromium is present and usable. Exits 2 loudly; never downloads."""
    bpath = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    if not bpath:
        fatal(
            "PLAYWRIGHT_BROWSERS_PATH is unset.\n"
            "  Chromium is preinstalled at /opt/pw-browsers. Re-run as:\n"
            "    PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers make visual-baseline\n"
            "  Refusing to run `playwright install` or trigger any browser download\n"
            "  (AURORA-STYLESHEET-REBUILD-PLAN.md §4.1/§4.6)."
        )
    if not Path(bpath).is_dir():
        fatal(
            f"PLAYWRIGHT_BROWSERS_PATH={bpath} does not exist or is not a directory.\n"
            "  Refusing to download a browser. Point it at an existing Playwright\n"
            "  browsers directory (here: /opt/pw-browsers)."
        )
    chromium_dirs = sorted(p.name for p in Path(bpath).glob("chromium*") if p.is_dir())
    if not chromium_dirs:
        fatal(
            f"no chromium* directory under PLAYWRIGHT_BROWSERS_PATH={bpath}.\n"
            f"  Found: {sorted(p.name for p in Path(bpath).iterdir()) if Path(bpath).is_dir() else '[]'}\n"
            "  Refusing to download a browser."
        )

    node = resolve_node()
    probe = (
        "const pw=require('playwright');"
        "const fs=require('fs');"
        "let exec=null,err=null;"
        "try{exec=pw.chromium.executablePath();}catch(e){err=String(e&&e.message||e);}"
        "process.stdout.write(JSON.stringify({"
        "version:require('playwright/package.json').version,"
        "exec:exec,execExists:exec?fs.existsSync(exec):false,err:err,node:process.version}));"
    )
    proc = subprocess.run(
        [node, "-e", probe], capture_output=True, text=True, env=node_env(), check=False
    )
    if proc.returncode != 0:
        fatal(
            "the `playwright` node package is not resolvable.\n"
            f"  node: {node}\n"
            f"  NODE_PATH: {node_env().get('NODE_PATH')}\n"
            f"  stderr: {proc.stderr.strip()[:500]}\n"
            "  Install it globally (npm i -g playwright) or set NODE_PATH.\n"
            "  Do NOT run `playwright install` — the browser is already at /opt/pw-browsers."
        )
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        fatal(f"could not parse playwright probe output: {proc.stdout[:300]!r}")
        raise AssertionError  # unreachable
    if not data.get("exec") or not data.get("execExists"):
        fatal(
            "Chromium executable is missing.\n"
            f"  playwright {data.get('version')} resolved executablePath to: {data.get('exec')}\n"
            f"  PLAYWRIGHT_BROWSERS_PATH={bpath} contains: {chromium_dirs}\n"
            f"  probe error: {data.get('err')}\n"
            "  Refusing to download it. Fix the install out of band."
        )
    return {
        "node": node,
        "node_version": data.get("node", ""),
        "playwright": data.get("version", ""),
        "chromium_exec": data.get("exec", ""),
        "browsers_path": bpath,
    }


def enabled_routes(only: list[str] | None) -> list[dict[str, Any]]:
    routes = [dict(r) for r in ROUTES if r.get("enabled", True)]
    if only:
        wanted = set(only)
        unknown = wanted - {r["id"] for r in routes} - {r["path"] for r in routes}
        if unknown:
            fatal(f"unknown route selector(s): {sorted(unknown)}")
        routes = [r for r in routes if r["id"] in wanted or r["path"] in wanted]
    return routes


def selected_viewports(only: list[str] | None, scale: int) -> list[dict[str, Any]]:
    vps = [dict(v, scale=scale) for v in VIEWPORTS]
    if only:
        wanted = set(only)
        unknown = wanted - {v["name"] for v in vps}
        if unknown:
            fatal(f"unknown viewport(s): {sorted(unknown)}")
        vps = [v for v in vps if v["name"] in wanted]
    return vps


def preflight_routes(base: str, routes: list[dict[str, Any]], strict: bool = True) -> list[dict]:
    """Assert every route still answers with the status the config expects."""
    out = []
    problems = []
    for r in routes:
        url = base.rstrip("/") + r["path"]
        # No -L here: a route that started redirecting is a config drift we want
        # to see, not follow.
        proc = subprocess.run(
            ["curl", "-sS", "-o", os.devnull, "-w", "%{http_code}", "--max-time", "45", url],
            capture_output=True,
            text=True,
            check=False,
        )
        status = int((proc.stdout or "0").strip() or 0)
        out.append({"id": r["id"], "path": r["path"], "status": status, "expected": r["expect_status"]})
        if status != r["expect_status"]:
            problems.append(f"  {r['id']:<18} {r['path']}  expected {r['expect_status']}, got {status}")
    if problems and strict:
        fatal(
            "route preflight failed — the route list has drifted from live:\n"
            + "\n".join(problems)
            + "\n  Fix ROUTES in scripts/visual_baseline.py (and say so in the PR) before\n"
            "  capturing. A baseline of the wrong page is worse than no baseline."
        )
    return out


# ==========================================================================
# live-vs-repo CSS identity + Boost bundle hash (§4.3 / §4.5)
# ==========================================================================


def theme_version(css_text: str) -> str | None:
    m = re.search(r"^\s*Version:\s*(.+?)\s*$", css_text, re.MULTILINE)
    return m.group(1) if m else None


def css_identity(base: str) -> dict[str, Any]:
    """md5 of each theme CSS file, live vs repo, plus both theme versions."""
    rows = []
    live_version = None
    repo_version = None
    for rel in THEME_CSS_FILES:
        url = base.rstrip("/") + THEME_LIVE_BASE + rel
        row: dict[str, Any] = {"file": rel, "live_url": url}
        try:
            status, body = curl_bytes(url)
            row["live_status"] = status
            if status == 200:
                row["live_md5"] = hashlib.md5(body).hexdigest()
                row["live_bytes"] = len(body)
                if rel == "style.css":
                    live_version = theme_version(body.decode("utf-8", "replace"))
            else:
                row["live_md5"] = None
        except Exception as exc:  # network flake must not be silent
            row["live_status"] = None
            row["live_md5"] = None
            row["error"] = str(exc)[:200]
        repo_path = THEME_REPO_DIR / rel
        if repo_path.exists():
            data = repo_path.read_bytes()
            row["repo_md5"] = hashlib.md5(data).hexdigest()
            row["repo_bytes"] = len(data)
            if rel == "style.css":
                repo_version = theme_version(data.decode("utf-8", "replace"))
        else:
            row["repo_md5"] = None
        row["identical"] = bool(row.get("live_md5")) and row.get("live_md5") == row.get("repo_md5")
        rows.append(row)
    return {
        "files": rows,
        "all_identical": all(r["identical"] for r in rows),
        "live_theme_version": live_version,
        "repo_theme_version": repo_version,
    }


BOOST_CSS_RE = re.compile(r"""["']([^"']*/boost-cache/static/([0-9a-f]+)\.min\.css)["']""")
BOOST_JS_RE = re.compile(r"""["']([^"']*/boost-cache/static/([0-9a-f]+)\.min\.js)["']""")


def boost_bundle(base: str) -> dict[str, Any]:
    """Jetpack Boost concatenated bundle hash — R-2's detection control.

    An unchanged hash after a deploy means the deploy did not reach the edge, not
    that the deploy had no visual effect. Recorded per run so the two readings
    can be compared.
    """
    out: dict[str, Any] = {"source": base.rstrip("/") + "/"}
    try:
        status, body = curl_bytes(out["source"])
        html = body.decode("utf-8", "replace")
        out["home_status"] = status
    except Exception as exc:
        out["error"] = str(exc)[:200]
        return out
    m = BOOST_CSS_RE.search(html)
    if m:
        url = m.group(1)
        out["css_bundle_url"] = url
        out["css_bundle_hash"] = m.group(2)
        try:
            st, css = curl_bytes(url if url.startswith("http") else base.rstrip("/") + url)
            if st == 200:
                out["css_bundle_md5"] = hashlib.md5(css).hexdigest()
                out["css_bundle_bytes"] = len(css)
        except Exception as exc:
            out["css_bundle_error"] = str(exc)[:200]
    else:
        out["css_bundle_url"] = None
        out["note"] = "no Jetpack Boost concatenated CSS bundle found on the homepage"
    mj = BOOST_JS_RE.search(html)
    out["js_bundle_hash"] = mj.group(2) if mj else None
    return out


# ==========================================================================
# the Node capture driver
# ==========================================================================

CAPTURE_JS = r"""
'use strict';
/* Capture driver for scripts/visual_baseline.py (issue #473).
 * Written into the run directory at runtime; never tracked by git.
 * Reads a JSON config on argv[2], writes <out>/captures.json. */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execFile } = require('child_process');
const { promisify } = require('util');
const execFileP = promisify(execFile);

function loadPlaywright() {
  for (const c of ['playwright', '/opt/node22/lib/node_modules/playwright',
                   '/usr/lib/node_modules/playwright', '/usr/local/lib/node_modules/playwright']) {
    try { return require(c); } catch (_) { /* next */ }
  }
  console.error('FATAL: playwright is not resolvable from the capture driver.');
  process.exit(2);
}

const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const CACHE = cfg.cacheDir;
fs.mkdirSync(CACHE, { recursive: true });
fs.mkdirSync(cfg.pngDir, { recursive: true });

const allow = new Set(cfg.allowHosts);
const inflight = new Map();
const stats = { fetched: 0, cached: 0, blocked: 0, failed: 0 };

function cacheKey(url) { return crypto.createHash('sha256').update(url).digest('hex').slice(0, 40); }

async function fetchThroughCurl(url) {
  const key = cacheKey(url);
  const bodyFile = path.join(CACHE, key + '.bin');
  const metaFile = path.join(CACHE, key + '.json');
  if (fs.existsSync(metaFile) && fs.existsSync(bodyFile)) {
    stats.cached++;
    return { meta: JSON.parse(fs.readFileSync(metaFile, 'utf8')), body: fs.readFileSync(bodyFile) };
  }
  if (inflight.has(key)) return inflight.get(key);
  const p = (async () => {
    const hdrFile = path.join(CACHE, key + '.hdr');
    const args = ['-sS', '-L', '--max-time', String(cfg.curlTimeout || 60),
                  '-H', 'Cache-Control: no-cache', '-H', 'Pragma: no-cache',
                  '-o', bodyFile, '-D', hdrFile, '-w', '%{http_code}', url];
    const { stdout } = await execFileP('curl', args, { maxBuffer: 1 << 24 });
    const headers = fs.readFileSync(hdrFile, 'utf8');
    const ct = headers.match(/^content-type:\s*(.+)$/im);
    const meta = { status: Number(String(stdout).trim()) || 200,
                   contentType: ct ? ct[1].trim() : 'application/octet-stream' };
    fs.writeFileSync(metaFile, JSON.stringify(meta));
    fs.rmSync(hdrFile, { force: true });
    stats.fetched++;
    return { meta, body: fs.readFileSync(bodyFile) };
  })().finally(() => inflight.delete(key));
  inflight.set(key, p);
  return p;
}

// Empty bodies for blocked hosts, typed so the browser does not warn-and-retry.
const EMPTY = {
  script: { contentType: 'application/javascript', body: '' },
  stylesheet: { contentType: 'text/css', body: '' },
  document: { contentType: 'text/html', body: '<!doctype html><html><head></head><body></body></html>' },
  image: { contentType: 'image/gif',
           body: Buffer.from('R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7', 'base64') },
  _: { contentType: 'text/plain', body: '' },
};

async function installRouting(ctx) {
  await ctx.route('**/*', async (route) => {
    const req = route.request();
    const url = req.url();
    let host;
    try { host = new URL(url).hostname; } catch (_) { return route.abort(); }
    if (!allow.has(host)) {
      stats.blocked++;
      const e = EMPTY[req.resourceType()] || EMPTY._;
      return route.fulfill({ status: 200, contentType: e.contentType, body: e.body });
    }
    try {
      const r = await fetchThroughCurl(url);
      return route.fulfill({ status: r.meta.status, contentType: r.meta.contentType, body: r.body });
    } catch (e) {
      stats.failed++;
      const em = EMPTY[req.resourceType()] || EMPTY._;
      return route.fulfill({ status: 599, contentType: em.contentType, body: em.body });
    }
  });
}

// Determinism: kill animation/transition/caret even where the theme's own
// prefers-reduced-motion blocks do not (11 @keyframes, 6 rm blocks per §1.3),
// and stop scroll-behavior:smooth from interfering with the settle pass.
const FREEZE_CSS = `
*, *::before, *::after {
  animation-delay: -0.0001s !important;
  animation-duration: 0.0001s !important;
  animation-iteration-count: 1 !important;
  transition-duration: 0.0001s !important;
  transition-delay: 0s !important;
  caret-color: transparent !important;
}
html { scroll-behavior: auto !important; }
`;

/* Force every image to load and decode NOW.
 *
 * This is the single most important determinism control in the harness. A
 * full-page screenshot renders content that was never scrolled into view, so
 * `loading="lazy"` images below the fold can be captured blank — and whether
 * they are blank depends on network timing, which means the same page produces
 * different pixels on consecutive runs. Measured on the homepage before this
 * existed: 2.65% of pixels differed between two back-to-back runs, entirely
 * from two image rows that painted in one run and not the other.
 *
 * So: flip loading to eager, drop async decoding, un-hide Jetpack/WP lazy
 * placeholders, then await decode() on every image rather than trusting
 * `complete` (which is true for a lazy image that has not started). */
const NORMALISE_IMG_SRC = `(function(stripSrcset){
  window.__vrNormaliseImg = function (i) {
    if (!i || i.tagName !== 'IMG') return;
    if (i.loading === 'lazy') i.loading = 'eager';
    i.decoding = 'sync';
    // Common lazy-loader attribute swaps (Jetpack, WP core, Boost).
    for (const pair of [['data-lazy-src', 'src'], ['data-src', 'src'],
                        ['data-lazy-srcset', 'srcset'], ['data-srcset', 'srcset']]) {
      const v = i.getAttribute(pair[0]);
      if (v && i.getAttribute(pair[1]) !== v) i.setAttribute(pair[1], v);
    }
    if (stripSrcset && (i.hasAttribute('srcset') || i.hasAttribute('sizes'))) {
      // Which srcset candidate the browser picks depends on the layout width at
      // the moment the parser reaches the tag, which is a race: the same page
      // can resolve to a different candidate on consecutive runs, and with
      // object-fit: cover a different candidate crops differently. Measured on
      // /blog/ before this: card imagery shifted between two back-to-back runs.
      // Dropping srcset/sizes pins every run to the single src URL. Layout is
      // unaffected (width/height and CSS own the box); only bitmap resolution
      // changes, identically in baseline and candidate.
      i.removeAttribute('srcset');
      i.removeAttribute('sizes');
    }
    const p = i.parentElement;
    if (stripSrcset && p && p.tagName === 'PICTURE') {
      for (const s of Array.from(p.querySelectorAll('source'))) s.remove();
    }
  };
  // Normalise as the parser produces nodes, not after load — by load time the
  // candidate has already been chosen and the race has already happened.
  const mo = new MutationObserver(function (records) {
    for (const r of records) {
      for (const n of r.addedNodes) {
        if (n.nodeType !== 1) continue;
        if (n.tagName === 'IMG') window.__vrNormaliseImg(n);
        else if (n.querySelectorAll) {
          for (const im of n.querySelectorAll('img')) window.__vrNormaliseImg(im);
        }
      }
    }
  });
  const start = function () {
    mo.observe(document.documentElement, { childList: true, subtree: true });
    for (const im of document.querySelectorAll('img')) window.__vrNormaliseImg(im);
  };
  if (document.documentElement) start();
  else document.addEventListener('readystatechange', start, { once: true });
})(STRIP_SRCSET);`;

const FORCE_IMAGES = () => {
  const imgs = Array.from(document.images);
  for (const i of imgs) {
    if (window.__vrNormaliseImg) window.__vrNormaliseImg(i);
    else { if (i.loading === 'lazy') i.loading = 'eager'; i.decoding = 'sync'; }
  }
  for (const el of Array.from(document.querySelectorAll('iframe[loading="lazy"]'))) {
    el.loading = 'eager';
  }
  return imgs.length;
};

const AWAIT_IMAGES = (budgetMs) => {
  const settled = (i) => new Promise((res) => {
    const done = () => res();
    if (i.complete) return i.decode().then(done, done);
    i.addEventListener('load', () => i.decode().then(done, done), { once: true });
    i.addEventListener('error', done, { once: true });
    setTimeout(done, budgetMs);
  });
  return Promise.all(Array.from(document.images).map(settled)).then(() => ({
    total: document.images.length,
    painted: Array.from(document.images).filter((i) => i.complete && i.naturalWidth > 0).length,
  }));
};

async function settle(page, opts) {
  // Fonts first: a late webfont swap is the classic false diff.
  await page.evaluate(() => (document.fonts ? document.fonts.ready.then(() => true) : true))
    .catch(() => {});
  await page.evaluate(FORCE_IMAGES).catch(() => {});
  // Scroll to the bottom in viewport-sized steps to trip IntersectionObserver
  // reveals and any JS-driven lazy loader, then back to the top.
  await page.evaluate(async () => {
    const step = Math.max(200, window.innerHeight);
    const pause = (ms) => new Promise((r) => setTimeout(r, ms));
    let y = 0;
    // Height can grow as content loads; re-read it each iteration, bounded.
    for (let i = 0; i < 300; i++) {
      const max = document.documentElement.scrollHeight;
      if (y >= max) break;
      window.scrollTo(0, y);
      await pause(60);
      y += step;
    }
    window.scrollTo(0, document.documentElement.scrollHeight);
    await pause(250);
    window.scrollTo(0, 0);
    await pause(250);
  });
  // Anything the scroll pass newly inserted also gets forced.
  await page.evaluate(FORCE_IMAGES).catch(() => {});
  // Drive reveal-gated components to the state a visitor actually sees.
  const revealCounts = await page.evaluate((reveals) => {
    const counts = {};
    for (const r of reveals) {
      const els = Array.from(document.querySelectorAll(r.selector));
      counts[r.selector] = els.length;
      for (const el of els) el.classList.add(r.add_class);
    }
    return counts;
  }, opts.reveals).catch(() => null);
  let imageState = null;
  try {
    imageState = await page.evaluate(AWAIT_IMAGES, opts.imageBudgetMs);
  } catch (_) { /* reported as null below */ }
  await page.waitForLoadState('networkidle', { timeout: 20000 }).catch(() => {});
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(opts.settleMs);
  // Re-read after the settle delay: this is the number that goes in the
  // manifest, so an unpainted image is visible as data, not as a mystery diff.
  try {
    imageState = await page.evaluate(() => ({
      total: document.images.length,
      painted: Array.from(document.images).filter((i) => i.complete && i.naturalWidth > 0).length,
    }));
  } catch (_) { /* keep the earlier reading */ }
  return { images: imageState, reveals: revealCounts };
}

async function main() {
  const { chromium } = loadPlaywright();
  const browser = await chromium.launch({ args: ['--no-sandbox', '--force-color-profile=srgb',
                                                 '--disable-lcd-text', '--hide-scrollbars'] });
  const results = [];
  const maskSelectors = [];
  for (const group of Object.keys(cfg.masks)) {
    for (const sel of cfg.masks[group]) maskSelectors.push({ group, sel });
  }

  for (const vp of cfg.viewports) {
    const ctx = await browser.newContext({
      viewport: { width: vp.width, height: vp.height },
      deviceScaleFactor: vp.scale,
      reducedMotion: 'reduce',
      colorScheme: 'light',
      forcedColors: 'none',
      locale: 'en-US',
      timezoneId: cfg.timezone,
      javaScriptEnabled: true,
      bypassCSP: true,
    });
    await installRouting(ctx);
    await ctx.addInitScript({
      content: NORMALISE_IMG_SRC.replace('STRIP_SRCSET', cfg.stripSrcset ? 'true' : 'false'),
    });
    const page = await ctx.newPage();
    page.setDefaultTimeout(cfg.navTimeout);

    for (const route of cfg.routes) {
      const url = cfg.baseUrl.replace(/\/$/, '') + route.path +
        (cfg.cacheBust ? (route.path.includes('?') ? '&' : '?') + 'vrb=' + cfg.runId : '');
      const rec = { id: route.id, path: route.path, template: route.template,
                    viewport: vp.name, width: vp.width, height: vp.height, scale: vp.scale };
      try {
        const resp = await page.goto(url, { waitUntil: 'load', timeout: cfg.navTimeout });
        rec.http_status = resp ? resp.status() : null;
        await page.addStyleTag({ content: FREEZE_CSS }).catch(() => {});
        const settled = await settle(page, cfg);
        rec.images = settled.images;
        rec.reveal_matches = settled.reveals;

        const counts = {};
        for (const m of maskSelectors) {
          counts[m.group] = (counts[m.group] || 0) +
            await page.locator(m.sel).count().catch(() => 0);
        }
        rec.mask_matches = counts;
        rec.scroll_height = await page.evaluate(() => document.documentElement.scrollHeight);
        rec.doc_title = await page.title();

        const file = path.join(cfg.pngDir, route.id + '-' + vp.name + '.png');
        await page.screenshot({
          path: file,
          fullPage: true,
          animations: 'disabled',
          caret: 'hide',
          scale: 'device',
          mask: maskSelectors.map((m) => page.locator(m.sel)),
          maskColor: cfg.maskColor,
          timeout: cfg.navTimeout,
        });
        rec.file = path.basename(file);
        rec.ok = true;
      } catch (e) {
        rec.ok = false;
        rec.error = String((e && e.message) || e).slice(0, 400);
      }
      process.stderr.write(`  ${rec.ok ? 'ok  ' : 'FAIL'} ${route.id}/${vp.name}` +
        (rec.error ? ' — ' + rec.error.split('\n')[0]
                   : ` (${rec.scroll_height}px, img ${rec.images ? rec.images.painted + '/' + rec.images.total : '?'})`) + '\n');
      results.push(rec);
    }
    await ctx.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(cfg.outDir, 'captures.json'),
    JSON.stringify({ stats, results }, null, 2));
}

main().catch((e) => { console.error('FATAL:', (e && e.stack) || e); process.exit(1); });
"""


COMPARE_JS = r"""
'use strict';
/* Pixel comparison driver for scripts/visual_baseline.py (issue #473).
 *
 * Runs in Chromium because neither pixelmatch/pngjs (node) nor Pillow/numpy
 * (python) exist in this environment, and Chromium decodes PNG natively. The
 * algorithm is pixelmatch's: YIQ colour-space delta with an antialias-tolerant
 * threshold. Images are processed in horizontal strips so a 2880x20000 full-page
 * capture does not need three full-size canvases resident at once. */

const fs = require('fs');
const path = require('path');
const http = require('http');

function loadPlaywright() {
  for (const c of ['playwright', '/opt/node22/lib/node_modules/playwright',
                   '/usr/lib/node_modules/playwright', '/usr/local/lib/node_modules/playwright']) {
    try { return require(c); } catch (_) { /* next */ }
  }
  console.error('FATAL: playwright is not resolvable from the compare driver.');
  process.exit(2);
}

const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));

function serve(roots, port) {
  const srv = http.createServer((req, res) => {
    const rel = decodeURIComponent(req.url.split('?')[0]);
    const m = rel.match(/^\/(base|cand|diff)\/(.+)$/);
    if (!m) {
      // The comparison page itself. Serving it from this origin (rather than
      // about:blank via setContent) is what keeps the canvas untainted so
      // getImageData is allowed.
      res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
      res.end('<!doctype html><html><head><title>vrdiff</title></head><body></body></html>');
      return;
    }
    const file = path.join(roots[m[1]], m[2]);
    if (!file.startsWith(roots[m[1]])) { res.writeHead(403); res.end(); return; }
    fs.readFile(file, (err, data) => {
      if (err) { res.writeHead(404); res.end(); return; }
      res.writeHead(200, {
        'content-type': 'image/png',
        'cache-control': 'no-store',
        'access-control-allow-origin': '*',
      });
      res.end(data);
    });
  });
  return new Promise((r) => srv.listen(port, '127.0.0.1', () => r(srv)));
}

const PAGE_FN = function (baseUrl, candUrl, threshold, stripHeight, wantDiff) {
  return new Promise(async (resolve) => {
    const load = (src) => new Promise((res, rej) => {
      const im = new Image();
      im.crossOrigin = 'anonymous';  // belt and braces against canvas tainting
      im.onload = () => res(im);
      im.onerror = () => rej(new Error('image load failed: ' + src));
      im.src = src;
    });
    let a, b;
    try { a = await load(baseUrl); b = await load(candUrl); }
    catch (e) { return resolve({ error: String(e.message || e) }); }

    const W = Math.max(a.naturalWidth, b.naturalWidth);
    const H = Math.max(a.naturalHeight, b.naturalHeight);
    const out = {
      base: { w: a.naturalWidth, h: a.naturalHeight },
      cand: { w: b.naturalWidth, h: b.naturalHeight },
      compareW: W, compareH: H,
    };
    // Pixels outside the smaller image count as differing: a page that got
    // taller has changed, and that must show up in the percentage too.
    const cw = Math.min(a.naturalWidth, b.naturalWidth);
    const ch = Math.min(a.naturalHeight, b.naturalHeight);
    let diffPixels = (W * H) - (cw * ch);

    const ca = document.createElement('canvas');
    const cb = document.createElement('canvas');
    ca.width = cw; cb.width = cw;
    const ga = ca.getContext('2d', { willReadFrequently: true });
    const gb = cb.getContext('2d', { willReadFrequently: true });

    let dctx = null;
    if (wantDiff) {
      const cd = document.createElement('canvas');
      cd.width = W; cd.height = H;
      dctx = cd.getContext('2d');
      dctx.fillStyle = '#ffffff';
      dctx.fillRect(0, 0, W, H);
      window.__diffCanvas = cd;
    }

    // pixelmatch's YIQ deltas.
    const rgb2y = (r, g, bl) => r * 0.29889531 + g * 0.58662247 + bl * 0.11448223;
    const rgb2i = (r, g, bl) => r * 0.59597799 - g * 0.27417610 - bl * 0.32180189;
    const rgb2q = (r, g, bl) => r * 0.21147017 - g * 0.52261711 + bl * 0.31114694;
    const maxDelta = 35215 * threshold * threshold;

    for (let y0 = 0; y0 < ch; y0 += stripHeight) {
      const h = Math.min(stripHeight, ch - y0);
      ca.height = h; cb.height = h;
      ga.clearRect(0, 0, cw, h); gb.clearRect(0, 0, cw, h);
      ga.drawImage(a, 0, y0, cw, h, 0, 0, cw, h);
      gb.drawImage(b, 0, y0, cw, h, 0, 0, cw, h);
      const da = ga.getImageData(0, 0, cw, h).data;
      const db = gb.getImageData(0, 0, cw, h).data;
      let dimg = null;
      if (dctx) dimg = dctx.createImageData(cw, h);
      for (let i = 0; i < da.length; i += 4) {
        const r1 = da[i], g1 = da[i + 1], b1 = da[i + 2], a1 = da[i + 3];
        const r2 = db[i], g2 = db[i + 1], b2 = db[i + 2], a2 = db[i + 3];
        let delta = 0;
        if (r1 !== r2 || g1 !== g2 || b1 !== b2 || a1 !== a2) {
          const y1 = rgb2y(r1, g1, b1), y2 = rgb2y(r2, g2, b2);
          const dy = y1 - y2;
          const di = rgb2i(r1, g1, b1) - rgb2i(r2, g2, b2);
          const dq = rgb2q(r1, g1, b1) - rgb2q(r2, g2, b2);
          const dalpha = (a1 - a2) * 0.5;
          delta = 0.5053 * dy * dy + 0.299 * di * di + 0.1957 * dq * dq + 0.25 * dalpha * dalpha;
        }
        if (delta > maxDelta) {
          diffPixels++;
          if (dimg) { dimg.data[i] = 255; dimg.data[i + 1] = 0; dimg.data[i + 2] = 60; dimg.data[i + 3] = 255; }
        } else if (dimg) {
          // Unchanged pixels ghosted so the red marks are readable in context.
          const v = 255 - (255 - (r1 * 0.299 + g1 * 0.587 + b1 * 0.114)) * 0.15;
          dimg.data[i] = v; dimg.data[i + 1] = v; dimg.data[i + 2] = v; dimg.data[i + 3] = 255;
        }
      }
      if (dctx && dimg) dctx.putImageData(dimg, 0, y0);
    }
    out.diffPixels = diffPixels;
    out.totalPixels = W * H;
    out.diffPct = W * H ? (diffPixels / (W * H)) * 100 : 0;
    resolve(out);
  });
};

async function main() {
  const { chromium } = loadPlaywright();
  const srv = await serve({ base: cfg.baseDir, cand: cfg.candDir, diff: cfg.diffDir }, cfg.port);
  fs.mkdirSync(cfg.diffDir, { recursive: true });
  const browser = await chromium.launch({ args: ['--no-sandbox', '--force-color-profile=srgb'] });
  const ctx = await browser.newContext({ viewport: { width: 400, height: 300 } });
  const page = await ctx.newPage();
  await page.goto(`http://127.0.0.1:${cfg.port}/`);
  await page.evaluate(`window.__cmp = ${PAGE_FN.toString()}`);

  const results = [];
  for (const pair of cfg.pairs) {
    const r = await page.evaluate(
      ([b, c, t, s, w]) => window.__cmp(b, c, t, s, w),
      [`http://127.0.0.1:${cfg.port}/base/${pair.baseFile}`,
       `http://127.0.0.1:${cfg.port}/cand/${pair.candFile}`,
       cfg.threshold, cfg.stripHeight, !!pair.wantDiff]
    );
    r.key = pair.key;
    if (pair.wantDiff && !r.error) {
      const b64 = await page.evaluate(() =>
        window.__diffCanvas ? window.__diffCanvas.toDataURL('image/png').split(',')[1] : null);
      if (b64) {
        fs.writeFileSync(path.join(cfg.diffDir, pair.diffFile), Buffer.from(b64, 'base64'));
        r.diffFile = pair.diffFile;
      }
      await page.evaluate(() => { window.__diffCanvas = null; });
    }
    process.stderr.write(`  cmp ${pair.key}: ` +
      (r.error ? 'ERROR ' + r.error : r.diffPct.toFixed(4) + '% of ' + r.totalPixels) + '\n');
    results.push(r);
  }
  await browser.close();
  srv.close();
  fs.writeFileSync(cfg.outFile, JSON.stringify({ results }, null, 2));
}

main().catch((e) => { console.error('FATAL:', (e && e.stack) || e); process.exit(1); });
"""


def write_driver(run_dir: Path, name: str, source: str) -> Path:
    """Materialise a driver into the (git-ignored) run directory."""
    p = run_dir / name
    p.write_text(source, encoding="utf-8")
    return p


# ==========================================================================
# capture
# ==========================================================================


def do_capture(
    *,
    base: str,
    routes: list[dict[str, Any]],
    viewports: list[dict[str, Any]],
    masks: dict[str, list[str]],
    reveals: list[dict[str, str]],
    run_id: str,
    tools: dict[str, str],
    settle_ms: int,
    cache_bust: bool,
    keep_cache: bool,
    strip_srcset: bool = True,
) -> tuple[Path, dict[str, Any]]:
    run_dir = ARTIFACT_ROOT / run_id
    png_dir = run_dir / "png"
    cache_dir = run_dir / "cache"
    run_dir.mkdir(parents=True, exist_ok=True)
    assert_ignored(run_dir)

    cfg = {
        "runId": run_id,
        "baseUrl": base,
        "routes": routes,
        "viewports": viewports,
        "masks": masks,
        "reveals": reveals,
        "maskColor": MASK_COLOR,
        "allowHosts": list(ALLOW_HOSTS),
        "outDir": str(run_dir),
        "pngDir": str(png_dir),
        "cacheDir": str(cache_dir),
        "settleMs": settle_ms,
        "imageBudgetMs": IMAGE_BUDGET_MS,
        "navTimeout": NAV_TIMEOUT_MS,
        "curlTimeout": 60,
        "cacheBust": cache_bust,
        "stripSrcset": strip_srcset,
        "timezone": "America/Vancouver",
    }
    cfg_path = run_dir / "capture-config.json"
    cfg_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    driver = write_driver(run_dir, "capture-driver.js", CAPTURE_JS)

    info(f"capturing {len(routes)} routes x {len(viewports)} viewports -> {png_dir}")
    proc = subprocess.run(
        [tools["node"], str(driver), str(cfg_path)], env=node_env(), check=False
    )
    if proc.returncode != 0:
        fatal(f"capture driver exited {proc.returncode}", code=1)

    captures_path = run_dir / "captures.json"
    if not captures_path.exists():
        fatal("capture driver produced no captures.json", code=1)
    driver_out = json.loads(captures_path.read_text(encoding="utf-8"))

    captures = []
    failures = []
    for rec in driver_out["results"]:
        entry = dict(rec)
        if rec.get("ok") and rec.get("file"):
            f = png_dir / rec["file"]
            entry["sha256"] = sha256_file(f)
            entry["bytes"] = f.stat().st_size
            w, h = png_dimensions(f)
            entry["png_width"] = w
            entry["png_height"] = h
            entry["rel_path"] = f"{run_id}/png/{rec['file']}"
        else:
            failures.append(f"{rec['id']}/{rec['viewport']}: {rec.get('error', 'unknown')}")
        captures.append(entry)

    if failures:
        fatal(
            "capture failed for "
            + str(len(failures))
            + " route/viewport pair(s):\n  "
            + "\n  ".join(failures)
            + "\n  A partial baseline is not a baseline. Nothing was written.",
            code=1,
        )

    manifest = {
        "schema": MANIFEST_SCHEMA,
        "run_id": run_id,
        "issue": 473,
        "created_at": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        "base_url": base,
        "artifact_dir": f"{ARTIFACT_ROOT_REL}/{run_id}",
        "artifacts_committed": False,
        "tools": tools,
        "settings": {
            "device_scale": viewports[0]["scale"] if viewports else DEFAULT_DEVICE_SCALE,
            "reduced_motion": "reduce",
            "color_scheme": "light",
            "forced_colors": "none",
            "timezone": "America/Vancouver",
            "settle_ms": settle_ms,
            "cache_bust": cache_bust,
            "strip_srcset": strip_srcset,
            "mask_color": MASK_COLOR,
            "allow_hosts": list(ALLOW_HOSTS),
            "full_page": True,
        },
        "tolerance": TOLERANCE,
        "masks": masks,
        "reveals": reveals,
        "routes": routes,
        "route_preflight": [],  # filled by the caller
        "viewports": viewports,
        "fetch_stats": driver_out.get("stats", {}),
        "captures": captures,
    }
    if not keep_cache and cache_dir.exists():
        shutil.rmtree(cache_dir, ignore_errors=True)
    return run_dir, manifest


# ==========================================================================
# storage guard — the mechanism that makes "never commit PNGs" enforceable
# ==========================================================================

# Only JSON manifests / diff results and markdown reports may be tracked under the
# artifact root. The run-id part is permissive (a human may pass --run-id), but the
# stem and extension are not: nothing binary can match this.
ALLOWED_TRACKED_RE = re.compile(
    r"^(?:manifest|diff)-[0-9A-Za-z._-]+\.json$|^report-[0-9A-Za-z._-]+\.md$|^README\.md$"
)
BINARY_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".bmp", ".tiff", ".mp4", ".zip")


def assert_ignored(path: Path) -> None:
    """Refuse to write artifacts into a directory git would track."""
    rel = path.relative_to(REPO_ROOT)
    proc = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "check-ignore", "-q", str(rel)],
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        fatal(
            f"{rel} is NOT git-ignored. Refusing to write capture artifacts into a\n"
            f"  tracked path — that is issue #318's failure mode.\n"
            f"  Add to .gitignore:\n    {ARTIFACT_ROOT_REL}/*\n"
            f"    !{ARTIFACT_ROOT_REL}/manifest-*.json\n"
            f"    !{ARTIFACT_ROOT_REL}/diff-*.json\n"
            f"    !{ARTIFACT_ROOT_REL}/report-*.md"
        )


def do_guard(quiet: bool = False) -> int:
    """Fail if any capture binary is tracked or staged. Run after every capture."""
    problems: list[str] = []

    tracked = [p for p in git("ls-files", "--", ARTIFACT_ROOT_REL).splitlines() if p.strip()]
    for p in tracked:
        name = Path(p).name
        if not ALLOWED_TRACKED_RE.match(name):
            problems.append(f"tracked file under the artifact root is not an allowed manifest: {p}")

    staged = [p for p in git("diff", "--cached", "--name-only").splitlines() if p.strip()]
    for p in staged:
        if p.lower().endswith(BINARY_EXT):
            problems.append(f"binary staged for commit: {p}")

    # The ignore rule itself must be live, not merely written down.
    probe = ARTIFACT_ROOT / "__guard_probe__" / "probe.png"
    rel = probe.relative_to(REPO_ROOT)
    rc = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "check-ignore", "-q", str(rel)],
        capture_output=True,
        check=False,
    ).returncode
    if rc != 0:
        problems.append(
            f"{rel} would NOT be ignored by git — the .gitignore rule for "
            f"{ARTIFACT_ROOT_REL}/* is missing or broken"
        )

    if problems:
        print("FATAL: visual-baseline storage guard failed (issue #318):", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        print(
            "  PNGs from this harness must never be tracked. Unstage them "
            "(git restore --staged <file>) and fix .gitignore.",
            file=sys.stderr,
        )
        return 1
    if not quiet:
        print(
            f"visual-baseline storage guard OK — {len(tracked)} tracked file(s) under "
            f"{ARTIFACT_ROOT_REL}, all manifests/reports; no binaries staged."
        )
    return 0


# ==========================================================================
# manifest / run discovery
# ==========================================================================


def manifest_path(run_id: str) -> Path:
    return ARTIFACT_ROOT / f"manifest-{run_id}.json"


def _created_at(p: Path) -> str:
    try:
        return json.loads(p.read_text(encoding="utf-8")).get("created_at", "")
    except Exception:
        return ""


def list_manifests(kind: str | None = None) -> list[Path]:
    """Manifests oldest-first, ordered by their recorded `created_at`.

    Deliberately not ordered by filename: run ids can be overridden with
    --run-id, and a lexicographic sort would then put "BASE1" after a real
    timestamp and silently pick the wrong "newest".
    """
    if not ARTIFACT_ROOT.exists():
        return []
    paths = list(ARTIFACT_ROOT.glob("manifest-*.json"))
    if kind:
        paths = [
            p
            for p in paths
            if json.loads(p.read_text(encoding="utf-8")).get("kind") == kind
        ]
    return sorted(paths, key=lambda p: (_created_at(p), p.name))


def resolve_base_manifest(base_arg: str | None) -> Path:
    if base_arg:
        cand = Path(base_arg)
        if cand.exists() and cand.is_file():
            return cand
        p = manifest_path(base_arg)
        if p.exists():
            return p
        fatal(
            f"no baseline manifest for BASE={base_arg}.\n"
            f"  Looked for {p}\n"
            f"  Available: {[m.name for m in list_manifests()] or 'none — run `make visual-baseline` first'}"
        )
    # Default to the newest manifest of kind "baseline". Falling back to a
    # candidate manifest would quietly compare a candidate against a candidate.
    manifests = list_manifests(kind="baseline")
    if not manifests:
        any_manifests = list_manifests()
        fatal(
            "no baseline manifest found. Run `make visual-baseline` first.\n"
            f"  (looked in {ARTIFACT_ROOT_REL}/manifest-*.json for kind=baseline)\n"
            + (
                f"  Found only candidate manifests: {[m.name for m in any_manifests]}"
                if any_manifests
                else ""
            )
        )
    return manifests[-1]


# ==========================================================================
# verdicts
# ==========================================================================


def verdict_for(diff_pct: float | None, height_delta_pct: float | None, tol: dict) -> str:
    if diff_pct is None:
        return "error"
    if height_delta_pct is not None and abs(height_delta_pct) > tol["height_delta_pct"]:
        return "fail"
    if diff_pct > tol["warn_pct"]:
        return "fail"
    if diff_pct > tol["pass_pct"]:
        return "warn"
    return "pass"


WORST_ORDER = {"pass": 0, "warn": 1, "fail": 2, "error": 3}


# ==========================================================================
# subcommands
# ==========================================================================


def cmd_preflight(args: argparse.Namespace) -> int:
    tools = preflight_browser()
    print("Chromium/Playwright preflight OK")
    for k, v in tools.items():
        print(f"  {k}: {v}")
    routes = enabled_routes(args.routes)
    checks = preflight_routes(args.base, routes, strict=not args.no_strict_routes)
    print(f"route preflight ({len(checks)} routes):")
    for c in checks:
        flag = "ok " if c["status"] == c["expected"] else "!! "
        print(f"  {flag}{c['status']}  {c['path']}")
    print(f"storage guard: {'OK' if do_guard(quiet=True) == 0 else 'FAILED'}")
    return 0


def cmd_capture(args: argparse.Namespace) -> int:
    tools = preflight_browser()
    routes = enabled_routes(args.routes)
    viewports = selected_viewports(args.viewports, args.scale)
    masks = DEFAULT_MASKS
    reveals = DEFAULT_REVEALS
    if args.masks:
        override = json.loads(Path(args.masks).read_text(encoding="utf-8"))
        masks = override.get("masks", override)
        reveals = override.get("reveals", reveals)

    strip_srcset = not args.keep_srcset
    checks = preflight_routes(args.base, routes, strict=not args.no_strict_routes)
    run_id = args.run_id or run_id_now()

    info(f"run {run_id}: css identity + Boost bundle readback")
    css = css_identity(args.base)
    boost = boost_bundle(args.base)

    if args.expect_theme_version and css.get("live_theme_version") != args.expect_theme_version:
        fatal(
            "live theme version is "
            f"{css.get('live_theme_version')!r}, expected {args.expect_theme_version!r}.\n"
            "  Refusing to freeze a baseline against an unexpected deploy "
            "(AURORA-STYLESHEET-REBUILD-PLAN.md §4.6)."
        )

    run_dir, manifest = do_capture(
        base=args.base,
        routes=routes,
        viewports=viewports,
        masks=masks,
        reveals=reveals,
        run_id=run_id,
        tools=tools,
        settle_ms=args.settle_ms,
        cache_bust=not args.no_cache_bust,
        keep_cache=args.keep_cache,
        strip_srcset=strip_srcset,
    )
    manifest["kind"] = args.kind
    manifest["route_preflight"] = checks
    manifest["css_identity"] = css
    manifest["boost"] = boost

    mpath = manifest_path(run_id)
    mpath.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    total_bytes = sum(c.get("bytes", 0) for c in manifest["captures"])
    print()
    print(f"baseline run {run_id}")
    print(f"  captures : {len(manifest['captures'])}  ({total_bytes / 1e6:.1f} MB, NOT committed)")
    print(f"  images   : {run_dir.relative_to(REPO_ROOT)}/png/  (git-ignored)")
    print(f"  manifest : {mpath.relative_to(REPO_ROOT)}  <- commit this")
    print(
        f"  theme    : live {css.get('live_theme_version')} / repo {css.get('repo_theme_version')}"
        f"  css identical: {css.get('all_identical')}"
    )
    print(f"  boost    : css bundle {boost.get('css_bundle_hash')} js {boost.get('js_bundle_hash')}")
    if not css.get("all_identical"):
        drifted = [r["file"] for r in css["files"] if not r["identical"]]
        print(f"  NOTE     : live != repo for {drifted} — expected while a deploy is pending")
    print()
    return do_guard()


def cmd_diff(args: argparse.Namespace) -> int:
    tools = preflight_browser()
    base_manifest_path = resolve_base_manifest(args.base_run)
    base_manifest = json.loads(base_manifest_path.read_text(encoding="utf-8"))
    if base_manifest.get("schema") != MANIFEST_SCHEMA:
        fatal(f"{base_manifest_path} has schema {base_manifest.get('schema')!r}, expected {MANIFEST_SCHEMA!r}")

    base_run = base_manifest["run_id"]
    base_png_dir = ARTIFACT_ROOT / base_run / "png"

    routes = enabled_routes(args.routes)
    viewports = selected_viewports(args.viewports, args.scale or base_manifest["settings"]["device_scale"])
    if viewports and viewports[0]["scale"] != base_manifest["settings"]["device_scale"]:
        fatal(
            f"device scale mismatch: baseline was captured at "
            f"{base_manifest['settings']['device_scale']}x, this run would use "
            f"{viewports[0]['scale']}x. Captures at different scales are not comparable."
        )

    # Capture settings must match the baseline's, not this invocation's defaults.
    strip_srcset = base_manifest["settings"].get("strip_srcset", True)
    checks = preflight_routes(args.base, routes, strict=not args.no_strict_routes)
    run_id = args.run_id or run_id_now()
    info(f"candidate run {run_id} (baseline {base_run})")
    css = css_identity(args.base)
    boost = boost_bundle(args.base)

    run_dir, manifest = do_capture(
        base=args.base,
        routes=routes,
        viewports=viewports,
        # Masks and reveal end-states must match the baseline exactly, or the
        # comparison is between two different pages.
        masks=base_manifest["masks"],
        reveals=base_manifest.get("reveals", DEFAULT_REVEALS),
        run_id=run_id,
        tools=tools,
        settle_ms=args.settle_ms,
        cache_bust=not args.no_cache_bust,
        keep_cache=args.keep_cache,
        strip_srcset=strip_srcset,
    )
    manifest["kind"] = "candidate"
    manifest["route_preflight"] = checks
    manifest["css_identity"] = css
    manifest["boost"] = boost
    manifest["baseline_run"] = base_run
    manifest_path(run_id).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    base_by_key = {f"{c['id']}/{c['viewport']}": c for c in base_manifest["captures"]}
    cand_by_key = {f"{c['id']}/{c['viewport']}": c for c in manifest["captures"]}

    pairs = []
    rows: dict[str, dict[str, Any]] = {}
    tol = base_manifest.get("tolerance", TOLERANCE)

    for key, cand in cand_by_key.items():
        base_cap = base_by_key.get(key)
        row: dict[str, Any] = {
            "key": key,
            "route": cand["id"],
            "path": cand["path"],
            "viewport": cand["viewport"],
            "candidate_sha256": cand.get("sha256"),
            "baseline_sha256": base_cap.get("sha256") if base_cap else None,
            "candidate_height": cand.get("png_height"),
            "baseline_height": base_cap.get("png_height") if base_cap else None,
            "candidate_scroll_height": cand.get("scroll_height"),
            "baseline_scroll_height": base_cap.get("scroll_height") if base_cap else None,
            "mask_matches": cand.get("mask_matches"),
        }
        if base_cap is None:
            row["verdict"] = "error"
            row["note"] = "no baseline capture for this route/viewport pair"
            rows[key] = row
            continue

        bh, chh = base_cap.get("png_height") or 0, cand.get("png_height") or 0
        row["height_delta_pct"] = ((chh - bh) / bh * 100) if bh else None

        if base_cap.get("sha256") and base_cap["sha256"] == cand.get("sha256"):
            # Byte-identical PNGs. Zero differing pixels by construction; no need
            # to decode. This is the fast path a stable site should take.
            row["diff_pct"] = 0.0
            row["diff_pixels"] = 0
            row["method"] = "sha256-identical"
            row["verdict"] = verdict_for(0.0, row["height_delta_pct"], tol)
            rows[key] = row
            continue

        base_file = base_png_dir / (base_cap.get("file") or "")
        if not base_file.exists():
            row["verdict"] = "error"
            row["method"] = "hash-only"
            row["note"] = (
                f"hashes differ but baseline PNG {base_file.relative_to(REPO_ROOT)} is gone "
                "(images are never committed). Re-freeze the baseline: make visual-baseline"
            )
            rows[key] = row
            continue

        row["method"] = "pixel"
        rows[key] = row
        pairs.append(
            {
                "key": key,
                "baseFile": base_cap["file"],
                "candFile": cand["file"],
                "diffFile": f"{cand['id']}-{cand['viewport']}-diff.png",
                "wantDiff": not args.no_diff_images,
            }
        )

    diff_dir = run_dir / "diff"
    if pairs:
        info(f"comparing {len(pairs)} changed pair(s) in Chromium")
        cmp_cfg = {
            "baseDir": str(base_png_dir),
            "candDir": str(run_dir / "png"),
            "diffDir": str(diff_dir),
            "outFile": str(run_dir / "compare.json"),
            "pairs": pairs,
            "threshold": tol["pixel_threshold"],
            "stripHeight": args.strip_height,
            "port": args.port,
        }
        cmp_cfg_path = run_dir / "compare-config.json"
        cmp_cfg_path.write_text(json.dumps(cmp_cfg, indent=2), encoding="utf-8")
        driver = write_driver(run_dir, "compare-driver.js", COMPARE_JS)
        proc = subprocess.run(
            [tools["node"], str(driver), str(cmp_cfg_path)], env=node_env(), check=False
        )
        if proc.returncode != 0:
            fatal(f"compare driver exited {proc.returncode}", code=1)
        cmp_out = json.loads((run_dir / "compare.json").read_text(encoding="utf-8"))
        for res in cmp_out["results"]:
            row = rows[res["key"]]
            if res.get("error"):
                row["verdict"] = "error"
                row["note"] = res["error"]
                continue
            row["diff_pct"] = round(res["diffPct"], 6)
            row["diff_pixels"] = res["diffPixels"]
            row["total_pixels"] = res["totalPixels"]
            if res.get("diffFile"):
                row["diff_image"] = f"{run_dir.relative_to(REPO_ROOT)}/diff/{res['diffFile']}"
            row["verdict"] = verdict_for(row["diff_pct"], row.get("height_delta_pct"), tol)

    # Report order follows the route/viewport declaration order, not the sort
    # order of the keys — a PR reviewer reads it top-to-bottom as the site.
    route_rank = {r["id"]: i for i, r in enumerate(routes)}
    vp_rank = {v["name"]: i for i, v in enumerate(viewports)}
    ordered = sorted(
        rows.values(),
        key=lambda r: (route_rank.get(r["route"], 99), vp_rank.get(r["viewport"], 99)),
    )
    worst = max((WORST_ORDER[r["verdict"]] for r in ordered), default=0)
    worst_name = [k for k, v in WORST_ORDER.items() if v == worst][0]

    # Prune diff images for pairs that passed — they are noise and they are bytes.
    if diff_dir.exists() and not args.keep_all_diffs:
        keep = {Path(r["diff_image"]).name for r in ordered if r.get("diff_image") and r["verdict"] != "pass"}
        for f in diff_dir.glob("*.png"):
            if f.name not in keep:
                f.unlink()
        for r in ordered:
            if r.get("diff_image") and Path(r["diff_image"]).name not in keep:
                r.pop("diff_image", None)

    result = {
        "schema": MANIFEST_SCHEMA,
        "kind": "diff",
        "issue": 473,
        "created_at": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        "baseline_run": base_run,
        "candidate_run": run_id,
        "base_url": args.base,
        "tolerance": tol,
        "masks": base_manifest["masks"],
        "verdict": worst_name,
        "counts": {
            v: sum(1 for r in ordered if r["verdict"] == v) for v in ("pass", "warn", "fail", "error")
        },
        "css_identity": {
            "baseline": {
                "live_theme_version": base_manifest.get("css_identity", {}).get("live_theme_version"),
                "all_identical": base_manifest.get("css_identity", {}).get("all_identical"),
            },
            "candidate": {
                "live_theme_version": css.get("live_theme_version"),
                "repo_theme_version": css.get("repo_theme_version"),
                "all_identical": css.get("all_identical"),
                "files": css["files"],
            },
        },
        "boost": {
            "baseline_css_bundle_hash": base_manifest.get("boost", {}).get("css_bundle_hash"),
            "candidate_css_bundle_hash": boost.get("css_bundle_hash"),
            "changed": base_manifest.get("boost", {}).get("css_bundle_hash")
            != boost.get("css_bundle_hash"),
            "candidate": boost,
        },
        "pairs": ordered,
    }
    dpath = ARTIFACT_ROOT / f"diff-{run_id}.json"
    dpath.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print()
    print(f"visual-diff {base_run} -> {run_id}: {worst_name.upper()}")
    for v in ("pass", "warn", "fail", "error"):
        print(f"  {v:<6} {result['counts'][v]}")
    print(f"  report data: {dpath.relative_to(REPO_ROOT)}")
    print(f"  markdown   : make visual-diff-report DIFF={run_id}")
    print()

    guard_rc = do_guard()
    if guard_rc != 0:
        return guard_rc
    if worst_name in ("fail", "error"):
        return 1
    if worst_name == "warn" and args.strict:
        return 1
    return 0


def _fmt_pct(v: float | None) -> str:
    if v is None:
        return "—"
    if v == 0:
        return "0"
    return f"{v:.4f}"


VERDICT_MARK = {"pass": "PASS", "warn": "WARN", "fail": "FAIL", "error": "ERROR"}


def render_report(result: dict[str, Any]) -> str:
    L: list[str] = []
    L.append(f"## Visual regression — {result['verdict'].upper()}")
    L.append("")
    L.append(
        f"Baseline `{result['baseline_run']}` → candidate `{result['candidate_run']}` "
        f"against `{result['base_url']}`, generated {result['created_at']}."
    )
    L.append("")
    c = result["counts"]
    L.append(
        f"**{c['pass']} pass · {c['warn']} warn · {c['fail']} fail · {c['error']} error** "
        f"across {len(result['pairs'])} route/viewport pairs."
    )
    L.append("")
    tol = result["tolerance"]
    L.append(
        f"Tolerance: pass ≤ {tol['pass_pct']}% differing pixels · warn ≤ {tol['warn_pct']}% · "
        f"fail > {tol['warn_pct']}% or > {tol['height_delta_pct']}% full-page height delta · "
        f"per-pixel threshold {tol['pixel_threshold']}."
    )
    L.append("")
    L.append("| Route | Viewport | Diff % | Height Δ% | Method | Verdict |")
    L.append("|---|---|---:|---:|---|---|")
    for p in result["pairs"]:
        L.append(
            f"| `{p['path']}` | {p['viewport']} | {_fmt_pct(p.get('diff_pct'))} | "
            f"{_fmt_pct(p.get('height_delta_pct'))} | {p.get('method', '—')} | "
            f"**{VERDICT_MARK[p['verdict']]}** |"
        )
    L.append("")

    notes = [p for p in result["pairs"] if p.get("note")]
    if notes:
        L.append("### Notes")
        L.append("")
        for p in notes:
            L.append(f"- `{p['key']}`: {p['note']}")
        L.append("")

    imgs = [p for p in result["pairs"] if p.get("diff_image")]
    if imgs:
        L.append("### Diff images")
        L.append("")
        L.append(
            "Not committed. Attach these to the PR comment or upload as CI artifacts "
            "(AURORA-STYLESHEET-REBUILD-PLAN.md §4.5.4):"
        )
        L.append("")
        for p in imgs:
            L.append(f"- `{p['key']}` → `{p['diff_image']}`")
        L.append("")

    L.append("### Environment readback")
    L.append("")
    cand = result["css_identity"]["candidate"]
    L.append(
        f"- Live theme version: **{cand.get('live_theme_version')}** "
        f"(repo `theme/kk-aurora/style.css`: **{cand.get('repo_theme_version')}**)"
    )
    L.append(
        f"- Live-vs-repo CSS md5 identity: **{'all identical' if cand.get('all_identical') else 'DRIFT'}**"
    )
    for f in cand.get("files", []):
        mark = "=" if f["identical"] else "≠"
        L.append(f"  - `{f['file']}` {mark} live `{(f.get('live_md5') or '')[:12]}` / repo `{(f.get('repo_md5') or '')[:12]}`")
    b = result["boost"]
    L.append(
        f"- Jetpack Boost CSS bundle: baseline `{b.get('baseline_css_bundle_hash')}` → "
        f"candidate `{b.get('candidate_css_bundle_hash')}` "
        f"({'CHANGED' if b.get('changed') else 'unchanged'})"
    )
    if not b.get("changed"):
        L.append(
            "  - If a deploy happened between these two runs, an unchanged Boost hash means "
            "it did not reach the edge (risk R-2) — not that it had no visual effect. Purge "
            "Boost + PressCACHE and re-run before reading this as a green light."
        )
    L.append("")
    L.append(
        "_Screenshots cannot see focus, hover or keyboard behaviour (#424 remains a separate "
        "gate), and there is no staging environment — this compares post-deploy live against "
        "pre-deploy live (§4.7)._"
    )
    return "\n".join(L)


def cmd_report(args: argparse.Namespace) -> int:
    if args.diff_run:
        p = Path(args.diff_run)
        if not p.exists():
            p = ARTIFACT_ROOT / f"diff-{args.diff_run}.json"
    else:
        diffs = (
            sorted(ARTIFACT_ROOT.glob("diff-*.json"), key=lambda p: (_created_at(p), p.name))
            if ARTIFACT_ROOT.exists()
            else []
        )
        if not diffs:
            fatal(
                "no diff result found. Run `make visual-diff BASE=<ts>` first.\n"
                f"  (looked in {ARTIFACT_ROOT_REL}/diff-*.json)"
            )
        p = diffs[-1]
    if not p.exists():
        fatal(f"{p} does not exist")
    result = json.loads(p.read_text(encoding="utf-8"))
    md = render_report(result)
    if args.out:
        out = Path(args.out)
        if not out.is_absolute():
            out = REPO_ROOT / out
    else:
        out = ARTIFACT_ROOT / f"report-{result['candidate_run']}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md + "\n", encoding="utf-8")
    print(md)
    print()
    print(f"(written to {out.relative_to(REPO_ROOT)})", file=sys.stderr)
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    manifests = list_manifests()
    if not manifests:
        print("no baseline manifests yet — run `make visual-baseline`")
        return 0
    print(f"{'run':<20} {'kind':<10} {'theme':<8} {'boost':<12} {'captures':>8}  images")
    for m in manifests:
        d = json.loads(m.read_text(encoding="utf-8"))
        png_dir = ARTIFACT_ROOT / d["run_id"] / "png"
        n_png = len(list(png_dir.glob("*.png"))) if png_dir.exists() else 0
        print(
            f"{d['run_id']:<20} {d.get('kind', '?'):<10} "
            f"{str(d.get('css_identity', {}).get('live_theme_version')):<8} "
            f"{str(d.get('boost', {}).get('css_bundle_hash')):<12} "
            f"{len(d.get('captures', [])):>8}  {n_png} png on disk"
        )
    return 0


def cmd_guard(args: argparse.Namespace) -> int:
    return do_guard()


def cmd_prune(args: argparse.Namespace) -> int:
    """Delete capture directories, keeping the newest N. Manifests are kept."""
    if not ARTIFACT_ROOT.exists():
        print("nothing to prune")
        return 0
    dirs = sorted(p for p in ARTIFACT_ROOT.iterdir() if p.is_dir())
    victims = dirs[: max(0, len(dirs) - args.keep)]
    freed = 0
    for d in victims:
        freed += sum(f.stat().st_size for f in d.rglob("*") if f.is_file())
        shutil.rmtree(d, ignore_errors=True)
        print(f"removed {d.relative_to(REPO_ROOT)}")
    print(f"kept {min(args.keep, len(dirs))} run dir(s); freed {freed / 1e6:.1f} MB")
    print("Manifests are untouched — a lost baseline is one `make visual-baseline` away (§4.5.5).")
    return 0


# ==========================================================================
# CLI
# ==========================================================================


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="visual_baseline.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p: argparse.ArgumentParser) -> None:
        p.add_argument("--base", default=BASE_URL, help="origin to capture (default %(default)s)")
        p.add_argument("--routes", nargs="*", help="subset of route ids or paths")
        p.add_argument("--viewports", nargs="*", help="subset of viewport names")
        p.add_argument(
            "--no-strict-routes",
            action="store_true",
            help="warn instead of aborting when a route's HTTP status is unexpected",
        )

    def capture_opts(p: argparse.ArgumentParser) -> None:
        p.add_argument("--scale", type=int, default=DEFAULT_DEVICE_SCALE, help="device scale factor")
        p.add_argument("--settle-ms", type=int, default=SETTLE_MS)
        p.add_argument("--no-cache-bust", action="store_true")
        p.add_argument("--keep-cache", action="store_true", help="keep the per-run curl cache")
        p.add_argument("--run-id", help="override the run id (default: UTC timestamp)")
        p.add_argument("--masks", help="path to a JSON file overriding masks/reveals")
        p.add_argument(
            "--keep-srcset",
            action="store_true",
            help="keep srcset/sizes (higher fidelity, but candidate selection is a race)",
        )

    p = sub.add_parser("preflight", help="check Chromium, routes and the storage guard")
    common(p)
    p.set_defaults(func=cmd_preflight)

    p = sub.add_parser("capture", help="capture and freeze a baseline (make visual-baseline)")
    common(p)
    capture_opts(p)
    p.add_argument("--kind", default="baseline", choices=["baseline", "candidate"])
    p.add_argument(
        "--expect-theme-version",
        help="abort unless live style.css reports this Version (§4.6)",
    )
    p.set_defaults(func=cmd_capture)

    p = sub.add_parser("diff", help="capture a candidate and compare (make visual-diff)")
    common(p)
    capture_opts(p)
    p.add_argument("--base-run", help="baseline run id or manifest path (default: newest)")
    p.add_argument("--strict", action="store_true", help="treat warn as failure")
    p.add_argument("--no-diff-images", action="store_true")
    p.add_argument("--keep-all-diffs", action="store_true", help="keep diff images for passing pairs too")
    p.add_argument("--strip-height", type=int, default=1024)
    p.add_argument("--port", type=int, default=8763)
    # Unlike `capture`, diff's --scale inherits the baseline's unless given.
    p.set_defaults(func=cmd_diff, scale=None)

    p = sub.add_parser("report", help="markdown summary of a diff (make visual-diff-report)")
    p.add_argument("--diff-run", help="diff run id or path (default: newest)")
    p.add_argument("--out", help="write markdown here instead of the artifact root")
    p.set_defaults(func=cmd_report)

    p = sub.add_parser("list", help="list baseline manifests and which still have images on disk")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("guard", help="fail if any capture binary is tracked or staged (#318)")
    p.set_defaults(func=cmd_guard)

    p = sub.add_parser("prune", help="delete old capture directories (manifests kept)")
    p.add_argument("--keep", type=int, default=2)
    p.set_defaults(func=cmd_prune)

    return ap


def main(argv: list[str] | None = None) -> int:
    ap = build_parser()
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
