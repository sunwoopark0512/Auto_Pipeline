import unittest
from unittest import mock
import run_pipeline

class TestPipeline(unittest.TestCase):
    def test_sequence(self):
        self.assertEqual(
            run_pipeline.PIPELINE_SEQUENCE,
            [
                "hook_generator.py",
                "retry_failed_uploads.py",
                "retry_dashboard_notifier.py",
            ],
        )

    def test_run_pipeline_invokes_all_scripts(self):
        calls = []

        def fake_run_script(name):
            calls.append(name)
            return True

        with mock.patch("run_pipeline.run_script", side_effect=fake_run_script):
            run_pipeline.run_pipeline()
        self.assertEqual(calls, run_pipeline.PIPELINE_SEQUENCE)

if __name__ == "__main__":
    unittest.main()
