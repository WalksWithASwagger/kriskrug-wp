# #339 publisher batch, re-cut against the live site on 2026-11-12

**Status:** APPROVED, NOT YET APPLIED. Kris approved all five changes in chat on 2026-11-12 (relayed by the orchestrating session), with new wording for #249 (below). The first live write, the About deploy, was stopped by the session's permission check before it ran. No WordPress write has happened, and no theme work or cache purge.
**Issue:** [#339](https://github.com/WalksWithASwagger/kriskrug-wp/issues/339), reopened 2026-11-12 (re-verification in #1221).
**Captured:** authenticated `context=edit` GETs at `2026-11-13T02:30:50Z` (evening of 2026-11-12, Pacific). Rechecked at `2026-11-13T02:50:14Z`: every `modified`, content hash and SEO value unchanged.
**Replaces:** the guards and the planned About body in [`../339-july-publisher-batch-2026-08-16/`](../339-july-publisher-batch-2026-08-16/README.md). Apply nothing from that folder. Its About FIND paragraph no longer exists after the November redesign (#1205), and the guards for posts 2950, 8802, 11171 and 12327 have moved since August.

All five updates are still needed. None is live today. Every source phrase still occurs exactly once, unlinked, and every link target returned 200 with a self-canonical on a logged-out GET.

## The five changes Kris approves

| Issue | Change |
|---|---|
| #249 | About page, "Vancouver, now" chapter: add one sentence to the end of the second paragraph: *In May 2026 I went to my first anti-AI protest and wrote about what both sides keep missing in [You Can’t Drink Data](https://kriskrug.co/2026/05/23/you-cant-drink-data/).* (Kris's wording, 2026-11-12.) |
| #328 | Link existing words to the [Most Benevolent Outcomes prayer](https://kriskrug.co/2023/11/04/the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things/) (post 3814): "Most Benevolent Outcomes" on post 2950 and "cultivating the most benevolent outcomes" on post 2665. No new words. |
| #335 | Post 35 search title `The Lord of the Rings Drinking Game: 4 Original Rules` and description `Four original Lord of the Rings drinking game rules for Frodo, Sam, Legolas, and cliff falls, plus a trilogy marathon option. Play responsibly.` The footer "See also" on posts 35 and 58 points at each other instead of the 2023 AI companions post. |
| #336 | Post 8802 search title `Build an AI Second Brain That Actually Works for You` and description `Build an AI second brain that works with your thought patterns, captures creative chaos, and turns scattered notes and voice memos into finished work.` Link existing words to post 8802: "AI as a second brain" on post 9774 and "knowledge bases and named assistants" on post 12327. |
| #342 | Post 11171: the closing "both hands full" link moves from the Notion keynote page to `https://www.bothhandsfull.com`. Anchor text unchanged. |

The #335 and #336 SEO strings are the ones approved in July. #994 (closed 2026-09-20) recommended keeping them unchanged.

## Targets and guards

Hashes are SHA-256 of `content.raw`. The exact FIND and REPLACE fragments, identity fields and hashes are in [`targets.json`](targets.json). No page bodies are stored in the repo.

| Issue | Object | Slug | `modified` guard | Current content SHA-256 | Proposed content SHA-256 |
|---|---|---|---|---|---|
| #249 | page 1208 | `about` | `2026-11-11T09:25:47` | `b11435ba9c60c06235adc0d1fdb4f824defa0b30aaa80d20bfd4ac529f6c376a` | `f826de25e0c9447524a351108b1b5d06e2d2adb8d0cdd5a40e0946ef980ad4f6` |
| #328 | post 2950 | `community-weaving-how-digital-interactions-shape-our-physical-world` | `2026-10-25T14:47:19` | `b56c4532fc5998b8711662a65b0310563893268afabaa3810089eb0d3d2f42fe` | `bd8781ad6b346ffd705ad864029b75423451fec64f90a472c7c4ba7cb6e9c2fa` |
| #328 | post 2665 | `embracing-the-future-my-journey-with-generative-ai-and-building-a-learning-community-on-discord` | `2026-06-28T20:39:43` | `0f252f0b234e09eb71766ed575f2d3541eb3376bb0c65d7508797989c22a8580` | `01785b0cb0b0db79185d542ed67adb3c3ed043bf22f4324b74ae0ecb95c47c5c` |
| #335 | post 35 | `the-lord-of-the-rings-drinking-game` | `2026-06-14T22:30:33` | `0cef531f2f03a2fe4c52c42a52aea44564d81b165c4b08334098e69251ba48a0` | `99a6d2566482863722589a7a955c6df39187bab645adf634977bcc6d4fb701e4` |
| #335 | post 58 | `mcsweeneys-lists` | `2026-06-14T22:29:25` | `7da6b58410027086db784ceaeeca764f9d5f3582e12dc24d661effb62c43b5fc` | `b45f6413ba975f5214c60ef1a8c6e6556c75f8c38cedd7bee7d1013f013206c6` |
| #336 | post 9774 | `what-journalists-need-to-know-about-ai-right-now` | `2026-06-14T20:05:53` | `cd8add62c762bec23ad6edc83a6577d2a2c215246edcf6321a4e22b938e0c82d` | `732937bbe661a4ff2fec36d62d8c495f7950fcd3b65d2c2a72c2bec5adcf4dcd` |
| #336 | post 12327 | `storyhive-haus-of-owl-jordan-dack` | `2026-09-07T13:07:06` | `5ea0fa894045b5266a511138d3444dc5a56e66fdf61b0e1edb96f20dd217527e` | `2fac7cafec6cd58c3e95ae9e7029e25fab7d8c73137cabee20b99751b4090fd7` |
| #342 | post 11171 | `both-hands-full` | `2026-09-18T04:57:44` | `8a9c2ba72f9c3743d6b09daa767c647f47e0803e99d5f99abdbade92038c0623` | `3d7000a8af5c6e0ef8cd85ccdc0d5645ce7371b26f2c8b987186d109c72dcc8c` |

SEO-only guards (from [`seo-meta-overwrite.json`](seo-meta-overwrite.json)): post 35 `modified` `2026-06-14T22:30:33`, content `0cef531f2f03a2fe4c52c42a52aea44564d81b165c4b08334098e69251ba48a0`; post 8802 `how-to-build-an-ai-second-brain-that-actually-works-for-you`, `modified` `2026-09-18T04:57:59`, content `da75b71fc03759cc368103c546622f9d377e5de6c1fd08bd1bbdcf8c45723040`.

### Marker to verify after each write

| Object | Expected in authenticated `content.raw` after the write | Public check (cache-busted) |
|---|---|---|
| page 1208 | `<a href="https://kriskrug.co/2026/05/23/you-cant-drink-data/">You Can’t Drink Data</a>` once | `/about/` has 1 `you-cant-drink-data` href (0 today) |
| post 2950 | `<a href="https://kriskrug.co/2023/11/04/the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things/">Most Benevolent Outcomes</a>` once | the words render as a link to post 3814 |
| post 2665 | the same href around `cultivating the most benevolent outcomes`, once | as above |
| post 35 | `See also: <a href="https://kriskrug.co/2004/07/16/mcsweeneys-lists/">McSweeney's Lists</a>.` once; `building-ai-companions` 0 | category archive link still present |
| post 58 | `See also: <a href="https://kriskrug.co/2004/05/27/the-lord-of-the-rings-drinking-game/">The Lord of the Rings Drinking Game</a>.` once; `building-ai-companions` 0 | category archive link still present |
| post 9774 | `<a href="https://kriskrug.co/2025/04/01/how-to-build-an-ai-second-brain-that-actually-works-for-you/">AI as a second brain</a>` once | the words render as a link to post 8802 |
| post 12327 | the same href around `knowledge bases and named assistants`, once | as above |
| post 11171 | `<a href="https://www.bothhandsfull.com">both hands full</a>` once; `keynote-both-hands-full` 0 | public HTML has 0 `keynote-both-hands-full` (1 today) |
| post 35 SEO | meta equals the proposed strings | `<title>` is `The Lord of the Rings Drinking Game: 4 Original Rules` |
| post 8802 SEO | meta equals the proposed strings | `<title>` is `Build an AI Second Brain That Actually Works for You` |

The theme prints `jetpack_seo_html_title` as the whole `<title>` (today's live titles match the stored values exactly), and `advanced_seo_description` as the standard description.

## Apply, after Kris approves

One object at a time, in this order: page 1208, posts 2950, 2665, 35, 58, 9774, 12327, 11171, then the two SEO overwrites. The SEO writes go last because a meta write bumps post 35's `modified`, which would trip the `modified` guard on its footer edit. Keep snapshots in the gitignored `.generated/current-state/339-recut-2026-11-12/` folder until public readback passes. Run every command from the repo root.

No repo CLI takes an outside find/replace spec with a `modified` guard. The two snippets below reuse existing tooling (`WPClient` from `scripts/common.py` and `update()` from `scripts/apply_issue_834_brand_links.py`). Save each one to a scratch file outside the repo and run it with `make varlock-run CMD='python3 <file>'`. Both were dry-run against the live site on 2026-11-12 with the results noted.

### 1. Guard check (read-only; run first, and again at the end)

Prints one line per object. Today all ten say `ready`. After the batch all ten should say `applied`. Any `DRIFT` stops the batch for re-review. Exit code is 1 on drift.

```python
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from common import WPClient

packet = Path("content/drafts/339-recut-2026-11-12")
targets = json.loads((packet / "targets.json").read_text())
seo = json.loads((packet / "seo-meta-overwrite.json").read_text())
client = WPClient.from_env()
drift = 0
for spec in [targets["about_page"], *targets["posts"]]:
    route = "pages" if spec["type"] == "page" else "posts"
    live = client.get(f"{route}/{spec['id']}", params={"context": "edit"})
    raw = live["content"]["raw"]
    digest = hashlib.sha256(raw.encode()).hexdigest()
    if live["slug"] != spec["slug"] or live["status"] != spec["status"]:
        state = "DRIFT"
    elif digest == spec["after_sha256"]:
        state = "applied"
    elif (
        digest == spec["before_sha256"]
        and live["modified"] == spec["modified"]
        and raw.count(spec["find"]) == 1
        and spec["href"] not in raw
    ):
        state = "ready"
    else:
        state = "DRIFT"
    drift += state == "DRIFT"
    print(spec["type"], spec["id"], live["modified"], state)
for item in seo["items"]:
    live = client.get(f"posts/{item['id']}", params={"context": "edit"})
    meta = {key: (live.get("meta") or {}).get(key) for key in item["meta"]}
    if live["slug"] != item["slug"]:
        state = "DRIFT"
    elif meta == item["meta"]:
        state = "applied"
    elif meta == item["live_before"]:
        state = "ready"
    else:
        state = "DRIFT"
    drift += state == "DRIFT"
    print("seo", item["id"], live["modified"], state)
sys.exit(1 if drift else 0)
```

### 2. #249 About, page 1208

About is repo-owned. Live `content.raw` is byte-identical to `content/source-packs/content-architecture-2026/wp-payloads/about.html` today, so apply it through that payload and keep the repo matching live.

1. `about.html` in this PR already carries the `about_page` FIND/REPLACE from `targets.json` and nothing else. `shasum -a 256` of the file is `f826de25e0c9447524a351108b1b5d06e2d2adb8d0cdd5a40e0946ef980ad4f6`. Do not merge that payload change before the live write lands, or payload parity will show drift.
2. Dry-run: `make varlock-run CMD='python3 scripts/content_architecture_deploy.py --page about'` (the script is stdlib-only, so `python3` works where the venv is missing). It printed this on 2026-11-12, and must print it again:
   `parity: about id=1208 DRIFT bytes=+185 lines=+0 first_diff_line=559 live_sha256=b11435ba9c60 payload_sha256=f826de25e0c9`
   A different `live_sha256` means the page changed: stop.
3. Write: the same command with `--execute --snapshot-dir .generated/current-state/339-recut-2026-11-12/about`. The tool checks ID, slug and status, snapshots before writing, and restores the snapshot itself if the readback loses a page marker. It does not check `modified`, so run the guard check (step 1) right before it.

### 3. Body edits on posts 2950, 2665, 35, 58, 9774, 12327, 11171

`update()` checks ID, slug, type, status, date and title, requires the current content hash to equal `before_sha256` and the result to equal `after_sha256`, requires FIND exactly once, re-reads `modified` between snapshot and write, posts `content` only, and fails if categories, tags, featured media, excerpt or meta move. The snippet adds the `modified` guard from the packet.

```python
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from apply_issue_834_brand_links import update
from common import WPClient

packet = json.loads(
    Path("content/drafts/339-recut-2026-11-12/targets.json").read_text()
)
spec = next(row for row in packet["posts"] if row["id"] == int(os.environ["ID"]))
restore = (
    json.loads(Path(os.environ["RESTORE"]).read_text())
    if os.environ.get("RESTORE")
    else None
)
client = WPClient.from_env()
live = client.get(
    f"posts/{spec['id']}", params={"context": "edit", "_fields": "modified"}
)
if restore is None and live["modified"] != spec["modified"]:
    sys.exit(f"modified guard: live {live['modified']} != packet {spec['modified']}")
folder = Path(".generated/current-state/339-recut-2026-11-12/apply")
print(
    update(client, spec, folder, apply=os.environ.get("APPLY") == "1", restore=restore)
)
```

- Dry-run: `ID=2950 make varlock-run CMD='python3 <file>'` prints the diff and `{'id': 2950, 'status': 'dry-run', 'sha256': '<after_sha256>'}`. All seven posts returned their planned `after_sha256` on 2026-11-12.
- Write: `ID=2950 APPLY=1 make varlock-run CMD='python3 <file>'`. It prints the snapshot and readback paths.

### 4. SEO overwrites on posts 35 and 8802

Both fields are non-empty on both posts, so this is an overwrite. The additive backfill would skip them.

- Dry-run: `make varlock-run CMD='make seo-backfill FROM_FILE=content/drafts/339-recut-2026-11-12/seo-meta-overwrite.json'`. It should report `planned=2 failed=0`.
- Write: the same with `EXECUTE=1`. The tool checks ID and slug, sends only the two allowlisted meta keys, reads both back, and records the prior values in its report.
- The tool does not check `modified` or the prior values, so the guard check must show both `seo` lines as `ready` right before the write.
- The file parses with the tool's own `parse_approved_entry` and both strings encode as cp1252. The tool dry-run itself was not run in this re-cut (it needs `scripts/notion-to-wp/.venv`, and its config loader can fall back to a sibling repo's legacy env file).

### 5. Readback

Run the guard check again (all `applied`), then check each public marker above with a cache-busted URL. REST edits do not purge the Pagely page cache on their own.

## Rollback

- Page 1208: `make varlock-run CMD='python3 scripts/content_architecture_deploy.py --page about --restore --snapshot-dir .generated/current-state/339-recut-2026-11-12/about'`, then revert the `about.html` commit.
- Posts: run the snippet with `ID=<id> APPLY=1 RESTORE=<that post's before snapshot>`. `update()` refuses unless live still holds the reviewed `after_sha256`.
- SEO: re-run the backfill `--from-file` with the `live_before` values as `meta`. The prior values are also in the write report.

## Left alone on purpose

- Existing em dashes in the source sentences on posts 2950 and 9774 stay as they are. This batch only wraps words.
- New copy is cp1252-safe (the database stores cp1252, PR #1273). The About sentence uses the same curly apostrophe as the rest of that page.
- Out of scope: any Aurora upload or theme change, #331, Search Console, analytics.
