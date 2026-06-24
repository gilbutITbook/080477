import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Tuple


class DatabaseChatMemory:
    """PostgreSQL을 사용해 대화 이력을 영구 저장하고 관리하는 클래스"""

    def __init__(self, db_config: dict):
        self.db_config = db_config

    def ensure_session(self, session_id: str):
        """세션이 없으면 먼저 생성"""
        query = """
            INSERT INTO chat_sessions (session_id)
            VALUES (%s)
            ON CONFLICT (session_id) DO NOTHING
        """
        with psycopg2.connect(**self.db_config) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (session_id,))

    def save_message(
        self,
        session_id: str,
        role: str,
        content: str
    ):
        """메시지 한 건 저장"""
        self.ensure_session(session_id)
        query = """
            INSERT INTO chat_messages
            (session_id, role, content)
            VALUES (%s, %s, %s)
        """
        with psycopg2.connect(**self.db_config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    query,
                    (session_id, role, content)
                )

    def get_history(
        self,
        session_id: str,
        limit: int = 10
    ) -> List[Tuple[str, str]]:
        """세션의 대화 이력을 시간 순으로 조회"""
        query = """
            SELECT role, content
            FROM chat_messages
            WHERE session_id = %s
            ORDER BY created_at ASC
            LIMIT %s
        """
        history = []
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor(
                    cursor_factory=RealDictCursor
                ) as cur:
                    cur.execute(
                        query,
                        (session_id, limit)
                    )
                    rows = cur.fetchall()
                    for row in rows:
                        history.append(
                            (row["role"], row["content"])
                        )
        except Exception as e:
            print(f"DB 이력 조회 중 오류: {e}")
        return history