import os
from typing import List, Tuple

import yaml
from dotenv import load_dotenv

from generator import Generator
from query_rewriter import QueryRewriter
from reranker import Reranker
from retriever import Retriever


# 환경 변수 로드 및 API 키 검증
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")

# 설정 파일 로드
def load_config(path="config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main_conversational_pipeline():
    """대화형 RAG 파이프라인의 전체 실행 흐름 관리"""

    config = load_config()

    # 1. 구성 요소 초기화
    retriever = Retriever(config["retriever"])
    reranker = Reranker(config["reranker"])
    generator = Generator(config["generator"])

    query_rewriter = QueryRewriter(
        model_name="gpt-4.1-mini",
        api_key=API_KEY
    )

    # 2. 대화 이력 저장
    chat_history: List[Tuple[str, str]] = []

    print("--- 대화형 RAG 챗봇을 시작합니다. 'exit'를 입력하면 종료됩니다. ---")

    while True:
        # 3. 사용자 입력
        user_question = input("You: ")
        if user_question.lower() == "exit":
            print("챗봇을 종료합니다.")
            break

        # 4. 쿼리 재작성
        print("\nStep 1: 쿼리 재작성 중...")
        rewritten_query = query_rewriter.rewrite(user_question, chat_history)
        print(f"재작성된 쿼리: {rewritten_query}")

        # 5. 문서 검색
        print("\nStep 2: 관련 문서 검색 중...")
        retrieved_documents = retriever.retrieve(rewritten_query, top_k=3)

        if not retrieved_documents:
            print("관련 문서를 찾지 못했습니다.")
            continue

        # 6. 문서 재정렬
        print("\nStep 3: 검색 결과 재정렬 중...")
        reranked_documents = reranker.rerank(
            query=rewritten_query,
            documents=retrieved_documents
        )

        # 7. 응답 생성
        print("\nStep 4: 응답 생성 중...")
        final_answer = generator.generate(user_question, reranked_documents)
        print(f"Bot: {final_answer}")

        # 8. 대화 이력 업데이트
        chat_history.append((user_question, final_answer))
        print("\n" + "=" * 50)


if __name__ == "__main__":
    main_conversational_pipeline()