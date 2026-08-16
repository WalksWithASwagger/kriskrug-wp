<?php
/**
 * Digital Composting Module
 * Registers Custom Post Type for Transcripts and Topics Taxonomy
 *
 * WHERE THIS RUNS: nowhere, as of 2026-08-15. Dormant.
 *
 * No tracked PHP loads this file. theme/kk-aurora/functions.php requires only
 * inc/seo-title.php and inc/seo-meta-rest.php from the theme's own inc/ dir,
 * and nothing else in the repo requires this repo-root path. So the only way it
 * could be running is out of repo scope, as a Code Snippet or an mu-plugin on
 * kriskrug.co. It is not.
 *
 * Read-only live check, 2026-08-15 against https://kriskrug.co:
 *   - /wp-json/wp/v2/types      -> no `transcript` key
 *   - /wp-json/wp/v2/taxonomies -> no `transcript_topic` key
 *   - /wp-json/wp/v2/transcript -> 404
 *   - /transcript/              -> 404
 * Both registrations below set 'show_in_rest' => true, so they would appear in
 * those two indexes if this code were loaded anywhere on live. It is not.
 *
 * Do not delete without KK approval. Archiving is proposed in issue #746.
 * Re-verify with the four URLs above before acting on this note.
 */
if (!defined('ABSPATH')) {
    exit;
}
function kk_register_transcript_assets() {
    register_post_type('transcript', [
        'labels' => [
            'name' => 'Transcripts',
            'singular_name' => 'Transcript',
            'menu_name' => 'Transcripts',
            'add_new' => 'Add New Transcript',
        ],
        'public' => true,
        'has_archive' => true,
        'show_in_rest' => true,
        'menu_icon' => 'dashicons-media-text',
        'supports' => ['title', 'editor', 'excerpt', 'custom-fields'],
        'taxonomies' => ['transcript_topic'],
    ]);

    register_taxonomy('transcript_topic', 'transcript', [
        'labels' => ['name' => 'Transcript Topics', 'singular_name' => 'Topic'],
        'hierarchical' => true,
        'show_in_rest' => true,
    ]);
}
add_action('init', 'kk_register_transcript_assets');
