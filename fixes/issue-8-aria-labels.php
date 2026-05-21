<?php
/**
 * Issue #8: ARIA labels and focus indicators for icon controls.
 *
 * Intended deploy path: Code Snippets plugin, sitewide frontend snippet.
 * When pasting into Code Snippets, remove the opening <?php tag.
 */

function kk_issue_8_icon_accessibility_styles() {
    ?>
    <style id="kk-issue-8-icon-accessibility">
        #header-left-menu:focus,
        #header-left-menu:focus-visible,
        #search-toggle:focus-within,
        #scrollup:focus,
        #scrollup:focus-visible,
        .widget_catchresponsive_social_icons a.genericon:focus,
        .widget_catchresponsive_social_icons a.genericon:focus-visible,
        .pum-close.popmake-close:focus,
        .pum-close.popmake-close:focus-visible,
        .jp-carousel-icon-btn:focus,
        .jp-carousel-icon-btn:focus-visible,
        .jp-carousel-image-download:focus,
        .jp-carousel-image-download:focus-visible {
            outline: 3px solid #005fcc;
            outline-offset: 3px;
            box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.95);
        }

        .nav-primary #search-toggle:focus-within {
            background-color: #005fcc;
        }

        .nav-primary #search-toggle:focus-within:before {
            color: #fff;
        }

        .widget_catchresponsive_social_icons a.genericon:focus,
        .widget_catchresponsive_social_icons a.genericon:focus-visible {
            background-color: #fff;
            color: #111;
        }
    </style>
    <?php
}
add_action('wp_head', 'kk_issue_8_icon_accessibility_styles', 99);

function kk_issue_8_icon_accessibility_labels() {
    ?>
    <script>
        (function () {
            var setAttributes = function (selector, attributes) {
                document.querySelectorAll(selector).forEach(function (element) {
                    Object.keys(attributes).forEach(function (name) {
                        element.setAttribute(name, attributes[name]);
                    });
                });
            };

            var setSocialLabel = function (className, label) {
                setAttributes(
                    '.widget_catchresponsive_social_icons a.' + className,
                    { 'aria-label': label }
                );
            };

            setAttributes('#header-left-menu', {
                'aria-label': 'Open primary menu',
                'aria-controls': 'mobile-header-left-nav'
            });
            setAttributes('#search-toggle > a', {
                'aria-label': 'Open site search',
                'aria-controls': 'search-container'
            });
            setAttributes('#scrollup', {
                'aria-label': 'Back to top'
            });

            setSocialLabel('genericon-twitter', 'Kris Krug on Twitter');
            setSocialLabel('genericon-mail', 'Email Kris Krug');
            setSocialLabel('genericon-github', 'Kris Krug on GitHub');
            setSocialLabel('genericon-youtube', 'Kris Krug on YouTube');
            setSocialLabel('genericon-instagram', 'Kris Krug on Instagram');
            setSocialLabel('genericon-phone', 'Call Kris Krug');

            document.querySelectorAll('.pum-close.popmake-close').forEach(function (button) {
                if (button.getAttribute('aria-label') === 'Close') {
                    button.setAttribute('aria-label', 'Close popup');
                }
            });

            document.querySelectorAll('.jp-carousel-image-download').forEach(function (link) {
                if (!link.getAttribute('aria-label')) {
                    link.setAttribute('aria-label', 'Download image');
                }
            });
        })();
    </script>
    <?php
}
add_action('wp_footer', 'kk_issue_8_icon_accessibility_labels', 99);
