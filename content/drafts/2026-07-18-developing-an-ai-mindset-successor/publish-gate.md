# Publish and routing gate

**Status:** Draft-only, human-gated handoff.

This packet does not authorize a WordPress, cache, Search Console, DNS, registrar, hosting, Vercel, redirect, or production change.

## Current state receipt

- On 2026-07-18, `https://developinganaimindset.com/` returned `307` to the public Notion page.
- On 2026-07-18, `https://kriskrug.co/speaking/developing-an-ai-mindset/` returned `404`.
- The old-domain root must stay unchanged until the successor is public, healthy, and verified while logged out.

## Gate 1: human copy and source approval

- [ ] Kris approves the visible page copy, title, excerpt, primary CTA, and related links.
- [ ] A human reviewer checks every material factual claim against `source-manifest.md`.
- [ ] The reviewer confirms that no private Notion material, unsupported event claim, audience count, testimonial, client outcome, duration, price, or guarantee entered the copy.
- [ ] The reviewer confirms the intended voice is Builder-first with a little Host warmth, and that no generic hype or forced swagger was added.
- [ ] The reviewer approves an image with confirmed reuse rights, or explicitly chooses a text-first page with no social image.

## Gate 2: WordPress preview

- [ ] A human publisher confirms a WordPress page preview exists at the intended nested route and remains unpublished during review.
- [ ] The preview matches `post.md` after any approved edits.
- [ ] There is exactly one visible H1: `Developing an AI Mindset`.
- [ ] The opening and closing CTAs resolve to the canonical Speaking page.
- [ ] The Innovate West deck, Punk Rock AI, Both Hands Full, and RAP links resolve to the approved destinations.
- [ ] Desktop and mobile previews have readable headings, lists, link states, and focus order.
- [ ] Any selected image has approved alt text and uses a stable WordPress-hosted asset rather than a temporary Notion URL.

## Gate 3: metadata and schema review

- [ ] Document title, canonical, standard meta description, Open Graph fields, Twitter fields, excerpt, and robots directives match `seo-meta.md` or a documented human-approved revision.
- [ ] The standard meta description remains between 140 and 160 characters.
- [ ] The canonical is exactly `https://kriskrug.co/speaking/developing-an-ai-mindset/`.
- [ ] Logged-out HTML contains one canonical tag and no reference to the old domain or Notion as canonical.
- [ ] Logged-out JSON-LD parses without errors.
- [ ] The page has one `WebPage` identity for the canonical route and references `https://kriskrug.co/#person`.
- [ ] The existing sitewide Person node remains the only Kris Krüg Person identity. No second Person owner or node was added.
- [ ] No `Event`, `Course`, `FAQPage`, or unsupported offer schema appears unless the visible copy and verified sources are separately expanded to satisfy it.

## Gate 4: live successor verification

- [ ] A human explicitly approves publication after the preview and metadata review.
- [ ] The public successor returns `200` while logged out on an ordinary request and a fresh cache-busted request.
- [ ] The public body, H1, CTA, links, canonical, metadata, and schema match the approved preview.
- [ ] The page is reachable from the KrisKrug.co Speaking surface without relying on the old domain.
- [ ] The page remains healthy after the ordinary site cache has settled.

If any check fails, stop. Fix and re-verify the successor before considering old-domain routing.

## Gate 5: provider-neutral old-domain handoff

- [ ] A human separately authorizes the exact routing map in `redirect-map.csv`.
- [ ] The domain operator identifies the current routing provider and captures the existing rule set as a rollback receipt before any change.
- [ ] The exact `/` rule is evaluated before the unmatched-path rule.
- [ ] `/` receives one permanent hop to the canonical successor, with no Notion hop and no generic KrisKrug.co homepage hop.
- [ ] `/robots.txt`, `/sitemap.xml`, and every other unmatched path receive `410 Gone` unless a future evidence review adds a truthful equivalent route.
- [ ] If a live `www` host alias is discovered during the human provider review, it receives the same reviewed disposition as the corresponding apex path. This packet does not claim that alias is currently provisioned.
- [ ] HTTPS behavior, certificate health, query-string handling, and trailing-slash behavior are verified by the domain operator without changing the content mapping.
- [ ] The final public response chain and status for every CSV row are recorded in a separate deployment receipt.

## Stop and rollback conditions

Stop the routing change if the successor returns anything other than the approved `200`, loses its canonical or metadata, emits duplicate identity schema, breaks logged-out rendering, or sends the root through more than one hop.

If a post-change failure appears, the domain operator should restore the captured pre-change rule set and leave the old domain on its prior behavior until the successor is healthy again. Do not improvise a redirect to the KrisKrug.co homepage.

## Search Console boundary

Search Console inspection, indexing requests, change-of-address decisions, sitemap work, and property administration are separate human-approved operations. None is required to review or merge this repository packet.

## Completion definition

This repository issue is complete when the five-file packet is reviewed in a PR and the repository checks pass. Publication, cache work, link replacement on existing pages, Search Console activity, and old-domain routing remain separate human-gated work after merge.
