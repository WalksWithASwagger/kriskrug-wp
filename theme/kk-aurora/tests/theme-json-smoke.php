<?php
/**
 * Static smoke for #1239: every custom template theme.json offers in the
 * editor must ship as a template file, or pages assigned it fall back silently.
 *
 * @package KK_Aurora
 */

declare(strict_types=1);

$theme_root = dirname(__DIR__);
$theme_json = json_decode((string) file_get_contents($theme_root . '/theme.json'), true);

if (! is_array($theme_json)) {
	fwrite(STDERR, "FAIL: theme.json is not valid JSON\n");
	exit(1);
}

foreach ($theme_json['customTemplates'] ?? array() as $template) {
	$name = (string) ($template['name'] ?? '');
	$path = $theme_root . '/templates/' . $name . '.html';

	if ($name === '' || ! is_readable($path)) {
		fwrite(STDERR, "FAIL: theme.json declares custom template '{$name}' with no templates/{$name}.html\n");
		exit(1);
	}
}

echo "Aurora theme.json smoke passed.\n";
