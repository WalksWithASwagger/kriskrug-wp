# Open facts for Kris

Questions only Kris can answer before this combined package can be pinned and staged. Each one is a yes/no or a pick-one, with a recommendation. Evidence and check times are in `research.md`. Nothing here has been decided for him.

Questions 1 to 7 block staging. Questions 8 to 14 have a safe default already in the draft, so a silent "go with the recommendation" is enough.

## Blocking

### 1. Post date (pick one)

- **a. The real publish day in the Nov 19 to 30 window, no backdating.** *Recommended.* The combine already makes the #925 pins stale, so keeping 2026-08-12 no longer saves anything. The draft leaves `post_date` out, so a staged draft floats its date until it is published.
- b. Backdate to 2026-09-09, the day the YouTube cut went public.
- c. Backdate to 2026-08-12, the old package date. This puts the post a month before the public YouTube cut.
- d. Another date.

### 2. Slug and canonical (pick one)

- **a. Keep `gorgeous-ghost`. Canonical becomes `https://kriskrug.co/<yyyy>/<mm>/<dd>/gorgeous-ghost/` from the date in question 1.** *Recommended.* It matches the film's name, every earlier slug check, and the existing tag (tag slugs live in their own namespace, so tag 1804 does not collide with a post).
- b. A making-of slug such as `gorgeous-ghost-making-of`.

Either way, the old package also uses `gorgeous-ghost`. Only one of the two may ever be staged. A same-day authenticated all-status slug check (posts and pages) runs before any write.

### 3. Release month (#1016 open fact 2; pick one)

#1016 dated the film "July 2026" from the site's release identifier `andromeda-signal-machine-2026-07`. That identifier names a build of the signal-machine site, not a premiere. YouTube shows the cut published 2026-09-09, and a Film Club meetup ran on 2026-09-10.

- **a. Keep the month out of the post, as the draft does.** *Recommended* unless you know the date.
- b. Say July 2026.
- c. Say September 2026.

### 4. Prompt word (#1016 open fact 1; pick one)

The prompt word is not on gorgeousghost.com or on the bc-ai.ca Film Club page (checked 2026-11-12).

- **a. Leave it unnamed. The draft says "Same club, new prompt".** *Recommended* if the word does not add anything.
- b. Name it. Tell us the word and it goes in that same sentence, the way the NOMAD post names "Retro".

### 5. Tool names (#1016 open fact 3; pick one)

The site credits only special thanks to Kaoru Yoshihira and Floyo.ai. The draft names no generation or edit tools and does not call Floyo a tool.

- **a. Name no tools. Floyo.ai stays a special thank-you.** *Recommended* default.
- b. Name the tools. List the generation and edit tools you want on record and what each one did.

### 6. Credit line (yes/no)

Approve this line, which matches the Credits section on gorgeousghost.com: "Created by Kris Krüg. The Scallywags: Kris Krüg, Magenta Rune, Mayumi Rawlings, Kevin Friel. Special thanks to Kaoru Yoshihira and Floyo.ai. Made for The BC + AI Film Club Prompt Challenge."

- Note the conflict: the in-film credits card lists the Scallywags as Kevin Friel, Magenta Rune and Mayumi Rawlings, with "Created by Kris Krüg" on its own. #1016 used that three-name form. The draft uses the four-name form.
- **Recommended: yes**, with the four-name form. Also confirm Magenta Rune, Mayumi Rawlings, Kevin Friel and Kaoru Yoshihira are fine being named in a kriskrug.co post. Names are unlinked because no personal URLs were verified. Send links if you want them.

### 7. Image, OG plan and rights (pick one, then yes/no on rights)

- **a. Hosted featured image made from your own master film art (a still or the title card), 16:9 at 1600x900 or larger. Run it through featured-image-forge crop QC and approve it before any upload. The YouTube embed stays the lead visual in the body.** *Recommended.* The theme's cards and social previews get a real featured image.
- b. Keep the external `https://gorgeousghost.com/og/share.jpg` as the first body image and OG source, as the #771 package did. No upload, `featured_media` stays unset, and the post depends on another domain. The file is 1200x630, under the hero master size in the crop QC rule, and its `Last-Modified` changed on 2026-11-12, so it may not be the image reviewed in August.
- c. No image beyond the YouTube embed.

Rights (yes/no): gorgeousghost.com says "Created by Kris Krüg" and has no separate image credit or licence line. Is the share image, and any film still you pick, yours to reuse on kriskrug.co? No other permission is documented in the repo.

## Defaults already in the draft

### 8. YouTube embed (yes/no)

Embed the public YouTube cut (`9TPcollGnjo`, "Gorgeous Ghost | Animated Short Film", public, 69 seconds, published 2026-09-09) near the top of the post. **Recommended: yes.** If no, the draft keeps the links and drops the embed.

### 9. Lyrics (pick one)

#1016 opened and closed with lines from the film. The draft quotes none and sends readers to the transcript on the film site.

- **a. Leave lyrics out.** *Recommended.*
- b. Add one spoken line as a pull quote. You pick the line.

### 10. Title (pick one)

- **a. "I Made a Gorgeous Ghost".** *Recommended.* It keeps the #771 framing.
- b. "I Made a Gorgeous Ghost: One Locked Song, Four Frequencies and a Colour Move".

### 11. Runtime wording (yes/no)

Use "69.42 seconds" everywhere, from the site manifest (69420 ms). YouTube rounds it to 69. **Recommended: yes.** #1016's "about 69 seconds" is dropped.

### 12. Series framing (yes/no)

Call this your second film for the BC + AI Film Club prompt challenge, after I AM NOMAD, as #1016's "AI Film Club #2" title does. **Recommended: yes.**

### 13. Network map link (yes/no)

The #771 package linked `https://kriskrug.ai/network` as "AI Garden's Signal Atlas". That path now returns 404. The draft links `https://kriskrug.ai/` and calls it your Hopecode Garden living lab. **Recommended: yes**, unless the network map moved somewhere else.

### 14. Retire the 2026-08-12 package (yes/no)

Once this combined package is approved, mark `content/drafts/2026-08-12-gorgeous-ghost-art-project/` as retired in a separate content PR, so two local packages stop claiming the same slug. **Recommended: yes, after approval.** This PR does not touch it, and its #925 pins stay valid until then.
