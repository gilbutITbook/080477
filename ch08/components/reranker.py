from typing import Any, Dict, List, Optional
from sentence_transformers import CrossEncoder
from components.document import Document

class Reranker:
    """Cross-Encoder를 사용해 문서 순서를 재정렬하는 클래스"""
    # 1. 모델 초기화
    def __init__(self, config: Dict[str, Any]):
        self.model_name = config.get(
            "model_name",
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )
        self.default_top_n = config.get("top_n", 3)
        print(f"Reranker 모델 로딩 중: {self.model_name} ...")
        self.model = CrossEncoder(self.model_name)
        print("Reranker 모델 로드 완료.")
    def rerank(
        self,
        query: str,
        documents: List[Document],
        top_n: Optional[int] = None
    ) -> List[Document]:
        if not documents:
            return []
        if top_n is None:
            top_n = self.default_top_n
        # 2. 질문-문서 쌍 생성
        pairs = [
            (query, doc.page_content)
            for doc in documents
        ]
        # 3. 관련성 점수 계산
        scores = self.model.predict(pairs)
        # 4. Document 객체에 점수 반영
        for doc, score in zip(documents, scores):
            doc.score = float(score)
        # 5. 점수 기준 내림차순 정렬 및 반환
        ranked_docs = sorted(
            documents,
            key=lambda x: x.score,
            reverse=True
        )
        return ranked_docs[:top_n]