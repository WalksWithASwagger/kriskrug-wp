<?php
/**
 * JSON-LD for single marquee boards: Article linked to the site Person entity, plus a
 * breadcrumb. Mirrors fixes/schema-snippets-deployed.php (Person @id = <site>/#person) so
 * marquee boards carry the same authorship signal as posts. Ships with the plugin so the
 * schema deploys atomically with the CPT.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action( 'wp_head', 'kk_mb_emit_schema', 7 );
function kk_mb_emit_schema() {
	if ( ! is_singular( KK_MB_POST_TYPE ) ) {
		return;
	}
	$person_id = home_url( '/#person' );
	$permalink = get_permalink();

	$article = [
		'@context'         => 'https://schema.org',
		'@type'            => 'Article',
		'headline'         => get_the_title(),
		'description'      => get_the_excerpt(),
		'datePublished'    => get_the_date( 'c' ),
		'dateModified'     => get_the_modified_date( 'c' ),
		'author'           => [ '@id' => $person_id ],
		'publisher'        => [ '@id' => $person_id ],
		'mainEntityOfPage' => [ '@type' => 'WebPage', '@id' => $permalink ],
		'inLanguage'       => 'en-US',
		'articleSection'   => 'Marquee',
	];

	if ( has_post_thumbnail() ) {
		$src = wp_get_attachment_image_src( get_post_thumbnail_id(), 'full' );
		if ( $src ) {
			$article['image'] = [
				'@type'  => 'ImageObject',
				'url'    => $src[0],
				'width'  => $src[1],
				'height' => $src[2],
			];
		}
	}

	$breadcrumb = [
		'@context'        => 'https://schema.org',
		'@type'           => 'BreadcrumbList',
		'itemListElement' => [
			[ '@type' => 'ListItem', 'position' => 1, 'name' => 'Home', 'item' => home_url( '/' ) ],
			[ '@type' => 'ListItem', 'position' => 2, 'name' => 'Marquee', 'item' => home_url( '/marquee/' ) ],
			[ '@type' => 'ListItem', 'position' => 3, 'name' => get_the_title(), 'item' => $permalink ],
		],
	];

	$flags = JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE;
	echo "\n<script type=\"application/ld+json\">" . wp_json_encode( $article, $flags ) . "</script>\n";
	echo '<script type="application/ld+json">' . wp_json_encode( $breadcrumb, $flags ) . "</script>\n";
}
