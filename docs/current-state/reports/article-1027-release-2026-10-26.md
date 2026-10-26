# Article 3 correction release: October 26, 2026

The approved two-line correction is live on [Article 3](https://kriskrug.co/2026/09/17/all-in-montreal-day-two-uncle-evan-and-the-extremely-suspicious-backpack/), WordPress post **12800**. This completes #1027 following the [version reconciliation](article-1027-reconciliation-2026-10-25.md) and [source-audio audit](article-1027-audio-audit-2026-10-25.md).

Kris instructed “ship it and cleanup and wind down” on October 26 in response to the prepared correction and quotation-retention decision packet. That authorizes publishing the reviewed copy with the existing quotations retained; it is not represented as a newly recovered historical third-party permission receipt.

## Applied

- The dinner remark about knowing when one is being sold to is attributed to **Martin**, replacing the incorrect first-person attribution.
- Justine's paragraph now uses the clearly supported sentence: **“It's an actual code,” she said.** The disputed machine-transcribed opening repetitions were omitted rather than reconstructed.

The other source-supported quotations remain, including Alexis's words as Kris's recorded retelling. The source review is documented as machine-assisted verification, not human ear review or voice biometrics.

## Verification and rollback

A fresh slug lookup resolved exactly post 12800. Dry-run and immediate pre-write reads matched the reviewed source hash. The Varlock-injected WordPress REST update sent only `content`, once, at **2026-10-26 15:00:18 UTC / 08:00:18 Pacific**. Independent authenticated readback exactly matched the candidate.

- Before SHA-256: `93d7136388cbcb9bee3ff467ce94f5b7c09a78c9a754a8578665df6d04a5e0e2`.
- After SHA-256: `94a41fc5abb434284a0813c91c7101ad836851683d5f39ca5b4607cce55e97fb`.
- Only two paragraphs changed. All seven body images, every link, headings and paragraph count are preserved.
- Featured media 12804, published status, slug, title, excerpt, author, publication dates, categories, tags, template, format and metadata match the immediate pre-write snapshot.
- Both the normal public URL and cache-bypassed request returned HTTP 200, both corrected quotes, neither superseded passage, and seven body images. No manual cache purge was needed.
- Startup `make doctor` passed with the expected unrelated-checkout warnings. Varlock-backed `make status-readonly` reported WordPress 7.0.7 and zero smoke failures or warnings.

Private rollback and verification evidence: `.generated/current-state/article-1027-release-2026-10-26/` in the original checkout. It includes `post-immediate-before.json`, `post-after.json`, dry-run/apply receipts and both public responses. To roll back, first verify post ID, slug and the current after hash, then restore only the prior `content.raw`; stop if another edit has intervened. Original audio and the audit packet remain private under `.generated/current-state/article-1027-audio-2026-10-25/`.

## Wind-down

No new kriskrug work lane is opened. The #1090 completed-signup heartbeat stays active and quiet on unchanged state; it still requires Beehiiv completion and independent GA4 delivery before issue closure. The managed social/newsletter worktree remains attached because that monitor references its release documentation. Preserve the original checkout, unrelated drafts and recovery evidence. Remove only this release branch after a verified merge and retain its recovery ref.
