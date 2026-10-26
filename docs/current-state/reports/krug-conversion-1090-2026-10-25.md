# KRÜG completed-signup conversion — October 25, 2026

Refs #1090. Kris selected **completed personal KRÜG newsletter signups**, excluding
link clicks, and authorized implementation and shipping. This supersedes the
September conversion-choice and GA4-save handoff. New service terms and production
test signups are not covered by that authorization.

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
- **Signup collection is not live.** GA4 is configured; the candidate tag below is
  not installed or published. Keep #1090 open.

Varlock doctor passed with warnings for preserved unrelated local files. The
managed-worktree public status check passed WordPress smoke; its draft counts were
unavailable because that invocation did not inherit credentials. The Beehiiv
connector supplied publication/settings readback; browser admin was needed because
it cannot edit live legacy pixels. Existing sign-ins were used, with no credential
values displayed or copied.

## Provider contract and boundaries

Personal publication `pub_4a933c7c-085f-4794-a0d8-6649f2e78f3a` is KRÜG at
`vancouver.beehiiv.com`. Its live builder is legacy. Double opt-in and subscriber
approval are off. All six legacy pixel fields were empty; Cookie Banner was off.
No Beehiiv setting was changed during preparation.

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

## Prepared deployment

- [Tag source](../../../fixes/issue-1090-krug-signup-tag.js) and
  [candidate GTM import](../../../fixes/issue-1090-krug-signup-gtm.json).
- Exact `signedUp` event on `vancouver.beehiiv.com`; runtime limited to current
  hosted signup routes `/` and `/subscribe[/]`.
- Once per page load, with a second runtime guard for duplicate evaluation.
  Two different people subscribing within one loaded page would count once. This
  is conservative deduplication, not a persistent subscriber-ID deduplicator.
- Both `marketing` and `dataProcessing` consent must explicitly be true. Missing,
  denied or malformed consent emits nothing. Enable Beehiiv's native Cookie Banner
  before installing GTM; leave its native GA4 pixel field empty.
- Offline harness is included in `make javascript-syntax`. It executes the actual
  source with network-free stubs and the exported trigger. Coverage includes page
  load, clicks, submit/error events, wrong host/path/event, consent denial,
  duplicate callbacks and PII exclusion. No production signup or synthetic
  Analytics event was sent.
- GTM import, Preview and real delivery remain unverified. Local harness success
  does not establish that a real Beehiiv signup reached GA4.

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

## Remaining activation

The signed-in `kk@bc-ai.ca` GTM account has no containers. Its pending invitation
belongs to BC + AI and was left untouched. Proposed personal account: **KRÜG**,
country **Canada**, container **vancouver.beehiiv.com**, platform **Web**, optional
data sharing off. Creating it requires accepting
[Google's Tag Manager terms](https://www.google.com/analytics/terms/tag-manager/).
The browser action policy requires Kris's confirmation for this new agreement.

After confirmation: import into an empty workspace, verify the exact tag/trigger,
enable the native cookie banner, publish the container, then save its assigned GTM
ID in the personal KRÜG legacy pixel field. Read back settings and the public page.
Repeat the isolated transport check if the imported tag or provider behavior
differs from this candidate. Do not modify WordPress Site Kit or Snippet 22.
Verify organic success delivery without manufacturing a DebugView signup.

This stream does not stitch the WordPress session across domains. Reports must
distinguish the signup stream from exact-host WordPress traffic. Beehiiv remains
the source of truth for all subscriptions; consent-denied or blocked analytics
visits will not appear in GA4. If double opt-in or approval is enabled later, pause
the tag and use the provider's confirmed/active signal instead.

## Rollback and evidence

The inert key event can be unmarked without deleting data. Retain the unused
stream; no historical data needs deletion. After activation, clear only the
personal publication's GTM field or pause this tag and publish a new version.
Preserve the export and prior settings. Leave Cookie Banner enabled so visitor
privacy choices remain available.

Private screenshots and public bundle snapshots are retained under
`.generated/current-state/conversion-1090-2026-10-25/` in the original checkout.
