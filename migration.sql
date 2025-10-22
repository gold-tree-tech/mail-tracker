-- Create email_metadata table
CREATE TABLE email_metadata (
    id BIGSERIAL PRIMARY KEY,
    recipient_email TEXT NOT NULL,
    tracking_id TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL
);

-- Create opens table
CREATE TABLE opens (
    id BIGSERIAL PRIMARY KEY,
    tracking_id TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL
);

-- Create indexes for better performance
CREATE INDEX idx_email_metadata_tracking_id ON email_metadata(tracking_id);
CREATE INDEX idx_opens_tracking_id ON opens(tracking_id);
