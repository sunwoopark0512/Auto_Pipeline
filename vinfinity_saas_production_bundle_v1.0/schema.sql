-- 전환(구매·가입) 로그
CREATE TABLE IF NOT EXISTS conversion_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  content_id UUID REFERENCES content_tracker(id),
  platform TEXT,
  revenue_cents BIGINT,
  currency CHAR(3) DEFAULT 'USD',
  event TEXT,
  occurred_at TIMESTAMP DEFAULT now()
);

-- 사용자 행동 이벤트 로그
CREATE TABLE IF NOT EXISTS event_log (
  id BIGSERIAL PRIMARY KEY,
  user_id UUID,
  event TEXT,
  meta JSONB,
  occurred_at TIMESTAMP DEFAULT now()
);
