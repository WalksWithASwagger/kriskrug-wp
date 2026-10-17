<?php
/**
 * Behavior smoke for #1131 final-URL chrome.
 *
 * Header, footer, and homepage CTAs must point at the services canonical and
 * the www Futureproof host. Copy is unchanged; this only inspects hrefs.
 *
 * @package KK_Aurora
 */

declare(strict_types=1);

$theme_root = dirname(__DIR__);
$surfaces   = array(
	$theme_root . '/parts/header.html',
	$theme_root . '/parts/footer.html',
	$theme_root . '/templates/front-page.html',
);

$forbidden = array(
	'href="/services/"',
	'href="https://kriskrug.co/services/"',
	'href="http://kriskrug.co/services/"',
	'href="https://futureproof.website/"',
	'href="http://futureproof.website/"',
);

$required_chrome = array(
	$theme_root . '/parts/header.html' => array(
		'href="/generative-ai-services/"',
	),
	$theme_root . '/parts/footer.html' => array(
		'href="/generative-ai-services/"',
		'href="https://www.futureproof.website/"',
	),
	$theme_root . '/templates/front-page.html' => array(
		'href="/generative-ai-services/"',
	),
);

foreach ($surfaces as $path) {
	if (! is_readable($path)) {
		fwrite(STDERR, "FAIL: missing theme surface {$path}\n");
		exit(1);
	}

	$source = file_get_contents($path);
	if (false === $source) {
		fwrite(STDERR, "FAIL: could not read {$path}\n");
		exit(1);
	}

	foreach ($forbidden as $needle) {
		if (str_contains($source, $needle)) {
			fwrite(STDERR, "FAIL: {$path} still contains {$needle}\n");
			exit(1);
		}
	}

	foreach ($required_chrome[$path] as $needle) {
		if (! str_contains($source, $needle)) {
			fwrite(STDERR, "FAIL: {$path} is missing {$needle}\n");
			exit(1);
		}
	}
}

echo "Aurora final-URL smoke passed.\n";
