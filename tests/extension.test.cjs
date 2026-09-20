const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.join(__dirname, '..');

test('hidden and disabled fields can get an icon on focus after becoming available', () => {
  const handlers = {}, timers = [], icons = [];
  const input = {
    tagName: 'INPUT', type: 'password', style: {}, hidden: true,
    attrs: {}, getAttribute(k) { return this.attrs[k]; },
    setAttribute(k, v) { this.attrs[k] = v; },
    getBoundingClientRect() { return { width: this.hidden ? 0 : 200, height: 30 }; },
    offsetTop: 0, offsetLeft: 0, offsetHeight: 30, offsetWidth: 200,
    parentNode: { style: {}, insertBefore(icon) { icons.push(icon); } }
  };
  const document = {
    readyState: 'complete', documentElement: {},
    addEventListener(k, fn) { handlers[k] = fn; },
    querySelectorAll() { return [input]; },
    createElement() { return { style: {}, setAttribute() {}, addEventListener() {} }; }
  };
  const context = {
    document,
    window: { getComputedStyle: () => ({ visibility: 'visible', display: 'block', paddingRight: '0', position: 'static' }), addEventListener() {} },
    chrome: { runtime: { getURL: x => x } },
    setTimeout(fn, delay) { if (delay === 150) timers.push(fn); }, clearTimeout() {},
    MutationObserver: class { observe() {} }
  };
  vm.runInNewContext(fs.readFileSync(path.join(root, 'inline-icon.js'), 'utf8'), context);
  timers.forEach(fn => fn());
  assert.equal(icons.length, 0);
  assert.equal(input.attrs['data-op-inline-icon'], undefined);
  input.hidden = false;
  input.disabled = true;
  handlers.focusin({ target: input });
  assert.equal(icons.length, 0);
  input.disabled = false;
  handlers.focusin({ target: input });
  assert.equal(icons.length, 1);
  handlers.focusin({ target: input });
  assert.equal(icons.length, 1, 'repeated focus must not duplicate icons');
});

test('inline click reports actual handler availability and forwards the sender tab', () => {
  let listener, received;
  const context = { self: {}, chrome: { runtime: { onMessage: { addListener(fn) { listener = fn; } } } }, importScripts() {} };
  vm.runInNewContext(fs.readFileSync(path.join(root, 'background.js'), 'utf8'), context);
  const sender = { tab: { id: 12 } };
  listener({ action: 'op-inline-icon-clicked' }, sender, x => received = x);
  assert.equal(received.success, false);
  let called;
  context.self._opToolbarHandler = tab => called = tab;
  listener({ action: 'op-inline-icon-clicked' }, sender, x => received = x);
  assert.equal(received.success, true);
  assert.equal(called, sender.tab);
  received = undefined;
  listener({ action: 'unrelated' }, sender, x => received = x);
  assert.equal(received, undefined);
});
