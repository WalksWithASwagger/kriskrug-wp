<?php
/**
 * Behavior smoke for theme functions.php, loaded against WordPress stubs.
 *
 * Covers the front-page marquee script enqueue (#1237).
 *
 * @package KK_Aurora
 */

declare(strict_types=1);

define('ABSPATH', __DIR__);

const SMOKE_THEME_URI = 'https://kriskrug.co/wp-content/themes/kk-aurora/';

$GLOBALS['smoke_filters'] = [];
$GLOBALS['smoke_scripts'] = [];
$GLOBALS['smoke_route'] = [];

/**
 * Reset per-request state. Flags left out are false.
 *
 * @param array<string, mixed> $route Conditional-tag flags for the request.
 */
function smoke_request(array $route): void {
    $GLOBALS['smoke_route'] = $route;
    $GLOBALS['smoke_scripts'] = [];
}

function smoke_flag(string $flag): bool {
    return (bool) ($GLOBALS['smoke_route'][$flag] ?? false);
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

    return $post_types === '' || in_array($GLOBALS['smoke_route']['post_type'] ?? '', (array) $post_types, true);
}

function is_category(): bool {
    return smoke_flag('category');
}

function is_tag(): bool {
    return smoke_flag('tag');
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

echo "Aurora functions smoke passed.\n";
