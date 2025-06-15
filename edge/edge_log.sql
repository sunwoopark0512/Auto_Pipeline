create table edge_log (
    id uuid primary key default gen_random_uuid(),
    uid text,
    variant text,
    path text,
    ts timestamp default now()
);
