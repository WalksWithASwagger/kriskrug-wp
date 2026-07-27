# Proposed alts — worst offenders (#4)

Visual review done on 2026-07-26 from public CDN URLs. Confidence is high for both rows.

## S0 — media `6835`

- **File:** `wp-content/uploads/2024/09/crowd-shot-vancovuer-ai.jpeg`
- **Public empty alt:** `https://kriskrug.co/home/`
- **Also appears on:** blog card for *Zero to One: From Meetup to Movement* (title used as alt fallback because media alt is empty)
- **Current `alt_text`:** empty
- **Proposed:**
  > Crowded Vancouver AI community meetup under blue and magenta lights — attendees watch a speaker in an industrial studio space.
- **Rejected alternatives:** post title only (“Zero to One…”) — fails image description.

## S1 — media `12604`

- **File:** `wp-content/uploads/2005/06/22181199_f3857c8ca6_b.jpg`
- **Public empty alt:** `https://kriskrug.co/flickr-photographr-badge/`
- **Current `alt_text`:** empty
- **Proposed:**
  > Early Flickr Photographer badge graphic for Kris Krug (kk+) with contact lines, portrait, barcode, and handwritten KK+ signature.
- **Note:** Do not paste real phone numbers into alt if KK wants PII out of alt; the graphic includes contact lines visually — this draft describes the *badge genre* without repeating digits. If KK wants stricter: `Vintage Flickr Photographer membership-badge graphic for Kris Krug (kk+), with portrait and signature.`

### PII-safer alternate (preferred if publishing alts broadly)

> Vintage Flickr Photographer membership-badge graphic for Kris Krug (kk+), with portrait and signature.

Use the PII-safer string in the JSON payload below.

## Optional polish (not in PATCH JSON)

| Surface | Current | Suggested |
|---|---|---|
| About `krug-1.jpg` | Portrait of Kris Krug | Close portrait of Kris Krug looking toward camera. |
| Media `11205` | AI for Creative Professionals Kris Krug | Needs visual confirm before replace |
