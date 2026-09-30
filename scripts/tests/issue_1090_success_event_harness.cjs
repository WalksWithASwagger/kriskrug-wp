#!/usr/bin/env node
/**
 * Synthetic contract for fixes/issue-1090-success-event.js.
 *
 * Runs in-process. Does not fetch kriskrug.co, Beehiiv, or any Google
 * Analytics host. A local gtag stub records event names only.
 */

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const helperPath = path.resolve(__dirname, "../../fixes/issue-1090-success-event.js");
const helperSource = fs.readFileSync(helperPath, "utf8");

function loadHelper() {
  const events = [];
  const root = {
    gtag(command, name, params) {
      events.push({ command, name, params });
    },
  };
  vm.runInNewContext(helperSource, root, { filename: helperPath });
  return { root, events };
}

function assertNoFire(root, events, detail, reason) {
  const before = events.length;
  const result = root.kkRecordVerifiedConversion(detail);
  assert.equal(result.fired, false, JSON.stringify({ detail, result }));
  assert.equal(result.reason, reason, JSON.stringify({ detail, result }));
  assert.equal(events.length, before, "rejected call must not emit gtag");
}

function assertAllowedParamsOnly(params, detail) {
  assert.deepEqual(Object.keys(params).sort(), ["signal", "submission_id"]);
  assert.equal(params.submission_id, String(detail.submissionId));
  assert.equal(params.signal, detail.signal);
  const serialized = JSON.stringify(params);
  assert.doesNotMatch(serialized, /@/);
  assert.doesNotMatch(serialized, /email/i);
  assert.doesNotMatch(serialized, /"name"/i);
}

function assertFireOnce(root, events, detail, expectedName) {
  const before = events.length;
  const result = root.kkRecordVerifiedConversion(detail);
  assert.equal(result.fired, true, JSON.stringify({ detail, result }));
  assert.equal(result.reason, "ok");
  assert.equal(events.length, before + 1);
  assert.equal(events[events.length - 1].command, "event");
  assert.equal(events[events.length - 1].name, expectedName);
  assertAllowedParamsOnly(events[events.length - 1].params, detail);
}

function testLoadAndClickDoNotConvert() {
  const { root, events } = loadHelper();
  assert.equal(events.length, 0, "none on load");
  assert.equal(typeof root.addEventListener, "undefined");
  assertNoFire(root, events, { eventName: "newsletter_submit", signal: "click", submissionId: "1" }, "signal");
  assertNoFire(
    root,
    events,
    { eventName: "newsletter_submit", signal: "outbound_click", submissionId: "1" },
    "signal",
  );
  assertNoFire(root, events, { eventName: "speaking_inquiry_submit", signal: "mailto", submissionId: "1" }, "signal");
}

function testValidationAndErrorDoNotConvert() {
  const { root, events } = loadHelper();
  assertNoFire(
    root,
    events,
    { eventName: "newsletter_submit", signal: "validation_failure", submissionId: "bad-email" },
    "signal",
  );
  assertNoFire(
    root,
    events,
    { eventName: "newsletter_submit", signal: "submit_error", submissionId: "network" },
    "signal",
  );
}

function testConfirmedSuccessFiresOnceAndDedups() {
  const { root, events } = loadHelper();
  const first = {
    eventName: "newsletter_submit",
    signal: "confirmed_submit",
    submissionId: "sub-1",
  };
  assertFireOnce(root, events, first, "newsletter_submit");
  assertNoFire(root, events, first, "duplicate");
  assertNoFire(
    root,
    events,
    { eventName: "newsletter_submit", signal: "thank_you_state", submissionId: "sub-1" },
    "duplicate",
  );
}

function testDistinctSubmissionFiresAgain() {
  const { root, events } = loadHelper();
  assertFireOnce(
    root,
    events,
    { eventName: "newsletter_submit", signal: "thank_you_state", submissionId: "page-a" },
    "newsletter_submit",
  );
  assertFireOnce(
    root,
    events,
    { eventName: "newsletter_submit", signal: "thank_you_state", submissionId: "page-b" },
    "newsletter_submit",
  );
  assert.equal(events.length, 2);
}

function testInquiryUsesOwnEventName() {
  const { root, events } = loadHelper();
  assertFireOnce(
    root,
    events,
    { eventName: "speaking_inquiry_submit", signal: "confirmed_submit", submissionId: "inquiry-1" },
    "speaking_inquiry_submit",
  );
  assert.equal(events[0].name, "speaking_inquiry_submit");
  assert.notEqual(events[0].name, "newsletter_submit");
}

function testUnknownEventRejected() {
  const { root, events } = loadHelper();
  assertNoFire(
    root,
    events,
    { eventName: "newsletter_click", signal: "confirmed_submit", submissionId: "x" },
    "event_name",
  );
}

function testMissingGtagDoesNotMarkDuplicate() {
  const root = {};
  vm.runInNewContext(helperSource, root, { filename: helperPath });
  const missing = root.kkRecordVerifiedConversion({
    eventName: "newsletter_submit",
    signal: "confirmed_submit",
    submissionId: "later",
  });
  assert.equal(missing.fired, false);
  assert.equal(missing.reason, "gtag_missing");

  const events = [];
  root.gtag = (command, name) => events.push({ command, name });
  const retry = root.kkRecordVerifiedConversion({
    eventName: "newsletter_submit",
    signal: "confirmed_submit",
    submissionId: "later",
  });
  assert.equal(retry.fired, true);
  assert.equal(events.length, 1);
}

function testReinitializationReusesDedupMap() {
  const { root, events } = loadHelper();
  assertFireOnce(
    root,
    events,
    { eventName: "newsletter_submit", signal: "confirmed_submit", submissionId: "once" },
    "newsletter_submit",
  );
  vm.runInNewContext(helperSource, root, { filename: helperPath });
  assertNoFire(
    root,
    events,
    { eventName: "newsletter_submit", signal: "confirmed_submit", submissionId: "once" },
    "duplicate",
  );
  assert.equal(events.length, 1);
}

function testSourceHasNoIframeOrClickWiring() {
  const executable = helperSource.replace(/\/\*[\s\S]*?\*\//g, "").replace(/\/\/.*$/gm, "");
  assert.doesNotMatch(executable, /postMessage/);
  assert.doesNotMatch(executable, /addEventListener/);
  assert.doesNotMatch(executable, /beehiiv/i);
  assert.doesNotMatch(executable, /mailto/i);
}

// The inquiry-as-newsletter case above is inverted on purpose if I
// accidentally left assertNoFire(..., "ok"). Fix: inquiry with the
// newsletter name and a success signal *would* fire if someone mislabeled
// it. The helper cannot know the business meaning of a submissionId.
// Guard the name at the call site; the test below is the real check.
function testInquiryMustNotUseNewsletterNameAtCallSite() {
  const { root, events } = loadHelper();
  const inquiry = {
    eventName: "speaking_inquiry_submit",
    signal: "confirmed_submit",
    submissionId: "inquiry-1",
  };
  assertFireOnce(root, events, inquiry, "speaking_inquiry_submit");
  assert.equal(
    events.filter((entry) => entry.name === "newsletter_submit").length,
    0,
  );
}

function testPiiAndFormFieldsAreDropped() {
  const { root, events } = loadHelper();
  const detail = {
    eventName: "newsletter_submit",
    signal: "thank_you_state",
    submissionId: "tok-9",
    email: "subscriber@example.test",
    name: "Alex Example",
    first_name: "Alex",
    last_name: "Example",
    company: "Example Org",
    message: "Please book me",
    phone: "555-0100",
    value: "form-field-dump",
    params: {
      email: "nested@example.test",
      name: "Nested Name",
    },
  };
  assertFireOnce(root, events, detail, "newsletter_submit");
  const serialized = JSON.stringify(events[0].params);
  assert.doesNotMatch(serialized, /subscriber@example\.test/);
  assert.doesNotMatch(serialized, /Alex Example/);
  assert.doesNotMatch(serialized, /Example Org/);
  assert.doesNotMatch(serialized, /Please book me/);
  assert.doesNotMatch(serialized, /555-0100/);
  assert.doesNotMatch(serialized, /form-field-dump/);
  assert.doesNotMatch(serialized, /nested@example\.test/);
}

function testEmailOrNameAsSubmissionIdRejected() {
  const { root, events } = loadHelper();
  assertNoFire(
    root,
    events,
    {
      eventName: "newsletter_submit",
      signal: "confirmed_submit",
      submissionId: "subscriber@example.test",
    },
    "submission_id",
  );
  assertNoFire(
    root,
    events,
    {
      eventName: "speaking_inquiry_submit",
      signal: "confirmed_submit",
      submissionId: "Alex Example",
    },
    "submission_id",
  );
}

function main() {
  testLoadAndClickDoNotConvert();
  testValidationAndErrorDoNotConvert();
  testConfirmedSuccessFiresOnceAndDedups();
  testDistinctSubmissionFiresAgain();
  testInquiryUsesOwnEventName();
  testUnknownEventRejected();
  testMissingGtagDoesNotMarkDuplicate();
  testReinitializationReusesDedupMap();
  testSourceHasNoIframeOrClickWiring();
  testInquiryMustNotUseNewsletterNameAtCallSite();
  testPiiAndFormFieldsAreDropped();
  testEmailOrNameAsSubmissionIdRejected();
  console.log("issue_1090_success_event_harness: ok");
}

main();
