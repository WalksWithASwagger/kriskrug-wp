<?php
/**
 * Title: Shop Buy Button
 * Slug: kk-aurora/shop-buy-button
 * Categories: kk-aurora
 * Keywords: shop, store, shopify, buy button, merch
 * Viewport Width: 1100
 */
?>
<!-- wp:group {"tagName":"section","layout":{"type":"constrained","contentSize":"900px"},"style":{"spacing":{"padding":{"top":"var:preset|spacing|120","bottom":"var:preset|spacing|120"}}}} -->
<section class="wp-block-group" style="padding-top:var(--wp--preset--spacing--120);padding-bottom:var(--wp--preset--spacing--120)">
  <!-- wp:heading {"level":2,"className":"aurora-shop-heading","style":{"typography":{"fontSize":"clamp(2rem, 5vw, 3rem)","fontWeight":"700","lineHeight":"1.1"}}} -->
  <h2 class="wp-block-heading aurora-shop-heading" style="font-size:clamp(2rem, 5vw, 3rem);font-weight:700;line-height:1.1">Shop</h2>
  <!-- /wp:heading -->

  <!-- wp:paragraph {"className":"aurora-shop-intro","style":{"spacing":{"margin":{"top":"var:preset|spacing|40"}}},"textColor":"text-secondary","fontSize":"lg"} -->
  <p class="aurora-shop-intro has-text-secondary-color has-text-color has-lg-font-size" style="margin-top:var(--wp--preset--spacing--40)">A small, evolving collection of prints, merch, and experiments. Checkout is handled securely by Shopify.</p>
  <!-- /wp:paragraph -->

  <!-- wp:html -->
  <div id="kk-shop" class="aurora-shop-mount" style="margin-top:2.5rem;">
    <p class="aurora-shop-fallback" style="font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.18em;color:#6b7280;">Shop opening soon</p>
  </div>
  <!--
    Shop config for the kriskrug.co Store A `kriskrug` collection.
    BuyButton.js runs client-side, so the Storefront token is public by design
    (publishable Storefront access token only — never an Admin API key).

    The companion snippet `fixes/issue-158-shopify-embed.php` reads window.kkShop,
    loads the Shopify SDK, and mounts the listed products into #kk-shop. Replace
    the PLACEHOLDER strings below with Store A's real values. While any value is
    still a literal placeholder, the snippet no-ops and the fallback stays visible.
  -->
  <script>
    window.kkShop = window.kkShop || {
      domain: 'SHOPIFY_DOMAIN',
      storefrontAccessToken: 'STOREFRONT_TOKEN',
      collection: 'kriskrug',
      productIds: ['PRODUCT_ID_1', 'PRODUCT_ID_2', 'PRODUCT_ID_3']
    };
  </script>
  <!-- /wp:html -->
</section>
<!-- /wp:group -->
