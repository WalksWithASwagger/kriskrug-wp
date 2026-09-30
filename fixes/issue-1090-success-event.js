/**
 * #1090 / #1103 candidate: fire one GA4 event on a verified success
 * signal only.
 *
 * NOT LIVE. Do not enqueue this file on kriskrug.co. It is a contract
 * helper for a future first-party thank-you page or same-origin form
 * success state. It does not listen for clicks, and it does not listen
 * for postMessage from Beehiiv or any other iframe.
 *
 * Allowed event names:
 *   - newsletter_submit          (newsletter candidate only)
 *   - speaking_inquiry_submit    (speaking inquiry candidate only)
 *
 * A conversion counts only when `signal` is `confirmed_submit` or
 * `thank_you_state` and a distinct `submissionId` is supplied. Click,
 * outbound navigation, mailto, validation failure, and submit error
 * are rejected.
 *
 * Dedup: the same eventName + submissionId pair fires once for the
 * lifetime of this page. A later distinct submissionId may fire again.
 * Loading the file twice reuses the same map; it does not attach
 * listeners, because there are none.
 */
(function (root) {
  "use strict";

  var ALLOWED_EVENTS = {
    newsletter_submit: true,
    speaking_inquiry_submit: true,
  };

  var ALLOWED_SIGNALS = {
    confirmed_submit: true,
    thank_you_state: true,
  };

  if (!root.__kkVerifiedConversionState) {
    root.__kkVerifiedConversionState = { fired: Object.create(null) };
  }

  function recordVerifiedConversion(detail) {
    var payload = detail || {};
    var eventName = payload.eventName;
    var signal = payload.signal;
    var submissionId = payload.submissionId == null ? "" : String(payload.submissionId);

    if (!ALLOWED_EVENTS[eventName]) {
      return { fired: false, reason: "event_name" };
    }
    if (!ALLOWED_SIGNALS[signal]) {
      return { fired: false, reason: "signal" };
    }
    if (!submissionId) {
      return { fired: false, reason: "submission_id" };
    }

    var key = eventName + ":" + submissionId;
    if (root.__kkVerifiedConversionState.fired[key]) {
      return { fired: false, reason: "duplicate" };
    }

    if (typeof root.gtag !== "function") {
      return { fired: false, reason: "gtag_missing" };
    }

    root.gtag("event", eventName, {
      transport_type: "beacon",
    });
    root.__kkVerifiedConversionState.fired[key] = true;
    return { fired: true, reason: "ok" };
  }

  root.kkRecordVerifiedConversion = recordVerifiedConversion;

  if (typeof module !== "undefined" && module.exports) {
    module.exports = {
      recordVerifiedConversion: recordVerifiedConversion,
      ALLOWED_EVENTS: ALLOWED_EVENTS,
      ALLOWED_SIGNALS: ALLOWED_SIGNALS,
    };
  }
})(typeof globalThis !== "undefined" ? globalThis : this);
