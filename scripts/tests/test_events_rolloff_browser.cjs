#!/usr/bin/env node
/**
 * In-process rolloff contract for the Events page script (#1100).
 *
 * Extracts the inline script from render_events_page.py and runs it against a
 * tiny DOM mock. No kriskrug.co fetch, no Playwright. Covers clock advance
 * while open, hidden-tab resume, and harmless repeated execution.
 */

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const rendererPath = path.resolve(
  __dirname,
  "../events_page/render_events_page.py",
);

function loadScriptSource() {
  const py = fs.readFileSync(rendererPath, "utf8");
  const match = py.match(/ROLLOFF_SCRIPT = """([\s\S]*?)""" %/);
  assert.ok(match, "could not find ROLLOFF_SCRIPT in render_events_page.py");
  assert.doesNotMatch(match[1], /&&/, "WordPress rewrites && into entities");
  assert.doesNotMatch(
    match[1].replace(/&amp;/g, ""),
    /&/,
    "bare ampersand in rolloff script",
  );
  return match[1]
    .replace("%(preview_rows)d", "4")
    .replace("%(next_up_limit)d", "4")
    .replace(/^\s*<script>/, "")
    .replace(/<\/script>\s*$/, "");
}

function el(tag, attrs, children) {
  const node = {
    tag,
    attrs: { ...attrs },
    children: children || [],
    hidden: false,
    textContent: "",
    classList: {
      toggle(name, on) {
        node._classes = node._classes || new Set();
        if (on) node._classes.add(name);
        else node._classes.delete(name);
      },
    },
    style: {
      setProperty() {},
    },
    addEventListener() {},
    getAttribute(name) {
      return Object.prototype.hasOwnProperty.call(node.attrs, name)
        ? node.attrs[name]
        : null;
    },
    setAttribute(name, value) {
      node.attrs[name] = String(value);
    },
    removeAttribute(name) {
      delete node.attrs[name];
    },
  };
  node.querySelector = (selector) => query(node, selector);
  node.querySelectorAll = (selector) => queryAll(node, selector);
  return node;
}

function matches(node, selector) {
  const cls = selector.match(/^\.([\w-]+)(?:\[([\w-]+)\])?$/);
  if (cls) return (node.attrs.class || "").split(" ").includes(cls[1]) &&
    (!cls[2] || Object.hasOwn(node.attrs, cls[2]));
  const count = selector.match(/^\[data-events-count="([^"]+)"\]$/);
  if (count) return node.attrs["data-events-count"] === count[1];
  if (selector === ".aurora-events-page") return node.tag === "page";
  if (selector === '[data-events-grid="sheet"]') {
    return node.attrs["data-events-grid"] === "sheet";
  }
  if (selector === "[data-events-sheet-toggle]") {
    return Object.prototype.hasOwnProperty.call(
      node.attrs,
      "data-events-sheet-toggle",
    );
  }
  if (selector === '[data-events-grid="upcoming"]') {
    return node.attrs["data-events-grid"] === "upcoming";
  }
  if (selector === '[data-events-bucket="upcoming"]') {
    return node.attrs["data-events-bucket"] === "upcoming";
  }
  if (selector === ".kk-ev-next[data-event-end]") {
    return (
      node.tag === "article" &&
      Object.prototype.hasOwnProperty.call(node.attrs, "data-event-end") &&
      (node.attrs.class || "").includes("kk-ev-next")
    );
  }
  if (selector === '.kk-ev-tile[data-tile-upcoming="true"]') {
    return (
      node.tag === "article" &&
      node.attrs["data-tile-upcoming"] === "true" &&
      (node.attrs.class || "").includes("kk-ev-tile")
    );
  }
  if (selector === "[data-event-end]") {
    return Object.prototype.hasOwnProperty.call(node.attrs, "data-event-end");
  }
  return false;
}

function descendants(root) {
  const out = [root];
  for (const child of root.children || []) {
    out.push(...descendants(child));
  }
  return out;
}

function queryAll(root, selector) {
  return descendants(root).filter((node) => matches(node, selector));
}

function query(root, selector) {
  return queryAll(root, selector)[0] || null;
}

function makeDom(nowMs) {
  const pastCard = el("article", {
    class: "kk-ev-next",
    "data-event-end": "2026-10-01T00:00:00-07:00",
    "data-event-id": "vancouver-ai-meetup-2026-09-30",
  });
  const futureCard = el("article", {
    class: "kk-ev-next",
    "data-event-end": "2026-10-31T00:00:00-07:00",
    "data-event-id": "futureproof-festival-2026",
  });
  const pastTile = el("article", {
    class: "kk-ev-tile",
    "data-event-end": "2026-10-01T00:00:00-07:00",
    "data-event-id": "vancouver-ai-meetup-2026-09-30",
    "data-tile-upcoming": "true",
  });
  const futureTile = el("article", {
    class: "kk-ev-tile",
    "data-event-end": "2026-10-31T00:00:00-07:00",
    "data-event-id": "futureproof-festival-2026",
    "data-tile-upcoming": "true",
  });
  const upcomingGrid = el("div", { "data-events-grid": "upcoming" }, [
    pastCard,
    futureCard,
  ]);
  const sheetGrid = el("div", { "data-events-grid": "sheet" }, [
    pastTile,
    futureTile,
  ]);
  const sheetToggle = el("button", { "data-events-sheet-toggle": "" });
  const upcomingBucket = el(
    "section",
    { "data-events-bucket": "upcoming", "data-events-empty": "false" },
    [upcomingGrid],
  );
  const pastRow = el("li", {class: "kk-ev-rec", "data-event-end": "2026-10-01T00:00:00-07:00", "data-event-edition": "33"});
  const futureRow = el("li", {class: "kk-ev-rec", "data-event-end": "2026-10-31T00:00:00-07:00"});
  const year = el("div", {class: "kk-ev-rec-year"}, [pastRow, futureRow]);
  const counts = Object.fromEntries(["rooms", "editions", "frames"].map(key => [key, el("b", {"data-events-count": key})]));
  const page = el("page", { class: "aurora-events-page" }, [
    upcomingBucket,
    sheetGrid,
    sheetToggle, year, ...Object.values(counts),
  ]);
  page.querySelector = (sel) => query(page, sel);
  page.querySelectorAll = (sel) => queryAll(page, sel);

  const listeners = { document: {}, window: {} };
  let visibility = "visible";
  const timeouts = [];

  const document = {
    readyState: "complete",
    visibilityState: visibility,
    documentElement: { clientWidth: 1280 },
    querySelector(sel) {
      return query(page, sel);
    },
    addEventListener(type, fn) {
      listeners.document[type] = listeners.document[type] || [];
      listeners.document[type].push(fn);
    },
  };
  Object.defineProperty(document, "visibilityState", {
    get() {
      return visibility;
    },
  });

  const windowObj = {
    addEventListener(type, fn) {
      listeners.window[type] = listeners.window[type] || [];
      listeners.window[type].push(fn);
    },
    getComputedStyle() {
      return { gridTemplateColumns: "1fr 1fr 1fr 1fr 1fr 1fr" };
    },
    setTimeout(fn, wait) {
      const id = timeouts.length + 1;
      timeouts.push({ id, fn, wait, now: nowMs });
      return id;
    },
    clearTimeout(id) {
      const idx = timeouts.findIndex((t) => t.id === id);
      if (idx >= 0) timeouts.splice(idx, 1);
    },
  };

  const context = {
    document,
    window: windowObj,
    Date: {
      now() {
        return nowMs;
      },
      parse: Date.parse,
    },
    Number,
    Array,
    Infinity,
    Boolean,
  };

  return {
    pastRow, futureRow, counts,
    pastCard,
    futureCard,
    pastTile,
    futureTile,
    upcomingBucket,
    timeouts,
    listeners,
    setNow(next) {
      nowMs = next;
    },
    setVisibility(next) {
      visibility = next;
      for (const fn of listeners.document.visibilitychange || []) fn();
    },
    fireTimeouts() {
      const due = timeouts.splice(0, timeouts.length);
      for (const item of due) item.fn();
    },
    run() {
      vm.runInNewContext(loadScriptSource(), context, {
        filename: "events-rolloff.js",
      });
    },
  };
}

function testPastCardHidesOnInitAndReleasesItsTile() {
  const audit = Date.parse("2026-10-17T09:57:00-07:00");
  const dom = makeDom(audit);
  dom.run();
  assert.equal(dom.pastCard.hidden, true);
  assert.equal(dom.futureCard.hidden, false);
  assert.equal(dom.pastRow.hidden, false);
  assert.equal(dom.futureRow.hidden, true);
  assert.equal(dom.counts.rooms.textContent, "1");
  assert.equal(dom.counts.editions.textContent, "1");
  assert.equal(dom.counts.frames.textContent, "1");
  assert.equal(dom.pastTile.getAttribute("data-tile-upcoming"), null);
  assert.equal(dom.futureTile.getAttribute("data-tile-upcoming"), "true");
  assert.equal(dom.upcomingBucket.getAttribute("data-events-empty"), "false");
}

function testClockAdvanceWhileOpenHidesTheFestival() {
  const before = Date.parse("2026-10-30T12:00:00-07:00");
  const dom = makeDom(before);
  dom.run();
  assert.equal(dom.futureCard.hidden, false);
  assert.equal(dom.timeouts.length, 1);
  dom.setNow(Date.parse("2026-10-31T00:00:00-07:00"));
  dom.fireTimeouts();
  assert.equal(dom.futureCard.hidden, true);
  assert.equal(dom.futureRow.hidden, false);
  assert.equal(dom.counts.rooms.textContent, "2");
  assert.equal(dom.counts.editions.textContent, "1");
  assert.equal(dom.counts.frames.textContent, "2");
  assert.equal(dom.futureTile.getAttribute("data-tile-upcoming"), null);
}

function testHiddenTabResumeRerunsRolloff() {
  const before = Date.parse("2026-10-30T12:00:00-07:00");
  const dom = makeDom(before);
  dom.run();
  assert.equal(dom.futureCard.hidden, false);
  dom.setNow(Date.parse("2026-10-31T00:01:00-07:00"));
  dom.setVisibility("hidden");
  assert.equal(dom.futureCard.hidden, false);
  dom.setVisibility("visible");
  assert.equal(dom.futureCard.hidden, true);
}

function testRepeatedRolloffIsHarmless() {
  const audit = Date.parse("2026-10-17T09:57:00-07:00");
  const dom = makeDom(audit);
  dom.run();
  dom.setVisibility("visible");
  dom.setVisibility("hidden");
  dom.setVisibility("visible");
  assert.equal(dom.pastCard.hidden, true);
  assert.equal(dom.futureCard.hidden, false);
  assert.equal(dom.pastTile.getAttribute("data-tile-upcoming"), null);
}

function main() {
  testPastCardHidesOnInitAndReleasesItsTile();
  testClockAdvanceWhileOpenHidesTheFestival();
  testHiddenTabResumeRerunsRolloff();
  testRepeatedRolloffIsHarmless();
  console.log("test_events_rolloff_browser.cjs: ok");
}

main();
