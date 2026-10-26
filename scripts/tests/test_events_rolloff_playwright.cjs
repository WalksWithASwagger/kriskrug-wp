#!/usr/bin/env node
/** Real Chromium regression for the WordPress-filtered Events rollover script. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');

const source = fs.readFileSync(path.join(__dirname, '../events_page/render_events_page.py'), 'utf8');
const css = source.match(/PAGE_SCOPED_CSS = """([\s\S]*?)"""/)[1];
const script = source.match(/ROLLOFF_SCRIPT = """([\s\S]*?)""" %/)[1]
  .replace('%(preview_rows)d', '4').replace('%(next_up_limit)d', '4')
  .replace(/&/g, '&#038;');
const cutoffs = ['2026-10-31T00:00:00-07:00', '2026-11-01T00:00:00-07:00',
  '2026-11-02T00:00:00-08:00', '2026-11-03T00:00:00-08:00',
  '2027-01-02T00:00:00-08:00', '2027-02-02T00:00:00-08:00'];
const past = Array.from({length: 30}, (_, index) => ({id: `p${index}`, end: '2026-09-01T00:00:00-07:00', edition: index === 0}));
const future = cutoffs.map((end, index) => ({id: `f${index}`, end, edition: index === 0}));
const attrs = row => `data-event-id="${row.id}" data-event-end="${row.end}"`;
const record = (row, hidden = false) => `<li class="kk-ev-rec" ${attrs(row)}${row.edition ? ' data-event-edition="1"' : ''}${hidden ? ' hidden' : ''}><span class="kk-ev-rec-date">Date</span><span class="kk-ev-rec-title">Event ${row.id}</span></li>`;
const tile = (row, upcoming = false) => `<article class="kk-ev-tile" ${attrs(row)}${upcoming ? ' data-tile-upcoming="true"' : ''}><span>Frame ${row.id}</span></article>`;
const fixture = `<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">${css}</head><body><main class="aurora-events-page">
<section class="kk-ev-upcoming" data-events-bucket="upcoming" data-events-empty="false"><h2>Next up</h2><ul class="kk-ev-stats">${['rooms','editions','frames'].map(key => `<li><b data-events-count="${key}">0</b><span>${key}</span></li>`).join('')}</ul><div data-events-grid="upcoming">${future.map((row, index) => `<article class="kk-ev-next" ${attrs(row)}${index >= 4 ? ' hidden' : ''}>Future ${row.id}</article>`).join('')}</div></section>
<section class="kk-ev-sheet"><div class="kk-ev-sheet-grid" data-events-grid="sheet">${past.map(row => tile(row)).join('')}${future.map(row => tile(row, true)).join('')}</div><button class="kk-ev-sheet-toggle" data-events-sheet-toggle aria-expanded="false">Show all frames</button></section>
<section class="kk-ev-record"><div class="kk-ev-rec-year"><h3>2026</h3><ul>${past.map(row => record(row)).join('')}${record({id:'bare',end:'2026-09-01T00:00:00-07:00'})}${future.slice(0,4).map(row => record(row,true)).join('')}</ul></div><div class="kk-ev-rec-year" hidden><h3>2027</h3><ul>${future.slice(4).map(row => record(row,true)).join('')}</ul></div><span data-events-count="rooms">0</span> rooms</section>
${script}</main></body></html>`;

async function assertCounts(page, rooms, editions, frames) {
  for (const [key,value] of Object.entries({rooms,editions,frames})) {
    const values = await page.locator(`[data-events-count="${key}"]`).allTextContents();
    assert(values.length > 0);
    assert(values.every(text => text === String(value)), `${key}: ${values}`);
  }
  assert.equal(await page.locator('.kk-ev-rec:visible').count(), rooms);
}

async function resume(page, time) {
  await page.clock.setSystemTime(new Date(time));
  await page.evaluate(() => document.dispatchEvent(new Event('visibilitychange')));
}

(async () => {
  const browser = await chromium.launch({headless:true, ...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE ? {executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE} : {})});
  const report = [];
  try {
    for (const width of [1440,390]) {
      const context = await browser.newContext({viewport:{width,height:1000}, serviceWorkers:'block'});
      await context.route('**/*', route => route.request().url() === 'http://events.test/'
        ? route.fulfill({contentType:'text/html',body:fixture}) : route.abort());
      const page = await context.newPage();
      const errors = []; page.on('pageerror', error => errors.push(error.message));
      await page.clock.install({time:new Date('2026-10-31T06:59:59Z')});
      await page.goto('http://events.test/');
      await assertCounts(page,31,1,30);
      assert.equal(await page.locator('.kk-ev-next:visible').count(),4);
      assert.equal(await page.locator('.kk-ev-rec-year:visible').count(),1);
      const toggle = page.locator('[data-events-sheet-toggle]');
      await toggle.focus(); await page.keyboard.press('Enter');
      assert.equal(await toggle.getAttribute('aria-expanded'),'true');
      assert.equal(await page.locator('.kk-ev-tile:visible').count(),30);
      await page.keyboard.press('Space');
      assert.equal(await toggle.getAttribute('aria-expanded'),'false');
      assert.equal(await page.locator('.kk-ev-tile:visible').count(),width === 390 ? 8 : 24);
      await page.clock.fastForward(1000);
      await assertCounts(page,32,2,31);
      assert.equal(await page.locator('.kk-ev-next[data-event-id="f0"]').isVisible(),false);
      assert.equal(await page.locator('.kk-ev-next[data-event-id="f4"]').isVisible(),true);
      assert.equal(await page.locator('.kk-ev-next:visible').count(),4);
      // A reload at the same clock must derive the same record and counts.
      await page.reload(); await assertCounts(page,32,2,31);
      await page.evaluate(() => Object.defineProperty(document,'visibilityState',{configurable:true,value:'hidden'}));
      await resume(page,'2026-11-02T08:00:00Z');
      await assertCounts(page,32,2,31);
      await page.evaluate(() => Object.defineProperty(document,'visibilityState',{configurable:true,value:'visible'}));
      await resume(page,'2026-11-02T08:00:00Z');
      await assertCounts(page,34,2,33);
      await resume(page,'2026-11-02T08:00:00Z');
      await assertCounts(page,34,2,33);
      await resume(page,'2027-03-01T08:00:00Z');
      await assertCounts(page,37,2,36);
      assert.equal(await page.locator('.kk-ev-next:visible').count(),0);
      assert.equal(await page.locator('.kk-ev-rec-year:visible').count(),2);
      assert.equal(await page.locator('.kk-ev-stats').isVisible(),true);
      assert.equal(errors.length,0,errors.join('\n'));
      report.push({width,clockRollover:true,reload:true,visibilityResume:true,promotionBeyondFour:true,keyboardSheetToggle:true,zeroUpcomingCounters:true,errors});
      await context.close();
    }
  } finally { await browser.close(); }
  console.log(JSON.stringify(report,null,2));
})().catch(error => {console.error(error); process.exitCode = 1;});
