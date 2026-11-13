<?php
/**
 * KK REST users restriction for kriskrug.co (#767)
 *
 * Stops unauthenticated GET/HEAD requests to the core users endpoints
 * (collection and single-user) from returning the public user list.
 * Authenticated requests are left to core permission checks.
 *
 * LIVE as Code Snippet 24 ("KK 767: restrict unauthenticated REST users",
 * scope: global) since 2026-09-03; v2 live since 2026-11-12. v2 adds
 * case-insensitive route matching and a controller-level backstop: core
 * matches REST routes case-insensitively, so v1's case-sensitive check let
 * /wp/v2/Users through.
 * Change the live snippet only with KK approval, a snippet snapshot, and the
 * post-apply checks below.
 *
 * When pasting into Code Snippets: strip the opening <?php tag (Code Snippets
 * wraps the snippet automatically). Run this snippet everywhere, not
 * admin-only. REST hooks only fire on REST requests, so a global scope costs
 * nothing elsewhere, and an admin-only scope would miss the leak.
 *
 * Rollback: restore the v1 code from the pre-apply snapshot, or deactivate the
 * snippet. Pagely's edge cache stores logged-out GET REST responses, 200s
 * included, so a URL fetched while the leak was open can keep serving the old
 * list until a purge or expiry (about an hour on 2026-11-12). Re-run
 * scripts/check_user_enumeration.sh after any apply or rollback; it adds a
 * unique query parameter so it measures the origin, not the cache.
 *
 * -------------------------------------------------------------------------
 * Site Kit / block-editor risk
 * -------------------------------------------------------------------------
 * The block editor author picker and Site Kit (logged-in dashboard,
 * /wp/v2/users/me, Search Console user matching) call this namespace with a
 * cookie + X-WP-Nonce or an Application Password. Those requests are
 * authenticated before rest_pre_dispatch and rest_request_before_callbacks
 * run, so is_user_logged_in() is reliable in both hooks.
 *
 * Do NOT unset the route from rest_endpoints based on is_user_logged_in().
 * That filter runs before REST authentication and would 404 the editor.
 *
 * After apply, verify while logged in as an editor:
 * 1. Posts > Add New: the author dropdown still lists users.
 * 2. Site Kit dashboard still loads (Settings / Search Console).
 * 3. Authenticated GET /wp-json/wp/v2/users/me still returns 200.
 * 4. scripts/check_user_enumeration.sh passes logged out, including its
 *    mixed-case probes.
 * If (1) or (2) fail, restore the snapshot immediately.
 */

/**
 * True when the REST route is the core users collection or a users sub-route.
 *
 * Case-insensitive, because WP_REST_Server matches routes with the `i` flag.
 *
 * @param string $route Matched REST route from WP_REST_Request::get_route().
 * @return bool
 */
function kk_767_is_users_rest_route(string $route): bool {
    return (bool) preg_match('#^/wp/v2/users(?:/|$)#i', $route);
}

/**
 * True when the matched REST handler belongs to the core users controller.
 *
 * @param mixed $handler Handler array passed to rest_request_before_callbacks.
 * @return bool
 */
function kk_767_is_users_controller_handler($handler): bool {
    if (!is_array($handler) || !isset($handler['callback']) || !is_array($handler['callback'])) {
        return false;
    }

    $target = $handler['callback'][0] ?? null;

    return $target instanceof WP_REST_Users_Controller;
}

/**
 * True for a logged-out GET or HEAD request.
 *
 * @param WP_REST_Request $request Current REST request.
 * @return bool
 */
function kk_767_is_unauthenticated_read($request): bool {
    $method = strtoupper((string) $request->get_method());

    return in_array($method, array('GET', 'HEAD'), true) && !is_user_logged_in();
}

/**
 * The response returned instead of user data.
 *
 * @return WP_Error
 */
function kk_767_users_rest_error(): WP_Error {
    return new WP_Error(
        'rest_cannot_access_users',
        'The users endpoint is not available to unauthenticated requests.',
        array('status' => 401)
    );
}

/**
 * Block unauthenticated reads of /wp/v2/users before routing.
 *
 * @param mixed           $result  Existing override, or null to continue.
 * @param WP_REST_Server  $server  REST server instance.
 * @param WP_REST_Request $request Current REST request.
 * @return mixed
 */
function kk_767_restrict_unauthenticated_users_rest($result, $server, $request) {
    unset($server);

    if (null !== $result) {
        return $result;
    }

    if (!kk_767_is_users_rest_route((string) $request->get_route())) {
        return $result;
    }

    if (!kk_767_is_unauthenticated_read($request)) {
        return $result;
    }

    return kk_767_users_rest_error();
}
add_filter('rest_pre_dispatch', 'kk_767_restrict_unauthenticated_users_rest', 10, 3);

/**
 * Backstop after routing: whatever spelling of the route core matched, refuse
 * to run the users controller for an unauthenticated read.
 *
 * @param mixed           $response Null, or a WP_Error from earlier checks.
 * @param array           $handler  Matched route handler.
 * @param WP_REST_Request $request  Current REST request.
 * @return mixed
 */
function kk_767_restrict_users_controller($response, $handler, $request) {
    if (is_wp_error($response)) {
        return $response;
    }

    if (!kk_767_is_users_controller_handler($handler)) {
        return $response;
    }

    if (!kk_767_is_unauthenticated_read($request)) {
        return $response;
    }

    return kk_767_users_rest_error();
}
add_filter('rest_request_before_callbacks', 'kk_767_restrict_users_controller', 10, 3);
