<?php
/**
 * Approved singular search-title handling.
 *
 * @package KK_Aurora
 */

declare(strict_types=1);

namespace KK_Aurora;

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Normalize an approved search title stored in post meta.
 */
function approved_document_title(mixed $value): string {
    if (!is_string($value)) {
        return '';
    }

    return trim(wp_strip_all_tags($value));
}

/**
 * Use the approved per-item search title without changing the public post title.
 */
function filter_pre_get_document_title(string $title): string {
    if (!is_singular()) {
        return $title;
    }

    $post = get_queried_object();
    if (!$post instanceof \WP_Post) {
        return $title;
    }

    $approved_title = approved_document_title(
        get_post_meta($post->ID, 'jetpack_seo_html_title', true)
    );

    return $approved_title !== '' ? $approved_title : $title;
}
add_filter(
    'pre_get_document_title',
    __NAMESPACE__ . '\\filter_pre_get_document_title',
    PHP_INT_MAX
);
