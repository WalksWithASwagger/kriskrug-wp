# #1028 APPLY — KK paste path (prep only)

**Track:** A — Content + SEO
**Live-apply status:** **prep-only**. This PR does not publish, PATCH, or
edit live WordPress. No credentials are required to review the packet.

Paste is a human wp-admin step. Do not invent a WP login. Do not run the
Notion connector. Do not send email or Buffer.

## What to paste

Visible FAQ only, from [`blocks/`](blocks/):

| Post | File | Insert immediately before |
|---|---|---|
| ALL IN 01 (12783) | [`blocks/all-in-01-faq.html`](blocks/all-in-01-faq.html) | `<section id="owned-network-links-2026"` |
| ALL IN 02 (12788) | [`blocks/all-in-02-faq.html`](blocks/all-in-02-faq.html) | `<section id="owned-network-links-2026"` |

That keeps the live #1030 series rail as the related-link block. The
Content Desk lock's trailing `Related:` line used homepage-only
`bc-ai.ca` / `futureproof.website` anchors (`Day-one follow-up`,
`Prior dispatch`). **Do not paste that line.** It would regress the
descriptive deep links already on both posts.

`FAQPage` files in `blocks/` stay gated. Paste one only after the
matching visible FAQ is live and unchanged.

## Identity (slug check before any edit)

Abort if a live slug differs. Never PATCH on ID alone.

| ID | Required slug | Public URL |
|---:|---|---|
| 12783 | `headed-east-for-all-in-montreal` | https://kriskrug.co/2026/09/15/headed-east-for-all-in-montreal/ |
| 12788 | `all-in-montreal-robot-mirror` | https://kriskrug.co/2026/09/16/all-in-montreal-robot-mirror/ |

## wp-admin steps (KK / Jake)

1. Open the post by slug, not by `?p=`.
2. Confirm ID + slug against the table above. Stop if either moved.
3. Snapshot `content.raw` (or a private revision) before the first edit.
4. In the block editor, add a Custom HTML block **above** the existing
   `ALL IN Montréal 2026` series rail (`#owned-network-links-2026`).
   Code editor paste of the Gutenberg comments in `blocks/` also works.
5. Paste the matching `*-faq.html` file. Content only. Do not send title,
   excerpt, slug, status, date, taxonomies, or SEO meta.
6. Update. Do not change publish status.
7. If Pagely still shows the old body, purge that URL only.
8. Logged-out readback with a cache-bust query. Confirm:
   - `id="faq"` once
   - each locked question + answer once
   - series rail still present
   - no new `Event` JSON-LD
   - no new Buffer / email / Request Indexing

One post at a time. Read back 01 before opening 02.

## After visible FAQ is live and unchanged

Optional, same paste rules, Custom HTML block **after** the visible FAQ:

- [`blocks/all-in-01-faqpage.html`](blocks/all-in-01-faqpage.html)
- [`blocks/all-in-02-faqpage.html`](blocks/all-in-02-faqpage.html)

Mirror only. If a Q or A changed on the page, recut the JSON-LD first.
Do not add a festival `Event`.

## Must not

- Publish a new post or unpublish these two.
- Replace or rewrite the #1030 series rail.
- Paste [`locked/`](locked/) related lines.
- Add Buffer, social, or email.
- Submit the URLs for indexing from this issue.
- Touch theme, plugins, `inc/`, or schema snippets.
- Apply this packet to ALL IN 03 or 04.

## Rollback

Restore the pre-paste `content.raw` snapshot for that post ID only.

## After-paste logged-out gates

```bash
curl -sL "https://kriskrug.co/2026/09/15/headed-east-for-all-in-montreal/?cb=$RANDOM" \
  | grep -c 'id="faq"'
curl -sL "https://kriskrug.co/2026/09/15/headed-east-for-all-in-montreal/?cb=$RANDOM" \
  | grep -F "What is ALL IN Montréal?"
curl -sL "https://kriskrug.co/2026/09/15/headed-east-for-all-in-montreal/?cb=$RANDOM" \
  | grep -F 'owned-network-links-2026'

curl -sL "https://kriskrug.co/2026/09/16/all-in-montreal-robot-mirror/?cb=$RANDOM" \
  | grep -c 'id="faq"'
curl -sL "https://kriskrug.co/2026/09/16/all-in-montreal-robot-mirror/?cb=$RANDOM" \
  | grep -F "What happened on day one at ALL IN Montréal?"
curl -sL "https://kriskrug.co/2026/09/16/all-in-montreal-robot-mirror/?cb=$RANDOM" \
  | grep -F 'owned-network-links-2026'
```

Expect: one FAQ heading per post, locked questions present, series rail
still present. `FAQPage` grep stays at zero until the optional second
paste.
