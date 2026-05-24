<?php
/**
 * Title: Utility Component System
 * Slug: kk-aurora/component-utility-system
 * Categories: kk-aurora, kk-aurora-cta
 * Keywords: search, newsletter, form, utility
 * Viewport Width: 1200
 */
?>
<!-- wp:group {"className":"aurora-utility-grid","layout":{"type":"constrained","contentSize":"1200px"}} -->
<div class="wp-block-group aurora-utility-grid">
  <!-- wp:group {"className":"aurora-search-utility","layout":{"type":"constrained"}} -->
  <div class="wp-block-group aurora-search-utility">
    <!-- wp:heading {"level":3} -->
    <h3 class="wp-block-heading">Find the signal</h3>
    <!-- /wp:heading -->
    <!-- wp:paragraph -->
    <p>Search projects, talks, field notes, and tools.</p>
    <!-- /wp:paragraph -->
    <!-- wp:search {"label":"Search kriskrug.co","showLabel":true,"placeholder":"Search the archive...","buttonText":"Search","buttonPosition":"button-inside","buttonUseIcon":true,"className":"aurora-search-form"} /-->
  </div>
  <!-- /wp:group -->

  <!-- wp:html -->
  <section class="aurora-newsletter-utility" aria-label="Newsletter">
    <p class="aurora-kicker">Newsletter</p>
    <h3>Get the useful weird stuff.</h3>
    <p>AI field notes, community signal, creative tools, and culture-first operating notes.</p>
    <a class="aurora-button aurora-button-primary" href="https://kriskrug.beehiiv.com/">Join the newsletter</a>
    <p class="aurora-form-message">Opens the Beehiiv signup.</p>
  </section>
  <!-- /wp:html -->

  <!-- wp:html -->
  <form class="aurora-form" action="/contact/" method="get">
    <div class="aurora-form-row">
      <label for="aurora-component-intent">What should we talk about?</label>
      <select id="aurora-component-intent" name="topic">
        <option value="keynote">Book a keynote</option>
        <option value="workshop">Plan a workshop</option>
        <option value="training">Build a training program</option>
        <option value="media">Media or podcast appearance</option>
      </select>
    </div>
    <button class="aurora-button aurora-button-primary" type="submit">Open contact path</button>
    <p class="aurora-form-message">Routes your intent to the contact page.</p>
  </form>
  <!-- /wp:html -->
</div>
<!-- /wp:group -->
