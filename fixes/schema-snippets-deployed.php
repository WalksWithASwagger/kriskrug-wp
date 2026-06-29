<?php
/**
 * Schema.org JSON-LD — kriskrug.co
 *
 * Deployed via Code Snippets plugin on 2026-05-15 (not as a mu-plugin yet;
 * SSH access still pending). This is the actual PHP that lives inside the
 * "KK Schema" Code Snippet on production — keep it in sync if either side
 * is edited.
 *
 * Differences from fixes/schema-snippets.php (the SSH-deployable mu-plugin
 * version):
 *   - VERIFY-ME placeholders replaced with confirmed values
 *   - Headshot omitted (no clean media-library file yet; add later)
 *   - LinkedIn / GitHub / YouTube / Wikipedia omitted (URLs unverified or 404)
 *   - kk_schema_is_ready() guard removed (values are baked in)
 *   - Conditional Person.image / Person.sameAs filtering
 *
 * When pasting into Code Snippets: strip the opening <?php tag (Code Snippets
 * wraps the snippet automatically).
 */

function kk_schema_constants() {
    return array(
        'site_name'    => 'Kris Krüg | Generative AI Tools & Techniques',
        'site_url'     => 'https://kriskrug.co',
        'person_name'  => 'Kris Krüg',
        'person_alt'   => 'Kris Krug',
        'person_image' => '',  // TODO: add a real headshot URL once uploaded to media
        'person_job'   => 'Generative AI Strategist, Photographer, Community Builder',
        'person_descr' => 'Vancouver-based generative AI strategist, photographer, and community builder. Founder of the BC + AI Ecosystem Industry Association.',
        // Only verified, owned URLs. Add LinkedIn etc. when KK confirms.
        'same_as' => array(
            'https://twitter.com/kriskrug',
            'https://x.com/kriskrug',
            'https://www.instagram.com/kriskrug/',
        ),
        'works_for' => array(
            array('name' => 'BC + AI Ecosystem Industry Association', 'url' => 'https://bc-ai.ca/'),
            array('name' => 'Vancouver AI',                           'url' => 'https://vancouver.ai/'),
            array('name' => 'Futureproof Festival',                   'url' => 'https://futureproof.website/'),
        ),
        'knows_about' => array(
            'Generative AI', 'AI Strategy', 'AI for Creative Professionals',
            'AI for Journalism', 'AI Ethics', 'Photography', 'Community Building',
            'Vancouver AI Ecosystem', 'Indigenous Technology', 'Generative AI Tools',
        ),
    );
}

function kk_schema_emit($schema) {
    if (empty($schema)) return;
    echo "\n<script type=\"application/ld+json\">"
        . wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE)
        . "</script>\n";
}

// 1. Person — sitewide
function kk_schema_person() {
    $c = kk_schema_constants();
    $works = array();
    foreach ($c['works_for'] as $org) {
        if (!empty($org['url'])) {
            $works[] = array('@type' => 'Organization', 'name' => $org['name'], 'url' => $org['url']);
        }
    }
    $person = array(
        '@context'      => 'https://schema.org',
        '@type'         => 'Person',
        '@id'           => $c['site_url'] . '/#person',
        'name'          => $c['person_name'],
        'alternateName' => $c['person_alt'],
        'description'   => $c['person_descr'],
        'url'           => $c['site_url'],
        'jobTitle'      => $c['person_job'],
        'worksFor'      => $works,
        'sameAs'        => array_values(array_filter($c['same_as'])),
        'knowsAbout'    => $c['knows_about'],
    );
    if (!empty($c['person_image'])) {
        $person['image'] = $c['person_image'];
    }
    kk_schema_emit($person);
}
add_action('wp_head', 'kk_schema_person', 5);

// 2. WebSite + SearchAction — homepage only
function kk_schema_website() {
    if (!is_front_page() && !is_home()) return;
    $c = kk_schema_constants();
    kk_schema_emit(array(
        '@context'        => 'https://schema.org',
        '@type'           => 'WebSite',
        '@id'             => $c['site_url'] . '/#website',
        'url'             => $c['site_url'],
        'name'            => $c['site_name'],
        'inLanguage'      => 'en-US',
        'publisher'       => array('@id' => $c['site_url'] . '/#person'),
        'potentialAction' => array(
            '@type'       => 'SearchAction',
            'target'      => array(
                '@type'       => 'EntryPoint',
                'urlTemplate' => $c['site_url'] . '/?s={search_term_string}',
            ),
            'query-input' => 'required name=search_term_string',
        ),
    ));
}
add_action('wp_head', 'kk_schema_website', 6);

// 3. Article — every blog post
function kk_schema_article() {
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
    $section = ($cats && $cats[0]->name !== 'Misc') ? $cats[0]->name : null;
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
    if ($image)   $schema['image']          = $image;
    if ($section) $schema['articleSection'] = $section;

    kk_schema_emit($schema);
}
add_action('wp_head', 'kk_schema_article', 7);

// 4. BreadcrumbList — non-homepage
function kk_schema_breadcrumb() {
    if (is_front_page()) return;
    $c = kk_schema_constants();
    $items = array(
        array('@type' => 'ListItem', 'position' => 1, 'name' => 'Home', 'item' => $c['site_url']),
    );
    $pos = 2;
    if (is_singular('post')) {
        $items[] = array('@type' => 'ListItem', 'position' => $pos++, 'name' => 'Blog',          'item' => $c['site_url'] . '/blog/');
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

// 5. Service — pages with a kk_service_audience custom field
function kk_schema_service() {
    if (!is_page()) return;
    $audience = get_post_meta(get_queried_object_id(), 'kk_service_audience', true);
    if (!$audience) return;
    $c = kk_schema_constants();
    kk_schema_emit(array(
        '@context'    => 'https://schema.org',
        '@type'       => 'Service',
        'name'        => wp_strip_all_tags(get_the_title()),
        'description' => wp_strip_all_tags(get_the_excerpt()),
        'provider'    => array('@id' => $c['site_url'] . '/#person'),
        'audience'    => array('@type' => 'Audience', 'audienceType' => $audience),
        'url'         => get_permalink(),
    ));
}
add_action('wp_head', 'kk_schema_service', 9);
