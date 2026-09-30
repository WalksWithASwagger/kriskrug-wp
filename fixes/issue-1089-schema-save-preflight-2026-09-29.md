# Issue #1089 / #1104: Snippet 5 save preflight

**Track:** A — Content + SEO
**Status:** repo-side decision, verification, and rollback packet. No live WordPress write.
**Preparation issue:** #1104
**Parent save issue:** #1089 (stays open; only KK may paste)
**Manifest:** `fixes/issue-1089-schema-save-preflight-2026-09-29.json`
**SEO brief:** [Sulu comment on #1104](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1104#issuecomment-5911308754)
**Candidate file:** `fixes/schema-snippets-deployed.php` (Code Snippet 5 / KK Schema)

This packet prepares Friday 2 October save work. It does not mark the
prepared Person consolidation or Speaking `VideoObject` records live. It does
not change approved schema payload values. Pasting the current file still
ships both merged changes (#1082 Person entity + #907/#641 Speaking videos).

## Option A — recommended, not approved

Sulu recommends **option A: Person + VideoObjects together**, because both
changes are already merged and reviewed on `main`. That is a recommendation,
not approval. This packet implements option A as the reviewed candidate and
waits for KK.

| Option | What KK pastes | When to use |
|---|---|---|
| **A (recommended default)** | The current `fixes/schema-snippets-deployed.php` body, after the X and YouTube `sameAs` decisions below | Ship Person consolidation and Speaking videos in one save |
| **B (separately reviewed reduced payload)** | The same file with `kk_schema_speaking_videos()` and its `add_action` removed, then re-reviewed | Only if KK wants Person-only now and videos later |

Pasting the current file **includes both merged changes**. There is no
silent video strip. Option B is a new review, not a hidden default.

## Candidate identity

Recorded against `origin/main` at packet time. The schema bytes last changed
in #1082; later `main` commits did not touch this file.

| Field | Value |
|---|---|
| Packet `main` SHA | `6931d8ab4dcb34f579ee0d3893841c341ecad55b` |
| Schema last-change SHA | `3807e6bcaff52009eb5e6667dc3e2a8a9fb94578` (#1082, 2026-09-27) |
| File | `fixes/schema-snippets-deployed.php` |
| SHA-256 | `a6037656daabafd5afacddea3885357e5d042ff204aa5ce01222bb1b8f8db0e6` |
| Byte length | `14765` |
| Repo vs live | **Prepared, not live.** Public JSON-LD still matches the pre-#1082 / pre-#641 snippet. |

Confirm the SHA and hash immediately before any paste:

```bash
git rev-parse origin/main
git log -1 --format='%H %s' -- fixes/schema-snippets-deployed.php
sha256sum fixes/schema-snippets-deployed.php
```

If either digest differs, stop and refresh this packet.

## Live Organization `@id` from bc-ai.ca

Fetched the public homepage as anonymous cache-busted HTML. Do not invent a
new Organization id.

- Retrieval (PT): `2026-09-30T05:30:50.196067-07:00`
- Command: `curl -sL "https://bc-ai.ca/?nocache=$(date +%s)"`
- Observed Organization `@id`: **`https://bc-ai.ca/#organization`**
- Observed `name` / `legalName`: `BC + AI Ecosystem Association`

The candidate `worksFor` entry for BC + AI already uses that exact `@id`.
Live kriskrug.co still emits `BC + AI Ecosystem Industry Association` with
**no** `@id`.

## Dated logged-out readbacks

Anonymous, cache-busted `GET`s. Retrieval (PT):
`2026-09-30T05:30:50.196067-07:00`. Footer / About social scan:
`2026-09-30T05:32:54.054358-07:00`.

```bash
curl -sL -H 'Cache-Control: no-cache' \
  "https://kriskrug.co/?nocache=$(date +%s)"
curl -sL -H 'Cache-Control: no-cache' \
  "https://kriskrug.co/speaking/?nocache=$(date +%s)"
curl -sL -H 'Cache-Control: no-cache' \
  "https://kriskrug.co/2026/08/10/keep-the-machine-strange/?nocache=$(date +%s)"
curl -sL -H 'Cache-Control: no-cache' \
  "https://kriskrug.co/about/?nocache=$(date +%s)"
```

Extract JSON-LD:

```bash
python3 -c "
import sys,re,json
doc=sys.stdin.read()
for b in re.findall(r'<script[^>]*ld\+json[^>]*>(.*?)</script>',doc,re.S|re.I):
    print(json.dumps(json.loads(b), indent=2, ensure_ascii=False))
"
```

All four kriskrug.co routes returned HTTP `200`. Zero `Event` nodes. No
Futureproof festival `@id`.

### Person — live vs candidate

| Field | Live 2026-09-30 | Option A candidate | Match? |
|---|---|---|---|
| Count / `@id` | 1 × `https://kriskrug.co/#person` on home, `/speaking/`, article, `/about/` | Same single `@id` | Yes |
| `name` | `Kris Krüg` | `Kris Krüg` | Yes |
| BC + AI `name` | `BC + AI Ecosystem Industry Association` | `BC + AI Ecosystem Association` | **No — prepared** |
| BC + AI `@id` | missing | `https://bc-ai.ca/#organization` | **No — prepared** |
| Futureproof URL | `https://futureproof.website/` | `https://www.futureproof.website/` | **No — prepared** |
| Futureproof `@id` | none | none (must stay none) | Yes |
| `sameAs` | twitter.com/kriskrug, x.com/kriskrug, Instagram | approved set below; X left pending | See decision 2 |
| `image` | CDN `s5102.pcdn.co/.../krug-1.jpg` | Origin `kriskrug.co/wp-content/uploads/2023/07/krug-1.jpg` | Same asset; Jetpack CDN rewrite is live-only |

### WebSite — live vs candidate

| Field | Live homepage | Candidate | Match? |
|---|---|---|---|
| Present on `/` | yes | yes | Yes |
| Present on `/speaking/`, article, `/about/` | no | no | Yes |
| `name` | `Kris Krug` | `Kris Krug` | **Preserve. Do not change.** |
| `alternateName` | `Kris Krüg`, `kriskrug.co` | same order | Yes |
| `publisher.@id` | `https://kriskrug.co/#person` | same | Yes |

### Article references — live vs candidate

Sample: `/2026/08/10/keep-the-machine-strange/` (`BlogPosting`).

| Field | Live | Candidate |
|---|---|---|
| `author` | `{"@id":"https://kriskrug.co/#person"}` | same reference, not an inline Person |
| `publisher` | `{"@id":"https://kriskrug.co/#person"}` | same |
| Extra Person nodes | none | none |

Headline, dates, excerpt, and image stay post-owned. This packet does not
retouch article body fields.

### VideoObject — live vs candidate

| Surface | Live 2026-09-30 | Option A candidate |
|---|---|---|
| `/speaking/` | Person + BreadcrumbList only | Person + BreadcrumbList + **two** `VideoObject`s |
| `/`, article, `/about/` | no `VideoObject` | no `VideoObject` |

Each prepared video has `name`, `thumbnailUrl`, `uploadDate`, and `embedUrl`.
`about` is `{"@id":"https://kriskrug.co/#person"}`. No inline Person, Event,
creator, or publisher on those nodes.

## Decision 1 — payload shape

**Default recommendation (not approval): option A.**

Ship Person consolidation and Speaking `VideoObject`s together. Both are on
`main`. Sulu's #1104 comment recommends this and still calls it a
recommendation.

Choose option B only if KK wants a separately reviewed Person-only paste.
Do not strip videos in the save session without that review.

## Decision 2 — Twitter / X identity (TODO)

**Pending KK. Do not guess. Leave X out of the approved `sameAs` set.**

| Source | X / Twitter URL |
|---|---|
| Live Person `sameAs` | `https://twitter.com/kriskrug`, `https://x.com/kriskrug` |
| Candidate file (merged #1082) | same two URLs still present in PHP |
| Live Aurora footer | `https://twitter.com/feelmoreplants` (404 as of 2026-09-30; redirects toward `x.com/feelmoreplants`) |
| Related open issue | #1024 (`twitter:site` `@feelmoreplants` → `@kriskrug`). Footer 404 rides with #1024 and this X decision, not as a third snippet change. |

Approved `sameAs` for this packet (already linked as Kris Krüg profiles):

1. `https://www.instagram.com/kriskrug/`
2. `https://www.linkedin.com/in/kriskrug/`
3. `https://www.youtube.com/kriskrug`
4. `https://www.flickr.com/photos/kk/` (Photography page, confirmed 200)

The SEO-review JSON-LD below **omits** the two X/Twitter URLs. The PHP file
still contains them because this packet does not change approved payload
bytes. Before paste, KK must either:

- confirm `kriskrug` and keep both URLs, or
- name a different handle, or
- strip `https://twitter.com/kriskrug` and `https://x.com/kriskrug` until that
  choice is made.

Do not add any other profile in this save unless Decision 3 explicitly
chooses to list both YouTube URLs.

## Decision 3 — YouTube `sameAs` (TODO)

**Pending KK. Keep, swap, or both. This packet does not change the approved
`sameAs` set.**

Sulu's soft LGTM on #1111 keeps `https://www.youtube.com/kriskrug` in the
approved set. Live checks ~05:45 PT on 2026-09-30:

| URL | HTTP | Resolves to | Notes |
|---|---|---|---|
| `https://www.youtube.com/kriskrug` | 200 | `@kriskrugdotcom` ("kris krüg") | Current approved / candidate value |
| `https://www.youtube.com/kriskrug10000` | 200 | `@feelmoreplants` ("Kris Krüg") | Hosts Speaking video `-c7mgY2aSgM` ("Both Hands Full…") |

Both channels look like KK's. Adding `/kriskrug10000` is a **new** `sameAs`
profile. It does not ride in on the #1109 footer change, and this packet
does not add it.

KK chooses one:

- **Keep** `https://www.youtube.com/kriskrug` (packet default; approved set unchanged)
- **Swap** to `https://www.youtube.com/kriskrug10000` (new profile; requires an explicit paste-time edit)
- **Both** (new profile added beside the current URL; requires an explicit paste-time edit)

Until KK chooses, paste the approved set as recorded here.

## Snippet 5 identity, scope, and activation

Complete these in wp-admin immediately before snapshot. This session had no
WordPress credentials (`make doctor` unresolved WP auth; Code Snippets REST
is 401 without an app password). **Authenticated snippet readback and the
private source snapshot stay pending for KK.**

1. Confirm snippet **ID 5** is still the active global PHP owner named
   `KK Schema` (or record the live name if it differs).
2. Confirm scope is sitewide PHP, active = true, and no second JSON-LD
   snippet is also emitting Person / WebSite.
3. Compare the live body to the last known pre-#1082 shape (live public
   JSON-LD above). Public output is **not** a recoverable source snapshot.
4. Stop if ID, scope, language, or a second owner does not match.

## Private pre-save snapshot checklist

Do this in a private note or local file. Do **not** commit the live snippet
body or hashes that would leak credentials.

- [ ] Full snippet body copied (every character, including comments)
- [ ] Snippet ID, name, active flag, scope, language
- [ ] SHA-256 of the captured body
- [ ] Capture timestamp (PT) and operator
- [ ] Confirmation that no one else is editing snippet 5
- [ ] Snapshot location recorded on #1089 (path only, not the body)

If any box is unchecked, do not paste.

## Save-once steps

Only KK, and only after all three decisions.

1. Snapshot as above.
2. Open `fixes/schema-snippets-deployed.php` at the SHA recorded here (or a
   newer SHA that still hashes identically).
3. Apply the X/`sameAs` decision. If X is still unset, delete the two
   twitter/x lines before paste.
4. Apply the YouTube `sameAs` decision. If unset, keep
   `https://www.youtube.com/kriskrug` only. Swap or both is a paste-time
   edit, not a change to this packet's approved set.
5. Paste into snippet 5. Strip only the opening `<?php` tag. Code Snippets
   wraps the file.
6. Save **once**. Do not edit another snippet, page, title, or theme.
7. Do not add `data-jetpack-boost="ignore"`; Boost stamps it at output.

## Post-save readback

Run authenticated snippet readback, then anonymous cache-busted GETs on `/`,
`/speaking/`, `/about/`, and
`https://kriskrug.co/2026/08/10/keep-the-machine-strange/`. Record retrieval
time in PT.

Expected assertions:

- Exactly one Person node per page, `@id` `https://kriskrug.co/#person`
- `worksFor` BC + AI `@id` is exactly `https://bc-ai.ca/#organization`
- `sameAs` is only the approved set, plus X and/or `/kriskrug10000` only if KK confirmed them
- `WebSite` on the homepage only; `name` remains `Kris Krug`
- Article `author` and `publisher` still reference `#person` (no inline Person)
- Two `VideoObject`s on `/speaking/` only, each with `name`, `thumbnailUrl`,
  `uploadDate`, and `embedUrl` or `contentUrl`
- Zero `Event` nodes; zero Futureproof festival `@id`
- Every `application/ld+json` block parses as JSON

## Schema Markup Validator

Use https://validator.schema.org/ on:

1. Homepage — Person + WebSite; `WebSite.name` is `Kris Krug`
2. `/speaking/` — Person + two VideoObjects; no Event
3. The sample article — Person + BlogPosting; author/publisher are `@id` refs

Do **not** treat Google Rich Results Test as the site-name check. Schema
Markup Validator is the site-name tool.

Stop and roll back if validator errors appear, JSON fails to parse, Person
count exceeds one, `WebSite.name` changes, videos leak off `/speaking/`, an
`Event` appears, or a Futureproof festival `@id` appears.

## Rollback

1. Detect unexpected concurrent snippet 5 edits by comparing the live body
   hash to the private snapshot and to this packet's candidate hash. If a
   third hash appeared, someone else edited snippet 5 — stop and reconcile
   before restoring.
2. Restore the captured snippet 5 source **and** its prior active/scope/name
   state. Do not restore a different snippet.
3. Purge only the affected cache surface (snippet/page cache and any CDN
   page cache for `/`, `/speaking/`, `/about/`, and the sample article).
4. Repeat authenticated and anonymous cache-busted readback.
5. Confirm public JSON-LD matches the pre-save live shape recorded here.

## Completed vs pending

| Item | State |
|---|---|
| Public cache-busted JSON-LD readbacks | **Done** 2026-09-30, PT timestamps above |
| bc-ai.ca Organization `@id` readback | **Done** — `https://bc-ai.ca/#organization` |
| Candidate SHA + file hash | **Done** against `6931d8ab4dcb34f579ee0d3893841c341ecad55b` |
| Option A recommendation recorded | **Done** — not approval |
| X/Twitter choice | **Pending KK** — omitted from approved `sameAs` |
| YouTube `sameAs` (keep / swap / both) | **Pending KK** — approved set still `https://www.youtube.com/kriskrug` only |
| Authenticated snippet 5 body/scope snapshot | **Pending KK** — no WP credentials in this session |
| WordPress save | **Pending KK under #1089** |
| Validator receipts | **Pending** — do not invent results |
| `fixes/README.md` "live" header/date | **Pending** follow-up after a verified save |

## Hard exclusions

- No `Event` nodes on kriskrug.co
- No Futureproof festival `@id` (Futureproof stays a `worksFor` Organization
  with a URL only; the Event lives on futureproof.website)
- No `WebSite.name` change
- No live WordPress write from this child issue
- No new `sameAs` profiles
- No sitemap, theme, or footer work in this packet

## See also

- `fixes/issue-316-schema-identity-handoff-2026-07-13.md` — approved `WebSite.name`
- `fixes/issue-641-speaking-video-schema-handoff-2026-08-27.md` — Speaking videos
- `fixes/README.md` Table A row for snippet 5
