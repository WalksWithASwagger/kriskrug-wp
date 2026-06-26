<?php
/**
 * Title: Marquee Board Hero
 * Slug: kk-aurora/marquee-hero
 * Categories: kk-aurora-hero
 * Keywords: marquee, hero, led, board, coupland, mcluhan
 * Viewport Width: 1400
 * Description: The self-improving "marquee board" hero. Renders the live board from the
 *   generated partial parts/marquee-current.html (source of truth: content/marquee/marquee.json,
 *   compiled by scripts/marquee/build.py). The flip animation is the deferred assets/js/marquee.js.
 *
 * This file is a thin, stable wrapper — the board markup is generated, so promoting a new
 * board (promote.py → build.py) updates the hero with no hand-editing here.
 */

$kk_marquee_partial = __DIR__ . '/../parts/marquee-current.html';
?>
<!-- wp:html -->
<?php
if ( is_readable( $kk_marquee_partial ) ) {
	// Trusted, theme-owned generated markup (pre-rendered board + scoped token styles).
	echo file_get_contents( $kk_marquee_partial ); // phpcs:ignore WordPress.WP.AlternativeFunctions, WordPress.Security.EscapeOutput.OutputNotEscaped
} else {
	// Fallback so the hero is never empty if the partial hasn't been generated yet.
	echo '<section class="kkm" data-skin="led" aria-label="Marquee board"><div class="kkm-frame">'
		. '<p class="kkm-kicker">now showing</p>'
		. '<div class="kkm-board" role="img" aria-label="The Model Is the Message">'
		. '<div class="kkm-row"><div class="kkm-cell" data-final="T">T</div></div>'
		. '</div></div></section>';
}
?>
<!-- /wp:html -->
