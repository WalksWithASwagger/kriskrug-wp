<?php
/**
 * Digital Composting Module
 * Registers Custom Post Type for Transcripts and Topics Taxonomy
 */
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
