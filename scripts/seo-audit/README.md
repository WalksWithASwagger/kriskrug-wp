# SEO audit scripts

Read-only inventory of SEO title and description coverage. Jetpack is removed, so the theme owns SEO titles (`theme/kk-aurora/inc/seo-title.php`). The values still live in post meta under the old Jetpack keys.

## inventory.py

Pulls published posts and pages via the WordPress REST API (`context=edit`) and reports whether these fields are set:

- `jetpack_seo_html_title`
- `advanced_seo_description`
- `jetpack_publicize_message` (posts only)

### What the default source covers

`--source meta` (the default) reads REST post meta. Those keys are only exposed by REST because `theme/kk-aurora/inc/seo-meta-rest.php` registers them for `post`. Pages are not registered, so their meta comes back empty and page rows read as missing even when a title is set. Treat meta output as accurate for posts only.

If no item at all exposes the keys, the script prints an explanation and exits 2 instead of reporting every item as missing. Exit 2 means the keys are unregistered on the site, not that content is missing. Exit 1 means WordPress credentials were not found.

### Auditing pages and what crawlers see

`--source rendered` fetches each item's delivered HTML and reads the actual `<title>` and meta description. Use it for pages, or to confirm what crawlers see. `--limit N` samples N items per kind.

```bash
make varlock-run CMD='make seo-audit'
make varlock-run CMD='scripts/notion-to-wp/.venv/bin/python scripts/seo-audit/inventory.py --source rendered --limit 20'
```

`make seo-audit` takes `FORMAT=markdown|json|csv` and always uses the default meta source.

Credentials come from Varlock (`WP_USER` + `WP_APP_PASSWORD`, or `WP_API_USERNAME` + `WP_API_PASSWORD`). Do not read or print `.env` files.

### Scope

- **In:** published `post` and `page` types
- **Out:** `transcript` CPT (not deployed), write operations
- Registering SEO meta for pages is a separate Track B follow-up.

### Tests

```bash
python3 -m unittest discover -s scripts/seo-audit/tests -v
```
