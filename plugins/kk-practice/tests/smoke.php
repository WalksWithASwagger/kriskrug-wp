<?php
/** Registration/privacy boundaries without a WordPress dependency. Browser tests exercise real WordPress. */
define( 'ABSPATH', __DIR__ );
function add_action( ...$args ) {}
function add_filter( ...$args ) {}
function is_singular() { return $GLOBALS['singular']; }
function has_block( ...$args ) { return $GLOBALS['block']; }
function get_queried_object() { return null; }
function esc_attr( $value ) { return htmlspecialchars( $value, ENT_QUOTES ); }
require dirname( __DIR__ ) . '/kk-practice.php';
function check( $condition, $message ) { if ( ! $condition ) { throw new RuntimeException( $message ); } }
$GLOBALS['singular'] = false;
$GLOBALS['block'] = true;
check( ! kk_practice_is_page(), 'Archives must not activate the exercise' );
$GLOBALS['singular'] = true;
$GLOBALS['block'] = false;
check( kk_practice_script_tag( '<script>keep</script>', 'other' ) === '<script>keep</script>', 'Other pages are unchanged' );
$GLOBALS['block'] = true;
check( kk_practice_script_tag( '<script>drop</script>', 'other' ) === '', 'Unapproved scripts are suppressed' );
check( str_contains( kk_practice_script_tag( '<script src="view.js"></script>', 'kk-context-brief-view-script' ), 'nonce="' ), 'Exercise gets its nonce' );
check( kk_practice_inline_attributes( array() )['type'] === 'application/json', 'Unexpected inline code is inert' );
check( count( kk_practice_copy()['fields'] ) === 6, 'Exactly six questions' );
echo "KK Practice smoke passed.\n";
