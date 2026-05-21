<?php
/**
 * Issue #9: accessible search forms for kriskrug.co.
 *
 * Deploy with Code Snippets after backup/restore proof exists. When pasting
 * into Code Snippets, remove this opening <?php tag.
 */

add_filter( 'get_search_form', 'kk_issue_9_accessible_search_form', 20, 2 );
function kk_issue_9_accessible_search_form( $form, $args ) {
    static $instance = 0;
    $instance++;

    $field_id   = 'kk-site-search-field-' . $instance;
    $form_label = 1 === $instance ? __( 'Header site search', 'kriskrug' ) : __( 'Navigation site search', 'kriskrug' );
    $query      = get_search_query( false );

    return sprintf(
        '<form role="search" aria-label="%1$s" method="get" class="search-form kk-search-form" action="%2$s">
            <label class="kk-search-label" for="%3$s">%4$s</label>
            <div class="kk-search-row">
                <input id="%3$s" type="search" class="search-field kk-search-field" placeholder="%5$s" value="%6$s" name="s" aria-label="%7$s">
                <button type="submit" class="kk-search-submit" aria-label="%8$s">%9$s</button>
            </div>
        </form>',
        esc_attr( $form_label ),
        esc_url( home_url( '/' ) ),
        esc_attr( $field_id ),
        esc_html__( 'Search the site', 'kriskrug' ),
        esc_attr__( 'Search', 'kriskrug' ),
        esc_attr( $query ),
        esc_attr__( 'Search the site', 'kriskrug' ),
        esc_attr__( 'Submit site search', 'kriskrug' ),
        esc_html__( 'Search', 'kriskrug' )
    );
}

add_action( 'wp_head', 'kk_issue_9_accessible_search_styles', 30 );
function kk_issue_9_accessible_search_styles() {
    ?>
    <style id="kk-issue-9-search-accessibility">
        .kk-search-form {
            margin: 0;
        }

        .kk-search-label {
            color: #111;
            display: block;
            font-size: 14px;
            font-weight: 700;
            line-height: 1.3;
            margin: 0 0 6px;
        }

        .kk-search-row {
            align-items: stretch;
            display: flex;
            gap: 8px;
        }

        .kk-search-form .kk-search-field {
            box-sizing: border-box;
            min-height: 44px;
            width: 100%;
        }

        #masthead .kk-search-form .kk-search-field {
            float: none;
            max-width: none;
            width: 100%;
        }

        .kk-search-form .kk-search-submit {
            cursor: pointer;
            min-height: 44px;
            padding: 8px 14px;
            white-space: nowrap;
        }

        .widget_search .kk-search-submit,
        .nav-primary .kk-search-submit {
            display: inline-block;
        }

        .nav-primary #search-container {
            bottom: auto;
            top: 100%;
        }

        #search-toggle {
            position: relative;
        }

        #search-toggle a.screen-reader-text {
            clip: auto;
            clip-path: none;
            color: transparent;
            display: block;
            height: 46px;
            left: 0;
            margin: 0;
            overflow: hidden;
            padding: 0;
            position: absolute !important;
            top: 0;
            width: 42px;
            z-index: 1;
        }

        #search-toggle a.screen-reader-text:focus,
        .kk-search-form .kk-search-field:focus,
        .kk-search-form .kk-search-submit:focus {
            outline: 3px solid #1b8be0;
            outline-offset: 2px;
        }

        #search-toggle a.screen-reader-text:focus {
            background: transparent;
            color: transparent;
        }

        @media screen and (max-width: 720px) {
            .kk-search-row {
                flex-direction: column;
            }

            .kk-search-form .kk-search-submit {
                width: 100%;
            }
        }
    </style>
    <?php
}

add_action( 'wp_footer', 'kk_issue_9_accessible_search_toggle', 30 );
function kk_issue_9_accessible_search_toggle() {
    ?>
    <script id="kk-issue-9-search-toggle">
        (function () {
            var wrapper = document.getElementById('search-toggle');
            var toggle = wrapper ? wrapper.querySelector('a') : null;
            var container = document.getElementById('search-container');

            if (!wrapper || !toggle || !container) {
                return;
            }

            function isOpen() {
                return !container.classList.contains('displaynone');
            }

            function setOpen(open) {
                container.classList.toggle('displaynone', !open);
                toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
                toggle.setAttribute('aria-label', open ? 'Close site search' : 'Open site search');
                toggle.textContent = open ? 'Close site search' : 'Open site search';

                if (open) {
                    var field = container.querySelector('input[type="search"]');
                    if (field) {
                        field.focus();
                    }
                }
            }

            function activate(event) {
                event.preventDefault();
                event.stopPropagation();
                setOpen(!isOpen());
            }

            toggle.setAttribute('aria-controls', 'search-container');
            toggle.setAttribute('aria-expanded', isOpen() ? 'true' : 'false');
            toggle.setAttribute('aria-label', isOpen() ? 'Close site search' : 'Open site search');
            toggle.setAttribute('role', 'button');
            toggle.textContent = isOpen() ? 'Close site search' : 'Open site search';

            toggle.addEventListener('click', activate);
            toggle.addEventListener('keydown', function (event) {
                if (event.key === ' ') {
                    activate(event);
                }
            });
        }());
    </script>
    <?php
}
