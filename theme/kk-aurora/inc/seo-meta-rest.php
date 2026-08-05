<?php
/**
 * Register Jetpack SEO meta keys for REST read/write.
 *
 * Jetpack registered `jetpack_seo_html_title` and `advanced_seo_description`
 * with `show_in_rest = true`. When Jetpack was deactivated on kriskrug.co,
 * those keys became unregistered, so WordPress silently drops them on REST
 * write (the POST returns 200 but the value is never stored) and omits them
 * from REST read responses.
 *
 * The theme already reads `jetpack_seo_html_title` via `get_post_meta()` in
 * `inc/seo-title.php` (PHP, never REST), so existing values still render.
 * This file restores the REST round-trip so the Notion → WP connector and
 * `verify_wp_draft.py` can write and read both keys again.
 *
 * See https://github.com/WalksWithASwagger/kriskrug-wp/issues/661
 *
 * @package KK_Aurora
 * @since 1.5.10
 */

declare(strict_types=1);

namespace KK_Aurora;

if (!defined('ABSPATH')) {
    exit;
}

add_action(
    'init',
    function (): void {
        register_post_meta(
            'post',
            'jetpack_seo_html_title',
            [
                'type' => 'string',
                'single' => true,
                'show_in_rest' => true,
                'default' => '',
                'sanitize_callback' => 'sanitize_text_field',
                'auth_callback' => function (): bool {
                    return current_user_can('edit_posts');
                },
            ]
        );

        register_post_meta(
            'post',
            'advanced_seo_description',
            [
                'type' => 'string',
                'single' => true,
                'show_in_rest' => true,
                'default' => '',
                'sanitize_callback' => 'sanitize_textarea_field',
                'auth_callback' => function (): bool {
                    return current_user_can('edit_posts');
                },
            ]
        );
    }
);
