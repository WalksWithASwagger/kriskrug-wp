# Local WP QA Path - 2026-06-04

## Summary

Issue #149 is unblocked for Track B QA. The Local site `kriskrug-local`
now serves real WordPress pages at `127.0.0.1:10003` using the host
`kriskrug-local.local`, and the Local theme copy was synced from canonical
`origin/main` so it serves `kk-aurora` 1.3.11 instead of stale 1.3.3.

Use Local WP as the preferred Track B browser QA surface before static
fixtures, but verify the theme version before trusting release evidence.

## Startup And Sync

Local site metadata:

- Site ID: `T6GsFbHbA`
- Site name: `kriskrug-local`
- Domain: `kriskrug-local.local`
- Web port: `10003`
- PHP CGI port: `10002`
- MySQL port: `10004`
- Path: `/Users/kk/Local Sites/kriskrug-local/app/public`

Start the Local app:

```bash
open -a Local
```

If Local says the site is running but nothing is listening on `10003`, use the
Local GraphQL endpoint recorded by Local itself:

```bash
python3 - <<'PY'
import json
import pathlib
import urllib.request

info = json.loads(
    (pathlib.Path.home() / "Library/Application Support/Local/graphql-connection-info.json").read_text()
)
body = {
    "query": "mutation startSite($siteId: ID!) { startSite(id: $siteId) { id name status } }",
    "variables": {"siteId": "T6GsFbHbA"},
}
req = urllib.request.Request(
    info["url"],
    data=json.dumps(body).encode(),
    headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer " + info["authToken"],
    },
)
with urllib.request.urlopen(req, timeout=30) as response:
    print(response.read().decode())
PY
```

Before syncing a repo theme into Local, preserve the previous Local copy:

```bash
cp -a "$HOME/Local Sites/kriskrug-local/app/public/wp-content/themes/kk-aurora" \
  "$HOME/Local Sites/kriskrug-local/app/public/wp-content/themes/kk-aurora.backup-20260604-152304Z"
rsync -a --delete theme/kk-aurora/ \
  "$HOME/Local Sites/kriskrug-local/app/public/wp-content/themes/kk-aurora/"
```

The backup created during this pass is:

```text
/Users/kk/Local Sites/kriskrug-local/app/public/wp-content/themes/kk-aurora.backup-20260604-152304Z
```

## Verification

Listener proof:

```bash
lsof -nP -iTCP:10003 -sTCP:LISTEN
lsof -nP -iTCP:10004 -sTCP:LISTEN
```

Observed result after the GraphQL start:

```text
nginx listening on 127.0.0.1:10003 and [::1]:10003
mysqld listening on 127.0.0.1:10004 and [::1]:10004
```

Theme proof:

```bash
php /Applications/Local.app/Contents/Resources/extraResources/bin/wp-cli/wp-cli.phar \
  --path="$HOME/Local Sites/kriskrug-local/app/public" \
  --allow-root theme list --status=active --fields=name,version,status
```

Observed result:

```text
name        version  status
kk-aurora  1.3.11   active
```

Public route proof:

```bash
curl -sSL --max-time 15 \
  --resolve kriskrug-local.local:10003:127.0.0.1 \
  http://kriskrug-local.local:10003/blog/

curl -sSL --max-time 15 \
  --resolve kriskrug-local.local:10003:127.0.0.1 \
  http://kriskrug-local.local:10003/2026/05/16/make-culture-not-content/
```

Observed results:

- `/blog/` returned `200`, loaded `kk-aurora` assets with `ver=1.3.11`, rendered one archive H1, and included `kriskrug-wordmark.png`.
- `/2026/05/16/make-culture-not-content/` returned `200`, loaded `kk-aurora` assets with `ver=1.3.11`, rendered `.aurora-single-2026`, and rendered the post H1 `Make Culture, Not Content`.

## Troubleshooting Notes

- Do not trust `~/Library/Application Support/Local/site-statuses.json` by itself. It reported `T6GsFbHbA: running` while no nginx/mysql processes were listening.
- Use `lsof` and `curl` as the truth source for whether the Local route is actually alive.
- Local redirects direct `127.0.0.1:10003` requests to `kriskrug-local.local:10003`; use `--resolve kriskrug-local.local:10003:127.0.0.1` for repeatable shell checks.
- WP-CLI currently emits a PHP deprecation warning from the bundled phar under PHP 8.2, but the command still returns useful output.
- Local's database/content snapshot is older than production. For article QA, pick posts that exist locally or sync a fresh content snapshot in a separate, explicit lane.
- When testing a feature branch, sync that branch's `theme/kk-aurora/` into Local before taking browser evidence, and record the theme version in the issue or PR.
