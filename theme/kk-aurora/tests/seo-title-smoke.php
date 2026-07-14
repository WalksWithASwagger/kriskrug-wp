<?php
/**
 * Behavior smoke for Aurora's approved singular search titles.
 *
 * @package KK_Aurora
 */

declare(strict_types=1);

define('ABSPATH', __DIR__);

final class WP_Post {
    public function __construct(public int $ID) {
    }
}

$GLOBALS['aurora_smoke_filters'] = [];
$GLOBALS['aurora_smoke_is_singular'] = true;
$GLOBALS['aurora_smoke_object'] = new WP_Post(5236);
$GLOBALS['aurora_smoke_meta'] = [];

function add_filter(
    string $hook,
    callable|string $callback,
    int $priority = 10,
    int $accepted_args = 1
): bool {
    $GLOBALS['aurora_smoke_filters'][] = compact(
        'hook',
        'callback',
        'priority',
        'accepted_args'
    );
    return true;
}

function is_singular(): bool {
    return $GLOBALS['aurora_smoke_is_singular'];
}

function get_queried_object(): object|null {
    return $GLOBALS['aurora_smoke_object'];
}

function get_post_meta(int $post_id, string $key, bool $single): mixed {
    if ($post_id !== 5236 || $key !== 'jetpack_seo_html_title' || !$single) {
        throw new RuntimeException('Unexpected post-meta lookup.');
    }

    return $GLOBALS['aurora_smoke_meta'][$key] ?? '';
}

function wp_strip_all_tags(string $value): string {
    return strip_tags($value);
}

function expect_same(mixed $expected, mixed $actual, string $message): void {
    if ($expected === $actual) {
        return;
    }

    fwrite(
        STDERR,
        sprintf("FAIL: %s\nExpected: %s\nActual: %s\n", $message, var_export($expected, true), var_export($actual, true))
    );
    exit(1);
}

require dirname(__DIR__) . '/inc/seo-title.php';

expect_same(
    [
        'hook'          => 'pre_get_document_title',
        'callback'      => 'KK_Aurora\\filter_pre_get_document_title',
        'priority'      => PHP_INT_MAX,
        'accepted_args' => 1,
    ],
    $GLOBALS['aurora_smoke_filters'][0] ?? null,
    'The title filter must be registered last.'
);

$GLOBALS['aurora_smoke_meta']['jetpack_seo_html_title'] = '  <b>AI Skills for Storytellers: OpenAI\'s Souki Mansoor</b>  ';
expect_same(
    "AI Skills for Storytellers: OpenAI's Souki Mansoor",
    KK_Aurora\filter_pre_get_document_title('Fallback title'),
    'A populated approved title must be trimmed and tag-free.'
);

$GLOBALS['aurora_smoke_meta']['jetpack_seo_html_title'] = "  Broetry, Content Farms, TL;DR \u{2014} Is the Internet OK?  ";
expect_same(
    "Broetry, Content Farms, TL;DR \u{2014} Is the Internet OK?",
    KK_Aurora\filter_pre_get_document_title('Fallback title'),
    'Unicode punctuation in approved titles must remain exact.'
);

$GLOBALS['aurora_smoke_meta']['jetpack_seo_html_title'] = 'AI and Music: A Digital Renaissance';
expect_same(
    'AI and Music: A Digital Renaissance',
    KK_Aurora\filter_pre_get_document_title('Fallback title'),
    'Short approved titles must remain exact.'
);

$GLOBALS['aurora_smoke_meta']['jetpack_seo_html_title'] = '';
expect_same(
    'Fallback title',
    KK_Aurora\filter_pre_get_document_title('Fallback title'),
    'Empty approved titles must preserve the existing fallback.'
);

$GLOBALS['aurora_smoke_meta']['jetpack_seo_html_title'] = ['not', 'a', 'string'];
expect_same(
    'Fallback title',
    KK_Aurora\filter_pre_get_document_title('Fallback title'),
    'Invalid approved titles must preserve the existing fallback.'
);

$GLOBALS['aurora_smoke_is_singular'] = false;
$GLOBALS['aurora_smoke_meta']['jetpack_seo_html_title'] = 'Must not render';
expect_same(
    'Archive fallback',
    KK_Aurora\filter_pre_get_document_title('Archive fallback'),
    'Non-singular routes must remain unchanged.'
);

$GLOBALS['aurora_smoke_is_singular'] = true;
$GLOBALS['aurora_smoke_object'] = new stdClass();
expect_same(
    'Invalid object fallback',
    KK_Aurora\filter_pre_get_document_title('Invalid object fallback'),
    'Unexpected queried objects must remain unchanged.'
);

echo "Aurora SEO title smoke passed.\n";
