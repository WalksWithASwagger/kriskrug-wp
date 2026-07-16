# Orchestra progress — Monday queue #360 children

**Captured:** `2026-07-16T00:43:21Z`  
**Branch tip at write:** `cursor/orchestra-monday-queue-2853` (from `main` @ `1b5ca7d`, PR #359 merged)  
**Mode:** public / repo-only. No live WordPress writes. Cloud `WP_*` secrets absent.

## Verdict

Agent-safe slices of `#361`–`#366` are finished. Live gates remain for KK. Open PRs after this commit land: this orchestra PR only (then empty again once merged). Post-issue PR plan is below.

| Issue | Agent-safe status | Blocker for “done” |
|---|---|---|
| [#361](https://github.com/WalksWithASwagger/kriskrug-wp/issues/361) Land front-door docs | **Complete** — PR [#359](https://github.com/WalksWithASwagger/kriskrug-wp/pull/359) merged `2026-07-16T00:41:49Z` | Close issue in GitHub UI (integration cannot comment/close) |
| [#362](https://github.com/WalksWithASwagger/kriskrug-wp/issues/362) Aurora 1.3.40 verify + smoke | **Pre-upload complete** — see [`aurora-140-package-verify-20260716-004321Z.md`](aurora-140-package-verify-20260716-004321Z.md) | KK exact checksum upload → post-deploy smoke |
| [#363](https://github.com/WalksWithASwagger/kriskrug-wp/issues/363) Publisher batch orchestration | **Prep complete** — see [`issue-363-publisher-orchestration-prep-20260716.md`](issue-363-publisher-orchestration-prep-20260716.md) | Live Aurora `1.3.40` + refreshed #339 checklist (1.3.40 hashes) + secrets + KK ticks |
| [#364](https://github.com/WalksWithASwagger/kriskrug-wp/issues/364) Hub-link wraps | **Prep complete** — see [`issue-364-hub-links-ready-20260716.md`](issue-364-hub-links-ready-20260716.md) | KK approve exact `patch_id`s; secrets for write |
| [#365](https://github.com/WalksWithASwagger/kriskrug-wp/issues/365) A11y → WP draft | **Prep complete** — see [`issue-365-a11y-draft-gates-20260716.md`](issue-365-a11y-draft-gates-20260716.md) | KK answers `[NEEDS KK REVIEW]` gates + secrets |
| [#366](https://github.com/WalksWithASwagger/kriskrug-wp/issues/366) Parking lot | **Triaged only** — see [`issue-366-parking-lot-triage-20260716.md`](issue-366-parking-lot-triage-20260716.md) | Explicit KK pick of one later item |

## Checks run this session

- Deploy/rollback SHA-256 match handoff (`8e1c1321…` / `cfa1307e…`)
- Live `style.css` Version still **1.3.37**
- Public SEO gaps still match pre-deploy baseline (home `og:title` missing; `/blog/` + `/blog/page/2/` no canonical)
- `/accessibility/` still **404**
- `make theme-smoke` · `make docs-truth-check` · `make verify` · handoff unit tests for #249/#284/#328/#335/#336/#342/#351 — green
- `make env-check`: Varlock not on PATH (expected in Cloud); `.env.schema` readable

## After issues — PR work plan

At orchestra start: **0** open PRs on `main`.

1. **Land this docs PR** (orchestra evidence) → merge when KK reviews.
2. **No other open PRs** to grind. Next PRs are event-driven:
   - Post-upload: Track B evidence PR for #362 smoke report (after live `1.3.40`).
   - Post-#339: Track A evidence PR with publisher snapshots/readback (secrets + checklist).
   - Post-#364 / #365: separate Track A PRs only after KK approvals / draft creation.
3. Do **not** open speculative PRs for parking-lot items (#366) until KK picks one.
4. Keep `allow_auto_merge=false` discipline: green CI ≠ merge permission unless KK says so.

## Human closeouts (GitHub UI)

Integration token cannot `gh issue comment` / `close`. Please close or annotate:

- Close **#361** (done via #359).
- Comment on **#362** linking the package-verify report; leave open until post-deploy.
- Comment on **#363–#365** linking prep reports; leave open at gates.
- Leave **#366** open until a parking-lot pick is chosen.
