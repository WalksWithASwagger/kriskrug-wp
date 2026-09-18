# #1030 APPLY notes — paste-ready, prep only

**Track:** A — Content + SEO
**Live-apply status:** **prep-only**. This session did not run an authenticated dry-run. `make doctor` reported WordPress credentials unresolved (no `WP_USER` / `WP_APP_PASSWORD` and no `WP_API_*` pair). Do not PATCH. Do not merge. SEO owns live paste after LGTM on this exact set.

Parent: #1025. Soft LGTM on #1030 (2026-09-18) already named the ALL IN 03 public canonical. This pack uses that permalink only.

## What this is

Paste-ready Gutenberg HTML plus find/replace notes for the exact #1030 matrix. New copy is short clauses or a compact series rail. No scene rewrites. No homepage dumps when a deep URL is listed. No Event schema. No Buffer. No Request Indexing. No `?p=12800`.

## Preflight already done (public, 2026-09-18)

Logged-out GET of every matrix target. All included URLs returned **200** with a self-canonical where WordPress emits one. Cross-host `bc-ai.ca` paths without a trailing slash resolve 200 to the slashless URL; `futureproof.website` festival and speaker paths resolve 200 with the trailing slash. Re-check immediately before paste.

Schema readback on ALL IN 01 and 03: `BlogPosting` only. Do not add Event.

## How to paste

1. Open the post or page by slug, not by `?p=`.
2. Confirm ID + slug against [`matrix.md`](matrix.md). Stop if either moved.
3. Snapshot `content.raw` (or a private editor revision) before the first edit on that object.
4. Paste one object at a time from [`blocks/`](blocks/).
5. Send **content only**. Do not send title, excerpt, slug, status, date, taxonomies, or SEO meta.
6. Read back the public page. Confirm the new href + exact anchor once, no new 404, no new Event schema, no `?p=12800`.
7. Keep the snapshot as the rollback payload. Restore only `content` if readback fails.

If a vault is available later: dry-run first, then paste or PATCH only after SEO LGTM on this PR. This folder is not an apply script.

## Shared series rail

Heading text is exactly `ALL IN Montréal 2026`. List only the other public entries. Place the rail near the end, before generic related / rabbit-hole lists.

```html
<!-- wp:heading -->
<h2 class="wp-block-heading">ALL IN Montréal 2026</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- per-post items in the block file -->
</ul>
<!-- /wp:list -->
```

## Object-by-object

### ALL IN 01 — post 12783

File: [`blocks/all-in-01.html`](blocks/all-in-01.html)

1. After `I am there as accredited media, but I am not a neutral observer floating above the action in a clean white lab coat.` insert the conferences clause.
2. After `British Columbia has excellent researchers, builders, artists and communities doing the work, but no enduring institutional anchor on that scale.` insert the west-coast vantage clause.
3. Change `Futureproof Festival runs October 28 to 30` so the specified `/festival/` anchor is the linked phrase. Leave the earlier homepage Futureproof link in the lede.
4. After the YVR closing figure, before the author panel, paste the series rail (02 + 03).

### ALL IN 02 — post 12788

File: [`blocks/all-in-02.html`](blocks/all-in-02.html)

1. After the Hanna `what about us on the West Coast?` paragraph, insert the regional-story clause.
2. After `Futureproof, October 28-30 in Vancouver`, insert the `/festival/` conversation clause. Do not rewrite the existing homepage CTA.
3. Insert the series rail (01 + 03) after `I will be there with the recorder, asking first.` and **before** `Further down the rabbit hole`. Keep the rabbit-hole Post 1 item; it is a source pack, not the series rail.

### ALL IN 03 — post 12800

File: [`blocks/all-in-03.html`](blocks/all-in-03.html)

Public permalink only:
`https://kriskrug.co/2026/09/17/all-in-montreal-day-two-uncle-evan-and-the-extremely-suspicious-backpack/`

1. Unwrap `four of the thirty-three submissions in the previous federal AI task-force process` so that sentence is plain text again.
2. After `So I am pulling them.` insert one clause with both Task Force anchors.
3. Replace the live `Continue the series` heading + numbered title links with the specified-anchor rail (01 + 02).
4. After that rail, paste the next-room speaker line. Do not touch the reported `invite him to Futureproof` `/speakers/` lineup link.

### January essay — post 11171

File: [`blocks/january-both-hands-full.html`](blocks/january-both-hands-full.html)

1. After the Workflow 3 guardrail paragraph, before The Human Moat, insert the `/ai-for-creatives/` clause.
2. After `Get in the room, because the room is making decisions whether you're there or not.` insert the Vancouver AI community clause.
3. After `Both hands full. Keep walking.` insert the Futureproof `/festival/` invitation.

Leave the bio `vancouver.bc-ai.net` link alone. Leave the old Notion `both hands full` href alone; that is #342, not this matrix.

### AI Second Brain — post 8802

File: [`blocks/ai-second-brain.html`](blocks/ai-second-brain.html)

1. After `because everything else flows from there.` insert the `/ai-tools/` clause.
2. After the membership-tier practical paragraph, insert the founders-workflow clause.
3. After the authenticity / ethics caveat, insert the January `keep both hands on the work` clause.

### `/ai-tools/` — page 12321

File: [`blocks/ai-tools.html`](blocks/ai-tools.html)

Retitle the existing card `h3` from `Build an AI second brain` to `Build an AI second brain that works for you`. Same href. Do not add a second card.

### Founders workflows — post 12744

File: [`blocks/founders-workflows.html`](blocks/founders-workflows.html)

After `That is a second brain, scoped to one project.` insert the specified inbound.

### Speak it into existence — post 11878

File: [`blocks/speak-it-into-existence.html`](blocks/speak-it-into-existence.html)

Insert the specified inbound after step 4 (`Attach your worldview, style guide, and refusal lines.`). Retitle the existing Related item to the same anchor so the URL appears once.

### God Skills — post 12263

File: [`blocks/god-skills.html`](blocks/god-skills.html)

After the `knowledge-signal` / reusable-context idea, insert the specified inbound.

### `/blog/` — page 2316 (optional)

File: [`blocks/blog-hub.html`](blocks/blog-hub.html)

Page content is currently empty. The posts archive already shows the three ALL IN cards at the top. Paste the hub rail only after confirming Aurora renders page 2316 body above the loop. If it does not, skip. Do not edit `/events/`.

## Out of scope

- Theme / FSE / `theme.json` (Track B)
- Event schema, Buffer, Request Indexing
- Live WP REST writes from this PR
- Rewriting ALL IN scenes to carry links
- Changing `#342` Notion href on the January essay
- Activating #1025 crawl-hygiene or any snippet

## Rollback

Each object: restore the pre-paste `content.raw` snapshot. No cache purge is required for a content-only rollback, but if Pagely still shows the pasted rail after restore, SEO can purge that URL only.
