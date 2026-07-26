# Media appearances review (#95) — 2026-07-26

Track A · draft/post review only · **no publish, no WP writes, no new backlinks in this pass**

## Verdict

**Post is already live.** Issue #95’s original “review private draft before publish” gate is obsolete. WP `11879` published on **2026-07-02** and still renders as the canonical roundup.

| Field | Live readback (public) |
| --- | --- |
| ID | `11879` |
| Status | `publish` |
| Slug | `ai-media-appearances-podcast-guesting` |
| URL | https://kriskrug.co/2026/07/02/ai-media-appearances-podcast-guesting/ |
| Title | AI Media Appearances, Podcast Guesting, and Broadcast Commentary |
| SEO title | AI Media Appearances and Podcast Guesting \| Kris Krüg |
| Meta description | Matches draft package |
| Featured media | `11205` (`ai-creatives-krug.jpeg`) |
| Modified | 2026-07-18 (StoryHive addition since May local package) |
| `/media/`, `/appearances/` | **404** — not the public surfaces; use this post + EPK + Publications |

**Disposition for #95:** close or re-label after KK accepts remaining polish/backlink decisions below. Nothing in this issue should publish or schedule anything new.

## Package inventory

Local review package (May 19, stale vs live body):

- `content/drafts/2026-05-19-ai-media-appearances-podcast-guesting/` (`post.md`, `post.html`, SEO, links, image brief, publish-gate)
- Source inventory: `content/source-packs/keynotes-2026/media-appearances/public-source-inventory-2026-05-19.md`
- Historical gates: `APPEARANCES-ROUNDUP-*-2026-05-19.md`

Live diverges from local `post.html` mainly by adding the STORYHIVE / Haus of Owl lead under **Produced Video Interviews** (companion post + KK-channel YouTube). Local package was not re-synced after that edit.

## Ready

- Public URL exists; slug redirects from bare `/ai-media-appearances-podcast-guesting/` to dated permalink.
- Structure still works as a booker-facing proof stack: Broadcast → Produced video → Podcasts → Hosting → Formats → Booking CTAs.
- Voice is recognizably KK: concrete rooms, “weird parts,” “both hands full,” no résumé parade, no corporate AI-slop tone.
- Privacy scan of local body: no private Notion/local paths, no contact PII patterns.
- Featured image is a real library photo (`11205`), not rejected generated media `12270`.
- Primary booking path still correctly points to `/podcast-guesting-page-epk/` and `/speaking/`.
- Outbound links checked 2026-07-26: almost all `200` (see risks for E-ChannelNews).
- EPK already deep-links this post (“see more media appearances”).
- StoryHive companion post reciprocally surfaces this roundup in related/nav chrome.
- Category archive lists the post.

## Blockers (none for “is it published?”)

No publish blockers remain — it is published.

**Hard blockers before treating #95 as fully done / closable without follow-up:**

1. **Local draft package drift.** `content/drafts/2026-05-19-ai-media-appearances-podcast-guesting/post.*` and `publish-gate.md` still describe draft-only / Rafiki-required state. Anyone reusing the package would overwrite live with an older body. Sync or archive before any future connector pass.
2. **Issue metadata stale.** GitHub #95 still reads as pre-publish draft review (`needs-human-review`, `swarm-parked`). Human should update scope to “post-publish polish + hub backlinks” or close with a follow-up issue.

## Backlink risks

Planned hubs from the May verification note: `/speaking/`, `/about/`, `/podcast-guesting-page-epk/` — add only after the post URL exists.

| Surface | Links to roundup? | Risk / note |
| --- | --- | --- |
| Podcast Guesting EPK | **Yes** — “see more media appearances” | Good; soft CTA near STORYHIVE sample |
| Speaking | **No** | Gap. Speaking mentions podcasts lightly but does not point bookers to this proof stack |
| About | **No** | Gap if About is meant to carry media credibility |
| Publications archive | Phrase “media appearances” only; **no slug link** | Overlap risk: Publications already archives interviews; linking the roundup would reduce duplicate-discovery friction |
| Work (`/recent-projects-include/` → `/work/`) | **No** | Optional; lower priority than Speaking/EPK |
| CBC AI Sandbox owned post | **No** | Roundup → CBC is one-way; reciprocal would strengthen cluster |
| StoryHive companion | Related/list chrome yes | Body already cited from roundup |

**Do not add hub backlinks from this swarm pass** without KK approval — that was the original #95 constraint and still applies to page-payload edits.

**Outbound link risks on the live post:**

| Link | Status | Risk |
| --- | --- | --- |
| E-ChannelNews ChannelNext interview | **403** (browser UA and curl) | Dead/blocked trade link; replace, drop, or archive-note if it stays soft-404 for readers |
| Rachel Thexton Amazon URL | `200` but **`/es-ar/` locale** | Inventory already flagged; prefer locale-neutral URL when editing |
| Teen2Life Amazon URL | `200` but **show-level**, not episode | Weak proof; episode URL if one exists |
| “Vancouver AI community archive” | Unlinked phrase | Sounds like a destination; either link MOTLEYKRUG/Luma/archive or rephrase |
| STORYHIVE anchor → `youtu.be/zVy9zCQXPu0` | `200` | KK-channel edition of the interview (title differs from Haus of Owl upload `sxDwQRTZfCA`). Companion post documents both. Not wrong, but anchor text “STORYHIVE On Location: Victoria” matches the Haus title more than the KK-edition title |

## Voice / editorial issues

None that demand an emergency rewrite. Polish notes:

1. **Footer freshness:** “based on public sources collected on May 19, 2026” is outdated after the June StoryHive insert and July publish. Bump or drop the dated claim.
2. **Featured-image alt/caption:** “AI for Creative Professionals Kris Krug” is recycled from another asset story; fine as stage photography, weak as media-appearances card copy.
3. **Human Biography:** inventory lists owned companion `https://kriskrug.co/2025/01/25/human-biography-podcast-w-sharad-khare/`; live roundup only links iHeart. Prefer owned + external, or owned alone.
4. **Formats list** still reads a bit brochure-y (“I can show up as a:”) but matches intentional EPK support-post role — leave unless KK wants sharper voice.
5. **No em dashes** in live body (good vs older gate rule).
6. **No embeds in the roundup body** — links only. EPK carries the heavy STORYHIVE embed; that split is coherent.

## Diff vs local May package (for editors)

Live-only additions (approximate):

- Lead STORYHIVE paragraph with `youtu.be/zVy9zCQXPu0` + companion `…/2026/06/17/storyhive-haus-of-owl-jordan-dack/`
- Featured media `11205` (local package still says image-blocked / featured false in places)

Everything else (CBC, IndigiGenius, Horizons, E-ChannelNews, four podcasts, hosting section, formats, booking) matches the May `post.md` spine.

## Recommended next actions (human / later Track A)

1. KK: accept “already published; #95 becomes polish + selective hub links” or close #95 and file a small follow-up.
2. Optional body polish: E-ChannelNews, Rachel locale, Teen2Life episode, Human Biography owned link, footer date, community-archive phrasing.
3. Optional hub links (separate explicit approval): Speaking (high), Publications (medium), About (medium), CBC post reciprocal (low).
4. Resync or archive `content/drafts/2026-05-19-ai-media-appearances-podcast-guesting/` so it cannot be republished as a create.

## Method

- Public REST: `GET /wp-json/wp/v2/posts?slug=ai-media-appearances-podcast-guesting`
- Public HTML fetch of live post + hubs (Speaking, EPK, About, Publications, Work, CBC post, StoryHive, category)
- Local package + source inventory + issue #95 comment history
- Link status curls for article outbound URLs (2026-07-26)
- **No authenticated WP writes; no publish; no page payload edits**

## Rollback note

N/A for this review pass (read-only). Live post rollback, if ever needed, is a separate KK-approved unpublish/delete after slug/ID confirmation — out of scope here.
