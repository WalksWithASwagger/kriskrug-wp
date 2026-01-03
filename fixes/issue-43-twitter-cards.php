<?php
/**
 * Issue #43: Add Twitter Card Tags
 *
 * Problem: No Twitter Card meta tags despite active X/Twitter presence
 * Solution: Add comprehensive Twitter Card markup to <head>
 *
 * Add this to your theme's functions.php or create as a plugin
 */

function kriskrug_add_twitter_cards() {
    // Only add on single posts, pages, and homepage
    if ( !is_singular() && !is_front_page() ) {
        return;
    }

    // Get current post/page data
    global $post;

    // Default values
    $twitter_card_type = 'summary_large_image';
    $twitter_title = get_the_title();
    $twitter_description = get_the_excerpt();
    $twitter_image = '';
    $twitter_site = '@YourTwitterHandle'; // UPDATE THIS!
    $twitter_creator = '@YourTwitterHandle'; // UPDATE THIS!

    // Homepage specific
    if ( is_front_page() ) {
        $twitter_title = get_bloginfo( 'name' );
        $twitter_description = get_bloginfo( 'description' );
    }

    // Get featured image
    if ( has_post_thumbnail() ) {
        $image_id = get_post_thumbnail_id();
        $image_url = wp_get_attachment_image_src( $image_id, 'full' );
        if ( $image_url ) {
            $twitter_image = $image_url[0];
        }
    }

    // Fallback to site logo or default image
    if ( empty( $twitter_image ) ) {
        $custom_logo_id = get_theme_mod( 'custom_logo' );
        if ( $custom_logo_id ) {
            $logo_url = wp_get_attachment_image_src( $custom_logo_id, 'full' );
            if ( $logo_url ) {
                $twitter_image = $logo_url[0];
            }
        }
    }

    // Sanitize description
    if ( empty( $twitter_description ) && !empty( $post->post_content ) ) {
        $twitter_description = wp_trim_words( strip_tags( $post->post_content ), 30 );
    }

    // Ensure description isn't too long (200 char max)
    $twitter_description = substr( $twitter_description, 0, 200 );

    // Output Twitter Card meta tags
    ?>
    <!-- Twitter Card Meta Tags (Issue #43) -->
    <meta name="twitter:card" content="<?php echo esc_attr( $twitter_card_type ); ?>">
    <meta name="twitter:site" content="<?php echo esc_attr( $twitter_site ); ?>">
    <meta name="twitter:creator" content="<?php echo esc_attr( $twitter_creator ); ?>">
    <meta name="twitter:title" content="<?php echo esc_attr( $twitter_title ); ?>">
    <meta name="twitter:description" content="<?php echo esc_attr( $twitter_description ); ?>">
    <?php if ( !empty( $twitter_image ) ) : ?>
    <meta name="twitter:image" content="<?php echo esc_url( $twitter_image ); ?>">
    <meta name="twitter:image:alt" content="<?php echo esc_attr( get_post_meta( $image_id, '_wp_attachment_image_alt', true ) ?: $twitter_title ); ?>">
    <?php endif; ?>
    <!-- End Twitter Card Meta Tags -->
    <?php
}
add_action( 'wp_head', 'kriskrug_add_twitter_cards', 5 );

/**
 * Installation Instructions:
 *
 * Option 1: Add to theme's functions.php
 * 1. Go to Appearance → Theme Editor
 * 2. Open functions.php
 * 3. Paste this code at the end (before closing ?>)
 * 4. Save
 *
 * Option 2: Create as plugin
 * 1. Create folder: wp-content/plugins/kriskrug-twitter-cards/
 * 2. Create file: kriskrug-twitter-cards.php
 * 3. Add plugin header:
 *    <?php
 *    /*
 *    Plugin Name: Kris Krug Twitter Cards
 *    Description: Adds Twitter Card meta tags for better social sharing
 *    Version: 1.0
 *    Author: Kris Krug
 *    *\/
 * 4. Paste this code
 * 5. Activate plugin
 *
 * IMPORTANT: Update @YourTwitterHandle with your actual handle!
 *
 * Test: https://cards-dev.twitter.com/validator
 * Paste any URL from your site and verify cards display correctly
 *
 * Status: ✅ Ready to deploy
 */
