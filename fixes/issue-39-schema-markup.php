<?php
/**
 * Issue #39: Add Schema Markup (Person, Organization, Article)
 *
 * Adds structured data for better SEO and rich snippets
 */

// Person Schema for Kris Krüg
function kriskrug_person_schema() {
    if ( !is_front_page() && !is_page('about') ) {
        return;
    }

    $schema = array(
        '@context' => 'https://schema.org',
        '@type' => 'Person',
        'name' => 'Kris Krüg',
        'alternateName' => 'Kris Krug',
        'description' => 'Executive Director of BC+AI, CTO of Indigenomics.ai, Co-founder of The Upgrade AI',
        'url' => 'https://kriskrug.co',
        'image' => 'https://kriskrug.co/wp-content/uploads/kris-krug-headshot.jpg',
        'sameAs' => array(
            'https://twitter.com/kriskrug',
            'https://www.linkedin.com/in/kriskrug',
            'https://github.com/kriskrug'
        ),
        'jobTitle' => array(
            'Executive Director',
            'Chief Technology Officer',
            'Co-founder'
        ),
        'worksFor' => array(
            array(
                '@type' => 'Organization',
                'name' => 'BC+AI',
                'url' => 'https://bc-ai.ca'
            ),
            array(
                '@type' => 'Organization',
                'name' => 'Indigenomics.ai',
                'url' => 'https://indigenomics.ai'
            ),
            array(
                '@type' => 'Organization',
                'name' => 'The Upgrade AI',
                'url' => 'https://theupgrade.ai'
            )
        ),
        'knowsAbout' => array(
            'Artificial Intelligence',
            'Community Building',
            'Indigenous Technology',
            'Photography',
            'AI Ethics',
            'Technology Strategy'
        ),
        'memberOf' => array(
            '@type' => 'Organization',
            'name' => 'BC+AI'
        )
    );

    echo '<script type="application/ld+json">' . json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT) . '</script>';
}
add_action('wp_head', 'kriskrug_person_schema');

// Article Schema for Blog Posts
function kriskrug_article_schema() {
    if ( !is_single() ) {
        return;
    }

    global $post;

    $schema = array(
        '@context' => 'https://schema.org',
        '@type' => 'BlogPosting',
        'headline' => get_the_title(),
        'description' => get_the_excerpt(),
        'datePublished' => get_the_date('c'),
        'dateModified' => get_the_modified_date('c'),
        'author' => array(
            '@type' => 'Person',
            'name' => 'Kris Krüg',
            'url' => 'https://kriskrug.co/about'
        ),
        'publisher' => array(
            '@type' => 'Person',
            'name' => 'Kris Krüg',
            'logo' => array(
                '@type' => 'ImageObject',
                'url' => 'https://kriskrug.co/wp-content/uploads/logo.png'
            )
        ),
        'mainEntityOfPage' => array(
            '@type' => 'WebPage',
            '@id' => get_permalink()
        )
    );

    // Add image if featured image exists
    if ( has_post_thumbnail() ) {
        $image_id = get_post_thumbnail_id();
        $image_url = wp_get_attachment_image_src( $image_id, 'full' );
        if ( $image_url ) {
            $schema['image'] = array(
                '@type' => 'ImageObject',
                'url' => $image_url[0],
                'width' => $image_url[1],
                'height' => $image_url[2]
            );
        }
    }

    echo '<script type="application/ld+json">' . json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT) . '</script>';
}
add_action('wp_head', 'kriskrug_article_schema');

/**
 * Installation: Add to theme's functions.php
 *
 * This adds:
 * - Person schema for Kris on homepage/about
 * - Article schema on all blog posts
 * - Enables rich snippets in search results
 *
 * Test: https://search.google.com/test/rich-results
 *
 * Status: ✅ Ready to deploy
 */
