# Publish gate — Keep the Machine Strange (2026-06-28)

**PUBLISHED 2026-08-10** (KK approval in-session): https://kriskrug.co/2026/08/10/keep-the-machine-strange/
Post 12410, dated 2026-08-10 at publish. Pre-publish voice audit in `voice-audit/` (verdict GO; one line edit applied at line 107, `--update` refreshed the body, then status flipped via slug-verified REST). Logged-out readback verified: HTTP 200, SEO title in `<title>`, McLuhan og:image, homepage + feed listing. Pre-publish snapshot retained in session scratchpad.

**2026-08-10 post-publish embed round** (KK request): added two verified-embeddable Postman videos — `hlrv7DIHllE` (College of DuPage, Surrender of Culture lecture) after the "in his own voice" paragraph, and `W36sM3_KY0k` (The Open Mind w/ Richard Heffner, taped 1985-12-14) after the Huxley paragraph. The 1995 PBS Cyberspace clip (`49rcVQ1vFAY`) is still embed-blocked (oEmbed 403); an anonymous "1992 Technopoly" upload was rejected for unverifiable provenance. Live via in-place body PATCH from rebuilt post.html; snapshot in session scratchpad. Featured-image replacement pending KK approval (see featured-image-forge skill).

DRAFT staged. Create on kriskrug.co:
  python3 scripts/notion-to-wp/publish_keep_the_machine_strange.py            # dry-run
  python3 scripts/notion-to-wp/publish_keep_the_machine_strange.py --execute  # draft-only, slug-idempotent

Routing: post; categories AI Ethics & Philosophy (1678) + Responsible AI & Policy (1754); status=draft.

Citation hygiene:
- "technological resistance: a discerning, lucid, vigilant engagement…" = contemporary paraphrase, NOT Postman. Said so in the piece.
- Verified: Technopoly Ch.11 ("strange, never inevitable, never natural"; "embedded in every tool…"); "Five Things" 1998 ("technology giveth…"; "what will a new technology undo?"); Amusing Ourselves to Death (Huxley). Agentic shift = Milgram, used by Postman (Technopoly Ch.7).

Receipts (verified + corrected):
- Stanford AI Index 2026: 53% gen-AI adoption = GLOBAL (US 28.3%).
- Canada "AI for All" (2026-06-04): $200B, 250k jobs, 12%->60% by 2034; "serves Canadians" = Min. Evan Solomon.
- AIDA died on order paper Jan 2025; no binding federal AI law. NIST AI RMF; OECD 2024 update for "human agency and oversight".

Media: McLuhan global-village embed (CBC 1960, HeDnPP6ntic, verified). Featured: McLuhan 1967 (public domain, LoC). Section art: Gutenberg press (CC BY 2.0, dronepicr); attribution in captions. No free Postman portrait; two Postman interview clips were not embeddable, so rendered as prose. img/ working copies are re-fetched by the script + uploaded to WP media; not committed.

Dry-run: 80 blocks | 9 headings, 5 pullquotes, 4 quotes, 1 embed, 2 images, 2 lists.
