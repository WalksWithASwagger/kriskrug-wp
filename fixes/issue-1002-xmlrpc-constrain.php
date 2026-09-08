<?php
/**
 * KK XML-RPC constrain — kriskrug.co (#1002)
 *
 * PREP ONLY. Not deployed as of 2026-09-08. Do not paste into Code Snippets
 * without KK approval, a snippets snapshot, and a stated rollback path.
 *
 * Preferred control is a Pagely / WAF deny of /xmlrpc.php. See
 * docs/current-state/XML-RPC-CONSTRAIN-DECISION-2026-09-08.md. Host deny
 * is safer: the request never reaches PHP, and logged-out GET/HEAD can
 * move off 405 so scripts/check_xmlrpc_reachability.sh can PASS.
 *
 * This file is the fallback if KK writes that the host cannot deny the
 * path. It flips xmlrpc_enabled to false. That does not change GET/HEAD
 * 405, so the check script will still FAIL after a snippet-only apply.
 *
 * Inventory (public 2026-09-08 + last authenticated plugin list 2026-08-03):
 * Jetpack core is not a required XML-RPC client. Boost / Protect / CRM
 * stay on REST or local paths. If Jetpack core is later reactivated, do
 * not enable this snippet. Cookie checks do not preserve a Jetpack
 * XML-RPC tunnel; do not "improve" this file with is_user_logged_in().
 *
 * When pasting into Code Snippets: strip the opening <?php tag. Run
 * everywhere, not admin-only — xmlrpc.php is a front-end request.
 *
 * Rollback: deactivate the snippet. Re-run
 * scripts/check_xmlrpc_reachability.sh (expect FAIL / 405 if only this
 * snippet is rolled back and no host deny was applied).
 */

/**
 * Disable XML-RPC while this fallback snippet is active.
 *
 * @param bool $enabled Whether core would leave XML-RPC enabled.
 * @return bool
 */
function kk_1002_disable_xmlrpc( $enabled ): bool {
	unset( $enabled );
	return false;
}
add_filter( 'xmlrpc_enabled', 'kk_1002_disable_xmlrpc' );
