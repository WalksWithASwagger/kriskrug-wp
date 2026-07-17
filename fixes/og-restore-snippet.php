<?php
/**
 * KK OG Restore — kriskrug.co
 *
 * Temporary production bridge for social link previews while Aurora 1.3.37 is
 * reviewed and deployed. The live Code Snippet must match this file exactly,
 * without the opening PHP tag.
 *
 * Rollback: deactivate the "Open Graph + Twitter Card meta (social link
 * previews)" snippet. Retire it after Aurora 1.3.37 is live and verified.
 */

if (!defined('KK_OG_SNIPPET_ACTIVE')) {
    define('KK_OG_SNIPPET_ACTIVE', true);
}

add_action('wp_head', function (): void {
    if (is_feed()) {
        return;
    }

    $site = get_bloginfo('name');
    $tags = [
        'og:site_name'        => $site,
        'og:title'            => wp_get_document_title(),
        'og:type'             => 'website',
        'og:url'              => home_url('/'),
        'og:description'      => get_bloginfo('description'),
        'twitter:site'        => '@feelmoreplants',
    ];

    if (is_singular()) {
        $post = get_queried_object();
        if ($post instanceof WP_Post) {
            $description = get_the_excerpt($post);
            if ($description === '') {
                $description = wp_trim_words(wp_strip_all_tags($post->post_content), 40);
            }

            $tags['og:title'] = get_the_title($post);
            $tags['og:type'] = is_singular('post') ? 'article' : 'website';
            $tags['og:url'] = get_permalink($post);
            $tags['og:description'] = $description;

            $image = get_the_post_thumbnail_url($post, 'large');
            if (!$image && preg_match('/<img[^>]+src=["\']([^"\']+)/i', $post->post_content, $match)) {
                $image = $match[1];
            }
            if ($image) {
                $tags['og:image'] = $image;
                $tags['og:image:secure_url'] = $image;
            }
        }
    }

    if (empty($tags['og:image']) && has_site_icon()) {
        $tags['og:image'] = get_site_icon_url(512);
        $tags['og:image:secure_url'] = $tags['og:image'];
    }

    if (function_exists('KKAurora\\work_page_open_graph_fallback')) {
        $tags = KKAurora\work_page_open_graph_fallback($tags);
    }
    if (function_exists('KKAurora\\writing_archive_open_graph_fallback')) {
        $tags = KKAurora\writing_archive_open_graph_fallback($tags);
    }
    if (function_exists('KKAurora\\twitter_card_tag_fallbacks')) {
        $tags = KKAurora\twitter_card_tag_fallbacks($tags);
    }

    $tags['og:description'] = mb_substr(wp_strip_all_tags((string) ($tags['og:description'] ?? '')), 0, 300);
    $tags['twitter:card'] = empty($tags['og:image']) ? 'summary' : 'summary_large_image';
    $tags['twitter:title'] = $tags['twitter:title'] ?? $tags['og:title'];
    $tags['twitter:description'] = $tags['twitter:description'] ?? $tags['og:description'];
    if (!empty($tags['og:image'])) {
        $tags['twitter:image'] = $tags['twitter:image'] ?? $tags['og:image'];
    }

    foreach ($tags as $name => $value) {
        if (!is_scalar($value) || $value === '') {
            continue;
        }
        $attribute = str_starts_with($name, 'twitter:') ? 'name' : 'property';
        printf(
            '<meta %s="%s" content="%s" />' . "\n",
            // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- $attribute is a hardcoded literal ('name' or 'property') selected by the ternary above.
            $attribute,
            esc_attr($name),
            esc_attr((string) $value)
        );
    }
}, 5);
