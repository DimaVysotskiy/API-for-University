CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    user_login VARCHAR(255) NOT NULL UNIQUE,
    user_role VARCHAR(255) NOT NULL, 
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO users (user_login, user_role, password_hash)
VALUES ('admin', 'admin', '$2b$12$IJUqtZzGWOa09kICIi0CdeHbPVlgRxdZP/Pnq.dOOQJV0f0R5qTn2'); --password=admin123