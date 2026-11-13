# Snippet 5 JSON_HEX_TAG release: November 12, 2026

Kris approved one live write in chat on November 12: saving the
[#1238](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1238)
hardening to active global Code Snippet **5, KK Schema**. It was saved through
Varlock at **2026-11-13 02:51:42 UTC** (November 12, 18:51 Vancouver). One POST
sent `code` only. Name, scope, priority (10), active state and the other
snippet fields were not sent and did not change.

## What changed

One line in `kk_schema_emit()`:

```
- . wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE)
+ . wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG | JSON_HEX_AMP)
```

`<`, `>` and `&` inside JSON-LD values now print as `\u003C`, `\u003E` and
`\u0026`, so a title or excerpt containing `</script>` can no longer close the
block early. Parsed JSON is unchanged, and URLs and names stay readable
because the slash and unicode flags stay.

The saved code is the live code with that one line swapped. Everything from
`function kk_schema_constants()` onward is byte-identical to
`fixes/schema-snippets-deployed.php` on `main`. The live header is the #1082
header (commit `3807e6b`) as the 2026-10-25 save stored it, so its comments
still say `LAST VERIFIED AGAINST LIVE: 2026-08-16` and `PREPARED, NOT LIVE`.
That header plus the repo runtime rebuilds the after hash below exactly. The
repo header differs in comments only, so it was not saved.

## Hashes

| Code | SHA-256 | Bytes |
|---|---|---:|
| Before, live since 2026-10-26 00:15:37 UTC | `b205b7b3f23d8164828d88e57bbc169c2e20f579fb45f468a2d8f1b8d29e6b1f` | 14,759 |
| After, sent and stored | `37ac8d9e1939abcdd652c8cc01d6e32f9c730ec767f7fa0148ed9d54c2ac7c92` | 14,789 |
| Runtime before | `c973458a7d6d414cd4aa82e044c55a1bc1c93c7fd742225f842b596ce13461fc` | |
| Runtime after, equal to the repo | `b184a513afba2bb8ab21403ff9d62d49c4513018356023a400652cadddeacce7` | |

The before hash is the code the [#1089 release](schema-1089-release-2026-10-25.md)
saved, so nothing had drifted in between. The
[machine-readable receipt](snippet-5-hextag-verification-2026-11-12.json)
records these hashes and every check below.

## Verification

- Snapshot before the save: id 5, name, active, global scope and no code
  error; the exact #1089 hash; the runtime equal to the repo with the two
  flags swapped back; and snippet 5 the only active JSON-LD snippet of 26. A
  dry run read it all again just before the POST.
- After the save, the authenticated readback equals the sent code exactly.
  `code_error` is null, the 11 metadata fields match the snapshot, and the
  other 25 snippets did not change.
- Logged-out GETs before and after, normal and `?cb=` cache-busted, on `/`,
  `/speaking/` and `/2026/11/09/who-gets-a-say-canada-ai-future-canada-now/`.
  Every JSON-LD block parses, each page has as many parsed blocks as opening
  tags, no block holds a raw `</script>`, and the `@type` values match the
  before state. Home has Person and WebSite; Speaking has Person,
  BreadcrumbList and two VideoObjects; the post has Person, BlogPosting and
  BreadcrumbList. Parsed JSON is identical before and after on every route.
- Home and Speaking have no `<`, `>` or `&` in their JSON-LD, so their bytes
  did not change. The post's two `&` characters (a Photon image query string
  and the "Conversations &amp; Interviews" section name) print as `\u0026` on
  the cache-busted request, which shows the new flags running.
- Schema Markup Validator, fetching cache-busted URLs: **0 errors and 0
  warnings** on all three routes. Home has 4 objects, Speaking 3 including
  both VideoObjects, and the post 5.
- Not run: Google Rich Results Test, which needs a browser session. Schema
  Markup Validator remains this site's schema check, as in #1089.

## Cache

No purge write was made. Home and Speaking serve the same JSON-LD bytes
either way. Right after the save, the post's normal URL still returned the
pre-save bytes: the same parsed JSON, with the two `&` unescaped. Its headers
show `x-gateway-cache-status: HIT` and `x-jetpack-boost-cache: miss`, so that
copy came from the Pagely gateway cache, not from Jetpack Boost. Saving a code
snippet does not purge it. The parsed JSON is the same either way, so no purge
was needed.

## Rollback

Rolling back means saving the snapshot code back to snippet 5. That is a live
write and needs Kris's go-ahead. The private packet in the ignored
`.generated/current-state/snippet-5-hextag-2026-11-12/` folder holds
`snippet-5-before.php` (SHA-256 `b205b7b3...6b1f`), the saved candidate, the
JSON readbacks and the public HTML. Its `snippet5.py rollback` mode, run
through Varlock, restores the before code only while live still equals the
after hash and the metadata still matches the snapshot. It also compares the
repo runtime with live, so point its `--repo` at a checkout of the #1305 merge
commit (`25aa5e9`), whose runtime hashes to `b184a513...ce7`. A checkout with a
later runtime edit makes it refuse.
