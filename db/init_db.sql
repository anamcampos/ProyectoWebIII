CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    external_id TEXT UNIQUE,
    title TEXT,
    price TEXT,
    url TEXT,
    last_seen TIMESTAMP DEFAULT now(),
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS files (
    id SERIAL PRIMARY KEY,
    item_id INTEGER REFERENCES items(id) ON DELETE CASCADE,
    file_name TEXT,
    file_path TEXT,
    sha256 TEXT,
    version INTEGER DEFAULT 1,
    last_checked TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    item_id INTEGER,
    event_type TEXT,
    details JSONB,
    created_at TIMESTAMP DEFAULT now()
);
