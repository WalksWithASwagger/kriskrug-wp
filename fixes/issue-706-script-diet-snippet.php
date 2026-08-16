<?php
/**
 * KK Script Diet — kriskrug.co (#706)
 *
 * Delays the Site Kit gtag.js load until the visitor interacts or the browser
 * goes idle after load. Pairs with the Meta Pixel removal, which is a
 * source-level change (deactivate the snippet that prints it) and is NOT done
 * here — see fixes/issue-706-script-diet.md for that half and the apply order.
 *
 * KK ruling on #706 (2026-08-10): drop the Facebook pixel entirely; delay gtag.
 *
 * Measured cost being addressed (docs/current-state/reports/psi-mobile-2026-08-10.md):
 * gtag G-X7JE8B32L7 is 178 KiB transfer, 156 ms main thread, two of the page's
 * four long tasks (115 ms + 67 ms), 72.9 KiB unused, and a 34 ms forced reflow.
 *
 * What injects gtag today, verified against the public homepage on 2026-08-15:
 * Site Kit by Google 1.185.0 enqueues the handle `google_gtagjs`
 * (`<script id="google_gtagjs-js" src="…/gtag/js?id=G-X7JE8B32L7" async>`) with
 * its config attached as `wp_add_inline_script(…, 'after')`
 * (`<script id="google_gtagjs-js-after">`). Jetpack Boost's defer-JS pass then
 * relocates both from `wp_head` to the footer. This snippet works on the
 * enqueue, before Boost sees it, so the relocation is irrelevant.
 *
 * Design notes:
 * - Site Kit stays the source of truth. We re-emit its own inline config
 *   verbatim rather than hand-writing gtag() calls, so linker domains, the
 *   developer_id, and anything Site Kit adds later survive untouched. Nothing
 *   in Site Kit's settings changes, which is also what makes rollback a
 *   one-toggle operation on this snippet.
 * - We only take over when Site Kit actually enqueued gtag for this request.
 *   If Site Kit is excluding the visitor (logged-in exclusion, consent gating),
 *   or if a Site Kit update renames the handle, this snippet does nothing and
 *   gtag behaves exactly as it does today. Failure mode is "no change", never
 *   "analytics silently gone".
 *
 * Deployed via the Code Snippets plugin (front-end scope). This file is the
 * source of truth — keep it in sync if either side is edited.
 *
 * When pasting into Code Snippets: strip the opening <?php tag (Code Snippets
 * wraps the snippet automatically).
 */

/**
 * Shared between the capture pass and the footer loader. Code Snippets
 * evaluates a snippet inside a function body, so this is snippet-local.
 */
$kk_gtag_delay = ['src' => '', 'inline' => '', 'handled' => false];

/**
 * 1. Capture Site Kit's gtag registration, then unhook it.
 *
 * Registered on two actions because Site Kit's enqueue priority is its own
 * business and has moved between releases: `wp_enqueue_scripts` at 999 catches
 * the normal case, `wp_print_scripts` at 100 is the last point before head
 * scripts print. The `handled` flag makes the second pass a no-op.
 */
$kk_gtag_capture = static function () use (&$kk_gtag_delay): void {
    if ($kk_gtag_delay['handled'] || is_admin()) {
        return;
    }
    if (!wp_script_is('google_gtagjs', 'enqueued')) {
        return;
    }

    $scripts    = wp_scripts();
    $registered = $scripts->registered['google_gtagjs'] ?? null;
    if (!$registered || empty($registered->src)) {
        return;
    }

    $after = $scripts->get_data('google_gtagjs', 'after');

    $kk_gtag_delay['src']     = $registered->src;
    $kk_gtag_delay['inline']  = is_array($after) ? trim(implode("\n", array_filter($after))) : '';
    $kk_gtag_delay['handled'] = true;

    wp_dequeue_script('google_gtagjs');
    wp_deregister_script('google_gtagjs');
};
add_action('wp_enqueue_scripts', $kk_gtag_capture, 999);
add_action('wp_print_scripts', $kk_gtag_capture, 100);

/**
 * 2. Print the delayed loader in place of the eager tag.
 *
 * The dataLayer + gtag() shim is installed immediately so any gtag() call
 * elsewhere on the page queues instead of throwing; gtag.js drains that queue
 * when it finally loads. Only the network fetch and Site Kit's config are
 * deferred.
 *
 * Fires on the first real interaction intent (pointerdown / keydown /
 * touchstart / wheel), or no earlier than 3s after the load event. At that
 * point it uses the browser's next idle opportunity, with a 1s ceiling on the
 * idle wait. The delay is measured from `load`, not from parse, so the tag
 * never competes with the page's own critical path.
 */
add_action('wp_footer', static function () use (&$kk_gtag_delay): void {
    if (!$kk_gtag_delay['handled']) {
        return;
    }

    $template = <<<'JS'
(function (w, d) {
	w.dataLayer = w.dataLayer || [];
	if (!w.gtag) {
		w.gtag = function () { w.dataLayer.push(arguments); };
	}

	var events = ['pointerdown', 'keydown', 'touchstart', 'wheel'];
	var opts = { passive: true, capture: true };
	var fired = false;
	var delayTimer = 0;

	function boot() {
		if (fired) { return; }
		fired = true;
		if (delayTimer) {
			w.clearTimeout(delayTimer);
			delayTimer = 0;
		}
		events.forEach(function (name) { w.removeEventListener(name, boot, opts); });

		%2$s

		var s = d.createElement('script');
		s.async = true;
		s.src = %1$s;
		d.head.appendChild(s);
	}

	function scheduleIdleBoot() {
		delayTimer = w.setTimeout(function () {
			delayTimer = 0;
			if (w.requestIdleCallback) {
				w.requestIdleCallback(boot, { timeout: 1000 });
			} else {
				boot();
			}
		}, 3000);
	}

	events.forEach(function (name) { w.addEventListener(name, boot, opts); });

	if (d.readyState === 'complete') {
		scheduleIdleBoot();
	} else {
		w.addEventListener('load', scheduleIdleBoot, { once: true });
	}
})(window, document);
JS;

    $js = sprintf($template, wp_json_encode($kk_gtag_delay['src']), $kk_gtag_delay['inline']);

    wp_print_inline_script_tag($js, ['id' => 'kk-gtag-delayed']);
}, 20);
