# Open facts for Kris

**All 14 questions are resolved.** Kris answered the blocking questions 1 to 7 in chat on 2026-11-12, recorded on #771. Questions 8 to 14 took the recommended defaults. Each ruling sits under its question below, and the copy in `post.md` and `post.html` follows them. Evidence and check times are in `research.md`.

Kris approved the featured image crop on 2026-11-12 too. The post is scheduled as WordPress post 13003 for 2026-11-19, with the approved image as media 13006 (`publish-gate.md`).

## Blocking (ruled 2026-11-12)

### 1. Post date (pick one)

- **a. The real publish day in the Nov 19 to 30 window, no backdating.** *Recommended.* The combine already makes the #925 pins stale, so keeping 2026-08-12 no longer saves anything. The draft leaves `post_date` out, so a staged draft floats its date until it is published.
- b. Backdate to 2026-09-09, the day the YouTube cut went public.
- c. Backdate to 2026-08-12, the old package date. This puts the post a month before the public YouTube cut.
- d. Another date.

**Ruling: a.** The post is dated the day it is published, inside the Nov 19 to 30 window. `post_date` stays out of `post.md`.

### 2. Slug and canonical (pick one)

- **a. Keep `gorgeous-ghost`. Canonical becomes `https://kriskrug.co/<yyyy>/<mm>/<dd>/gorgeous-ghost/` from the date in question 1.** *Recommended.* It matches the film's name, every earlier slug check, and the existing tag (tag slugs live in their own namespace, so tag 1804 does not collide with a post).
- b. A making-of slug such as `gorgeous-ghost-making-of`.

Either way, the old package also uses `gorgeous-ghost`. Only one of the two may ever be staged. A same-day authenticated all-status slug check (posts and pages) runs before any write.

**Ruling: a.** Slug `gorgeous-ghost`. The canonical takes its date from the publish day.

### 3. Release month (#1016 open fact 2; pick one)

#1016 dated the film "July 2026" from the site's release identifier `andromeda-signal-machine-2026-07`. That identifier names a build of the signal-machine site, not a premiere. YouTube shows the cut published 2026-09-09, and a Film Club meetup ran on 2026-09-10.

- **a. Keep the month out of the post, as the draft does.** *Recommended* unless you know the date.
- b. Say July 2026.
- c. Say September 2026.

**Ruling: a.** No release month anywhere in the copy or the metadata.

### 4. Prompt word (#1016 open fact 1; pick one)

The prompt word is not on gorgeousghost.com or on the bc-ai.ca Film Club page (checked 2026-11-12).

- **a. Leave it unnamed. The draft says "Same club, new prompt".** *Recommended* if the word does not add anything.
- b. Name it. Tell us the word and it goes in that same sentence, the way the NOMAD post names "Retro".

**Ruling: a.** The prompt stays unnamed.

### 5. Tool names (#1016 open fact 3; pick one)

The site credits only special thanks to Kaoru Yoshihira and Floyo.ai. The draft names no generation or edit tools and does not call Floyo a tool.

- **a. Name no tools. Floyo.ai stays a special thank-you.** *Recommended* default.
- b. Name the tools. List the generation and edit tools you want on record and what each one did.

**Ruling: a.** No tool names. Floyo.ai appears only as a special thank-you.

### 6. Credit line (yes/no)

Approve this line, which matches the Credits section on gorgeousghost.com: "Created by Kris Krüg. The Scallywags: Kris Krüg, Magenta Rune, Mayumi Rawlings, Kevin Friel. Special thanks to Kaoru Yoshihira and Floyo.ai. Made for The BC + AI Film Club Prompt Challenge."

- Note the conflict: the in-film credits card lists the Scallywags as Kevin Friel, Magenta Rune and Mayumi Rawlings, with "Created by Kris Krüg" on its own. #1016 used that three-name form. The draft uses the four-name form.
- **Recommended: yes**, with the four-name form. Also confirm Magenta Rune, Mayumi Rawlings, Kevin Friel and Kaoru Yoshihira are fine being named in a kriskrug.co post. Names are unlinked because no personal URLs were verified. Send links if you want them.

**Ruling: the in-film card's form, not the four-name form.** "Created by Kris Krüg" stands on its own. The Scallywags are Kevin Friel, Magenta Rune and Mayumi Rawlings. Then the special thanks to Kaoru Yoshihira and Floyo.ai. "The ghost is a band" and the project manifest now use that form in both `post.md` and `post.html`. Kris's ruling names all four people, so they stay named. They stay unlinked because no links were sent. The manifest keeps "Made for: The BC + AI Film Club Prompt Challenge" as its own line, since the film's title card carries that line too.

### 7. Image, OG plan and rights (pick one, then yes/no on rights)

- **a. Hosted featured image made from your own master film art (a still or the title card), 16:9 at 1600x900 or larger. Run it through featured-image-forge crop QC and approve it before any upload. The YouTube embed stays the lead visual in the body.** *Recommended.* The theme's cards and social previews get a real featured image.
- b. Keep the external `https://gorgeousghost.com/og/share.jpg` as the first body image and OG source, as the #771 package did. No upload, `featured_media` stays unset, and the post depends on another domain. The file is 1200x630, under the hero master size in the crop QC rule, and its `Last-Modified` changed on 2026-11-12, so it may not be the image reviewed in August.
- c. No image beyond the YouTube embed.

Rights (yes/no): gorgeousghost.com says "Created by Kris Krüg" and has no separate image credit or licence line. Is the share image, and any film still you pick, yours to reuse on kriskrug.co? No other permission is documented in the repo.

**Ruling: a, and rights yes.** The film art is Kris's to reuse. A hosted 16:9 featured image from his own film art, crop-checked and shown to him before any upload. The YouTube embed leads the body, as the draft already has it. The crop QC picked the film site's reveal art, the lightning-painted eye in a jeweled star field, as a 1600x900 master. Kris approved that crop on 2026-11-12 after seeing the QC sheet. It was uploaded as media 13006 and the post scheduled for 2026-11-19 (`publish-gate.md`). (The `Last-Modified` worry in option b turned out to be noise. On 2026-11-13 at 02:50 UTC the site returned a `Last-Modified` equal to the request time, and the share image's bytes still match the SHA-256 in the site's own asset manifest.)

## Defaults (taken 2026-11-12)

### 8. YouTube embed (yes/no)

Embed the public YouTube cut (`9TPcollGnjo`, "Gorgeous Ghost | Animated Short Film", public, 69 seconds, published 2026-09-09) near the top of the post. **Recommended: yes.** If no, the draft keeps the links and drops the embed.

**Resolved: yes.** The embed sits under the opening, and it is the lead visual of the body.

### 9. Lyrics (pick one)

#1016 opened and closed with lines from the film. The draft quotes none and sends readers to the transcript on the film site.

- **a. Leave lyrics out.** *Recommended.*
- b. Add one spoken line as a pull quote. You pick the line.

**Resolved: a.** No lyrics.

### 10. Title (pick one)

- **a. "I Made a Gorgeous Ghost".** *Recommended.* It keeps the #771 framing.
- b. "I Made a Gorgeous Ghost: One Locked Song, Four Frequencies and a Colour Move".

**Resolved: a.** "I Made a Gorgeous Ghost".

### 11. Runtime wording (yes/no)

Use "69.42 seconds" everywhere, from the site manifest (69420 ms). YouTube rounds it to 69. **Recommended: yes.** #1016's "about 69 seconds" is dropped.

**Resolved: yes.** "69.42 seconds" throughout.

### 12. Series framing (yes/no)

Call this your second film for the BC + AI Film Club prompt challenge, after I AM NOMAD, as #1016's "AI Film Club #2" title does. **Recommended: yes.**

**Resolved: yes.**

### 13. Network map link (yes/no)

The #771 package linked `https://kriskrug.ai/network` as "AI Garden's Signal Atlas". That path now returns 404. The draft links `https://kriskrug.ai/` and calls it your Hopecode Garden living lab. **Recommended: yes**, unless the network map moved somewhere else.

**Resolved: yes.** The draft links `https://kriskrug.ai/`.

### 14. Retire the 2026-08-12 package (yes/no)

Once this combined package is approved, mark `content/drafts/2026-08-12-gorgeous-ghost-art-project/` as retired in a separate content PR, so two local packages stop claiming the same slug. **Recommended: yes, after approval.** This PR does not touch it, and its #925 pins stay valid until then.

**Resolved: yes.** The PR that pinned this package's hashes did not touch the old package. Kris then ruled on 2026-11-12 to archive it, and it now lives at `content/drafts/archive/2026-08-12-gorgeous-ghost-art-project/` with a row in that folder's README. This package is the only one that claims `gorgeous-ghost`.
