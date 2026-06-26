"""Shared marquee board renderer (Tier 1: token colors, pre-rendered cells, single-source JS).

Renders a board (list of text lines) to HTML in the LED skin (+ alt skins), using Aurora
design tokens rather than hardcoded hex. Cells are PRE-RENDERED in HTML so the board shows
without JS (no CLS); the flip animation is progressive enhancement.

Consumers:
- build.py → static /marquee/ archive pages (content/marquee/dist/) — inline ANIM_JS.
- build.py → theme partial theme/kk-aurora/parts/marquee-current.html — no script
  (the home page enqueues assets/js/marquee.js, also generated from ANIM_JS, deferred).
"""
from __future__ import annotations
import html
import json

SKINS = ("led", "splitflap", "letterpress", "teletype")

# Aurora tokens (theme.json slugs). Two binding contexts share one set of --kkm-* vars:
#   dist pages have no theme CSS, so bind to literal hex;
#   the WP theme has --wp--preset--color--*, so bind to those (with hex fallback).
TOKENS_DIST = """
:root{--kkm-signal:#F15B43;--kkm-wildcard:#C8FF3D;--kkm-cyan:#00E5FF;
  --kkm-void:#000000;--kkm-deep:#0D0D12;--kkm-surface:#12121A;--kkm-elevated:#1A1A25;
  --kkm-text:#F0F0F5;--kkm-text-muted:#8E8EA8;--kkm-line:#252532}
"""
TOKENS_WP = """
.kkm{--kkm-signal:var(--wp--preset--color--signal,#F15B43);
  --kkm-cyan:var(--wp--preset--color--cyan,#00E5FF);
  --kkm-void:var(--wp--preset--color--void,#000000);
  --kkm-deep:var(--wp--preset--color--deep,#0D0D12);
  --kkm-surface:var(--wp--preset--color--surface,#12121A);
  --kkm-elevated:var(--wp--preset--color--elevated,#1A1A25);
  --kkm-text:var(--wp--preset--color--text-primary,#F0F0F5);
  --kkm-text-muted:var(--wp--preset--color--text-muted,#8E8EA8);
  --kkm-line:var(--wp--preset--color--muted,#252532)}
"""

# Geometry + skins. References only --kkm-* vars, so it works in both contexts.
BOARD_RULES = """
.kkm{--kkm-mono:"JetBrains Mono",ui-monospace,monospace;
     display:flex;justify-content:center;padding:clamp(20px,4vw,44px) 16px}
.kkm-frame{width:min(960px,100%);border-radius:18px;padding:clamp(24px,4vw,40px) clamp(18px,3vw,32px);
     background:linear-gradient(180deg,var(--kkm-elevated),var(--kkm-deep));border:1px solid var(--kkm-line);
     box-shadow:0 40px 120px -50px rgba(0,0,0,.85),inset 0 1px 0 rgba(255,255,255,.04)}
.kkm-kicker{font-family:var(--kkm-mono);text-transform:uppercase;letter-spacing:.22em;font-size:11px;
     color:var(--kkm-signal);display:flex;gap:10px;align-items:center;margin:0 0 22px}
.kkm-kicker::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--kkm-signal);
     box-shadow:0 0 12px var(--kkm-signal);animation:kkm-pulse 2s infinite}
@keyframes kkm-pulse{0%,100%{opacity:1}50%{opacity:.3}}
.kkm-board{display:flex;flex-direction:column;gap:10px;user-select:none}
.kkm-row{display:flex;flex-wrap:wrap;gap:6px}
.kkm-cell{position:relative;display:inline-flex;align-items:center;justify-content:center;
     contain:layout;width:clamp(26px,5.4vw,56px);height:clamp(40px,8vw,82px);font-family:var(--kkm-mono);
     font-weight:700;font-size:clamp(20px,4.4vw,46px);line-height:1;border-radius:4px;
     background:var(--kkm-deep);color:var(--kkm-signal);
     text-shadow:0 0 10px var(--kkm-signal),0 0 22px var(--kkm-signal);
     background-image:radial-gradient(rgba(255,255,255,.05) 1px,transparent 1.4px);background-size:6px 6px;
     box-shadow:inset 0 1px 0 rgba(255,255,255,.04),0 2px 4px rgba(0,0,0,.5)}
.kkm-cell.kkm-space{background:transparent;box-shadow:none;text-shadow:none;width:clamp(10px,2.4vw,24px)}
/* alt skins (kept available; default is led) */
.kkm[data-skin="splitflap"] .kkm-cell{background:var(--kkm-surface);text-shadow:none;color:var(--kkm-signal)}
.kkm[data-skin="splitflap"] .kkm-cell::after{content:"";position:absolute;left:0;right:0;top:50%;height:1px;background:#000;opacity:.7}
.kkm[data-skin="letterpress"] .kkm-frame{background:var(--kkm-text);border-color:#ddd6c4}
.kkm[data-skin="letterpress"] .kkm-cell{background:transparent;box-shadow:none;text-shadow:none;color:#16140f;
     font-weight:800;font-size:clamp(26px,6vw,72px);width:auto;height:auto;padding:0 .02em;background-image:none}
.kkm[data-skin="teletype"] .kkm-frame{background:var(--kkm-void);border-color:#0c2a26}
.kkm[data-skin="teletype"] .kkm-cell{background:transparent;box-shadow:none;color:var(--kkm-cyan);
     text-shadow:0 0 8px var(--kkm-cyan);font-weight:600;font-size:clamp(18px,4.2vw,42px);width:auto;height:auto;background-image:none}
.kkm[data-skin="teletype"] .kkm-kicker,.kkm[data-skin="teletype"] .kkm-kicker::before{color:var(--kkm-cyan);background:var(--kkm-cyan)}
@media(prefers-reduced-motion:reduce){.kkm-cell{transition:none}}
"""

# Single-source flip animation. Animates PRE-RENDERED cells (reads data-final), so the board
# is fully visible without JS. Wrapped per-context by partial_js()/inline_js().
ANIM_JS = """
function kkmHydrate(scope){
  var boards = (scope||document).querySelectorAll('.kkm-board');
  if(!boards.length) return;
  if(window.matchMedia && window.matchMedia('(prefers-reduced-motion:reduce)').matches) return;
  var GLYPHS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ#@%&".split("");
  boards.forEach(function(board){
    board.querySelectorAll('.kkm-cell:not(.kkm-space)').forEach(function(cell,idx){
      var fin = cell.getAttribute('data-final'); if(fin===null) return;
      var ticks = 6 + (idx % 7) + Math.floor(idx/3);
      var iv = setInterval(function(){
        if(ticks<=0){ cell.textContent = fin; clearInterval(iv); return; }
        cell.textContent = GLYPHS[(idx*3+ticks)%GLYPHS.length]; ticks--;
      }, 45);
    });
  });
}
"""


def cells_html(lines, indent="    "):
    """Pre-render board rows + cells with letters present in the HTML (no-JS safe)."""
    rows = []
    for line in lines:
        cells = []
        for ch in line:
            if ch == " ":
                cells.append('<div class="kkm-cell kkm-space" aria-hidden="true"></div>')
            else:
                e = html.escape(ch)
                cells.append(f'<div class="kkm-cell" data-final="{e}" aria-hidden="true">{e}</div>')
        rows.append(f'{indent}<div class="kkm-row">' + "".join(cells) + "</div>")
    return "\n".join(rows)


def board_section(lines, kicker, skin="led", label=None):
    """A standalone <section> for dist pages — cells pre-rendered, board labelled for AT."""
    label = label or " ".join(lines)
    return (
        f'<section class="kkm" data-skin="{html.escape(skin)}">\n'
        f'  <div class="kkm-frame">\n'
        f'    <p class="kkm-kicker">{html.escape(kicker)}</p>\n'
        f'    <div class="kkm-board" role="img" aria-label="{html.escape(label)}">\n'
        f'{cells_html(lines, indent="      ")}\n'
        f'    </div>\n'
        f'  </div>\n'
        f'</section>'
    )


def inline_js():
    """ANIM_JS + a DOMContentLoaded trigger, for the standalone dist pages."""
    return ANIM_JS + "\ndocument.addEventListener('DOMContentLoaded',function(){kkmHydrate(document);});"


def theme_js():
    """ANIM_JS wrapped as the deferred theme asset (assets/js/marquee.js)."""
    return (
        "/* GENERATED by scripts/marquee/build.py from render.ANIM_JS — do not edit by hand. */\n"
        "(function(){\n" + ANIM_JS +
        "\n  if(document.readyState!=='loading'){kkmHydrate(document);}"
        "\n  else{document.addEventListener('DOMContentLoaded',function(){kkmHydrate(document);});}\n"
        "})();\n"
    )
