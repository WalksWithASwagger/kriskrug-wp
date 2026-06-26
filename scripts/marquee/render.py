"""Shared marquee board renderer.

Renders a board (list of text lines) to self-contained HTML/CSS/JS in any of the
four skins. Used by build.py for the static /marquee/ archive pages. The live hero
is rendered by the WordPress pattern (theme/kk-aurora/patterns/marquee-hero.php),
which mirrors this markup.
"""
from __future__ import annotations
import html
import json

SKINS = ("led", "splitflap", "letterpress", "teletype")

# Scoped CSS for the static archive board. Mirrors the WP pattern's .kkm styles.
BOARD_CSS = """
.kkm{--kkm-amber:#ffb000;--kkm-line:#1d1d2b;--kkm-mono:"JetBrains Mono",ui-monospace,monospace;
     display:flex;justify-content:center;padding:clamp(20px,4vw,44px) 16px}
.kkm-frame{width:min(960px,100%);border-radius:18px;padding:clamp(24px,4vw,40px) clamp(18px,3vw,32px);
     background:linear-gradient(180deg,#0e0e16,#08080d);border:1px solid var(--kkm-line);
     box-shadow:0 40px 120px -50px rgba(0,0,0,.85),inset 0 1px 0 rgba(255,255,255,.04)}
.kkm-kicker{font-family:var(--kkm-mono);text-transform:uppercase;letter-spacing:.22em;font-size:11px;
     color:var(--kkm-amber);display:flex;gap:10px;align-items:center;margin:0 0 22px}
.kkm-kicker::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--kkm-amber);
     box-shadow:0 0 12px var(--kkm-amber);animation:kkm-pulse 2s infinite}
@keyframes kkm-pulse{0%,100%{opacity:1}50%{opacity:.3}}
.kkm-board{display:flex;flex-direction:column;gap:10px;user-select:none}
.kkm-row{display:flex;flex-wrap:wrap;gap:6px}
.kkm-cell{position:relative;display:inline-flex;align-items:center;justify-content:center;
     width:clamp(26px,5.4vw,56px);height:clamp(40px,8vw,82px);font-family:var(--kkm-mono);font-weight:700;
     font-size:clamp(20px,4.4vw,46px);line-height:1;background:#15151f;color:var(--kkm-amber);border-radius:6px;
     box-shadow:inset 0 1px 0 rgba(255,255,255,.05),inset 0 -1px 0 rgba(0,0,0,.6),0 2px 4px rgba(0,0,0,.5)}
.kkm-cell::after{content:"";position:absolute;left:0;right:0;top:50%;height:1px;background:#000;opacity:.7}
.kkm-cell.kkm-space{background:transparent;box-shadow:none;width:clamp(10px,2.4vw,24px)}
/* LED */
.kkm[data-skin="led"] .kkm-cell{background:#0a0a0f;color:#ff3b3b;border-radius:4px;
     text-shadow:0 0 10px #ff3b3b,0 0 22px #ff1010;
     background-image:radial-gradient(rgba(255,255,255,.05) 1px,transparent 1.4px);background-size:6px 6px}
.kkm[data-skin="led"] .kkm-cell::after{display:none}
.kkm[data-skin="led"] .kkm-kicker{color:#ff5a5a}
.kkm[data-skin="led"] .kkm-kicker::before{background:#ff3b3b;box-shadow:0 0 12px #ff3b3b}
/* Letterpress */
.kkm[data-skin="letterpress"] .kkm-frame{background:linear-gradient(180deg,#f6f3ec,#ece7da);border-color:#ddd6c4}
.kkm[data-skin="letterpress"] .kkm-cell{background:transparent;box-shadow:none;color:#16140f;
     font-family:var(--kkm-mono);font-weight:800;font-size:clamp(26px,6vw,72px);width:auto;height:auto;
     padding:0 .02em;letter-spacing:-.02em}
.kkm[data-skin="letterpress"] .kkm-cell::after{display:none}
.kkm[data-skin="letterpress"] .kkm-kicker{color:#8a6a00}
.kkm[data-skin="letterpress"] .kkm-kicker::before{background:#8a6a00;box-shadow:none}
/* Teletype */
.kkm[data-skin="teletype"] .kkm-frame{background:#04060a;border-color:#0c2a26}
.kkm[data-skin="teletype"] .kkm-cell{background:transparent;box-shadow:none;color:#00e0c6;
     font-family:var(--kkm-mono);font-weight:600;font-size:clamp(18px,4.2vw,42px);width:auto;height:auto;
     text-shadow:0 0 8px rgba(0,224,198,.5)}
.kkm[data-skin="teletype"] .kkm-cell::after{display:none}
.kkm[data-skin="teletype"] .kkm-kicker{color:#00e0c6}
"""

BOARD_JS = """
document.querySelectorAll('.kkm-board').forEach(function(board){
  var lines = JSON.parse(board.getAttribute('data-board'));
  var GLYPHS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ#@%&".split("");
  var reduce = window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  lines.forEach(function(line){
    var row = document.createElement('div'); row.className='kkm-row';
    line.split('').forEach(function(ch){
      var c=document.createElement('div');
      c.className='kkm-cell'+(ch===' '?' kkm-space':'');
      c.setAttribute('data-final', ch); c.textContent = ch===' '?'':ch;
      row.appendChild(c);
    });
    board.appendChild(row);
  });
  if(reduce) return;
  board.querySelectorAll('.kkm-cell:not(.kkm-space)').forEach(function(cell,idx){
    var ticks = 6 + (idx % 7) + Math.floor(idx/3);
    var iv = setInterval(function(){
      if(ticks<=0){ cell.textContent = cell.getAttribute('data-final'); clearInterval(iv); return; }
      cell.textContent = GLYPHS[(idx*3+ticks)%GLYPHS.length]; ticks--;
    }, 45);
  });
});
"""


def board_html(board_lines, kicker, skin="led"):
    """Return the .kkm <section> markup for a board (animation hydrated by BOARD_JS)."""
    data = html.escape(json.dumps(board_lines), quote=True)
    return (
        f'<section class="kkm" data-skin="{html.escape(skin)}" '
        f'aria-label="{html.escape(" ".join(board_lines))}">\n'
        f'  <div class="kkm-frame">\n'
        f'    <p class="kkm-kicker">{html.escape(kicker)}</p>\n'
        f'    <div class="kkm-board" data-board="{data}" '
        f'aria-label="{html.escape(" ".join(board_lines))}"></div>\n'
        f'  </div>\n'
        f'</section>'
    )
