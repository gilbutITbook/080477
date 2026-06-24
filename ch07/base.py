class Retriever:
    def __init__(self, config: dict):
        """검색기 초기화"""
        self.config = config
    def retrieve(
        self,
        query: str,
        top_k: int,
        filters: dict | None = None
    ) -> list[Document]:
        """질문과 관련된 문서를 검색"""
        pass

class Reranker:
    def __init__(self, config: dict):
        """재순위 모델 초기화"""
        self.config = config
    def rerank(
        self,
        query: str,
        documents: list[Document],
        top_n: int
    ) -> list[Document]:
        """문서 순서를 재조정"""
        pass

class Generator:
    def __init__(self, config: dict):
        """생성 모델 초기화"""
        self.config = config
    def generate(
        self,
        query: str,
        context_docs: list[Document]
    ) -> str:
        """답변 생성"""
        pass