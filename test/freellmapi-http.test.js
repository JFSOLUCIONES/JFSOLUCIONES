// Exercises actual Node HTTP -> localhost:3001 -> OpenAI-shaped JSON,
// without installing FreeLLMAPI, using provider keys, or reaching external APIs.
import test from 'node:test';
import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { runSyntheticProbe } from '../src/labs/freellmapi-contract.js';

test('contrato HTTP real en loopback + rechazo de redirección y 429', async () => {
  const requests = [];
  let mode = 'ok';
  const server = createServer(async (req, res) => {
    const chunks = [];
    for await (const chunk of req) chunks.push(chunk);
    requests.push({
      method: req.method,
      path: req.url,
      authorization: req.headers.authorization,
      contentType: req.headers['content-type'],
      body: Buffer.concat(chunks).toString('utf8'),
    });

    if (mode === 'redirect') {
      res.writeHead(302, { Location: 'http://example.invalid/should-not-be-called' });
      res.end();
      return;
    }
    if (mode === 'limited') {
      res.writeHead(429, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'limit reached' }));
      return;
    }
    res.writeHead(200, {
      'Content-Type': 'application/json',
      'X-Routed-Via': 'mock/fixture-model',
    });
    res.end(JSON.stringify({
      model: 'mock-fixture',
      choices: [{ message: { content: 'PRUEBA_JF_OK' } }],
    }));
  });
  try {
    await new Promise((resolve, reject) => {
      server.once('error', reject);
      server.listen(3001, '127.0.0.1', resolve);
    });

    const result = await runSyntheticProbe({ apiKey: 'FAKE_FOR_UNIT_TEST_ONLY' });
    assert.deepEqual(result, {
      schemaValid: true,
      matchedSyntheticPrompt: true,
      routedVia: 'mock/fixture-model',
      model: 'mock-fixture',
    });
    assert.equal(requests[0].method, 'POST');
    assert.equal(requests[0].path, '/v1/chat/completions');
    assert.equal(requests[0].authorization, 'Bearer FAKE_FOR_UNIT_TEST_ONLY');
    assert.match(requests[0].contentType, /^application\/json/);
    assert.deepEqual(JSON.parse(requests[0].body), {
      model: 'auto',
      messages: [{ role: 'user', content: 'Responde exactamente con el texto PRUEBA_JF_OK.' }],
      max_tokens: 64,
      stream: false,
    });

    mode = 'limited';
    await assert.rejects(
      runSyntheticProbe({ apiKey: 'FAKE_FOR_UNIT_TEST_ONLY' }),
      (err) => err.message === 'LAB_HTTP_429',
    );

    mode = 'redirect';
    await assert.rejects(
      runSyntheticProbe({ apiKey: 'FAKE_FOR_UNIT_TEST_ONLY' }),
      (err) => err.message === 'LAB_TRANSPORT_FAILED',
    );
  } finally {
    server.closeAllConnections?.();
    if (server.listening) {
      await new Promise((resolve, reject) => server.close((err) => err ? reject(err) : resolve()));
    }
  }
});
