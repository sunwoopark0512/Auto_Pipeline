-- content_tracker
CREATE TABLE IF NOT EXISTS content_tracker (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    keyword TEXT NOT NULL,
    title TEXT,
    content TEXT,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT now(),
    published_at TIMESTAMP
);

-- performance_tracker
CREATE TABLE IF NOT EXISTS performance_tracker (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_id UUID REFERENCES content_tracker (id),
    platform TEXT,
    views INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    collected_at TIMESTAMP DEFAULT now()
);

-- scheduler_queue
CREATE TABLE IF NOT EXISTS scheduler_queue (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_id UUID REFERENCES content_tracker (id),
    scheduled_at TIMESTAMP,
    status TEXT DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT now()
);
