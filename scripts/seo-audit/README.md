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

Requires WordPress credentials in the process environment: `WP_USER` and `WP_APP_PASSWORD`, or the `WP_API_USERNAME` and `WP_API_PASSWORD` names Varlock injects. Run it as `make varlock-run CMD='make seo-audit'`. A gitignored `scripts/notion-to-wp/.env` still works as a compat fallback, but process env wins and secrets should not be copied into it.

### Scope

- **In:** published `post` and `page` types
- **Out:** `transcript` CPT (not deployed), write operations

### Tests

```bash
python3 -m unittest discover -s scripts/seo-audit/tests -v
```
