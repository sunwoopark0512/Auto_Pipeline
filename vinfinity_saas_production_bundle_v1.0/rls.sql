ALTER TABLE content_tracker ENABLE ROW LEVEL SECURITY;
ALTER TABLE scheduler_queue ENABLE ROW LEVEL SECURITY;

CREATE POLICY own_rows_only ON content_tracker
USING (auth.uid() = user_id);

CREATE POLICY own_rows_only ON scheduler_queue
USING (auth.uid() = user_id);
