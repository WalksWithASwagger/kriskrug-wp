# Apply + rollback runbook: WP page 2409 testimonials v2 (#602)

**PREPARE, DO NOT APPLY.** This PR ships the procedure and a 2026-08-16 live
diff. It does not PATCH WordPress. Live apply waits on an explicit KK approval
comment on [#602](https://github.com/WalksWithASwagger/kriskrug-wp/issues/602).

Live target:

- ID **2409**
- slug **`testimonials`**
- URL https://kriskrug.co/testimonials/
- Field written: **`content` only**. Do not send title, slug, excerpt, or meta.

Payload (already on `main` via [PR #630](https://github.com/WalksWithASwagger/kriskrug-wp/pull/630)):
`content/source-packs/content-architecture-2026/wp-payloads/testimonials.html`

This is an UPDATE of a published page. The 2026-05-15 overwrite incident applies:
slug match before PATCH, snapshot before write, dry-run first, rollback file on
disk before the write returns.

Do **not** use `backup/20260801-testimonials/` as the v2 snapshot directory. That
tree is the v1 rollback baseline. Use a fresh dir so both remain intact.

## Current truth — verified 2026-08-16 (public REST + cache-bypass HTML)

Do not close #602. Live does **not** match the v2 payload.

| Check | Live 2409 | v2 payload |
|---|---|---|
| REST `modified` | `2026-08-01T19:09:19` | n/a (repo file) |
| Headline | Proof from the rooms, stages, and cohorts. | Proof with names attached. |
| Marker comment | `content-architecture-2026:testimonials` | `content-architecture-2026:testimonials-v2` |
| Quote cards | 19 `aurora-quote-card` | 40 `aurora-tstm-card aurora-quote-card` |
| `aurora-tstm` in body | 0 | present (hero, stats, press, wall) |
| Featured three | Kerris, Landon, Carly | Kerris, Simon (Meetup #10), Arno |
| Hard blocks (Jordan / McKay / `user-infos`) | absent | absent |
| Theme CSS | Live Aurora **1.6.5**; `aurora-tstm` rules present (#601 closed 2026-08-10) | n/a |

Full name/section table: [`live-vs-payload-2026-08-16.md`](./live-vs-payload-2026-08-16.md).
Public REST rendered body: [`live-content-rendered-2026-08-16.html`](./live-content-rendered-2026-08-16.html)
(diagnosis only; not a restore source — public REST has no `content.raw`).

## Still gated on KK (do not apply without these)

1. Editorial/public-use rulings in [`curated-set-v2.md`](./curated-set-v2.md): Featured three, Peter Bowles profanity (WA-10), duplicate-era Rob Cottingham, Landon/Carly moved out of Featured, T2 ship-and-log.
2. Exact approval of **this** payload file, not a paraphrase.
3. Fresh snapshot + dry-run diff reviewed in the apply session.

#601 is complete. Theme CSS is already on live. This issue is body-only.

## Identity gate (hard abort if any fail)

Public (no secrets):

1. `GET https://kriskrug.co/wp-json/wp/v2/pages/2409` returns `id == 2409`.
2. That object has `slug == testimonials` and `status == publish`.
3. `GET https://kriskrug.co/wp-json/wp/v2/pages?slug=testimonials` returns exactly one page, and that page's `id` is 2409.
4. Title is still `Testimonials`. If it is not, stop. Do not "fix forward."

Authenticated (`context=edit`), immediately before write:

5. Same ID/slug/status.
6. `content.raw` still matches the v1 body (headline `Proof from the rooms, stages, and cohorts.` and **19** `aurora-quote-card`s), unless KK has already accepted a drifted live body and a re-reconciled payload. If `modified` is no longer `2026-08-01T19:09:19`, stop and re-diff against the payload. Do not PATCH a drifted body.

If slug or ID disagree, you are about to write the wrong page. Stop.

## Snapshot (before any write)

Authenticated, via Varlock. Do not print secrets. Fresh directory so the 2026-08-01 v1 backups stay untouched.

```bash
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
SNAPDIR="backup/${STAMP}-testimonials-v2/page-snapshots"
mkdir -p -m 700 "$SNAPDIR"

make varlock-run CMD="python3 scripts/content_architecture_deploy.py \
  --page testimonials \
  --snapshot-dir $SNAPDIR"
```

That command is **dry-run by default**. It verifies ID/slug/status and payload
markers. It does **not** write WordPress. It also does **not** save a snapshot
until `--execute`. Capture `content.raw` yourself before the write:

```bash
make varlock-run CMD="python3 -c \"
import json, os, urllib.request, base64, pathlib
user = os.environ['WP_USER']
pw = os.environ['WP_APP_PASSWORD']
auth = 'Basic ' + base64.b64encode(f'{user}:{pw}'.encode()).decode()
url = 'https://kriskrug.co/wp-json/wp/v2/pages/2409?context=edit'
req = urllib.request.Request(url, headers={'Authorization': auth, 'User-Agent': 'kriskrug-ops/602'})
with urllib.request.urlopen(req, timeout=90) as resp:
    data = json.load(resp)
path = pathlib.Path('$SNAPDIR/page-2409-testimonials-before.json')
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
raw = data['content']['raw']
pathlib.Path('$SNAPDIR/2409-before-content.raw.html').write_text(raw, encoding='utf-8')
print('id', data['id'], 'slug', data['slug'], 'modified', data['modified'], 'raw_bytes', len(raw.encode('utf-8')))
\""
```

Also save a logged-out rendered page:

```bash
curl -sS -o "$SNAPDIR/page-2409-testimonials-before.html" \
  "https://kriskrug.co/testimonials/?cb=$RANDOM$RANDOM"
```

Public REST does not return `content.raw`. The apply session must use
`context=edit` for the rollback file.

Write the rollback manifest **before** `--execute`:

```json
{
  "page_id": 2409,
  "slug": "testimonials",
  "url": "https://kriskrug.co/testimonials/",
  "before_snapshot_json": "backup/<STAMP>-testimonials-v2/page-snapshots/page-2409-testimonials-before.json",
  "restore_command": "varlock run --inject vars -- scripts/notion-to-wp/.venv/bin/python scripts/content_architecture_deploy.py --page testimonials --snapshot-dir backup/<STAMP>-testimonials-v2/page-snapshots --restore"
}
```

Save it as `backup/<STAMP>-testimonials-v2/rollback-testimonials-2409.json`.

## Dry-run

The deploy script without `--execute` is the dry-run. Then print a unified diff
of snapshot `content.raw` vs the payload and show it to Kris.

```bash
diff -u \
  "$SNAPDIR/2409-before-content.raw.html" \
  content/source-packs/content-architecture-2026/wp-payloads/testimonials.html
```

Confirm before asking for the apply comment:

- Opening H2 is `Proof with names attached.`
- `aurora-quote-card` count is 40 in the payload, 19 in the snapshot
- Featured cites are Kerris Hougardy, Simon Haworth, Arno Apeldoorn
- `Don't fucking stop` is present iff KK approved WA-10
- `William Jordan` and `Stephanie McKay` counts are 0
- `user-infos` count is 0
- Butterfield appears once, Archive-only, photography rec (not the camera-in-hand line)
- Camera-in-hand cite is Rob Cottingham
- Request body would be `{"content": "<payload>"}` only — no title/slug/date
- Payload markers in `page-map.json` `testimonials.markers` are all present

Do not POST.

Repo check (no live write):

```bash
scripts/notion-to-wp/.venv/bin/python -m unittest \
  scripts.tests.test_content_architecture_payloads
```

## Apply (only after KK comment-approves on #602)

Re-check identity against the snapshot just taken. Abort if `modified` drifted.
Then:

```bash
make varlock-run CMD="python3 scripts/content_architecture_deploy.py \
  --page testimonials \
  --snapshot-dir $SNAPDIR \
  --execute"
```

`--execute` snapshots again immediately before the write, POSTs `content` only,
readback-checks markers, and restores automatically if readback fails.

Then save `$SNAPDIR/page-2409-testimonials-after.json` if the script did not
already (it does, as `page-2409-testimonials-after.json`).

## Verify (logged out, cache-bypassed)

```bash
curl -sS -o /tmp/2409-after.html \
  "https://kriskrug.co/testimonials/?cb=$RANDOM$RANDOM"
```

Must all be true:

- HTTP 200
- `Proof with names attached.` present
- `Proof from the rooms, stages, and cohorts.` absent from the entry body
- `aurora-quote-card` count is 40
- `aurora-tstm` present
- Section H2s in order: Proof with names attached. / Start with three. / The monthly rooms. / Responsible AI Professional, Cohort 1. / Keynotes and guest sessions. / Workshops that use your real work. / Said in the group chat. / Film Club nights. / The photography and connector years. / Want a room like these?
- Kerris, Simon (Meetup #10 URL `simon-haworth-uk-us-prc`), Arno in Featured
- `kaoruyoshihira` present
- `user-infos` absent
- `William Jordan` and `Stephanie McKay` absent
- Camera-in-hand cite remains Rob Cottingham; Butterfield chip says 2006 LinkedIn rec

Purge Pagely cache for `/testimonials/` if the readback is stale. Re-fetch with a
new `cb`. Desktop/mobile screenshots are KK's pixel pass; this runbook does not
replace them.

Comment the live headline plus card count on #602.

## Rollback

If anything is wrong, restore `content` from the snapshot taken immediately
before the write. Do not reconstruct from memory. Do not use the 2026-08-01 v1
backup if the fresh `$SNAPDIR` snapshot exists.

```bash
make varlock-run CMD="python3 scripts/content_architecture_deploy.py \
  --page testimonials \
  --snapshot-dir $SNAPDIR \
  --restore"
```

Purge cache. Cache-bypass confirm `Proof from the rooms, stages, and cohorts.`
is back and `aurora-quote-card` is 19. Then stop and report.

Fallback if the apply-time snapshot is missing: `backup/20260801-testimonials/`
is the last shipped v1 body, valid only if live `modified` is still
`2026-08-01T19:09:19` **or** the failed apply is the only change since. If live
moved some other way, that tree is not a safe restore source.

## Encoding

Live v1 public REST already stores curly quotes, em dashes, ellipses, and `ü`
(U+00FC) without turning them into `?`. The v2 payload uses the same set
(U+201C/U+201D/U+2013/U+2014/U+2026 plus `ü`). Scan the cache-bypass HTML after
apply for replacement `?` inside quotes. If they appear, roll back; do not
"fix forward" with a second PATCH in the same session.

## Explicit non-actions

- Do not PATCH any page other than 2409.
- Do not deploy theme files. #601 already landed `aurora-tstm` on live 1.6.5.
- Do not touch Homepage #415, Speaking #419, or consent-outreach sending.
- Do not run the Notion connector.
- Do not change the slug, title, or excerpt.
- Do not merge this PR as a substitute for the live write.
- Do not apply from `backup/20260801-testimonials-enrichment/` "after" JSON.
  That is v1, not the 40-card payload.
