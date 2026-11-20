# Current state on November 20, 2026

The 18:39 UTC `make status-readonly` readback establishes the
baseline for the next drift check. Run it again for the current queue.
The [November 13 snapshot](CURRENT-STATE-2026-11-13.md) records the previous baseline.

- Open PRs: `0` at closeout.
- Open issues: `0` at closeout.
- Production publicly reports WordPress `7.0.9`.
- WordPress draft queue: `1` scheduled post, `72` draft posts, `4` draft pages.
- The public Aurora stylesheet and fetched `origin/main` both declare version
  `1.7.3`. Theme file contents require a separate comparison.
- `/projects/` returned HTTP 301 with location `/work/`.

The opening read at 18:11 UTC found three open PRs and two open issues. At closeout the public smoke reported zero failures and zero warnings. All 18 mapped page payloads matched, and a separate read of Publications page 1895 matched its tracked HTML exactly.

The startup smoke initially flagged the prior 7.0.8 expectation. At 18:13 UTC
`make wp7-smoke EXPECT_VERSION=7.0.9` passed the homepage, blog, Speaking,
Work, Contact, REST index, sitemap and search checks.

The [roadmap](ROADMAP-2026-11-12.md) holds editorial milestones, booking goals
and decisions. GitHub holds the current [pull requests](https://github.com/WalksWithASwagger/kriskrug-wp/pulls)
and [issues](https://github.com/WalksWithASwagger/kriskrug-wp/issues).
