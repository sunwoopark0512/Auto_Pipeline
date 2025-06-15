from airflow.decorators import dag, task
from airflow.models import Variable
from datetime import datetime, timedelta
import requests, openai, wandb

@dag(schedule_interval="0 */6 * * *", start_date=datetime(2025,1,1), catchup=False)
def drift_retrain():
    @task
    def detect_drift():
        drift = requests.get("http://phoenix:6006/api/drift").json()["value"]
        return drift > 0.2

    @task.trigger_rule("all_success")
    def retrain():
        wandb.login()
        openai.api_key = Variable.get("OPENAI_API_KEY")
        openai.FineTuningJob.create(
            training_file=Variable.get("FT_FILE"),
            model="gpt-3.5-turbo",
            hyperparameters={"n_epochs":2}
        )

    retrain(detect_drift())


dag = drift_retrain()
