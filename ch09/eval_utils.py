import os

import psycopg2
import psycopg2.extras
import yaml
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

# ➊ 평가 데이터셋: 어떤 질문에 대해 어떤 문서가 정답인지 미리 정의해 둔 데이터
EVAL_DATASET = [
    {
        "chunk_id": "doc_rag_def",
        "content": "RAG(Retrieval-Augmented Generation)는 검색(retrieval)과 생성(generation)을 결합한 LLM 활용 방식입니다. LLM이 학습한 지식뿐 아니라 외부 데이터베이스에서 관련 정보를 검색한 뒤 이를 바탕으로 답변을 생성하는 구조입니다.",
        "queries": [
            "RAG의 정의는 무엇인가?",
            "RAG 아키텍처의 장점은?",
            "검색 증강 생성이란?"
        ]
    },
    {
        "chunk_id": "doc_chunking",
        "content": "청킹(chunking)은 긴 문서를 의미 있는 단위로 나누어 저장하고, 필요한 부분만 선택적으로 검색할 수 있도록 만드는 방법입니다.",
        "queries": [
            "청킹이 왜 중요한가?",
            "문서를 작게 나누는 것을 무엇이라고 하는가?",
            "검색 정확도를 높이는 문서 분할 방법은?"
        ]
    },
    {
        "chunk_id": "doc_vector_db",
        "content": "벡터 데이터베이스(Vector Database)는 대규모 데이터를 빠르게 검색하고, 의미 기반 유사도를 효율적으로 계산하기 위해 설계된 전용 시스템입니다.",
        "queries": [
            "벡터 DB의 역할은?",
            "의미 기반 검색을 위한 저장소는?",
            "비정형 데이터를 저장하는 방법은 무엇인가?"
        ]
    }
]

# ➋ 
def load_config():
    """설정 파일을 읽어 파이썬 딕셔너리로 변환"""
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# 평가용 데이터를 벡터 데이터베이스에 삽입하는 함수
def insert_eval_data():
    """평가용 데이터를 DB에 주입"""
    config = load_config()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("오류: OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
        return

    client = OpenAI(api_key=api_key)
    db_config = config["retriever"]["db_config"]

    print("평가용 데이터 주입 시작...")

    try:
        with psycopg2.connect(**db_config) as conn: # ➌
            with conn.cursor() as cur:
                # ➍ documents 테이블이 없으면 생성
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS documents (
                        id BIGSERIAL PRIMARY KEY,
                        content TEXT,
                        metadata JSONB,
                        embedding vector(1536)
                    );
                """)
                # 중복 방지를 위해 chunk_id로 기존 데이터 확인(선택 사항)
                # 여기서는 간단히 무조건 삽입하되 metadata에 chunk_id 심기
                for item in EVAL_DATASET: # ➎
                    response = client.embeddings.create( # ➏
                        input=[item["content"]],
                        model=config["retriever"]["embedding_model"]
                    )
                    embedding = response.data[0].embedding

                    metadata = { # ➐
                        "source": "eval_set",
                        "chunk_id": item["chunk_id"]
                    }

                    cur.execute( # ➑
                        """
                        INSERT INTO documents (content, metadata, embedding)
                        VALUES (%s, %s, %s)
                        """,
                        (
                            item["content"],
                            psycopg2.extras.Json(metadata),
                            embedding
                        )
                    )
        print(f"평가 데이터 {len(EVAL_DATASET)}개 그룹 주입 완료")
    except Exception as e:
        print(f"데이터 주입 중 오류 발생: {e}")

# 이 파일을 직접 실행할 때만 insert_eval_data()가 호출되어 데이터 주입 수행
if __name__ == "__main__":
    insert_eval_data()