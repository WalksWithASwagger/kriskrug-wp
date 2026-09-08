import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {gzipSync} from 'node:zlib';
import {savedWorksheet} from './worksheet.mjs';
const copy = JSON.parse(readFileSync(new URL('../blocks/context-brief/copy.json', import.meta.url)));
const packet = readFileSync(new URL('../../../content/drafts/open-studio-context-brief/copy.md', import.meta.url), 'utf8');
assert.equal(copy.fields.length, 6);
assert.equal(copy.examples.length, 6);
for (const field of copy.fields) { assert.ok(packet.includes(field.title)); assert.ok(packet.includes(field.help)); }
for (const text of [...copy.examples, ...copy.intro, ...copy.before, copy.disclosure]) assert.ok(packet.includes(text));
const fallback = savedWorksheet();
assert.equal((fallback.match(/Not provided/g) || []).length, 6);
assert.ok(fallback.includes('Use the worksheet below'));
const bytes = ['view.js', 'style.css'].reduce((sum, file) => sum + gzipSync(readFileSync(new URL('../blocks/context-brief/' + file, import.meta.url))).length, 0);
assert.ok(bytes <= 20000, 'Incremental compressed JS/CSS must stay below20KB');
console.log(JSON.stringify({approvedCopy: true, savedEditorWorksheet: true, compressedFrontendBytes: bytes}));
