# #764 APPLY — posts 12327 + 12032

**Applied 2026-08-17T05:03Z.** Live REST: 12327 body U+2014 = 0; 12032 `?p=11876` = 0. `Eth??s Lab` left as-is. Snapshot dir `backup/issue-764-em-dash-404/`. Script remains dry-run by default; `--apply` is the write switch.

Long-form notes: [RUNBOOK.md](RUNBOOK.md). 12032 files live next door at
`content/drafts/2026-05-24-what-would-chat-do-and-why-thats-the-wrong-question/fix-764/`.

## Live reconfirm (logged-out, 2026-08-17T02:39:11Z)

| Check | Result | Still a defect? |
|---|---|---|
| `GET /wp-json/wp/v2/posts/12327` `content.rendered` U+2014 | **21** (0 × `&mdash;`) | yes |
| same body contains `Eth??s` | **1** (`Eth??s Lab`) | yes, **out of payload** |
| `GET /wp-json/wp/v2/posts/12032` contains `?p=11876` | **1** | yes |
| `https://kriskrug.co/?p=11876` | **404** | expected (11876 is private) |
| 11876 permalink `/2026/06/11/the-75-percent-rule-ai-art-adjacent-work/` | **404** (rechecked 2026-08-17T02:40Z) | expected |
| live `content.rendered` sha256 vs 2026-08-15 baseline | **identical** on both posts | apply-ready |

Public HTML of 12327 can show more em dashes than 21 (theme chrome). The issue
gate is REST `content.rendered`. Do not re-derive from the full page.

`content.raw` is auth-only. The apply script hash-checks it via `context=edit`.
Rendered-hash match today is the logged-out proof the bodies have not drifted.

## Identity (slug check before any write)

| ID | Expected slug | Public URL | `modified_gmt` today |
|---|---|---|---|
| 12327 | `storyhive-haus-of-owl-jordan-dack` | `/2026/06/17/storyhive-haus-of-owl-jordan-dack/` | `2026-07-18T19:20:49` |
| 12032 | `what-would-chat-do-and-why-thats-the-wrong-question` | `/2026/06/28/what-would-chat-do-and-why-thats-the-wrong-question/` | `2026-08-01T20:00:50` |

Abort if either ID's live slug differs. Incident rule: never PATCH on ID alone.

## Endpoints (script-owned; do not curl PATCH by hand)

Base: `https://kriskrug.co`

| Step | Method | URL | Body |
|---|---|---|---|
| identity + raw hash | GET | `/wp-json/wp/v2/posts/{id}?context=edit` | — |
| apply | POST | `/wp-json/wp/v2/posts/{id}?context=edit` | `{"content": <payload html>}` |
| verify | GET | `/wp-json/wp/v2/posts/{id}?context=edit` | — |
| logged-out gate | GET | `/wp-json/wp/v2/posts/{id}?_fields=content` | — |

Only `content` is written. Title, excerpt, SEO meta, categories, featured media,
and dates stay untouched.

## Payloads + hashes (must still match `scripts/apply_issue_764_fix.py`)

| ID | Payload | payload sha256 | baseline sha256 (`content.raw`) |
|---|---|---|---|
| 12327 | `12327-content-payload.html` | `045c697906260becae376d39fcf0987911ac9c94e5d3b25def8a4f1b4a69981d` | `e29a7e8e0f7c47d8ffe157c09003b3c5ff71832341b3956dfa1b662daee5773a` |
| 12032 | `../../2026-05-24-what-would-chat-do-and-why-thats-the-wrong-question/fix-764/12032-content-payload.html` | `28d87a5d2817579e18bedc67fd4914cf70bbb1c3d8ed4e59e073aaa70da26b9d` | `f2b4374560746f10d8c5e1c7eb1b347ff73745f9032a5931691c523536036ddb` |

Baselines: `*-baseline-20260815.json` (full `context=edit` capture). Fallback
rollback source if a live snapshot is missing.

12032 change is one Related-block line: `?p=11876` ("The 75% Rule") →
`https://kriskrug.co/2026/06/17/storyhive-haus-of-owl-jordan-dack/`
("Send AI After the Art-Adjacent Work"). 11876 has no public permalink.

Neither payload has a codepoint above U+00FF. No NCR encoding required.
`Eth??s Lab` is **left as-is** (issue: do not batch other copy).

## Commands (resolved creds via Varlock)

```bash
# Offline safety tests (no network, no WP).
python3 -m unittest scripts.tests.test_apply_issue_764_fix

# Dry run: authenticated GET + printed diffs. No snapshot, no POST.
make varlock-run CMD='python3 scripts/apply_issue_764_fix.py'

# Apply only after KK approves that diff.
make varlock-run CMD='python3 scripts/apply_issue_764_fix.py --apply'
```

`--post-id 12327` or `--post-id 12032` limits to one post. Re-run after a
successful apply prints `[SKIP]`.

Preflight (all must hold, else abort): ID→slug match, live `content.raw`
sha256 == baseline, payload file sha256 == recorded. `--apply` re-GETs every
pending target before the first snapshot/POST, then again immediately before
each POST.

Snapshot dir (mode 0700, files 0600):
`backup/issue-764-em-dash-404/rest-post-<id>-before-<stamp>.json`

## Rollback

```bash
make varlock-run CMD='python3 scripts/apply_issue_764_fix.py --restore backup/issue-764-em-dash-404/rest-post-<id>-before-<stamp>.json'
make varlock-run CMD='python3 scripts/apply_issue_764_fix.py --restore backup/issue-764-em-dash-404/rest-post-<id>-before-<stamp>.json --apply'
```

Restore is dry-run by default. It refuses snapshots outside {12327, 12032},
wrong slug, or body hash ≠ baseline. If the live snapshot is gone, restore
from the committed `*-baseline-20260815.json` the same way.

## After-apply logged-out gates

```bash
# expect 0
curl -s "https://kriskrug.co/wp-json/wp/v2/posts/12327?_fields=content" \
  | python3 -c "import json,sys;print(json.load(sys.stdin)['content']['rendered'].count(chr(8212)))"

# expect 0 then 1
curl -s "https://kriskrug.co/wp-json/wp/v2/posts/12032?_fields=content" \
  | python3 -c "import json,sys;c=json.load(sys.stdin)['content']['rendered'];print(c.count('?p=11876'),c.count('/2026/06/17/storyhive-haus-of-owl-jordan-dack/'))"
```

Pagely ARES purges on post save. Prove the public edge with a cache-busted
anonymous curl (`?cb=$RANDOM`). Link / image / h2 counts must not change;
see RUNBOOK.md.

## Out of payload (do not fold in)

1. `Eth??s Lab` on 12327 — NCR `Eth&#7885;&#769;s Lab` or ASCII `Ethos Lab`; own verification.
2. One em dash each in 12327 `excerpt` and `meta.advanced_seo_description` (already fixed in `post.md`).
