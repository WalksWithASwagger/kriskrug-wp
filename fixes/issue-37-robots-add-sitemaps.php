<?php
/**
 * Issue #37: Add the image + video sitemaps to robots.txt for kriskrug.co.
 *
 * Context: the site already serves a healthy Jetpack sitemap index at
 * https://kriskrug.co/sitemap.xml (986 URLs as of 2026-06-07, auto-updating).
 * robots.txt already declares /sitemap.xml and /news-sitemap.xml, but NOT the
 * image or video sitemaps that the index links to, so some crawlers won't
 * discover them. This snippet appends only those two lines.
 *
 * Scope: this is the minimal, additive, sitemap-only patch. It deliberately
 * does NOT touch the AI-crawler stance (GPTBot / ClaudeBot / Google-Extended /
 * etc.) — that's a separate strategic decision documented in
 * fixes/robots-txt-update.txt. Deploy this without having to make that call.
 *
 * IMPORTANT — this only works if robots.txt is VIRTUAL (served by WordPress).
 * If a PHYSICAL /robots.txt file exists at the Pagely document root, that file
 * wins and the `robots_txt` filter never runs. To find out which you have:
 *     curl https://kriskrug.co/robots.txt          # see current content
 *     ls -la <site-root>/robots.txt                # on Pagely SSH; if present, edit directly
 * If physical, just add these two lines to the file by hand instead:
 *     Sitemap: https://kriskrug.co/image-sitemap-index-1.xml
 *     Sitemap: https://kriskrug.co/video-sitemap-1.xml
 *
 * Deploy:   paste into the Code Snippets plugin (run everywhere) OR drop in
 *           wp-content/mu-plugins/kk-robots-sitemaps.php.
 * Verify:   curl https://kriskrug.co/robots.txt  -> image + video sitemaps listed.
 * Rollback: deactivate the snippet / delete the mu-plugin file. No data changes.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_filter( 'robots_txt', 'kk_issue_37_add_sitemaps', 20, 2 );

/**
 * Append the Jetpack image + video sitemaps to the virtual robots.txt.
 *
 * Additive and idempotent: a sitemap already present in the output is skipped,
 * so this is safe to run alongside Jetpack/core's own Sitemap line.
 *
 * @param string $output The robots.txt content built so far.
 * @param bool   $public Whether the site is set to be indexed (Settings > Reading).
 * @return string
 */
function kk_issue_37_add_sitemaps( $output, $public ) {
	// Respect the "Discourage search engines" toggle — don't advertise sitemaps if off.
	if ( ! $public ) {
		return $output;
	}

	$sitemaps = array(
		home_url( '/image-sitemap-index-1.xml' ),
		home_url( '/video-sitemap-1.xml' ),
	);

	$lines = array();
	foreach ( $sitemaps as $sitemap_url ) {
		if ( false === strpos( $output, $sitemap_url ) ) {
			$lines[] = 'Sitemap: ' . esc_url_raw( $sitemap_url );
		}
	}

	if ( empty( $lines ) ) {
		return $output;
	}

	return rtrim( $output ) . "\n" . implode( "\n", $lines ) . "\n";
}
