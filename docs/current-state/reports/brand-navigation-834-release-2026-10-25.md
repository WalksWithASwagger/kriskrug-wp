# Brand-navigation links #834: live release, 2026-10-25

Applied through Varlock at 2026-10-26 03:44 UTC (October 25 Pacific), under KK's instruction to continue and ship the kriskrug plan. All three content-only writes passed authenticated exact-content readback and normal/cache-bypassed public verification. #829 and #833 anchors were confirmed live before writing and remain present.

## Scope and outcome

| Post | Added link | Placement |
|---|---|---|
| 12653, AI Lands Inside Every Profession | [I give a talk about exactly this](https://kriskrug.co/speaking/) | Final paragraph |
| 12030, Canada Does Not Need a Bigger AI Machine | [why I keep saying this out loud](https://kriskrug.co/about/) | Closing paragraph before Public source checks |
| 11700, Punk Rock AI | [plain definitions for the words in here](https://kriskrug.co/glossary/) | Opening on-ramp paragraph, immediately after the first AI reference |

Each change appends one sentence to one existing paragraph. Reversing that single replacement reproduces the original body exactly. No theme, schema, media, title, category, tag, excerpt, or post-meta write was included. Collection footers and existing source lists are preserved. The model post 11879 is unchanged (`fe63fb845d5b16cb868c5509713883c96823bb9a3071f13d0fbb07f7f1d1d7a4`). Homepage title readback is unchanged: `Kris Krüg | AI Keynote Speaker &#038; Creative Technologist`.

## Verification

- All three destination pages returned HTTP 200.
- Each exact new anchor appears once on normal and cache-bypassed article fetches.
- Both earlier dependency anchors still appear once.
- All three immediate pre-write snapshots and authenticated readbacks are mode 0600.
- All three restore dry-runs reproduce the original body; no restore was executed.
- Twelve focused publisher tests pass, including wrong identity, stale body, missing/duplicate markers, snapshot-before-write, readback mismatch, no ambiguous-write replay, and guarded restore.
- Full declared Python suites pass: 184 publisher, 855 operations, 12 inventory, and 68 backfill/link-safety tests.
- Ruff check/format and `git diff --check` pass.

## Exact hashes

| Post | Before SHA-256 | Applied SHA-256 |
|---|---|---|
| 12653 | `c1f8fd882636fdc25984be04238841bc369903a375aeab61127cd48be71b3f8b` | `a65121142ee711cce65f1105cff2ff5a870a39eb8ec20df196e86165e3e90558` |
| 12030 | `c857c818be43ab42ddaa4b57d1a47e1586e5b6ecce56a13b2a9246a357c2e925` | `459a8390e4086ba95b571742b245d5ffeb446b3d8b8a41aaba37ec525cc6efbf` |
| 11700 | `b676bb1bb1b017b5a9d36f86ead677b25402b3e2edc113583e296c70eff4a7a9` | `320acb2a886acea0e6e2d1933599302187f9d7c995ca7ce44bc2f1c7ac569efa` |

## Recovery

The private packet is `/Users/kk/Code/kriskrug-wp/.generated/current-state/brand-links-834-2026-10-25/`. It holds original snapshots, candidates, public fetches, `public-verification.json`, and restore previews. Immediate pre-write snapshots live under `apply-snapshots/`:

- `12653-before-20261026T034443944719Z.json`
- `12030-before-20261026T034447387805Z.json`
- `11700-before-20261026T034450592238Z.json`

Use `scripts/apply_issue_834_brand_links.py --id <ID> --restore <snapshot>` through Varlock for a dry-run. Add `--apply` only for an authorized rollback. It refuses to restore over newer content. The helper compares a fresh read immediately before its single POST; WordPress does not provide an atomic compare-and-swap for this operation, so do not run concurrent editors on these posts. Ambiguous writes are never replayed; inspect live state first.

The exact operation and identity/hash guards are in `fixes/issue-834-brand-navigation.json`. No private snapshot is committed. Parent #402 remains open.
