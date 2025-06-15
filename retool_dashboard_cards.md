| 카드 | 쿼리 |
| --- | --- |
| Revenue by Channel | `SELECT platform, SUM(revenue_cents)/100 AS revenue FROM conversion_log GROUP BY platform` |
| Weekly Retention | `SELECT * FROM storage.public.cohort_retention.csv` |
| Current CPU Load | Render Metrics API 또는 Prometheus Exporter |
