import pandas as pd
from db_utils import get_conn


def compute_weekly_cohorts():
    with get_conn() as conn:
        df = pd.read_sql(
            """
          SELECT user_id, occurred_at::date AS d
          FROM event_log
          WHERE event='login'
        """,
            conn,
        )
    df['signup_week'] = (
        df.groupby('user_id')['d'].transform('min').dt.isocalendar().week
    )
    df['activity_week'] = df['d'].dt.isocalendar().week
    cohort = (
        df.groupby(['signup_week', 'activity_week']).user_id.nunique().unstack(fill_value=0)
    )
    cohort.to_csv("cohort_retention.csv")


if __name__ == "__main__":
    compute_weekly_cohorts()
