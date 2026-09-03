# Press Kit v2 Release Checklist

Release gate for the page-3609 EPK payload. Issue #881, epic #876. The publish
step itself is #882.

> **KK approval is required before `--execute`.** Every command below through
> the dry-run is read-only. Nothing writes to WordPress until KK has seen the
> dry-run diff and said go, for this specific release. An open issue is not
> approval.

## Target

| Field | Value |
|---|---|
| Payload | `content/source-packs/content-architecture-2026/wp-payloads/podcast-guesting-page-epk.html` |
| Page ID | `3609` |
| Slug | `podcast-guesting-page-epk` |
| URL | `https://kriskrug.co/podcast-guesting-page-epk/` |
| Page key | `podcast_epk` |

Title, slug, and page ID do not change in this release. The write is
content-only.

## 1. Preflight, read-only

- [ ] `make doctor` reports credentials resolving and a clean tree.
- [ ] `python3 -m unittest scripts.tests.test_press_kit_payload` passes.
- [ ] `python3 -m unittest scripts.tests.test_content_architecture_payloads scripts.tests.test_payload_neon_islands` passes.
- [ ] `make verify` exits 0.
- [ ] `make check-live-parity` reports live and repo agreeing on the Aurora
      version. The payload's brand section is read from the theme, so a version
      disagreement means the brand card may be describing something that is not
      what visitors see. Stop and reconcile before publishing.
- [ ] The version named in the payload's usage note matches that agreed version.

## 2. Rights, before anything is published

- [ ] Every download in the payload maps to a `status: approved` entry in
      `press-kit/assets/manifest.json`. The contract test asserts this; confirm
      it ran.
- [ ] Each approved entry still carries its credit, reuse terms, rights
      evidence, alt text, and dimensions.
- [ ] The photographer credit for each image appears in the rendered payload.
- [ ] No `candidate`, `blocked-rights`, or `missing` asset is linked.
- [ ] Clearances in the manifest are still current. Clearance is recorded as
      KK's dated attestation, so if a creator has since withdrawn permission,
      the manifest is the thing to change first, not the payload.

## 3. Identity check

- [ ] Fetch `context=edit` for page 3609 with
      `id,slug,status,title,content,modified,link`.
- [ ] Stop unless ID, slug, and status match the table above.
- [ ] Record the current `modified` timestamp and the SHA-256 of `content.raw`.
      If either differs from what the dry-run reported, someone else edited the
      page. Re-run the dry-run rather than writing over them.

## 4. Snapshot

- [ ] Snapshot to `backup/<UTC timestamp>-press-kit-v2/page-snapshots/`.
- [ ] The set must contain the before JSON and the before public HTML, plus
      `sha256sums.txt` and a `rollback-manifest.json`.
- [ ] Confirm the before JSON is present. `restore_page` in
      `scripts/content_architecture_deploy.py` restores from that file, so a
      snapshot without it is not a rollback path.

## 5. Dry run

```
make varlock-run CMD='python3 scripts/content_architecture_deploy.py --page podcast_epk'
```

- [ ] The dry run plans exactly one page and reports no unrelated changes.
- [ ] Review the exact content diff, not just the summary.
- [ ] **Show KK the diff and get an explicit go.**

## 6. Publish, only after approval

```
make varlock-run CMD='python3 scripts/content_architecture_deploy.py --page podcast_epk --execute'
```

- [ ] Write `content` only. Do not send `title`.

## 7. Verify

- [ ] Authenticated REST readback matches the intended payload.
- [ ] Every marker in `page-map.json` for `podcast_epk` is present in the
      rendered public HTML.
- [ ] Purge the Pagely page cache for the URL. REST edits do not purge it
      automatically, so re-check logged out and with a cache-busting query.
- [ ] Public readback, logged out and cache-bypassed, matches.
- [ ] Each of the four download links returns HTTP 200 and the expected file
      size. A download that 404s in public is worse than no download at all.
- [ ] The interview embed loads and plays.

## 8. Visual review

- [ ] Desktop at 1440 and 768: no horizontal overflow, cards align, the
      download buttons wrap sanely.
- [ ] Mobile at 390 and 360: no horizontal overflow, buttons meet the 44px
      touch target, the embed keeps its aspect ratio.
- [ ] Booking CTA is visible before the brand material and again at the end.
- [ ] No body `H1` was introduced.

## 9. Rollback

If any verification step fails, restore before doing anything else:

```
make varlock-run CMD='python3 scripts/content_architecture_deploy.py \
  --page podcast_epk \
  --snapshot-dir backup/<UTC timestamp>-press-kit-v2/page-snapshots \
  --restore'
```

- [ ] Re-run the public readback after restoring and confirm the previous body
      is back.
- [ ] Purge the cache again.

## 10. Record

- [ ] Commit the snapshot set, the deploy report, and the rollback manifest.
- [ ] Post the before/after markers, the content SHA-256, and the readback
      evidence to #882.
- [ ] Note anything still outstanding: the unresolved #735 descriptor and
      organization-spacing choices, the missing vector wordmark master, and the
      missing print-resolution stage frame.
