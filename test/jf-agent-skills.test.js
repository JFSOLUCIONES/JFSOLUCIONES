import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { resolve, dirname } from 'node:path';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const specs = [
  ['jf-safe-change', '.agents/skills/jf-safe-change/SKILL.md'],
  ['jf-oss-screen', '.agents/skills/jf-oss-screen/SKILL.md'],
];

test('agent skills have stable names and nonempty descriptions', () => {
  const names = [];
  for (const [expected, path] of specs) {
    const text = readFileSync(resolve(root, path), 'utf8');
    const frontmatter = text.match(/^---\n([\s\S]*?)\n---\n/);
    assert.ok(frontmatter, path + ': missing frontmatter');
    const name = frontmatter[1].match(/^name: (.+)$/m)?.[1];
    const description = frontmatter[1].match(/^description: (.+)$/m)?.[1];
    assert.equal(name, expected);
    assert.ok(description && description.length >= 20, path + ': missing description');
    names.push(name);
  }
  assert.equal(new Set(names).size, specs.length);
});

test('skills require review and never advertise automatic deployment', () => {
  for (const [name, path] of specs) {
    const content = readFileSync(resolve(root, path), 'utf8');
    assert.match(content, /GitHub Actions|CI/);
    assert.match(content, /licencia|licencias/i);
    assert.match(content, /aprobaci[oó]n humana|revisi[oó]n humana/i);
    assert.match(content, /no concede permisos|no permite root/i);
    assert.ok(!/(?:sk-|ghp_|github_pat_)[A-Za-z0-9_-]{12,}/.test(content),
      name + ': potential literal secret');
  }
});
