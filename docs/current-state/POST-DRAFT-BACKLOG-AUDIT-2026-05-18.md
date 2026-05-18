# Post, Draft, and Backlog Audit - 2026-05-18

**Purpose:** Re-establish trust after the Notion-to-WordPress overwrite incident by separating verified live WordPress state, local draft-pack state, and GitHub backlog state.

**Mode:** Read-only analysis. No WordPress writes, no connector live runs, no GitHub issue edits except creating the incident-tracking issue `#75`.

**Verification update:** After the first public-corpus pass, an authenticated read-only WordPress REST pass was run through the local connector credentials. No dedicated WordPress MCP tool was exposed in the current Codex tool surface, but authenticated WordPress access did work.

---

## Trust Boundary

The 2026-05-15 incident is real and should remain the operating constraint:

- Post `11765` used to be `web-summit-vancouver-2026`.
- The connector overwrote it with `calling-us-all-in`.
- Web Summit was later restored as new post `11826`.
- Local draft folders can say `status: draft` even when the post is now live.
- Notion `Published` or `Review` status is not proof of WordPress state.

Current rule: authenticated WordPress state plus explicit WP IDs/slugs are truth for posts and pages. The public REST API proves only what is visible publicly. Local `content/drafts/` is a staging/capture area, not current production truth.

## Security Gate

The exposed WordPress application password was rotated on 2026-05-18 at 11:14 PT.

Completed:

1. The exposed `kk-notion-to-wp` application password was revoked.
2. The older `MCP AI` application password was revoked.
3. A replacement connector credential was created.
4. New credentials are stored only in gitignored `scripts/notion-to-wp/.env`.
5. A read-only auth check verified the new credential without printing it.

Do not use the connector for live WordPress writes until a fresh backup/rollback path is confirmed, a dry-run is reviewed, target slug/ID/status are verified, and category routing is fixed.

Issue created: [#75 - Lock down Notion-to-WordPress publishing after overwrite incident](https://github.com/WalksWithASwagger/kriskrug-wp/issues/75).

## Authenticated WordPress Corpus

Verified from authenticated, read-only WordPress REST calls on 2026-05-18:

| Surface | Publish | Draft | Pending | Future | Private | Trash |
|---|---:|---:|---:|---:|---:|---:|
| Posts | 944 | 32 | 0 | 0 | 0 | 0 |
| Pages | 34 | 3 | 0 | 0 | 0 | 0 |

Important admin-state findings:

- Every authenticated draft post currently has an empty slug and the `Misc` category.
- The three draft pages are old placeholders, not near-term publish candidates.
- Exact-slug authenticated `status=any` checks found no post or draft for `sovereign-ai-for-whom`, `comox-valley-ai-is-becoming-its-own-thing`, `why-we-built-the-responsible-ai-professional-certification`, or `welcome-to-web-summit-now-show-us-the-numbers`.
- Exact-slug checks did find `web-summit-vancouver-2026` as WP `11826`, `calling-us-all-in` as WP `11765`, `your-taste-is-your-moat` as WP `11178`, `make-culture-not-content` as WP `10594`, and the April RAP post as WP `11620`.
- Revision checks for the recent key posts returned empty revision arrays through REST, so do not assume WordPress has a usable revision safety net for incident recovery.

Recent published posts:

| WP ID | Date | Slug | Live title | Category note |
|---:|---|---|---|---|
| 10594 | 2026-05-16 | `make-culture-not-content` | Make Culture, Not Content | AI for Creatives |
| 11178 | 2026-05-15 | `your-taste-is-your-moat` | Why Judgment Beats "Creativity" in the AI Era | AI for Creatives |
| 11765 | 2026-05-14 | `calling-us-all-in` | Calling Us All In | AI Ethics & Philosophy |
| 11826 | 2026-05-07 | `web-summit-vancouver-2026` | Web Summit Vancouver 2026 | Events & Reports |
| 11700 | 2026-05-04 | `punk-rock-ai` | Punk Rock AI | AI Ethics & Philosophy |
| 11620 | 2026-04-17 | `applied-ethical-ai-responsible-ai-professional-certification-rap` | Applied Ethical AI: Responsible AI Professional Certification (RAP) | AI Ethics & Philosophy |

Public post distribution by year:

| Year | Count |
|---:|---:|
| 2003 | 1 |
| 2004 | 30 |
| 2005 | 242 |
| 2006 | 304 |
| 2007 | 119 |
| 2008 | 12 |
| 2009 | 21 |
| 2010 | 19 |
| 2011 | 6 |
| 2012 | 1 |
| 2013 | 3 |
| 2015 | 7 |
| 2016 | 3 |
| 2017 | 1 |
| 2019 | 5 |
| 2020 | 1 |
| 2021 | 1 |
| 2023 | 64 |
| 2024 | 75 |
| 2025 | 20 |
| 2026 | 9 |

## Category State

Post-by-post aggregation from public REST data, used only for the public corpus distribution:

| Category | Public post count |
|---|---:|
| Misc | 769 |
| No category returned | 70 |
| Field Notes | 35 |
| AI for Creatives | 22 |
| AI Ethics & Philosophy | 11 |
| Vancouver AI Ecosystem | 11 |
| Events & Reports | 10 |
| Indigenous & Reconciliation in Tech | 5 |
| Generative AI Tools | 5 |
| Conversations & Interviews | 3 |
| AI for Journalism & Media | 2 |
| Oil Spill | 1 |

Important category gap:

- `Web Summit Vancouver` exists but has public count `0`.
- Current Web Summit post `web-summit-vancouver-2026` is under `Events & Reports`, not `Web Summit Vancouver`.
- Connector still maps Notion `Feature` to `Misc` unless category handling is fixed or manually overridden.

## Local Draft Pack Readiness

| Local pack | WP state | Readiness | Blockers | Next action |
|---|---|---|---|---|
| `content/drafts/2026-05-06-comox-valley-ai-is-becoming-its-own-thing/` | No authenticated exact-slug post or draft found | Promising, not publish-ready | Draft-status excerpt/meta, body TODOs, `Misc`, no images, zero internal links | Editorial prep first; do not publish |
| `content/drafts/2026-05-07-web-summit-vancouver-2026/` | Published as WP `11826` | Recovery pack, not normal draft | Tied to overwrite recovery; local frontmatter may still say draft/Misc | No publish action |
| `content/drafts/2026-05-13-sovereign-ai-for-whom/` | No authenticated exact-slug post or draft found | Strongest next candidate, high-risk | Fact-check claims/quotes, opening formatting glitch, `Misc`, alt text polish | Prep as next WP draft only after gates |
| `content/drafts/2026-05-14-calling-us-all-in/` | Published as WP `11765` | Live post pack | First connector run caused overwrite incident | No publish action; future edits require exact WP ID/slug verification |
| `content/drafts/2026-05-16-why-we-built-the-responsible-ai-professional-certification/` | No authenticated exact-slug post or draft found; related RAP post exists as WP `11620` | Useful, not ready | Possible duplicate/replacement conflict, Notion workspace links, weak excerpt/meta, `Misc`, repetitive/truncated alt text | Compare against live RAP post before deciding |
| `content/drafts/wp-draft-10594-post-10594/` | Published as WP `10594` | Historical polish capture | Local capture conflicts with current live state | Treat as historical |
| `content/drafts/wp-draft-11178-post-11178/` | Published as WP `11178` | Historical polish capture | Local capture conflicts with current live state | Treat as historical |

## Admin Draft Summary

The full authenticated WordPress draft inventory is intentionally not committed here because this GitHub repository is public.

Read-only draft triage found:

| Signal | Count |
|---|---:|
| Draft posts | 32 |
| Draft posts in `Misc` | 32 |
| Draft posts with empty slugs | 32 |
| Draft posts with no images | 26 |
| Draft posts under 250 words | 8 |
| Draft posts with explicit TODO/draft language | 4 |
| Empty-title draft posts | 1 |
| Metric-level candidate | 1 |
| Needs editorial prep | 18 |
| Hold/archive | 13 |

Interpretation:

- The admin draft pile is mostly an old rescue/archive queue, not a ready publish queue.
- Metric-level candidate does not mean publish-ready; it means enough body length, media, and links to justify a human/editorial pass.
- The current Notion batch remains the cleaner next publishing lane once security and connector gates are fixed.
- If a private draft-title inventory is needed, keep it local or in a private system; do not paste it into this public repo.

Recommended publishing order after gates:

1. `Sovereign AI for Whom?` as a reviewed WP draft, not direct publish.
2. RAP follow-up only if differentiated from the April 17 live RAP post.
3. Comox Valley recap after editorial TODOs, image decision, internal links, and category fix.

## GitHub Backlog State

Open issues after first hygiene pass and creation of #75: 64.

Label drift:

| Label | Open issue count | Note |
|---|---:|---|
| `auto-implement` | 62 | Overbroad; many of these touch live WordPress, product decisions, or Track B theme work. |
| `needs-human-review` | 2 | Currently #23 and #75; more issues probably need this label before agents run. |

PRs:

| PR | State | Triage |
|---:|---|---|
| #73 | Open, conflicting, no checks | Live-WP/plugin lane; not safe to merge casually |
| #74 | Open, mergeable, checks green | Static design preview; useful Track B input, not Aurora itself |

New issue:

| Issue | Purpose |
|---:|---|
| #75 | P0 publishing-trust gate after Notion overwrite incident |

## Issue Lane Classification

### Stale / Duplicate / Already Partly Satisfied

- #3: original Projects 404 symptom appears stale because `/work/` now redirects to `/recent-projects-include/`; final Work URL decision remains.
- #12 and #66: duplicate homepage hero positioning issues; verify current live copy before closing.
- #13, #14, #15: component-level duplicates of broader page/content issues #65-#68.
- #16, #17: mostly superseded by #65 and #68.
- #23: partly satisfied, not close-ready; category UX/search/category-page SEO remain.

### Needs Human Review

- #75: credential rotation and publishing approval.
- #7, #11: pricing/membership decisions.
- #23: category UX/SEO scope.
- #49-#58: marketing strategy/campaign systems.
- #59, #61: archive/KB source ownership and curation.
- #62, #64: platform/product/credential decisions.
- #65-#68: page copy can be drafted, but claims/offers/metrics require KK review.

### Safe Autonomous Repo-Only Lanes

- #36: draft meta descriptions locally.
- #38: internal-linking map/recommendations.
- #40: image SEO/performance inventory and proposed plan.
- #44: glossary draft.
- #46: accessibility audit report.
- #48: accessibility statement draft.
- #60: speaking archive inventory.
- #65-#68: draft copy packs in repo, no WordPress publishing.
- #75 partial: connector docs/tests/diff/category behavior.

### Live-WP-Gated / Dangerous Lanes

- #4, #5, #8, #9, #10, #23, #36, #38, #40, #41, #42, #43, #45, #47, #65-#68 when applying to production.
- PR #73 because it involves plugin/live sidebar behavior.

### Track B / Aurora Lanes

- #24-#35 belong on `aurora/v2`, not `main`.
- #63 is design exploration unless reduced to a static concept doc.
- PR #74 can inform Track B, but is not a production theme cutover.

## Recommended Next Swarm

Do not send agents directly at production WordPress.

Next safe wave:

1. **Issue hygiene worker:** remove misleading `auto-implement` labels from live-WP-gated issues; add `needs-human-review` where required.
2. **Connector worker:** implement `Feature` category routing and a dry-run/diff review gate for `--update`.
3. **Draft-prep worker:** clean `Sovereign AI for Whom?` locally and produce a fact-check checklist, without WP writes.
4. **Corpus worker:** make a compact CSV/Markdown inventory of the 944 public posts by year/category/topic for future content planning.

Production publisher remains a separate, serialized session after password rotation and backup confirmation.
