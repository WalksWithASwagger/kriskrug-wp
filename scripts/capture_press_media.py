#!/usr/bin/env python3
"""Manifest-driven press media capture for the Publications tear sheet.

Reads ``press-media-manifest.json``, captures or fetches each asset, writes JPEGs
to the keynotes assets directory, and emits ``contact-sheet.html`` for KK review.

Capture methods:
  - article_clip: Playwright/Chrome, 1440 viewport, h1-anchored 16:10 clip → 1200×750
  - youtube_thumbnail: YouTube maxresdefault / hqdefault
  - vimeo_thumbnail: Vimeo oEmbed thumbnail
  - itunes_artwork: iTunes Lookup API (600×600 podcast art)

Default is dry-run friendly: skips existing outputs unless ``--force``.
Does not upload to WordPress or PATCH live content.

Usage:
  python3 scripts/capture_press_media.py
  python3 scripts/capture_press_media.py --only press-2026-05-20-storyhive-v2.jpg
  python3 scripts/capture_press_media.py --force --skip-clips
  python3 scripts/capture_press_media.py --contact-sheet-only
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import textwrap
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import requests
from PIL import Image


REPO_ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = REPO_ROOT / "content" / "source-packs" / "keynotes-2026" / "assets"
MANIFEST_PATH = ASSETS_DIR / "press-media-manifest.json"
CONTACT_SHEET_PATH = ASSETS_DIR / "contact-sheet.html"
SPEC_PATH = (
    REPO_ROOT
    / "content"
    / "source-packs"
    / "keynotes-2026"
    / "PUBLICATIONS-DESIGN-SPEC.md"
)

VIEWPORT_WIDTH = 1440
VIEWPORT_HEIGHT = 900
CLIP_VIEWPORT_HEIGHT = 900  # 16:10 at 1440
JPEG_QUALITY = 88

YOUTUBE_ID_RE = re.compile(
    r"(?:youtube\.com/watch\?.*v=|youtu\.be/|youtube\.com/embed/)([A-Za-z0-9_-]{11})"
)
VIMEO_ID_RE = re.compile(r"vimeo\.com/(?:video/)?(\d+)")
APPLE_PODCAST_ID_RE = re.compile(r"/podcast/id(\d+)")


# ---------------------------------------------------------------------------
# Manifest helpers
# ---------------------------------------------------------------------------


def load_manifest(path: Path = MANIFEST_PATH) -> dict:
    if not path.exists():
        raise SystemExit(f"[ABORT] missing manifest: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if "entries" not in data:
        raise SystemExit("[ABORT] manifest missing 'entries' array")
    return data


def entry_by_key(manifest: dict, key: str) -> dict | None:
    for entry in manifest["entries"]:
        if entry["key"] == key:
            return entry
    return None


# ---------------------------------------------------------------------------
# Remote fetch helpers
# ---------------------------------------------------------------------------


def http_get_bytes(url: str, timeout: int = 45) -> bytes:
    response = requests.get(
        url,
        timeout=timeout,
        headers={"User-Agent": "kriskrug-wp-capture/1.0"},
    )
    response.raise_for_status()
    return response.content


def youtube_video_id(url: str) -> str | None:
    match = YOUTUBE_ID_RE.search(url)
    return match.group(1) if match else None


def fetch_youtube_thumbnail(url: str) -> bytes:
    video_id = youtube_video_id(url)
    if not video_id:
        raise ValueError(f"could not parse YouTube id from {url!r}")
    for quality in ("maxresdefault", "hqdefault", "mqdefault"):
        thumb_url = f"https://img.youtube.com/vi/{video_id}/{quality}.jpg"
        response = requests.get(
            thumb_url,
            timeout=30,
            headers={"User-Agent": "kriskrug-wp-capture/1.0"},
        )
        if response.status_code == 200 and len(response.content) > 5000:
            return response.content
    raise RuntimeError(f"YouTube thumbnail fetch failed for {video_id}")


def vimeo_video_id(url: str) -> str | None:
    match = VIMEO_ID_RE.search(url)
    return match.group(1) if match else None


def fetch_vimeo_thumbnail(url: str) -> bytes:
    oembed_url = "https://vimeo.com/api/oembed.json"
    response = requests.get(
        oembed_url,
        params={"url": url},
        timeout=30,
        headers={"User-Agent": "kriskrug-wp-capture/1.0"},
    )
    response.raise_for_status()
    data = response.json()
    thumb_url = data.get("thumbnail_url")
    if not thumb_url:
        raise RuntimeError(f"Vimeo oEmbed missing thumbnail_url for {url}")
    return http_get_bytes(thumb_url)


def apple_podcast_show_id(url: str) -> str | None:
    match = APPLE_PODCAST_ID_RE.search(url)
    return match.group(1) if match else None


def fetch_itunes_artwork(url: str) -> bytes:
    show_id = apple_podcast_show_id(url)
    if not show_id:
        raise ValueError(f"could not parse Apple Podcasts show id from {url!r}")
    lookup_url = "https://itunes.apple.com/lookup"
    response = requests.get(
        lookup_url,
        params={"id": show_id, "entity": "podcast"},
        timeout=30,
        headers={"User-Agent": "kriskrug-wp-capture/1.0"},
    )
    response.raise_for_status()
    data = response.json()
    results = data.get("results") or []
    if not results:
        raise RuntimeError(f"iTunes lookup returned no results for show id {show_id}")
    artwork = results[0].get("artworkUrl600") or results[0].get("artworkUrl100")
    if not artwork:
        raise RuntimeError(f"iTunes lookup missing artwork for show id {show_id}")
    return http_get_bytes(artwork)


# ---------------------------------------------------------------------------
# Image processing
# ---------------------------------------------------------------------------


def save_jpeg_exact(
    raw: bytes,
    dest: Path,
    width: int,
    height: int,
) -> None:
    """Resize/crop center to exact dimensions and write JPEG."""
    with Image.open(BytesIO(raw)) as img:
        img = img.convert("RGB")
        target_ratio = width / height
        src_ratio = img.width / img.height
        if abs(src_ratio - target_ratio) > 0.01:
            if src_ratio > target_ratio:
                new_width = int(img.height * target_ratio)
                left = (img.width - new_width) // 2
                img = img.crop((left, 0, left + new_width, img.height))
            else:
                new_height = int(img.width / target_ratio)
                top = (img.height - new_height) // 2
                img = img.crop((0, top, img.width, top + new_height))
        if img.size != (width, height):
            img = img.resize((width, height), Image.Resampling.LANCZOS)
        dest.parent.mkdir(parents=True, exist_ok=True)
        img.save(dest, format="JPEG", quality=JPEG_QUALITY, optimize=True)


# ---------------------------------------------------------------------------
# Playwright article clip capture (Node driver)
# ---------------------------------------------------------------------------

CLIP_CAPTURE_JS = r"""
'use strict';
const fs = require('fs');
const path = require('path');
const os = require('os');
const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));

function loadPlaywright() {
  const candidates = [
    'playwright',
    'playwright-core',
    path.join(os.homedir(), 'node_modules/playwright'),
    path.join(os.homedir(), 'node_modules/playwright-core'),
    '/opt/node22/lib/node_modules/playwright',
    '/usr/lib/node_modules/playwright',
    '/usr/local/lib/node_modules/playwright',
  ];
  for (const c of candidates) {
    try { return require(c); } catch (_) { /* next */ }
  }
  console.error('FATAL: playwright/playwright-core is not installed. Install with: npm i -g playwright-core');
  process.exit(2);
}

const HIDE_CSS = `
  [class*="cookie" i], [id*="cookie" i], [class*="consent" i], [id*="consent" i],
  [class*="gdpr" i], [class*="banner" i][class*="privacy" i],
  [class*="sticky" i], [style*="position: fixed" i], [style*="position:fixed" i],
  header[class*="sticky" i], nav[class*="sticky" i],
  [class*="ad-" i], [id*="ad-" i], [data-ad], iframe,
  [class*="chat" i], [id*="chat" i], [class*="popup" i],
  [id*="onetrust" i], [class*="onetrust" i],
  [class*="newsletter" i][class*="modal" i],
  [aria-label*="cookie" i], [aria-label*="consent" i]
  { visibility: hidden !important; pointer-events: none !important; }
  html { scroll-behavior: auto !important; }
`;

(async () => {
  const pw = loadPlaywright();
  const launchOpts = {
    headless: true,
    args: ['--disable-dev-shm-usage', '--disable-notifications'],
  };
  if (cfg.executablePath) {
    launchOpts.executablePath = cfg.executablePath;
  } else if (cfg.channel) {
    launchOpts.channel = cfg.channel;
  }
  const browser = await pw.chromium.launch(launchOpts);
  const page = await browser.newPage({
    viewport: { width: cfg.viewportWidth, height: cfg.viewportHeight },
    deviceScaleFactor: 1,
  });
  await page.goto(cfg.url, { waitUntil: 'domcontentloaded', timeout: cfg.timeoutMs || 60000 });
  try {
    await page.waitForLoadState('networkidle', { timeout: 15000 });
  } catch (_) { /* some news sites never idle */ }
  await page.addStyleTag({ content: HIDE_CSS });
  // Extra pass: hide remaining fixed/sticky overlays via computed style.
  await page.evaluate(() => {
    for (const el of document.querySelectorAll('body *')) {
      const style = window.getComputedStyle(el);
      if (style.position === 'fixed' || style.position === 'sticky') {
        el.style.setProperty('visibility', 'hidden', 'important');
        el.style.setProperty('pointer-events', 'none', 'important');
      }
    }
  });
  await page.waitForTimeout(cfg.settleMs || 800);

  const h1 = page.locator('article h1, main h1, h1').first();
  if (await h1.count()) {
    await h1.scrollIntoViewIfNeeded();
    await page.evaluate(() => {
      const el = document.querySelector('article h1, main h1, h1');
      if (!el) return;
      const rect = el.getBoundingClientRect();
      const targetY = Math.max(0, window.scrollY + rect.top - 120);
      window.scrollTo(0, targetY);
    });
    await page.waitForTimeout(cfg.settleMs || 800);
  }

  const clipHeight = cfg.clipHeight || 900;
  const buffer = await page.screenshot({
    type: 'jpeg',
    quality: cfg.jpegQuality || 88,
    clip: { x: 0, y: 0, width: cfg.viewportWidth, height: clipHeight },
  });
  fs.writeFileSync(cfg.outputPath, buffer);
  await browser.close();
  console.log(JSON.stringify({ ok: true, output: cfg.outputPath }));
})().catch((err) => {
  console.error(String(err && err.stack || err));
  process.exit(1);
});
"""

SYSTEM_CHROME_CANDIDATES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
)


def resolve_chromium_executable() -> str | None:
    """Prefer Playwright browser caches, then system Google Chrome."""
    env = __import__("os").environ
    explicit = env.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH") or env.get("CHROME_PATH")
    if explicit and Path(explicit).is_file():
        return explicit

    browsers_path = Path.home() / ".local" / "pw-browsers"
    env_path = env.get("PLAYWRIGHT_BROWSERS_PATH")
    search_roots: list[Path] = []
    if env_path:
        search_roots.append(Path(env_path))
    search_roots.extend(
        [
            Path("/opt/pw-browsers"),
            browsers_path,
            Path.home() / "Library" / "Caches" / "ms-playwright",
            Path.home() / ".cache" / "ms-playwright",
        ]
    )
    patterns = (
        "chromium-*/chrome-linux/chrome",
        "chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium",
        "chromium-*/chrome-mac*/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing",
        "chromium_headless_shell-*/chrome-linux/headless_shell",
        "chromium_headless_shell-*/chrome-mac*/headless_shell",
    )
    found: list[Path] = []
    for root in search_roots:
        if not root.is_dir():
            continue
        for pattern in patterns:
            found.extend(root.glob(pattern))
    if found:
        return str(sorted(found)[-1])

    for candidate in SYSTEM_CHROME_CANDIDATES:
        if Path(candidate).is_file():
            return candidate
    return None


def capture_article_clip_playwright(url: str, raw_jpeg: Path) -> None:
    cfg = {
        "url": url,
        "outputPath": str(raw_jpeg),
        "viewportWidth": VIEWPORT_WIDTH,
        "viewportHeight": VIEWPORT_HEIGHT,
        "clipHeight": CLIP_VIEWPORT_HEIGHT,
        "jpegQuality": JPEG_QUALITY,
        "timeoutMs": 90000,
        "settleMs": 1000,
    }
    chromium = resolve_chromium_executable()
    if chromium:
        cfg["executablePath"] = chromium
    else:
        # Last resort: let Playwright use channel=chrome if installed.
        cfg["channel"] = "chrome"

    with tempfile.TemporaryDirectory(prefix="press-capture-js-") as tmp:
        tmp_path = Path(tmp)
        cfg_path = tmp_path / "clip-config.json"
        js_path = tmp_path / "clip-capture.js"
        cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
        js_path.write_text(CLIP_CAPTURE_JS, encoding="utf-8")

        env = __import__("os").environ.copy()
        env["PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD"] = "1"
        if chromium:
            env["PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH"] = chromium

        proc = subprocess.run(
            ["node", str(js_path), str(cfg_path)],
            capture_output=True,
            text=True,
            env=env,
            timeout=120,
        )
        if proc.returncode != 0:
            stderr = (proc.stderr or proc.stdout or "").strip()
            raise RuntimeError(f"Playwright clip capture failed: {stderr[:500]}")
        if not raw_jpeg.exists():
            raise RuntimeError("Playwright clip capture did not write output file")


def capture_article_clip_chrome_cdp(url: str, raw_jpeg: Path) -> None:
    """Fallback: Chrome headless via DevTools Protocol (no Playwright required)."""
    chrome = resolve_chromium_executable()
    if not chrome:
        raise RuntimeError("No Chrome/Chromium executable found for CDP fallback")

    try:
        import websocket  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "websocket-client required for Chrome CDP fallback (pip install websocket-client)"
        ) from exc

    import json as _json
    import time
    import urllib.request

    port = 9222
    user_data = tempfile.mkdtemp(prefix="press-chrome-profile-")
    chrome_proc = subprocess.Popen(
        [
            chrome,
            f"--remote-debugging-port={port}",
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--disable-dev-shm-usage",
            f"--user-data-dir={user_data}",
            f"--window-size={VIEWPORT_WIDTH},{VIEWPORT_HEIGHT}",
            "about:blank",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        ws_url = None
        deadline = time.time() + 15
        while time.time() < deadline:
            try:
                with urllib.request.urlopen(
                    f"http://127.0.0.1:{port}/json/version", timeout=1
                ) as resp:
                    meta = _json.loads(resp.read().decode())
                    ws_url = meta.get("webSocketDebuggerUrl")
                    if ws_url:
                        break
            except Exception:  # noqa: BLE001
                time.sleep(0.2)
        if not ws_url:
            raise RuntimeError("Chrome CDP endpoint did not become ready")

        ws = websocket.create_connection(ws_url, timeout=60)
        msg_id = 0

        def cdp(method: str, params: dict | None = None, session_id: str | None = None):
            nonlocal msg_id
            msg_id += 1
            payload: dict = {"id": msg_id, "method": method}
            if params:
                payload["params"] = params
            if session_id:
                payload["sessionId"] = session_id
            ws.send(_json.dumps(payload))
            while True:
                raw = ws.recv()
                data = _json.loads(raw)
                if data.get("id") == msg_id:
                    if "error" in data:
                        raise RuntimeError(f"CDP {method}: {data['error']}")
                    return data.get("result") or {}

        target = cdp("Target.createTarget", {"url": "about:blank"})
        session = cdp(
            "Target.attachToTarget",
            {"targetId": target["targetId"], "flatten": True},
        )
        sid = session["sessionId"]
        cdp(
            "Emulation.setDeviceMetricsOverride",
            {
                "width": VIEWPORT_WIDTH,
                "height": VIEWPORT_HEIGHT,
                "deviceScaleFactor": 1,
                "mobile": False,
            },
            session_id=sid,
        )
        cdp("Page.enable", session_id=sid)
        cdp("Runtime.enable", session_id=sid)
        nav = cdp("Page.navigate", {"url": url}, session_id=sid)
        # Wait for load event roughly.
        load_deadline = time.time() + 45
        while time.time() < load_deadline:
            try:
                ws.settimeout(0.5)
                evt = _json.loads(ws.recv())
                if evt.get("method") == "Page.loadEventFired":
                    break
            except Exception:  # noqa: BLE001
                pass
        time.sleep(1.2)
        hide_js = """
        (() => {
          const css = `%s`;
          const style = document.createElement('style');
          style.textContent = css;
          document.documentElement.appendChild(style);
          for (const el of document.querySelectorAll('body *')) {
            const s = getComputedStyle(el);
            if (s.position === 'fixed' || s.position === 'sticky') {
              el.style.setProperty('visibility', 'hidden', 'important');
              el.style.setProperty('pointer-events', 'none', 'important');
            }
          }
          const el = document.querySelector('article h1, main h1, h1');
          if (el) {
            const rect = el.getBoundingClientRect();
            const targetY = Math.max(0, window.scrollY + rect.top - 120);
            window.scrollTo(0, targetY);
          }
          return true;
        })()
        """ % (
            "[class*=cookie i],[id*=cookie i],[class*=consent i],[id*=consent i],"
            "[class*=gdpr i],[class*=sticky i],[class*=ad- i],[id*=ad- i],[data-ad],iframe,"
            "[class*=chat i],[id*=chat i],[class*=popup i],[id*=onetrust i],[class*=onetrust i]"
            "{visibility:hidden!important;pointer-events:none!important;}"
            "html{scroll-behavior:auto!important;}"
        )
        cdp(
            "Runtime.evaluate",
            {"expression": hide_js, "awaitPromise": False},
            session_id=sid,
        )
        time.sleep(0.8)
        shot = cdp(
            "Page.captureScreenshot",
            {
                "format": "jpeg",
                "quality": JPEG_QUALITY,
                "clip": {
                    "x": 0,
                    "y": 0,
                    "width": VIEWPORT_WIDTH,
                    "height": CLIP_VIEWPORT_HEIGHT,
                    "scale": 1,
                },
            },
            session_id=sid,
        )
        import base64

        raw_jpeg.write_bytes(base64.b64decode(shot["data"]))
        ws.close()
        _ = nav  # silence unused
    finally:
        chrome_proc.terminate()
        try:
            chrome_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            chrome_proc.kill()
        import shutil

        shutil.rmtree(user_data, ignore_errors=True)


def capture_article_clip(url: str, dest: Path, width: int, height: int) -> None:
    with tempfile.TemporaryDirectory(prefix="press-capture-") as tmp:
        tmp_path = Path(tmp)
        raw_jpeg = tmp_path / "raw.jpg"
        try:
            capture_article_clip_playwright(url, raw_jpeg)
        except Exception as pw_exc:  # noqa: BLE001
            try:
                capture_article_clip_chrome_cdp(url, raw_jpeg)
            except Exception as cdp_exc:  # noqa: BLE001
                raise RuntimeError(
                    f"clip capture failed (playwright: {pw_exc}; cdp: {cdp_exc})"
                ) from cdp_exc
        if not raw_jpeg.exists():
            raise RuntimeError("clip capture did not write output file")
        save_jpeg_exact(raw_jpeg.read_bytes(), dest, width, height)


# ---------------------------------------------------------------------------
# Per-entry capture dispatch
# ---------------------------------------------------------------------------


def capture_entry(entry: dict, dest: Path, force: bool) -> dict:
    """Capture one manifest entry. Returns result metadata for contact sheet."""
    method = entry["capture_method"]
    width = int(entry["width"])
    height = int(entry["height"])
    source_url = entry["source_url"]
    result = {
        "key": entry["key"],
        "method": method,
        "dest": str(dest),
        "status": "skipped",
        "error": None,
    }

    if dest.exists() and not force:
        result["status"] = "exists"
        return result

    try:
        if method == "article_clip":
            capture_article_clip(source_url, dest, width, height)
        elif method == "youtube_thumbnail":
            raw = fetch_youtube_thumbnail(source_url)
            save_jpeg_exact(raw, dest, width, height)
        elif method == "vimeo_thumbnail":
            raw = fetch_vimeo_thumbnail(source_url)
            save_jpeg_exact(raw, dest, width, height)
        elif method == "itunes_artwork":
            raw = fetch_itunes_artwork(source_url)
            save_jpeg_exact(raw, dest, width, height)
        elif method == "owned_photo":
            raise NotImplementedError(
                "owned_photo capture is Phase 2 (kk-kb media-credits)"
            )
        else:
            raise ValueError(f"unknown capture_method: {method!r}")
        result["status"] = "captured"
    except Exception as exc:  # noqa: BLE001 — collect per-entry errors for contact sheet
        result["status"] = "error"
        result["error"] = str(exc)[:300]
    return result


# ---------------------------------------------------------------------------
# Contact sheet
# ---------------------------------------------------------------------------


def render_contact_sheet(
    manifest: dict,
    results: list[dict],
    output_path: Path = CONTACT_SHEET_PATH,
) -> None:
    result_map = {r["key"]: r for r in results}
    rows = []
    for entry in manifest["entries"]:
        key = entry["key"]
        legacy = entry.get("legacy_file", "")
        dest = ASSETS_DIR / key
        legacy_path = ASSETS_DIR / legacy if legacy else None
        preview = (
            dest
            if dest.exists()
            else (legacy_path if legacy_path and legacy_path.exists() else None)
        )
        preview_href = preview.name if preview else ""
        run_result = result_map.get(key, {})
        run_status = run_result.get("status", "not_run")
        file_status = entry.get("status", "pending_recapture")
        if dest.exists() and run_status in ("captured", "exists"):
            file_status = "captured"

        error = run_result.get("error") or ""
        slots = [entry["slot"]] + entry.get("slots_also", [])
        rows.append(
            f"""
            <article class="sheet-card">
              <figure>
                {'<img src="' + preview_href + '" alt="" loading="lazy">' if preview_href else '<div class="missing">no preview</div>'}
              </figure>
              <div class="meta">
                <h2>{key}</h2>
                <dl>
                  <dt>Tier</dt><dd>{entry["tier"]}</dd>
                  <dt>Slot</dt><dd>{", ".join(slots)}</dd>
                  <dt>Ratio</dt><dd>{entry["ratio"]} ({entry["width"]}×{entry["height"]})</dd>
                  <dt>Outlet</dt><dd>{entry["outlet"]}</dd>
                  <dt>Credit</dt><dd>{entry["credit"]}</dd>
                  <dt>Method</dt><dd>{entry["capture_method"]}</dd>
                  <dt>Legacy</dt><dd>{legacy or "—"}</dd>
                  <dt>Manifest status</dt><dd>{file_status}</dd>
                  <dt>Run</dt><dd>{run_status}</dd>
                  <dt>Source</dt><dd><a href="{entry["source_url"]}" target="_blank" rel="noopener noreferrer">{entry["source_url"]}</a></dd>
                </dl>
                {'<p class="error">' + error + "</p>" if error else ""}
              </div>
            </article>
            """
        )

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Publications press media — contact sheet</title>
  <style>
    :root {{
      --paper: #efe6d2;
      --ink: #171310;
      --muted: #5c5044;
      --line: rgba(23, 19, 16, 0.14);
      --signal: #9a2f14;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 1.5rem;
      background: var(--paper);
      color: var(--ink);
      font: 16px/1.5 "DM Sans", system-ui, sans-serif;
    }}
    header {{
      max-width: 1200px;
      margin: 0 auto 2rem;
      border-bottom: 4px solid var(--signal);
      padding-bottom: 1rem;
    }}
    header h1 {{
      margin: 0 0 0.5rem;
      font: 700 2rem/1.1 "Space Grotesk", system-ui, sans-serif;
    }}
    header p {{ margin: 0; color: var(--muted); max-width: 70ch; }}
    .grid {{
      max-width: 1200px;
      margin: 0 auto;
      display: grid;
      gap: 1.25rem;
    }}
    .sheet-card {{
      display: grid;
      grid-template-columns: minmax(220px, 360px) 1fr;
      gap: 1rem;
      border: 1px solid var(--line);
      border-radius: 4px;
      background: #f7f0df;
      overflow: hidden;
    }}
    .sheet-card figure {{
      margin: 0;
      background: #ddd4c0;
      min-height: 140px;
    }}
    .sheet-card img {{
      display: block;
      width: 100%;
      height: 100%;
      object-fit: cover;
    }}
    .missing {{
      display: grid;
      place-items: center;
      min-height: 160px;
      color: var(--muted);
      font-size: 0.85rem;
    }}
    .meta {{ padding: 1rem 1rem 1rem 0; }}
    .meta h2 {{
      margin: 0 0 0.75rem;
      font: 700 1rem/1.2 "Space Grotesk", system-ui, sans-serif;
      word-break: break-all;
    }}
    dl {{
      display: grid;
      grid-template-columns: 7rem 1fr;
      gap: 0.25rem 0.75rem;
      margin: 0;
      font-size: 0.85rem;
    }}
    dt {{ color: var(--muted); font-weight: 700; }}
    dd {{ margin: 0; }}
    .error {{ color: var(--signal); font-size: 0.85rem; margin: 0.75rem 0 0; }}
    @media (max-width: 720px) {{
      .sheet-card {{ grid-template-columns: 1fr; }}
      .meta {{ padding: 0 1rem 1rem; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Publications press media — contact sheet</h1>
    <p>Generated {generated}. Review every crop before upload. Spec: PUBLICATIONS-DESIGN-SPEC.md. Gate: KK approval required.</p>
  </header>
  <div class="grid">
    {"".join(rows)}
  </div>
</body>
</html>
"""
    output_path.write_text(html, encoding="utf-8")
    output_path.chmod(0o644)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Capture Publications press media from manifest.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
            Examples:
              python3 scripts/capture_press_media.py
              python3 scripts/capture_press_media.py --only press-2026-05-20-storyhive-v2.jpg
              python3 scripts/capture_press_media.py --skip-clips
              python3 scripts/capture_press_media.py --contact-sheet-only
            """
        ),
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=MANIFEST_PATH,
        help=f"Manifest JSON (default: {MANIFEST_PATH.relative_to(REPO_ROOT)})",
    )
    parser.add_argument(
        "--assets-dir",
        type=Path,
        default=ASSETS_DIR,
        help="Output directory for JPEG assets",
    )
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        metavar="KEY",
        help="Capture only this manifest key (repeatable)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing output files",
    )
    parser.add_argument(
        "--skip-clips",
        action="store_true",
        help="Skip article_clip entries (YouTube/iTunes/Vimeo only)",
    )
    parser.add_argument(
        "--contact-sheet-only",
        action="store_true",
        help="Regenerate contact-sheet.html without capturing",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    manifest = load_manifest(args.manifest)
    entries = manifest["entries"]

    if args.only:
        allowed = set(args.only)
        entries = [e for e in entries if e["key"] in allowed]
        missing = allowed - {e["key"] for e in entries}
        if missing:
            raise SystemExit(
                f"[ABORT] unknown manifest keys: {', '.join(sorted(missing))}"
            )

    results: list[dict] = []

    if not args.contact_sheet_only:
        for entry in entries:
            if args.skip_clips and entry["capture_method"] == "article_clip":
                results.append(
                    {
                        "key": entry["key"],
                        "method": entry["capture_method"],
                        "dest": str(args.assets_dir / entry["key"]),
                        "status": "skipped_clip",
                        "error": None,
                    }
                )
                continue
            dest = args.assets_dir / entry["key"]
            print(f"[capture] {entry['key']} ({entry['capture_method']}) …", flush=True)
            result = capture_entry(entry, dest, force=args.force)
            results.append(result)
            if result["status"] == "error":
                print(f"  ERROR: {result['error']}", file=sys.stderr)
            else:
                print(
                    f"  {result['status']}: {dest.relative_to(REPO_ROOT)}", flush=True
                )

    render_contact_sheet(manifest, results, args.assets_dir / "contact-sheet.html")
    print(
        f"[done] contact sheet → {CONTACT_SHEET_PATH.relative_to(REPO_ROOT)}",
        flush=True,
    )
    errors = [r for r in results if r.get("status") == "error"]
    if errors:
        print(
            f"[warn] {len(errors)} capture error(s); see contact sheet", file=sys.stderr
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
