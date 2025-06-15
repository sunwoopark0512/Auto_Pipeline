import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from unittest import mock

# Patch psycopg2 before importing module
sys.modules['psycopg2'] = mock.MagicMock()
sys.modules['psycopg2.extras'] = mock.MagicMock()

import rag.rag_tuner as rt


def test_update_vector_feedback_executes_sql(monkeypatch):
    mock_cur = mock.MagicMock()
    mock_conn = mock.MagicMock()
    mock_cur.fetchone.return_value = ([1.0, 2.0],)
    monkeypatch.setattr(rt, "cur", mock_cur)
    monkeypatch.setattr(rt, "conn", mock_conn)
    rt.update_vector_feedback(1, 0.5)
    mock_cur.execute.assert_any_call("SELECT embedding FROM rag_store WHERE id=%s", (1,))
    mock_cur.execute.assert_any_call(
        "UPDATE rag_store SET embedding=%s WHERE id=%s", mock.ANY
    )
    mock_conn.commit.assert_called_once()
