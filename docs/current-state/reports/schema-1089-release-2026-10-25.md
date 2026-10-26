# Snippet 5 schema release — October 25, 2026

Kris explicitly directed the #1089 save through Varlock on October 25. This
supersedes the older instruction assigning the save to Kris. Active global
Snippet **5, KK Schema**, was saved at **5:15:37 p.m. PDT**
(`2026-10-26T00:15:37Z`). Authenticated readback matches the approved combined
Person and Speaking VideoObject payload exactly, with only its opening PHP
tag removed for Code Snippets. Other snippets and all captured metadata were
unchanged; the plugin reports no code error.

## What is live

- One Person at `https://kriskrug.co/#person`, linking BC + AI to
  `https://bc-ai.ca/#organization` and using “BC + AI Ecosystem Association.”
- The approved six social profiles: Twitter, X, Instagram, LinkedIn, YouTube
  `/kriskrug`, and Flickr. The later YouTube sameAs choice remains separate.
- Futureproof uses its `www` URL as a worksFor Organization, without a festival
  `@id` or Event schema on this site.
- Two exact approved VideoObjects on Speaking page 1887 only. Each has its
  title, thumbnail, upload date, duration and embed URL, and references the
  shared Person. Both thumbnails and both embed URLs returned HTTP 200.
- Home retains WebSite.name “Kris Krug”; the sample BlogPosting retains author
  and publisher references to the shared Person.

## Verification and delivery

The [machine-readable receipt](schema-1089-verification-2026-10-25.json) records
the source hashes, public checks and validator results. Public verification
covers Home, Speaking, About and
`/2026/08/10/keep-the-machine-strange/`, with normal and cache-busted requests.
Each JSON-LD block parses, each page has exactly one Person, videos stay on
Speaking, and no Event or Futureproof festival identity appears.

Schema Markup Validator's Fetch URL mode reports **0 errors and 0 warnings**
on the fresh homepage, Speaking and sample article. Speaking reports two
VideoObject items. Its results group referenced Person nodes under their
parent items; raw JSON-LD checks independently establish the Person count.
This is schema validation, not proof of Google indexing or rich-result display.

Fresh requests initially passed while normal responses retained the old
output in two cache layers. At `2026-10-26T00:52:26Z`, the generated Jetpack
Boost page-cache directory was rotated through the existing host-verified
SFTP connection, following [Jetpack's manual cache recovery guidance](https://jetpack.com/support/jetpack-boost/troubleshooting-caching-issues/#manually-deleting-the-boost-cache-directory).
Static assets, cache configuration and `advanced-cache.php` were preserved.
Pagely's outer cached responses were then allowed to expire. At
`2026-10-26T01:16:05Z`, all four normal routes and all four fresh requests
passed. Speaking, About and the sample article had expired the old outer
response and returned the updated Boost-cached output. The repeat warm-cache
check is recorded in the machine-readable receipt.

The repeat at `2026-10-26T01:16:21Z` passed **8/8 requests**, with all four
normal routes reporting a Pagely cache **HIT** and a Boost cache **hit**.
Schema Markup Validator then fetched the normal Speaking URL directly and
again reported **0 errors, 0 warnings, and two VideoObject items**.

PHP syntax and the 29 focused Person, site-identity, Speaking and preflight
tests passed before the save; the full Python suite passed **1,107 tests**.
The repository follow-up changes only deployment
documentation and header comments. The historical preflight manifest stays
historical; its hash test now verifies the approved original file identity and
the current executable suffix against this authenticated release receipt.

## Recovery

Private recovery packet in the original checkout:
`.generated/current-state/schema-1089-2026-10-25/`. It contains the full
authenticated before/after snapshots, exact diff, dry-run/apply receipts,
public HTML/JSON-LD, and validator text/screenshots. `apply.py --rollback`, run
through Varlock with the existing Python runtime, restores the original code
only after confirming the current source is the saved candidate and metadata
still matches. A concurrent edit stops recovery rather than being overwritten.

The generated-cache recovery copy is retained as `page-cache-before.zip` in
that private packet. All **881 files, 32,575,581 uncompressed bytes** were
verified individually against their SHA-256 digests, and the ZIP passed its
integrity check. Archive SHA-256:
`7ad486e3a26d3bf5797b8f32037918c54a291add616680a80ed1604af9873945`.
This cache archive is separate from the original Snippet 5 rollback snapshot.

The sole active JSON-LD snippet was 5. Snippet 13 references its article-type
helper for an XML news sitemap; it does not emit a second JSON-LD graph.
The approved source-file digest was
`a6037656daabafd5afacddea3885357e5d042ff204aa5ce01222bb1b8f8db0e6`;
the exact saved code digest is
`b205b7b3f23d8164828d88e57bbc169c2e20f579fb45f468a2d8f1b8d29e6b1f`.
The repo header was updated after the save and is not claimed byte-identical
to the live comments. Everything from `kk_schema_constants()` onward matches.
