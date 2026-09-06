(function () {
  'use strict';
  var root = document.querySelector('.kk-practice');
  if (!root) return;
  var fields = Array.from(root.querySelectorAll('.kk-practice-field textarea'));
  var output = root.querySelector('.kk-practice-output');
  var result = root.querySelector('#kk-practice-result');
  var status = root.querySelector('.kk-practice-status');
  var actions = root.querySelectorAll('[data-action]');
  var headings = ['Objective', 'Audience', 'Available sources and missing context', 'Observable success conditions', 'Privacy boundaries and exclusions', 'Human reviewer and required checks'];
  var missing = 'Not provided. Resolve before relying on this brief.';
  var source = 'https://kriskrug.co/2026/09/03/what-i-showed-founders-about-ai-workflows/';
  var lastAnswers = null;
  var printText = root.querySelector('.kk-practice-print');
  function length(value) { return Array.from(value).length; }
  function total() { return fields.reduce(function (count, field) { return count + length(field.value); }, 0); }
  function announce(message) { status.textContent = message; }
  function check() {
    var count = total();
    var over = count > 8000;
    root.querySelector('#kk-practice-limit').textContent = count.toLocaleString() + ' of 8,000 characters total. Nothing is silently removed.';
    fields.forEach(function (field) { field.setAttribute('aria-invalid', String(over)); });
    root.querySelector('[data-action="preview"]').disabled = over;
    if (over) announce('Your answers exceed 8,000 characters. Shorten them before previewing. All your text is still here.');
    else announce('');
    return !over;
  }
  fields.forEach(function (field) { field.disabled = false; field.addEventListener('input', check); });
  root.querySelector('.kk-practice-nojs').hidden = true;
  root.querySelector('.kk-practice-start').hidden = false;
  root.querySelector('.kk-practice-start').addEventListener('click', function () { fields[0].focus(); });
  root.querySelector('.kk-practice-work .kk-practice-actions').hidden = false;
  function preview() {
    if (!check()) return;
    var answers = fields.map(function (field) { return field.value; });
    var serialized = JSON.stringify(answers);
    if (serialized !== lastAnswers) {
      result.value = '# My work brief\n\n' + answers.map(function (answer, index) {
        return '## ' + (index + 1) + '. ' + headings[index] + '\n\n' + (answer.trim() || missing);
      }).join('\n\n') + '\n\n---\n\nContext brief · Method version 0.1-draft.\n\nInspired by [Kris Krüg\'s North House recap](' + source + '). These six questions are a newly authored exercise, not a transcript of the workshop. An unfinished brief is a draft, not permission to act. No email signup is needed.\n';
      lastAnswers = serialized;
    }
    output.hidden = false;
    root.querySelector('#kk-practice-output-title').focus();
    announce(answers.some(function (answer) { return !answer.trim(); }) ? 'Your draft has unanswered questions. You can still save it. Missing answers stay marked.' : 'Your brief is ready to review.');
  }
  function validOutput() {
    if (length(result.value) > 10000) {
      announce('Your edited brief exceeds 10,000 characters including headings. Shorten it before export. All your text is still here.');
      result.focus();
      return false;
    }
    return true;
  }
  actions.forEach(function (button) {
    button.addEventListener('click', async function () {
      var action = button.dataset.action;
      if (action === 'preview') preview();
      if (action === 'edit') fields[0].focus();
      if (action === 'clear' && window.confirm('Clear all six answers? Save a copy first if you want to keep them.')) {
        fields.forEach(function (field) { field.value = ''; });
        result.value = ''; lastAnswers = null; output.hidden = true; check(); fields[0].focus();
      }
      if (['copy', 'download', 'print'].includes(action) && !validOutput()) return;
      if (action === 'copy') {
        try { await navigator.clipboard.writeText(result.value); announce('Brief copied.'); }
        catch (_) { result.focus(); result.select(); announce('Copy did not work. Select the text below and copy it, or download your brief.'); }
      }
      if (action === 'download') {
        var url = URL.createObjectURL(new Blob([result.value], { type: 'text/markdown;charset=utf-8' }));
        var link = document.createElement('a'); link.href = url; link.download = 'my-work-brief.md';
        link.click(); window.setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
        announce('Markdown download requested.');
      }
      if (action === 'print') {
        printText.textContent = result.value; root.classList.add('kk-practice-printing');
        window.print(); root.classList.remove('kk-practice-printing');
      }
    });
  });
  check();
})();
