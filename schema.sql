CREATE TABLE IF NOT EXISTS ab_test_queue (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content_id UUID REFERENCES content_tracker(id),
  variant TEXT,
  field TEXT,
  original TEXT,
  variant_text TEXT,
  status TEXT DEFAULT 'queued',
  created_at TIMESTAMP DEFAULT now()
);
