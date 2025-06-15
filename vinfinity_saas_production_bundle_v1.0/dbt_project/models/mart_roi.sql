WITH conv AS (
  SELECT date_trunc('day', occurred_at) AS d,
         SUM(revenue_cents)/100 AS revenue
  FROM {{ ref('fct_conversion') }}
  GROUP BY 1
), spend AS (
  SELECT d, SUM(cost_usd) AS ad_spend
  FROM marketing_spend
  GROUP BY 1
)
SELECT conv.d,
       revenue,
       ad_spend,
       revenue / NULLIF(ad_spend,0) AS ROAS
FROM conv
LEFT JOIN spend USING (d);
