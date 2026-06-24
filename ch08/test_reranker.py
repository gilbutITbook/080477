# 테스트 코드
from components.document import Document
from components.reranker import Reranker

if __name__ == "__main__":
    # 테스트용 문서 데이터
    docs = [
        Document(
            page_content="서울의 날씨는 맑습니다.",
            metadata={"id": 1}
        ),
        Document(
            page_content="RAG는 검색 증강 생성을 의미합니다.",
            metadata={"id": 2}
        ),
        Document(
            page_content="사과는 맛있는 과일입니다.",
            metadata={"id": 3}
        ),
    ]
    # 설정 및 초기화
    config = {
        "model_name": "cross-encoder/ms-marco-MiniLM-L-6-v2",
        "top_n": 2
    }
    reranker = Reranker(config)
    # 질문
    query = "RAG가 무엇인가요?"
    print("\n--- 재순위 실행 ---")
    results = reranker.rerank(query, docs)
    for i, doc in enumerate(results):
        print(
            f"순위 {i+1}: "
            f"{doc.page_content} "
            f"(점수: {doc.score:.4f})"
        )