import zipfile
import os

MODULE_FILES = [
    "cursor_chunk_doc_gen.py",
    "auto_rewriter.py",
    "qa_tester.py",
    "auto_insight.py",
    "hook_uploader.py",
    "content_formatter.py",
    "snippet_generator.py",
    "podcast_creator.py",
    "graphic_generator.py",
    "ab_variant_manager.py",
    "osmu_analytics.py",
    "pipeline_api.py",
    "orchestrator.py",
    "notion_sync.py",
    "webhook_receiver.py",
    "strategy_optimizer.py",
    "super_scheduler.py",
    "self_healing_monitor.py",
    "run_pipeline.py",
    "pipeline_config.py",
    "zip_package.py",
    "README.md",
    "requirements.txt"
]

TEST_DIR = "tests"
WORKFLOW_DIR = ".github/workflows"
ZIP_NAME = "v-infinity.zip"

def zip_package():
    with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as zipf:
        for f in MODULE_FILES:
            if os.path.exists(f):
                zipf.write(f)
        if os.path.exists(TEST_DIR):
            for dirpath, _, filenames in os.walk(TEST_DIR):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    zipf.write(filepath)
        if os.path.exists(WORKFLOW_DIR):
            for dirpath, _, filenames in os.walk(WORKFLOW_DIR):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    zipf.write(filepath)

    print(f"✅ Created {ZIP_NAME} with all modules, tests, and CI workflows.")


if __name__ == "__main__":
    zip_package()
