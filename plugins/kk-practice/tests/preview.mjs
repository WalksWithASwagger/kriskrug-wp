import { existsSync, readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import {savedWorksheet} from './worksheet.mjs';
const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const localCLI = path.join(repo, 'node_modules/@wp-playground/cli/index.js');
if (!existsSync(localCLI)) throw new Error('Run npm ci in the repository first; shared parent dependencies are not used.');
const {runCLI} = await import(localCLI);
export async function startPreview(port = 9832) {
  const server = await runCLI({ command: 'server', wp: '7.0.4', php: '8.2', port, workers: 6,
    mount: [
      {hostPath: path.join(repo, 'plugins/kk-practice'), vfsPath: '/wordpress/wp-content/plugins/kk-practice'},
      {hostPath: path.join(repo, 'theme/kk-aurora'), vfsPath: '/wordpress/wp-content/themes/kk-aurora'}
    ],
    blueprint: {steps: [
      {step: 'activatePlugin', pluginPath: 'kk-practice/kk-practice.php'},
      {step: 'activateTheme', themeFolderName: 'kk-aurora'},
      {step: 'setSiteOptions', options: {blogname: 'Open Studio proof', permalink_structure: '/%postname%/'}}
    ]}
  });
  await new Promise((resolve, reject) => server.server.close(error => error ? reject(error) : resolve()));
  await new Promise(resolve => server.server.listen(port, '127.0.0.1', resolve));
  await server.playground.mkdir('/wordpress/wp-content/mu-plugins');
  const snippet = readFileSync(path.join(repo, 'fixes/issue-706-script-diet-snippet.php'), 'utf8');
  await server.playground.writeFile('/wordpress/wp-content/mu-plugins/fixture-script-diet.php', snippet);
  await server.playground.writeFile('/wordpress/wp-content/mu-plugins/fixture-gtag.php', `<?php
add_action('wp_enqueue_scripts', function () { wp_enqueue_script('google_gtagjs', 'https://www.googletagmanager.com/gtag/js?id=G-SYNTHETIC', [], null, false); wp_add_inline_script('google_gtagjs', 'window.fixtureConfig = true;', 'after'); });
add_action('wp_footer', function () { if (isset($_GET['raw_probe'])) { echo '<script>window.rawProbeExecuted = true;</script>'; } });
`);
  const photo = await fetch('https://kriskrug.co/wp-content/uploads/2026/09/kris-krug-north-house-show-and-tell-2026.jpg');
  if (!photo.ok) throw new Error('Approved public photograph unavailable');
  await server.playground.writeFile('/wordpress/north-house.jpg', new Uint8Array(await photo.arrayBuffer()));
  const fixture = await server.playground.run({code: `<?php
require '/wordpress/wp-load.php';
$fallback = base64_decode('${Buffer.from(savedWorksheet()).toString('base64')}');
$practice = wp_insert_post(['post_type'=>'page','post_status'=>'publish','post_title'=>'Prepare your AI work brief','post_name'=>'context-brief','post_content'=>'<!-- wp:image --><figure class="wp-block-image"><img src="/north-house.jpg" alt="Kris Krüg speaking to founders at North House in Vancouver, with the Futureproof Festival speaker page on the screen behind him" /><figcaption>The North House workshop. The photo-walk example below is fictional.</figcaption></figure><!-- /wp:image --><!-- wp:kk/context-brief -->' . $fallback . '<!-- /wp:kk/context-brief -->']);
$control = wp_insert_post(['post_type'=>'page','post_status'=>'publish','post_title'=>'North House source fixture','post_name'=>'source','post_content'=>'<!-- wp:paragraph --><p>At North House, Kris showed a habit: give each project a home and gather the context it needs.</p><!-- /wp:paragraph --><!-- wp:paragraph --><p><a href="/?page_id=' . $practice . '">Prepare my brief</a></p><!-- /wp:paragraph -->']);
$synced = wp_insert_post(['post_type'=>'wp_block','post_status'=>'publish','post_title'=>'Nested practice','post_content'=>'<!-- wp:kk/context-brief -->' . $fallback . '<!-- /wp:kk/context-brief -->']);
$nested = wp_insert_post(['post_type'=>'page','post_status'=>'publish','post_title'=>'Nested fixture','post_content'=>'<!-- wp:block {"ref":' . $synced . '} /-->']);
echo wp_json_encode(['nested'=>$nested,'version'=>get_bloginfo('version'),'practice'=>$practice,'control'=>$control]);
`});
  const ids = JSON.parse(fixture.text);
  if (ids.version !== '7.0.4') throw new Error('Unexpected actual WordPress version: ' + ids.version);
  return {server, ids, url: 'http://127.0.0.1:' + port, close: () => server[Symbol.asyncDispose]()};
}
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const fixture = await startPreview(Number(process.env.PRACTICE_PORT || 9832));
  console.log(JSON.stringify({version: fixture.ids.version, source: fixture.url + '/?page_id=' + fixture.ids.control, practice: fixture.url + '/?page_id=' + fixture.ids.practice}));
  for (const signal of ['SIGINT', 'SIGTERM']) process.once(signal, async () => { await fixture.close(); process.exit(0); });
}
