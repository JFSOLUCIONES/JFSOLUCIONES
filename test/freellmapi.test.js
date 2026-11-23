import test from 'node:test';
import assert from 'node:assert/strict';
import { runSyntheticProbe, validateLabBaseUrl } from '../src/labs/freellmapi-contract.js';

test('solo acepta puerto local 3001', () => {
  assert.equal(validateLabBaseUrl('http://127.0.0.1:3001'), 'http://127.0.0.1:3001');
  assert.equal(validateLabBaseUrl('http://localhost:3001'), 'http://localhost:3001');
  for (const unsafe of [
    'https://localhost:3001',
    'http://192.168.1.2:3001',
    'http://example.com:3001',
    'http://localhost:3002',
    'http://user:pass@localhost:3001',
    'http://localhost:3001/other',
  ]) {
    assert.throws(() => validateLabBaseUrl(unsafe), /LAB_LOCAL_ONLY/);
  }
});

test('no permite llamadas sin token', async () => {
  await assert.rejects(runSyntheticProbe({ transport: async () => {} }), /LAB_MISSING_KEY/);
});

test('solicitud sintética y respuesta compatible sin red real', async () => {
  let called = false;
  const result = await runSyntheticProbe({
    apiKey: 'TOKEN_DE_PRUEBA_NO_REAL',
    transport: async (url, options) => {
      called = true;
      assert.equal(url, 'http://127.0.0.1:3001/v1/chat/completions');
      assert.equal(options.method, 'POST');
      assert.equal(options.headers.Authorization, 'Bearer TOKEN_DE_PRUEBA_NO_REAL');
      const body = JSON.parse(options.body);
      assert.deepEqual(body.messages, [
        { role: 'user', content: 'Responde exactamente con el texto PRUEBA_JF_OK.' },
      ]);
      assert.equal(body.model, 'auto');
      assert.equal(body.stream, false);
      return {
        ok: true,
        headers: { get: (name) => name === 'x-routed-via' ? 'mock/model' : null },
        json: async () => ({
          model: 'mock-model',
          choices: [{ message: { content: 'PRUEBA_JF_OK' } }],
        }),
      };
    },
  });
  assert.equal(called, true);
  assert.deepEqual(result, {
    schemaValid: true,
    matchedSyntheticPrompt: true,
    routedVia: 'mock/model',
    model: 'mock-model',
  });
});

test('no refleja texto de error del servidor ni credenciales', async () => {
  await assert.rejects(
    runSyntheticProbe({
      apiKey: 'TOKEN_DE_PRUEBA_NO_REAL',
      transport: async () => ({
        ok: false,
        status: 429,
        text: async () => 'PRIVATE SECRET: TOKEN_DE_PRUEBA_NO_REAL',
      }),
    }),
    (error) => error.message === 'LAB_HTTP_429'
  );
});

test('rechaza respuestas que no cumplen el contrato', async () => {
  await assert.rejects(
    runSyntheticProbe({
      apiKey: 'test',
      transport: async () => ({
        ok: true,
        json: async () => ({ choices: [] }),
      }),
    }),
    /LAB_UNEXPECTED_SCHEMA/
  );
});

test('falla de transporte sin exposición del error original', async () => {
  await assert.rejects(
    runSyntheticProbe({
      apiKey: 'test',
      transport: async () => { throw new Error('secreto en un error upstream'); },
    }),
    (error) => error.message === 'LAB_TRANSPORT_FAILED'
  );
});

test('respuesta válida pero contenido no exacto se detecta', async () => {
  const r = await runSyntheticProbe({
    apiKey: 'test',
    transport: async () => ({
      ok: true,
      headers: { get: () => null },
      json: async () => ({ choices: [{ message: { content: 'respuesta distinta' } }] }),
    }),
  });
  assert.equal(r.schemaValid, true);
  assert.equal(r.matchedSyntheticPrompt, false);
});
