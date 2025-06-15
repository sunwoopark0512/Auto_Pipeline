CREATE TABLE IF NOT EXISTS campaign_calendar (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  campaign_name TEXT,
  start_date DATE,
  end_date DATE,
  goal_views BIGINT,
  goal_signups BIGINT,
  notes TEXT
);
