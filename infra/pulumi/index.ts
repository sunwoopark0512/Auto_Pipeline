import * as render from "@pulumi/render";
import * as cf from "@pulumi/cloudflare";
import * as aws from "@pulumi/aws";
import * as fs from "fs";

const dash = new render.Service("dashboard", {
  type: "web",
  env: "python",
  repo: "github.com/sunwoopark0512/Auto_Pipeline",
  startCommand: "streamlit run dashboard.py",
});

const kv = new cf.KVNamespace("abkv");
const worker = new cf.WorkerScript("ab-router", {
  content: fs.readFileSync("../edge/ab_router.js", "utf8"),
  kvNamespaceBindings: [{ kvNamespaceId: kv.id, name: "KV_AB" }],
});

const feastTable = new aws.dynamodb.Table("feastOnline", {
  billingMode: "PAY_PER_REQUEST",
  hashKey: "entity_id",
  attributes: [{ name: "entity_id", type: "S" }],
});
