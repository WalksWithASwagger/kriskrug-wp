# Issue 36 Public Description Regression

Date: 2026-07-12
Track: B, Aurora theme
Status: repo fix prepared; production deployment not performed

## Production Evidence

The current WordPress sitemap contains 1,641 URLs across posts, pages,
categories, tags, and authors. A deterministic 116-URL sample produced:

- 116 final HTTP `200` responses
- 116 titles present
- 116 valid JSON-LD responses
- 0 standard `<meta name="description">` tags
- Open Graph and Twitter descriptions still present

Direct cache-normal readback confirmed the same missing standard description on
the homepage, `/indigenous-ai/`, legacy posts, and taxonomy archives.

## Diagnosis

Aurora 1.3.37 became the direct Open Graph and Twitter metadata owner. Its
renderer emits `og:description` and `twitter:description`, but it does not emit
the standard search description. Jetpack's stored SEO values remain populated,
so this is a render-owner regression rather than a content backfill problem.

## Prepared Fix

Aurora 1.3.38:

- reads the approved front-page option for `/`
- reads `advanced_seo_description` for singular posts and pages
- preserves the Writing archive's existing description source
- uses a term description only when a retained taxonomy archive has one
- falls back to excerpt/body copy only when a singular page has no stored value
- aligns Open Graph and Twitter descriptions to the same resolved value
- suppresses only Jetpack's duplicate `description` field while leaving its
  `robots` and other SEO fields intact
- leaves the temporary bridge guard intact for rollback compatibility

Author archives and thin taxonomy archives remain policy work in issue #331.

## Deployment Gate

Do not upload the theme from this PR. A separate approved publisher session must:

1. package Aurora 1.3.38 with current Aurora 1.3.37 as the rollback source
2. upload through WordPress admin and confirm the reported version
3. purge PressCACHE
4. verify exactly one standard, Open Graph, and Twitter description on `/`,
   `/blog/`, `/about/`, `/indigenous-ai/`, one current post, and one legacy post
5. confirm no sampled page loses its canonical, title, social image, or robots tag
6. retain the 1.3.37 package until the public crawl and Search Console readback pass

No WordPress write, deployment, cache purge, or Search Console action occurred
while preparing this fix.
