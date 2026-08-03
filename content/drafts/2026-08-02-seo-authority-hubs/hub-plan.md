# Hub plan, one section per term

Issue [#402](https://github.com/WalksWithASwagger/kriskrug-wp/issues/402). Researched 2026-08-02.
Plan only. Read `README.md` first for method and for what rests on inference.

Insertion points reference block indexes from the live rendered body, counted by walking
block-level tags in order (`<p>`, `<h2>`, `<h3>`, `<ul>`, `<ol>`, `<figure>`, `<blockquote>`).
Block 1 is the first block after the featured image.

Every post on the site already ends with an auto-generated `kk-collection-footer` paragraph
that reads "Part of the X collection. See also: Y." Do not duplicate it. Where this plan puts
a link near the end of a post, it goes **before** that footer.

---

## 1 and 2. `most benevolent outcome` and `most benevolent outcome prayer`

**Hub:** https://kriskrug.co/2023/11/04/the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things/ (post 3814)

This one is unusual: the ranking asset is the hub. There is no spiritual or optimism landing
page on the site and I am not proposing to build one. The MBO post is 33 blocks, has the full
prayer text, ends with a named original prayer, and is already the deepest thing on the topic
anywhere on the domain. It just has no inbound links from anything published after 2023.

The post currently has exactly two internal links, both from the auto-footer, and one of them
points at `https://kriskrug.co/category/web-early-blog/`, the 2005 blog archive. That is wrong
and it is the first fix.

**Spokes in:**

| Source | Anchor text | Where |
|---|---|---|
| `/the-kk-worldview/` (page 3948) | there is a prayer I actually say about this | End of the "On Truth and Understanding" list, block 10, as a new paragraph after the `<ul>` |
| `you-cant-drink-data` (11936) | I say a prayer about this most mornings, which is either funny or the whole point | Block 4, the paragraph starting "I was there because they're right about a lot of it", as a trailing sentence |
| `spa-at-the-end-of-time` (11358) | I have my own version of the seance | Block 6, the paragraph about the medium and the astral plane, as a trailing sentence |
| `punk-rock-ai` (11700) | the optimistic version of the same argument | Final paragraph, before the collection footer |

**Spokes out from the hub:**

| Target | Anchor text | Where |
|---|---|---|
| `/the-kk-worldview/` | the rest of my lens, written out plainly | Block 5, after "This prayer was shared with me by a friend this summer", as a trailing sentence |
| `/ai-ethics/` | the less mystical version of this, which is how I actually practice it | Block 21, end of the "Embracing the Digital Future" section, before the "How To Practice MBOs" heading |

**Not a link, but do it:** move post 3814 out of `web-early-blog` and into
`ai-ethics-philosophy`. A 2023 essay about praying for AI outcomes is not an early blog
artifact, and the auto-footer currently sends readers of the best-performing spiritual post
into the 2005 Drupal archive.

---

## 3. `you cant drink data`

**Hub:** https://kriskrug.co/2026/05/23/you-cant-drink-data/ (post 11936)

Strong post, 60+ blocks, first-person, already links out to four internal posts. The gap is
entirely inbound. `/ai-ethics/` is the topic hub and its "Source trail" section links only to
Punk Rock AI and the RAP certification. The post that owns the term is not on its own hub.

Companion post `both-hands-full-at-the-data-center` (11929) already links to it. Leave that
alone.

**Spokes in:**

| Source | Anchor text | Where |
|---|---|---|
| `/ai-ethics/` (page 12318) | You Can't Drink Data | New card in the "Source trail" section, first position, ahead of Punk Rock AI. Card blurb: "A thousand people on Granville Street, and the AI guy standing in the middle of them." |
| `canada-doesnt-need-a-bigger-ai-machine` (12030) | what the water math looks like from street level | First paragraph that raises compute or infrastructure cost, as a trailing sentence |
| `ai-is-not-your-friend` (6144) | two years later I went to the protest and wrote down what the signs said | Final paragraph, before the collection footer |
| `we-trained-ai-on-stolen-work` (11882) | the march where the illustrators showed up as a guild | Near the paragraph about creative labour, as a trailing sentence |

**Spoke out from the hub:** none needed. 11936 already links to BC AI, Punk Rock AI, Both
Hands Full, and Your Taste Is Your Moat.

---

## 4. `modelmayhem.com`

**Hub:** https://kriskrug.co/photography/ (page 12013)
**Ranking asset:** https://kriskrug.co/2006/10/23/kk-on-modelmayhemcom/ (post 1056)

Honest read: this is a navigational query for somebody else's website. Most of the people
typing it want modelmayhem.com, not Kris. It is not worth building content for and I would not
optimize a title for it.

What it is worth: it proves the 2006 and 2007 fashion photography cluster still has crawl
weight, and that cluster currently dead-ends. Post 1056 is 3 blocks long, links out to a
ModelMayhem member profile, and its only internal route is the category archive.

The fix is structural and it serves terms 4, 7, and 10 at once: `/photography/` has zero
internal links. It is a beautiful gallery page that sends every reader to Flickr and none of
them into the 158-post archive.

**Spokes in:**

| Source | Anchor text | Where |
|---|---|---|
| `/photography/` (page 12013) | the whole archive, twenty years of it | Block 23, the closing "This is a fraction of it" paragraph, as a second link next to the existing Flickr link. Target: `/category/photography-visual-storytelling/` |
| `/photography/` (page 12013) | the fashion and model years, 2006 to 2008 | Same block 23, new sentence. Target: post 1056 |
| `to-all-you-wannabe-fashion-photographers` (1222) | how I found those people in the first place | Body, as a trailing sentence. Target: post 1056 |

**Spoke out from the ranking asset:**

| Source | Target | Anchor text | Where |
|---|---|---|---|
| `kk-on-modelmayhemcom` (1056) | `/photography/` | where all of that ended up | Block 2, after "I've met a couple cool peeps already", as a new sentence |

---

## 5. `matt mckenna miami`

**Hub:** https://kriskrug.co/2023/09/22/coffee-community-and-sobriety-matt-mckennas-decade-at-dent/ (post 3183)

The term ranks because Miami is in the body: "opening the doors to Imperial Moto Coffee in
Miami" in block 4. This is a person-entity query and the post is a real interview with a real
person, 18 blocks, sobriety and coffee and DENT. It deserves to be the answer.

The topic hub is `/ai-conversations/` (page 12319) and it does not link to this post.

**Spokes in:**

| Source | Anchor text | Where |
|---|---|---|
| `/ai-conversations/` (page 12319) | Matt McKenna's decade at DENT | New card in the interview list. Card blurb: "Ten years of DENT, ten years sober, and a coffee shop in Miami." |
| `dent-the-future-an-insiders-experiences` (2833) | Matt McKenna, who has been at every single one | The paragraph introducing the DENT community, as an inline link on the name |
| `dent-2019-photo-recap-gallery` (2423) | I sat down with Matt McKenna a few years after this | Intro paragraph, as a trailing sentence |

`the-future-called-i-answered` (3330) already links to post 3183. Leave it.

**Not a link:** post 3330 is also sitting in `web-early-blog`. Same fix as the MBO post.

---

## 6. `vancouver ai community meetup`

**Hub:** https://kriskrug.co/events/ (page 2250) for the query, https://kriskrug.co/vancouver-ai/ (page 12315) for the topic

This is the healthiest cluster of the ten and it still has one clean gap.

Nine meetup recap posts exist going back to the 2023 launch tease. Six were checked for
internal links and all six already point at `/vancouver-ai/`. Good. None of them point at
`/events/`, which is the page carrying the live card: "Wed, Sept 30, Space Centre, Vancouver AI
Community Meetup, Register on Luma."

Somebody searching this term wants to attend the next one. Right now the recap posts route
them to a topic hub instead of a registration link.

**Spokes in, all targeting `/events/`:**

| Source | Anchor text | Where |
|---|---|---|
| `inside-the-innaugural-vancouver-ai-community-meetup` (4495) | we still do this every month, and the next one is on the calendar | Final paragraph, before the collection footer |
| `vancouver-ai-meetup-16` (9197) | the next one | Final paragraph, before the collection footer |
| `vancouver-ai-february-meetup-recap` (8418) | come to the next one | Final paragraph, before the collection footer |
| `august-vancouver-ai-community-meetup-recap` (6815) | the current calendar | Final paragraph, before the collection footer |
| `creativity-in-the-age-of-ai-june-2024-highlights` (6251) | where the next one lands | Final paragraph, before the collection footer |
| `june-vancouver-ai-community-meetup-recap` (5768) | still monthly, still free, still worth the trip | Final paragraph, before the collection footer |
| `2024-vancouver-ai-community-meetups` (4348) | the live calendar, which is the version that stays current | Intro section. This post is a 2023 directory with 60 external links and no date-proofing, so an early route to `/events/` matters more here than anywhere else |

**Spoke out from the topic hub:**

| Source | Target | Anchor text | Where |
|---|---|---|---|
| `/vancouver-ai/` (12315) | `/events/` | the calendar | The "Events and recaps" card, block 11, where "Browse AI events" currently points at `/ai-events/`. Add the calendar as a second link rather than replacing the archive link |

---

## 7. `hardcore photoshoot`

**Hub:** none. Do not build one.
**Ranking asset:** https://kriskrug.co/2006/11/15/hardcore-superstar-photoshoot/ (post 1067)

Read the post. It is a 2006 shoot for a Vancouver boutique legal valet service called Hardcore
Superstar. The impressions are almost certainly people looking for something else entirely,
and the click-through is probably close to zero. I would not write anything for this term, I
would not touch the title, and I would not put it in a hub.

There is still a real bug here worth fixing. Post 1067 is filed under
`vancouver-ai-ecosystem`, so its auto-footer currently reads "Part of the Vancouver AI
Ecosystem collection. See also: The Long Road to Futureproof." A 2006 photoshoot for a valet
company is presented as a Vancouver AI ecosystem artifact. That is a content-model error
visible to every reader and every crawler.

**Action:** recategorize 1067 to `photography-visual-storytelling`. The auto-footer then
rewrites itself to point at the photography archive and the term stops polluting the AI hub.

Same problem, same fix, on `made-in-vancouver-photoshoot` (1063, also in
`vancouver-ai-ecosystem`) and `fashion-photoshoot-for-discollection` (1147, in `ai-creatives`).

---

## 8. `cyber love garden`

**Hub:** https://kriskrug.co/2023/05/30/the-cyber-love-garden-a-crossroads-of-art-and-ai-at-otherworld/ (post 2650)

Genuinely distinctive term, genuinely distinctive post: an Otherworld burn, an XR garden
curated by MOVE37XR, two sessions, Midjourney 5.1 prompts printed in the captions. Nobody else
on the internet owns this phrase. The post is correctly categorized in `ai-creatives` and
correctly footers into `/ai-for-creatives/`.

The topic hub does not return the favour. `/ai-for-creatives/` links to Both Hands Full and
Your Taste Is Your Moat and nothing else.

**Spokes in:**

| Source | Anchor text | Where |
|---|---|---|
| `/ai-for-creatives/` (page 12316) | The Cyber Love Garden | New card in the "Read next" section. Card blurb: "Art, AI, and XR in a burn camp built for it." |
| `exquisite-corpse` (2819) | the garden where we ran this in person | Paragraph describing the Discord experiment, as a trailing sentence |
| `headed-to-burning-man-shambhala-or-coachella` (2661) | what we built at Otherworld | Body, as a trailing sentence |
| `community-art-project-development-process-guide` (3567) | a worked example of all of this | Intro paragraph, as a trailing sentence |

**Not a link:** post 2819 has a dead outbound link, `http://www.kriskrug.com/contact`, which
returns connection failure. Wrong domain, `.com` instead of `.co`. Repoint it at
`https://kriskrug.co/contact/`.

---

## 9. `krug ai`

**Hub:** https://kriskrug.co/ (homepage)

Brand navigational query, and the homepage is already set up for it. The live `<title>` reads
`Kris Krug | AI Keynote Speaker & Creative Technologist`, unaccented Krug included, and the
meta description names BC+AI and Both Hands Full. No title change needed.

Worth knowing before anyone tries: the homepage title and description do **not** come from
page 3930 post-meta. They come from Jetpack `advanced_seo_title_formats.front_page` and
`advanced_seo_front_page_description`. That is outside this lane. Do not go looking for it in
the theme.

The useful move for a brand query is making sure the pages that answer "who is this and what
does he do" are one click from the AI posts that people actually land on.

**Spokes in:**

| Source | Target | Anchor text | Where |
|---|---|---|---|
| `ai-lands-inside-every-profession` (12653) | `/speaking/` | I give a talk about exactly this | Closing section, before the collection footer |
| `canada-doesnt-need-a-bigger-ai-machine` (12030) | `/about/` | why I keep saying this out loud | Closing paragraph, before the collection footer |
| `punk-rock-ai` (11700) | `/glossary/` | plain definitions for the words in here | Early body, first time a term of art appears |

`ai-media-appearances-podcast-guesting` (11879) already links to `/about/`, `/speaking/`,
`/publications/`, `/contact/`, and `/recent-projects-include/`. It is the model. Leave it.

---

## 10. `negotiation equipment for photographers`

**Hub:** https://kriskrug.co/2007/04/10/checklist-of-model-photographer-negotiation-items/ (post 1210)

This is the most interesting one in the list and the only one where the fix is writing, not
linking.

The post is 84 words. It is a 2007 link-blog entry: a title that links out to a ModelMayhem
forum thread, and one paragraph saying every model and photographer arrangement is unique and
problems come from things left unsaid. That is the entire post.

The link is `http://modelmayhem.com/posts.php?thread_id=138265`. It returns **404**. The
Wayback Machine has no snapshot of it. The checklist that this post exists to point at does
not exist anywhere anymore.

So a term is pulling impressions on a page that promises a checklist and delivers a dead link.
That is a bad experience and a wide-open opportunity, because the thing being searched for is
practical and evergreen and Kris genuinely knows it.

**Action, in order:**

1. Rewrite post 1210 to contain the actual checklist, in KK voice, from his own two decades of
   shooting. Usage rights and territory. Duration of licence. Model release, and whether it is
   limited. Nudity and implied nudity, spelled out. Third-party sale and stock. Retouching and
   approval. Who owns the raws. Credit and how it must appear. Trade versus paid and what TFP
   actually costs both sides. Escort policy. Call time, wrap time, overtime. Travel and
   parking. Who supplies wardrobe, hair, makeup. Cancellation and weather. Gear the model
   should not be asked to carry.
2. Remove the dead 404 link. Keep one honest line about where the original lived, because that
   is the true story of this post.
3. Then wire it.

**Spokes in:**

| Source | Anchor text | Where |
|---|---|---|
| `/photography/` (page 12013) | the negotiation checklist I wrote in 2007 and still stand behind | Block 23, closing section, alongside the archive links from term 4 |
| `to-all-you-wannabe-fashion-photographers` (1222) | the checklist version of this rant | Final paragraph, before the collection footer |
| `kk-on-modelmayhemcom` (1056) | the one useful thing I posted over there | Block 2, as a trailing sentence |

**Spoke out:**

| Source | Target | Anchor text | Where |
|---|---|---|---|
| `checklist-of-model-photographer-negotiation-items` (1210) | `/photography/` | twenty years of shooting since I wrote this | Closing line of the rewritten post, before the collection footer |

---

## Category fixes, collected

These are not links. They change what the auto-generated collection footer says on five posts,
which is why they should land before the link inserts.

| Post | ID | Currently in | Should be in | Why |
|---|---|---|---|---|
| Most Benevolent Outcomes Prayer | 3814 | `web-early-blog` | `ai-ethics-philosophy` | 2023 essay on AI and intention, footered into the 2005 archive |
| The Future Called: I Answered | 3330 | `web-early-blog` | `events-reports` | 2023 DENT writeup, same problem |
| Hardcore Superstar Photoshoot | 1067 | `vancouver-ai-ecosystem` | `photography-visual-storytelling` | 2006 photoshoot presented as AI ecosystem content |
| Made in Vancouver Photoshoot | 1063 | `vancouver-ai-ecosystem` | `photography-visual-storytelling` | Same |
| Fashion Photoshoot for Discollection | 1147 | `ai-creatives` | `photography-visual-storytelling` | Same |

## Dead links found while researching

| On post | Dead URL | Status | Fix |
|---|---|---|---|
| 1210 | `http://modelmayhem.com/posts.php?thread_id=138265` | 404, no Wayback snapshot | Remove, replace with the rewritten checklist |
| 2819 | `http://www.kriskrug.com/contact` | 000, connection failure | Repoint to `https://kriskrug.co/contact/` |

## Priority order if only part of this gets done

1. Wire `/photography/` (page 12013). It is a hub with zero internal links and it sits behind
   three of the ten terms.
2. Rewrite post 1210. A ranking page whose only content is a 404 is the worst single state on
   this list.
3. Add `You Can't Drink Data` to `/ai-ethics/`, `Cyber Love Garden` to `/ai-for-creatives/`,
   and `Matt McKenna` to `/ai-conversations/`. Three cards, three hubs, fifteen minutes.
4. The five category fixes.
5. The `/events/` links on the seven meetup posts.
6. Everything else.
