SELECT variant, SUM(conversions)::float / NULLIF(SUM(views),0) AS ctr
FROM ab_test_queue
GROUP BY variant ORDER BY ctr DESC;
