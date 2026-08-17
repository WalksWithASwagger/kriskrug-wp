<?php
/**
 * KK REST users restriction — kriskrug.co (#767)
 *
 * Stops unauthenticated GET/HEAD /wp-json/wp/v2/users (collection and
 * single-user) from returning the public user list. Authenticated requests
 * are left to core permission checks.
 *
 * PREP ONLY. Not deployed as of 2026-08-16. Do not paste into Code Snippets
 * without KK approval, a snippets snapshot, and the post-apply checks below.
 *
 * When pasting into Code Snippets: strip the opening <?php tag (Code Snippets
 * wraps the snippet automatically). Run this snippet everywhere, not
 * admin-only — rest_pre_dispatch only fires on REST requests, so a
 * front-end/REST scope is enough and an admin-only scope would miss the leak.
 *
 * Rollback: deactivate the snippet. REST responses are not page-cached on
 * this stack in the #709 header audit; still re-run
 * scripts/check_user_enumeration.sh after any apply or rollback.
 *
 * -------------------------------------------------------------------------
 * Site Kit / block-editor risk
 * -------------------------------------------------------------------------
 * The block editor author picker and Site Kit (logged-in dashboard,
 * /wp/v2/users/me, Search Console user matching) call this namespace with a
 * cookie + X-WP-Nonce or an Application Password. Those requests are
 * authenticated by the time rest_pre_dispatch runs, so is_user_logged_in()
 * is reliable here.
 *
 * Do NOT unset the route from rest_endpoints based on is_user_logged_in().
 * That filter runs before REST authentication and would 404 the editor.
 *
 * After apply, verify while logged in as an editor (not with this file —
 * this file must stay inactive until KK says otherwise):
 * 1. Posts → Add New: the author dropdown still lists users.
 * 2. Site Kit dashboard still loads (Settings / Search Console).
 * 3. Authenticated GET /wp-json/wp/v2/users still returns 200.
 * 4. Logged-out GET /wp-json/wp/v2/users is 401 and not a user array.
 * If (1) or (2) fail, deactivate this snippet immediately.
 */

/**
 * True when the REST route is the core users collection or a users sub-route.
 *
 * @param string $route Matched REST route from WP_REST_Request::get_route().
 * @return bool
 */
function kk_767_is_users_rest_route(string $route): bool {
    return (bool) preg_match('#^/wp/v2/users(?:/|$)#', $route);
}

/**
 * Block unauthenticated reads of /wp/v2/users without touching other routes.
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

    $method = strtoupper((string) $request->get_method());
    if (!in_array($method, array('GET', 'HEAD'), true)) {
        return $result;
    }

    if (is_user_logged_in()) {
        return $result;
    }

    return new WP_Error(
        'rest_cannot_access_users',
        'The users endpoint is not available to unauthenticated requests.',
        array('status' => 401)
    );
}
add_filter('rest_pre_dispatch', 'kk_767_restrict_unauthenticated_users_rest', 10, 3);
