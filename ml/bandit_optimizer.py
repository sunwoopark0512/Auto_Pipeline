"""Thompson-sampling based variant selection utilities."""

try:
    from db_utils import get_conn
except ImportError:  # pragma: no cover - optional dependency
    get_conn = None
import numpy as np
import pandas as pd


def choose_variant(content_id: int) -> str:
    """Return the best variant using Thompson Sampling."""
    if get_conn is None:
        raise ImportError("db_utils is required for choose_variant")

    with get_conn() as conn:
        df = pd.read_sql(
            """
          SELECT variant, views, conversions
          FROM ab_test_queue
          WHERE content_id=%s
        """,
            conn,
            params=(content_id,),
        )
    alpha = 1 + df["conversions"]
    beta = 1 + df["views"] - df["conversions"]
    theta = np.random.beta(alpha, beta)
    return df.loc[theta.idxmax(), "variant"]
