import os
from typing import Any, Dict, List

import psycopg2
from dotenv import load_dotenv
from openai import OpenAI
from psycopg2.extras import RealDictCursor

from document import Document


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


class Retriever:
    """PostgreSQL/PGVector 데이터베이스에서 문서를 검색하는 클래스"""

    def __init__(self, config: Dict[str, Any]):
        """설정 딕셔너리를 받아 초기화"""

        self.db_config = config["db_config"]
        self.embedding_model = config.get("embedding_model", "text-embedding-3-small")
        self.top_k = config.get("top_k", 5)

        # API 키는 환경 변수에서 로드
        self.client = OpenAI(api_key=api_key)
        self.embedding_cache = {}

    def _get_embedding(self, text: str) -> List[float]:
        """텍스트를 임베딩 벡터로 변환하는 private 헬퍼 메서드"""

        if text in self.embedding_cache:
            return self.embedding_cache[text]

        response = self.client.embeddings.create(
            input=[text],
            model=self.embedding_model
        )

        embedding = response.data[0].embedding
        self.embedding_cache[text] = embedding

        return embedding

    def retrieve(self, query: str, top_k: int = None) -> List[Document]:
        """주어진 쿼리와 가장 유사한 문서를 데이터베이스에서 검색"""

        if top_k is None:
            top_k = self.top_k

        query_vector = self._get_embedding(query)

        # pgvector의 코사인 거리 연산자(<=>) 사용
        sql_query = """
            SELECT id, content, (embedding <=> %s::vector) AS distance
            FROM documents
            ORDER BY distance
            LIMIT %s
        """

        params = (str(query_vector), top_k)
        results = []

        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(sql_query, params)
                    fetched_rows = cur.fetchall()

                    for row in fetched_rows:
                        doc = Document(
                            page_content=row["content"],
                            metadata={
                                "id": row["id"],
                                "distance": row["distance"]
                            },
                            score=1 - row["distance"]
                        )
                        results.append(doc)

        except Exception as e:
            print(f"Retriever DB 작업 중 오류 발생: {e}")
            return []

        return results