import yaml
from components.base import Retriever, Reranker, Generator

class RAGPipeline:
    def __init__(self, config_path: str):
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        # 설정 파일 기반 컴포넌트 초기화
        self.retriever = Retriever(config["retriever"])
        self.reranker = Reranker(config["reranker"])
        self.generator = Generator(config["generator"])

    def run(self, query: str) -> str:
        """RAG 파이프라인 전체 흐름 실행"""

        # 1. 문서 검색
        retrieved_docs = self.retriever.retrieve(
            query=query,
            top_k=self.retriever.config["top_k"]
        )

        # 2. 문서 재정렬
        reranked_docs = self.reranker.rerank(
            query=query,
            documents=retrieved_docs,
            top_n=self.reranker.config["top_n"]
        )

        # 3. 응답 생성
        answer = self.generator.generate(
            query=query,
            context_docs=reranked_docs
        )

        return answer