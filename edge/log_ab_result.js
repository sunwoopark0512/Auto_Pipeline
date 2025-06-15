export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const uid = request.headers.get("CF-Connecting-IP");
    const variant = await env.KV_AB.get(uid) || "A";
    // Supabase Edge Log
    await fetch(env.SUPABASE_EDGE_URL + "/log", {
      method: "POST",
      headers: { "apikey": env.SUPABASE_EDGE_KEY },
      body: JSON.stringify({ uid, variant, path: url.pathname })
    });
    url.pathname = variant === "A" ? "/index-a.html" : "/index-b.html";
    return fetch(url, request);
  }
}
