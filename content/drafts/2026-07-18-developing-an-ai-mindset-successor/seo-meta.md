# SEO and social metadata

**Status:** Draft-only handoff. Nothing in this file authorizes a WordPress or domain write.

## Page identity

| Field | Proposed value |
| --- | --- |
| Document title | `Developing an AI Mindset Keynote & Workshop | Kris Krüg` |
| Visible H1 | `Developing an AI Mindset` |
| Slug | `developing-an-ai-mindset` |
| Target route | `https://kriskrug.co/speaking/developing-an-ai-mindset/` |
| Canonical URL | `https://kriskrug.co/speaking/developing-an-ai-mindset/` |
| Standard meta description | `Develop an AI mindset with Kris Krüg: a practical keynote or workshop on curiosity, useful experiments, critical thinking, and human judgment.` |
| Meta description length | 142 characters, including spaces and punctuation |
| Open Graph title | `Developing an AI Mindset | Kris Krüg` |
| Open Graph description | `Move from tool panic to useful practice. Kris Krüg's keynote and workshop help people test AI, learn together, and keep human judgment visible.` |
| Twitter title | `Developing an AI Mindset | Kris Krüg` |
| Twitter description | `Move from tool panic to useful practice. Kris Krüg's keynote and workshop help people test AI, learn together, and keep human judgment visible.` |
| Excerpt | `A practical keynote and workshop for people who need shared language, useful AI experiments, and a humane way to keep curiosity, critical thinking, and human judgment in the loop.` |
| Primary CTA | `Book Kris for a keynote or workshop` to `https://kriskrug.co/speaking/` |

## Search intent

**Primary intent:** Find or book Kris Krüg's Developing an AI Mindset keynote or workshop.

**Primary phrase:** `developing an AI mindset`

**Supporting phrases:**

- `AI mindset keynote`
- `AI mindset workshop`
- `AI literacy keynote`
- `practical AI workshop for organizations`
- `human judgment in AI`

Use these phrases only where they read naturally. Do not expand the page with keyword variants that add no value.

## Link plan

| Destination | Placement | Reason |
| --- | --- | --- |
| `https://kriskrug.co/speaking/` | Opening and closing CTA | Keeps the booking action on the canonical Speaking surface. |
| `https://www.punkrockai.com/` | Related lanes | Supports the visible culture-first creative agency copy. |
| `https://www.bothhandsfull.com/` | Related lanes | Supports the visible critique-and-possibility framing. |
| `https://bc-ai.ca/certification/responsible-ai-professional` | Related lanes | Supports the visible governance and deployment-decision copy. |
| `https://innovatewest.tech/wp-content/uploads/2024/04/Developing-an-AI-Mindset.pdf` | Original talk receipt | Public event-hosted deck verifies the 2024 Innovate West talk and framing. |

After the successor is live and verified, a separate human-approved content pass should replace existing old-domain links on the Speaking page and other current editorial surfaces with this canonical route. Backup snapshots and generated evidence should remain unchanged.

## Social image

No image is selected in this packet. A publisher should choose an image with confirmed reuse rights, a stable WordPress-hosted URL, and descriptive alt text before setting `og:image` or `twitter:image`. Do not reuse a temporary Notion asset URL.

## Schema plan

Use one `WebPage` node for the successor and reference the existing sitewide Kris Krüg `Person` entity. Do not create a second `Person` node.

Proposed relationships:

```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "@id": "https://kriskrug.co/speaking/developing-an-ai-mindset/#webpage",
  "url": "https://kriskrug.co/speaking/developing-an-ai-mindset/",
  "name": "Developing an AI Mindset",
  "description": "Develop an AI mindset with Kris Krüg: a practical keynote or workshop on curiosity, useful experiments, critical thinking, and human judgment.",
  "inLanguage": "en-US",
  "isPartOf": {
    "@id": "https://kriskrug.co/#website"
  },
  "author": {
    "@id": "https://kriskrug.co/#person"
  },
  "publisher": {
    "@id": "https://kriskrug.co/#person"
  }
}
```

The active metadata owner may already emit a `WebPage` node. The publisher must inspect the logged-out preview and live output, then merge these fields into the existing node instead of adding a duplicate.

Do not add the following types in this pass:

- `Event`: the page does not advertise one scheduled event with a verified date, place, and offer.
- `Course`: the page is an evergreen keynote or workshop offer, not a formal course with the visible fields required for course markup.
- `FAQPage`: the draft contains no visible question-and-answer section.
- `Service`: the simpler `WebPage` plus existing `Person` relationship matches the visible page and avoids inventing offer details.

If visible copy changes before publication, re-evaluate the schema against that copy rather than treating this draft as permanent.
