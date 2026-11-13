<?php
/**
 * Smoke tests for fixes/issue-767-hide-rest-users.php (live Code Snippet 24).
 *
 * Stubs the small WordPress surface the snippet touches so it runs without a
 * WordPress install. Core matches REST routes case-insensitively, so every
 * spelling of the users route must be blocked for logged-out reads.
 */

class WP_Error {
	private $code;
	private $data;

	public function __construct( $code = '', $message = '', $data = null ) {
		unset( $message );
		$this->code = $code;
		$this->data = $data;
	}

	public function get_error_code() {
		return $this->code;
	}

	public function get_error_data() {
		return $this->data;
	}
}

class WP_REST_Users_Controller {}
class WP_REST_Posts_Controller {}

class KK_Test_REST_Request {
	private $route;
	private $method;

	public function __construct( $method, $route ) {
		$this->method = $method;
		$this->route  = $route;
	}

	public function get_route() {
		return $this->route;
	}

	public function get_method() {
		return $this->method;
	}
}

$GLOBALS['kk_767_logged_in'] = false;
$GLOBALS['kk_767_filters']   = array();

function is_user_logged_in() {
	return (bool) $GLOBALS['kk_767_logged_in'];
}

function is_wp_error( $thing ) {
	return $thing instanceof WP_Error;
}

function add_filter( $hook, $callback, $priority = 10, $args = 1 ) {
	$GLOBALS['kk_767_filters'][ $hook ] = array( $callback, $priority, $args );
}

require dirname( __DIR__ ) . '/issue-767-hide-rest-users.php';

$failures = 0;

function kk_767_assert( $condition, $label ) {
	global $failures;
	if ( ! $condition ) {
		$failures++;
		fwrite( STDERR, "FAIL: {$label}\n" );
	}
}

function kk_767_is_block( $result ) {
	if ( ! $result instanceof WP_Error ) {
		return false;
	}
	$data = $result->get_error_data();

	return 'rest_cannot_access_users' === $result->get_error_code() && 401 === ( $data['status'] ?? null );
}

function kk_767_pre_dispatch( $method, $route ) {
	return kk_767_restrict_unauthenticated_users_rest( null, null, new KK_Test_REST_Request( $method, $route ) );
}

function kk_767_before_callbacks( $method, $route, $controller, $response = null ) {
	$handler = array( 'callback' => array( $controller, 'get_items' ) );

	return kk_767_restrict_users_controller( $response, $handler, new KK_Test_REST_Request( $method, $route ) );
}

kk_767_assert( isset( $GLOBALS['kk_767_filters']['rest_pre_dispatch'] ), 'rest_pre_dispatch filter registered' );
kk_767_assert( isset( $GLOBALS['kk_767_filters']['rest_request_before_callbacks'] ), 'rest_request_before_callbacks filter registered' );
kk_767_assert( 3 === $GLOBALS['kk_767_filters']['rest_request_before_callbacks'][2], 'backstop receives three arguments' );

$users_routes = array( '/wp/v2/users', '/wp/v2/users/', '/wp/v2/users/18', '/wp/v2/users/me', '/wp/v2/Users', '/wp/v2/USERS', '/WP/V2/users', '/wp/v2/Users/18', '/Wp/V2/uSeRs/1' );
foreach ( $users_routes as $route ) {
	kk_767_assert( kk_767_is_block( kk_767_pre_dispatch( 'GET', $route ) ), "logged-out GET {$route} is blocked before routing" );
	kk_767_assert( kk_767_is_block( kk_767_pre_dispatch( 'head', $route ) ), "logged-out HEAD {$route} is blocked before routing" );
}

foreach ( array( '/wp/v2/posts', '/wp/v2/usersx', '/wp/v2/user', '/wp/v2/pages/2', '/oembed/1.0/embed', '/wp/v2' ) as $route ) {
	kk_767_assert( null === kk_767_pre_dispatch( 'GET', $route ), "other route {$route} passes through" );
}

kk_767_assert( null === kk_767_pre_dispatch( 'POST', '/wp/v2/Users' ), 'non-read methods are left to core' );

$existing = new WP_Error( 'earlier', 'earlier override', array( 'status' => 418 ) );
kk_767_assert( $existing === kk_767_restrict_unauthenticated_users_rest( $existing, null, new KK_Test_REST_Request( 'GET', '/wp/v2/users' ) ), 'an earlier rest_pre_dispatch override is preserved' );

$users = new WP_REST_Users_Controller();
$posts = new WP_REST_Posts_Controller();
kk_767_assert( kk_767_is_block( kk_767_before_callbacks( 'GET', '/wp/v2/any-spelling', $users ) ), 'backstop blocks the users controller for any route spelling' );
kk_767_assert( null === kk_767_before_callbacks( 'GET', '/wp/v2/posts', $posts ), 'backstop ignores other controllers' );
kk_767_assert( null === kk_767_before_callbacks( 'POST', '/wp/v2/users', $users ), 'backstop leaves non-read methods to core' );
kk_767_assert( $existing === kk_767_before_callbacks( 'GET', '/wp/v2/users', $users, $existing ), 'backstop preserves an earlier error' );
kk_767_assert( null === kk_767_restrict_users_controller( null, array( 'callback' => 'rest_get_server' ), new KK_Test_REST_Request( 'GET', '/wp/v2/users' ) ), 'string callbacks are not treated as the users controller' );

$GLOBALS['kk_767_logged_in'] = true;
foreach ( array( '/wp/v2/users', '/wp/v2/Users', '/wp/v2/users/me' ) as $route ) {
	kk_767_assert( null === kk_767_pre_dispatch( 'GET', $route ), "logged-in GET {$route} is left to core" );
}
kk_767_assert( null === kk_767_before_callbacks( 'GET', '/wp/v2/users/me', $users ), 'logged-in users controller reads are left to core' );

if ( $failures > 0 ) {
	fwrite( STDERR, "#767 REST users smoke failed: {$failures} assertion(s).\n" );
	exit( 1 );
}

echo "#767 REST users smoke passed.\n";
