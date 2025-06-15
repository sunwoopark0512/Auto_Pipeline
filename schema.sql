-- 퍼포먼스 수집 로그
CREATE TABLE IF NOT EXISTS analytics_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_id UUID REFERENCES content_tracker (id),
    platform TEXT,
    metric TEXT,
    value BIGINT,
    collected_at TIMESTAMP DEFAULT now()
);
