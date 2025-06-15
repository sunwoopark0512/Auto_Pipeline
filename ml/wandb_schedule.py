import os
import subprocess
import datetime
import wandb
import openai

wandb.login()


def launch_finetune():
    run = wandb.init(project="vinfinity-ft", job_type="train")
    job = openai.FineTuningJob.create(
        training_file=os.getenv("FT_TRAIN_FILE"),
        model="gpt-3.5-turbo",
        hyperparameters={"n_epochs": 1}
    )
    run.log({"job_id": job.id})
    run.finish()


def canary_deploy(model_id):
    # 10% traffic to new model
    subprocess.run([
        "wrangler", "kv:key", "put",
        "MODEL_CANARY", model_id, "--namespace", os.getenv("KV_AB")
    ])


if __name__ == "__main__":
    launch_finetune()
