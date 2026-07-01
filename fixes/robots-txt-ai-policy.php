<?php
/**
 * Issue #171: Full robots.txt policy for kriskrug.co via WordPress filter.
 *
 * Stance: AI/search discovery and citation — all known AI crawlers are allowed
 * to index public content, with the standard admin/search disallows applied.
 *
 * This snippet supersedes fixes/issue-37-robots-add-sitemaps.php. It handles
 * everything in one filter: canonical sitemap stance, User-agent: * search
 * disallows, and the named AI-crawler group. Do not run both snippets at once.
 *
 * IMPORTANT — this only works if robots.txt is VIRTUAL (served by WordPress).
 * If a physical /robots.txt exists at the Pagely document root, that file wins
 * and this filter never runs. To check:
 *     curl https://kriskrug.co/robots.txt
 * If the physical file is present, edit it directly instead (see fixes/robots.txt).
 *
 * Deploy:   paste into the Code Snippets plugin (run everywhere) OR drop in
 *           wp-content/mu-plugins/kk-robots-ai-policy.php.
 * Verify:   curl https://kriskrug.co/robots.txt | grep -i "ClaudeBot\|Sitemap:"
 * Rollback: deactivate the snippet / delete the mu-plugin file. No data changes.
 * Updated:  2026-07-01 — Jetpack core is inactive, so robots.txt must not
 *           advertise Jetpack-only news/image/video sitemap endpoints.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_filter( 'robots_txt', 'kk_robots_ai_policy', 20, 2 );

/**
 * Apply full robots.txt policy: sitemaps + User-agent: * additions + AI-crawler group.
 *
 * Additive and idempotent: lines already present in the output are skipped.
 *
 * @param string $output The robots.txt content built so far.
 * @param bool   $public Whether the site is set to be indexed (Settings > Reading).
 * @return string
 */
function kk_robots_ai_policy( $output, $public ) {
	if ( ! $public ) {
		return $output;
	}

	$additions = array();

	// ── Sitemaps ────────────────────────────────────────────────────────────
	// WordPress core emits the canonical /sitemap.xml. Do not add Jetpack-only
	// news/image/video sitemap URLs here; they 404 when Jetpack core is inactive.

	// ── User-agent: * search disallows ──────────────────────────────────────
	// WordPress core emits "Disallow: /wp-admin/" already; add the missing
	// search/query-string rules.
	$wildcard_disallows = array(
		'Disallow: /?s=',
		'Disallow: /search/',
	);
	foreach ( $wildcard_disallows as $rule ) {
		if ( false === strpos( $output, $rule ) ) {
			$additions[] = $rule;
		}
	}

	// ── Named AI-crawler group ───────────────────────────────────────────────
	// Explicit group so these crawlers see clear per-agent rules even if they
	// do not inherit from User-agent: *. Stance: allow all public content.
	$ai_group_marker = 'User-agent: OAI-SearchBot';
	if ( false === strpos( $output, $ai_group_marker ) ) {
		$ai_crawlers = array(
			'OAI-SearchBot',
			'GPTBot',
			'ChatGPT-User',
			'ClaudeBot',
			'Claude-User',
			'Claude-SearchBot',
			'PerplexityBot',
			'Perplexity-User',
			'Google-Extended',
			'Applebot-Extended',
			'CCBot',
			'Amazonbot',
			'cohere-ai',
			'Bytespider',
		);

		$additions[] = '';
		$additions[] = '# AI/search crawlers are intentionally allowed for public content.';
		foreach ( $ai_crawlers as $bot ) {
			$additions[] = 'User-agent: ' . $bot;
		}
		$additions[] = 'Disallow: /wp-admin/';
		$additions[] = 'Allow: /wp-admin/admin-ajax.php';
		$additions[] = 'Disallow: /?s=';
		$additions[] = 'Disallow: /search/';
		$additions[] = 'Allow: /';
	}

	if ( empty( $additions ) ) {
		return $output;
	}

	return rtrim( $output ) . "\n" . implode( "\n", $additions ) . "\n";
}
