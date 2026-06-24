import psycopg2
from psycopg2.extras import RealDictCursor

from embedding_utils import get_embedding


conn_info = (
    "dbname='vectordb' "
    "user='user' "
    "password='password' "
    "host='localhost' "
    "port='5433'"
)


def insert_documents():
    # 앞에서 정의한 데이터 삽입 함수
    pass


def search_with_filters(query_text: str, k: int = 5, filters: dict = None):
    """메타데이터 필터를 적용해 벡터 검색을 수행합니다."""

    query_vector = get_embedding(query_text)
    query_vector_str = "[" + ",".join(map(str, query_vector)) + "]"

    sql_query = """
        SELECT
            id,
            content,
            (embedding <-> %s::vector) AS distance
        FROM documents
    """

    params = [query_vector_str]
    where_clauses = []

    allowed_filter_keys = {"category", "source", "status"}

    if filters:
        for key, value in filters.items():
            if key not in allowed_filter_keys:
                raise ValueError(f"허용되지 않은 필터 칼럼입니다: {key}")

            where_clauses.append(f"{key} = %s")
            params.append(value)

    if where_clauses:
        sql_query += " WHERE " + " AND ".join(where_clauses)

    sql_query += " ORDER BY distance LIMIT %s"
    params.append(k)

    with psycopg2.connect(conn_info) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql_query, tuple(params))
            results = cur.fetchall()

    return results


insert_documents()

results = search_with_filters(
    "How to optimize database performance?",
    filters={"category": "tech"}
)

print("\n--- 검색 결과 ---")

for res in results:
    print(
        f"Distance: {res['distance']:.4f}, "
        f"Content: {res['content'][:50]}..."
    )