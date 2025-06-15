export default {
  async fetch(request, env, ctx) {
    const ip = request.headers.get("CF-Connecting-IP");
    const now = Date.now();
    // 1) 10 req/min 레이트 제한
    const count = (await env.KV_GATE.get(ip)) || 0;
    if (count > 10) return new Response("429 Too Many", {status:429});
    await env.KV_GATE.put(ip, +count + 1, { expirationTtl: 60 });

    // 2) 쿼리 욕설·정책 필터 (edge-regex)
    const prompt = await request.clone().text();
    const banned = /(?:\b(?:kill|nazi|terror)\b)/i;
    if (banned.test(prompt)) return new Response("Content Blocked", {status:403});

    // 3) 통과한 요청만 GPT Proxy로
    return fetch(request);
  }
}
