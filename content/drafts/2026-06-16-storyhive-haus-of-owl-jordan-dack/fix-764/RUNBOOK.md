# Issue #764 apply runbook: posts 12327 and 12032

**Status: prepared, not applied. No live write has happened.** Nothing here runs
without KK saying go and someone passing `--apply`.

Covers both posts in the issue. The 12032 payload lives in its own package at
`content/drafts/2026-05-24-what-would-chat-do-and-why-thats-the-wrong-question/fix-764/`.

## What ships

| Post | Change | Payload |
|---|---|---|
| 12327 `/2026/06/17/storyhive-haus-of-owl-jordan-dack/` | 21 em dashes rewritten out of the body | `12327-content-payload.html` |
| 12032 `/2026/06/28/what-would-chat-do-and-why-thats-the-wrong-question/` | Related-block `?p=11876` (404) → resolved permalink | `../../2026-05-24-what-would-chat-do-and-why-thats-the-wrong-question/fix-764/12032-content-payload.html` |

Only `content` is written. Titles, excerpts, SEO meta, categories, featured
media, and dates are untouched. The rewrites are in `12327-rewrites.md`.

### What `?p=11876` was

ID 11876 is **"Send AI After the Art-Adjacent Work"**, slug
`the-75-percent-rule-ai-art-adjacent-work`, and it is **still `private`** on
kriskrug.co. It was never published, which is why `?p=11876` 404s for logged-out
readers. Its own permalink 404s too:
`/2026/06/11/the-75-percent-rule-ai-art-adjacent-work/` (verified 404,
2026-08-15). **There is no permalink for 11876 to resolve to.**

It was deliberately retired. `content/drafts/2026-05-21-the-75-percent-rule-ai-art-adjacent-work/SUPERSEDED.md`
records the call: an automated "blog gap" pass split the STORYHIVE interview into
three thin idea essays, KK wanted **one** cited companion instead, and 11876's
argument was folded into post **12327** under the heading "Galiano, Midjourney,
and the Orbit Around the Art."

So the link goes to 12327, carrying 11876's published title as the anchor text:

```html
<li><a href="https://kriskrug.co/2026/06/17/storyhive-haus-of-owl-jordan-dack/">Send AI After the Art-Adjacent Work</a></li>
```

Removal was the alternative. Kept it because the successor post exists, is
published, and covers the same argument. A live link beats a hole in a Related
list. The other three links in that block were checked and all return 200.

## Latin1 / NCR check

The DB is latin1, so anything above U+00FF written through REST comes back as `?`.

- **Both payloads are clean.** After the rewrites, neither contains a single
  codepoint above U+00FF. The only >U+00FF character in either post was the em
  dash itself, and all 21 are gone. `é`, `ü`, `×`, `·` are all inside latin1 and
  ride through untouched. **No NCR encoding is required for this apply.**
- **But 12327 already has a latin1 casualty**, unrelated to the em dashes and
  pre-dating this work. Live body reads `Eth??s Lab`; the local source has
  `Ethọ́s Lab`. A past REST write ate `ọ` (U+1ECD) and the combining acute
  (U+0301). See "Optional" below. It is **not** in the payload.

## Apply

Requires resolved creds. Everything below is safe to run as-is; the script is
dry-run by default and writes nothing without `--apply`.

```bash
# 1. Dry run. Prints the unified diff and the em-dash delta for both posts.
make varlock-run CMD='python3 scripts/apply_issue_764_fix.py'

# 2. Read the diff. Confirm it is only the rewrites in 12327-rewrites.md
#    plus the one link line in 12032.

# 3. Apply, only after KK approves the diff.
make varlock-run CMD='python3 scripts/apply_issue_764_fix.py --apply'
```

`--post-id 12327` or `--post-id 12032` runs one at a time.

Before each write the script hard-aborts unless all three hold:

1. the ID resolves to the expected slug (2026-05-15 incident rule 2),
2. the live body still hashes to the 2026-08-15 baseline, so a body that drifted
   since this payload was built will stop the run instead of clobbering someone
   else's edit,
3. the payload file still hashes to what was reviewed in this PR.

It also writes `backup/issue-764-em-dash-404/rest-post-<id>-before-<stamp>.json`
(full `context=edit` snapshot) before the PATCH, and prints the exact rollback
command on success. If the live body already equals the payload it prints `[SKIP]`
and moves on, so re-running is safe.

## Verify

The PATCH is a post save, which triggers Pagely's site-wide ARES purge, so no
separate purge step is needed. Prove it anyway, because an authenticated fetch always
shows `BYPASS`, so only an anonymous curl proves the public edge.

```bash
# Em dashes gone from the live rendered body (expect 0).
curl -s "https://kriskrug.co/wp-json/wp/v2/posts/12327?_fields=content" \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['content']['rendered'].count(chr(8212)))"

# Dead link gone, successor link present (expect 0 then 1).
curl -s "https://kriskrug.co/wp-json/wp/v2/posts/12032?_fields=content" \
  | python3 -c "import json,sys;c=json.load(sys.stdin)['content']['rendered'];print(c.count('?p=11876'),c.count('/2026/06/17/storyhive-haus-of-owl-jordan-dack/'))"

# Logged-out public render, cache bypassed. Expect 200 and a MISS on the header.
curl -s -A "Mozilla/5.0" -D- -o /dev/null \
  "https://kriskrug.co/2026/06/17/storyhive-haus-of-owl-jordan-dack/?cb=$RANDOM" \
  | grep -i "HTTP/\|x-gateway-cache-status"
curl -s -A "Mozilla/5.0" "https://kriskrug.co/2026/06/28/what-would-chat-do-and-why-thats-the-wrong-question/?cb=$RANDOM" \
  | grep -c "p=11876"   # expect 0

# Nothing else moved: word count, link count, image count against the baselines.
python3 - <<'PY'
import json, re, urllib.request
for pid, base in ((12327, 'content/drafts/2026-06-16-storyhive-haus-of-owl-jordan-dack/fix-764/12327-baseline-20260815.json'),
                  (12032, 'content/drafts/2026-05-24-what-would-chat-do-and-why-thats-the-wrong-question/fix-764/12032-baseline-20260815.json')):
    before = json.load(open(base))['content']['rendered']
    after = json.load(urllib.request.urlopen(f"https://kriskrug.co/wp-json/wp/v2/posts/{pid}?_fields=content"))['content']['rendered']
    for label, pat in (('links', r'<a '), ('images', r'<img '), ('h2', r'<h2')):
        b, a = len(re.findall(pat, before)), len(re.findall(pat, after))
        print(pid, label, b, '->', a, 'OK' if a == b else 'CHANGED')
PY
```

Word counts will move slightly on 12327, because the rewrites add a few words where a
dash became "It runs on" or "He is a". Link, image, and heading counts must not
change on either post.

## Rollback

Every applied post has a snapshot under `backup/issue-764-em-dash-404/`. The
script prints the restore command; it is:

```bash
make varlock-run CMD='python3 scripts/apply_issue_764_fix.py --restore backup/issue-764-em-dash-404/rest-post-12327-before-<stamp>.json'
make varlock-run CMD='python3 scripts/apply_issue_764_fix.py --restore backup/issue-764-em-dash-404/rest-post-12327-before-<stamp>.json --apply'
```

Restore is dry-run by default too. If the snapshot is somehow missing, the
committed `*-baseline-20260815.json` files in these `fix-764/` directories hold
the same pre-change `content.raw` and work the same way.

## Optional, KK's call, not in the payload

1. **`Eth??s Lab` → `Ethọ́s Lab` in 12327.** Real defect, visible on the page,
   an organization's name spelled with question marks. Not batched in because the
   issue says not to batch other copy changes, and because it needs its own
   verification: the NCR form is `Eth&#7885;&#769;s Lab`, and this site has a
   history of 500s on combining-diacritic REST writes to Jetpack SEO fields. If
   it 500s in the body too, fall back to plain `Ethos Lab`. To fold it in, patch
   the payload before applying (the script's payload hash guard will need
   updating to match):

   ```bash
   python3 - <<'PY'
   from pathlib import Path
   p = Path('content/drafts/2026-06-16-storyhive-haus-of-owl-jordan-dack/fix-764/12327-content-payload.html')
   t = p.read_text(encoding='utf-8')
   assert t.count('Eth??s Lab') == 1
   p.write_text(t.replace('Eth??s Lab', 'Eth&#7885;&#769;s Lab'), encoding='utf-8')
   PY
   ```

2. **The `excerpt` and `advanced_seo_description` em dashes** on 12327, one each.
   Before/after in `12327-rewrites.md`. Both are already correct in `post.md`, so
   a re-emit carries them regardless.

## Source-package sync

`post.md` and `post.html` in both packages were fixed in the same PR, so a
re-emit will not put any of this back. `post.md` also carries the excerpt and SEO
description fixes. `scripts/notion-to-wp/wp_blocks.py` was checked and contains
no em dashes. Every one of the 21 came from prose, not generated markup.

Known, untouched, pre-existing: this package's `post.html` has drifted from live
in ways unrelated to #764 (live gained a production-credit paragraph and swapped
the embedded video to the KK-channel edition). A blind re-emit from `post.html`
would undo those. Out of scope here; worth its own issue.
