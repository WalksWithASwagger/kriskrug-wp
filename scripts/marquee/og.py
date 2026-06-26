"""OG share-card generation for marquee boards (1200x630, on-brand, local render).

Builds a branded card HTML per board (reusing the board renderer + Aurora tokens) and
screenshots it to og.png via headless Chromium (scripts/marquee/render_og.cjs). The card
has NO animation script — the pre-rendered cells already show the final letters.

Rendering needs node + Chromium, which are present locally (where promote/build runs) but
not in scan-only CI. og_available() gates it; build.py preserves committed PNGs when absent.
"""
from __future__ import annotations
import glob
import html
import os
import shutil
import subprocess
from pathlib import Path

from render import TOKENS_DIST, BOARD_RULES, board_section

OG_W, OG_H = 1200, 630
HERE = Path(__file__).resolve().parent
CJS = HERE / "render_og.cjs"

CARD_CSS = f"""
*{{box-sizing:border-box}}
html,body{{margin:0;width:{OG_W}px;height:{OG_H}px;overflow:hidden;background:var(--kkm-deep);
  font-family:"Clash Display",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  background:radial-gradient(900px 500px at 50% -20%,rgba(241,91,67,.10),transparent 60%),var(--kkm-deep)}}
.card{{width:{OG_W}px;height:{OG_H}px;display:flex;flex-direction:column;justify-content:center;
  padding:54px 64px;gap:6px}}
.card .wm{{font-family:"JetBrains Mono",monospace;text-transform:uppercase;letter-spacing:.32em;
  font-size:15px;color:var(--kkm-signal);display:flex;align-items:center;gap:12px}}
.card .wm::before{{content:"";width:9px;height:9px;border-radius:50%;background:var(--kkm-signal);
  box-shadow:0 0 14px var(--kkm-signal)}}
.card .kkm{{padding:18px 0 0;justify-content:flex-start}}
.card .kkm-frame{{background:none;border:none;box-shadow:none;padding:0;width:100%}}
.card .kkm-kicker{{display:none}}
.card .foot{{margin-top:auto;font-family:"JetBrains Mono",monospace;font-size:15px;color:var(--kkm-text-muted);
  display:flex;justify-content:space-between;align-items:flex-end}}
.card .foot b{{color:var(--kkm-text)}}
"""


def card_html(board):
    """Self-contained 1200x630 card document for one board (no animation script)."""
    e = html.escape
    after = board.get("after")
    section = board_section(board["board"], "", board.get("skin", "led"))
    foot_left = f'kriskrug.co<span style="opacity:.5"> · the marquee</span>'
    foot_right = f'after {e(after)}' if after else ""
    return (
        "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        f"<style>{TOKENS_DIST}{BOARD_RULES}{CARD_CSS}</style></head><body>"
        f'<div class="card"><div class="wm">The Marquee</div>{section}'
        f'<div class="foot"><span>{foot_left}</span><span>{foot_right}</span></div>'
        "</div></body></html>"
    )


def og_available():
    """True when node + a Chromium binary are present (so a PNG can actually be produced)."""
    if not shutil.which("node"):
        return False
    bases = [os.environ.get("PLAYWRIGHT_BROWSERS_PATH", ""), "/opt/pw-browsers"]
    return any(glob.glob(os.path.join(b, "chromium-*/chrome-linux/chrome")) for b in bases if b)


def render_og(board, out_dir: Path) -> bool:
    """Write the card HTML and screenshot og.png. Returns True if the PNG was produced."""
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "og.html").write_text(card_html(board), encoding="utf-8")
    if not og_available():
        return False
    try:
        subprocess.run(
            ["node", str(CJS), str(out_dir / "og.html"), str(out_dir / "og.png")],
            check=True, capture_output=True, timeout=90,
        )
        return (out_dir / "og.png").exists()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return False
