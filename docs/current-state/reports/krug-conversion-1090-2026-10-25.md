# KRÜG completed-signup conversion — October 25, 2026

Refs #1090. Kris selected **completed personal KRÜG newsletter signups**, excluding
link clicks, and authorized implementation and shipping. This supersedes the
September conversion-choice and GA4-save handoff. Kris subsequently approved the
personal GTM account and Google Tag Manager terms, then explicitly approved the
additional Data Processing Terms. No production test signup was submitted.

## Applied and verified

- Existing account **Kris Krüg** `137499310`, property **KK.co - GA4** `311967290`.
- Created key event **`krug_newsletter_signup`**, **Once per event**, **no default
  monetary value**, using Create with code. Fresh readback showed it starred with
  no stream data. No click/page-view derived event was created.
- Created stream **KRÜG newsletter — completed signups**, ID `16202914769`,
  measurement ID **`G-ZPQP315FNS`**, URL `https://vancouver.beehiiv.com`.
  Independent readback confirms enhanced measurement **off**, email redaction
  **active**, zero connected tags and no data received. The six existing streams
  were not changed. The optional Google-tag setup panel reported no permission;
  the stream configuration itself saved and was independently read back.
- **The collection installation is live.** Personal GTM account `6399923946`,
  container `283573969` / **`GTM-MGD93937`**, published **version 2**. The native
  Beehiiv Cookie Banner is enabled and its GTM pixel contains this container ID.
  Both persisted after reload. Keep #1090 open until organic delivery is observed.
- Public `/subscribe` readback showed no GTM script before consent, then exactly
  the new container after acceptance. The GA4 loader remained absent. Live Tag
  Assistant connected to this container and showed **Tags Fired: None** and the
  signup tag under **Tags Not Fired** on page load.

Varlock doctor passed with warnings for preserved unrelated local files. The
initial managed-worktree public status check passed WordPress smoke; its draft
counts were unavailable because that invocation did not inherit credentials. A
fresh original-checkout status run resolved all sources through the existing
runtime; its only smoke failure was the stale declared WordPress version (expected
7.0.5, observed 7.0.7). The Beehiiv
connector supplied publication/settings readback; browser admin was needed because
it cannot edit live legacy pixels. Existing sign-ins were used, with no credential
values displayed or copied.

## Provider contract and boundaries

Personal publication `pub_4a933c7c-085f-4794-a0d8-6649f2e78f3a` is KRÜG at
`vancouver.beehiiv.com`. Its live builder is legacy. Double opt-in and subscriber
approval are off. Before deployment all six legacy pixel fields were empty and
Cookie Banner was off. Deployment changed only Cookie Banner and the GTM field;
the native GA4 and other pixel fields remain empty.

[Beehiiv documents the case-sensitive `signedUp` custom event](https://www.beehiiv.com/support/article/14493016863127-how-to-set-up-subscriber-sign-up-tracking-for-ig-and-fb-for-a-legacy-website).
The public October 22 bundles `CreateAction-BGxfy4WK.js` and `types-B-nLKI8t.js`
push `dataLayerEvent` from the `/create` response, not the button handler. The
server decides which response contains `signedUp`; duplicate-email and actual
delivery behavior have not been production-tested.

Provider redirects can include an email query parameter. The candidate strips all
query strings/fragments, reduces referrers to their origin, and never forwards
provider event properties, email, name, subscriber ID, form fields or monetary
value. The isolated stream disables enhanced measurement; the tag also sets
`send_page_view: false` and disables advertising signals.

## Deployed tag

- [Tag source](../../../fixes/issue-1090-krug-signup-tag.js) and
  [GTM import](../../../fixes/issue-1090-krug-signup-gtm.json).
- Exact `signedUp` event on `vancouver.beehiiv.com`; runtime limited to current
  hosted signup routes `/` and `/subscribe[/]`.
- Once per page load, with a second runtime guard for duplicate evaluation.
  Two different people subscribing within one loaded page would count once. This
  is conservative deduplication, not a persistent subscriber-ID deduplicator.
- Both `marketing` and `dataProcessing` consent must explicitly be true. Missing,
  denied or malformed consent emits nothing. Beehiiv's native Cookie Banner was
  enabled before installing GTM; its native GA4 pixel field remains empty.
- Offline harness is included in `make javascript-syntax`. It executes the actual
  source with network-free stubs and the exported trigger. Coverage includes page
  load, clicks, submit/error events, wrong host/path/event, consent denial,
  duplicate callbacks and PII exclusion. No production signup or synthetic
  Analytics event was sent.
- Google accepted the import with **2 additions, 0 modifications, 0 deletions**
  using Merge into the new empty workspace. Default built-in variables were
  preserved. Version 2 is published; the current workspace has zero changes.
- Live Preview confirms connection and no conversion on load. An actual Beehiiv
  signup reaching GA4 remains unverified; no synthetic event was sent to Google.

The [local browser fixture](../../../scripts/tests/issue_1090_collect_fixture.html)
also ran the actual Google tag downloaded for `G-ZPQP315FNS`, served locally.
CSP blocked external connections, images and frames; fetch, beacon and image
transports were captured locally. Results: no requests on load/click/error; one
GA4 `/g/collect` request with `en=krug_newsletter_signup` on provider success;
repeated callbacks added none; denied consent loaded no tag and emitted nothing.
Starting the fixture with an email query and fragment leaked neither into any
captured request. The Google SDK also produced one separate cookieless
consent-mode ping to `pagead2.googlesyndication.com`; it is not a second GA4
conversion. Both payloads were checked for fixture PII. Nothing reached Google.

To reproduce, copy the fixture into an ignored local directory as
`collect-fixture.html`, download the public measurement-ID tag as `gtag-krug.js`,
and write `tag-wrapper.js` as `window.runTag=function(window,document){` followed by
the exact candidate source and `};`. Serve only that directory on `127.0.0.1`.
Use the visible controls, inspecting GA4 requests separately from consent pings.
The fixture uses synthetic provider callbacks; it does not test Beehiiv's server.

## Activation verification

Account **KRÜG**, country **Canada**, container **vancouver.beehiiv.com**, platform
**Web**, optional data sharing off. The unrelated BC + AI invitation was untouched.
The initial DPA action was rejected by automatic approval review because that
additional agreement had not been explicitly approved. Kris then approved it;
account creation succeeded. Both approval receipts are in the chat.

Published version 2 is named **KRÜG completed signup — #1090**. Google compiled the
same tag and exact `signedUp`/hostname trigger from PR #1147. A second isolated
fixture exercised the **published GTM container**, including its event queue and
compiled Custom HTML, with the real Google SDK. Only the three personal-hostname
occurrences were replaced with `127.0.0.1` in the local test copy; production code
was unchanged. All outgoing fetch/beacon/image traffic was captured and CSP
blocked external connections. This addresses the command-ordering warning GTM
shows for `gtag` in Custom HTML in the tested single-tag container; it does not
prove future integrations will preserve that ordering.

Results: no requests on load/click/error; one GA4 signup request on `signedUp`;
repeated callbacks and an email-bearing redirect added none; denied consent
produced zero requests. The separate consent-mode ping was present, as in the
standalone test. Neither payload contained the fixture email, name, form fields,
query string or fragment. No production signup or synthetic GA event was sent.

Public browser readback and connected Tag Assistant confirm installation. Direct
Python HTML retrieval returned HTTP 403; browser verification supplied the public
evidence. WordPress Site Kit and Snippet 22 were not changed. **Remaining: observe
an organic, consented `krug_newsletter_signup` in GA4 and verify the completed
subscription in Beehiiv before closing #1090.**

This stream does not stitch the WordPress session across domains. Reports must
distinguish the signup stream from exact-host WordPress traffic. Beehiiv remains
the source of truth for all subscriptions; consent-denied or blocked analytics
visits will not appear in GA4. If double opt-in or approval is enabled later, pause
the tag and use the provider's confirmed/active signal instead.

## Rollback and evidence

To stop collection, clear only the personal publication's GTM field or pause this
tag and publish a new version. GTM version 1 is the empty-container rollback.
Retain the GA4 stream and historical data; the key event can be unmarked if needed.
Preserve the export and prior settings. Leave Cookie Banner enabled so visitor
privacy choices remain available.

Private screenshots and public bundle snapshots are retained under
`.generated/current-state/conversion-1090-2026-10-25/` in the original checkout.
