#!/usr/bin/env node

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const snippetPath = path.resolve(__dirname, '../../fixes/issue-706-script-diet-snippet.php');
const snippet = fs.readFileSync(snippetPath, 'utf8');
const match = snippet.match(/\$template = <<<'JS'\n([\s\S]*?)\nJS;/);

assert.ok(match, 'embedded gtag loader template must be present');

function renderedLoader() {
  return match[1]
    .replace('%1$s', JSON.stringify('https://www.googletagmanager.com/gtag/js?id=G-TEST'))
    .replace('%2$s', "w.gtag('config', 'G-TEST');");
}

function browser({ idleCallback = true } = {}) {
  const listeners = new Map();
  const timers = [];
  const idleCallbacks = [];
  const appended = [];

  function addEventListener(name, callback, options) {
    const entries = listeners.get(name) || [];
    entries.push({ callback, options });
    listeners.set(name, entries);
  }

  function removeEventListener(name, callback) {
    const entries = listeners.get(name) || [];
    listeners.set(
      name,
      entries.filter((entry) => entry.callback !== callback),
    );
  }

  const window = {
    addEventListener,
    removeEventListener,
    setTimeout(callback, delay) {
      timers.push({ callback, delay, cancelled: false });
      return timers.length;
    },
    clearTimeout(id) {
      if (timers[id - 1]) timers[id - 1].cancelled = true;
    },
  };

  if (idleCallback) {
    window.requestIdleCallback = (callback, options) => {
      idleCallbacks.push({ callback, options, cancelled: false });
      return idleCallbacks.length;
    };
    window.cancelIdleCallback = (id) => {
      if (idleCallbacks[id - 1]) idleCallbacks[id - 1].cancelled = true;
    };
  }

  const document = {
    readyState: 'loading',
    head: {
      appendChild(element) {
        appended.push(element);
      },
    },
    createElement(tagName) {
      return { tagName };
    },
  };

  function trigger(name) {
    const entries = [...(listeners.get(name) || [])];
    for (const entry of entries) {
      entry.callback();
      if (entry.options && entry.options.once) {
        removeEventListener(name, entry.callback);
      }
    }
  }

  vm.runInNewContext(renderedLoader(), { document, window });
  return { appended, document, idleCallbacks, listeners, timers, trigger, window };
}

{
  const page = browser();
  assert.equal(page.appended.length, 0, 'gtag must not load during parse');
  page.window.gtag('event', 'queued-before-boot');
  assert.equal(page.window.dataLayer.length, 1, 'early gtag calls must queue');

  page.trigger('load');
  assert.equal(page.appended.length, 0, 'load alone must not boot gtag');
  assert.equal(page.idleCallbacks.length, 0, 'idle must not be requested before the delay');
  assert.equal(page.timers.length, 1, 'load must start one delay timer');
  assert.equal(page.timers[0].delay, 3000, 'delay contract is three seconds after load');

  page.timers[0].callback();
  assert.equal(page.appended.length, 0, 'the delayed path waits for an idle callback');
  assert.equal(page.idleCallbacks.length, 1, 'idle is requested after the delay');
  assert.equal(page.idleCallbacks[0].options.timeout, 1000, 'idle wait has a one-second ceiling');

  page.idleCallbacks[0].callback();
  assert.equal(page.appended.length, 1, 'idle callback boots gtag once');
  assert.equal(page.appended[0].async, true, 'gtag script is async');
  assert.match(page.appended[0].src, /G-TEST$/, 'captured Site Kit src is preserved');
  assert.equal(page.window.dataLayer.length, 2, 'queued call and Site Kit config both survive');

  for (const event of ['pointerdown', 'keydown', 'touchstart', 'wheel']) {
    assert.equal((page.listeners.get(event) || []).length, 0, `${event} listener is removed`);
    page.trigger(event);
  }
  assert.equal(page.appended.length, 1, 'later events cannot append a duplicate script');
}

{
  const page = browser({ idleCallback: false });
  page.trigger('load');
  assert.equal(page.appended.length, 0, 'fallback also waits three seconds');
  assert.equal(page.timers[0].delay, 3000);
  page.timers[0].callback();
  assert.equal(page.appended.length, 1, 'fallback boots after the delay');
}

{
  const page = browser();
  page.trigger('pointerdown');
  page.trigger('keydown');
  assert.equal(page.appended.length, 1, 'first interaction boots exactly once');
}

console.log('issue-706 script diet harness: PASS');
