import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const html = readFileSync(new URL('../prototipos/no-mas-ui-preview.html', import.meta.url), 'utf8');

test('el prototipo es una maqueta, no una publicación', () => {
  assert.match(html, /No es el portal publicado/);
  assert.match(html, /Sin noticias reales/);
  assert.match(html, /Plantilla sin artículo publicado/);
});
test('HTML accesible con navegación por teclado', () => {
  assert.match(html, /lang="es"/);
  assert.match(html, /href="#contenido">Saltar al contenido/);
  assert.match(html, /<main id="contenido">/);
  assert.match(html, /aria-controls="menu" aria-expanded="false"/);
  assert.match(html, /event\.key==="Escape"/);
  assert.match(html, /:focus-visible/);
});
test('responsive y con reducción de movimiento', () => {
  assert.match(html, /name="viewport"/);
  assert.match(html, /@media\(max-width:960px\)/);
  assert.match(html, /@media\(max-width:700px\)/);
  assert.match(html, /prefers-reduced-motion:reduce/);
});
test('el prototipo no incorpora servicios externos ni datos personales', () => {
  assert.doesNotMatch(html, /<iframe\b/i);
  assert.doesNotMatch(html, /<script\b[^>]*\bsrc=/i);
  assert.doesNotMatch(html, /<link\b[^>]*\bhref="https?:\/\//i);
  assert.doesNotMatch(html, /(?:api[_-]?key|password|authorization)\s*[:=]/i);
});
