CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    user_login VARCHAR(255) NOT NULL UNIQUE,
    user_role VARCHAR(255) NOT NULL, 
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO users (user_login, user_role, password_hash)
VALUES ('admin', 'admin', '$2b$12$yqhy.sAQScugWg7M3w2/2OKr35xp/k8ya/clI0QLDVZZwKs4QoOkC'); --password=AdminPass1!

-- Ученик
INSERT INTO users (user_login, user_role, password_hash)
VALUES ('student1', 'student', '$2b$12$NAUtm.J404IS9ZWr6kWN8eQx7..4/VHUci.6SeIuc6WqKgWwiYg8i'); --password=StudentPass1!

-- Учитель
INSERT INTO users (user_login, user_role, password_hash)
VALUES ('teacher1', 'teacher', '$2b$12$iui6JxiWcPeDPAkQxnoZWelFePT6Y3ZkmG7ejcHxaSm2yGFlHABEq'); --password=TeacherPass1!