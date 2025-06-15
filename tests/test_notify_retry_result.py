import os
import json
import tempfile
import importlib
import unittest


class TestNotifyRetryResult(unittest.TestCase):
    def test_notify_reads_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "reparsed.json")
            data = [{"keyword": "a"}, {"keyword": "b", "retry_error": "err"}]
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f)

            os.environ["REPARSED_OUTPUT_PATH"] = path

            mod = importlib.import_module("scripts.notify_retry_result")
            importlib.reload(mod)
            count = mod.notify()
            self.assertEqual(count, 2)


if __name__ == "__main__":
    unittest.main()
