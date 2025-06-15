from airflow.decorators import dag, task
from datetime import datetime
import retrain_logic


@dag(schedule_interval="0 */12 * * *", start_date=datetime(2024, 1, 1), catchup=False)
def self_retraining_loop():
    @task
    def check_drift() -> bool:
        """Return True if model drift exceeds threshold."""
        return retrain_logic.detect_drift() > 0.25

    @task
    def retrain():
        retrain_logic.run_rlhf_train()

    if check_drift():
        retrain()


dag = self_retraining_loop()
