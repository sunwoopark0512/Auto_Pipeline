-- View definitions for Retool/Metabase dashboard
-- 1. 콘텐츠 상태 요약
create or replace view view__content_status as
select
    id,
    title,
    published_channel,
    public_url,
    published_at,
    podcast_generated,
    graphic_generated,
    ab_test_ready,
    published
from content
order by published_at desc;

-- 2. 채널별 KPI 성과 요약
create or replace view view__channel_performance as
select
    published_channel,
    count(*) as total_posts,
    avg(youtube_views) as avg_yt,
    avg(medium_reads) as avg_md,
    avg(x_engagement) as avg_x,
    avg(tistory_views) as avg_ts
from content
where published_at > now() - interval '30 days'
group by published_channel
order by total_posts desc;

-- 3. A/B 테스트 현황
create or replace view view__ab_test_status as
select
    id,
    title,
    ab_test_ready,
    published,
    array_length(title_variants, 1) as n_title_variants,
    array_length(thumb_text_variants, 1) as n_thumb_variants
from content
where ab_test_ready is true
order by published_at desc;

-- 4. 우선순위 콘텐츠 분석
create or replace view view__osmu_priority as
select
    c.id,
    c.title,
    c.published_channel,
    p.priority_score,
    p.computed_at
from content as c
inner join strategy_optimizer as p
    on c.id = p.content_id
order by p.priority_score desc
limit 50;

-- 5. 최근 실행 실패 로그
create or replace view view__execution_errors as
select
    module,
    status,
    error_message,
    timestamp
from execution_log
where status = 'fail'
order by timestamp desc
limit 20;
