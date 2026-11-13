# Open facts for Kris

**All 14 questions are resolved.** Kris answered the blocking questions 1 to 6 in chat on 2026-11-12, recorded on #959. Questions 7 to 14 took the recommended defaults. Every ruling matched the draft's recommendation, so the body copy did not change. Each ruling sits under its question below. Evidence and check times are in `research.md`.

The one thing still waiting on Kris is his approval of the featured image crop (question 5). That approval is a staging gate in `publish-gate.md`, not an open fact.

## Blocking (ruled 2026-11-12)

### 1. The LaSalle line, word for word (pick one, then confirm by ear)

#959 requires the quote verbatim from the recording. Two machine transcripts disagree by one word, so please listen to **4:05 to 4:23** of the public recording (https://www.youtube.com/watch?v=-c7mgY2aSgM&t=245s) and confirm.

- **a. The public YouTube captions, which the draft uses:** "AI is trained on the stolen work of mankind without consent, and I'm more creative, productive, and more powerful than I've ever been in my whole life. Both of these things are true." *Recommended*, because readers can check it against the video, if it matches what you hear.
- b. The wording in #959, from your private Plaud transcript: the same line with "more creative, more productive, and more powerful".
- c. The published script wording instead of the room wording: "AI is trained on stolen work without consent. And I'm more creative, more productive, and more powerful than I've ever been in my whole life. Both statements are true." If you pick this, the opening sentence stops saying it's what you said four minutes in.

Also confirm you're fine with "mankind" in a pull quote. Verbatim means it stays unless you pick c.

**Ruling: a.** The public YouTube caption wording, verbatim, and "mankind" stays. The pull quote in `post.md` and `post.html` already reads exactly as option a. Re-checked on 2026-11-13 UTC against the committed caption file, cues 00:04:08.879 to 00:04:23.030: every word matches. The only change from the captions is punctuation, joining their two sentences with a comma.

### 2. The photo count (pick one)

Your published pages (the Jan 24 Both Hands Full post, the bothhandsfull.com script and the YouTube description) say roughly 1,800 images in "a major training corpus". In the LaSalle recording you say about 1,900 in the main NVIDIA dataset, then correct to 1,700 or 1,800. #959 repeats the 1,900 and NVIDIA version.

- **a. Keep "roughly 1,800 of my images in a major training corpus", no dataset named, with the evidence-not-proof line after it.** *Recommended.* It matches everything you've already published.
- b. Say 1,900 and name the NVIDIA dataset. Send the source you want cited, and the caveat line stays.

**Ruling: a.** "Roughly 1,800", no dataset named, and the evidence-not-proof line stays. The draft already says exactly that.

### 3. São Paulo (yes/no)

The draft says you took the talk to "the World AI Film Festival Brasil in February" and that "the São Paulo script runs 44 minutes". The Events page lists a Feb 26 keynote. The recording on bothhandsfull.com/talk is labelled "Dress rehearsal", and the script there is marked "Draft for review".

- **Recommended: yes**, if you delivered Both Hands Full in person in São Paulo. If the delivered talk ran differently, give the real runtime and the draft changes "script" to "talk".
- Want the festival name linked? No festival URL was verified, so it's plain text now. Send the link you want.

**Ruling: yes.** Kris delivered the talk in person in São Paulo. Both sentences stay as written. No festival link was sent, so the name stays plain text.

### 4. Post date, slug and canonical (pick one)

- **a. Slug `both-things-are-true`, dated the real publish day, no backdating.** *Recommended.* The draft leaves `post_date` out, so a staged draft floats its date until it is published. Canonical becomes `https://kriskrug.co/<yyyy>/<mm>/<dd>/both-things-are-true/`. `https://kriskrug.co/both-things-are-true/` returned 404 on 2026-11-13 00:47 UTC.
- b. Another slug, such as `both-hands-full-the-talk` (also 404 on the same check).

`both-hands-full` is taken by the live Jan 24 post, so it is not an option.

**Ruling: a.** Slug `both-things-are-true`, dated the real publish day. `post_date` stays out of `post.md`.

### 5. Featured image and rights (pick one, then yes/no on rights)

- **a. Reuse a LaSalle keynote frame already in your WordPress media library**, such as `kk-laSalle-both-hands-full-10-scaled.jpg` or `-20-scaled.jpg`, both 16:9 at 2560x1440 by their public resize URLs and already used in Your Taste Is Your Moat. *Recommended.* No new upload. It still goes through featured-image-forge crop QC and your approval. One catch: the local publisher only sets `featured_media` from images it uploads, so attaching an existing media item is a second, separate write you'd approve after the draft is created.
- b. The LaSalle stage photo on the Events page (`lasalle-college-graduation.jpg`). Dimensions not checked yet.
- c. Upload the bothhandsfull.com share image, which is already in this repo at `content/source-packs/keynotes-2026/assets/both-hands-full-og.png`. It is 1200x630, under the 1600x900 hero master in the crop QC rule, so not recommended.
- d. No featured image. The YouTube embed carries the post and `featured_media` stays unset.

Rights (yes/no): the LaSalle frames on Your Taste Is Your Moat carry no photographer credit. Are they yours to reuse, and is there a credit line you want?

**Ruling: a, and rights yes.** A LaSalle keynote frame already in the media library, Kris's to reuse, crop-checked and shown to him first. He gave no credit line, so none is added. The crop QC compared frame 10 (media 11831) and frame 20 (media 11833) and picked **frame 10, media 11831**. It is **awaiting Kris's crop approval**. Details and the media plan are in `publish-gate.md`.

### 6. WordPress draft 11881 (pick one)

The repo records a thin LaSalle recap as WordPress draft 11881 (slug `both-hands-full-ai-creatives-lasalle-college`), marked CULL in the September 3 triage. Its current state was not checked, because this lane made no WordPress calls. This package does that job better.

- **a. Leave 11881 alone for now. After this post is live, trash 11881 with your explicit approval for that ID, never force-delete.** *Recommended.*
- b. Build this post into 11881 instead of creating a new one. That changes its slug and needs the update path, not the create-only publisher.

**Ruling: a.** Leave 11881 alone until this post is live. Trashing it later needs Kris's explicit approval for that ID, and never `force=true`.

## Defaults (taken 2026-11-12)

### 7. Title (pick one)

- **a. "Both Things Are True".** *Recommended.* It's the stance in four words and the last words of the LaSalle line.
- b. "Both Hands Full, in Writing".
- c. "I Don't Reconcile It. I Hold It."

**Resolved: a.** "Both Things Are True".

### 8. The protester paragraph (yes/no)

The "Stay in the room" section retells the protester story from your published script: back row, camera rolling, took the mic and kept it. She is not named. **Recommended: yes.** It shows bookers the talk can take pushback. If no, the paragraph goes and the section still stands.

**Resolved: yes.** The paragraph stays, and she stays unnamed.

### 9. Other people's stories (yes/no)

The right-hand section describes the people in the talk only as "an animator, a VFX veteran, a writer, a book editor and more" and links the Stories page. Nobody is named or quoted, per #959. **Recommended: yes.**

**Resolved: yes.**

### 10. YouTube embed (yes/no)

Embed the full LaSalle keynote under the opening, with a caption link to 4:05. **Recommended: yes.**

**Resolved: yes.**

### 11. Category and tags (yes/no)

Category `AI for Creatives`, the same as the Jan 24 post. Tags `Both Hands Full`, `Keynotes`, `speaking`, `taste`. All five archives returned 200 on 2026-11-13 00:49 UTC. **Recommended: yes.** Term IDs get resolved on the day of the write.

**Resolved: yes.** Term IDs still resolve on the day of the write.

### 12. The 2027 line (yes/no)

"If your people need this conversation in 2027, send me..." It asks for the room's details and makes no claim about your calendar. **Recommended: yes.**

**Resolved: yes.**

### 13. "I teach AI for a living" (yes/no)

From your February script. Still true for a 2027 reader? **Recommended: yes.**

**Resolved: yes.**

### 14. Runtimes (yes/no)

"The São Paulo script runs 44 minutes" and "the LaSalle recording runs about 80, and the last half hour is Q&A". Both come from the public pages. **Recommended: yes**, subject to question 3.

**Resolved: yes.** Question 3 confirmed São Paulo, so both runtimes stay.
