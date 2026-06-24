def reciprocal_rank_fusion(
    ranked_lists: list,
    k: int = 60
):
    """여러 개의 순위 리스트를 RRF 방식으로 결합"""

    fused_scores = {}

    for rank_list in ranked_lists:

        for rank, doc_id in enumerate(rank_list):

            if doc_id not in fused_scores:
                fused_scores[doc_id] = 0

            # RRF 점수 계산
            # rank가 높을수록 더 큰 점수를 부여
            # k는 점수 차이를 완화하기 위한 상수
            fused_scores[doc_id] += 1 / (k + rank + 1)

    # 점수가 높은 순서대로 정렬
    reranked_results = sorted(
        fused_scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return reranked_results


# 1. 시맨틱 검색 결과
semantic_results = [
    "doc_3",
    "doc_1",
    "doc_5"
]

# 2. 키워드 검색 결과
keyword_results = [
    "doc_1",
    "doc_4",
    "doc_3"
]

# 3. RRF를 사용해 결과 결합
final_ranked_ids = reciprocal_rank_fusion(
    [semantic_results, keyword_results]
)

print("Hybrid Search Final Ranking:")
print(final_ranked_ids)