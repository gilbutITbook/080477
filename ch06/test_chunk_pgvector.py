import os
from typing import List

import psycopg2
from openai import OpenAI

from test_recursive_chunk_doc import build_chunks
from dotenv import load_dotenv

load_dotenv()
# OpenAI 클라이언트 초기화
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) 

# 임베딩 생성 함수
def get_embedding(text: str) -> List[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


# 청크 생성
chunks = build_chunks()

# DB 연결 정보
conn_info = (
    "dbname='vectordb' "
    "user='user' "
    "password='password' "
    "host='localhost' "
    "port='5433'"
)

saved_count = 0

try:
    with psycopg2.connect(conn_info) as conn:
        with conn.cursor() as cur:

            for chunk in chunks:
                # Document → 텍스트 추출
                text = chunk.page_content

                if not text or not text.strip():
                    continue

                # 텍스트 → 벡터 변환
                embedding_vector = get_embedding(text)

                # 원문과 벡터 저장
                cur.execute(
                    "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
                    (text, embedding_vector)
                )

                saved_count += 1

            conn.commit()

    print(f"{saved_count}개의 청크를 성공적으로 저장했습니다.")

except Exception as e:
    print(f"데이터베이스 작업 중 오류 발생: {e}")