# Published-page featured-image shortlist: October 25, 2026

Refs #1115. Read-only audit: **46 published pages, 37 with featured_media = 0**. Public REST was paginated at 20 items (three requests); unique IDs and the API total agree. A second enumeration returned the same 46 IDs and 37 missing-featured IDs. No WordPress or media writes occurred for this audit.

**Recommendation: preview one candidate, Media/Podcasts page 3609 with existing portrait media 12627. Do not bulk-fill the other pages.** Many already have in-content imagery or intentional text-first leads. Assigning featured media would add a template-level image above their body.

## Evidence and limits

- [Public REST inventory](https://kriskrug.co/wp-json/wp/v2/pages?status=publish&per_page=20&page=1); check time: 2026-10-25T22:49:53.749879+00:00.
- [Per-page rendered evidence and complete inventory](page-featured-image-audit-2026-10-25.json) contains all IDs, URLs, desktop/mobile heading geometry, first body images, OG URLs, judgments and screenshot hashes.
- All 37 missing-featured pages were rendered at 1440×1050 and 390×844: **74 successful captures**. All 46 page URLs resolved to HTTP 200; `/home/` redirects to `/`.
- Screenshots remain in the original checkout under `.generated/current-state/social-newsletter-2026-10-25/page-audit/screenshots/`. The JSON is the durable equivalent rendered evidence; screenshots are not committed.
- Third-party embeds were blocked during capture. No blank iframe is called broken from these screenshots. Below-fold lazy images are not judged by their loaded flag alone.
- “Intentional absence” means existing in-content imagery or a specialized renderer makes a new featured hero redundant. “Intentionally text-only” is this audit’s no-change recommendation, not a claim about an undocumented owner decision.

## Ranked shortlist

1. **Page 3609, Media/Podcasts → media 12627**, close CreativeMornings portrait. The public page already offers this image in its press-download links, but has no `og:image`. [Media record](https://kriskrug.co/wp-json/wp/v2/media/12627). Credit: **Photo: Michelle Diamond.** The [site photography manifest](../../../content/source-packs/site-photography-2026/media-manifest.json) records approval for kriskrug.co; the [press-kit manifest](../../../content/source-packs/content-architecture-2026/press-kit/assets/manifest.json) records Kris’s September 2 permission attestation. This is not a new broad licence. Preview desktop/mobile first: a portrait-shaped template hero could become too tall or duplicate the existing heading. A metadata-only solution may be preferable, but requires its own scoped change.
2. **Page 11914, Responsible AI Professional:** potentially useful share-image work, but **no cleared asset selected**. Keep unchanged until the offer/asset choice is made.
3. **Page 2672, Work:** keep featured_media unset. The existing share image is correct; the first in-content BC + AI image still uses an external `.webp` URL that returned 403. The already-packaged site image is a plausible repair candidate, but this audit does not apply it.

## Complete missing-featured review

Each row’s paired desktop/mobile evidence is keyed by page ID in the linked JSON. Empty REST template fields use the default page template except the observed homepage/archive cases.

| ID / page | Judgment | Desktop/mobile treatment and no-change decision |
|---|---|---|
| [1895 · publications](https://kriskrug.co/publications/) | intentional absence | Text-first press archive; desktop columns become a mobile stack; press images start below the lead. Existing OG image. No featured hero. |
| [2315 · home](https://kriskrug.co/home/) | intentional absence | /home/ redirects to the custom homepage with its existing full-width portrait hero. Do not assign media to the redirecting page. |
| [2316 · blog](https://kriskrug.co/blog/) | intentional absence | Writing archive has article thumbnails and its own share image. A page featured image is not the archive renderer. |
| [2389 · news](https://kriskrug.co/news/) | intentionally text-only | Short legacy press-link list on both viewports. Keep text-only; no cleared asset selected. |
| [2409 · testimonials](https://kriskrug.co/testimonials/) | intentionally text-only | Typography, evidence links and metrics lead both viewports. No added portrait or testimonial photograph; no cleared page-specific asset selected. |
| [2418 · contact](https://kriskrug.co/contact/) | intentional absence | Existing Contact portrait and copy sit side by side on desktop and stack on mobile; OG already uses that portrait. Avoid duplicate hero. |
| [2603 · generative-ai-workshop-for-artists-creatives](https://kriskrug.co/generative-ai-workshop-for-artists-creatives/) | needs owner review | Legacy workshop copy and video area; no image/OG. Confirm current offer before selecting a hero; no cleared asset. |
| [2672 · work](https://kriskrug.co/work/) | needs owner review | Text-led portfolio with project cards. Dedicated share image works. First BC + AI card image returned HTTP 403; repair that asset separately, not by setting featured_media. |
| [2808 · subscribe](https://kriskrug.co/subscribe/) | needs owner review | Legacy iframe-only subscription page. External embed is suppressed in audit captures; provider cannot identify the legacy form. No hero recommendation until signup ownership is resolved. |
| [2828 · motleykrug-podcast](https://kriskrug.co/motleykrug-podcast/) | intentional absence | Existing podcast cover sits beside copy on desktop and above it on mobile; OG already uses the cover. Avoid duplicate hero. |
| [2985 · privacy-policy](https://kriskrug.co/privacy-policy/) | intentionally text-only | Policy headings and text on both viewports. No image needed; no cleared asset selected. |
| [3595 · japanese-introduction-page-kaykaysan](https://kriskrug.co/japanese-introduction-page-kaykaysan/) | intentionally text-only | Language introduction with headings and text on both viewports. Keep no added hero; no cleared page-specific asset selected. |
| [3598 · chinese-introduction-kang-jia](https://kriskrug.co/chinese-introduction-kang-jia/) | intentionally text-only | Language introduction with headings and text on both viewports. Keep no added hero; no cleared page-specific asset selected. |
| [3600 · russian-introduction-kristofor-kruglov](https://kriskrug.co/russian-introduction-kristofor-kruglov/) | intentionally text-only | Language introduction with headings and text on both viewports. Keep no added hero; no cleared page-specific asset selected. |
| [3601 · farsi-introduction-khalil-khalifa](https://kriskrug.co/farsi-introduction-khalil-khalifa/) | intentionally text-only | Language introduction with headings and text on both viewports. Keep no added hero; no cleared page-specific asset selected. |
| [3603 · swahili-introduction-kintu-krowfeather-karibu-kwenye-kabila-la-kidijitali-la-dunia-la-kris-krug-kuunganisha-dunia-kupitia-lugha-na-teknolojia](https://kriskrug.co/swahili-introduction-kintu-krowfeather-karibu-kwenye-kabila-la-kidijitali-la-dunia-la-kris-krug-kuunganisha-dunia-kupitia-lugha-na-teknolojia/) | intentionally text-only | Language introduction with headings and text on both viewports. Keep no added hero; no cleared page-specific asset selected. |
| [3606 · hindi-introduction-krishna-vishwanathapriyadhanvanshi](https://kriskrug.co/hindi-introduction-krishna-vishwanathapriyadhanvanshi/) | intentionally text-only | Language introduction with headings and text on both viewports. Keep no added hero; no cleared page-specific asset selected. |
| [3609 · podcast-guesting-page-epk](https://kriskrug.co/podcast-guesting-page-epk/) | candidate | Media/podcast landing page is text-led on both viewports and lacks og:image. Existing press-download portrait 12627 is approved for site use; preview any new template hero before setting it. |
| [3623 · karibu-kwenye-kabila-la-kidijitali-la-dunia-la-kris-krug-kuunganisha-dunia-kupitia-lugha-na-teknolojia-swahili-welcome-page](https://kriskrug.co/karibu-kwenye-kabila-la-kidijitali-la-dunia-la-kris-krug-kuunganisha-dunia-kupitia-lugha-na-teknolojia-swahili-welcome-page/) | intentionally text-only | Language introduction with headings and text on both viewports. Keep no added hero; no cleared page-specific asset selected. |
| [3696 · urdu-language-introduction-kris-krug](https://kriskrug.co/urdu-language-introduction-kris-krug/) | intentionally text-only | Language introduction with headings and text on both viewports. Keep no added hero; no cleared page-specific asset selected. |
| [3948 · the-kk-worldview](https://kriskrug.co/the-kk-worldview/) | intentionally text-only | Personal principles as headings/lists on both viewports. Preserve the text-first treatment; no cleared asset selected. |
| [3969 · sponsor-cyberpunk-chronicles-newsletter](https://kriskrug.co/sponsor-cyberpunk-chronicles-newsletter/) | needs owner review | Older Cyberpunk Chronicles sponsor proposition. Confirm naming/offer before adding artwork; no cleared asset. |
| [3974 · product-review-policy-instructions](https://kriskrug.co/product-review-policy-instructions/) | intentionally text-only | Review policy and instructions; text is the content on both viewports. No cleared asset selected. |
| [6755 · ai-upgrade-community-coaching-w-kris-krug-peter-bittner](https://kriskrug.co/ai-upgrade-community-coaching-w-kris-krug-peter-bittner/) | intentional absence | Text lead followed by existing coaching card/testimonials. The card already supplies OG; mobile retains the same order. Avoid duplicate hero. |
| [7764 · cinematic-podcasts-hollywood-grade-storytelling-meets-generative-ai](https://kriskrug.co/cinematic-podcasts-hollywood-grade-storytelling-meets-generative-ai/) | intentional absence | Text lead with existing cinematic-podcast imagery/video below; mobile stacks the body. Existing image supplies OG; no extra hero. |
| [11887 · glossary](https://kriskrug.co/glossary/) | intentionally text-only | Reference glossary with text/code-style introduction and headings on both viewports. No cleared asset selected; preserve the reference layout. |
| [11914 · responsible-ai-professional](https://kriskrug.co/responsible-ai-professional/) | needs owner review | Certification offer has a text lead and structured explanation on both viewports, without OG image. No approved page-specific asset selected; do not borrow another organization’s branding. |
| [12013 · photography](https://kriskrug.co/photography/) | intentional absence | Large in-content Iggy Pop photograph already leads the portfolio on desktop and mobile. Existing image supplies OG; no duplicate hero. |
| [12315 · vancouver-ai](https://kriskrug.co/vancouver-ai/) | intentional absence | Topic hub leads with text and route cards, followed by existing article imagery below the fold. Mobile stacks the same hierarchy; OG already derives from an article image. No featured hero. |
| [12316 · ai-for-creatives](https://kriskrug.co/ai-for-creatives/) | intentional absence | Topic hub leads with text and route cards, followed by existing article imagery below the fold. Mobile stacks the same hierarchy; OG already derives from an article image. No featured hero. |
| [12317 · ai-events](https://kriskrug.co/ai-events/) | intentional absence | Topic hub leads with text and route cards, followed by existing article imagery below the fold. Mobile stacks the same hierarchy; OG already derives from an article image. No featured hero. |
| [12318 · ai-ethics](https://kriskrug.co/ai-ethics/) | intentional absence | Topic hub leads with text and route cards, followed by existing article imagery below the fold. Mobile stacks the same hierarchy; OG already derives from an article image. No featured hero. |
| [12319 · ai-conversations](https://kriskrug.co/ai-conversations/) | intentional absence | Topic hub leads with text and route cards, followed by existing article imagery below the fold. Mobile stacks the same hierarchy; OG already derives from an article image. No featured hero. |
| [12320 · ai-for-journalists](https://kriskrug.co/ai-for-journalists/) | intentional absence | Topic hub leads with text and route cards, followed by existing article imagery below the fold. Mobile stacks the same hierarchy; OG already derives from an article image. No featured hero. |
| [12321 · ai-tools](https://kriskrug.co/ai-tools/) | intentional absence | Topic hub leads with text and route cards, followed by existing article imagery below the fold. Mobile stacks the same hierarchy; OG already derives from an article image. No featured hero. |
| [12322 · indigenous-ai](https://kriskrug.co/indigenous-ai/) | intentional absence | Topic hub leads with text and route cards, followed by existing article imagery below the fold. Mobile stacks the same hierarchy; OG already derives from an article image. No featured hero. |
| [12625 · sponsor-deck](https://kriskrug.co/sponsor-deck/) | intentional absence | Custom sponsor deck already pairs stage photo with copy on desktop and stacks on mobile. Existing photo supplies OG; no added template hero. |

## Pages that already have featured media

These nine inventory rows remain unchanged; missing-featured capture work does not replace their existing choices.

| Page ID | Slug | Media ID |
|---|---|---|
| 1208 | about | 2682 |
| 1887 | speaking | 2726 |
| 2250 | events | 2726 |
| 2543 | art-island-perspectives-from-a-creative-community | 2601 |
| 2666 | generative-ai-services | 3932 |
| 3899 | reconciliation-indigenous-land-acknowledgement | 3946 |
| 3930 | empowering-events-organizations-for-the-ai-age | 7548 |
| 6770 | ai-upgrade-for-creative-professionals | 7534 |
| 7610 | ai-upgrade-for-modern-media-leaders | 7622 |

## Separate findings

The Publications page (1895) measured 1670 px document width at a 1440 px viewport and 406 px at 390 px. This is a separate overflow investigation, not a reason to assign featured media. The legacy Subscribe iframe (2808) could not be mapped through the current provider form API; no ownership or successful signup claim is made.

## Verification and decision

- Re-enumeration: 46 unique IDs, API total 46, missing-featured count 37; exact ID sets match the report JSON.
- Render evidence: 37 pages × 2 viewports, all capture records successful; viewport screenshots reviewed.
- Source checks: portrait 12627 exists, and the existing site-use/press-kit rights ledgers support the candidate.
- `make verify` passed on the report branch using the existing Python and PHPCS dependencies; docs truth, scoped voice checks and `git diff --check` also passed. These checks do not constitute image-selection approval.

**Approval request for a later apply:** accept **page 3609 → existing media 12627**, with Michelle Diamond’s credit, only after reviewing the exact desktop/mobile preview. No other page/media pair is proposed for a live set.
