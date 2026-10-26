/* Candidate for a GTM Custom HTML tag triggered only by Beehiiv's signedUp event. */
(function () {
  "use strict";

  if (window.location.hostname !== "vancouver.beehiiv.com" ||
      !/^\/(subscribe\/?)?$/.test(window.location.pathname) ||
      window.__kkKrugSignupRecorded) return;

  // Beehiiv gates GTM on data-processing consent; GA additionally needs marketing consent.
  var match = document.cookie.match(/(?:^|;\s*)beehiiv_honey=([^;]*)/);
  var consent;
  try {
    consent = match && JSON.parse(decodeURIComponent(match[1]));
  } catch (_) {
    return;
  }
  if (!consent || consent.marketing !== true || consent.dataProcessing !== true) return;

  var referrer = "";
  try {
    var source = new URL(document.referrer);
    if (source.protocol === "https:" || source.protocol === "http:") referrer = source.origin + "/";
  } catch (_) {
    // Direct visits have no referrer.
  }

  var measurementId = "G-ZPQP315FNS";
  var pageLocation = "https://vancouver.beehiiv.com" + window.location.pathname;
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }

  window.__kkKrugSignupRecorded = true;
  gtag("consent", "default", {
    analytics_storage: "granted",
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied"
  });
  gtag("js", new Date());
  gtag("config", measurementId, {
    send_page_view: false,
    allow_google_signals: false,
    allow_ad_personalization_signals: false,
    page_location: pageLocation,
    page_referrer: referrer,
    page_title: "KRÜG newsletter signup"
  });
  gtag("event", "krug_newsletter_signup", {
    send_to: measurementId,
    signal: "beehiiv_signed_up",
    publication: "krug",
    page_location: pageLocation,
    page_referrer: referrer,
    page_title: "KRÜG newsletter signup"
  });

  var script = document.createElement("script");
  script.async = true;
  script.src = "https://www.googletagmanager.com/gtag/js?id=" + measurementId;
  document.head.appendChild(script);
})();
