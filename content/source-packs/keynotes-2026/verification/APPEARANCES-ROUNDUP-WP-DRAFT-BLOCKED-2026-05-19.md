# Appearances Roundup WP Draft Blocked - 2026-05-19

> Superseded 2026-05-22: the strict backup gate was retired and private WP draft `11879` was created at <https://kriskrug.co/wp-admin/post.php?post=11879&action=edit>. This file remains as historical evidence of the stopped 2026-05-19 attempt.

Scope: Track A publisher preflight for creating a private WordPress draft from `../../../drafts/2026-05-19-ai-media-appearances-podcast-guesting/`.

Result: stopped before the live WordPress write. No WordPress post, page, media, tag, category, or backlink was created or changed.

## Intended Draft

| Field | Value |
| --- | --- |
| Title | `AI Media Appearances, Podcast Guesting, and Broadcast Commentary` |
| Slug | `ai-media-appearances-podcast-guesting` |
| Status | `draft` only |
| Category | `Conversations & Interviews` / `1677` |
| Existing tags to reuse | `cbc` / `1626`, `speaking` / `89` |
| Missing tags not created | `Podcast Guesting`, `Media Appearances`, `AI Interviews` |
| Media treatment | Embed-only; `featured_media=0` |

## Preflight Checks

| Check | Result |
| --- | --- |
| Git sync | `main` clean and even with `origin/main` |
| Local credentials | `scripts/notion-to-wp/.env` present; values were not printed |
| Connector deps | `scripts/notion-to-wp/.venv` can import `requests` and `dotenv` |
| Auth capability | REST credential returned `administrator` role with `manage_options`, `edit_posts`, `publish_posts`, and `upload_files` |
| Target slug | Authenticated `GET /wp/v2/posts?slug=ai-media-appearances-podcast-guesting&status=any` returned `0` posts |
| Category | Authenticated `GET /wp/v2/categories/1677` returned `conversations-interviews` |
| Existing tags | `cbc` / `1626` and `speaking` / `89` exist |
| Draft links | All URLs in `post.html` returned `200` |
| Privacy scan | No matches |

## Backup Gate

The plan required a fresh full-site backup before the live WordPress write. That gate could not be satisfied in this session:

- Existing local full backup is from `backup/2026-05-16/`; it is not fresh for this write, and the uploads archive was skipped.
- No `scripts/backup-from-pagely.sh` exists in this repo.
- Local `wp` CLI is not installed.
- SSH exists locally, but no Pagely backup script/target is configured in the repo.
- Authenticated plugin inventory shows Jetpack/Jetpack Boost/Jetpack CRM/Jetpack Protect, but no active UpdraftPlus plugin route was available.
- Jetpack backup preflight returned `ok:false` with `Unable to get preflight status.`

Decision: no WordPress draft creation. This follows the plan's stop rule: if a fresh full backup is unavailable, stop before the live write.

Rollback status: no rollback action is needed because nothing was created or changed in WordPress. If this pass is repeated later and a draft is created, rollback before publication is to delete the draft by its WP post ID after confirming the slug/title match.

## Link Check Results

Command:

```bash
rg -o 'https?://[^" )]+' content/drafts/2026-05-19-ai-media-appearances-podcast-guesting/post.html | sort -u | while read url; do code=$(curl -L -sS -o /dev/null -w '%{http_code}' --max-time 20 "$url" || true); printf '%s %s\n' "$code" "$url"; done
```

Results:

| Status | URL |
| --- | --- |
| 200 | `https://bc-ai.ca/` |
| 200 | `https://horizons.compassdatacenters.com/series/exploring-ai-models-the-future-of-machine-learning/` |
| 200 | `https://kriskrug.co/2024/07/03/new-segment-on-cbc-radio-early-edition-ai-sandbox-with-kris-krug/` |
| 200 | `https://kriskrug.co/about/` |
| 200 | `https://kriskrug.co/contact/` |
| 200 | `https://kriskrug.co/motleykrug-podcast/` |
| 200 | `https://kriskrug.co/podcast-guesting-page-epk/` |
| 200 | `https://kriskrug.co/recent-projects-include/` |
| 200 | `https://kriskrug.co/speaking/` |
| 200 | `https://music.amazon.com/es-ar/podcasts/efb24614-5724-4412-a377-755e3b3ebdd4/episodes/cd1d024c-e3d4-496f-ace3-2901c89c3882/rachel-thexton-connects-03x08-kris-kr%C3%BCg-one-of-canada%27s-leading-ai-voices-talks-tech-and-tells-his-story` |
| 200 | `https://music.amazon.com/es-us/podcasts/ba75295d-60de-4701-8eb6-12e17e49838a/teen2life-experience` |
| 200 | `https://music.amazon.com/podcasts/369594c8-9548-47ed-9dee-b61dae6c7c5a/vancouver-ai-pods` |
| 200 | `https://podcasts.apple.com/us/podcast/053-widen-the-lens-with-kris-krug/id1575595225?i=1000634160006` |
| 200 | `https://www.e-channelnews.com/interview-with-kris-krug-at-channelnext-central-2025/` |
| 200 | `https://www.iheart.com/podcast/338-the-human-biography-podcas-108140410/episode/kris-krug-live-with-curiosity-256487014/` |
| 200 | `https://www.indigigenius.org/media-appearances/michaelandkrisinterview` |
| 200 | `https://www.youtube.com/watch?v=T5ANAthZewE` |

## Privacy Scan

Command:

```bash
rg -n -i 'visa|boarding|passport|hotel|whatsapp|phone|tel:|mailto:|@[A-Za-z0-9._%+-]+\.[A-Za-z]{2,}|778|898|3076|secret_|api[_-]?key|password|nonce|token|sig=|application password' content/drafts/2026-05-19-ai-media-appearances-podcast-guesting content/source-packs/keynotes-2026/media-appearances || true
```

Result: no matches.

## Next Safe Action

1. Take a fresh full backup through wp-admin/UpdraftPlus, Pagely SSH, or another approved full-site backup path.
2. Re-run the slug/category/tag/link/privacy preflight.
3. Create the private WordPress draft after a fresh slug check and review of the draft payload.
4. Do not publish or add backlinks until KK reviews the wp-admin draft.
