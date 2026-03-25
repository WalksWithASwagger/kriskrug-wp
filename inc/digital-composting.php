<?php
/**
 * Digital Composting Module
 * Registers Custom Post Type for Transcripts
 */
function kk_register_transcript_cpt() {
    $labels = array(
        'name' => 'Transcripts',
        'singular_name' => 'Transcript',
        'menu_name' => 'Transcripts',
    );
    $args = array(
        'labels' => $labels,
        'public' => true,
        'has_archive' => true,
        'show_in_rest' => true,
        'menu_icon' => 'dashicons-media-text',
        'supports' => array('title', 'editor', 'excerpt', 'custom-fields'),
    );
    register_post_type('transcript', $args);
}
add_action('init', 'kk_register_transcript_cpt');
