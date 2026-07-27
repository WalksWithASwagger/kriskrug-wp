# #415 What People Say redesign + network diagram spike

Track A draft packet only. No live WordPress writes. No theme deploy.

Issue: [#415](https://github.com/WalksWithASwagger/kriskrug-wp/issues/415)

## Files

| File | Job |
|---|---|
| [`audit.md`](audit.md) | Live + archive audit of the quotes surface |
| [`curated-quotes.md`](curated-quotes.md) | Candidate quote set with sources and permission gates |
| [`redesign-options.md`](redesign-options.md) | Section concepts for KK pick |
| [`copy.md`](copy.md) | Kicker / H2 / dek / CTA copy options |
| [`placement.md`](placement.md) | Homepage slot + newsletter collision rules |
| [`network-diagram-spike/index.html`](network-diagram-spike/index.html) | Standalone SVG/CSS cluster prototype (no CDN) |
| [`network-diagram-spike/NOTES.md`](network-diagram-spike/NOTES.md) | Spike intent, go/no-go, what is fake vs real |

## Verdict in one line

Homepage currently has **no** "What People Say" band. The old placeholder ("Fresh proof belongs here before launch" + invented cites) is gone from live. Rebuild needs real cleared quotes, a quieter proof section that does not fight the newsletter ask, and a separate network diagram preview for KK reaction.

## Hard gates before anything goes live

1. KK clears each attributed quote for public use (permission gate is hard).
2. Zero `fresh proof` / placeholder cites / invented organizer quotes on render.
3. Network diagram stays a shareable preview until explicit go/no-go.
4. Theme markup for the section is a later Track B (or approved template) pass. This packet is content + concept only.

## Recommended pick (agent)

- Section concept: **Option B (clustered themes)** with three named quotes only after clearance.
- Copy: **Option 2** in `copy.md`.
- Placement: after Services, before Writing. Never adjacent as a twin CTA to Newsletter.
- Network spike: open `network-diagram-spike/index.html` in a browser; treat names as illustrative until KK supplies a real map.
