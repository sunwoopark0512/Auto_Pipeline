import os
import json
import tempfile
import importlib
import unittest


class TestParseFailedGPT(unittest.TestCase):
    def test_parse_failed_creates_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            failed_path = os.path.join(tmp, "failed.json")
            output_path = os.path.join(tmp, "out.json")

            sample = [{
                "keyword": "test",
                "generated_text": "후킹 문장1: hi\n블로그 초안: a\nb\nc\n영상 제목: t1\n- t2"
            }]
            with open(failed_path, "w", encoding="utf-8") as f:
                json.dump(sample, f)

            os.environ["FAILED_HOOK_PATH"] = failed_path
            os.environ["REPARSED_OUTPUT_PATH"] = output_path

            mod = importlib.import_module("scripts.parse_failed_gpt")
            importlib.reload(mod)
            result = mod.parse_failed()
            self.assertEqual(len(result), 1)
            self.assertTrue(os.path.exists(output_path))
            with open(output_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIn("parsed", data[0])


if __name__ == "__main__":
    unittest.main()
