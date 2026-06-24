from sentence_transformers.cross_encoder import CrossEncoder


# Cross-Encoder 모델 로드
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

query = "How to build a RAG system?"


# 1단계에서 검색된 후보 문서
retrieved_docs = [
    "To build a RAG system, you need a vector database and an LLM.",
    "A vector database stores embeddings for fast retrieval.",
    "First, you must chunk your documents into smaller pieces.",
    "LLM stands for Large Language Model."
]


# 재순위 평가를 위한 (쿼리, 문서) 쌍 생성
pairs = [
    (query, doc)
    for doc in retrieved_docs
]


# 관련성 점수 계산
scores = reranker.predict(pairs)

print("--- Scores before re-ranking ---")
print(scores)


# 점수 기준으로 재정렬
reranked_results = sorted(
    zip(scores, retrieved_docs),
    key=lambda x: x[0],
    reverse=True
)

print("\n--- Results after re-ranking ---")

for score, doc in reranked_results:
    print(f"Score: {score:.4f}, Doc: {doc}")