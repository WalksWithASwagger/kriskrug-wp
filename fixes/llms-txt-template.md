# llms.txt deployment guide for kriskrug.co

`fixes/llms.txt` is the deployment-ready source for the site-root file at:

```text
https://kriskrug.co/llms.txt
```

A source change in this repo is not evidence that live `/llms.txt` changed.

## Deployed state

**2026-06-14:** Live `https://kriskrug.co/llms.txt` returned `200 text/plain` and its body matched `fixes/llms.txt` (PR #180 / #187 closed).

**2026-10-17 (#1129):** Repo source replaced the Vancouver AI Meetup search target `https://kriskrug.co/?s=vancouver+ai+meetup` with `https://kriskrug.co/events/`. Live `/llms.txt` still served the pre-#1129 body at implementation time. Apply remains WordPress-gated.

Live response headers indicate it is **served dynamically by WordPress, not as a static document-root file**: the response carries `vary: accept,content-type` and `cache-control: no-store, private` — the signature of a PHP `template_redirect`/`init` handler echoing the text, the same delivery family as the robots.txt `robots_txt` filter (`fixes/robots-txt-ai-policy.php`). There is **no static `llms.txt` at the Pagely document root** to SFTP.

To confirm/edit the live source: wp-admin → **Code Snippets** (or mu-plugins). The snippet intercepts `/llms.txt` and returns the body as `text/plain`. To change content, edit the snippet's embedded text (keep `fixes/llms.txt` as the canonical source and re-paste), then re-verify. The earlier static-SFTP path below is the fallback if the snippet is ever removed. Snapshot the current snippet body before replacing it.

## Deploy (fallback / re-deploy)

Preferred (matches current live mechanism): a mu-plugin or Code Snippets entry that registers `/llms.txt` and returns the exact contents of `fixes/llms.txt` as `text/plain; charset=utf-8`.

Alternative: upload `fixes/llms.txt` to the Pagely document root as a static `llms.txt` via SSH/SFTP. A static root file takes precedence over the WP handler, so disable the snippet first to avoid ambiguity.

Do not change this file's live source without KK approval and a current rollback path.

## Rollback

If the site previously returned 404, remove the deployed `llms.txt` file or disable the snippet/rewrite that serves it.

If an older live `llms.txt` exists by the time this deploy runs, copy it to a timestamped backup before replacing it, then restore that backup to roll back.

## Verify

Confirm live state and source parity. After a KK-approved apply, expect HTTP 200 and `diff` empty. Until then, live still has the meetup search URL and `diff` is expected:

```bash
curl -fsSL https://kriskrug.co/llms.txt -o /tmp/kriskrug-llms-live.txt
diff -u fixes/llms.txt /tmp/kriskrug-llms-live.txt   # empty only after apply
curl -i https://kriskrug.co/llms.txt | sed -n '1,12p' # expect: HTTP 200, Content-Type text/plain
```

## Maintenance

Refresh `fixes/llms.txt` every 3-6 months or after major page/archive changes. Keep it curated; `llms-full.txt` remains a separate future artifact and should not be bundled with this first deploy.
