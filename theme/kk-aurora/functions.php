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
define('KK_AURORA_VERSION', '1.3.18');

/**
 * Theme setup
 */
function theme_setup(): void {
    // Add theme support
    add_theme_support('title-tag');
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
    wp_enqueue_style(
        'kk-aurora-style',
        get_stylesheet_uri(),
        [],
        KK_AURORA_VERSION
    );

    // Refined typography
    wp_enqueue_style(
        'kk-aurora-typography',
        get_theme_file_uri('assets/css/typography-refined.css'),
        [],
        KK_AURORA_VERSION
    );

    // Custom animations CSS
    wp_enqueue_style(
        'kk-aurora-animations',
        get_theme_file_uri('assets/css/animations.css'),
        [],
        KK_AURORA_VERSION
    );

    // Bleeding edge CSS (progressive enhancement)
    wp_enqueue_style(
        'kk-aurora-bleeding-edge',
        get_theme_file_uri('assets/css/bleeding-edge.css'),
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

    // Micro-interactions (no dependencies, vanilla JS)
    wp_enqueue_script(
        'kk-aurora-micro',
        get_theme_file_uri('assets/js/micro-interactions.js'),
        [],
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

    register_block_pattern_category(
        'kk-aurora-article',
        ['label' => __('Article Modules', 'kk-aurora')]
    );

    register_block_pattern_category(
        'kk-aurora-media',
        ['label' => __('Media & Galleries', 'kk-aurora')]
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

    register_block_style('core/paragraph', [
        'name'  => 'lead',
        'label' => __('Lead', 'kk-aurora'),
    ]);

    $quote_styles = [
        'callout'        => __('Callout', 'kk-aurora'),
        'callout-blue'   => __('Callout Blue', 'kk-aurora'),
        'callout-green'  => __('Callout Green', 'kk-aurora'),
        'callout-yellow' => __('Callout Yellow', 'kk-aurora'),
        'callout-red'    => __('Callout Red', 'kk-aurora'),
        'callout-gray'   => __('Callout Gray', 'kk-aurora'),
        'callout-purple' => __('Callout Purple', 'kk-aurora'),
    ];

    foreach ($quote_styles as $name => $label) {
        register_block_style('core/quote', [
            'name'  => $name,
            'label' => $label,
        ]);
    }

    register_block_style('core/group', [
        'name'  => 'bookmark',
        'label' => __('Bookmark', 'kk-aurora'),
    ]);

    register_block_style('core/group', [
        'name'  => 'aurora-source-trail',
        'label' => __('Source Trail', 'kk-aurora'),
    ]);

    register_block_style('core/group', [
        'name'  => 'aurora-article-aside',
        'label' => __('Article Aside', 'kk-aurora'),
    ]);

    register_block_style('core/pullquote', [
        'name'  => 'aurora-pullquote',
        'label' => __('Aurora Pullquote', 'kk-aurora'),
    ]);
}
add_action('init', __NAMESPACE__ . '\\register_block_styles');

/**
 * Keep Aurora's browser titles aligned with the keynote-first positioning.
 *
 * SEO plugins can still override titles, but the theme fallback should not
 * inherit the old "Generative AI Tools & Techniques" site identity.
 *
 * @param array<string, string> $title Document title parts.
 * @return array<string, string>
 */
function filter_document_title_parts(array $title): array {
    $site_descriptor = 'Kris Krug | AI Keynote Speaker & Creative Technologist';

    unset($title['tagline']);

    if (is_front_page()) {
        $title['title'] = $site_descriptor;
        unset($title['site']);
        return $title;
    }

    $title['site'] = $site_descriptor;

    return $title;
}
add_filter('document_title_parts', __NAMESPACE__ . '\\filter_document_title_parts');

function filter_document_title_separator(string $separator): string {
    return '—';
}
add_filter('document_title_separator', __NAMESPACE__ . '\\filter_document_title_separator');

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
    <link rel="preload" href="<?php echo esc_url(get_theme_file_uri('assets/fonts/Inter-Variable.woff2')); ?>" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="<?php echo esc_url(get_theme_file_uri('assets/fonts/ClashDisplay-700.woff2')); ?>" as="font" type="font/woff2" crossorigin>
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

/**
 * Article dek: render the single-post excerpt block ONLY when the author wrote a
 * manual excerpt. Replaces the old hardcoded "proof trail" line — per-post control,
 * blank by default (no auto-generated filler).
 */
function manual_excerpt_dek_only(string $block_content, array $block): string {
    if (($block['blockName'] ?? '') === 'core/post-excerpt'
        && is_singular()
        && ! has_excerpt(get_the_ID())) {
        return '';
    }
    return $block_content;
}
add_filter('render_block', __NAMESPACE__ . '\\manual_excerpt_dek_only', 10, 2);

function enhance_search_block_accessibility(string $block_content, array $block): string {
    if (($block['blockName'] ?? '') !== 'core/search') {
        return $block_content;
    }

    $attrs = isset($block['attrs']) && is_array($block['attrs']) ? $block['attrs'] : [];
    $label = isset($attrs['label']) ? trim(wp_strip_all_tags((string) $attrs['label'])) : '';
    if ($label === '') {
        $label = __('Search kriskrug.co', 'kk-aurora');
    }

    $processor = new \WP_HTML_Tag_Processor($block_content);

    if ($processor->next_tag('form')) {
        $processor->set_attribute('role', 'search');
        $processor->set_attribute('aria-label', $label);
    }

    if ($processor->next_tag('input')) {
        $input_type = strtolower((string) $processor->get_attribute('type'));
        $input_name = (string) $processor->get_attribute('name');

        if ($input_type === 'search' || $input_name === 's') {
            $processor->set_attribute('aria-label', $label);
        }
    }

    if ($processor->next_tag('button')) {
        $processor->set_attribute('aria-label', __('Submit search', 'kk-aurora'));
    }

    return $processor->get_updated_html();
}
add_filter('render_block', __NAMESPACE__ . '\\enhance_search_block_accessibility', 10, 2);

/**
 * Keep the public Writing label on the canonical posts archive URL.
 */
function redirect_writing_archive_alias(): void {
    if (is_admin() || wp_doing_ajax() || wp_doing_cron()) {
        return;
    }

    if (defined('REST_REQUEST') && REST_REQUEST) {
        return;
    }

    $request_uri = isset($_SERVER['REQUEST_URI']) ? sanitize_text_field(wp_unslash((string) $_SERVER['REQUEST_URI'])) : '';
    $request_path = trim((string) wp_parse_url($request_uri, PHP_URL_PATH), '/');
    if ($request_path !== 'writing') {
        return;
    }

    $method = isset($_SERVER['REQUEST_METHOD']) ? strtoupper(sanitize_key(wp_unslash((string) $_SERVER['REQUEST_METHOD']))) : 'GET';
    if (!in_array($method, ['GET', 'HEAD'], true)) {
        return;
    }

    wp_safe_redirect(home_url('/blog/'), 301, 'KK Aurora');
    exit;
}
add_action('template_redirect', __NAMESPACE__ . '\\redirect_writing_archive_alias', 1);

/**
 * Redirect the legacy /projects path to the canonical Work page permalink.
 */
function redirect_legacy_projects_path(): void {
    if (is_admin() || wp_doing_ajax() || wp_doing_cron()) {
        return;
    }

    if (defined('REST_REQUEST') && REST_REQUEST) {
        return;
    }

    $request_uri = isset($_SERVER['REQUEST_URI']) ? sanitize_text_field(wp_unslash((string) $_SERVER['REQUEST_URI'])) : '';
    $request_path = trim((string) wp_parse_url($request_uri, PHP_URL_PATH), '/');
    if ($request_path !== 'projects') {
        return;
    }

    $method = isset($_SERVER['REQUEST_METHOD']) ? strtoupper(sanitize_key(wp_unslash((string) $_SERVER['REQUEST_METHOD']))) : 'GET';
    if (!in_array($method, ['GET', 'HEAD'], true)) {
        return;
    }

    $target_url = home_url('/recent-projects-include/');
    $work_page = get_page_by_path('recent-projects-include');
    if (!$work_page instanceof \WP_Post) {
        $work_page = get_page_by_path('work');
    }

    if ($work_page instanceof \WP_Post) {
        $permalink = get_permalink($work_page);
        if ($permalink !== false) {
            $target_url = $permalink;
        }
    }

    wp_safe_redirect($target_url, 301, 'KK Aurora');
    exit;
}
add_action('template_redirect', __NAMESPACE__ . '\\redirect_legacy_projects_path', 1);

/**
 * Keep single-post related cards from repeating the article being read and
 * prefer same-category posts when they exist.
 *
 * @param array<string, mixed> $query Query args generated by the Query Loop block.
 * @return array<string, mixed>
 */
function exclude_current_post_from_related_query(array $query, \WP_Block $block): array {
    if (!is_singular('post')) {
        return $query;
    }

    $class_name = (string) ($block->parsed_block['attrs']['className'] ?? '');
    $query_id = isset($block->context['queryId']) ? (int) $block->context['queryId'] : 0;
    if (!str_contains($class_name, 'aurora-related-query') && $query_id !== 3) {
        return $query;
    }

    $current_post_id = get_queried_object_id();
    if ($current_post_id <= 0) {
        return $query;
    }

    $excluded = isset($query['post__not_in']) && is_array($query['post__not_in'])
        ? $query['post__not_in']
        : [];
    $excluded[] = $current_post_id;

    $query['post__not_in'] = array_values(array_unique(array_map('absint', $excluded)));

    $category_ids = wp_get_post_categories($current_post_id);
    if ($category_ids === []) {
        return $query;
    }

    $has_same_category = get_posts([
        'category__in'        => $category_ids,
        'fields'              => 'ids',
        'ignore_sticky_posts' => true,
        'no_found_rows'       => true,
        'post__not_in'        => [$current_post_id],
        'post_status'         => 'publish',
        'posts_per_page'      => 1,
    ]);

    if ($has_same_category !== []) {
        $query['category__in'] = $category_ids;
    }

    return $query;
}
add_filter('query_loop_block_query_vars', __NAMESPACE__ . '\\exclude_current_post_from_related_query', 10, 2);

/**
 * Set a real social fallback image on Work when Jetpack emits a blank og:image.
 *
 * @param array<string, string> $tags Existing Open Graph tags.
 * @return array<string, string>
 */
function work_page_open_graph_fallback(array $tags): array {
    if (!is_page(['recent-projects-include', 'work'])) {
        return $tags;
    }

    $image = 'https://i0.wp.com/bc-ai.ca/wp-content/uploads/2026/05/bcai-living-ecosystem.webp?w=1200&ssl=1';

    $tags['og:image'] = $image;
    $tags['og:image:secure_url'] = $image;
    $tags['og:image:width'] = '1200';
    $tags['og:image:height'] = '630';
    $tags['og:image:alt'] = 'BC + AI ecosystem graphic showing community programs and events';
    $tags['twitter:image'] = $image;
    $tags['twitter:image:alt'] = 'BC + AI ecosystem graphic showing community programs and events';

    return $tags;
}
add_filter('jetpack_open_graph_tags', __NAMESPACE__ . '\\work_page_open_graph_fallback');

/**
 * Set archive-specific social metadata for the Writing landing page.
 *
 * @param array<string, string> $tags Existing Open Graph tags.
 * @return array<string, string>
 */
function writing_archive_open_graph_fallback(array $tags): array {
    if (!is_home() || is_front_page()) {
        return $tags;
    }

    $image = 'https://i0.wp.com/kriskrug.co/wp-content/uploads/2026/02/06-mycelial-action-network.png?fit=1200%2C686&ssl=1';
    $description = 'Essays on AI, culture, community, creative practice, consent, taste, and what stays human when the tools get loud.';

    $tags['og:title'] = 'Writing — Kris Krug';
    $tags['og:description'] = $description;
    $tags['og:image'] = $image;
    $tags['og:image:secure_url'] = $image;
    $tags['og:image:width'] = '1200';
    $tags['og:image:height'] = '686';
    $tags['og:image:alt'] = 'Mycelial network artwork representing connected AI-era field notes';
    $tags['twitter:card'] = 'summary_large_image';
    $tags['twitter:title'] = 'Writing — Kris Krug';
    $tags['twitter:description'] = $description;
    $tags['twitter:image'] = $image;
    $tags['twitter:image:alt'] = 'Mycelial network artwork representing connected AI-era field notes';

    return $tags;
}
add_filter('jetpack_open_graph_tags', __NAMESPACE__ . '\\writing_archive_open_graph_fallback');
