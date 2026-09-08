(function (wp, copy) {
  'use strict';
  var el = wp.element.createElement;
  function worksheet() {
    return el('section', { className: 'kk-practice-worksheet' },
      el('h2', null, 'Prepare your AI work brief'),
      el('p', null, 'Use the worksheet below. Write your answers in a document or print a copy.'),
      copy.fields.map(function (field, index) {
        return el('section', { key: index }, el('h3', null, field.title), el('p', null, field.help),
          el('p', null, 'Not provided. Resolve before relying on this brief.'));
      }),
      el('p', null, 'Context brief · Method version 0.1-draft · Inspired by the North House recap.')
    );
  }
  wp.blocks.registerBlockType('kk/context-brief', {
    edit: function () { return el('div', null, el('p', null, 'The interactive exercise runs on the published page. Visitor answers are never editor attributes.'), worksheet()); },
    save: worksheet
  });
})(window.wp, window.KKPracticeCopy);
