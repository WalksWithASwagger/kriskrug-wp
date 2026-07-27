# Placement + newsletter collision

## Live homepage stack (2026-07-26)

1. Masthead / hero
2. Proof strip (stages logos)
3. Working archive
4. Current work (Community / Festival / Tour cards)
5. Services
6. Writing
7. **Newsletter** (`#newsletter`)  -  kicker "Newsletter", H2 "AI and creativity, once a week, no hype.", dek already uses **"Named people, real work, no vaporware."**
8. Footer (includes a second newsletter tile)

#416 owns newsletter copy/CTA/thumbnails. Do not restyle or rewrite that band in this packet.

## Recommended slot for What People Say

**Insert after Services, before Writing.**

```
… → Services → [What People Say] → Writing → Newsletter → Footer
```

Why:

- Services ends on commercial intent; proof immediately after is classic conversion order.
- Writing stays editorial.
- Newsletter keeps the last ask before footer.
- Avoids two "people / network" stories stacked against the email CTA.

## Alternate slot (acceptable)

After Current work, before Services:

```
… → Current work → [What People Say] → Services → Writing → Newsletter
```

Use if KK wants proof before the service cards. Still keep Newsletter last.

## Collision rules (hard)

1. Do not place What People Say **between Writing and Newsletter** or **after Newsletter**. That creates double-ask fatigue (read me / email me / trust me).
2. Do not reuse newsletter vocabulary: Named people, vaporware, subscribe, weekly email, Beehiiv, dispatch, field notes.
3. Do not put an email field or Beehiiv button in the quotes section.
4. Visual: keep quotes on the dark void treatment (existing `.aurora-testimonial-band` background `#030405`). Leave the newsletter's warmer signal gradient alone.
5. Footer already links `/testimonials/`. Section secondary CTA may repeat that; primary CTA should not compete with Subscribe free.

## ID / aria

Suggested when markup lands:

- `id="what-people-say"`
- `aria-labelledby="aurora-testimonials-title"` (reuse) or `kk-people-say-title`
- Do not reuse `id="newsletter"`

## Theme note

Repo `front-page.html` currently has no testimonial markup. Returning the band is a template edit after KK approves copy + quotes. This draft package does not patch the theme.
