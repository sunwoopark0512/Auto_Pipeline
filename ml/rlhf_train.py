import wandb, pandas as pd, torch, trl, openai
from db_utils import get_conn

wandb.init(project="vinfinity-rlhf")
df = pd.read_sql("select trace_id, rating from llm_feedback", get_conn())
# fetch original prompt/response via Phoenix API
prompts, responses, rewards = [], [], []
for _, row in df.iterrows():
    j = requests.get(f"http://phoenix:6006/api/trace/{row.trace_id}").json()
    prompts.append(j["prompt"])
    responses.append(j["completion"])
    rewards.append(row.rating)
dataset = trl.SFTDataset(prompts, responses, rewards)
model = trl.SFTTrainer("gpt-3.5-turbo", dataset).train()
model.save_pretrained("models/rlhf-ft")
wandb.log({"accuracy": model.evaluate(dataset)})
