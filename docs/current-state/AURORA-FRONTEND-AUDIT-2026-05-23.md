# Aurora Front-End Audit — harsh critique (2026-05-23)

Live audit of the `kk-aurora` theme on kriskrug.co. Method: rendered inspection + computed styles + the inlined critical CSS and loaded scripts. **Caveat:** Jetpack Boost defers the non-critical stylesheet, so some hover/focus/transition rules may live in CSS not fetched here — items tagged *(verify in full CSS)* need a look at the deferred sheet. The showstopper is observed live and is not a measurement artifact.

---

## 🔴 SHOWSTOPPER — the homepage is a black void for everyone

The front page renders **blank above and below the fold**. The content is in the DOM, but **6 of 7 sections (hero copy, feature band, every media card) are stuck at `opacity:0`** — including the hero, which already has the `is-revealed` class applied yet still computes `opacity:0; transform:translateY(20px)`. `prefers-reduced-motion` is **OFF**, so this is not an edge case — **every visitor sees nothing.**

**Root cause:** reveal visibility is **gated on GSAP + ScrollTrigger** (loaded from `cdn.jsdelivr.net`). Content's *base* state is `opacity:0`, and only the JS animation is supposed to bring it to `1`. The animation isn't applying the end state, so everything stays invisible. This is the cardinal sin of scroll animation: **content is hidden by default and depends on JS to become visible.**

**Fix (do this first, before any aesthetic work):**
- Make content **visible by default**; reveal is an *enhancement*, not a gate. Baseline `opacity:1`; only set the from-state when JS is confirmed running (e.g. add a `js`/`gsap-ready` class to `<html>` and scope the hidden from-state to `.gsap-ready .aurora-reveal`).
- Add a hard fallback: `@media (prefers-reduced-motion: reduce){ .aurora-reveal{opacity:1!important;transform:none!important} }` and a no-JS fallback.
- Then fix the ScrollTrigger init so the play state actually applies.

## 🔴 ARCHITECTURE — render-gating on a third-party CDN

Two libraries (`gsap.min.js` + `ScrollTrigger.min.js`) pulled from **jsdelivr** power *decorative* scroll reveals — and currently gate whether the page is visible at all. If that CDN is slow, blocked (corp firewall, ad-block, GDPR/privacy tooling), or rate-limited, the homepage is **permanently blank**. That's a lot of fragility + ~50KB+ + a third-party dependency for fade-ins.
**Recommend:** self-host GSAP *or* replace with `IntersectionObserver` + CSS transitions (no dependency, lighter, robust). Either way, **never let it control base visibility.**

## 🟠 ACCESSIBILITY — no visible keyboard focus

`:focus-visible` appears **0×** in the critical CSS *(verify in full CSS)*. If it's truly absent, keyboard users get no visible focus ring — a WCAG 2.4.7 failure on a site that's otherwise polished. Add a branded focus ring (cyan glow outline) globally.

## 🟠 BRAND / BADASSERY — you built a neon engine and left it in the garage

The token system is genuinely cool and on-brand: `--aurora-primary` is a **cyan→teal→purple** gradient, `--aurora-secondary` **purple→pink** (#8B5CF6→#EC4899), plus radial **glow** washes (cyan + amber) on the body, 91 gradient declarations, glow/box-shadow tokens. **But the rendered pages read flat dark + one cyan** — the purple/pink/gradient/glow arsenal is barely visible. The result is *tasteful and safe*, not *techartist / cyberpunk anti-hero*.
**Deploy the neon (tastefully):**
- Gradient-fill the big hero `h1` (it's `clamp(…,8.2rem)` / weight 900 — a perfect canvas) or key accent words.
- Use the radial glows behind hero + section breaks so the black has depth instead of dead flatness.
- One signature move repeated: a cyan→purple underline/edge on links/CTAs, a soft glow on the primary button on hover.
- Restraint rule: pick 2–3 places to go loud (hero, CTA, section anchors); keep the rest calm so it reads designed, not Geocities.

## 🟡 INTERACTIONS & ANIMATION

- Only **5 `:hover` rules** in critical CSS *(verify in full CSS)* — micro-interactions feel thin. Cards, nav links, and buttons should each have a deliberate, fast (120–180ms) hover with transform/glow.
- Animation is **all GSAP**; there are **0 CSS transitions/keyframes** in the critical CSS, so anything not scripted is abrupt. Add CSS transitions for the small stuff (hover, focus, button press) and reserve GSAP for the one or two hero moments.
- The reveal motion itself (`translateY(20px)` fade) is generic. For KK, consider one characterful entrance (e.g. a quick clip-path wipe or a glitch/scanline flash on the hero) — singular, not on every block.

## 🟡 GLASSMORPHISM

Present and reasonable: `backdrop-filter: blur(18px)` (the sticky header reads as frosted glass) with a `backdrop-filter:none` fallback. Good baseline.
**Push it where it earns attention:** a frosted card treatment for the "Book Kris" CTA region or the nav-on-scroll, and frosted overlays on image cards. **Don't** glass everything — blur is expensive (watch mobile perf) and turns to mud over busy backgrounds. Pair every glass surface with a 1px light hairline border (you have `--aurora-line`) so edges read.

## 🟡 WIDGETS / FOOTER / CHROME *(couldn't fully audit — browser contention)*
- Header is clean (logo + 7-item nav + Newsletter + cyan "Book Kris"). Solid; consider scroll-state (shrink/frost-intensify).
- Footer + any widgets (newsletter, events, latest posts) need their own dark-theme + voice pass — verify they're not the old light-theme leftovers.
- There's a duplicate page-title H1 on generic-template pages (theme prints the title above my content hero) — dedupe.

---

## Priority order
1. **Fix the blank homepage** (visibility-by-default + reveal fallback + ScrollTrigger init). Nothing else matters until the page is visible.
2. De-risk GSAP (self-host or IntersectionObserver; never gate visibility).
3. Add `:focus-visible` globally.
4. **Deploy the neon** — gradient hero headline + radial glows + one signature hover. This is the "badassery" delta.
5. Micro-interaction pass (hover/transition on cards/nav/buttons).
6. Widgets/footer dark+voice pass; dedupe the title H1.

**Bottom line:** the foundation (dark canvas, Inter, fluid type, a real gradient/glow token system, glass header) is genuinely strong — but it's shipping **broken (invisible homepage)** and **timid (neon unused)**. Fix the visibility, then turn the brand up. The ingredients for badass are already in the stylesheet; they're just not on the plate.
