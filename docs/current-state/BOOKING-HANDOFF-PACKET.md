# Booking handoff preparation — #984

**Status:** Preparation only; no mail, DNS, WordPress, analytics or service changes.
**Evidence collected:** 2026-09-06, 17:45–17:49 UTC. Track A.
**Owner decisions still needed:** address, mail account/admin, any paid service,
live rollout and optional confirmation automation. Approval to prepare this
packet does not establish that a mailbox works.

## Current public handoff

Public GETs at 17:46 UTC returned HTTP 200 at every final URL below. These are
fresh observations, not the field audit's earlier contact snapshot.

| Entry surface | Booking/contact links observed | Actual destination |
|---|---|---|
| [Homepage](https://kriskrug.co/) | Header/footer “Contact”; “Get in touch” | `/contact/` |
| [Contact](https://kriskrug.co/contact/) | “Email Kris”; “Send the note” | `mailto:feelmoreplants@gmail.com?subject=Inquiry%20from%20kriskrug.co` |
| Contact | Visible `feelmoreplants@gmail.com` address | `mailto:feelmoreplants@gmail.com` |
| [Speaking](https://kriskrug.co/speaking/) | “Start a booking conversation” twice; “Contact Kris about your event”; “Ask about this talk” three times | `/contact/` |
| [Services](https://kriskrug.co/services/) | Redirects to `/generative-ai-services/`; “Start a conversation” | `/contact/` |
| [EPK](https://kriskrug.co/podcast-guesting-page-epk/) | “Start a media inquiry” twice; `kriskrug.co/contact` | `/contact/` |
| All five surfaces | Shared header/footer Contact and “Get in touch” | `/contact/` |

The homepage newsletter link (“Get the weekly email”) goes to
`https://kriskrug.beehiiv.com/`; it is not a booking CTA and must not change.
Existing booking links already converge on Contact. Preserve those links and
change only Contact's three email anchors and associated helper copy during a
separately approved rollout. Do not replace old addresses in articles, archives,
Feelmore Plants history, or unrelated schema/templates.

Public HTML and headless Chromium DOM checks at 390×900 and 1440×900 cover the
five routes and resolved link destinations. These checks establish rendered
links, not delivery, real-device mail-client handoff or successful inquiries.
Those owner/device checks remain in the release checklist below.

## Mail/DNS ownership and reusable path

Public DNS on 2026-09-06:

- NS: `salvador.ns.porkbun.com`, `fortaleza.ns.porkbun.com`,
  `curitiba.ns.porkbun.com`, `maceio.ns.porkbun.com`.
- Authoritative query to `salvador.ns.porkbun.com` for apex MX: `NOERROR`,
  zero answers. No explicit mail exchanger was published in this observation;
  this is not proof that no mail service/account exists.
- Apex TXT contained site/domain verification records, no `v=spf1` record.
- Authoritative `_dmarc.kriskrug.co` TXT: `NXDOMAIN`.
- DKIM remains unknown: selectors must come from the chosen sending provider;
  guessing one selector cannot prove domain-wide absence.

Porkbun is the observable DNS authority. The human account owner, access rights,
existing mail subscription, aliases, forwarding rules and actual inbox handling
are **owner-only unknowns**. Public Gmail contact usage does not prove a Google
Workspace tenant. Do not infer a provider from verification TXT records.

**Proposed address:** `hello@kriskrug.co`, subject to KK's explicit address choice.
**Preferred reusable path:** KK/admin checks existing domain-mail entitlements
first. If an existing provider supports both receipt and authenticated sending,
add an alias to a retained, monitored mailbox there, using its supported outbound
identity. Avoid a new subscription or MX migration where an existing entitlement
suffices. If none exists, stop for a provider/budget decision; DNS hosting alone
is not a usable mail service. Forwarding alone is insufficient without tested,
authenticated replies from the branded identity.

Owner/admin records, privately: account/admin identity; provider and entitlement;
intended receiving mailbox; allowed sender identity; current records and TTLs;
rollback operator. Record only pass/fail and provider name publicly, not account
identifiers, message headers or customer correspondence.

## Proposed rollout and recovery

1. **Owner gate:** approve the address, identify provider/admin and receiving
   mailbox, confirm no unapproved purchase, and confirm the old Gmail inbox will
   remain monitored. Keep existing public CTAs intact.
2. **Private snapshot:** export exact current DNS records/TTLs and mail routing;
   record existing sending services before changing authentication. Preserve
   recovery access and the old inbox. No migration/deletion is part of this work.
3. **Separately approved configuration:** provision receipt and authenticated
   branded sending through the selected provider. Use its actual generated
   records; do not invent MX targets, DKIM keys or SPF includes in this packet.
   Maintain one SPF policy containing all approved senders and validate it;
   enable DKIM and verify signing/alignment. Introduce DMARC monitoring only
   after sender inventory and report destination approval; do not jump to
   quarantine/reject while legitimate senders are unknown.
4. **Delivery gate:** with explicit permission for test emails, test inbound from
   two external providers, receipt in the monitored mailbox, spam placement,
   a branded reply back to each sender and a follow-up reply. Verify From and
   Reply-To identity plus SPF, DKIM and DMARC results/alignment in received
   headers. Test the old Gmail address in both directions as well. Record dated
   pass/fail privately; no public CTA switch until all tests pass.
5. **Content gate:** after separate live approval, recheck Contact slug and ID,
   snapshot its exact editable content privately and prepare a dry-run diff of
   only the three anchors/helper text. Use the existing snapshot-aware publishing
   path. Do not bulk-replace the mailbox across historical content.
6. **Release/readback:** apply the approved Contact change, fetch normal and
   cache-bypassed public HTML, and walk the five entry paths at both viewport
   sizes. Confirm the email target/subject and visible copy match this packet.
7. **Recovery:** on failed delivery or wrong reply identity, restore the exact
   prior Contact snapshot and invalidate/read back affected cache. Retain the
   branded mailbox/routing to receive already-sent inquiries while the owner
   resolves failure; do not immediately delete it. Restore changed DNS/mail
   configuration from the private snapshot only when needed and owner-approved,
   allowing for cached TTLs. Keep checking both inboxes and resolve any queued or
   failed inquiries privately. Do not declare recovery from a page readback alone.

## Exact proposed copy

Apply only after the branded mailbox passes the delivery gate:

- Primary Contact CTA: **Email Kris**
- Destination: `mailto:hello@kriskrug.co?subject=Inquiry%20from%20kriskrug.co`
- Helper: **Send a short brief, not a vague hello: who is the audience, what date
  are you considering, what format, where will it happen, and what question does
  the room need answered? If a detail is undecided, say so.**
- Direct option: **Prefer to write directly? hello@kriskrug.co**
- Direct link: `mailto:hello@kriskrug.co`
- Closing CTA: **Send the note**, using the primary destination above.

Keep the current Speaking, Services, homepage and EPK CTA labels and `/contact/`
destinations. There is no demonstrated reason to rewrite them for this rollout.

## Optional form — owned by #277

[#277](https://github.com/WalksWithASwagger/kriskrug-wp/issues/277) remains open
and owns email-versus-form choice; email-only is the current default. No plugin
or form implementation belongs to #984. If that issue selects a form, its
implementation contract must include:

- Name and reply email plus audience, date/timing, format, location/platform and
  the question the room needs answered. Allow “undecided” briefing answers;
  require usable name/email and an intelligible brief without forcing fake dates.
- Visible associated labels, keyboard operation, focusable error summary and
  field-specific accessible errors; preserve entries after validation failure.
- Server-side email/length validation and bounded rate limiting, a low-friction
  spam control, duplicate-submit handling and no arbitrary attachment uploads.
- Authenticated domain sender with validated visitor email as Reply-To, not a
  forged visitor From. Distinguish server acceptance from confirmed delivery.
- Success after server acceptance: **Your inquiry has been submitted. Keep a copy
  of your brief. This is an inquiry, not a confirmed booking.** Delivery must be
  monitored separately; do not report success when sending fails.
- Failure: **Your inquiry could not be sent. Your brief is still here. Try again,
  or email hello@kriskrug.co directly.** Keep the direct email available throughout.
- A short retention/privacy notice, limited staff access and deletion policy
  selected in the implementation issue; message contents never enter analytics.

## Speaker one-pager and confirmation draft

Reuse [#876](https://github.com/WalksWithASwagger/kriskrug-wp/issues/876) and its
[producer copy deck](../../content/source-packs/content-architecture-2026/press-kit/copy-deck.md).
Do not rebuild the EPK here. Its approved September 3 descriptor/bios supersede
older unresolved-brand notes elsewhere in that source pack.

Proposed public one-pager outline for that lane:

1. Kris Krüg and the approved one-line booking descriptor from the copy deck.
2. Approved 75-word bio verbatim; no unverified availability, rates or credits.
3. Keynote, workshop, interview, commentary and host/moderator formats using the
   deck's proposed descriptions after editorial review.
4. Three source-backed topic angles: Both Hands Full; AI for creative people;
   responsible AI in practice. Link Speaking for context and examples.
5. Booking link to `/contact/`, the short-brief instructions above and revision
   date. Optional portrait only after manifest permission verification.

Publish accessible HTML within the existing EPK workflow; a downloadable PDF is
optional work in #876. Never promise a file before its public URL resolves.
Follow the [asset manifest](../../content/source-packs/content-architecture-2026/press-kit/assets/manifest.json)
entry status, rights and public URL at implementation time, not stale README
summaries. Do not bundle unapproved photography.

**Draft confirmation email (not sent; automation requires separate approval):**

> Subject: Your inquiry to Kris Krüg
>
> Thanks for sending your brief. This confirms receipt of your inquiry; it does
> not confirm a booking or availability.
>
> If any details are still taking shape, you can reply with the audience, date,
> format, location and the question the room needs answered.
>
> Producer background and materials: https://kriskrug.co/podcast-guesting-page-epk/
>
> Kris Krüg

Only enable receipt language once confirmed delivery triggers it. Link the
existing public EPK now; call it a “speaker one-pager” only once #876 actually
publishes that resource. No response-time guarantee, fees, invented credits or
unsolicited promotional subscription. Prevent reply loops and repeated auto-replies.

## Measurement and release verification

Baseline: owner tallies 28 days of delivered booking inquiries and qualified
inquiries, distinguishing spam/test traffic; use dates and counts only in a
private aggregate sheet. Define qualified as a real prospective engagement with
a usable reply route and enough audience/format/timing context to follow up.
Record unknowns honestly; never reconstruct completion from mailto clicks.

After rollout compare the same 28-day windows and source categories, noting
traffic/seasonality and small counts. A mailto click is intent, not completion.
For an optional form, track start, accepted submission and delivery failure as
separate aggregate events; confirmation and delivery logs supply actual completion.
Analytics may contain route and fixed CTA identifier, never email, name, message,
subject/body query strings or individual qualification notes. Baseline event
instrumentation, if missing, needs its own approved implementation; this packet
adds none. Success means reliable delivery/replies and more useful inquiries,
not an asserted conversion lift without evidence.

Completed preparation verification:

- [x] `make doctor` then `make status-readonly` at 17:45 UTC: successful; read-only
  safe, all startup sources resolved, WP smoke zero failures/warnings. Shared
  worktrees present; no unrelated changes included.
- [x] Live #277 and #876 read; both open. Ownership preserved.
- [x] Five public routes fetched; actual CTA targets and Services redirect recorded.
- [x] Authoritative mail DNS checked; owner-only unknowns distinguished.
- [x] Desktop/mobile Chromium rendered-link inventory completed, without sending mail.
- [x] Copy and confirmation contain no fees, response-time or availability promises.

Future release checklist (not executed):

- [ ] KK selects address; owner/admin/provider entitlement and DNS access confirmed.
- [ ] Exact private DNS/mail/page snapshots and tested recovery instructions retained.
- [ ] Two-provider receipt/reply/authentication tests and old-inbox continuity pass.
- [ ] Failure recovery exercised with a controlled test and owner-approved messages.
- [ ] Live Contact edit explicitly approved; slug/ID, dry-run and readbacks pass.
- [ ] Desktop and physical mobile mail-client handoff opens correct address/subject;
  copyable address works without a configured mail client. No test email sent silently.
- [ ] Each entry CTA reaches Contact by keyboard/touch; navigation focus and visible
  CTA layout checked, including responsive menu and footer.
- [ ] If selected under #277: invalid email, keyboard errors, spam/rate limit,
  repeated submit, confirmed receipt, server failure and retry preserve the brief.
- [ ] Baseline/reporting owner assigned; delivery failures monitored after release.
