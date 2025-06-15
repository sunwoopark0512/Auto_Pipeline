import unittest
from ops_log_model import OpsLogModel


class TestOpsLogModel(unittest.TestCase):
    def test_build_payload_basic(self):
        payload = OpsLogModel.build_payload(
            log_type="DevOps",
            operator="tester",
            module="module",
            environment="Local",
            task_summary="summary",
            action_details="details",
            database_id="db",
        )
        self.assertEqual(payload["parent"]["database_id"], "db")
        props = payload["properties"]
        self.assertEqual(props["Log Type"]["select"]["name"], "DevOps")
        self.assertEqual(props["Operator"]["title"][0]["text"]["content"], "tester")


if __name__ == "__main__":
    unittest.main()
