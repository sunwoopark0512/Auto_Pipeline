import pandas as pd, numpy as np, psycopg2, random
from db_utils import get_conn

def choose_variant(content_id):
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
