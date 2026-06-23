# Decision Queue — 2026-06-23

**For:** KK. **Mode:** read-only brief. Nothing here was edited, published, or sent.
**Purpose:** one scannable page to unblock the gated backlog. Each item gives you the blocker, the exact input I need from you, my recommended call, and what an agent can run the moment you unblock it.

> Convention: "KK input needed" is the specific decision/access/content that only you can provide. "Prepared work waiting" is already staged in-repo and executable immediately on your go.

---

## Decide in this order (highest-leverage first)

1. **You-Can't-Drink-Data 3-post publish window (#233 dependency)** — ~95% done, one scheduling decision unblocks a coordinated drop + SEO internal-links win. *Biggest payoff per minute of your attention.*
2. **#95 media-appearances draft** — needs a Rafiki image + your editorial sign-off; draft 11879 already exists live. Small, closable.
3. **Contact forms #128 / #174** — the form is **confirmed working**; what's left is a Gmail filter + an optional external delivery test + your private-triage policy. Mostly an access/policy call, not engineering.
4. **#23 blog categories** — likely **already mostly done** by closed #223. Needs your verify-or-rescope call, not a fresh build.
5. **Content-credential sections #13 / #14 / #15** — pure content: you write/approve ~3 short bios.
6. **Epics & marketing #222 / #219 / #64 / #62 / #61 / #51 / #49** — sequencing + external-decision calls; mostly defer/rescope.

---

## 1. You-Can't-Drink-Data — coordinated 3-post publish window
*(draft at `content/drafts/2026-05-23-you-cant-drink-data/`; dependency for the internal-links half of #233)*

- **Blocker:** Three companion posts must flip from `draft` → `publish` **together** (WP 11882 "Both Hands Full / Vancouver AI March", 11929 "Data-Center Protest Signs", and this one, draft 11936). Their cross-links are hand-placed and only resolve once all three are live. No agent will publish without your explicit window approval (live-write gate).
- **KK input needed:**
  1. **A publish date/time** for the coordinated drop (the post is dated 2026-05-23; confirm you want it published now at that date, back-dated, or re-dated to today).
  2. **One preview pass** — say "looks good" after viewing `?p=11936&preview=true` (and 11882, 11929).
  3. **Confirm SEO title + meta** as staged: title "You Can't Drink Data | Notes From My First AI Protest"; meta "At Vancouver's anti-AI data-centre protest, Kris Krug follows the chant 'you can't drink data' toward cleaner, more accountable AI infrastructure." (#233 says omit title changes unless you confirm — this is your confirm.)
- **Recommendation:** **DEPLOY** — pick a window this week and drop all three. Editorial is done, 26 march photos uploaded (media 11937–11962) + 3 in-body (11963–11965), all 13 publish checks green, cross-links placed. This is the cheapest high-value win in the queue and it directly closes the internal-links acceptance criterion on #233.
- **Prepared work waiting:** Agent runs `publish_you_cant_drink_data.py` to flip all three to `publish`, then purges Pagely page cache and does a logged-out render + click-check of every internal/external link (link list in `internal-links.md`). After live: add mutual backlinks from 11882/11929, and one contextual `you can't drink data` backlink from `/about/` or the Vancouver AI hub. Then report `you cant drink data` striking-distance movement into the next SEO digest to close #233.

---

## 2. #95 — media-appearances draft review
*(`content/drafts/2026-05-19-ai-media-appearances-podcast-guesting/`)*

- **What's there:** A live WordPress **draft already exists: post 11879** (`ai-media-appearances-podcast-guesting`, edit URL `https://kriskrug.co/wp-admin/post.php?post=11879&action=edit`). Body is a clean "proof stack" for podcast guesting / CBC commentary / panels / hosting, with hand-placed internal links (EPK page, /speaking/) and external proof links (CBC segment, IndigiGenius). SEO meta staged. The old backup-gate blocker in the issue text is **stale** — the draft was created 2026-05-22 and updated 2026-06-11.
- **Blocker:** Two things: (a) the one generated feature image was **rejected and detached** on 2026-06-11 (`featured_media=0`), and `publish-gate.md` requires a Rafiki image before your approval; (b) your editorial review before publish/backlinks.
- **KK input needed:**
  1. **Read draft 11879 and approve or redline** the body copy.
  2. **Approve a feature image** — either green-light an agent to generate a Rafiki image to the brief in `image-brief.md`, or hand me one.
  3. Confirm it's OK to add the planned internal backlinks after publish.
- **Recommendation:** **DEPLOY (after image + your read).** This is a low-risk evergreen booking/credibility page; the only real gates are your editorial eye and one image. Smallest closable item after #1.
- **Prepared work waiting:** Agent generates the Rafiki feature image, attaches it to 11879, re-runs readback (slug/title/links/meta), and — on your publish word — flips to `publish`, purges cache, verifies logged-out render, and adds the staged internal backlinks.

---

## 3. Contact forms — #128 (triage + routing) & #174 (verify monitored routing)

> **Headline correction for KK:** the contact form is **NOT broken.** The 2026-06-14 live test plus Gmail evidence (`CONTACT-FORM-DELIVERABILITY-FIX-2026-06-14.md`) confirmed real leads arrive at `feelmoreplants@gmail.com` and Alex has been replying (Tyler Funk, Tayyaba Mansoor, Steve Cahill, etc.). The earlier "545 unread submissions" alarm was **retracted** — those are stored copies of mail you already received. So this is mostly hygiene + policy, not a fire.

- **Blocker:** Three residual items, none of them engineering: (a) **durable routing proof** wants one sterile external (non-KK) test submission + an inbox-not-spam readback — needs you to OK a test and ideally a Gmail filter; (b) **spam rescue** — ~104–110 Jetpack notifications may be sitting in Gmail spam (SPF/DKIM alignment); (c) **historical-triage / newsletter policy** — replying to or exporting any past submitter touches private lead PII, and CASL means no bulk-add without opt-in. Repo + issues are public, so all PII work stays in Gmail/Jetpack CSV, never in-repo.
- **KK input needed:**
  1. **Confirm the monitored recipient** is `feelmoreplants@gmail.com` (it is, per page 2418) or name a different/alias inbox — I won't guess an inbox.
  2. **Create a Gmail filter** (or OK me to draft the exact spec for you to apply): `From:*@kriskrug.co` / the `wordpress@` server address → "Never send to Spam" + label "kriskrug.co / contact"; then sweep the ~104 spam items into inbox.
  3. **OK one sterile external test** submission so #174 can pass a clean inbox-not-spam readback.
  4. **Decide the historical-triage + newsletter policy:** do nothing / reply-only in your voice / consent-first opt-in invite. No bulk newsletter adds either way (CASL).
- **Recommendation:** **RESCOPE to two small lanes + close-on-proof.** Lane A (do now): Gmail filter + spam rescue + one external test → closes #174. Lane B (your policy call): historical triage stays private and gated → closes the remaining #128 task. Drop the heavy "SPF/DKIM/SMTP hardening" unless the clean external test actually fails.
- **Prepared work waiting:** `scripts/jetpack_feedback_audit.py` (`make jetpack-feedback-audit`) re-runs the PII-safe inventory anytime (last: 547 inbox / 104 spam / 0 trash, one form on page 2418, routing keys redacted). Agent can draft the exact Gmail filter spec, run the post-filter external test, do the inbox/spam readback, and record the redacted routing path in `CONTACT-FORM-DELIVERABILITY-FIX-2026-06-14.md` to close #174 — all without touching any message body. The PII-safe routing doc shape is already established in that file (record recipient *category*/alias only).

---

## 4. #23 — blog-category reorganization

> **Check this before commissioning new work:** closed issue **#223** ("Consolidate categories to ~14 and re-categorize the 780 'Misc' posts") already did most of what #23 asks. There is a full proposed mapping staged in-repo: `CATEGORY-LEGACY-MAPPING-2026-06-14.md` (378 Misc posts → Photography or Web & Early Blog) and `CATEGORY-MAPPING-MISC-2026-06-14.md` (96KB detailed map). The live taxonomy already has named categories (e.g. AI Ethics & Philosophy 1678, Conversations & Interviews, Photography & Visual Storytelling).

- **Blocker:** Need to confirm whether #23's "5 primary categories" model is still the target, or whether the live ~14-category structure from #223 supersedes it. If superseded, #23 is mostly bucket-assignment of the long tail. The non-content acceptance items (category filter UI, search, featured-by-category, SEO/mobile/WCAG) are **separate frontend/Aurora work**, not taxonomy.
- **KK input needed:** **The category map / decision**, specifically:
  1. Confirm the canonical category set — the ~14 from live/#223, **or** the original 5 in #23 (AI Strategy / Community Building / Indigenous Tech & Futures / Policy & Impact / Photography & Visual Storytelling)? If 5, that's a re-mapping of all categories, not just Misc.
  2. **Approve or redline** the staged Misc → bucket mapping in `CATEGORY-LEGACY-MAPPING-2026-06-14.md` (era-bucket rule: photo-signal → Photography, else → Web & Early Blog; reversible, rollback recorded).
  3. Decide whether the UI/SEO acceptance criteria (filter, search, featured posts, category pages) are in-scope for #23 or split to an Aurora frontend issue.
- **Recommendation:** **RESCOPE + close the taxonomy half.** Approve the staged mapping → agent applies it (reversible) and closes the categorization work. Split the filter/search/featured-by-category UI into its own Aurora issue; don't keep it bundled here.
- **Prepared work waiting:** Agent applies the approved mapping via guarded REST (create-only/reversible, rollback recorded), readback-verifies each reassignment, and re-runs a category-distribution count to prove the Misc bucket shrank. No new mapping authoring needed — it's already written and waiting on your approve/redline.

---

## 5. Content-credential sections — #13 (BC+AI), #14 (Indigenomics), #15 (The Upgrade AI)

- **Blocker:** All three need **you to write/approve the bio copy and confirm the stats** before any agent drafts or publishes a section. These are public claims about your roles and partners — they must be in your voice and factually yours, not agent-invented.
- **KK input needed (the exact gaps):**
  - **#13 BC+AI:** confirm title ("Executive Director, BC+AI"), and the **stats** — "2,000+ members, 250+ Vancouver AI monthly, policy/government advisory." Are those current and OK to publish? Provide 2–3 sentences on community-impact areas. CTA wording for "Join BC+AI."
  - **#14 Indigenomics.ai:** confirm title ("CTO, Indigenomics.ai") and the **"$200B+ Indigenous economic discovery"** claim (this is a strong public number — confirm it's attributable and you want it on your personal site). 2–3 sentences on the sovereignty / tech-for-justice framing. Partnership-inquiry CTA wording.
  - **#15 The Upgrade AI:** confirm "Co-founder (with Peter Bittner)," confirm which **Fortune 500 clients** (if any) you can name publicly, the "democratizing AI" mission line, and the training-inquiry CTA + correct platform link.
- **Recommendation:** **DEFER until you batch the copy** (one ~20-minute pass for all three), then **build.** They're high-value credibility sections but fully blocked on your voice/claims — no agent should guess role stats or a $200B figure. Once you supply the copy, they're straightforward Aurora section builds.
- **Prepared work waiting:** Agent can pre-stage the section scaffolds (layout, links to bc-ai.ca / indigenomics.ai / The Upgrade, CTA blocks, mobile + WCAG AA structure) with your copy dropped in, then produce a draft preview for review. Nothing goes live without your sign-off. *Note: about-page CSS lives in an inline `<style>` block edited via WP REST — see memory `about-page-inline-style-block`.*

---

## 6. Broad epics & marketing — one-line calls

| Issue | What it is | Blocker | Recommendation |
|---|---|---|---|
| **#222** | EPIC: harden platform trust / forms / publisher ops (coordinates #128, #174, #173, #196, #197, #75) | Coordinating shell; depends on the contact-form lanes in item 3 | **Keep open as tracker; act via item 3.** Once #174 passes and you set the triage policy, this epic's form criteria clear. Decision gate is just "form-routing first" — yes, do that. |
| **#219** | EPIC: restore KrisKrug.co content cadence | Largely **already satisfied** — cadence is live through 07-02, #207/#208 closed | **Close or downgrade.** Verify the draft queue once; the cadence is running. Item 1 (3-post drop) is the live sub-decision. |
| **#64** | Unified search across all 6 projects (Elasticsearch) | Huge scope; depends on #61 ingest + infra; no source-of-truth or budget decided | **DEFER.** Park until #61 ingest strategy exists; this is a quarter-scale project, not a swarm task. |
| **#62** | Unified event calendar / Luma API | Needs Luma source-of-truth + API creds + publishing boundary; spike (#177/PR #212) shows MVP feasible by extending `kk-sidebar-promos` | **RESCOPE to a narrow one-feed "upcoming events" MVP** (per `LUMA-UPCOMING-EVENTS-SPIKE-2026-06-11.md`), gated by #196. KK input: which single Luma iCal feed + OK to extend the plugin. Defer the full multi-calendar portal. |
| **#61** | Ingest Indigenomics KB (1.13M words) | No ingest strategy, attribution/permission model, or storage decided | **DEFER pending a strategy note.** KK input: do you have **rights/attribution clearance** from Indigenomics to surface this on kriskrug.co, and is the target a search index vs. published pages? Agent can draft a read-only ingest/attribution plan first — no ingest until you decide. |
| **#51** | Email onboarding sequences (6 sequences) | No email infra decision; you run **Beehiiv** across 3 pubs — issue predates that | **RESCOPE to Beehiiv.** KK input: which pub owns kriskrug.co subscribers, and which 1–2 sequences matter (new-subscriber + re-engagement?). Drop the "6 sequences / 15–25% conversion" spec as over-scoped. Defer until #49 lead magnets exist (sequences need something to deliver). |
| **#49** | 5 audience-specific lead magnets | No magnet content authored; depends on your voice + positioning | **DEFER, then rescope to 1–2.** KK input: which **one** audience first (creatives? Indigenous leaders? journalists?). Building all 5 at once is the trap; pick one, prove the funnel, then scale. Pairs with #51. |

---

## Risks & guardrails (apply to every item above)

- **Live-write gate:** every WordPress publish/flip is human-gated and requires snapshot/readback + rollback path (slug/ID/version checks). No agent publishes without your explicit window.
- **PII / CASL:** all contact-form submitter data stays in Gmail/Jetpack CSV, never in repo, issues, or commits. No bulk newsletter adds — opt-in only.
- **Public claims:** role titles, member counts, and the $200B Indigenomics figure are your claims to confirm; agents won't invent or publish them.
- **Voice:** all public copy in KK voice, no em-dashes, no AI-polished tone (per memory rules).
- **Pagely cache:** REST/admin edits don't auto-purge; every deploy needs a Pagely page-cache purge + logged-out render check.

## Next handoff

- **On your "publish" for items 1 & 2:** hand to **build-implement** for the staged publish scripts, then **safety-review** before the live flip (public publish + backlinks).
- **On your contact-form filter/policy (item 3):** hand to **build-implement** for the Gmail-filter spec + external test, **safety-review** before any test submission or historical-triage action.
- **On your category map (item 4):** hand to **build-implement** to apply the reversible mapping.
- **For #13/#14/#15 copy:** once you supply bios, hand to **growth-content** to draft, then **build-implement** for the Aurora sections.
- **For epics #61/#62/#51/#49:** hand to **strategy-plan** for the narrow rescope notes before any build.
