# LinkedIn gaps — testimonials overhaul

Verified profile URLs only. Do **not** invent slugs. Cite as plain text until KK (or a people-profile update) supplies a URL.

---

## v2 resolution table (TSTM-2, #595, 2026-08-01)

Resolution order: (1) `kk-kb/content/people/*/` profiles and sources, (2) live `/testimonials/` cites (public readback 2026-08-01), (3) web verify. A URL ships only when the evidence chain confirms both that the slug exists and that it belongs to this person. `MISSING` means resolution was attempted and no confirmable URL exists. `SKIP` means resolution is not attemptable (no resolvable identity anchor).

Useful calibration from this pass: LinkedIn returns **404** for a dead or renamed slug even to logged-out clients, and **999** (bot wall) for slugs that exist but are guest-blocked. So a 999 confirms slug existence; a 404 means the slug is gone.

### Priority names (packet list)

| Person | Status | URL | Evidence path |
|---|---|---|---|
| Simon Haworth | FOUND | https://ca.linkedin.com/in/simon-haworth-uk-us-prc | Web verify: search result "Simon Haworth - Intelligent OMICS Ltd", Vancouver, matches kb CEO of Intellomx/Intelligent OMICS with UK/Vancouver/Wuhan-PRC footprint (`kk-kb/content/people/simon-haworth/profile.md`, `.../sources/office-hours-2025-10-24.md`). HTTP 200. **Old kb/live URL `linkedin.com/in/simon-haworth` now 404s (slug changed); TSTM-5 must swap the live cite.** |
| Arno Apeldoorn | MISSING | | `kk-kb/content/people/arno-apeldoorn/profile.md` has no URL; newcollider.com shows no social links; ContactOut confirms a LinkedIn exists (Owner, New Collider Creative) but exposes no slug. Do not guess. |
| Ishtar Beck | FOUND | https://ca.linkedin.com/in/ishtar-beck-ma-rcc-73711761 | Web verify: search result "Ishtar Beck, MA, RCC - CounsellingHome", Vancouver; distinctive name + city match. HTTP 999 (slug exists). Caveat: `kk-kb/content/people/ishtar-beck/profile.md` has no role anchor to cross-check; KK eyeball logged-in before public cite. |
| Jesse Benson | FOUND | https://www.linkedin.com/in/jesse-robert-benson/ | First-party chain: kb lists jessebenson.ca (`kk-kb/content/people/jesse-benson/profile.md`); jessebenson.ca links this exact profile (fetched 2026-08-01). |
| Gus Santos | MISSING | | `kk-kb/content/people/gus-santos/sources/public-enrichment-2026-05-13.md`: "no verified professional profile found". Common name, no role anchor to disambiguate. |
| Alex Samur | FOUND | https://www.linkedin.com/in/alexandrasamur | `kk-kb/content/people/alex-samur/profile.md` |
| Sean Copeland | MISSING | | `kk-kb/content/people/sean-copeland/sources/public-enrichment-2026-05-15.md`: "Multiple matches for this name; no single confirmed public profile" (only a LinkedIn pub-dir search URL). Strongest web candidate `/in/seancopeland` (TuffTek, AI/sales) has no confirmed BC/Vancouver tie. Do not guess. |
| Aynsley Vogel | FOUND | https://ca.linkedin.com/in/aynsley-vogel-6158293 | Web verify: search result "Aynsley Vogel - Director of Development at Paperny Films", Vancouver, CBC/TV background; matches kb "podcast producer, self-described old media" (`kk-kb/content/people/aynsleyvogel/profile.md`). HTTP 999 (slug exists). |
| Penn Father (= Patrick Parra Pennefather) | FOUND | https://www.linkedin.com/in/patrickpennefather | "Penn Father" is the transcript spelling of Dr. Patrick Parra Pennefather, UBC (`kk-kb/content/people/kevin-hayes/sources/meetups.md`). Web verify: his own posts publish under `linkedin.com/posts/patrickpennefather_...` with UBC context, which fixes the vanity slug. HTTP 999 (slug exists). |
| Brittney Ashley | FOUND | https://www.linkedin.com/in/brittneyashley | `kk-kb/content/people/brittney-ashley/profile.md` |
| Rachel Krayenhoff | FOUND | https://www.linkedin.com/in/rachel-krayenhoff | `kk-kb/content/people/rachel-krayenhoff/profile.md` |
| Daniel Bashaw | FOUND | https://www.linkedin.com/in/danbashaw | `kk-kb/content/people/dan-bashaw/profile.md` |
| Allan Baedak | FOUND | https://www.linkedin.com/in/allanbaedak | `kk-kb/content/people/allan-baedak/profile.md` |
| Bruce Ratzlaff | FOUND | https://www.linkedin.com/in/bruce-ratzlaff-bb926a40 | `kk-kb/content/people/bruce-ratzlaff/profile.md` |
| Melisa DiPietro | FOUND | https://ca.linkedin.com/in/meldip | Web verify: public profile renders logged-out (HTTP 200) showing Flock n Fur ("FlocknFir") and a Responsible AI Professional Certification issued in BC, matching kb RAP Cohort 1 context (`kk-kb/content/people/melisa-dipietro/sources/rap-cohort-1-class-1.md`, which had "URL not captured"). |
| Marty Avery | FOUND | https://www.linkedin.com/in/martyavery | KK personal LinkedIn export, recommender link (`kk-kb/content/people/kris-krug/sources/kk-personal-2026-06-03/bios-identity/kk-background-bio-info-life.md`). HTTP 999 (slug exists). |
| Joel Solomon | FOUND | https://www.linkedin.com/in/joel-solomon-a5a4b5 | KK personal LinkedIn export, recommender link, "Co-Founding Partner at Renewal Funds" (same file as Marty Avery). |
| Harrison Reed | MISSING | | AI Upgrade testimonial context only (`kk-kb/content/projects/02-bc-ai-ecosystem-nonprofit/founding-member-campaign-2025/testimonial-directory.md`, "Digital Marketing Specialist"). No kb person dir; web candidates (e.g. `/in/hj-reed`, R1 RCM healthcare) do not match. Do not guess. |
| Jill Manuel | FOUND | https://www.linkedin.com/in/jillannmanuel/ | Web verify: search result "Jill Manuel - JCat Group \| LinkedIn" at this URL, plus her posts tagged #jcatgroup; matches testimonial attribution "JCat Group, AI Upgrade Graduate" (same testimonial-directory.md). HTTP 200 after 301. |
| Pete Young | FOUND | https://www.linkedin.com/in/pete-young-8a7a89a5 | `kk-kb/content/people/pete-young/sources/member-directory-2025.md` |
| Darren Nicholls | FOUND | https://www.linkedin.com/in/darren-nicholls | `kk-kb/content/people/darren-nicholls/profile.md` |
| carla ritchie | FOUND | https://ca.linkedin.com/in/carla-ritchie-mba-8ba5851a3 | `kk-kb/content/people/carla-ritchie/profile.md` |
| Volodya | SKIP | | Mononym; `kk-kb/content/people/volodya/profile.md` has no surname, org, or public anchor. Nothing to resolve against. |
| Kaoru Yoshihira | FOUND | https://jp.linkedin.com/in/kaoruyoshihira | `kk-kb/content/people/kaoru-yoshihira/sources/2026-07-19-futureproof-speaker-bio.md` |
| Melinda Wittstock | FOUND | https://www.linkedin.com/in/melindawittstock/ | Web verify: search result for this URL plus her own posts under `linkedin.com/posts/melindawittstock_...` as "CEO Founder Podopolo". HTTP 200. |
| Steve Jones, CFA | FOUND | https://www.linkedin.com/in/jonessteven | Live `/testimonials/` cite (readback 2026-08-01) + VeilStream CEO public profile (v1 verification). Note: kb `steven-jones` is a different thin profile; do not conflate. |
| Suzy Easton | FOUND | https://www.linkedin.com/in/suzyeaston | Live `/testimonials/` cite (readback 2026-08-01); v1 verification (Vancouver AI / BC + AI). |
| Stewart Butterfield | FOUND | https://www.linkedin.com/in/butterfield/ | **Archive only** per #593 board (2006 photography rec; never the conference/camera quote, which is Rob Cottingham's). Web verify: search result "Stewart Butterfield - New York, New York \| Professional Profile" at this URL. HTTP 200 after 301. |
| Kristen Hughes | FOUND | https://www.linkedin.com/in/kristen-hughes-b403705 | KK personal LinkedIn export, recommender link, "Co-Founder and Creative Director at Hairpin" / PopTech attribution (`.../bios-identity/kk-background-bio-info-life.md`). |

### TSTM-1 inventory fold-in (v1 inventory in tree; v2 expansion not yet merged)

Rows the merged `quote-inventory.md` marks `MISSING`, plus the already-linked ship set so TSTM-5 can join against one table.

| Person | Status | URL | Evidence path |
|---|---|---|---|
| Landon Steele | FOUND | https://www.linkedin.com/in/landonsteele | Live `/testimonials/` cite (readback 2026-08-01); resolves inventory row LI-LANDON `MISSING`. |
| Lucas Drury-Godden | FOUND | https://ca.linkedin.com/in/lucasdg | Web verify: search result "Lucas Drury-Godden - Vancouver, British Columbia, Canada" at this URL; distinctive hyphenated surname, VP Western Canada at Procom (ZoomInfo cross-ref). HTTP 200. Resolves inventory row LU-LUCAS `MISSING`. |
| Joshua Dunford | FOUND | https://www.linkedin.com/in/joshdunford | Live `/testimonials/` cite (readback 2026-08-01); resolves inventory row LEG-JOSH `MISSING`. |
| Benjamin Random | MISSING | | v1 finding stands: no reliable public LinkedIn match (inventory LEG-BEN). |
| Corey Dennis | MISSING | | v1 finding stands: Gnomedex-era attribution, ambiguous modern profiles (inventory LEG-COREY). |
| Claudine Co | MISSING | | v1 finding stands: no verified match for archival attribution (inventory LEG-CLAUDINE). |
| Danie Peace | MISSING | | v1 finding stands: no verified match (inventory LEG-DANIE). |
| Stephanie Vacher | FOUND | https://www.linkedin.com/in/stephanievacher | Live `/testimonials/` cite + KK LinkedIn export; resolves inventory row LEG-STEPH `MISSING`. |
| Rob Cottingham | FOUND | https://www.linkedin.com/in/robcottingham | Live `/testimonials/` cite + KK LinkedIn export. Attribution rule stands: never Butterfield on this quote. |
| Kerris Hougardy | FOUND | https://www.linkedin.com/in/kerrishougardy | Live `/testimonials/` cite + `kk-kb` LinkedIn capture (v1). |
| Carly Steiman | FOUND | https://www.linkedin.com/in/carlysteiman | Live `/testimonials/` cite + people profile (v1). |
| David Gloyn-Cox | FOUND | https://www.linkedin.com/in/dreffed | Live `/testimonials/` cite + LinkedIn capture (v1). |
| Fiann O'Hagan | FOUND | https://www.linkedin.com/in/fiann | Live `/testimonials/` cite + LinkedIn capture (v1). |
| Tavis Yeung | FOUND | https://www.linkedin.com/in/tavisyeung | Live `/testimonials/` cite + LinkedIn capture (v1). |
| Jai Djwa | FOUND | https://www.linkedin.com/in/djwa | Live `/testimonials/` cite + people profile (v1). |
| Ed Kennedy | FOUND | https://www.linkedin.com/in/kennedy-ed | Live `/testimonials/` cite + people profile (v1). |

### Spot-check (2026-08-01, logged-out curl, browser UA, redirects followed)

| URL | HTTP | Reading |
|---|---|---|
| https://ca.linkedin.com/in/simon-haworth-uk-us-prc | 200 | Renders logged-out |
| https://ca.linkedin.com/in/meldip | 200 | Renders logged-out (FlocknFir + BC RAP cert visible) |
| https://www.linkedin.com/in/butterfield/ | 301 → 200 | Renders logged-out |
| https://www.linkedin.com/in/jillannmanuel/ | 301 → 200 | Renders logged-out |
| https://www.linkedin.com/in/melindawittstock/ | 200 | Renders logged-out |
| https://ca.linkedin.com/in/lucasdg | 200 | Renders logged-out |
| https://www.linkedin.com/in/alexandrasamur | 999 | Known LinkedIn bot wall; slug exists (kb-sourced) |
| https://www.linkedin.com/in/martyavery | 999 | Known LinkedIn bot wall; slug exists (KK export-sourced) |
| https://www.linkedin.com/in/patrickpennefather | 999 | Known LinkedIn bot wall; slug exists (fixed by his posts URLs) |
| https://ca.linkedin.com/in/aynsley-vogel-6158293 | 999 | Known LinkedIn bot wall; slug exists (search-indexed) |
| https://ca.linkedin.com/in/ishtar-beck-ma-rcc-73711761 | 999 | Known LinkedIn bot wall; slug exists (search-indexed) |
| https://www.linkedin.com/in/simon-haworth/ | 404 | **Dead slug.** Currently linked on live `/testimonials/`; replace with `-uk-us-prc` URL in TSTM-5 |

### Flags for TSTM-5

1. **Live-page fix:** Simon Haworth's cite on `/testimonials/` points at the 404ing `linkedin.com/in/simon-haworth`; swap to `https://ca.linkedin.com/in/simon-haworth-uk-us-prc` when the payload is rebuilt.
2. **Stewart Butterfield URL is Archive-only** use, per the #593 hard-block rules.
3. **Ishtar Beck** row carries an identity caveat (unique name + city only); KK confirm logged-in before the URL goes on the public page.
4. kb `steven-jones` directory is not Steve Jones, CFA (VeilStream); the correct URL is the live-cited `jonessteven`.

### v2 counts

| Metric | Count |
|---:|---|
| Rows resolved | 45 (29 packet priority + 16 fold-in) |
| FOUND verified URLs | **36** (24 priority + 12 fold-in) |
| MISSING | 8 (Arno Apeldoorn, Gus Santos, Sean Copeland, Harrison Reed, Benjamin Random, Corey Dennis, Claudine Co, Danie Peace) |
| SKIP | 1 (Volodya, mononym) |
| Invented slugs | 0 |

---

## v1 (shipped #584) — historical below this line

Superseded by the v2 table above. Kept verbatim except where noted; the Simon Haworth v1 URL has since gone 404 (slug change), see v2 row.

## Verified (used as links in payload)

| Person | URL | Source |
|---|---|---|
| Kerris Hougardy | https://www.linkedin.com/in/kerrishougardy/ | LinkedIn capture + people profile |
| Landon Steele | https://www.linkedin.com/in/landonsteele | Public LinkedIn (Vancouver / Steele Consulting) |
| Carly Steiman | https://www.linkedin.com/in/carlysteiman/ | people profile |
| David Gloyn-Cox | https://www.linkedin.com/in/dreffed | LinkedIn capture + people profile |
| Fiann O'Hagan | https://www.linkedin.com/in/fiann/ | LinkedIn capture + people profile |
| Tavis Yeung | https://www.linkedin.com/in/tavisyeung/ | LinkedIn capture + people profile |
| Jai Djwa | https://www.linkedin.com/in/djwa/ | people profile |
| Ed Kennedy | https://www.linkedin.com/in/kennedy-ed/ | people profile |
| Steve Jones, CFA | https://www.linkedin.com/in/jonessteven | VeilStream CEO public profile |
| Simon Haworth | https://www.linkedin.com/in/simon-haworth/ | people profile — **404 as of 2026-08-01; superseded, see v2 table** |
| Suzy Easton | https://www.linkedin.com/in/suzyeaston | Public LinkedIn (Vancouver AI / BC + AI) |
| Rob Cottingham | https://www.linkedin.com/in/robcottingham | KK personal LinkedIn export in kk-kb |
| Joshua Dunford | https://www.linkedin.com/in/joshdunford | Burnkit partner public profile |
| Stephanie Vacher | https://www.linkedin.com/in/stephanievacher | KK personal LinkedIn export in kk-kb |

## Still plain text (no verified URL)

| Person | Quote IDs | Notes |
|---|---|---|
| Benjamin Random | A3 | No reliable public LinkedIn match |
| Corey Dennis | A4 | Historical IODA / Gnomedex-era; ambiguous modern profiles — leave unlinked |
| Claudine Co | A5 | No verified match for the archival attribution |
| Danie Peace | A7 | No verified match |

## Coverage snapshot (enriched ship set)

| Metric | Count |
|---:|---|
| Named people on page | 16 (+ 1 audience label) |
| LinkedIn-linked cites | 14 |
| Plain-text cites | 4 (Benjamin, Corey, Claudine, Danie) |
| LinkedIn coverage among named cites | **14 / 16 (~88%)** |
