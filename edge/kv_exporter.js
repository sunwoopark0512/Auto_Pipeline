export default {
  async fetch(request, env) {
    const usage = await env.KV_AB.list();
    const body = `vinfinity_kv_objects ${usage.objects.length}\n`;
    return new Response(body, { headers: { "Content-Type": "text/plain" }});
  }
}
