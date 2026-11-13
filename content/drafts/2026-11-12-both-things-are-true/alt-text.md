# Alt text

`post.html` has no `<img>`. The body's only visual is the YouTube embed, which WordPress renders as an iframe titled from oEmbed: `Both Hands Full: What Creatives Actually Need to Know About AI`.

## Featured image (open-facts question 5, ruled 2026-11-12)

The crop QC pick is LaSalle frame 10, media 11831, still **awaiting Kris's crop approval**. It is an existing media item, so the featured image block renders that item's own alt text.

- Live alt text on media 11831 (public REST, 2026-11-13 02:51 UTC): `Kris Krüg presenting Both Hands Full keynote at LaSalle College Vancouver`, then an em dash, then `frame 10`. It carries an em dash and a frame number, and it does not describe the picture.
- Proposed alt text: `Kris Krüg on stage at LaSalle College Vancouver, grinning with a mic in hand, a keynote slide glowing on the screen behind him`
- The proposed line describes what is in the frame, uses no em dash, and stays cp1252-safe (the only character outside ASCII is the precomposed `ü`).

Changing the alt text is a write to an existing media item, so it needs Kris's approval on its own (see `publish-gate.md`). Your Taste Is Your Moat is not affected: an image block keeps the alt text it was inserted with.

If Kris picks frame 20 (media 11833) instead, write alt text from that frame: the wide room shot of the audience facing the stage and the reflection slide.
