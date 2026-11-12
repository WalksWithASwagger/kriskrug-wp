<?php
/**
 * Behavior smoke for theme functions.php, loaded against WordPress stubs.
 *
 * Covers the front-page marquee script enqueue (#1237), route-specific social
 * metadata (#1228), and the /writing and /projects redirects.
 *
 * @package KK_Aurora
 */

declare(strict_types=1);

define('ABSPATH', __DIR__);

const SMOKE_HOME = 'https://kriskrug.co';
const SMOKE_THEME_URI = 'https://kriskrug.co/wp-content/themes/kk-aurora/';
const SMOKE_RETIRED_TAGLINE = 'Empowering Events & Organizations for the AI Age';
const SMOKE_POSTS_PAGE_ID = 4242;
// Live readbacks on 2026-11-12: the /blog/ posts-page description and the
// Jetpack front-page description.
const SMOKE_WRITING_DESCRIPTION = "Read Kris Krüg's field notes on responsible AI, creative technology, community building, Indigenous tech, media, culture, practical workflows, and events.";
const SMOKE_FRONT_PAGE_DESCRIPTION = 'Kris Krüg is an AI keynote speaker and creative technologist building community-first tools, talks, training, and media across BC+AI and Both Hands Full.';

final class WP_Post {
    public function __construct(public int $ID, public string $post_content = '') {
    }
}

final class SmokeRedirect extends RuntimeException {
    public function __construct(public string $location, public int $status) {
        parent::__construct($location);
    }
}

$GLOBALS['smoke_filters'] = [];
$GLOBALS['smoke_scripts'] = [];
$GLOBALS['smoke_route'] = [];
$GLOBALS['smoke_options'] = [
    'page_for_posts'                      => SMOKE_POSTS_PAGE_ID,
    'advanced_seo_front_page_description' => SMOKE_FRONT_PAGE_DESCRIPTION,
];
$GLOBALS['smoke_meta'] = [
    SMOKE_POSTS_PAGE_ID => ['advanced_seo_description' => SMOKE_WRITING_DESCRIPTION],
];
$GLOBALS['smoke_permalinks'] = [];
$GLOBALS['smoke_pages'] = [];

/**
 * Reset per-request state. Flags left out are false.
 *
 * @param array<string, mixed> $route Conditional-tag flags and request data.
 */
function smoke_request(array $route): void {
    $GLOBALS['smoke_route'] = $route;
    $GLOBALS['smoke_scripts'] = [];
}

function smoke_flag(string $flag): bool {
    return (bool) ($GLOBALS['smoke_route'][$flag] ?? false);
}

function smoke_route_value(string $key, mixed $default = ''): mixed {
    return $GLOBALS['smoke_route'][$key] ?? $default;
}

function add_action(string $hook, callable|string $callback, int $priority = 10, int $accepted_args = 1): bool {
    return true;
}

function add_filter(string $hook, callable|string $callback, int $priority = 10, int $accepted_args = 1): bool {
    $GLOBALS['smoke_filters'][] = compact('hook', 'callback', 'priority', 'accepted_args');
    return true;
}

function get_template_directory(): string {
    return dirname(__DIR__);
}

function get_stylesheet_uri(): string {
    return SMOKE_THEME_URI . 'style.css';
}

function get_theme_file_uri(string $file = ''): string {
    return SMOKE_THEME_URI . $file;
}

function wp_enqueue_style(string $handle, string $src = '', array $deps = [], string|bool|null $ver = false, string $media = 'all'): void {
}

function wp_enqueue_script(string $handle, string $src = '', array $deps = [], string|bool|null $ver = false, array|bool $args = []): void {
    $GLOBALS['smoke_scripts'][$handle] = compact('src', 'deps', 'ver', 'args');
}

function is_front_page(): bool {
    return smoke_flag('front_page');
}

function is_home(): bool {
    return smoke_flag('home');
}

function is_singular(string|array $post_types = ''): bool {
    if (!smoke_flag('singular')) {
        return false;
    }

    return $post_types === '' || in_array(smoke_route_value('post_type'), (array) $post_types, true);
}

function is_page(int|string|array $page = ''): bool {
    return false;
}

function is_archive(): bool {
    return smoke_flag('archive');
}

function is_category(): bool {
    return smoke_flag('category');
}

function is_tag(): bool {
    return smoke_flag('tag');
}

function is_tax(): bool {
    return false;
}

function is_date(): bool {
    return smoke_flag('date');
}

function is_author(): bool {
    return smoke_flag('author');
}

function is_search(): bool {
    return smoke_flag('search');
}

function is_feed(): bool {
    return false;
}

function is_admin(): bool {
    return false;
}

function wp_doing_ajax(): bool {
    return false;
}

function wp_doing_cron(): bool {
    return false;
}

function home_url(string $path = ''): string {
    return $path === '' ? SMOKE_HOME : SMOKE_HOME . '/' . ltrim($path, '/');
}

function wp_parse_url(string $url, int $component = -1): mixed {
    return parse_url($url, $component);
}

function get_query_var(string $name, mixed $default = ''): mixed {
    return $name === 'paged' ? smoke_route_value('paged', 0) : $default;
}

/**
 * Mirror core: keep the request path and query, replace any page segment.
 */
function get_pagenum_link(int $pagenum = 1, bool $escape = true): string {
    $request = (string) smoke_route_value('request_url', SMOKE_HOME . '/');
    $path = (string) parse_url($request, PHP_URL_PATH);
    $query = parse_url($request, PHP_URL_QUERY);
    $path = (string) preg_replace('#page/\d+/?$#', '', $path);

    if ($pagenum > 1) {
        $path = rtrim($path, '/') . '/page/' . $pagenum . '/';
    }

    return SMOKE_HOME . $path . (is_string($query) ? '?' . $query : '');
}

function get_search_link(): string {
    return SMOKE_HOME . '/search/' . rawurlencode((string) smoke_route_value('search_query')) . '/';
}

function get_option(string $name, mixed $default = false): mixed {
    return $GLOBALS['smoke_options'][$name] ?? $default;
}

function get_post_meta(int $post_id, string $key = '', bool $single = false): mixed {
    return $GLOBALS['smoke_meta'][$post_id][$key] ?? '';
}

function get_bloginfo(string $show = ''): string {
    return $show === 'description' ? SMOKE_RETIRED_TAGLINE : 'Kris Krug';
}

function get_queried_object(): ?object {
    return smoke_route_value('object', null);
}

function get_the_title(mixed $post = 0): string {
    return (string) smoke_route_value('title');
}

function wp_get_document_title(): string {
    return (string) smoke_route_value('title', 'Kris Krüg');
}

function get_permalink(mixed $post = 0): string|false {
    return $post instanceof WP_Post ? ($GLOBALS['smoke_permalinks'][$post->ID] ?? false) : false;
}

function get_the_excerpt(mixed $post = null): string {
    return (string) smoke_route_value('excerpt');
}

function get_the_post_thumbnail_url(mixed $post = null, string|array $size = 'post-thumbnail'): string|false {
    return false;
}

function has_site_icon(): bool {
    return false;
}

function term_description(): string {
    return (string) smoke_route_value('term_description');
}

function wp_trim_words(string $text, int $num_words = 55): string {
    return implode(' ', array_slice(preg_split('/\s+/', trim($text)) ?: [], 0, $num_words));
}

function wp_strip_all_tags(string $text): string {
    return trim(strip_tags($text));
}

function esc_attr(string $text): string {
    return htmlspecialchars($text, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function get_page_by_path(string $page_path): ?WP_Post {
    return $GLOBALS['smoke_pages'][$page_path] ?? null;
}

function sanitize_text_field(string $text): string {
    return trim($text);
}

function wp_unslash(mixed $value): mixed {
    return $value;
}

function sanitize_key(string $key): string {
    return (string) preg_replace('/[^a-z0-9_\-]/', '', strtolower($key));
}

function wp_safe_redirect(string $location, int $status = 302, string $x_redirect_by = 'WordPress'): bool {
    throw new SmokeRedirect($location, $status);
}

function fail(string $message, mixed $expected, mixed $actual): never {
    fwrite(
        STDERR,
        sprintf("FAIL: %s\nExpected: %s\nActual: %s\n", $message, var_export($expected, true), var_export($actual, true))
    );
    exit(1);
}

function expect_same(mixed $expected, mixed $actual, string $message): void {
    if ($expected !== $actual) {
        fail($message, $expected, $actual);
    }
}

/**
 * Render the social tags for one request and return them by name, decoded.
 *
 * @param array<string, mixed> $route Conditional-tag flags and request data.
 * @return array<string, string>
 */
function smoke_social_meta(array $route): array {
    smoke_request($route);
    ob_start();
    KK_Aurora\render_social_meta_tags();
    $html = (string) ob_get_clean();

    expect_same(
        false,
        str_contains(html_entity_decode($html, ENT_QUOTES | ENT_HTML5, 'UTF-8'), SMOKE_RETIRED_TAGLINE),
        'The retired site tagline must never render.'
    );

    preg_match_all('/<meta (?:property|name)="([^"]+)" content="([^"]*)" \/>/', $html, $matches, PREG_SET_ORDER);
    $tags = [];
    foreach ($matches as $match) {
        $tags[$match[1]] = html_entity_decode($match[2], ENT_QUOTES | ENT_HTML5, 'UTF-8');
    }

    return $tags;
}

/**
 * Run a redirect handler for one request; return [location, status] or null.
 *
 * @return array{0: string, 1: int}|null
 */
function smoke_redirect(callable $handler, string $uri, string $method): ?array {
    $_SERVER['REQUEST_URI'] = $uri;
    $_SERVER['REQUEST_METHOD'] = $method;

    try {
        $handler();
    } catch (SmokeRedirect $redirect) {
        return [$redirect->location, $redirect->status];
    }

    return null;
}

require dirname(__DIR__) . '/functions.php';

// Marquee board script (#1237).

$marquee_filters = array_values(array_filter(
    $GLOBALS['smoke_filters'],
    static fn(array $row): bool => $row['callback'] === 'KK_Aurora\\enqueue_marquee_for_rendered_board'
));
expect_same(1, count($marquee_filters), 'The marquee enqueue must be hooked exactly once.');
expect_same('render_block', $marquee_filters[0]['hook'], 'The marquee enqueue must run on rendered blocks.');

smoke_request(['front_page' => true, 'singular' => true, 'post_type' => 'page']);
KK_Aurora\enqueue_assets();
expect_same(true, isset($GLOBALS['smoke_scripts']['kk-aurora-theme']), 'The base theme script must still load on the front page.');
expect_same(false, isset($GLOBALS['smoke_scripts']['kk-aurora-marquee']), 'The front-page asset pass must not enqueue the marquee script unconditionally.');

$hero_without_board = '<section class="aurora-hero"><h1>Kris Krüg</h1></section>';
expect_same(
    $hero_without_board,
    KK_Aurora\enqueue_marquee_for_rendered_board($hero_without_board),
    'Rendered blocks must pass through unchanged.'
);
expect_same(false, isset($GLOBALS['smoke_scripts']['kk-aurora-marquee']), 'A front page without a marquee board must not load marquee.js.');

ob_start();
include dirname(__DIR__) . '/patterns/marquee-hero.php';
$marquee_pattern = (string) ob_get_clean();
expect_same(true, str_contains($marquee_pattern, 'kkm-board'), 'The marquee pattern must render a board.');

expect_same(
    $marquee_pattern,
    KK_Aurora\enqueue_marquee_for_rendered_board($marquee_pattern),
    'Rendered marquee blocks must pass through unchanged.'
);
$marquee_script = $GLOBALS['smoke_scripts']['kk-aurora-marquee'] ?? null;
expect_same(SMOKE_THEME_URI . 'assets/js/marquee.js', $marquee_script['src'] ?? null, 'A front page rendering the marquee pattern must load marquee.js.');
expect_same(['strategy' => 'defer', 'in_footer' => true], $marquee_script['args'] ?? null, 'marquee.js must stay deferred in the footer.');
expect_same(true, is_readable(dirname(__DIR__) . '/assets/js/marquee.js'), 'The enqueued marquee.js must exist in the theme.');

smoke_request(['singular' => true, 'post_type' => 'marquee_board']);
KK_Aurora\enqueue_marquee_for_rendered_board($marquee_pattern);
expect_same(false, isset($GLOBALS['smoke_scripts']['kk-aurora-marquee']), 'Marquee board singles keep the plugin-owned assets.');

// Route social metadata (#1228).

$GLOBALS['smoke_permalinks'][3930] = SMOKE_HOME . '/';
$GLOBALS['smoke_permalinks'][12801] = SMOKE_HOME . '/2026/11/02/you-cant-rent-a-social-licence/';

$social_cases = [
    'singular post' => [
        'route' => [
            'singular'  => true,
            'post_type' => 'post',
            'object'    => new WP_Post(12801, '<p>Body copy.</p>'),
            'title'     => "You Can't Rent a Social Licence",
            'excerpt'   => 'Why community trust cannot be bought.',
        ],
        'og:url'         => SMOKE_HOME . '/2026/11/02/you-cant-rent-a-social-licence/',
        'og:description' => 'Why community trust cannot be bought.',
    ],
    'category with a description' => [
        'route' => [
            'archive'          => true,
            'category'         => true,
            'request_url'      => SMOKE_HOME . '/category/ai-ethics-philosophy/?utm_source=share',
            'term_description' => "<p>Essays on AI ethics and philosophy.</p>\n",
        ],
        'og:url'         => SMOKE_HOME . '/category/ai-ethics-philosophy/',
        'og:description' => 'Essays on AI ethics and philosophy.',
    ],
    'category page two without a description' => [
        'route' => [
            'archive'     => true,
            'category'    => true,
            'paged'       => 2,
            'request_url' => SMOKE_HOME . '/category/ai-ethics-philosophy/page/2/',
        ],
        'og:url'         => SMOKE_HOME . '/category/ai-ethics-philosophy/page/2/',
        'og:description' => SMOKE_WRITING_DESCRIPTION,
    ],
    'tag' => [
        'route' => [
            'archive'     => true,
            'tag'         => true,
            'request_url' => SMOKE_HOME . '/tag/sxsw-sxswi/',
        ],
        'og:url'         => SMOKE_HOME . '/tag/sxsw-sxswi/',
        'og:description' => SMOKE_WRITING_DESCRIPTION,
    ],
    'date' => [
        'route' => [
            'archive'     => true,
            'date'        => true,
            'request_url' => SMOKE_HOME . '/2026/08/',
        ],
        'og:url'         => SMOKE_HOME . '/2026/08/',
        'og:description' => SMOKE_WRITING_DESCRIPTION,
    ],
    'author' => [
        'route' => [
            'archive'     => true,
            'author'      => true,
            'request_url' => SMOKE_HOME . '/author/kriskrug/',
        ],
        'og:url'         => SMOKE_HOME . '/author/kriskrug/',
        'og:description' => SMOKE_WRITING_DESCRIPTION,
    ],
    'search' => [
        'route' => [
            'search'       => true,
            'search_query' => 'vancouver',
            'request_url'  => SMOKE_HOME . '/?s=vancouver',
        ],
        'og:url'         => SMOKE_HOME . '/search/vancouver/',
        'og:description' => SMOKE_WRITING_DESCRIPTION,
    ],
    'Writing archive' => [
        'route' => [
            'home'        => true,
            'request_url' => SMOKE_HOME . '/blog/?utm_medium=share',
        ],
        'og:url'         => SMOKE_HOME . '/blog/',
        'og:description' => SMOKE_WRITING_DESCRIPTION,
    ],
    'front page' => [
        'route' => [
            'front_page' => true,
            'singular'   => true,
            'post_type'  => 'page',
            'object'     => new WP_Post(3930),
        ],
        'og:url'         => SMOKE_HOME . '/',
        'og:description' => SMOKE_FRONT_PAGE_DESCRIPTION,
    ],
    'not found' => [
        'route'          => ['request_url' => SMOKE_HOME . '/no-such-page/'],
        'og:url'         => SMOKE_HOME . '/',
        'og:description' => KK_Aurora\homepage_meta_description(),
    ],
];

foreach ($social_cases as $label => $case) {
    $tags = smoke_social_meta($case['route']);
    expect_same($case['og:url'], $tags['og:url'] ?? null, "{$label}: og:url must be the route's own URL.");
    expect_same($case['og:description'], $tags['og:description'] ?? null, "{$label}: og:description must fit the route.");
    expect_same($case['og:description'], $tags['twitter:description'] ?? null, "{$label}: twitter:description must mirror og:description.");
}

// Legacy path redirects: GET and HEAD only.

$writing_redirect = 'KK_Aurora\\redirect_writing_archive_alias';
$writing_target = [SMOKE_HOME . '/blog/', 301];
expect_same($writing_target, smoke_redirect($writing_redirect, '/writing', 'GET'), '/writing must redirect to /blog/ on GET.');
expect_same($writing_target, smoke_redirect($writing_redirect, '/writing/?ref=nav', 'HEAD'), '/writing must redirect to /blog/ on HEAD.');
expect_same(null, smoke_redirect($writing_redirect, '/writing/', 'POST'), '/writing must not redirect a POST.');
expect_same(null, smoke_redirect($writing_redirect, '/writing-tools/', 'GET'), 'Only the exact /writing path redirects.');

$projects_redirect = 'KK_Aurora\\redirect_legacy_projects_path';
$GLOBALS['smoke_pages'] = ['recent-projects-include' => new WP_Post(2672)];
$GLOBALS['smoke_permalinks'][2672] = SMOKE_HOME . '/recent-projects-include/';
$projects_target = [SMOKE_HOME . '/recent-projects-include/', 301];
expect_same($projects_target, smoke_redirect($projects_redirect, '/projects/', 'GET'), '/projects must redirect to the Work page on GET.');
expect_same($projects_target, smoke_redirect($projects_redirect, '/projects', 'HEAD'), '/projects must redirect to the Work page on HEAD.');
expect_same(null, smoke_redirect($projects_redirect, '/projects/', 'POST'), '/projects must not redirect a POST.');
expect_same(null, smoke_redirect($projects_redirect, '/projects/ai-garden/', 'GET'), 'Only the exact /projects path redirects.');

$GLOBALS['smoke_pages'] = ['work' => new WP_Post(77)];
$GLOBALS['smoke_permalinks'][77] = SMOKE_HOME . '/work/';
expect_same([SMOKE_HOME . '/work/', 301], smoke_redirect($projects_redirect, '/projects/', 'GET'), '/projects must fall back to the work page slug.');

echo "Aurora functions smoke passed.\n";
