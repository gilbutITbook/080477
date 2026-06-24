import numpy as np

from eval_utils import EVAL_DATASET, load_config
from retriever import Retriever


# 개별 질문 평가 함수
def calculate_metrics(
    retrieved_docs: list,
    target_chunk_id: str
) -> tuple[float, float]:
    """
    검색 결과에서 Hit 여부와
    역순위(Reciprocal Rank)를 계산합니다.
    """

    hit = 0
    rank = 0
    for i, doc in enumerate(retrieved_docs):
        # 검색 결과 문서의 chunk_id 확인
        doc_chunk_id = doc.metadata.get(
            "chunk_id"
        )
        # 정답 문서인지 비교
        if doc_chunk_id == target_chunk_id:
            hit = 1
            # 검색 순위(1부터 시작)
            rank = i + 1
            break

    # Reciprocal Rank 계산
    reciprocal_rank = (
        1.0 / rank if rank > 0 else 0.0
    )

    return hit, reciprocal_rank

# 전체 검색 평가 실행
def run_evaluation(
    top_k: int = 3
) -> tuple[float, float]:
    
    # 설정 로드
    config = load_config()
    # 검색기 초기화
    retriever = Retriever(
        config["retriever"]
    )
    print(
        f"=== 검색 품질 평가 시작 "
        f"(Top-K={top_k}) ==="
    )

    hits = []
    reciprocal_ranks = []
    total_queries = 0

    # 골든 데이터셋 순회
    for group in EVAL_DATASET:
        # 현재 문서의 정답 ID
        target_id = group["chunk_id"]
        # 연결된 질문 반복
        for query in group["queries"]:
            total_queries += 1
            # 문서 검색 수행
            results = retriever.retrieve(
                query=query,
                top_k=top_k
            )
            # 검색 결과 평가
            is_hit, rr = calculate_metrics(
                results,
                target_id
            )
            # 평가 결과 저장
            hits.append(is_hit)
            reciprocal_ranks.append(rr)
            # 개별 로그 확인용
            # print(
            #     f"Query: {query} | "
            #     f"Hit: {is_hit} | "
            #     f"RR: {rr:.4f}"
            # )

    # 최종 평가 지표 계산
    hit_rate = np.mean(hits)
    mrr = np.mean(reciprocal_ranks)
    print("\n" + "=" * 40)
    print(
        f"평가 결과 요약 "
        f"(총 쿼리 수: {total_queries})"
    )
    print("=" * 40)
    print(
        f"적중률: "
        f"{hit_rate:.4f}"
    )
    print(
        f"MRR: "
        f"{mrr:.4f}"
    )
    print("=" * 40)
    return hit_rate, mrr

if __name__ == "__main__":

    # 검색 평가 실행
    run_evaluation(top_k=3)