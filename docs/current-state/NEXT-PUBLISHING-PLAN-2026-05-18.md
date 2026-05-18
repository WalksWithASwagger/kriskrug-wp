# Next Publishing Plan - 2026-05-18

**Purpose:** Decide what publishes next after the first draft-publishing swarm, with explicit security and quality gates.

**Hard rule:** The exposed application password has been rotated, but live WordPress publishing still requires backup confirmation, dry-run review, slug/ID verification, and category cleanup.

---

## Security Remediation

Current-file status:

- The plaintext WordPress application password is no longer present in the current tracked docs.
- A working-tree scan excluding the gitignored local `.env` found no pasted app password.
- The local `.env` remains gitignored and untracked.
- Token-shaped examples in the connector docs were replaced with non-secret placeholders.
- Raw HTML snapshots were sanitized for token-like Stripe/Jetpack values that were not needed for the audit record.

History status:

- The credential was introduced in commit `ca94502` (`docs: comprehensive resume-here handoff doc`).
- It was redacted from current docs in commit `d746ecb` (`docs: record swarm results`).
- Because `ca94502` was pushed, the credential should be treated as public even though current files are clean.
- On 2026-05-18 at 11:14 PT, the exposed application password was revoked and replaced.
- The older `MCP AI` application password was also revoked during the rotation.
- A read-only authenticated check verified that only the new connector application password remains active.

Completed:

1. Revoked the exposed `kk-notion-to-wp` application password.
2. Revoked the older `MCP AI` application password.
3. Created a replacement connector password.
4. Stored the replacement only in `scripts/notion-to-wp/.env`, which is gitignored.
5. Re-ran a read-only authenticated check without printing credentials.

Still required before any live connector publishing:

1. Confirm a fresh backup/rollback path.
2. Re-run connector `--dry-run`.
3. Verify slug, title, WP ID, and target status before any update.
4. Fix category routing so `Feature` posts do not silently land in `Misc`.
5. Keep credentials out of docs, issue comments, commit messages, and terminal output.

Git-history cleanup decision:

- Password rotation is complete.
- Rewriting public git history is optional cleanup and requires explicit approval because it means force-pushing `main`.
- If history rewrite is approved, coordinate with any active clones/worktrees first, scrub the secret from `ca94502`, force-push with lease, then verify the GitHub file view and commit diff no longer expose it.

## What Is Already Published

Verified from authenticated, read-only WordPress REST calls on 2026-05-18:

| WP ID | Slug | Live status | Notes |
|---:|---|---|---|
| 10594 | `make-culture-not-content` | Published | Recent flagship post |
| 11178 | `your-taste-is-your-moat` | Published | Live title renders as `Why Judgment Beats "Creativity" in the AI Era` |
| 11765 | `calling-us-all-in` | Published | Notion row `Calling Us All In` is live |
| 11826 | `web-summit-vancouver-2026` | Published | Notion row `Welcome to Web Summit. Now Show Us the Numbers.` appears to be the source, but live slug/title differ |
| 11700 | `punk-rock-ai` | Published | Recent May 2026 post |
| 11620 | `applied-ethical-ai-responsible-ai-professional-certification-rap` | Published | Existing RAP/certification-related post |

Authenticated exact-slug checks found no existing WP post or draft for:

- `sovereign-ai-for-whom`
- `comox-valley-ai-is-becoming-its-own-thing`
- `why-we-built-the-responsible-ai-professional-certification`
- `welcome-to-web-summit-now-show-us-the-numbers`

Recent Notion rows marked `Published` but not found by exact WP slug should be treated as inventory follow-up, not proof they are missing. They may have been posted under different titles/slugs or to another surface.

Authenticated WordPress draft inventory:

| Surface | Count | Publishing implication |
|---|---:|---|
| Draft posts | 32 | Old admin draft queue; not automatically connected to the current Notion batch |
| Draft pages | 3 | Old placeholders; not near-term publishing work |
| Draft posts in `Misc` | 32 | Category handling must be fixed before any batch publishing |
| Draft posts with empty slugs | 32 | Slug assignment must be deliberate during any rescue/publish pass |
| Draft posts with no images | 26 | Most admin drafts still need media decisions |
| Metric-level candidate | 1 | Worth editorial review, but not automatically next |
| Needs prep / hold | 31 | Requires editorial triage before any WordPress write |

The full authenticated draft-title inventory should stay out of this public repo. Use a private/local admin inventory when assigning draft-rescue workers.

## Candidate Ranking

### 1. Sovereign AI for Whom?

**Local pack:** `content/drafts/2026-05-13-sovereign-ai-for-whom/`

**Verdict:** Strongest next candidate, but high-risk. Publish only after a fact-check/human signoff pass.

Why it is strong:

- Timely Web Summit / sovereign AI piece.
- Strong public voice and clear argument.
- Has 6 images and 44 links.
- Not already present on WP by exact slug.

Must fix before creating a WP draft:

- Category is currently `Misc`; should not ship that way. Likely category: `Web Summit Vancouver`, with a second editorial decision on `AI Ethics & Philosophy` or `Events & Reports`.
- Opening formatting glitch: `**For all of us… w**e`.
- Verify all high-stakes claims and quotes: minister quotes, TELUS/MOU status, BC Hydro allocation, Westbank/Q&A timeline, host Nation/land governance framing, CHPC creative-labour claims, water/heat numbers.
- Review external links; there are enough links that one broken or mismatched citation could hurt trust.
- Review alt text; current alt text is slide-caption-like, acceptable as a starting point but not polished.

Recommended next action:

1. Create a fact-check checklist from the post's claims.
2. Fix local metadata/category/alt/opening formatting.
3. Create a WP draft only, not publish.
4. Review in wp-admin, then publish after KK signoff.

### 2. Why We Built the Responsible AI Professional Certification

**Local pack:** `content/drafts/2026-05-16-why-we-built-the-responsible-ai-professional-certification/`

**Verdict:** Good commercial/educational post, but not next until duplication and internal-link issues are fixed.

Why it is useful:

- Clear service/program positioning.
- Lower political/factual risk than `Sovereign AI for Whom?`.
- Has 13 images and a direct CTA.

Must fix before creating a WP draft:

- Existing live post `applied-ethical-ai-responsible-ai-professional-certification-rap` already covers RAP. Decide whether this is a replacement, update, or distinct follow-up.
- Internal link audit includes Notion workspace URLs. These must not publish.
- Excerpt/meta description is just a byline.
- Category is currently `Misc`; likely category: `AI Ethics & Philosophy`.
- Slide-derived alt text is repetitive and several entries are truncated.

Recommended next action:

1. Compare against the April 17 live RAP post.
2. Reframe as a newer launch/follow-up only if it adds enough new value.
3. Replace internal Notion links with public URLs or remove them.
4. Clean excerpt/meta and alt text before WP draft creation.

### 3. Comox Valley AI Is Becoming Its Own Thing

**Local pack:** `content/drafts/2026-05-06-comox-valley-ai-is-becoming-its-own-thing/`

**Verdict:** Promising community recap, but not publish-ready.

Why it is promising:

- Original regional/community story.
- Strong BC + AI ecosystem-building value.
- Not already present on WP by exact slug.

Must fix before creating a WP draft:

- The excerpt/meta are the Notion `Draft status` note.
- The body still includes editorial TODOs: add GitHub links, confirm attendance count, confirm author surface, consider photos, cross-link related pages, decide whether to split the technical section.
- No images or featured image.
- Category is currently `Misc`; likely category: `Vancouver AI Ecosystem` or `Events & Reports`, with tags for Comox/CV + AI.
- Internal links are currently zero.

Recommended next action:

1. Treat this as an editorial-prep task, not a publisher task.
2. Remove the draft-status material and TODO block from the rendered post.
3. Add at least one strong image or decide it deliberately ships text-only.
4. Add internal links to relevant BC + AI / Vancouver AI / Comox Valley pieces.

## Connector / Pipeline Fixes Before The Next Batch

The connector currently maps Notion `Feature` to no specific category, so these posts fall into `Misc`.

Minimal next fix:

- Add an explicit `Feature` category decision, or derive category from tags when `Type=Feature`.
- For Web Summit-tagged features, prefer `Web Summit Vancouver`.
- For AI ethics/certification features, prefer `AI Ethics & Philosophy`.
- For community/event recaps, prefer `Vancouver AI Ecosystem` or `Events & Reports`.

Do not publish another batch while `Feature` silently lands in `Misc`.

## Recommended Next Work Order

1. Rotate the exposed WordPress app password.
2. Fix connector category behavior for `Feature` or manually override categories before WP draft creation.
3. Prep `Sovereign AI for Whom?` as the next WP draft, with fact-check and high-stakes claim review.
4. Run a private editorial triage pass on the 32 existing WordPress admin drafts before rescuing any of them.
5. Prep RAP second only after comparing it to the April 17 live RAP post.
6. Prep Comox third as a community recap after editorial TODOs and imagery are resolved.
