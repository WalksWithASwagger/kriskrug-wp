const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.resolve(__dirname, '../..');
const source = fs.readFileSync(path.join(root, 'fixes/issue-1090-krug-signup-tag.js'), 'utf8');
const container = JSON.parse(fs.readFileSync(path.join(root, 'fixes/issue-1090-krug-signup-gtm.json'), 'utf8')).containerVersion;
const tag = container.tag[0];
const trigger = container.trigger[0];
const html = tag.parameter.find(p => p.key === 'html').value;
assert.equal(html, '<script>\n' + source + '</script>');
assert.equal(tag.tagFiringOption, 'ONCE_PER_LOAD');
assert.equal(trigger.type, 'CUSTOM_EVENT');
assert.equal(tag.firingTriggerId[0], trigger.triggerId);
const allowed = encodeURIComponent(JSON.stringify({ marketing: true, dataProcessing: true }));

function fixture({ host = 'vancouver.beehiiv.com', route = '/subscribe', cookie = 'beehiiv_honey=' + allowed } = {}) {
  const scripts = [];
  const window = { location: { hostname: host, pathname: route }, dataLayer: [] };
  const document = {
    cookie,
    referrer: 'https://kriskrug.co/subscribe/?email=private@example.test#private',
    createElement: type => ({ type }),
    head: { appendChild: script => scripts.push(script) }
  };
  const context = vm.createContext({
    window, document, URL,
    Date: class extends Date {
      constructor(...args) {
        super(...(args.length ? args : ['2026-10-26T04:36:09.699Z']));
      }
    }
  });
  function matches(condition, event) {
    assert.equal(condition.type, 'EQUALS');
    const values = Object.fromEntries(condition.parameter.map(p => [p.key, p.value]));
    const actual = { '{{_event}}': event, '{{Page Hostname}}': host }[values.arg0];
    return actual === values.arg1;
  }
  return {
    window, document, scripts,
    deliver(event, eventProps = {}) {
      window.dataLayer.push({ event, eventProps });
      if ([...trigger.customEventFilter, ...trigger.filter].every(c => matches(c, event))) {
        vm.runInContext(source, context);
      }
    },
    commands: () => window.dataLayer.filter(x => !x.event).map(x => Array.from(x)),
    events: () => window.dataLayer.filter(x => x[0] === 'event').map(x => Array.from(x))
  };
}

const page = fixture();
assert.equal(page.events().length, 0);
for (const event of ['gtm.js', 'page_view', 'click', 'form_submit', 'error', 'alreadySubscribed', 'signedIn', 'signedup']) page.deliver(event);
assert.equal(page.events().length, 0);
assert.equal(page.scripts.length, 0);

const sensitive = { email: 'private@example.test', name: 'Private Person', label: 'https://vancouver.beehiiv.com/?email=private@example.test', value: 99, subscription_id: 'private-id' };
page.deliver('signedUp', sensitive);
page.deliver('signedUp', sensitive);
assert.equal(page.events().length, 1);
assert.equal(page.scripts.length, 1);
assert.equal(page.scripts[0].src, 'https://www.googletagmanager.com/gtag/js?id=G-ZPQP315FNS');
const event = page.events()[0];
assert.equal(event[1], 'krug_newsletter_signup');
assert.equal(event[2].send_to, 'G-ZPQP315FNS');
assert.equal(event[2].page_location, 'https://vancouver.beehiiv.com/subscribe');
assert.equal(event[2].page_referrer, 'https://kriskrug.co/');
assert.equal(page.commands().find(x => x[0] === 'config')[2].send_page_view, false);
assert.equal(page.commands().find(x => x[0] === 'consent')[2].ad_user_data, 'denied');
const serializedCommands = JSON.stringify(page.commands());
assert.doesNotMatch(serializedCommands, /private|email|subscription_id|Private Person/);
assert.doesNotMatch(serializedCommands, /(?:[:,\[])99(?=[,}\]])/);

for (const options of [
  { host: 'kriskrug.beehiiv.com' },
  { host: 'kriskrug.co' },
  { route: '/thanks' },
  { route: '/p/article' },
  { cookie: '' },
  { cookie: 'beehiiv_honey=broken%' },
  { cookie: 'beehiiv_honey=null' },
  { cookie: 'beehiiv_honey=' + encodeURIComponent(JSON.stringify({ marketing: false, dataProcessing: true })) },
  { cookie: 'beehiiv_honey=' + encodeURIComponent(JSON.stringify({ marketing: true, dataProcessing: false })) },
  { cookie: 'beehiiv_honey=' + encodeURIComponent(JSON.stringify({ marketing: 'true', dataProcessing: true })) }
]) {
  const blocked = fixture(options);
  blocked.deliver('signedUp', sensitive);
  assert.equal(blocked.events().length, 0, JSON.stringify(options));
  assert.equal(blocked.scripts.length, 0, JSON.stringify(options));
}

const direct = fixture({ route: '/' });
direct.document.referrer = '';
direct.deliver('signedUp');
assert.equal(direct.events().length, 1);
assert.equal(direct.events()[0][2].page_referrer, '');
console.log('issue_1090_krug_signup_harness: ok; success-only, consent, deduplication, host and PII boundaries');
