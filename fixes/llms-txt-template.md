# llms.txt deployment guide for kriskrug.co

`fixes/llms.txt` is the deployment-ready source for the site-root file at:

```text
https://kriskrug.co/llms.txt
```

As of 2026-06-07, the live URL returns `404 text/html`, so the expected first deploy changes that response to `200` with plain-text or Markdown content.

## Deploy

Recommended path: upload `fixes/llms.txt` to the Pagely document root as `llms.txt` through SSH or SFTP. A static root file is preferred because it avoids WordPress routing and plugin dependencies.

Alternative path: if a static root file is not available, deploy a tiny mu-plugin or Code Snippets entry that registers `/llms.txt` and returns the exact contents of `fixes/llms.txt` as `text/plain; charset=utf-8`.

Do not deploy this file without KK approval and a current rollback path.

## Rollback

If the site previously returned 404, remove the deployed `llms.txt` file or disable the snippet/rewrite that serves it.

If an older live `llms.txt` exists by the time this deploy runs, copy it to a timestamped backup before replacing it, then restore that backup to roll back.

## Verify

Before deploy:

```bash
curl -i https://kriskrug.co/llms.txt
# expected before first deploy: HTTP 404 text/html
```

After deploy:

```bash
curl -fsSL https://kriskrug.co/llms.txt -o /tmp/kriskrug-llms-live.txt
diff -u fixes/llms.txt /tmp/kriskrug-llms-live.txt
curl -i https://kriskrug.co/llms.txt | sed -n '1,12p'
# expected: HTTP 200 and Content-Type text/plain, text/markdown, or compatible text content
```

## Maintenance

Refresh `fixes/llms.txt` every 3-6 months or after major page/archive changes. Keep it curated; `llms-full.txt` remains a separate future artifact and should not be bundled with this first deploy.
