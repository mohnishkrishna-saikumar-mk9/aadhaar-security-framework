-- Database Schema for Aadhaar-Inspired Identity System

CREATE TABLE IF NOT EXISTS identity (
    identity_id TEXT PRIMARY KEY,
    credential_hash TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS biometric_templates (
    identity_id TEXT PRIMARY KEY,
    face_template_path TEXT,
    fingerprint_template_path TEXT,
    FOREIGN KEY (identity_id) REFERENCES identity (identity_id)
);

CREATE TABLE IF NOT EXISTS verification_logs (
    attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    identity_id TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    credential_result TEXT,
    face_pad_result TEXT,
    face_match_score REAL,
    fingerprint_pad_result TEXT,
    fingerprint_match_score REAL,
    final_result TEXT,
    attack_type TEXT,
    FOREIGN KEY (identity_id) REFERENCES identity (identity_id)
);

-- Note: The demo_details table holds the synthetic PII returned only on successful auth
CREATE TABLE IF NOT EXISTS demo_details (
    identity_id TEXT PRIMARY KEY,
    name TEXT,
    age INTEGER,
    gender TEXT,
    service_status TEXT,
    verification_status TEXT,
    FOREIGN KEY (identity_id) REFERENCES identity (identity_id)
);
