# Post 12732 deadline copy update (#729)

**KK ruling (2026-08-16):** close the Call for Talks; extend the Earlyworm window to **August 31, 2026**.
**Target:** live WP post `12732` (https://kriskrug.co/2026/08/11/futureproof-festival-announcement/), Track A.
**Method:** two exact find/replace ops on `content.rendered`, snapshot-first, slug/ID verified. No em dashes. No other copy touched.

---

## Replace 1 — Call for Talks (close it)

**FIND (exact):**
```html
<li><strong><a href="https://www.futureproof.website/call-for-talks/">Propose a talk</a>:</strong> first-time speakers and rough first drafts are welcome. If you are reading this before August 15, 2026, the current call is still open. Check the page for live status after that date.</li>
```

**REPLACE:**
```html
<li><strong><a href="https://www.futureproof.website/call-for-talks/">Propose a talk</a>:</strong> submissions for this round have closed. The lineup is coming together on the event page, and the odd late slot still opens up, so the call page is worth a look if you have something ready.</li>
```

## Replace 2 — Earlyworm window (extend to Aug 31)

**FIND (exact):**
```html
The Earlyworm ticket window currently runs through August 15, 2026. After that, the official ticket and Luma pages remain the source of truth.
```

**REPLACE:**
```html
The Earlyworm ticket window runs through August 31, 2026. After that, the official ticket and Luma pages remain the source of truth.
```

---

## Apply steps (needs WP_USER + WP_APP_PASSWORD, which were absent in the session that prepared this)

1. Snapshot: `GET /wp-json/wp/v2/posts/12732?context=edit` -> save raw `content.raw` to `backup/post-snapshots/12732-pre-729-<ts>.json`.
2. Verify slug is `futureproof-festival-announcement` and ID is `12732` before any write (2026-05-15 incident rule).
3. Apply both find/replace ops to `content.raw`. Confirm each FIND matches exactly once; abort if 0 or >1.
4. `POST /wp-json/wp/v2/posts/12732` with the edited content only.
5. Purge Pagely edge (no-op save or purge), then logged-out readback:
   - `curl -s .../futureproof-festival-announcement/ | grep -c "August 15, 2026"` -> `0`
   - `grep -c "August 31, 2026"` -> `1`
   - `grep -c "—"` in the post body region -> `0`
6. Rollback: re-POST `content.raw` from the snapshot.

## Notes
- No non-latin1 codepoints in either replacement, so no NCR handling needed.
- The `<title>` on this post is unaffected (it has a custom SEO title).
