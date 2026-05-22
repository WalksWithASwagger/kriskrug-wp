# Issue 15 - The Upgrade AI Co-Founder Section Verification - 2026-05-21

## Scope

- Track A only.
- No live WordPress write.
- No theme, Aurora, Work, Home, Speaking, shared metadata, or deploy-checklist edits.
- Shared About payload inspected but not edited in this lane: `content/source-packs/keynotes-2026/wp-payloads/about.html`.

## Decision

Issue #15 is repo-ready for the normal target-check, rollback-note, and WordPress publish flow, but it should not close yet.

The local source pack already contains a dedicated `The Upgrade AI` card in the About-page `Current operating roles` section. It names the role as `Co-founder / AI training`, links to `https://www.theupgrade.ai/`, references Peter Bittner, and describes cohorts, custom trainings, resource portals, workshops, team workflows, AI for creative professionals, PR/communications training, and enterprise-ready adoption.

I did not edit `about.html` because the required section is present and the file already has unrelated in-progress edits from another lane. Touching it here would create avoidable coordination risk.

## About Payload Evidence

Current local payload markers:

- `Current operating roles`
- `Co-founder / AI training`
- `The Upgrade AI`
- `With Peter Bittner and collaborators`
- `cohorts, custom trainings, resource portals, and workshops`
- `AI for creative pros`
- `PR and communications training`
- `enterprise-ready adoption`
- `team trainings`
- `certification cohorts`
- `enterprise logos`

The section is scoped to the About page only and does not require changes to Work, Home, Speaking, Services, or `page-meta.json`.

## Source Grounding Already In Repo

- `content/source-packs/keynotes-2026/verification/ABOUT-ROLE-SECTIONS-VERIFICATION-2026-05-20.md`
  - Records that the About payload added equal-weight role cards for BC+AI, Indigenomics AI, and The Upgrade AI.
  - Notes that The Upgrade evidence came from `https://www.theupgrade.ai/`, the XML source referencing Peter Bittner and TheUpgrade.ai, and public Upgrade copy around live/on-demand courses, group coaching, team trainings, certification cohorts, and enterprise logo proof.
  - Explains the conservative wording choice: use `enterprise logos` instead of an unqualified `Fortune 500 training` claim.
- `docs/current-state/raw/pages/ai-upgrade-for-creative-professionals.html`
  - Contains the local WordPress export evidence for Kris and Peter as course instructors.
  - References Kris as Founder of The Upgrade Academy and Peter Bittner as Founder of The Upgrade.
- `content/source-packs/keynotes-2026/verification/SERVICES-ROLE-ALIGNMENT-VERIFICATION-2026-05-20.md`
  - Confirms The Upgrade AI positioning around live/on-demand courses, 1:1 and group coaching, team trainings, Creative Pros, PR/Communications Pros, and Sales Leaders.
- `content/source-packs/keynotes-2026/wp-payloads/services.html`
  - Provides supporting site-copy precedent for `The Upgrade AI Training`, including team training and platform links.

## Copy Guidance For Live Update

Use the current About payload section as the publish candidate. Keep the claim language conservative unless new live evidence is captured:

- Recommended role label: `Co-founder / AI training`.
- Recommended proof chips: `Peter Bittner`, `team trainings`, `certification cohorts`, `enterprise logos`.
- Recommended link: `https://www.theupgrade.ai/`.
- Avoid using `Fortune 500 training` as a standalone claim until a source-backed Fortune 500 client list, logo proof, or approved private-client wording is captured in the publish notes.

## Remaining Live Verification And Closure Criteria

Issue #15 can close only after the live About page is updated and verified:

1. Fresh backup or restore point exists.
2. Live target is verified as page ID `1208`, slug `/about/`, with the intended title/status.
3. The About payload is patched only after slug/title/id verification.
4. REST readback confirms the deployed content includes:
   - `Current operating roles`
   - `The Upgrade AI`
   - `Co-founder / AI training`
   - `Peter Bittner`
   - `team trainings`
   - `certification cohorts`
   - `enterprise logos`
5. Browser check confirms desktop and mobile render without layout overlap.
6. Link check confirms `https://www.theupgrade.ai/` and the Peter Bittner link resolve.
7. GitHub issue #15 is updated with the deployed URL, readback markers, and backup/rollback evidence.

Until those live checks pass, #15 remains blocked by deployment and live evidence, not by repo content readiness.

## Verification Run

- `git status --short --branch`
- `rg -n "Upgrade AI|The Upgrade|co-founder|cofounder|AI co-founder|cofounder" content/source-packs/keynotes-2026 docs/current-state issues-to-create -S`
- `sed -n '1,220p' content/source-packs/keynotes-2026/wp-payloads/about.html`
- `git diff -- content/source-packs/keynotes-2026/wp-payloads/about.html`
- `sed -n '1,140p' content/source-packs/keynotes-2026/verification/ABOUT-ROLE-SECTIONS-VERIFICATION-2026-05-20.md`
- `sed -n '1,120p' content/source-packs/keynotes-2026/verification/SERVICES-ROLE-ALIGNMENT-VERIFICATION-2026-05-20.md`
- `sed -n '540,585p' docs/current-state/raw/pages/ai-upgrade-for-creative-professionals.html`
- `git diff --check`
- `git diff --no-index --check /dev/null content/source-packs/keynotes-2026/verification/ISSUE-15-UPGRADE-AI-SECTION-VERIFICATION-2026-05-21.md`

Both whitespace checks produced no output. The `--no-index` check exits non-zero because it compares `/dev/null` to a real untracked file, but it reported no whitespace errors.
