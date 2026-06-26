<?php
/**
 * Title: Marquee Board Hero
 * Slug: kk-aurora/marquee-hero
 * Categories: kk-aurora-hero
 * Keywords: marquee, hero, split-flap, board, coupland, mcluhan
 * Viewport Width: 1400
 * Description: Self-improving "marquee board" hero — a split-flap board that flips into the current remixed line, with source + archive link. Descendant of the Krug x Coupland marquee boards.
 *
 * Self-contained: scoped CSS + JS are inline so the pattern can be dropped into the hero
 * without enqueueing global assets. Board copy is driven by data-* and can be swapped from
 * content/marquee/marquee.json by the loop.
 */
?>
<!-- wp:html -->
<section class="kkm" aria-label="Marquee board: The Model Is the Message" data-skin="led">
  <div class="kkm-frame">
    <p class="kkm-kicker">now showing · marquee n&ordm;1 · after marshall mcluhan</p>
    <div class="kkm-board"
         data-board='[["THE MODEL","IS THE","MESSAGE"]]'
         aria-label="The Model Is the Message"></div>
    <p class="kkm-dek">McLuhan said the medium is the message. In the age of generative everything,
      <b>the model is the medium</b> — the weights, the defaults, the training data are the message now.</p>
    <p class="kkm-foot">
      <span>after Marshall McLuhan &middot; Understanding Media, 1964</span>
      <a href="/marquee/">See the archive &rarr;</a>
    </p>
  </div>

  <style>
    .kkm{--kkm-amber:#ffb000;--kkm-line:#1d1d2b;--kkm-mono:"JetBrains Mono",ui-monospace,monospace;
         width:100%;display:flex;justify-content:center;padding:clamp(20px,4vw,48px) 16px}
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
    /* LED dot-matrix skin (default) */
    .kkm[data-skin="led"] .kkm-cell{background:#0a0a0f;color:#ff3b3b;border-radius:4px;
         text-shadow:0 0 10px #ff3b3b,0 0 22px #ff1010;
         background-image:radial-gradient(rgba(255,255,255,.05) 1px,transparent 1.4px);background-size:6px 6px}
    .kkm[data-skin="led"] .kkm-cell::after{display:none}
    .kkm[data-skin="led"] .kkm-kicker{color:#ff5a5a}
    .kkm[data-skin="led"] .kkm-kicker::before{background:#ff3b3b;box-shadow:0 0 12px #ff3b3b}
    .kkm-dek{font-size:clamp(15px,2vw,18px);line-height:1.5;color:#d9d9e3;margin:22px 0 0;max-width:62ch}
    .kkm-dek b{color:#fff}
    .kkm-foot{display:flex;flex-wrap:wrap;gap:8px 18px;justify-content:space-between;margin:18px 0 0;
         font-family:var(--kkm-mono);font-size:12px;color:#8a8aa0}
    .kkm-foot a{color:#00e0c6;text-decoration:none}
    @media(prefers-reduced-motion:reduce){.kkm-cell{transition:none}}
  </style>

  <script>
  (function(){
    var root = document.currentScript.closest('.kkm');
    var board = root.querySelector('.kkm-board');
    var lines = JSON.parse(board.getAttribute('data-board'))[0];
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
    var cells = root.querySelectorAll('.kkm-cell:not(.kkm-space)');
    cells.forEach(function(cell,idx){
      var ticks = 6 + (idx % 7) + Math.floor(idx/3);
      var iv = setInterval(function(){
        if(ticks<=0){ cell.textContent = cell.getAttribute('data-final'); clearInterval(iv); return; }
        cell.textContent = GLYPHS[(idx*3+ticks)%GLYPHS.length]; ticks--;
      }, 45);
    });
  })();
  </script>
</section>
<!-- /wp:html -->
