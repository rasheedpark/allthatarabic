import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const golden = JSON.parse(readFileSync('tests/arabic-highlight-legacy.json', 'utf8'));
for (const app of ['teacher', 'textbook']) {
  const path = `ata144_${app}/ata144_${app}.html`;
  const source = readFileSync(path, 'utf8');
  for (const match of source.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g)) {
    new vm.Script(match[1], { filename: path });
  }
  assert(source.includes('../assets/arabic-highlight.js?v=20261014'));
  assert(source.includes('protectNewUnitHighlight('));
  const name = app === 'teacher' ? 'parseText' : 'parseInline';
  const parser = s => s.match(new RegExp(`function ${name}\\([^)]*\\) \\{[\\s\\S]*?\\n\\}`))[0];
  const helper = s => s.match(/const _AR_LETTER[\s\S]*?\n}\n(?=function parse)/)[0];
  const scope = source.match(/function newUnitHighlight\(\).*\nfunction protectNewUnitHighlight\(html\).*\n/)[0];
  for (const unit of ['A01', 'A31', 'A35', 'A40']) {
    const current = new Function(`const currentPg='${unit}', state={unit:currentPg};` + scope + helper(source) + parser(source) + `return ${name};`)();
    for (const [text, expected] of Object.entries(golden[app])) {
      assert.equal(current(text), expected, `${app} ${unit} must remain unchanged`);
    }
  }
  console.log(`${path}: syntax and integration passed`);
}
new vm.Script(readFileSync('assets/arabic-highlight.js', 'utf8'));
console.log('Open tests/arabic-highlight.html and ?fallback=1 for browser checks.');
