<?php
/**
 * Title: Photography Showcase
 * Slug: kk-aurora/photo-gallery
 * Categories: kk-aurora-media, kk-aurora
 * Keywords: photography, gallery, portfolio, images, lightbox
 * Viewport Width: 1200
 *
 * Responsive photography grid that positions the photo archive as a credential.
 * Each tile is a core Image block, so it gets the native WordPress lightbox
 * (keyboard-operable click-to-zoom) and lazy-loading for free. Replace the
 * placeholder image sources, alt text, and captions on insertion — every image
 * must have meaningful alt text (WCAG 2.1 AA).
 */

$kk_placeholder = get_theme_file_uri( 'assets/img/kriskrug-wordmark.png' );
$kk_tiles       = array(
	array( 'cat' => 'Climate', 'caption' => 'Environmental expeditions and the people doing the work.' ),
	array( 'cat' => 'Movements', 'caption' => 'On the ground with the communities shaping change.' ),
	array( 'cat' => 'Music', 'caption' => 'Two decades in the pit, with a camera.' ),
	array( 'cat' => 'Sport', 'caption' => 'Motion, grit, and the moment before it breaks.' ),
	array( 'cat' => 'Power', 'caption' => 'Rooms where decisions get made.' ),
	array( 'cat' => 'Film', 'caption' => 'Sets, festivals, and the craft behind the frame.' ),
);
?>
<!-- wp:group {"className":"aurora-photo-section","layout":{"type":"constrained","contentSize":"1200px"}} -->
<div class="wp-block-group aurora-photo-section">
	<!-- wp:paragraph {"className":"aurora-kicker"} -->
	<p class="aurora-kicker">Photography</p>
	<!-- /wp:paragraph -->

	<!-- wp:heading {"level":2} -->
	<h2 class="wp-block-heading">Two decades in the room, with a camera.</h2>
	<!-- /wp:heading -->

	<!-- wp:paragraph {"className":"aurora-photo-lede"} -->
	<p class="aurora-photo-lede">Documentary work across climate, culture, music, and power — 144,000+ exposures and counting. A practiced habit of paying attention, brought to the AI conversation.</p>
	<!-- /wp:paragraph -->

	<!-- wp:group {"className":"aurora-photo-gallery","layout":{"type":"default"}} -->
	<div class="wp-block-group aurora-photo-gallery">
<?php foreach ( $kk_tiles as $kk_tile ) : ?>
		<!-- wp:group {"className":"aurora-photo-tile","layout":{"type":"default"}} -->
		<div class="wp-block-group aurora-photo-tile">
			<!-- wp:paragraph {"className":"aurora-photo-cat"} -->
			<p class="aurora-photo-cat"><?php echo esc_html( $kk_tile['cat'] ); ?></p>
			<!-- /wp:paragraph -->

			<!-- wp:image {"lightbox":{"enabled":true},"sizeSlug":"large","className":"aurora-photo-image"} -->
			<figure class="wp-block-image size-large aurora-photo-image"><img src="<?php echo esc_url( $kk_placeholder ); ?>" alt="<?php echo esc_attr( sprintf( '%s — replace with photograph and descriptive alt text', $kk_tile['cat'] ) ); ?>"/><figcaption class="wp-element-caption"><?php echo esc_html( $kk_tile['caption'] ); ?></figcaption></figure>
			<!-- /wp:image -->
		</div>
		<!-- /wp:group -->
<?php endforeach; ?>
	</div>
	<!-- /wp:group -->

	<!-- wp:paragraph {"className":"aurora-photo-note","fontSize":"sm"} -->
	<p class="aurora-photo-note has-sm-font-size">Replace each placeholder with your own photograph (click-to-zoom lightbox is on by default). The full archive lives on <a href="https://www.flickr.com/photos/kk">Flickr</a>.</p>
	<!-- /wp:paragraph -->
</div>
<!-- /wp:group -->
