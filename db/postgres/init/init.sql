CREATE TABLE "Users"(
    id SERIAL PRIMARY KEY,
    user_login VARCHAR(255) NOT NULL UNIQUE,
    user_role VARCHAR(255) NOT NULL, 
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO "Users" (user_login, user_role, password_hash)
VALUES ('admin', 'admin', '$2b$12$yqhy.sAQScugWg7M3w2/2OKr35xp/k8ya/clI0QLDVZZwKs4QoOkC'); --password=AdminPass1!

-- Ученик
INSERT INTO "Users" (user_login, user_role, password_hash)
VALUES ('student1', 'student', '$2b$12$NAUtm.J404IS9ZWr6kWN8eQx7..4/VHUci.6SeIuc6WqKgWwiYg8i'); --password=StudentPass1!

-- Учитель
INSERT INTO "Users" (user_login, user_role, password_hash)
VALUES ('teacher1', 'teacher', '$2b$12$iui6JxiWcPeDPAkQxnoZWelFePT6Y3ZkmG7ejcHxaSm2yGFlHABEq'); --password=TeacherPass1!

-- Таблица Groups
CREATE TABLE "Groups"(
    id SERIAL PRIMARY KEY,
    timetable JSONB NOT NULL,
    faculty VARCHAR(100) NOT NULL
);

-- Таблица StudentInfo
CREATE TABLE "StudentInfo"(
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES "Users"(id) ON DELETE CASCADE,
    group_id INTEGER NOT NULL REFERENCES "Groups"(id) ON DELETE RESTRICT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    zach_number VARCHAR(100) NOT NULL UNIQUE,
    status VARCHAR(100) NOT NULL
);