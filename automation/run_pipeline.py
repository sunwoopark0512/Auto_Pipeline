from datetime import datetime
from automation.orchestration import run_workflow, schedule_publication, scheduler
from automation.content_generation import ContentGenerationEngine
from automation.data_hub import DataHub
from automation.deployment import Deployer


data_hub = DataHub()
content_engine = ContentGenerationEngine()
deployer = Deployer(channels=["blog", "newsletter", "social"])

def main():
    run_workflow(data_hub, content_engine, deployer)


if __name__ == "__main__":
    # Schedule next run for demonstration
    schedule_publication(main, datetime.now())
    scheduler.start()
    scheduler._event.wait()  # Keep the scheduler running
