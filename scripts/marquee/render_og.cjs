// Marquee OG card renderer — screenshots an HTML card to a 1200x630 PNG via headless Chromium.
//   usage: node render_og.cjs <input.html> <output.png>
// Resolves Playwright + the Chromium binary defensively so it works locally (and is a clean
// no-op where neither is installed — build.py gates on og_available() before calling this).
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

function loadPlaywright() {
  try { return require('playwright'); } catch (e) {}
  try {
    const root = execSync('npm root -g').toString().trim();
    return require(path.join(root, 'playwright'));
  } catch (e) {}
  for (const p of ['/opt/node22/lib/node_modules/playwright',
                   '/usr/lib/node_modules/playwright',
                   '/usr/local/lib/node_modules/playwright']) {
    try { return require(p); } catch (e) {}
  }
  throw new Error('playwright not found');
}

function chromiumPath() {
  const globs = ['/opt/pw-browsers'];
  if (process.env.PLAYWRIGHT_BROWSERS_PATH) globs.unshift(process.env.PLAYWRIGHT_BROWSERS_PATH);
  for (const base of globs) {
    try {
      for (const d of fs.readdirSync(base)) {
        if (!d.startsWith('chromium-')) continue;
        const exe = path.join(base, d, 'chrome-linux', 'chrome');
        if (fs.existsSync(exe)) return exe;
      }
    } catch (e) {}
  }
  return null; // let Playwright try its default resolution
}

(async () => {
  const [input, output] = process.argv.slice(2);
  if (!input || !output) { console.error('usage: render_og.cjs <in.html> <out.png>'); process.exit(2); }
  const { chromium } = loadPlaywright();
  const exe = chromiumPath();
  const browser = await chromium.launch(exe ? { executablePath: exe } : {});
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(input));
  await page.waitForTimeout(400); // let fonts settle (animation is disabled in the card)
  await page.screenshot({ path: output, clip: { x: 0, y: 0, width: 1200, height: 630 } });
  await browser.close();
  console.log('og →', output);
})().catch((e) => { console.error(String(e)); process.exit(1); });
