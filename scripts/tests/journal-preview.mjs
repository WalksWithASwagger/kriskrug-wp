import {readFileSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const {runCLI} = await import(path.join(repo, 'node_modules/@wp-playground/cli/index.js'));
const sourceFile = process.argv[2];
if (!sourceFile) throw new Error('Pass the GET-only WordPress source snapshot path.');
const source = JSON.parse(readFileSync(sourceFile));
const proofAssets = process.argv[3];
if (!proofAssets) throw new Error('Pass the previously captured public photo directory.');
const port = Number(process.env.JOURNAL_PORT || 8794);
const server = await runCLI({command:'server',wp:'7.0.8',php:'8.2',port,workers:6,
  mount:[{hostPath:path.join(repo,'theme/kk-aurora'),vfsPath:'/wordpress/wp-content/themes/kk-aurora'}],
  blueprint:{steps:[{step:'defineWpConfigConsts',consts:{WP_AUTO_UPDATE_CORE:false,AUTOMATIC_UPDATER_DISABLED:true,DISABLE_WP_CRON:true}},{step:'activateTheme',themeFolderName:'kk-aurora'},{step:'setSiteOptions',options:{blogname:'Kris Krüg · Writing review',permalink_structure:'/%year%/%monthnum%/%day%/%postname%/',posts_per_page:5}}]}
});
await new Promise((resolve,reject)=>server.server.close(e=>e?reject(e):resolve()));
await new Promise(resolve=>server.server.listen(port,'127.0.0.1',resolve));
await server.playground.mkdir('/wordpress/wp-content/uploads/journal-review');
for (const post of source.posts) await server.playground.writeFile('/wordpress/wp-content/uploads/journal-review/'+post.id+'.jpg',readFileSync(path.join(proofAssets,'post-'+post.id+'.jpg')));
await server.playground.writeFile('/wordpress/journal-review.html',readFileSync(path.join(repo,'scripts/tests/journal-review.html')));
await server.playground.writeFile('/wordpress/journal-nojs.html','<!doctype html><title>Article without JavaScript</title><style>body{margin:0}iframe{display:block;border:0;width:100vw;height:100vh}</style><iframe sandbox="allow-same-origin allow-forms" title="Article without JavaScript" src="/2026/11/02/you-cant-rent-a-social-licence/"></iframe>');
await server.playground.writeFile('/tmp/posts.json',JSON.stringify(source.posts));
const result=await server.playground.run({code:`<?php
require '/wordpress/wp-load.php';
wp_set_current_user(1);
wp_delete_post(1,true);
$home=wp_insert_post(['post_type'=>'page','post_status'=>'publish','post_title'=>'Home','post_name'=>'home']);
$blog=wp_insert_post(['post_type'=>'page','post_status'=>'publish','post_title'=>'Writing','post_name'=>'blog']);
update_option('show_on_front','page');update_option('page_on_front',$home);update_option('page_for_posts',$blog);
wp_update_user(['ID'=>1,'display_name'=>'Kris Krüg']);
$ids=[];
foreach(json_decode(file_get_contents('/tmp/posts.json'),true) as $post){
 $categories=[];
 foreach(($post['_embedded']['wp:term'][0]??[]) as $term){
  $exists=term_exists($term['slug'],'category');
  $created=$exists?:wp_insert_term($term['name'],'category',['slug'=>$term['slug']]);
  if(!is_wp_error($created)) $categories[]=(int)$created['term_id'];
 }
 $id=wp_insert_post(wp_slash(['post_type'=>'post','post_status'=>'publish','post_author'=>1,'post_title'=>$post['title']['raw'],'post_name'=>$post['slug'],'post_date'=>$post['date'],'post_content'=>$post['content']['raw'],'post_excerpt'=>$post['excerpt']['raw'],'post_category'=>$categories]));
 if(get_post_field('post_content',$id)!==$post['content']['raw']) throw new Exception('Fixture changed authored content for '.$post['slug']);
 $media=$post['_embedded']['wp:featuredmedia'][0]??null;
 if($media){
  $attachment=wp_insert_attachment(['post_status'=>'inherit','post_mime_type'=>$media['mime_type'],'post_title'=>$media['title']['rendered'],'guid'=>$media['source_url']],'',$id);
  update_post_meta($attachment,'_wp_attached_file','journal-review/'.$post['id'].'.jpg');
  update_post_meta($attachment,'_wp_attachment_image_alt',$media['alt_text']);
  wp_update_attachment_metadata($attachment,['file'=>'journal-review/'.$post['id'].'.jpg','width'=>$media['media_details']['width'],'height'=>$media['media_details']['height'],'sizes'=>[]]);
  set_post_thumbnail($id,$attachment);
 }
 $ids[$post['slug']]=['id'=>$id,'url'=>get_permalink($id)];
}
$edge=wp_insert_post(['post_type'=>'post','post_status'=>'publish','post_title'=>'Review fixture: older post without an image or manual excerpt','post_name'=>'older-post-fixture','post_date'=>'2005-01-01 12:00:00','post_content'=>'<p>This local fixture checks generated excerpts, missing photographs, wide tables, long links and media. It is not a published article.</p><h2>Long links</h2><p><a href="https://example.com/long">https://example.com/a-very-long-unbroken-address-with-enough-characters-to-test-wrapping-on-a-small-phone-screen</a></p><h2>Table</h2><figure class="wp-block-table"><table><caption>Local review fixture</caption><thead><tr><th>Subject</th><th>Observation</th><th>Result</th></tr></thead><tbody><tr><td>Legacy writing</td><td>Descriptions remain visible with no image.</td><td>Review at 320 pixels</td></tr></tbody></table></figure><h2>Code</h2><pre><code>const longLine = "A deliberately long code sample that should scroll within its own box instead of widening the page";</code></pre><blockquote><p>Reading should work even when JavaScript is unavailable.</p></blockquote><details><summary>Additional context</summary><p>Disclosure content stays in the authored order.</p></details>']);
$control=wp_insert_post(['post_type'=>'page','post_status'=>'publish','post_title'=>'Unchanged page control','post_name'=>'page-control','post_content'=>'<p>This page checks the existing page template outside the blog redesign.</p>']);
flush_rewrite_rules();
echo wp_json_encode(['version'=>get_bloginfo('version'),'blog'=>get_permalink($blog),'posts'=>$ids,'edge'=>get_permalink($edge),'control'=>get_permalink($control)]);
`});
console.log(result.text);
for(const signal of ['SIGINT','SIGTERM']) process.once(signal,async()=>{await server[Symbol.asyncDispose]();process.exit(0);});
