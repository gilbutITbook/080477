-- pgvector 확장 활성화(DB에서 실행)
CREATE EXTENSION IF NOT EXISTS vector;
-- 문서 저장 테이블 생성
CREATE TABLE IF NOT EXISTS documents (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    embedding vector(1536)
);
