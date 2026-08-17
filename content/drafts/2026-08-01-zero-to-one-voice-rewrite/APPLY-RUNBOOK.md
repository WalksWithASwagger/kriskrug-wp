# Apply + rollback runbook: post 12034 Zero to One (#612)

**Applied 2026-08-17T05:05Z.** Snapshot `backup/20260817T050528Z-12034-zero-to-one-612/`. This file remains the rollback procedure.

Live target:

- ID **12034**
- slug **`zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey`**
- URL https://kriskrug.co/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/
- Field written: **`content` only**. Do not send title, slug, date, excerpt, or taxonomies.

Payload: `proposed-content-raw.html` in this directory.

This is an UPDATE of a published post. The 2026-05-15 overwrite incident applies:
slug match before PATCH, snapshot before write, dry-run first, rollback file on
disk before the write returns.

## Identity gate (hard abort if any fail)

1. `GET /wp-json/wp/v2/posts/12034?context=edit` returns `id == 12034`.
2. That same object has `slug == zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey`.
3. Public `GET /wp-json/wp/v2/posts?slug=zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey`
   returns exactly one post, and that post's `id` is 12034.
4. Title still starts with `Zero to One`. If it does not, stop. Do not "fix
   forward."

If slug or ID disagree, you are about to write the wrong post. Stop.

## Snapshot (before any write)

Authenticated, via Varlock. Do not print secrets.

```bash
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
SNAPDIR="backup/${STAMP}-12034-zero-to-one-612"
mkdir -p -m 700 "$SNAPDIR"

make varlock-run CMD="python3 -c \"
import json, os, urllib.request, base64, pathlib
user = os.environ['WP_USER']
pw = os.environ['WP_APP_PASSWORD']
auth = 'Basic ' + base64.b64encode(f'{user}:{pw}'.encode()).decode()
url = 'https://kriskrug.co/wp-json/wp/v2/posts/12034?context=edit'
req = urllib.request.Request(url, headers={'Authorization': auth, 'User-Agent': 'kriskrug-ops/612'})
with urllib.request.urlopen(req, timeout=90) as resp:
    data = json.load(resp)
path = pathlib.Path('$SNAPDIR/rest-post-12034-before.json')
path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
raw = data['content']['raw']
pathlib.Path('$SNAPDIR/12034-before-content.raw.html').write_text(raw, encoding='utf-8')
print('id', data['id'], 'slug', data['slug'], 'modified', data['modified'], 'raw_bytes', len(raw.encode('utf-8')))
\""
```

Also save a logged-out rendered page:

```bash
curl -sS -o "$SNAPDIR/12034-public-before.html" \
  "https://kriskrug.co/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/?cb=$RANDOM$RANDOM"
```

Diff the fresh `content.raw` against `live-content-raw-2026-08-01.html` in this
directory (last authenticated raw snapshot in-repo) and against
`live-content-rendered-2026-08-16.html` (public rendered, 2026-08-16). If live
drifted, stop and re-reconcile the payload. Do not PATCH a drifted body.

Public REST does not return `content.raw`. The apply session must use
`context=edit` for the rollback file. The 2026-08-16 rendered file is diagnosis
only.

## Dry-run

Print a unified diff of snapshot `content.raw` vs `proposed-content-raw.html`.
Confirm:

- opening paragraph is first person (`I opened my studio doors`)
- `130 paid members` count is 0
- `$240` count is 0
- `$340/year` is present (tier list + Core AI conversion)
- `300` members is the current count (lede, launch, turning points, closer)
- `{EMDASH}` / U+2014 count is 0
- no title/slug/date in the request body

Do not POST.

## Apply (only after KK comment-approves on #612)

Body-only update. Explicit UPDATE. Slug re-checked against the snapshot just taken.

```bash
make varlock-run CMD="python3 -c \"
import json, os, urllib.request, base64, pathlib
user = os.environ['WP_USER']
pw = os.environ['WP_APP_PASSWORD']
auth = 'Basic ' + base64.b64encode(f'{user}:{pw}'.encode()).decode()
payload = pathlib.Path('content/drafts/2026-08-01-zero-to-one-voice-rewrite/proposed-content-raw.html').read_text(encoding='utf-8')
url = 'https://kriskrug.co/wp-json/wp/v2/posts/12034?context=edit'
req = urllib.request.Request(url, headers={'Authorization': auth, 'User-Agent': 'kriskrug-ops/612'})
with urllib.request.urlopen(req, timeout=90) as resp:
    live = json.load(resp)
assert live['id'] == 12034
assert live['slug'] == 'zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey'
body = json.dumps({'content': payload}).encode('utf-8')
req = urllib.request.Request(
    'https://kriskrug.co/wp-json/wp/v2/posts/12034',
    data=body,
    headers={'Authorization': auth, 'Content-Type': 'application/json', 'User-Agent': 'kriskrug-ops/612'},
    method='POST',
)
with urllib.request.urlopen(req, timeout=90) as resp:
    after = json.load(resp)
print('wrote id', after['id'], 'slug', after['slug'], 'modified', after['modified'])
\""
```

Then save `$SNAPDIR/rest-post-12034-after.json` the same way as the before snapshot.

## Verify (logged out, cache-bypassed)

```bash
curl -sS -o /tmp/12034-after.html \
  "https://kriskrug.co/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/?cb=$RANDOM$RANDOM"
```

Must all be true:

- HTTP 200
- first body paragraph contains `I opened my studio doors`
- `Kris Krüg opened the doors` is 0
- `As Krüg stated` is 0
- `130 paid members` is 0
- `$240` is 0
- `$340/year` is present
- `300 members` / `300 paid members` is present
- U+2014 in the `entry-content` container is 0 (theme chrome dashes elsewhere do not count)

Purge Pagely cache for that URL if the readback is stale. Re-fetch with a new `cb`.

Comment the live opening paragraph on #612.

## Rollback

If anything is wrong, PATCH `content` from the snapshot taken immediately before
the write. Do not reconstruct from memory. Do not use the May 24 package. Do not
use this directory's August 1 raw file if the fresh `$SNAPDIR` snapshot exists.

```bash
make varlock-run CMD="python3 -c \"
import json, os, urllib.request, base64, pathlib
user = os.environ['WP_USER']
pw = os.environ['WP_APP_PASSWORD']
auth = 'Basic ' + base64.b64encode(f'{user}:{pw}'.encode()).decode()
raw = pathlib.Path('$SNAPDIR/12034-before-content.raw.html').read_text(encoding='utf-8')
# re-check identity
req = urllib.request.Request('https://kriskrug.co/wp-json/wp/v2/posts/12034?context=edit', headers={'Authorization': auth, 'User-Agent': 'kriskrug-ops/612'})
with urllib.request.urlopen(req, timeout=90) as resp:
    live = json.load(resp)
assert live['id'] == 12034
assert live['slug'] == 'zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey'
body = json.dumps({'content': raw}).encode('utf-8')
req = urllib.request.Request(
    'https://kriskrug.co/wp-json/wp/v2/posts/12034',
    data=body,
    headers={'Authorization': auth, 'Content-Type': 'application/json', 'User-Agent': 'kriskrug-ops/612'},
    method='POST',
)
with urllib.request.urlopen(req, timeout=90) as resp:
    after = json.load(resp)
print('restored id', after['id'], 'modified', after['modified'])
\""
```

Purge cache. Cache-bypass confirm the before strings are back (`Kris Krüg opened
the doors` present again means rollback landed; then stop and report).

Fallback if the apply-time snapshot is missing: the in-repo
`live-content-raw-2026-08-01.html` is the last authenticated raw capture, but it
is only valid if live `modified` is still `2026-08-01T18:44:59`. If live moved,
that file is not a safe restore source.

## Latin1

The DB is latin1. Codepoints above U+00FF written through REST come back as `?`.
`ü` (U+00FC) and `Ø` (U+00D8) are inside latin1 and may travel as literals, matching
live. Anything above U+00FF in the payload must be an NCR (`Kr&#252;g` is the
example; not required here because `ü` is already latin1). Scan the payload for
`ord(ch) > 255` before apply. Expected: 0.

## Explicit non-actions

- Do not PATCH cert post 12257 from this lane.
- Do not run the Notion connector.
- Do not change the slug, date, or title.
- Do not merge this PR as a substitute for the live write.
- Do not apply from the May 24 draft package.
