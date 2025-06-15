export default {
  async fetch(request, env) {
    const { continent } = request.cf || {};
    const key = `llm:${continent}:${btoa(request.url)}`;
    let cached = await env.LLM_CACHE.get(key);
    if (!cached) {
      const resp = await fetch(request);              // Origin → GPT Proxy
      cached = await resp.text();
      await env.LLM_CACHE.put(key, cached, { expirationTtl: 60 });
    }
    return new Response(cached, { headers: { "Cache-Control": "max-age=60" }});
  }
}
