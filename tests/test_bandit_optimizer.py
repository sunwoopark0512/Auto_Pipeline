import sys
import pathlib
import types
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

sys.modules["db_utils"] = types.SimpleNamespace(get_conn=lambda: None)
from ml.bandit_optimizer import choose_variant


def test_choose_variant_selects_highest_theta():
    df = pd.DataFrame({
        "variant": ["A", "B"],
        "views": [100, 100],
        "conversions": [10, 20],
    })

    mock_ctx = MagicMock()
    mock_ctx.__enter__.return_value = MagicMock()
    mock_ctx.__exit__.return_value = False

    with patch("ml.bandit_optimizer.get_conn", return_value=mock_ctx), \
         patch("pandas.read_sql", return_value=df) as read_sql_mock, \
         patch("numpy.random.beta", return_value=pd.Series([0.1, 0.9])):
        variant = choose_variant(1)

    read_sql_mock.assert_called_once()
    assert variant == "B"
