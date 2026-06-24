import os

import psycopg2
import psycopg2.extras
import yaml
from dotenv import load_dotenv
from openai import OpenAI


# .env 환경 변수 로드
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


# 설정 파일 로드
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

db_config = config["retriever"]["db_config"]


# 실습용 샘플 문서
sample_docs = [
    {
        "content": (
            "RAG(Retrieval-Augmented Generation)는 검색(retrieval)과 "
            "생성(generation)을 결합한 LLM 활용 방식입니다. "
            "LLM이 학습한 지식뿐 아니라 외부 데이터베이스에서 관련 정보를 "
            "검색한 뒤 이를 바탕으로 답변을 생성하는 구조입니다."
        ),
        "metadata": {
            "source": "chapter_7",
            "topic": "rag"
        }
    },
    {
        "content": (
            "청킹(chunking)은 긴 문서를 의미 있는 단위로 나누어 저장하고, "
            "필요한 부분만 선택적으로 검색할 수 있도록 만드는 방법입니다."
        ),
        "metadata": {
            "source": "chapter_6",
            "topic": "chunking"
        }
    },
    {
        "content": (
            "벡터 데이터베이스(Vector Database)는 대규모 데이터를 빠르게 "
            "검색하고, 의미 기반 유사도를 효율적으로 계산하기 위해 설계된 "
            "전용 시스템입니다."
        ),
        "metadata": {
            "source": "chapter_6",
            "topic": "vector_db"
        }
    },
]


def get_embedding(text: str):
    """텍스트 임베딩 생성"""

    response = client.embeddings.create(
        input=[text],
        model=config["retriever"]["embedding_model"]
    )

    return response.data[0].embedding


def insert_data():
    """샘플 문서를 PostgreSQL에 저장"""

    print("데이터를 주입합니다.")

    try:
        # PostgreSQL 연결
        with psycopg2.connect(**db_config) as conn:

            with conn.cursor() as cur:

                # 테이블이 없으면 생성
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS documents (
                        id BIGSERIAL PRIMARY KEY,
                        content TEXT,
                        metadata JSONB,
                        embedding vector(1536)
                    );
                """)

                for doc in sample_docs:

                    print(f"임베딩 생성 중: {doc["content"][:20]}...")

                    # 임베딩 생성
                    embedding = get_embedding(doc["content"])

                    # DB 저장
                    cur.execute("""
                        INSERT INTO documents (
                            content,
                            metadata,
                            embedding
                        )
                        VALUES (%s, %s, %s)
                    """, (
                        doc["content"],
                        psycopg2.extras.Json(doc["metadata"]),
                        embedding
                    ))

            conn.commit()

            print(f"성공적으로 {len(sample_docs)}개의 문서를 저장했습니다.")

    except Exception as e:
        print(f"오류 발생: {e}")


if __name__ == "__main__":

    if not api_key:
        print("오류: OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")

    else:
        insert_data()