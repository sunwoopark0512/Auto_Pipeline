export default {
  async fetch(req, env) {
    const { searchParams } = new URL(req.url);
    const uid = searchParams.get("user_id");
    const resp = await fetch(`https://dax-endpoint.aws/feast/${uid}`);
    return new Response(await resp.arrayBuffer(), { headers: {"Content-Type":"application/grpc-web"}});
  }
}
