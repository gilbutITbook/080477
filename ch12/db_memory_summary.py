import psycopg2
from openai import OpenAI


def summarize_and_save(
    self,
    session_id: str,
    client: OpenAI
):
    """지정된 세션의 대화를 요약해 저장"""

    # ➊ 대화 이력 조회
    history = self.get_history(
        session_id,
        limit=20
    )

    # (role, content) → 문자열 변환
    history_str = "\n".join(
        [f"{role}: {content}" for role, content in history]
    )

    # ➋ LLM 기반 요약 수행
    prompt = (
        "다음 대화 내용을 핵심만 유지해 "
        "한 문장으로 요약해 주세요.\n\n"
        f"{history_str}"
    )

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=prompt
        )

        summary = response.output_text

        # ➌ 요약 결과 저장
        query = """
            UPDATE chat_sessions
            SET summary = %s
            WHERE session_id = %s
        """

        with psycopg2.connect(self.db_config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    query,
                    (summary, session_id)
                )

    except Exception as e:
        print(f"대화 요약 중 오류 발생: {e}")