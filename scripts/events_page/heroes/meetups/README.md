# Meetup hero assets (Wave 3 target dir)

Local hero files for `meetup-editions.yaml` rows land here, referenced as
`repo:scripts/events_page/heroes/meetups/<file>`. Keep each file under 1 MB.
Night photos (Michelle Diamond / Caswell sets) beat promo posters when both exist.
Engine cache belongs in `heroes/_engine_cache/` (gitignored), not here.

2026-08-01 audit (#591): the kk-kb meetup archive has no `photos/` or
`promo-graphics/` for any of the 23 heroless editions. The only months with local
images are the eight editions that already carry heroes (#4, #11, #14, #17, #18,
#28, #30, #31). So no binaries land here yet; rows carry `hero_hint: luma-og`
(14 past editions plus the Sep 30 upcoming row, hero engine fetches the Luma OG
card) or `hero_hint: missing-no-source` (9 editions with no Luma URL and no local
photos: #1, #2, #3, #5, #6, #7, #8, #9, #27).
