export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const uid = request.headers.get("CF-Connecting-IP");
    const variant = await env.KV_AB.get(uid) ||
      (Math.random() < 0.5 ? "A" : "B");
    await env.KV_AB.put(uid, variant, { expirationTtl: 86400 });

    url.pathname = variant === "A" ? "/index-a.html" : "/index-b.html";
    return fetch(url, request);
  }
}
