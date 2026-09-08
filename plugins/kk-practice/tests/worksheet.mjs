import vm from 'node:vm';
import {readFileSync} from 'node:fs';
const escape = value => String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
export function savedWorksheet() {
  let definition;
  const wp = {blocks: {registerBlockType: (_, value) => { definition = value; }}, element: {createElement: (tag, props, ...children) => ({tag, props, children})}};
  const copy = JSON.parse(readFileSync(new URL('../blocks/context-brief/copy.json', import.meta.url)));
  vm.runInNewContext(readFileSync(new URL('../blocks/context-brief/editor.js', import.meta.url), 'utf8'), {window: {wp, KKPracticeCopy: copy}});
  function render(node) {
    if (Array.isArray(node)) return node.map(render).join('');
    if (typeof node !== 'object') return escape(node);
    const attributes = Object.entries(node.props || {}).filter(([key]) => key !== 'key').map(([key, value]) => ' ' + (key === 'className' ? 'class' : key) + '="' + escape(value) + '"').join('');
    return '<' + node.tag + attributes + '>' + node.children.map(render).join('') + '</' + node.tag + '>';
  }
  return render(definition.save());
}
