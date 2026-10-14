/* Paint Arabic emphasis without inserting characters or splitting shaping runs. */
(function () {
  'use strict';
  const colors = '.highlight-text, .hl-text, .hl-bold';
  const boxes = '.highlight-box, .hl-box-inline, .hl-box';
  const arabic = /\p{Script=Arabic}/u;
  const wordChar = /[\p{L}\p{M}\p{N}\u200c\u200d]/u;
  const nativePaint = !!(globalThis.CSS?.highlights && globalThis.Highlight);

  function textNodes(root) {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    const result = [];
    let offset = 0;
    while (walker.nextNode()) {
      const node = walker.currentNode;
      result.push({ node, start: offset, end: offset + node.length });
      offset += node.length;
    }
    return result;
  }

  function fallback(root, ranges) {
    // Older browsers emphasize whole words, never a fragment of a cursive word.
    const text = root.textContent;
    const expanded = ranges.map(([a, b]) => {
      while (a > 0 && wordChar.test(text[a - 1])) a--;
      while (b < text.length && wordChar.test(text[b])) b++;
      return [a, b];
    });
    for (const { node, start } of textNodes(root)) {
      const fragment = document.createDocumentFragment();
      const parts = node.data.match(/\S+|\s+/gu) || [];
      let position = start;
      for (const part of parts) {
        const end = position + part.length;
        const marked = /\S/u.test(part) && expanded.some(([a, b]) => a < end && b > position);
        const child = marked ? document.createElement('span') : document.createTextNode(part);
        if (marked) {
          child.className = 'ata-ar-fallback';
          child.textContent = part;
        }
        fragment.append(child);
        position = end;
      }
      node.replaceWith(fragment);
    }
  }

  function protect(html) {
    if (!arabic.test(html) || !/class=/.test(html)) return html;
    const template = document.createElement('template');
    template.innerHTML = html;
    const root = template.content;
    const nodes = textNodes(root);
    const text = root.textContent;
    const ink = { c: [], b: [] };
    const unwrap = [];
    for (const element of root.querySelectorAll(colors + ', ' + boxes)) {
      const children = nodes.filter(({ node }) => element.contains(node));
      if (!children.length) continue;
      const a = children[0].start;
      const b = children[children.length - 1].end;
      let left = a, right = b;
      while (left > 0 && wordChar.test(text[left - 1])) left--;
      while (right < text.length && wordChar.test(text[right])) right++;
      if (!arabic.test(text.slice(left, right))) continue;

      if (element.matches(boxes) && left === a && right === b) {
        // A box at word boundaries cannot cut a letter or its diacritics.
        element.classList.add('ata-ar-whole-box');
        continue;
      }
      ink[element.matches(colors) ? 'c' : 'b'].push([a, b]);
      unwrap.push(element);
    }
    for (const element of unwrap) element.replaceWith(...element.childNodes);
    root.normalize();
    if (!ink.c.length && !ink.b.length) return template.innerHTML;
    if (!nativePaint) {
      fallback(root, ink.c.concat(ink.b));
      return template.innerHTML;
    }
    const wrapper = document.createElement('span');
    wrapper.className = 'ata-ar-ink';
    wrapper.dataset.ataInk = JSON.stringify(ink);
    wrapper.append(root.cloneNode(true));
    return wrapper.outerHTML;
  }

  function refresh() {
    if (!nativePaint) return;
    const color = new Highlight();
    const box = new Highlight();
    for (const element of document.querySelectorAll('[data-ata-ink]')) {
      const nodes = textNodes(element);
      const ink = JSON.parse(element.dataset.ataInk);
      for (const key of ['c', 'b']) {
        for (const [a, b] of ink[key]) {
          const first = nodes.find(n => n.start <= a && n.end > a);
          const last = nodes.find(n => n.start < b && n.end >= b);
          if (!first || !last) continue;
          const range = new Range();
          range.setStart(first.node, a - first.start);
          range.setEnd(last.node, b - last.start);
          (key === 'c' ? color : box).add(range);
        }
      }
    }
    CSS.highlights.set('ata-color', color);
    CSS.highlights.set('ata-box', box);
  }

  function observe() {
    if (!nativePaint) return;
    let queued = false;
    new MutationObserver(() => {
      if (queued) return;
      queued = true;
      queueMicrotask(() => { queued = false; refresh(); });
    }).observe(document.body, { childList: true, subtree: true, characterData: true });
    refresh();
    window.addEventListener('beforeprint', refresh);
  }
  globalThis.ATAHighlight = { protect, refresh };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', observe);
  else observe();
})();
