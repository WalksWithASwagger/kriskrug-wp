# Apply + rollback runbook: WP page 2250 events hero backfill (#635)

**PREPARE, DO NOT APPLY.** This PR ships the procedure and a 2026-08-16 live
diff. It does not PATCH WordPress, upload media, or write the catalog. Live
apply waits on an explicit KK approval comment on
[#635](https://github.com/WalksWithASwagger/kriskrug-wp/issues/635) naming the
hero set.

Live target:

- ID **2250**
- slug **`events`**
- URL https://kriskrug.co/events/
- Field written: **`content` only**. Do not send title, slug, excerpt, or meta.

Payload sources (already on `main` via PRs #647 / #648 / the catalog):

- `scripts/events_page/heroes/LEDGER-2024-2025.md`
- `scripts/events_page/heroes/LEDGER-2026-MEETUP.md`
- `scripts/events_page/events-catalog.yaml` (SSOT; mutate only approved `image` fields)
- Generator: `scripts/events_page/render_events_page.py` →
  gitignored `scripts/events_page/out/events-2250.generated.html`

There is **no** pre-baked HTML that already contains the new heroes. The apply
session must: restrict to KK-approved rows → stage local files or attach
existing media IDs → `sync_event_media.py` → re-render → eyeball → snapshot →
POST. See [`live-vs-payload-2026-08-16.md`](./live-vs-payload-2026-08-16.md).

This is an UPDATE of a published page. The 2026-05-15 overwrite incident
applies: slug match before POST, snapshot before write, dry-run first, rollback
file on disk before the write returns.

#635 inherits #592 exclusivity. No other open issue may mutate the catalog,
upload event media, or write page 2250. Do **not** run concurrently with
testimonials (#602) or speaking live writes.

Do **not** use `backup/20260801-events-backfill-ship/` as the restore snapshot.
That tree is the #592 body. Live `modified` is `2026-08-10T10:38:46` after the
IIDA Coffee card. Use a fresh dated dir so both remain intact.

## Current truth — verified 2026-08-16 (public REST + cache-bypass HTML)

Do not close #635. Live does **not** carry the ledger heroes.

| Check | Live 2250 |
|---|---|
| REST `modified` | `2026-08-10T10:38:46` |
| Public cards | 66 `data-event-id` |
| Compact empty media | **49** `aurora-event-compact-media--empty` (2026-08-02 baseline was **48**) |
| Event `<img>` | 16, all HTTP 200 |
| `file:///` | 0 |
| TruNorth | not on the public page |

## Still gated on KK (do not apply without these)

1. Named row set. Default exclude every `NO SOURCE — needs KK` row. Do not
   improvise an image.
2. Photographer courtesy checks in `LEDGER-2026-MEETUP.md`: Peter Holst, Aaron
   Hockenstein, Tristan Brand. Michelle Diamond already has live precedent
   (media 12663).
3. Series-fallback ruling for `van-ai-meetup-01/03/06/07/08/09` (labelled 2024
   frames vs stay empty).
4. `van-ai-meetup-24` credit + date conflict; TED2025 fetch path; AEFL Morten
   wrong-night photo.
5. TruNorth stays art-free unless the organizer grants an image. No speaking
   claim.
6. Every `PROVISIONAL` alt rewritten against the actual frame at upload.
7. Fresh snapshot + dry-run render eyeballed in the apply session.

Repo-side blockers #631 / #632 / #633 are closed. The `blocked` label is stale
as a code dependency; this remains human-gated.

## Identity gate (hard abort if any fail)

Public (no secrets):

1. `GET https://kriskrug.co/wp-json/wp/v2/pages/2250` returns `id == 2250`.
2. That object has `slug == events` and `status == publish`.
3. `GET https://kriskrug.co/wp-json/wp/v2/pages?slug=events` returns exactly one
   page, and that page's `id` is 2250.
4. Title is still `Events`. If it is not, stop. Do not "fix forward."

Authenticated (`context=edit`), immediately before write:

5. Same ID/slug/status.
6. If `modified` is no longer `2026-08-10T10:38:46`, stop and re-diff against
   live. Someone else wrote 2250. Reconcile; do not POST over an unexpected body.

If slug or ID disagree, you are about to write the wrong page. Stop.

## Pre-flight (no live write)

```bash
scripts/notion-to-wp/.venv/bin/python -m unittest \
  scripts.tests.test_events_render_contract -v
```

Must be green. That suite is the guard against re-shipping `file:///`.

Confirm every asset in the approved set has a recorded rights basis. Skip gaps.

Suggested first wave after a narrow KK comment (attach existing library IDs;
confirm each ID via authenticated `GET /wp/v2/media/<id>` before catalog write):

- `2025-03-20-data-storytelling-hackathon` → 8675
- `bcama-vision-conference-panel-2024` → 5740
- `enya-liftoff-keynote-2024` → 6964
- `innovate-west-keynote-2024` → 5360

Do not upload for those four if the media object is the intended file. Write
`image.media_id` + `image.url` + a frame-checked `alt`, then re-render.

For rows that need a new file: download the ledger URL to
`scripts/events_page/heroes/` (keep each file under 1 MB; R2 `large` is often
too big — prefer `grid` or resize), set `image.path` to
`repo:scripts/events_page/heroes/…`, never a hotlink and never a `file://` src.

## Snapshot (before any media upload or page POST)

Authenticated, via Varlock. Do not print secrets.

```bash
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
SNAPDIR="backup/${STAMP}-events-hero-backfill/page-snapshots"
mkdir -p -m 700 "$SNAPDIR"
```

Capture `content.raw` before any write:

```bash
make varlock-run CMD="python3 -c \"
import json, os, urllib.request, base64, pathlib
user = os.environ['WP_USER']
pw = os.environ['WP_APP_PASSWORD']
auth = 'Basic ' + base64.b64encode(f'{user}:{pw}'.encode()).decode()
url = 'https://kriskrug.co/wp-json/wp/v2/pages/2250?context=edit'
req = urllib.request.Request(url, headers={'Authorization': auth, 'User-Agent': 'kriskrug-ops/635'})
with urllib.request.urlopen(req, timeout=90) as resp:
    data = json.load(resp)
path = pathlib.Path('$SNAPDIR/page-2250-events-before.json')
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
raw = data['content']['raw']
pathlib.Path('$SNAPDIR/2250-before-content.raw.html').write_text(raw, encoding='utf-8')
print('id', data['id'], 'slug', data['slug'], 'modified', data['modified'], 'raw_bytes', len(raw.encode('utf-8')))
\""
```

Also save a logged-out rendered page:

```bash
curl -sS -o "$SNAPDIR/page-2250-events-before.html" \
  "https://kriskrug.co/events/?cb=$RANDOM$RANDOM"
```

Public REST does not return `content.raw`. The apply session must use
`context=edit` for the rollback file.

Write the rollback manifest **before** any `--execute` or POST:

```json
{
  "page_id": 2250,
  "slug": "events",
  "url": "https://kriskrug.co/events/",
  "before_snapshot_json": "backup/<STAMP>-events-hero-backfill/page-snapshots/page-2250-events-before.json"
}
```

Save it as `backup/<STAMP>-events-hero-backfill/rollback-events-2250.json`.

Restore (content only; no title/slug/date):

```bash
jq -r '.content.raw' \
  "$SNAPDIR/page-2250-events-before.json" \
  > /tmp/events-2250-rollback.html

make varlock-run CMD="python3 -c \"
import json, os, urllib.request, base64, pathlib
user = os.environ['WP_USER']
pw = os.environ['WP_APP_PASSWORD']
body = pathlib.Path('/tmp/events-2250-rollback.html').read_text(encoding='utf-8')
payload = json.dumps({'content': body}).encode()
auth = 'Basic ' + base64.b64encode(f'{user}:{pw}'.encode()).decode()
url = 'https://kriskrug.co/wp-json/wp/v2/pages/2250?_fields=id,slug,modified,status,link'
req = urllib.request.Request(url, data=payload, method='POST',
    headers={'Authorization': auth, 'Content-Type': 'application/json', 'User-Agent': 'kriskrug-ops/635-rollback'})
with urllib.request.urlopen(req, timeout=90) as resp:
    print(resp.read().decode())
\""
```

## Dry-run media + render (still no page POST)

```bash
scripts/notion-to-wp/.venv/bin/python scripts/events_page/sync_event_media.py
scripts/notion-to-wp/.venv/bin/python scripts/events_page/render_events_page.py
```

Eyeball `scripts/events_page/out/events-2250.generated.html` before any POST:

- `file://` count is 0
- no `/Users/` in any `src`
- every approved row that should have art now has an `https://` `src`
- skipped `NO SOURCE` rows still use `aurora-event-compact-media--empty`
- `data-event-id` set still matches the 66 live ids (do not retitle or redate)
- TruNorth still absent
- `compact-empty` count is **lower than 49** (issue bar: drop vs the 2026-08-02
  baseline of 48 — today's live is 49 because IIDA Coffee is heroless)

Diff generated vs the snapshot raw:

```bash
diff -u \
  "$SNAPDIR/2250-before-content.raw.html" \
  scripts/events_page/out/events-2250.generated.html
```

Show that diff to Kris. Do not POST.

## Apply (only after KK comment-approves on #635)

Re-check identity against the snapshot just taken. Abort if `modified` drifted.

1. `sync_event_media.py --execute` **only** for ledger-approved local files.
   Log the new media ID range. Do not upload skipped rows.
2. Re-render. Re-run `test_events_render_contract`. Abort on fail.
3. POST **content only** from the generated HTML (already wrapped in
   `<!-- wp:html -->` by `shell-events-2250.html`):

```bash
make varlock-run CMD="python3 -c \"
import json, os, urllib.request, base64, pathlib
user = os.environ['WP_USER']
pw = os.environ['WP_APP_PASSWORD']
body = pathlib.Path('scripts/events_page/out/events-2250.generated.html').read_text(encoding='utf-8')
payload = json.dumps({'content': body}).encode()
auth = 'Basic ' + base64.b64encode(f'{user}:{pw}'.encode()).decode()
url = 'https://kriskrug.co/wp-json/wp/v2/pages/2250?_fields=id,slug,modified,status,link'
req = urllib.request.Request(url, data=payload, method='POST',
    headers={'Authorization': auth, 'Content-Type': 'application/json', 'User-Agent': 'kriskrug-ops/635'})
with urllib.request.urlopen(req, timeout=90) as resp:
    print(resp.read().decode())
\""
```

4. Save `$SNAPDIR/page-2250-events-after.json` (`context=edit` GET).

## Verify (logged out, cache-bypassed)

```bash
curl -sS -o /tmp/2250-after.html \
  "https://kriskrug.co/events/?cb=$RANDOM$RANDOM"
```

Must all be true:

- HTTP 200, id/slug still 2250 / `events`
- `file:///` count is 0
- every `<img>` on `/events/` that is an event hero returns HTTP 200
- `aurora-event-compact-media--empty` is measurably below **49** (and below the
  2026-08-02 baseline of **48** if the approved set is large enough)
- every dated card still has `data-event-end`; upcoming/past buckets still
  sensible (IIDA / Pitch Night / Sep 30 / Futureproof remain the upcoming set
  until those dates roll)
- no TruNorth speaking claim
- 66 public `data-event-id` values unless KK approved adding/removing a card
  (this issue's default is heroes only)

Purge Pagely cache for `/events/` if the readback is stale. Re-fetch with a
new `cb`.

Comment on #635: media ID range, before/after empty-media counts, rollback path.

## Rollback

If anything is wrong, restore `content` from the snapshot taken immediately
before the write using the restore commands in the Snapshot section above. Do
not reconstruct from memory. Do not use the 2026-08-01 #592 backup if the
fresh `$SNAPDIR` snapshot exists. Purge cache and cache-bypass confirm the
pre-apply empty-media count and card set are back, then stop and report.

New media objects can stay in the library; they are unused if the page rolls
back. Do not bulk-delete media in the same session.

## Explicit non-actions

- Do not PATCH any page other than 2250.
- Do not retitle or redate events.
- Do not deploy theme files.
- Do not run the Notion connector.
- Do not change the slug, title, or excerpt.
- Do not upload `NO SOURCE` rows or hotlink Luma/R2 URLs on the live page.
- Do not merge this PR as a substitute for the live write.
- Do not apply from `backup/20260801-events-backfill-ship/` "after" JSON.
  That is the #592 body, not current live.
