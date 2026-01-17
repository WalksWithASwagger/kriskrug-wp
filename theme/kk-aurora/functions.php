<?php
/**
 * KK Aurora Theme Functions
 *
 * @package KK_Aurora
 * @since 1.0.0
 */

declare(strict_types=1);

namespace KK_Aurora;

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Theme version for cache busting
 */
define('KK_AURORA_VERSION', '1.0.0');

/**
 * Theme setup
 */
function theme_setup(): void {
    // Add theme support
    add_theme_support('wp-block-styles');
    add_theme_support('editor-styles');
    add_theme_support('responsive-embeds');
    add_theme_support('html5', [
        'comment-list',
        'comment-form',
        'search-form',
        'gallery',
        'caption',
        'style',
        'script',
    ]);
    
    // Custom logo
    add_theme_support('custom-logo', [
        'height'      => 100,
        'width'       => 400,
        'flex-height' => true,
        'flex-width'  => true,
    ]);
    
    // Add editor styles
    add_editor_style('style.css');
    add_editor_style('assets/css/editor.css');
}
add_action('after_setup_theme', __NAMESPACE__ . '\\theme_setup');

/**
 * Enqueue frontend styles and scripts
 */
function enqueue_assets(): void {
    // Main stylesheet is automatically enqueued by FSE themes
    
    // Custom animations CSS
    wp_enqueue_style(
        'kk-aurora-animations',
        get_theme_file_uri('assets/css/animations.css'),
        [],
        KK_AURORA_VERSION
    );
    
    // Theme JavaScript (deferred)
    wp_enqueue_script(
        'kk-aurora-theme',
        get_theme_file_uri('assets/js/theme.js'),
        [],
        KK_AURORA_VERSION,
        [
            'strategy' => 'defer',
            'in_footer' => true,
        ]
    );
    
    // GSAP for animations (loaded from CDN for performance)
    wp_enqueue_script(
        'gsap',
        'https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js',
        [],
        '3.12.5',
        [
            'strategy' => 'defer',
            'in_footer' => true,
        ]
    );
    
    // GSAP ScrollTrigger
    wp_enqueue_script(
        'gsap-scrolltrigger',
        'https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js',
        ['gsap'],
        '3.12.5',
        [
            'strategy' => 'defer',
            'in_footer' => true,
        ]
    );
    
    // Aurora animations (depends on GSAP)
    wp_enqueue_script(
        'kk-aurora-animations',
        get_theme_file_uri('assets/js/aurora-animations.js'),
        ['gsap', 'gsap-scrolltrigger'],
        KK_AURORA_VERSION,
        [
            'strategy' => 'defer',
            'in_footer' => true,
        ]
    );
}
add_action('wp_enqueue_scripts', __NAMESPACE__ . '\\enqueue_assets');

/**
 * Enqueue editor assets
 */
function enqueue_editor_assets(): void {
    wp_enqueue_style(
        'kk-aurora-editor',
        get_theme_file_uri('assets/css/editor.css'),
        [],
        KK_AURORA_VERSION
    );
}
add_action('enqueue_block_editor_assets', __NAMESPACE__ . '\\enqueue_editor_assets');

/**
 * Register block patterns
 */
function register_block_patterns(): void {
    // Register pattern category
    register_block_pattern_category(
        'kk-aurora',
        ['label' => __('KK Aurora', 'kk-aurora')]
    );
    
    register_block_pattern_category(
        'kk-aurora-hero',
        ['label' => __('Heroes', 'kk-aurora')]
    );
    
    register_block_pattern_category(
        'kk-aurora-cards',
        ['label' => __('Cards', 'kk-aurora')]
    );
    
    register_block_pattern_category(
        'kk-aurora-cta',
        ['label' => __('Call to Action', 'kk-aurora')]
    );
}
add_action('init', __NAMESPACE__ . '\\register_block_patterns');

/**
 * Register block styles
 */
function register_block_styles(): void {
    // Button styles
    register_block_style('core/button', [
        'name'  => 'aurora-primary',
        'label' => __('Aurora Primary', 'kk-aurora'),
    ]);
    
    register_block_style('core/button', [
        'name'  => 'aurora-ghost',
        'label' => __('Aurora Ghost', 'kk-aurora'),
    ]);
    
    // Group/container styles
    register_block_style('core/group', [
        'name'  => 'aurora-card',
        'label' => __('Aurora Card', 'kk-aurora'),
    ]);
    
    register_block_style('core/group', [
        'name'  => 'aurora-glass',
        'label' => __('Aurora Glass', 'kk-aurora'),
    ]);
    
    // Cover styles
    register_block_style('core/cover', [
        'name'  => 'aurora-hero',
        'label' => __('Aurora Hero', 'kk-aurora'),
    ]);
}
add_action('init', __NAMESPACE__ . '\\register_block_styles');

/**
 * Modify script loading attributes
 */
function script_loader_tag(string $tag, string $handle, string $src): string {
    // Add crossorigin for CDN scripts
    $cdn_scripts = ['gsap', 'gsap-scrolltrigger'];
    
    if (in_array($handle, $cdn_scripts, true)) {
        $tag = str_replace(' src', ' crossorigin="anonymous" src', $tag);
    }
    
    return $tag;
}
add_filter('script_loader_tag', __NAMESPACE__ . '\\script_loader_tag', 10, 3);

/**
 * Add custom body classes
 */
function body_classes(array $classes): array {
    // Add aurora class for styling hooks
    $classes[] = 'aurora-theme';
    
    // Add reduced motion class if preference detected via JS
    // This is also handled in CSS with @media query
    
    return $classes;
}
add_filter('body_class', __NAMESPACE__ . '\\body_classes');

/**
 * Preload critical fonts
 */
function preload_fonts(): void {
    ?>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preload" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap"></noscript>
    <?php
}
add_action('wp_head', __NAMESPACE__ . '\\preload_fonts', 1);

/**
 * Add theme color meta tag
 */
function theme_color_meta(): void {
    ?>
    <meta name="theme-color" content="#0D0D12">
    <meta name="color-scheme" content="dark">
    <?php
}
add_action('wp_head', __NAMESPACE__ . '\\theme_color_meta', 2);

/**
 * Remove WordPress emoji scripts for performance
 */
function disable_emojis(): void {
    remove_action('wp_head', 'print_emoji_detection_script', 7);
    remove_action('admin_print_scripts', 'print_emoji_detection_script');
    remove_action('wp_print_styles', 'print_emoji_styles');
    remove_action('admin_print_styles', 'print_emoji_styles');
    remove_filter('the_content_feed', 'wp_staticize_emoji');
    remove_filter('comment_text_rss', 'wp_staticize_emoji');
    remove_filter('wp_mail', 'wp_staticize_emoji_for_email');
}
add_action('init', __NAMESPACE__ . '\\disable_emojis');
