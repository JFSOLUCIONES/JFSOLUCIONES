// JF SOLUCIONES - Synthetic contract probe. No real client data, no provider key persistence.
const PROMPT = 'Responde exactamente con el texto PRUEBA_JF_OK.';
const LOCAL_HOSTS = new Set(['127.0.0.1', 'localhost', '[::1]']);

export function validateLabBaseUrl(value) {
  let url;
  try {
    url = new URL(value);
  } catch {
    throw new Error('LAB_INVALID_URL');
  }
  if (
    url.protocol !== 'http:' ||
    !LOCAL_HOSTS.has(url.hostname) ||
    url.port !== '3001' ||
    url.pathname !== '/' ||
    url.search !== '' ||
    url.hash !== '' ||
    url.username !== '' ||
    url.password !== ''
  ) {
    throw new Error('LAB_LOCAL_ONLY');
  }
  return url.origin;
}

/**
 * Exercise only the OpenAI-compatible request/response contract with a fixed,
 * synthetic prompt. FreeLLMAPI itself handles routing/failover; this probe does
 * not claim to verify its provider selection or external quota limits.
 *
 * Never use customer content or production credentials with this laboratory.
 */
export async function runSyntheticProbe({
  baseUrl = 'http://127.0.0.1:3001',
  apiKey,
  transport = globalThis.fetch,
} = {}) {
  const origin = validateLabBaseUrl(baseUrl);
  if (typeof apiKey !== 'string' || apiKey.length < 1) {
    throw new Error('LAB_MISSING_KEY');
  }
  if (typeof transport !== 'function') {
    throw new Error('LAB_MISSING_TRANSPORT');
  }

  // No logging of keys, headers or server response bodies on errors.
  let response;
  try {
    response = await transport(origin + '/v1/chat/completions', {
      method: 'POST',
      headers: {
        Authorization: 'Bearer ' + apiKey,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'auto',
        messages: [{ role: 'user', content: PROMPT }],
        max_tokens: 64,
        stream: false,
      }),
      signal: AbortSignal.timeout(10000),
    });
  } catch {
    throw new Error('LAB_TRANSPORT_FAILED');
  }

  if (!response || typeof response.ok !== 'boolean') {
    throw new Error('LAB_INVALID_RESPONSE');
  }
  if (!response.ok) {
    const status = Number(response.status);
    throw new Error('LAB_HTTP_' + (Number.isInteger(status) && status >= 400 && status <= 599 ? status : 'ERROR'));
  }

  let data;
  try {
    data = await response.json();
  } catch {
    throw new Error('LAB_INVALID_JSON');
  }
  const text = data?.choices?.[0]?.message?.content;
  if (typeof text !== 'string') {
    throw new Error('LAB_UNEXPECTED_SCHEMA');
  }
  const routedVia = response.headers?.get?.('x-routed-via') ?? null;
  return {
    schemaValid: true,
    matchedSyntheticPrompt: text.trim() === 'PRUEBA_JF_OK',
    routedVia,
    model: typeof data.model === 'string' ? data.model : null,
    // Deliberately do not return any echoed prompt or response text.
  };
}
