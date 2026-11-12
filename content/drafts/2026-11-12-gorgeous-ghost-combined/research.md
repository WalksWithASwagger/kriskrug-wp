# Gorgeous Ghost combined package: source log

Built 2026-11-12 after Kris's ruling on #771 to combine the art-project package (#771) with the making-of draft (#1016). All public checks below were logged-out GETs made on 2026-11-12 between 21:14 and 21:22 UTC. No WordPress write and no authenticated call was made.

The base package `content/drafts/2026-08-12-gorgeous-ghost-art-project/` was read and left untouched. Its #925 pins still matched on 2026-11-12 (`post.md` `301a9baf...1414412`, `post.html` `f1fdc8fd...346f79326b`).

## Claim log

| Claim in the combined draft | Source | Checked (UTC) |
|---|---|---|
| Film site is live; title "A song-long glam space opera" | https://gorgeousghost.com/ returned 200, `<title>Gorgeous Ghost \| A song-long glam space opera</title>` | 2026-11-12 21:14 |
| Runtime 69.42 seconds | Public bundle `https://gorgeousghost.com/assets/index-CLVTWTKC.js`: `film.durationMs: 69420`; last phase ends at 69420 ms | 2026-11-12 21:15 |
| Seven phases from signal forming to credits | Same bundle: phases `signal-forming`, `dead-frequency`, `colour-rising`, `full-glamour`, `the-fall`, `far-out`, `credits` | 2026-11-12 21:15 |
| "At 21 seconds the door gives way" | Same bundle: `colour-rising` starts at 21250 ms; Atlas chapter story "The door gives way" | 2026-11-12 21:15 |
| Peak "runs under three seconds" | Same bundle: `full-glamour` runs 54750 to 57550 ms (2.8 s) | 2026-11-12 21:15 |
| Seven Atlas chapters, 29 moments, each with timestamp, song line and craft note | Same bundle: `atlas.chapters` length 7, `atlas.moments` length 29, moment fields include `startMs`, `lyric`, `craftNote` | 2026-11-12 21:15 |
| Song first, cold open/door/bloom/peak/fall/wink, colour move, hand-finished | Same bundle `atlas.makingNotes`: "Song first", "Four frequencies", "The colour move", "Hand-finished" (Kris selected the footage, cut to the beat, finished with texture, light and sound) | 2026-11-12 21:15 |
| Early holds and narrow blue range; matched gestures; hard tonal contraction after the peak; last look slips back through the receiver | Same bundle, Atlas chapter `story` and `craft` fields for `dead-frequency`, `colour-rising`, `full-glamour`, `the-fall`, `far-out` | 2026-11-12 21:15 |
| Four characters: Ziggy (Kris Krüg), Magenta Rune, Mayumi (Mayumi Rawlings), Kevin (Kevin Friel); roles Starman prophet, Receiver, Space Boss, Static | Same bundle `characters` array (`displayName`, `creditName`, `role`) | 2026-11-12 21:15 |
| Credits: Created by Kris Krüg. The Scallywags: Kris Krüg, Magenta Rune, Mayumi Rawlings, Kevin Friel. Special thanks to Kaoru Yoshihira and Floyo.ai. Made for The BC + AI Film Club Prompt Challenge | Static Credits section on https://gorgeousghost.com/ and bundle `credits` object | 2026-11-12 21:14 |
| Console on Andromeda, channel 04; four-channel tuner; Signal Lab with playable instruments; Relic keepsake; reduce-effects switch; transcript and captions; WebGL field | Homepage text "ANDROMEDA · CH 04", "Reduce effects", "Accessible transcript"; bundle strings "of 4 frequencies locked", "Signal Lab · Playable instruments", "Forge a relic", `no-webgl` mode, captions file `https://gorgeousghost.com/film/gorgeous-ghost.vtt` (200 text/vtt) | 2026-11-12 21:15 |
| Signal field runs on the film's timecode | Bundle: `cues` and `energySamples` keyed by `timeMs` drive bloom, energy and glitch | 2026-11-12 21:15 |
| "Planet Andromeda speaks in lightning" | Bundle `publicCopy.film.metaDescription` | 2026-11-12 21:15 |
| "Civilization is wobbling. The chorus still absolutely slaps." | Paraphrase of bundle `publicCopy.film.ogDescription`; same line already in the #771 package | 2026-11-12 21:15 |
| YouTube cut is public, 69 seconds, by Kris Krüg | https://www.youtube.com/watch?v=9TPcollGnjo returned 200; oEmbed title "Gorgeous Ghost \| Animated Short Film", author Kris Krüg; watch page `isUnlisted: false`, `lengthSeconds: 69`, `datePublished 2026-09-09T14:10:08-07:00` | 2026-11-12 21:15 |
| Second film for the Film Club prompt challenge; first was I AM NOMAD with Suzy Easton | #1016 title ("AI Film Club #2") and body; https://kriskrug.co/2026/07/18/i-am-nomad-ai-film/ (post 12612, 200) names Suzy Easton and the BC + AI Film Club | 2026-11-12 21:16 |
| BC + AI Film Club page | https://bc-ai.ca/communities/film-club (200 after a trailing-slash redirect): "A monthly meetup for people making films with AI" | 2026-11-12 21:16 |
| Ghost Radio has a Gorgeous Ghost station at 100.7 with three tracks | https://ghost.radio.fm/ (200); its public tracks bundle lists station `gorgeous-ghost` at `100.7` with "Gorgeous Ghost (NOW)", "The Dark's Just a Door (Remastered)" and "Gorgeous Ghost" | 2026-11-12 21:17 |
| kriskrug.ai is the Hopecode Garden living lab and lists Gorgeous Ghost | https://kriskrug.ai/ (200); page title names it the Hopecode Garden Living Lab; project list includes Gorgeous Ghost | 2026-11-12 21:19 |
| No One Knows What to Call Us Yet | https://kriskrug.co/2026/07/28/no-one-knows-what-to-call-us-yet/ (post 12638, 200, tagged AI Film Club) | 2026-11-12 21:16 |
| Floyo.ai link | https://www.floyo.ai/ (200; https://floyo.ai/ redirects there) | 2026-11-12 21:16 |
| Network links | https://www.punkrockai.com/, https://www.bothhandsfull.com/, https://kriskrug.co/work/, https://kriskrug.co/tag/ai-film-club/, https://www.suzyeaston.ca/bio/ all 200 | 2026-11-12 21:15 to 21:19 |

## Changes from the sources, and why

- `https://kriskrug.ai/network`, linked by the #771 package as "AI Garden's Signal Atlas", now returns 404. The combined draft links `https://kriskrug.ai/` instead. Open fact for Kris.
- The #771 package hotlinked `https://gorgeousghost.com/og/share.jpg` as the first body image. The combined draft does not, per the lane rule against hotlinking or copying images. The public YouTube embed is the lead visual. The image plan is an open fact.
- The share image's `Last-Modified` header reads `Thu, 12 Nov 2026 16:32:25 GMT`, so the file served today may not be the one reviewed in August.
- #1016 quotes several spoken and sung lines from the film. The combined draft quotes none of them and points readers at the transcript on the film site instead. Whether to add one line back is an open fact.
- #1016 says "about 69 seconds". The site manifest says 69420 ms and YouTube rounds to 69. The draft uses 69.42 seconds.
- #1016 says "Seven phases" and then names six beats. The bundle has seven phases including credits, and six named edit beats in the making notes. The draft keeps both, each in its own place.
- All copy uses straight apostrophes and latin1-safe characters, so a REST write cannot turn a curly quote into `?` (see the latin1 note on the kriskrug.co database).

## Conflicts between sources (not resolved silently)

| Topic | #771 package | #1016 draft | Public source today | Used in combined draft |
|---|---|---|---|---|
| Runtime | 69.42 seconds | "about 69 seconds" | Site manifest 69420 ms; YouTube 69 s | 69.42 seconds (better sourced) |
| Film date | `post_date: 2026-08-12`, dated canonical | "July 2026" from the site release identifier | Site `release.id` is `andromeda-signal-machine-2026-07` (a site build identifier, not a stated film date); YouTube published 2026-09-09; a Film Club meetup ran 2026-09-10 | No month named in the copy; post date left to Kris |
| Credit line | "The Scallywags: Kris Krüg, Magenta Rune, Mayumi Rawlings, and Kevin Friel" | "created by Kris Krüg, with The Scallywags. That is Magenta Rune, Mayumi Rawlings, and Kevin Friel" | Site Credits section: four names including Kris. In-film credits card in the transcript: "The Scallywags. Kevin Friel, Magenta Rune, Mayumi Rawlings. Created by Kris Krüg." | Site Credits section wording, four names, pending Kris's approval |
| Floyo.ai | Special thanks; old `research.md` says the source package named Floyo as part of the video-generation workflow | Special thanks only, no tool claims | Special thanks only | Special thanks only, no tool claim |
| Network map URL | `https://kriskrug.ai/network` | not linked | `/network` is 404; `https://kriskrug.ai/` is 200 | `https://kriskrug.ai/` |
| Prompt word | not named | not named, flagged | Not on gorgeousghost.com or the bc-ai.ca Film Club page | Not named |

## Source map: where each section of the combined draft came from

| Section | From #771 | From #1016 | New from public sources |
|---|---|---|---|
| Opening hook and "film, song, transcript, Atlas" paragraph | Hook line and Andromeda paragraph | | Atlas anchor link |
| Second film for the club, NOMAD with Suzy, "take it personally" rule | | "The challenge" section | NOMAD and Film Club links |
| YouTube embed | | Premiere via YouTube inside the site | Public video metadata |
| The ghost is a band | Scallywags paragraph, fingerprints line | Four characters list, Static as a musician, pull quote on channels | |
| Song first | | "Song first" section | Phase timing |
| The colour move | | "The colour move" section | "Under three seconds" from phase timing |
| Hand-finished | "The human is still on the wheel" paragraph and pull quote | "Hand-finished" section, directing line | Link to No One Knows What to Call Us Yet |
| A song with a body around it | Section title, Ghost Radio paragraph | "The signal machine" section | Ghost Radio station 100.7 |
| The network is the artwork | Whole section | | kriskrug.ai root replaces the 404 |
| Field notes | | Whole section, lightly edited | |
| Project manifest | | Whole section, credits aligned to the site | YouTube watch link |
| Closing invitation | Closing lines | "Push to watch, tune the channels, read the atlas, stay for the wink" | AI Film Club tag link |

## Left out on purpose

- Song lyrics and spoken lines from the film (#1016 opened and closed with them). The transcript is one click away on the film site.
- #1016's "July 2026" month claim and its "about 69 seconds" wording.
- The hotlinked share image from #771.
- "Live now" phrasing from #771, because the post date is still open.
- #1015 (The Sky Smoked Back). Out of scope; its source is a private repo.
