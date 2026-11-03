<?php
/**
 * Title: Journal results
 * Slug: kk-aurora/journal-query
 * Inserter: no
 *
 * @package KK_Aurora
 */
?>
<!-- wp:query {"queryId":4,"query":{"perPage":10,"pages":0,"offset":0,"postType":"post","order":"desc","orderBy":"date","author":"","search":"","exclude":[],"sticky":"exclude","inherit":true},"className":"aurora-journal-query"} -->
<div class="wp-block-query aurora-journal-query">
<!-- wp:post-template {"className":"aurora-journal-list","layout":{"type":"default"}} -->
<!-- wp:pattern {"slug":"kk-aurora/journal-entry"} /-->
<!-- /wp:post-template -->
<!-- wp:query-pagination {"className":"aurora-journal-pagination","layout":{"type":"flex","justifyContent":"center"}} -->
<!-- wp:query-pagination-previous {"label":"Newer posts"} /-->
<!-- wp:query-pagination-numbers /-->
<!-- wp:query-pagination-next {"label":"Older posts"} /-->
<!-- /wp:query-pagination -->
<!-- wp:query-no-results -->
<!-- wp:paragraph --><p>No posts found. Try another search or <a href="/blog/">browse the latest writing</a>.</p><!-- /wp:paragraph -->
<!-- /wp:query-no-results -->
</div><!-- /wp:query -->
