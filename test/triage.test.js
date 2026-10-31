import test from 'node:test';
import assert from 'node:assert/strict';
import { triage } from '../src/editorial/triage.js';

test('clasifica denuncia sin publicarla', () => {
  const r = triage({ message: 'Presento una denuncia por presuntas irregularidades.' });
  assert.equal(r.category, 'denuncia');
  assert.equal(r.autoPublish, false);
  assert.equal(r.verified, false);
  assert.equal(r.publicationApproved, false);
});

test('clasifica solicitud comercial', () => {
  assert.equal(triage({ message: 'Solicito tarifas de publicidad.' }).category, 'publicidad');
});

test('clasifica noticia', () => {
  assert.equal(triage({ message: 'Noticia sobre incendio.' }).category, 'noticia');
});

test('consulta simple', () => {
  assert.equal(triage({ message: 'Hola, buenas tardes.' }).category, 'consulta');
});

test('ambiguedad va a revision manual', () => {
  const r = triage({ message: 'Tengo una denuncia y deseo publicidad.' });
  assert.equal(r.category, 'revision_manual');
  assert.equal(r.ambiguous, true);
});

test('texto vacio va a revision manual', () => {
  assert.equal(triage({ message: '' }).category, 'revision_manual');
});

test('recorta longitud y no acepta canal arbitrario', () => {
  const r = triage({ message: 'x'.repeat(15000), channel: 'admin' });
  assert.equal(r.message.length, 10000);
  assert.equal(r.channel, 'manual');
});
