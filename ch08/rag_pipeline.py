import yaml

from components.generator import Generator
from components.reranker import Reranker
from components.retriever import Retriever

class RAGPipeline:
    def __init__(self, config_path: str):
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        # 설정 파일 기반 컴포넌트 초기화
        self.retriever = Retriever(config["retriever"])
        self.reranker = Reranker(config["reranker"])
        self.generator = Generator(config["generator"])
    def run(self, query: str) -> str:
        """RAG 파이프라인 전체 실행"""
        # Retriever: 관련 문서 검색
        retrieved_docs = self.retriever.retrieve(query=query)
        # Reranker: 문서 중요도 재정렬
        reranked_docs = self.reranker.rerank(
            query=query,
            documents=retrieved_docs
        )
        # Generator: 최종 답변 생성
        answer = self.generator.generate(
            query=query,
            context_docs=reranked_docs
        )
        return answer

if __name__ == "__main__":
    try:
        pipeline = RAGPipeline("config.yaml")
        question = "RAG 시스템에서 청킹은 왜 중요한가요?"
        final_answer = pipeline.run(question)
        print("--- 최종 답변 ---")
        print(final_answer)
    except Exception as e:
        print(f"파이프라인 실행 중 오류 발생: {e}")