import wasm from 'feature.wasm';
const { instance } = await WebAssembly.instantiate(wasm);

export default {
  async fetch(req) {
    const userid = new URL(req.url).searchParams.get("user_id");
    const reqBuf = new TextEncoder().encode(JSON.stringify({user_id: userid}));
    const p = instance.exports.allocate(reqBuf.length);
    new Uint8Array(instance.exports.memory.buffer, p, reqBuf.length).set(reqBuf);
    const [outPtr, outLen] = instance.exports.handle(p, reqBuf.length);
    const out = new Uint8Array(instance.exports.memory.buffer, outPtr, outLen);
    return new Response(out, { headers: {"Content-Type":"application/json"}});
  }
}

