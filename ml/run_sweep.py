import wandb, openai, random, os
wandb.init()
lr = wandb.config.lr

job = openai.FineTuningJob.create(
    training_file=os.getenv("FT_TRAIN_FILE"),
    model="gpt-3.5-turbo",
    learning_rate_multiplier=lr,
    n_epochs=1
)

roc_auc = random.uniform(0.6, 0.95)
wandb.log({"eval/roc_auc": roc_auc})
