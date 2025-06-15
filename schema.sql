-- Supabase initial schema

CREATE TABLE IF NOT EXISTS content_tracker (
    id SERIAL PRIMARY KEY,
    content_id TEXT NOT NULL UNIQUE,
    generated_at TIMESTAMPTZ DEFAULT NOW(),
    status TEXT NOT NULL,
    metadata JSONB
);

CREATE TABLE IF NOT EXISTS performance_tracker (
    id SERIAL PRIMARY KEY,
    content_id TEXT NOT NULL REFERENCES content_tracker(content_id),
    metric TEXT NOT NULL,
    value NUMERIC,
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS scheduler_queue (
    id SERIAL PRIMARY KEY,
    job_name TEXT NOT NULL,
    payload JSONB,
    scheduled_for TIMESTAMPTZ,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pipeline_runs (
    id SERIAL PRIMARY KEY,
    started_at TIMESTAMPTZ DEFAULT NOW(),
    finished_at TIMESTAMPTZ,
    status TEXT NOT NULL,
    details JSONB
);

CREATE TABLE IF NOT EXISTS error_logs (
    id SERIAL PRIMARY KEY,
    run_id INTEGER REFERENCES pipeline_runs(id),
    message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
