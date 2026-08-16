# Issue #764: post 12032 dead Related link

**Prepared, not applied.** Runbook, apply commands, and rollback live in
[`../../2026-06-16-storyhive-haus-of-owl-jordan-dack/fix-764/RUNBOOK.md`](../../2026-06-16-storyhive-haus-of-owl-jordan-dack/fix-764/RUNBOOK.md).

One line changes in the Related block:

```diff
-<li><a href="https://kriskrug.co/?p=11876">The 75% Rule</a></li>
+<li><a href="https://kriskrug.co/2026/06/17/storyhive-haus-of-owl-jordan-dack/">Send AI After the Art-Adjacent Work</a></li>
```

`?p=11876` returns 404 to logged-out readers because post 11876 is `private` and
always was. Its own permalink 404s too, so there is nothing to resolve it to.
11876 was retired on purpose. See
[`../../2026-05-21-the-75-percent-rule-ai-art-adjacent-work/SUPERSEDED.md`](../../2026-05-21-the-75-percent-rule-ai-art-adjacent-work/SUPERSEDED.md).
Its argument now lives in post 12327 under "Galiano, Midjourney, and the
Orbit Around the Art." The link points there, keeping 11876's title as the anchor.

`12032-content-payload.html` is the full `content` value to PATCH.
`12032-baseline-20260815.json` is the pre-change `context=edit` readback that the
apply script hash-checks against, and the fallback rollback source.

The other three links in that block were checked on 2026-08-15 and all return 200.
The post body has no em dashes and no characters outside latin1.
