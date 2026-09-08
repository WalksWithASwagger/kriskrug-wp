<?php
/** Browser-only practice. The saved block content remains the deactivation fallback. */
if ( ! kk_practice_is_page() ) {
	echo wp_kses_post( $content );
	return;
}
$copy = kk_practice_copy();
?>
<div role="region" class="kk-practice" aria-labelledby="kk-practice-title">
	<header>
		<p class="kk-practice-kicker">Try a method · About 10 minutes</p>
		<h2 id="kk-practice-title">Prepare your AI work brief</h2>
		<?php foreach ( $copy['intro'] as $paragraph ) : ?>
			<p><?php echo esc_html( $paragraph ); ?></p>
		<?php endforeach; ?>
		<p><a href="https://kriskrug.co/2026/09/03/what-i-showed-founders-about-ai-workflows/">Read the North House recap</a></p>
		<h3>Before you start</h3>
		<?php foreach ( $copy['before'] as $paragraph ) : ?>
			<p><?php echo esc_html( $paragraph ); ?></p>
		<?php endforeach; ?>
	</header>
	<div class="kk-practice-layout">
		<aside class="kk-practice-example" aria-labelledby="kk-practice-example-title">
			<h3 id="kk-practice-example-title">Teaching example: a neighbourhood photo walk</h3>
			<p><strong>Newly authored, fictional example.</strong> <?php echo esc_html( $copy['disclosure'] ); ?></p>
			<?php foreach ( $copy['fields'] as $index => $field ) : ?>
				<details><summary><?php echo esc_html( $field['title'] ); ?></summary><p><?php echo esc_html( $copy['examples'][ $index ] ); ?></p></details>
			<?php endforeach; ?>
		</aside>
		<div class="kk-practice-work">
			<p class="kk-practice-nojs">Use the worksheet below. Write your answers in a document or print a copy.</p>
			<button class="kk-practice-start" type="button" hidden>Prepare my brief</button>
			<div class="kk-practice-fields">
				<?php foreach ( $copy['fields'] as $index => $field ) : ?>
					<div class="kk-practice-field">
						<label for="kk-practice-<?php echo esc_attr( $index ); ?>"><?php echo esc_html( ( $index + 1 ) . '. ' . $field['title'] ); ?></label>
						<p id="kk-practice-help-<?php echo esc_attr( $index ); ?>"><?php echo esc_html( $field['help'] ); ?></p>
						<textarea id="kk-practice-<?php echo esc_attr( $index ); ?>" rows="4" aria-describedby="kk-practice-help-<?php echo esc_attr( $index ); ?> kk-practice-limit" autocomplete="off" spellcheck="false" disabled></textarea>
					</div>
				<?php endforeach; ?>
			</div>
			<p id="kk-practice-limit">8,000 characters total across all six answers. Nothing is silently removed.</p>
			<p class="kk-practice-status" role="status" aria-live="polite"></p>
			<div class="kk-practice-actions" hidden>
				<button type="button" data-action="preview">Preview my brief</button>
				<button type="button" data-action="clear">Clear my answers</button>
			</div>
		</div>
	</div>
	<section class="kk-practice-output" aria-labelledby="kk-practice-output-title" hidden>
		<h3 id="kk-practice-output-title" tabindex="-1">Read your brief once more</h3>
		<p>Could another person start from this? Check the sources and the gaps before you copy it into another tool. That tool's privacy rules will apply when you share it there.</p>
		<p>Keep the parts you know. Mark the parts you do not. Download a copy of an unfinished draft and add better information in your own document later.</p>
		<label for="kk-practice-result">Your editable brief</label>
		<textarea id="kk-practice-result" rows="20" spellcheck="false" autocomplete="off"></textarea>
		<p>Editing answers after preview replaces these output edits when you preview again.</p>
		<div class="kk-practice-actions">
			<button type="button" data-action="copy">Copy brief</button>
			<button type="button" data-action="download">Download Markdown</button>
			<button type="button" data-action="print">Print brief</button>
			<button type="button" data-action="edit">Back to answers</button>
		</div>
	</section>
	<pre class="kk-practice-print" hidden></pre>
	<footer><p>Context brief · Method version 0.1-draft · Inspired by the <a href="https://kriskrug.co/2026/09/03/what-i-showed-founders-about-ai-workflows/">North House recap</a>.</p><p><a href="https://kriskrug.co/contact/">Contact Kris</a>. Your brief is not attached or sent.</p></footer>
</div>
