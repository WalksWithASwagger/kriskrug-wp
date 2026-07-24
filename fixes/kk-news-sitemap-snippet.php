<?php
/**
 * Google News-style sitemap — kriskrug.co (#425)
 *
 * DRAFT for Code Snippets. Do not paste/activate without KK approval.
 * Emits only posts classified as NewsArticle (see kk_schema_post_type in
 * schema-snippets-deployed.php) from the last 48 hours at /news-sitemap.xml.
 *
 * When pasting into Code Snippets: strip the opening <?php tag.
 */

if (!defined('ABSPATH')) {
    exit;
}

add_action('init', function () {
    add_rewrite_rule('^news-sitemap\.xml$', 'index.php?kk_news_sitemap=1', 'top');
    add_rewrite_tag('%kk_news_sitemap%', '1');
});

add_filter('query_vars', function ($vars) {
    $vars[] = 'kk_news_sitemap';
    return $vars;
});

add_action('template_redirect', function () {
    if (!get_query_var('kk_news_sitemap')) {
        return;
    }

    $posts = get_posts(array(
        'post_type'           => 'post',
        'post_status'         => 'publish',
        'posts_per_page'      => 100,
        'ignore_sticky_posts' => true,
        'date_query'          => array(
            array(
                'after'     => '48 hours ago',
                'inclusive' => true,
            ),
        ),
        'orderby'             => 'date',
        'order'               => 'DESC',
    ));

    header('Content-Type: application/xml; charset=UTF-8');
    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
    echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"'
        . ' xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">' . "\n";

    foreach ($posts as $post) {
        $type = function_exists('kk_schema_post_type')
            ? kk_schema_post_type($post)
            : 'BlogPosting';
        if ($type !== 'NewsArticle') {
            continue;
        }
        $loc = esc_url(get_permalink($post));
        $title = esc_html(get_the_title($post));
        $pub = get_the_date('c', $post);
        echo "  <url>\n";
        echo "    <loc>{$loc}</loc>\n";
        echo "    <news:news>\n";
        echo "      <news:publication>\n";
        echo "        <news:name>Kris Krug</news:name>\n";
        echo "        <news:language>en</news:language>\n";
        echo "      </news:publication>\n";
        echo "      <news:publication_date>{$pub}</news:publication_date>\n";
        echo "      <news:title>{$title}</news:title>\n";
        echo "    </news:news>\n";
        echo "  </url>\n";
    }

    echo '</urlset>';
    exit;
});

/**
 * After first activate: flush rewrite rules once (Settings → Permalinks → Save)
 * or run `flush_rewrite_rules()` from a one-shot admin action.
 */
