-- Leave types table
CREATE TABLE IF NOT EXISTS leave_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(200),
    active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_leave_types_active ON leave_types(active);