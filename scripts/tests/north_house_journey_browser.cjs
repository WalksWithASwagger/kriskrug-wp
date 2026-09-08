// Run against private public-shell previews, never production content mutations.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const path = require('node:path');
const { chromium } = require('playwright');

const root = path.resolve(process.argv[2]);
const evidence = path.join(root, 'evidence');
fs.mkdirSync(evidence, { recursive: true, mode: 0o700 });
const routes = {
  events: '/events/',
  recap: '/2026/09/03/what-i-showed-founders-about-ai-workflows/',
  services: '/generative-ai-services/',
  contact: '/contact/',
};
const eventCard = '[data-event-id="league-innovators-north-house-ai-show-tell-2026"]';
const allowedHosts = new Set(['127.0.0.1', 'kriskrug.co', 's5102.pcdn.co', 'i0.wp.com', 'c0.wp.com', 's0.wp.com', 'fonts.googleapis.com', 'fonts.gstatic.com']);
const report = { runs: [], journey: [] };

async function serve() {
  let state = 'baseline';
  const server = http.createServer((req, res) => {
    const pathname = new URL(req.url, 'http://127.0.0.1').pathname;
    if (!Object.values(routes).includes(pathname)) {
      res.writeHead(404).end('Outside the proof preview');
      return;
    }
    const file = path.join(root, state, pathname, 'index.html');
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' });
    res.end(fs.readFileSync(file));
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  return { server, base: `http://127.0.0.1:${server.address().port}`, select: next => { state = next; } };
}

async function contextFor(browser, width, javaScriptEnabled = true, imageFailure = false) {
  const context = await browser.newContext({ viewport: { width, height: 900 }, javaScriptEnabled, serviceWorkers: 'block' });
  await context.route('**/*', route => {
    const request = route.request();
    const url = new URL(request.url());
    if (request.method() !== 'GET' || !allowedHosts.has(url.hostname)
        || (imageFailure && url.pathname.includes('kris-krug-north-house-show-and-tell-2026.jpg'))) {
      return route.abort();
    }
    return route.continue();
  });
  return context;
}

async function inspect(page, name, base) {
  await page.goto(base + routes[name], { waitUntil: 'domcontentloaded' });
  await page.waitForFunction(() => [...document.querySelectorAll('link[rel="stylesheet"]')].every(link => link.sheet || link.media === 'print'));
  // Expose existing lazy proof images in both states before comparing asset errors.
  if (name === 'services') {
    await page.locator('.kk-services-proof-grid').scrollIntoViewIfNeeded();
    await page.evaluate(() => Promise.all([...document.querySelectorAll('.kk-services-proof-grid img')].map(img => img.decode().catch(() => {}))));
  }
  const target = page.locator(name === 'events' ? eventCard : name === 'recap' ? '#north-house-next-step' : '#north-house-workflow');
  if (await target.count()) await target.scrollIntoViewIfNeeded();
  await page.evaluate(async () => {
    const images = [...document.querySelectorAll('#north-house-workflow img, [data-event-id="league-innovators-north-house-ai-show-tell-2026"] img')];
    await Promise.race([Promise.all(images.map(img => img.decode().catch(() => {}))), new Promise(resolve => setTimeout(resolve, 10000))]);
  });
  await page.waitForFunction(() => document.fonts.status === 'loaded');
  await page.waitForFunction(() => [...document.querySelectorAll('#north-house-workflow img')].every(img => {
    if (!img.naturalWidth) return true;
    const style = getComputedStyle(img);
    return style.opacity === '1' && ['none', 'blur(0px)'].includes(style.filter);
  }));
  return page.evaluate(() => ({
    width: innerWidth,
    overflow: document.documentElement.scrollWidth - innerWidth,
    h1s: document.querySelectorAll('h1').length,
    proof: document.querySelector('#north-house-workflow')?.innerText,
    photo: [...document.querySelectorAll('#north-house-workflow img')].map(img => ({ loaded: img.naturalWidth > 0, alt: img.alt, ratio: img.naturalWidth / img.naturalHeight })),
  }));
}

async function tabTo(page, selector) {
  for (let n = 0; n < 120; n++) {
    await page.keyboard.press('Tab');
    if (await page.locator(selector).evaluate(el => el === document.activeElement)) {
      const focus = await page.locator(selector).evaluate(el => {
        const style = getComputedStyle(el);
        return { outline: style.outlineStyle, width: style.outlineWidth, shadow: style.boxShadow };
      });
      assert((focus.outline !== 'none' && parseFloat(focus.width) > 0) || focus.shadow !== 'none', 'Visible keyboard focus');
      return { tabs: n + 1, focus };
    }
  }
  throw new Error(`Keyboard cannot reach ${selector}`);
}

async function main() {
  const browser = await chromium.launch({ headless: true });
  const preview = await serve();
  try {
    for (const state of ['baseline', 'candidate']) {
      preview.select(state);
      for (const width of [1280, 768, 390]) {
        const context = await contextFor(browser, width);
        try {
          const page = await context.newPage();
          let errors = [];
          page.on('pageerror', error => errors.push(error.message));
          page.on('console', message => { if (message.type() === 'error') errors.push(`${message.text()} [${message.location().url}]`); });
          for (const name of ['events', 'recap', 'services']) {
            errors = [];
            const metrics = await inspect(page, name, preview.base);
            report.runs.push({ state, width, name, ...metrics, consoleErrors: [...new Set(errors)] });
            assert(metrics.overflow <= 1, `${state} ${name} ${width}: horizontal overflow`);
            assert.equal(metrics.h1s, 1);
            if (state === 'candidate' && name === 'services') {
              assert(metrics.photo[0].loaded, 'Proof photo loads');
              assert.equal(metrics.photo[0].ratio, 0.75, 'Original portrait is not cropped');
              await page.locator('#north-house-workflow').screenshot({ path: path.join(evidence, `services-${width}.png`) });
            }
            if (state === 'candidate' && name === 'events' && width === 390) {
              await page.locator(eventCard).screenshot({ path: path.join(evidence, 'events-390.png') });
            }
            if (state === 'candidate' && name === 'recap' && width === 390) {
              await page.locator('#north-house-next-step').screenshot({ path: path.join(evidence, 'recap-390.png') });
            }
          }
        } finally { await context.close(); }
      }
    }
    for (const javaScriptEnabled of [true, false]) {
      const context = await contextFor(browser, 390, javaScriptEnabled);
      try {
        const page = await context.newPage();
        await page.goto(preview.base + routes.events, { waitUntil: 'domcontentloaded' });
        const steps = [];
        steps.push(await tabTo(page, `${eventCard} .aurora-event-compact-link`));
        await page.keyboard.press('Enter');
        await page.waitForURL('**' + routes.recap, { waitUntil: 'domcontentloaded' });
        steps.push(await tabTo(page, '#north-house-next-step a'));
        await page.keyboard.press('Enter');
        await page.waitForURL('**' + routes.services + '#north-house-workflow', { waitUntil: 'domcontentloaded' });
        assert(await page.locator('#north-house-workflow').isVisible());
        steps.push(await tabTo(page, '#north-house-workflow .kk-services-button'));
        await page.keyboard.press('Enter');
        await page.waitForURL('**' + routes.contact, { waitUntil: 'domcontentloaded' });
        assert(await page.locator('a[href^="mailto:"]').count(), 'Existing email enquiry is present; never send it');
        report.journey.push({ javaScriptEnabled, complete: true, steps });
      } finally { await context.close(); }
    }
    const fallback = await contextFor(browser, 390, true, true);
    try {
      const page = await fallback.newPage();
      const metrics = await inspect(page, 'services', preview.base);
      assert(!metrics.photo[0].loaded && metrics.photo[0].alt);
      assert(await page.locator('#north-house-workflow .kk-services-button').isVisible());
      assert(metrics.overflow <= 1);
      report.imageFallback = { copyAndEnquiryVisible: true, altPresent: true };
    } finally { await fallback.close(); }
    report.newConsoleErrors = report.runs.filter(run => run.state === 'candidate').flatMap(run => {
      const baseline = report.runs.find(b => b.state === 'baseline' && b.width === run.width && b.name === run.name);
      return run.consoleErrors.filter(error => !baseline.consoleErrors.includes(error)).map(error => ({ route: run.name, width: run.width, error }));
    });
    assert.equal(report.newConsoleErrors.length, 0, 'No new console errors relative to baseline');
  } finally {
    fs.writeFileSync(path.join(evidence, 'browser-report.json'), JSON.stringify(report, null, 2), { mode: 0o600 });
    await browser.close();
    await new Promise(resolve => preview.server.close(resolve));
  }
  console.log(JSON.stringify({ renderChecks: report.runs.length, journeys: report.journey, imageFallback: report.imageFallback, newConsoleErrors: report.newConsoleErrors, evidence }, null, 2));
}

main().catch(error => { console.error(error); process.exitCode = 1; });
