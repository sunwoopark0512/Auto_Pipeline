create or replace view public.kpi_dashboard as
select
  date_trunc('day', published_at) as day,
  channel,
  count(*)                        as posts,
  sum(views)                      as views,
  sum(clicks)                     as clicks,
  round(sum(clicks)::numeric / nullif(sum(views),0), 4) as ctr
from performance_tracker
group by 1, 2
order by 1 desc;
