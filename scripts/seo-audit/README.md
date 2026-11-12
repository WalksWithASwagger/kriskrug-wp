# SEO audit scripts

Read-only tooling for Jetpack SEO metadata coverage.

## inventory.py

Pulls published posts and pages via the WordPress REST API (`context=edit`) and reports whether Jetpack SEO fields are set:

- `jetpack_seo_html_title`
- `advanced_seo_description`
- `jetpack_publicize_message` (posts only)

### Usage

```bash
make seo-audit
# or
scripts/notion-to-wp/.venv/bin/python scripts/seo-audit/inventory.py --format csv --output content/seo-audit-$(date +%Y%m%d).csv
```

Requires `WP_USER` and `WP_APP_PASSWORD` in `scripts/notion-to-wp/.env` (same as the Notion connector).

### Scope

- **In:** published `post` and `page` types
- **Out:** `transcript` CPT (not deployed), write operations

### Tests

```bash
python3 -m unittest discover -s scripts/seo-audit/tests -v
```
