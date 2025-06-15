export default {
  async fetch(req, env) {
    const key = new URL(req.url).pathname;
    let val = await env.KV_CACHE.get(key);
    if (!val) {
      val = await env.R2_BUCKET.get(key);             // ❶ R2 cold fetch
      if (val) await env.KV_CACHE.put(key, val.body, { expirationTtl: 60 });
    }
    // PUT 키(60초 넘은 값) → R2
    req.cf?.cacheTtl === 0 && env.R2_BUCKET.put(key, val, { httpMetadata: req.headers });
    return new Response(val);
  }
}
