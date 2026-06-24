-- 대화 세션(대화방)을 관리하는 테이블
CREATE TABLE IF NOT EXISTS chat_sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
-- 세션에 속한 메시지를 저장하는 테이블
CREATE TABLE IF NOT EXISTS chat_messages (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255)
        NOT NULL
        REFERENCES chat_sessions(session_id)
        ON DELETE CASCADE,
    role VARCHAR(10)
        NOT NULL
        CHECK (role IN ('user', 'ai')),
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
); 
