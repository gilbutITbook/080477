import psycopg2

from embedding_utils import get_embedding

# DB 연결 정보
conn_info = (
    "dbname='vectordb' "
    "user='user' "
    "password='password' "
    "host='localhost' "
    "port='5433'"
)

# ➊ 데이터 삽입 함수
def insert_documents():
    documents_with_metadata = [
        ("PostgreSQL indexing strategies", "blog_1.md", "tech"),
        ("How to cook pasta", "recipe.pdf", "food"),
        ("Vector databases explained", "blog_2.md", "tech"),
        ("Healthy diet tips", "health.pdf", "health"),
    ]
    with psycopg2.connect(conn_info) as conn:
        with conn.cursor() as cur:
            for content, source, category in documents_with_metadata:
                # ➋ 텍스트를 임베딩 벡터로 변환
                embedding_vector = get_embedding(content)
                # ➌ PGVector 저장 형식으로 변환
                embedding_vector_str = (
                    "[" + ",".join(map(str, embedding_vector)) + "]"
                )
                # ➍ 메타데이터와 함께 저장
                cur.execute(
                    """
                    INSERT INTO documents
                    (content, source, category, embedding)
                    VALUES (%s, %s, %s, %s::vector)
                    """,
                    (
                        content,
                        source,
                        category,
                        embedding_vector_str
                    )
                )
        conn.commit()
    print("데이터 삽입 완료!")

if __name__ == "__main__":      # ← 추가
    insert_documents()