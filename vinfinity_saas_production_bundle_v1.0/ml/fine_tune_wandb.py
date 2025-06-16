import wandb, openai, os, json
wandb.init(project="vInfinity-ft")

openai.api_key = os.getenv("OPENAI_API_KEY")
train_file = openai.File.create(
    file=open("data/fine_tune.jsonl", "rb"), purpose="fine-tune"
)
job = openai.FineTuningJob.create(
    training_file=train_file.id,
    model="gpt-3.5-turbo",
    hyperparameters={"n_epochs": 3}
)
wandb.log({"job_id": job.id})
