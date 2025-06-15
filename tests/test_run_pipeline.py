import os
import unittest
from run_pipeline import PIPELINE_SEQUENCE, run_script

class PipelineTestCase(unittest.TestCase):
    def test_scripts_exist(self):
        for script in PIPELINE_SEQUENCE:
            candidates = [os.path.join('scripts', script), script]
            self.assertTrue(any(os.path.exists(p) for p in candidates), f"Missing script {script}")

    def test_run_script_nonexistent(self):
        self.assertFalse(run_script('nonexistent_script.py'))

if __name__ == '__main__':
    unittest.main()
