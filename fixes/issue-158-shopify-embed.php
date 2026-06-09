<?php
/**
 * Issue #158: Shopify Buy Button embed for the kriskrug.co Shop page.
 *
 * What it does:
 * Loads the Shopify BuyButton.js Storefront SDK and mounts one product
 * component per ID into the `#kk-shop` container rendered by the
 * `kk-aurora/shop-buy-button` Gutenberg pattern. Config (domain, token,
 * product IDs) is single-sourced from `window.kkShop`, which the pattern
 * emits — so KK fills the placeholders in ONE place (the page), not here.
 * This snippet only runs the wiring.
 *
 * Placeholders to replace (in the pattern, via window.kkShop):
 *   SHOPIFY_DOMAIN    -> Store A domain, e.g. kriskrug.myshopify.com
 *   STOREFRONT_TOKEN  -> publishable Storefront access token (public by design;
 *                        BuyButton.js is client-side — never an Admin API key)
 *   PRODUCT_ID_1...   -> numeric Shopify product IDs in the `kriskrug` collection
 *
 * Graceful no-op: if `#kk-shop` is absent, or any value is still a literal
 * placeholder / empty, the init script does nothing and the pattern's
 * "Shop opening soon" fallback stays visible. No console errors, no half-mount.
 *
 * How to install:
 * Add this file as a Code Snippets (Pro) PHP snippet set to run "only on the
 * front end", or drop it in `wp-content/mu-plugins/` as a must-use plugin.
 * It enqueues only on the page whose slug matches KK_ISSUE_158_SHOP_SLUG, so it
 * adds nothing to the rest of the site. After the /shop page is published, set
 * KK_ISSUE_158_SHOP_SLUG to its slug if it differs from `shop`.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'KK_ISSUE_158_SHOP_SLUG', 'shop' );
define( 'KK_ISSUE_158_SDK_HANDLE', 'shopify-buy-button-storefront' );
define( 'KK_ISSUE_158_SDK_SRC', 'https://sdks.shopifycdn.com/buy-button/latest/buy-button-storefront.min.js' );

add_action( 'wp_enqueue_scripts', 'kk_issue_158_enqueue_shop_embed' );

function kk_issue_158_enqueue_shop_embed() {
	if ( ! kk_issue_158_is_shop_surface() ) {
		return;
	}

	wp_enqueue_script(
		KK_ISSUE_158_SDK_HANDLE,
		KK_ISSUE_158_SDK_SRC,
		[],
		null,
		true
	);

	wp_add_inline_script( KK_ISSUE_158_SDK_HANDLE, kk_issue_158_init_script() );
}

function kk_issue_158_is_shop_surface() {
	return is_page( KK_ISSUE_158_SHOP_SLUG );
}

function kk_issue_158_init_script() {
	return <<<'JS'
(function () {
	var node = document.getElementById('kk-shop');
	var cfg = window.kkShop || {};
	var ids = Array.isArray(cfg.productIds) ? cfg.productIds : [];

	function unset(value) {
		return !value || /^(SHOPIFY_DOMAIN|STOREFRONT_TOKEN|PRODUCT_ID_)/.test(value);
	}

	var ready = ids.filter(function (id) { return !unset(id); });

	if (!node || unset(cfg.domain) || unset(cfg.storefrontAccessToken) || !ready.length) {
		return;
	}

	var options = {
		product: {
			buttonDestination: 'cart',
			contents: { img: true, title: true, price: true, options: true },
			text: { button: 'Add to cart' },
			styles: {
				product: { 'max-width': '100%', 'margin-bottom': '1.5rem' },
				button: {
					'background-color': '#111418',
					color: '#f5f5f4',
					'border-radius': '0.375rem',
					'font-weight': '600',
					':hover': { 'background-color': '#2a2f37' },
					':focus': { 'background-color': '#2a2f37' }
				}
			}
		},
		cart: {
			text: { title: 'Cart', total: 'Subtotal', button: 'Checkout' },
			styles: {
				button: {
					'background-color': '#111418',
					color: '#f5f5f4',
					':hover': { 'background-color': '#2a2f37' },
					':focus': { 'background-color': '#2a2f37' }
				}
			}
		},
		toggle: {
			styles: {
				toggle: {
					'background-color': '#111418',
					':hover': { 'background-color': '#2a2f37' },
					':focus': { 'background-color': '#2a2f37' }
				}
			}
		}
	};

	function mount() {
		var client = window.ShopifyBuy.buildClient({
			domain: cfg.domain,
			storefrontAccessToken: cfg.storefrontAccessToken
		});
		window.ShopifyBuy.UI.onReady(client).then(function (ui) {
			node.innerHTML = '';
			ready.forEach(function (id) {
				ui.createComponent('product', {
					id: id,
					node: node,
					moneyFormat: '%24%7B%7Bamount%7D%7D',
					options: options
				});
			});
		});
	}

	if (window.ShopifyBuy && window.ShopifyBuy.UI) {
		mount();
	} else {
		var poll = setInterval(function () {
			if (window.ShopifyBuy && window.ShopifyBuy.UI) {
				clearInterval(poll);
				mount();
			}
		}, 100);
	}
})();
JS;
}
