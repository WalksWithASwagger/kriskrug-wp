# #364 Hub-link wraps — execution checklist (PREP ONLY)

**Captured:** `2026-07-26T22:37:28Z`  
**Branch intent:** `cursor/364-hub-link-wraps-prep-f196`  
**Lane:** Track A — Content + SEO  
**Live writes this session:** none (no `WP_USER` / `WP_APP_PASSWORD`; no REST PATCH)

## Verdict

Most of the #284 review-ready batch is **already live** from the 2026-07-24 apply (`content/drafts/2026-07-24-issue-284-apply.json`, #284 closed). Public readback on 2026-07-26 confirms exact hub wrappers on posts **12035**, **12257**, **2781**, and **12030**.

**Residual write for a future approved session:** only `11905-indigenous-ai` (still bare; still human-gated). Do not re-apply already-wrapped needles.

## Source packets

| Artifact | Path |
|---|---|
| Handoff MD | `fixes/issue-284-topic-hub-links-handoff-2026-07-12.md` |
| Handoff JSON | `fixes/issue-284-topic-hub-links-handoff-2026-07-12.json` |
| Unit tests | `scripts/tests/test_issue_284_topic_hub_links_handoff.py` |
| Prior agent-ready note | `docs/current-state/reports/issue-364-hub-links-ready-20260716.md` |
| Pre-apply public recheck | `docs/current-state/reports/issue-284-public-recheck-20260716.md` |
| Apply receipt | `content/drafts/2026-07-24-issue-284-apply.json` |
| Repo draft mirror (11905) | `content/drafts/2026-05-13-sovereign-ai-for-whom/` |

Related issues: [#364](https://github.com/WalksWithASwagger/kriskrug-wp/issues/364) (open execute gate), [#284](https://github.com/WalksWithASwagger/kriskrug-wp/issues/284) (closed; packet + 2026-07-24 apply), #278 (parent hub work).

---

## 1. Live public truth (2026-07-26 recheck)

Method: public WP REST by exact slug + normalized hub href counts in `content.rendered`. No auth. No writes.

### Hub targets (unchanged identity)

| Hub | ID | Slug | URL | `modified` | HTTP |
|---|---:|---|---|---|---|
| AI Ethics | 12318 | `ai-ethics` | https://kriskrug.co/ai-ethics/ | `2026-07-01T12:27:51` | 200 |
| AI Tools | 12321 | `ai-tools` | https://kriskrug.co/ai-tools/ | `2026-07-01T12:27:55` | 200 |
| Indigenous AI | 12322 | `indigenous-ai` | https://kriskrug.co/indigenous-ai/ | `2026-07-01T12:28:09` | 200 |

### Source href counts + wrap status

| ID | Slug | Live counts `(ethics, tools, indigenous)` | Live `modified` | Wrap status |
|---:|---|---|---|---|
| 5723 | `unpacking-ai-ethics-…` | 3 / 0 / 0 | `2026-06-28T20:34:21` | no-op (pre-existing) |
| 5489 | `cognitive-ai-creativity-…` | 1 / 0 / 0 | `2026-06-28T20:34:50` | no-op |
| 4635 | `bridging-innovation-…` | 2 / 0 / 0 | `2026-07-01T16:24:10` | no-op |
| 4773 | `creative-toolbox` | 0 / 1 / 0 | `2026-06-14T20:08:44` | no-op |
| 3275 | `how-ai-tools-like-midjourney-…` | 0 / 1 / 0 | `2026-06-14T20:34:30` | no-op |
| 7450 | `indigenomics-now-2024-…` | 1 / 0 / 1 | `2026-06-28T20:31:08` | footer-only no-op (kept) |
| **12035** | `ai-wont-fix-your-broken-permit-process` | 0 / **1** / **1** | `2026-07-24T14:40:28` | **DONE** `12035-ai-tools`, `12035-indigenous-ai` |
| **12257** | `why-we-built-the-responsible-ai-…` | **1** / 0 / **1** | `2026-07-24T14:40:40` | **DONE** `12257-ai-ethics`, `12257-indigenous-ai` |
| **2781** | `audio-deep-fakes-…` | 0 / **1** / 0 | `2026-07-24T14:40:23` | **DONE** `2781-ai-tools` |
| **12030** | `canada-doesnt-need-a-bigger-ai-…` | **1** / **1** / **1** | `2026-07-24T14:40:27` | **DONE** ordinary + `12030-indigenous-ai` |
| **11905** | `sovereign-ai-for-whom` | 0 / 0 / **0** | `2026-07-01T16:24:30` | **RESIDUAL** bare `host Nation governance` |

### Apply receipt vs live

`2026-07-24-issue-284-apply.json` recorded `12257` ordinary as `MISSING` / `ok: false`. Live HTML now has the exact wrapper:

```html
<a href="https://kriskrug.co/ai-ethics/">ethical practice</a>
```

Treat ordinary + indigenous wraps on 12035 / 12257 / 2781 / 12030 as **already applied**. Do not PATCH them again.

---

## 2. Approval gates (must all pass before any write)

### Gate A — Credentials

- Process env has `WP_USER` and `WP_APP_PASSWORD` (Cloud secrets or Varlock inject).
- Redacted presence check only (`WP_USER` length). Never print secrets.
- Soft check: `make env-check` when `varlock` is on `PATH`.

### Gate B — KK patch_id approval (attach to #364)

Paste an explicit list. Suggested shapes:

**Closeout-only (recommended default given live state):**

```text
VERIFY-ONLY (no writes):
  12035-ai-tools
  12257-ai-ethics
  2781-ai-tools
  12030-ai-ethics
  12030-ai-tools
  12035-indigenous-ai
  12257-indigenous-ai
  12030-indigenous-ai
  7450 keep-footer-no-op

WRITE (optional, separate Indigenous GO):
  11905-indigenous-ai   # approve | revise | skip
```

**If KK wants a fresh write batch from the original packet:** refuse unless public recheck shows bare needles again. Re-wrapping already-linked text is unsafe.

### Gate C — Fresh live-write go-ahead

Even after editorial approval, require a fresh explicit “GO” in the publisher session (packet rule + #364 acceptance).

### Gate D — Stale-guard refresh

Original handoff `source_modified_guard` values are **stale** for edited posts. Before any residual write on **11905**, re-fetch and lock:

| Field | Expected now (public) |
|---|---|
| ID | `11905` |
| Slug | `sovereign-ai-for-whom` |
| Status | `publish` |
| `modified` guard | `2026-07-01T16:24:30` (abort if different) |
| Target indigenous-ai ID/slug | `12322` / `indigenous-ai` |
| Current indigenous href count | `0` |
| Exact needle count outside anchors | `1` for `host Nation governance` |

---

## 3. Residual wrap payload (only if KK approves `11905-indigenous-ai`)

| Field | Value |
|---|---|
| `patch_id` | `11905-indigenous-ai` |
| Source ID | `11905` |
| Source URL | https://kriskrug.co/2026/06/16/sovereign-ai-for-whom/ |
| Target | https://kriskrug.co/indigenous-ai/ |
| Operation | `wrap_exact_text` |
| Needle | `host Nation governance` |
| Replacement | `<a href="https://kriskrug.co/indigenous-ai/">host Nation governance</a>` |
| Expected before href count | `0` |
| Expected after href count | `1` |
| Copy change | none (wrap only) |

Public context (rendered, 2026-07-26):

> …The other hand is holding ethics: consent, inclusion, **host Nation governance**, fair pay for the people whose work trains the models…

Editorial caution (from handoff): hub must not substitute for Nation-led sources or imply authority over host Nation governance. KK chooses approve / different destination / revise / skip.

**Out of residual scope:** 7450 (keep footer), all ordinary wraps, indigenous wraps already live on 12030 / 12035 / 12257.

---

## 4. Snapshot requirements (per source write)

Path template from handoff:

`backup/<UTC>-issue-284-topic-hub-links/source-<id>/`

Required files before PATCH:

| File | Contents |
|---|---|
| `before-edit.json` | Authenticated `GET /wp-json/wp/v2/posts/<id>?context=edit` |
| `before-content.raw.html` | `content.raw` only |
| `before-public.html` | Cache-busted public HTML |
| `before-sha256sums.txt` | SHA-256 of the above |
| `rollback-content-only.json` | `{"content":"<exact before content.raw>"}` |

Also record: ID, slug, status, title, `modified`, taxonomy IDs, featured media — for non-content drift checks after write.

Historical note: #284 comment cites snapshots under `/private/tmp/kk-284-snapshots/` (not in repo). Re-snapshot any source before a new write; do not rely on that path in Cloud.

---

## 5. Dry-run / command plan (no execute without Gate A–D)

### 5a. Credential-free public recheck (safe anytime)

```bash
# Href + modified smoke for residual + already-applied sources
python3 - <<'PY'
import json, re, urllib.request
from html import unescape

HUBS = {
  "ai_ethics": "https://kriskrug.co/ai-ethics/",
  "ai_tools": "https://kriskrug.co/ai-tools/",
  "indigenous_ai": "https://kriskrug.co/indigenous-ai/",
}
SLUGS = [
  "ai-wont-fix-your-broken-permit-process",
  "why-we-built-the-responsible-ai-professional-certification",
  "audio-deep-fakes-ai-chatbots-and-new-web-development-tools",
  "canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one",
  "sovereign-ai-for-whom",
  "indigenomics-now-2024-redefining-the-future-of-indigenous-economic-and-digital-sovereignty-through-ai",
]

def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "kk-364-recheck/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

def counts(html):
    out = {k: 0 for k in HUBS}
    for m in re.finditer(r'href=["\']([^"\']+)["\']', html, re.I):
        h = unescape(m.group(1)).split("?")[0].split("#")[0]
        if not h.endswith("/"):
            h += "/"
        for k, t in HUBS.items():
            if h == t:
                out[k] += 1
    return out

for slug in SLUGS:
    p = get_json(
        f"https://kriskrug.co/wp-json/wp/v2/posts?slug={slug}"
        "&_fields=id,slug,modified,link,content"
    )[0]
    print(p["id"], p["modified"], counts(p["content"]["rendered"]), p["link"])
PY
```

Expected residual line: `11905` → indigenous count `0`, needle bare.

### 5b. Authenticated snapshot + dry payload (creds required; still no PATCH)

```bash
# Requires WP_USER + WP_APP_PASSWORD in env (or: make varlock-run CMD='…')
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
SRC=11905
DIR="backup/${STAMP}-issue-284-topic-hub-links/source-${SRC}"
mkdir -p "$DIR"

curl -sS -u "$WP_USER:$WP_APP_PASSWORD" \
  "https://kriskrug.co/wp-json/wp/v2/posts/${SRC}?context=edit" \
  -o "$DIR/before-edit.json"

python3 - <<PY
import json, hashlib
from pathlib import Path
d = Path("$DIR")
edit = json.loads((d / "before-edit.json").read_text())
assert edit["id"] == 11905
assert edit["slug"] == "sovereign-ai-for-whom"
assert edit["status"] == "publish"
assert edit["modified"] == "2026-07-01T16:24:30"
raw = edit["content"]["raw"]
assert raw.count("host Nation governance") == 1
assert '<a href="https://kriskrug.co/indigenous-ai/">host Nation governance</a>' not in raw
(d / "before-content.raw.html").write_text(raw)
(d / "rollback-content-only.json").write_text(json.dumps({"content": raw}, ensure_ascii=False))
print("guards OK; snapshot raw written")
PY

curl -sS "https://kriskrug.co/2026/06/16/sovereign-ai-for-whom/?nocache=$STAMP" \
  -o "$DIR/before-public.html"

(
  cd "$DIR" && sha256sum before-edit.json before-content.raw.html before-public.html \
    > before-sha256sums.txt
)

# Build proposed body locally (dry) — do NOT send yet
python3 - <<'PY'
import json
from pathlib import Path
import os
d = Path(os.environ["DIR"])
raw = (d / "before-content.raw.html").read_text()
needle = "host Nation governance"
repl = '<a href="https://kriskrug.co/indigenous-ai/">host Nation governance</a>'
assert raw.count(needle) == 1
after = raw.replace(needle, repl, 1)
assert after.count(repl) == 1
assert after.count('href="https://kriskrug.co/indigenous-ai/"') == \
       raw.count('href="https://kriskrug.co/indigenous-ai/"') + 1
(d / "proposed-content.raw.html").write_text(after)
(d / "proposed-content-only.json").write_text(json.dumps({"content": after}, ensure_ascii=False))
print("dry payload ready:", d / "proposed-content-only.json")
PY
```

Set `DIR` in the environment for the second Python block, or inline the path.

### 5c. Live body-only PATCH (FORBIDDEN until Gate A–D + KK GO)

```bash
# ONLY after explicit KK GO for patch_id 11905-indigenous-ai
curl -sS -u "$WP_USER:$WP_APP_PASSWORD" \
  -X POST "https://kriskrug.co/wp-json/wp/v2/posts/11905" \
  -H "Content-Type: application/json" \
  --data-binary @"$DIR/proposed-content-only.json"
```

REST body boundary: **only** top-level key `content`. Forbidden: `title`, slug, status, dates, taxonomy, meta, excerpt, author, featured media, comments, template, format, sticky, password.

### 5d. Immediate readback + smoke

1. Authenticated `context=edit`: ID/slug/status/title/dates/tax/meta unchanged; wrapper appears once in `content.raw`.
2. Public source HTML: HTTP 200; exactly one `https://kriskrug.co/indigenous-ai/` href for this new wrap (total indigenous count `1`).
3. Hub URLs HTTP 200: `/ai-ethics/`, `/ai-tools/`, `/indigenous-ai/`.
4. Homepage + `/blog/` HTTP 200.
5. On any failure: POST `rollback-content-only.json` to the same ID; verify before counts; stop.

### 5e. Verify-only smoke for already-applied wraps

Confirm each expected exact anchor once:

| `patch_id` | Source URL | Expected substring |
|---|---|---|
| `12035-ai-tools` | `/2026/06/24/ai-wont-fix-your-broken-permit-process/` | `<a href="https://kriskrug.co/ai-tools/">AI tools</a>` |
| `12035-indigenous-ai` | same | `<a href="https://kriskrug.co/indigenous-ai/">Indigenous leadership</a>` |
| `12257-ai-ethics` | `/2026/06/18/why-we-built-the-responsible-ai-professional-certification/` | `<a href="https://kriskrug.co/ai-ethics/">ethical practice</a>` |
| `12257-indigenous-ai` | same | `<a href="https://kriskrug.co/indigenous-ai/">Indigenous ceremony</a>` |
| `2781-ai-tools` | `/2023/07/30/audio-deep-fakes-ai-chatbots-and-new-web-development-tools/` | `<a href="https://kriskrug.co/ai-tools/">the entire field of AI technology</a>` |
| `12030-ai-ethics` | `/2026/06/26/canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one/` | `<a href="https://kriskrug.co/ai-ethics/">AI ethics</a>` |
| `12030-ai-tools` | same | `<a href="https://kriskrug.co/ai-tools/">community-built tools</a>` |
| `12030-indigenous-ai` | same | `<a href="https://kriskrug.co/indigenous-ai/">Indigenous data sovereignty and stewardship</a>` |

---

## 6. Ordered execution checklist (post-approval)

1. [ ] Attach KK `patch_id` decision list to #364 (verify-only set ± optional `11905-indigenous-ai`).
2. [ ] Confirm secrets present; abort if missing.
3. [ ] Re-run public recheck (§5a); abort on unexpected drift vs this report.
4. [ ] If **no** write approved: document verify-only smoke results; close #364 as applied/verified with residual disposition for 11905.
5. [ ] If `11905-indigenous-ai` approved: snapshot (§4 / §5b); abort if guards fail.
6. [ ] Review full body diff; ensure only the one wrap changes.
7. [ ] Body-only PATCH (§5c); immediate readback (§5d).
8. [ ] Update before/after manifest with **observed** counts (not projected).
9. [ ] No taxonomy / menu / theme / title changes.
10. [ ] Comment on #364 with snapshot path, patch_ids applied, public href counts.

---

## 7. Acceptance mapping (#364)

| Acceptance item | Status as of this prep |
|---|---|
| KK approval list attached (which `patch_id`s) | **Still required** on #364 |
| Snapshots retained | Prior apply used `/private/tmp/kk-284-snapshots/` (outside repo); re-snapshot before any new write |
| Public href counts match expected-after | Ordinary + most indigenous **match live**; residual 11905 still `0→1` only if approved |
| No taxonomy/menu/theme changes | Required for any residual write |

---

## 8. Blockers / stop conditions (now)

1. Cloud `WP_USER` / `WP_APP_PASSWORD` unset in this session → no authenticated dry-run or write.
2. No KK `patch_id` list attached to #364 yet (2026-07-24 agent comment still open).
3. Residual row is Indigenous AI → separate per-row editorial GO required even though #284 had a blanket apply for other rows.
4. Re-applying already-wrapped sources is **out of scope** and unsafe.

---

## 9. Suggested #364 closeout paths

**Path V — Verify & close (no further write):** KK confirms verify-only list; agent runs §5e; leaves `11905` as skip or separate issue; close #364.

**Path W — Residual Indigenous wrap:** KK explicitly approves `11905-indigenous-ai`; agent runs §5b–§5d with secrets; then close #364.

This prep document does **not** choose Path V or W and does **not** perform live WordPress writes.
