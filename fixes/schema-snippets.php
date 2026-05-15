<?php
/**
 * Schema.org JSON-LD snippets for kriskrug.co
 *
 * Extends fixes/issue-39-schema-markup.php for sitewide coverage and adds
 * WebSite, Breadcrumb, Service schemas.
 *
 * DEPLOY AS A MUST-USE PLUGIN (not theme functions.php), so it survives
 * theme switches:
 *   - Place this file at: wp-content/mu-plugins/kk-schema.php
 *   - mu-plugins are auto-loaded, no activation needed
 *   - On Pagely: drop via SSH/SFTP into wp-content/mu-plugins/
 *
 * Test after deploy:
 *   - https://search.google.com/test/rich-results  (paste any URL)
 *   - https://validator.schema.org/                 (general schema check)
 *
 * !!!  SAFETY: this file is INERT BY DEFAULT.  !!!
 * Until you replace every value containing the literal string
 * "VERIFY-ME" with a real value, the schema emitters all return early
 * and nothing is output. This is to prevent shipping placeholder URLs
 * as live JSON-LD claims about Kris.
 *
 * Walk through kk_schema_constants() once, fill in real values, remove
 * every "VERIFY-ME" string, then the schema will start emitting.
 */

// ----------------------------------------------------------------------
// Configuration — every VERIFY-ME marker must be replaced before this
// file emits any schema. See kk_schema_is_ready() below.
// ----------------------------------------------------------------------
function kk_schema_constants() {
    return array(
        'site_name'        => 'Kris Krüg | Generative AI Tools & Techniques',
        'site_url'         => 'https://kriskrug.co',
        'person_name'      => 'Kris Krüg',
        'person_alt'       => 'Kris Krug',
        // Confirm the file exists at this path AND is your current headshot.
        'person_image'     => 'VERIFY-ME-headshot-url',
        'person_job'       => 'Generative AI Strategist, Photographer, Community Builder',
        'person_descr'     => 'Vancouver-based generative AI strategist, photographer, and community builder. Founder of the BC + AI Ecosystem Industry Association.',
        // Logo image for publisher schema. Confirm exists.
        'logo_url'         => 'VERIFY-ME-logo-url',
        // Profiles — every URL here is a public CLAIM that this profile is yours.
        // Only include accounts you actually own. DELETE any line you don't use.
        'same_as' => array(
            'VERIFY-ME-linkedin-url',     // e.g. https://www.linkedin.com/in/kriskrug/
            'VERIFY-ME-twitter-or-x-url', // e.g. https://x.com/kriskrug  -- confirm actual handle
            'VERIFY-ME-youtube-url',
            'VERIFY-ME-instagram-url',
            'VERIFY-ME-github-url',
            // Add Wikipedia entry here if KK has one — strong signal.
        ),
        // Organizations Kris is affiliated with. Replace each url. Remove rows that don't apply.
        'works_for' => array(
            array('name' => 'BC + AI Ecosystem Industry Association', 'url' => 'VERIFY-ME-bcai-url'),
            array('name' => 'Indigenomics.ai',                        'url' => 'VERIFY-ME-indigenomics-url'),
            array('name' => 'The Upgrade AI',                         'url' => 'VERIFY-ME-upgrade-ai-url'),
        ),
        'knows_about' => array(
            'Generative AI', 'AI Strategy', 'AI for Creative Professionals',
            'AI for Journalism', 'AI Ethics', 'Photography', 'Community Building',
            'Vancouver AI Ecosystem', 'Indigenous Technology', 'Generative AI Tools',
        ),
    );
}

/**
 * Returns true only when every VERIFY-ME placeholder has been replaced.
 * Every emitter below gates on this; until ready, nothing is output.
 */
function kk_schema_is_ready() {
    $c = kk_schema_constants();
    $blob = wp_json_encode($c);
    return strpos($blob, 'VERIFY-ME') === false;
}

// ----------------------------------------------------------------------
// Output a JSON-LD <script> block.
// ----------------------------------------------------------------------
function kk_schema_emit($schema) {
    if (empty($schema)) return;
    echo "\n<script type=\"application/ld+json\">"
        . wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE)
        . "</script>\n";
}

// ----------------------------------------------------------------------
// 1. Person schema — sitewide.
//    Renders on every page so LLMs see consistent entity identity.
// ----------------------------------------------------------------------
function kk_schema_person() {
    if (!kk_schema_is_ready()) return;
    $c = kk_schema_constants();
    $works = array();
    foreach ($c['works_for'] as $org) {
        $works[] = array('@type' => 'Organization', 'name' => $org['name'], 'url' => $org['url']);
    }
    kk_schema_emit(array(
        '@context'     => 'https://schema.org',
        '@type'        => 'Person',
        '@id'          => $c['site_url'] . '/#person',
        'name'         => $c['person_name'],
        'alternateName'=> $c['person_alt'],
        'description'  => $c['person_descr'],
        'url'          => $c['site_url'],
        'image'        => $c['person_image'],
        'jobTitle'     => $c['person_job'],
        'worksFor'     => $works,
        'sameAs'       => array_values(array_filter($c['same_as'])),
        'knowsAbout'   => $c['knows_about'],
    ));
}
add_action('wp_head', 'kk_schema_person', 5);

// ----------------------------------------------------------------------
// 2. WebSite schema with SearchAction — sitewide (homepage in particular).
//    Triggers Google's sitelinks search box. Also gives LLMs the canonical
//    "site name" + "publisher" entity to reference.
// ----------------------------------------------------------------------
function kk_schema_website() {
    if (!kk_schema_is_ready()) return;
    if (!is_front_page() && !is_home()) return;
    $c = kk_schema_constants();
    kk_schema_emit(array(
        '@context'      => 'https://schema.org',
        '@type'         => 'WebSite',
        '@id'           => $c['site_url'] . '/#website',
        'url'           => $c['site_url'],
        'name'          => $c['site_name'],
        'inLanguage'    => 'en-US',
        'publisher'     => array('@id' => $c['site_url'] . '/#person'),
        'potentialAction' => array(
            '@type'      => 'SearchAction',
            'target'     => array(
                '@type'        => 'EntryPoint',
                'urlTemplate'  => $c['site_url'] . '/?s={search_term_string}',
            ),
            'query-input' => 'required name=search_term_string',
        ),
    ));
}
add_action('wp_head', 'kk_schema_website', 6);

// ----------------------------------------------------------------------
// 3. Article schema — for every blog post.
//    Extends the existing fixes/issue-39-schema-markup.php version:
//      - links the author by @id (so it resolves to the sitewide Person)
//      - uses Article (not BlogPosting — Article is broader and rendered
//        identically by Google; gives more flexibility)
//      - adds wordCount and articleSection (using primary category)
// ----------------------------------------------------------------------
function kk_schema_article() {
    if (!kk_schema_is_ready()) return;
    if (!is_singular('post')) return;
    $c = kk_schema_constants();
    global $post;

    $image = null;
    if (has_post_thumbnail()) {
        $src = wp_get_attachment_image_src(get_post_thumbnail_id(), 'full');
        if ($src) {
            $image = array(
                '@type'  => 'ImageObject',
                'url'    => $src[0],
                'width'  => $src[1],
                'height' => $src[2],
            );
        }
    }
    $cats = get_the_category();
    $section = $cats && $cats[0]->name !== 'Misc' ? $cats[0]->name : null;
    $wc = str_word_count(wp_strip_all_tags($post->post_content));

    $schema = array(
        '@context'         => 'https://schema.org',
        '@type'            => 'Article',
        'headline'         => get_the_title(),
        'description'      => get_the_excerpt(),
        'datePublished'    => get_the_date('c'),
        'dateModified'     => get_the_modified_date('c'),
        'author'           => array('@id' => $c['site_url'] . '/#person'),
        'publisher'        => array('@id' => $c['site_url'] . '/#person'),
        'mainEntityOfPage' => array('@type' => 'WebPage', '@id' => get_permalink()),
        'wordCount'        => $wc,
        'inLanguage'       => 'en-US',
    );
    if ($image) $schema['image'] = $image;
    if ($section) $schema['articleSection'] = $section;

    kk_schema_emit($schema);
}
add_action('wp_head', 'kk_schema_article', 7);

// ----------------------------------------------------------------------
// 4. BreadcrumbList schema — for non-home pages and posts.
// ----------------------------------------------------------------------
function kk_schema_breadcrumb() {
    if (!kk_schema_is_ready()) return;
    if (is_front_page()) return;
    $c = kk_schema_constants();
    $items = array(
        array('@type' => 'ListItem', 'position' => 1, 'name' => 'Home', 'item' => $c['site_url']),
    );
    $pos = 2;
    if (is_singular('post')) {
        $items[] = array('@type' => 'ListItem', 'position' => $pos++, 'name' => 'Blog', 'item' => $c['site_url'] . '/blog/');
        $items[] = array('@type' => 'ListItem', 'position' => $pos++, 'name' => get_the_title(), 'item' => get_permalink());
    } elseif (is_page()) {
        $items[] = array('@type' => 'ListItem', 'position' => $pos++, 'name' => get_the_title(), 'item' => get_permalink());
    } elseif (is_category() || is_tag()) {
        $items[] = array('@type' => 'ListItem', 'position' => $pos++, 'name' => single_term_title('', false), 'item' => get_term_link(get_queried_object()));
    }
    kk_schema_emit(array(
        '@context'        => 'https://schema.org',
        '@type'           => 'BreadcrumbList',
        'itemListElement' => $items,
    ));
}
add_action('wp_head', 'kk_schema_breadcrumb', 8);

// ----------------------------------------------------------------------
// 5. Service schema — for the AI Upgrade / services pages.
//
//    Slug-independent: in wp-admin, edit the service page and add a
//    custom field named `kk_service_audience` (e.g. "Media leaders,
//    newsroom managers"). When that field is set, this emits a Service
//    schema using the page's own title and excerpt.
//
//    This survives IA renames (planned in FIX_QUEUE P2.1) because it's
//    keyed off post_meta, not slugs.
// ----------------------------------------------------------------------
function kk_schema_service() {
    if (!kk_schema_is_ready()) return;
    if (!is_page()) return;
    $audience = get_post_meta(get_queried_object_id(), 'kk_service_audience', true);
    if (!$audience) return;
    $c = kk_schema_constants();
    kk_schema_emit(array(
        '@context'   => 'https://schema.org',
        '@type'      => 'Service',
        'name'       => wp_strip_all_tags(get_the_title()),
        'description'=> wp_strip_all_tags(get_the_excerpt()),
        'provider'   => array('@id' => $c['site_url'] . '/#person'),
        'audience'   => array('@type' => 'Audience', 'audienceType' => $audience),
        'url'        => get_permalink(),
    ));
}
add_action('wp_head', 'kk_schema_service', 9);

// ----------------------------------------------------------------------
// END.
//
// Schemas intentionally NOT included here (can add later):
//   - FAQPage    (requires per-page FAQ data; use a plugin or ACF)
//   - Event      (requires event date/venue; add when listing concrete events)
//   - VideoObject (requires per-video metadata; add to podcast page)
//   - Review     (testimonials page; add when consolidating testimonials)
// ----------------------------------------------------------------------
