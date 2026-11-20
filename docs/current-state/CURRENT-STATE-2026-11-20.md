# Current state on November 20, 2026

The 10:11 a.m. Vancouver `make status-readonly` readback establishes the
baseline for the next drift check. Run it again for the current queue.
The [November 13 snapshot](CURRENT-STATE-2026-11-13.md) records the previous baseline.

- Open PRs: `3` at readback, #1341, #1342 and #1343.
- Open issues: `2` at readback, #1335 and #1336.
- Production publicly reports WordPress `7.0.9`.
- WordPress draft queue: `1` scheduled post, `72` draft posts, `4` draft pages.
- The public Aurora stylesheet and fetched `origin/main` both declare version
  `1.7.3`. Theme file contents require a separate comparison.
- `/projects/` returned HTTP 301 with location `/work/`.

The startup smoke initially flagged the prior 7.0.8 expectation. At 10:13 a.m.
`make wp7-smoke EXPECT_VERSION=7.0.9` passed the homepage, blog, Speaking,
Work, Contact, REST index, sitemap and search checks.

The [roadmap](ROADMAP-2026-11-12.md) holds editorial milestones, booking goals
and decisions. GitHub holds the current [pull requests](https://github.com/WalksWithASwagger/kriskrug-wp/pulls)
and [issues](https://github.com/WalksWithASwagger/kriskrug-wp/issues).
