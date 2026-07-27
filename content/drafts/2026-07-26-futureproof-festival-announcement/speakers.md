# Futureproof Festival — public speaker lineup (#498 / FP-2)

Verified **2026-07-26T19:47Z** against public web only.

**Safety gate:** active speaker embargo. Local festival allowlist / pipeline files were **not** available on this VM (`~/Code/futureproof-festival/...`). Clearance below is based solely on live public pages at [futureproof.website](https://www.futureproof.website/). No allowlist JSON was read or edited.

**Public source of truth used:**
- Directory: https://www.futureproof.website/speakers/ (heading: "Public Futureproof Festival speakers") — HTTP 200
- Per-speaker profile URLs under `/speakers/<slug>/` — each HTTP 200
- Public news announcements where linked from profiles (HTTP 200)
- Site payload field `confirmed: true` on each directory entry (read-only observation from public HTML/RSC)

**For FP-3:** announce only the **Cleared** list below. Do not invent additional names.

---

## Cleared / public (safe to announce)

Directory order as listed on `/speakers/` (festival director Kris Krüg also appears publicly there; out of scope for this issue's 8-name checklist — see note at bottom).

| Name | Affiliation (title · org) | Live link | Verification note |
|---|---|---|---|
| **Amber Case** | Founder · Calm Tech Institute | https://www.futureproof.website/speakers/amber-case/ | On public `/speakers/` directory (`data-speaker-directory-entry="amber-case"`, `confirmed: true`). Live profile HTTP 200. Public news: https://www.futureproof.website/news/2026-07-18-amber-case-joins-futureproof (HTTP 200). |
| **Ana Serrano** | President & Vice-Chancellor · OCAD University | https://www.futureproof.website/speakers/ana-serrano/ | On public `/speakers/` directory (`confirmed: true`). Live profile HTTP 200. Public news: https://www.futureproof.website/news/2026-07-18-ana-serrano-joins-futureproof (HTTP 200). |
| **Lynda Brown-Ganzert** | CEO · RxPx Inc | https://www.futureproof.website/speakers/lynda-brown-ganzert/ | On public `/speakers/` directory (`confirmed: true`). Live profile HTTP 200. Public news: https://www.futureproof.website/news/2026-07-18-lynda-brown-ganzert-joins-futureproof (HTTP 200). |
| **Zaro** (Gabriel "Zaro") | Community Intelligence Architect · zaro.me | https://www.futureproof.website/speakers/gabe-zaro/ | Public site lists display name **Zaro** (slug `gabe-zaro`), not "Gabriel". On public `/speakers/` directory (`confirmed: true`). Live profile HTTP 200. Own site live: https://www.zaro.me/ (HTTP 200; `zaro.me` redirects there). Public news: https://www.futureproof.website/news/2026-07-19-zaro-joins-futureproof (HTTP 200). |
| **Mayumi Rollings** | Founder & CEO · Tiny Ghost Studios | https://www.futureproof.website/speakers/mayumi-rollings/ | On public `/speakers/` directory (`confirmed: true`). Live profile HTTP 200. Public news: https://www.futureproof.website/news/2026-07-21-mayumi-rollings-joins-futureproof (HTTP 200). |
| **Anthonia Ogundele** | Founder & Executive Director · Ethọ́s Lab | https://www.futureproof.website/speakers/anthonia-ogundele/ | On public `/speakers/` directory (`confirmed: true`). Live profile HTTP 200. Public news: https://www.futureproof.website/news/2026-07-21-anthonia-ogundele-joins-futureproof (HTTP 200). |
| **Kaoru Yoshihira** | Head of Partner Development · BytePlus | https://www.futureproof.website/speakers/kaoru-yoshihira/ | On public `/speakers/` directory (`confirmed: true`). Live profile HTTP 200 with full bio. Card shows "Portrait pending"; public payload has `publicProfile: null` (no featured artwork / news post yet) but the name is still publicly listed on the speakers directory and profile route. Cleared on that public listing. |
| **Peter Bittner** | AI Trainer & Consultant · The AI Upgrade | https://www.futureproof.website/speakers/peter-bittner/ | On public `/speakers/` directory (`confirmed: true`). Live profile HTTP 200. |

### Copy-ready lineup (name → affiliation → link)

1. Amber Case — Founder, Calm Tech Institute — https://www.futureproof.website/speakers/amber-case/
2. Ana Serrano — President & Vice-Chancellor, OCAD University — https://www.futureproof.website/speakers/ana-serrano/
3. Lynda Brown-Ganzert — CEO, RxPx Inc — https://www.futureproof.website/speakers/lynda-brown-ganzert/
4. Zaro — Community Intelligence Architect, zaro.me — https://www.futureproof.website/speakers/gabe-zaro/ (also https://www.zaro.me/)
5. Mayumi Rollings — Founder & CEO, Tiny Ghost Studios — https://www.futureproof.website/speakers/mayumi-rollings/
6. Anthonia Ogundele — Founder & Executive Director, Ethọ́s Lab — https://www.futureproof.website/speakers/anthonia-ogundele/
7. Kaoru Yoshihira — Head of Partner Development, BytePlus — https://www.futureproof.website/speakers/kaoru-yoshihira/
8. Peter Bittner — AI Trainer & Consultant, The AI Upgrade — https://www.futureproof.website/speakers/peter-bittner/

---

## HOLD — do not announce

**None of the eight issue-named speakers are on HOLD.**

Each was found on the public Futureproof speakers directory with a live `/speakers/<slug>/` page at verification time.

If a later re-check removes a name from https://www.futureproof.website/speakers/ or returns non-200 on their profile, move that name here before any announce copy ships.

---

## Verification matrix

| Issue name | Public display name | Slug | Directory | Profile HTTP | `confirmed` | News / own site | Status |
|---|---|---|---|---|---|---|---|
| Amber Case | Amber Case | `amber-case` | yes | 200 | true | news 200 | **CLEARED** |
| Ana Serrano | Ana Serrano | `ana-serrano` | yes | 200 | true | news 200 | **CLEARED** |
| Lynda Brown-Ganzert | Lynda Brown-Ganzert | `lynda-brown-ganzert` | yes | 200 | true | news 200 | **CLEARED** |
| Gabriel "Zaro" | Zaro | `gabe-zaro` | yes | 200 | true | news 200; zaro.me 200 | **CLEARED** |
| Anthonia Ogundele | Anthonia Ogundele | `anthonia-ogundele` | yes | 200 | true | news 200 | **CLEARED** |
| Mayumi Rollings | Mayumi Rollings | `mayumi-rollings` | yes | 200 | true | news 200 | **CLEARED** |
| Peter Bittner | Peter Bittner | `peter-bittner` | yes | 200 | true | (no news link on profile) | **CLEARED** |
| Kaoru Yoshihira | Kaoru Yoshihira | `kaoru-yoshihira` | yes | 200 | true | portrait pending; `publicProfile` null | **CLEARED** (public directory + live profile) |

---

## Evidence URLs (cited)

- https://www.futureproof.website/speakers/
- https://www.futureproof.website/speakers/amber-case/
- https://www.futureproof.website/speakers/ana-serrano/
- https://www.futureproof.website/speakers/lynda-brown-ganzert/
- https://www.futureproof.website/speakers/gabe-zaro/
- https://www.futureproof.website/speakers/mayumi-rollings/
- https://www.futureproof.website/speakers/anthonia-ogundele/
- https://www.futureproof.website/speakers/kaoru-yoshihira/
- https://www.futureproof.website/speakers/peter-bittner/
- https://www.futureproof.website/news/2026-07-18-amber-case-joins-futureproof
- https://www.futureproof.website/news/2026-07-18-ana-serrano-joins-futureproof
- https://www.futureproof.website/news/2026-07-18-lynda-brown-ganzert-joins-futureproof
- https://www.futureproof.website/news/2026-07-19-zaro-joins-futureproof
- https://www.futureproof.website/news/2026-07-21-mayumi-rollings-joins-futureproof
- https://www.futureproof.website/news/2026-07-21-anthonia-ogundele-joins-futureproof
- https://www.zaro.me/

---

## Notes for downstream (FP-3 / human review)

1. **Display name for Zaro:** public site uses **Zaro**. Prefer that over "Gabriel" in announce copy unless KK directs otherwise; slug remains `gabe-zaro`.
2. **Kaoru Yoshihira:** cleared via public directory + live profile; artwork/news still thin ("Portrait pending"). Worth a human glance before hero treatment.
3. **Also public on `/speakers/` but not in #498's eight:** Kris Krüg (Founder & Festival Director, BC + AI Ecosystem Association) — https://www.futureproof.website/speakers/kris-krug/. FP-3 may reference him as festival director separately; not counted in this checklist.
4. **Local allowlist gap:** when festival-repo allowlist/pipeline are available, re-cross-check before publish. This package does not claim allowlist-file clearance.
5. **No WP writes. No allowlist edits.** Track A draft artifact only.
