# Issue #4 — public image-alt inventory refresh

**Captured:** 2026-07-16 (public HTML only; no media PATCH / no `--execute`).
**Tool:** `make public-image-audit` / `scripts/public_image_audit.py --default-urls`

## Summary for humans

- Most `missing-attr` hits on the default URL set are the **Facebook pixel** 1×1 (`facebook.com/tr?...`), not content photos.
- Real content flags on this pass: empty alt on `/home/` crowd-shot JPEG; empty alt on flickr photographer badge page.
- Archive-wide alt debt still needs authenticated inventory + KK-approved writes under #4.

---

- Pages scanned: 8
- Images found: 78
- Missing alt attribute: 8
- Empty non-decorative alt: 2
- Decorative empty alt: 0
- Filename-style alt: 0
- Images with srcset: 33
- Lazy-loaded images: 54
- Broken checked image URLs: 0
- Checked images over 500 KB response size: 0

## Flagged Images

| Page | Media ID | State | Status | Bytes | Alt | Source |
|---|---:|---|---:|---:|---|---|
| https://kriskrug.co/ |  | missing-attr |  |  |  | https://www.facebook.com/tr?id=1720755522050230&ev=PageView&noscript=1 |
| https://kriskrug.co/blog/ |  | missing-attr |  |  |  | https://www.facebook.com/tr?id=1720755522050230&ev=PageView&noscript=1 |
| https://kriskrug.co/home/ |  | missing-attr |  |  |  | https://www.facebook.com/tr?id=1720755522050230&ev=PageView&noscript=1 |
| https://kriskrug.co/home/ |  | empty |  |  |  | https://i0.wp.com/kriskrug.co/wp-content/uploads/2024/09/crowd-shot-vancovuer-ai.jpeg?fit=1024%2C683&ssl=1 |
| https://kriskrug.co/speaking/ |  | missing-attr |  |  |  | https://www.facebook.com/tr?id=1720755522050230&ev=PageView&noscript=1 |
| https://kriskrug.co/generative-ai-services/ |  | missing-attr |  |  |  | https://www.facebook.com/tr?id=1720755522050230&ev=PageView&noscript=1 |
| https://kriskrug.co/contact/ |  | missing-attr |  |  |  | https://www.facebook.com/tr?id=1720755522050230&ev=PageView&noscript=1 |
| https://kriskrug.co/photography/ |  | missing-attr |  |  |  | https://www.facebook.com/tr?id=1720755522050230&ev=PageView&noscript=1 |
| https://kriskrug.co/flickr-photographr-badge/ |  | missing-attr |  |  |  | https://www.facebook.com/tr?id=1720755522050230&ev=PageView&noscript=1 |
| https://kriskrug.co/flickr-photographr-badge/ |  | empty |  |  |  | https://s5102.pcdn.co/wp-content/uploads/2005/06/22181199_f3857c8ca6_b.jpg |
