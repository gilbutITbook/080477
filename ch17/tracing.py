from opentelemetry import trace

# ➊ 트레이서 생성
tracer = trace.get_tracer(__name__)

def run_rag_pipeline(query: str):
    # ➋ 전체 요청 추적 시작
    with tracer.start_as_current_span(
        "rag_pipeline"
    ) as parent_span:
        # ➌ 사용자 질문 기록
        parent_span.set_attribute(
            "user.query",
            query
        )
        # ➍ 검색 단계 추적
        with tracer.start_as_current_span(
            "retrieval"
        ) as child_span:
            # 실제 검색 로직 위치
            retrieved_docs = [
                "RAG 개념 문서",
                "벡터 검색 설명 문서"
            ]
            # 검색된 문서 수 기록
            child_span.set_attribute(
                "retrieved_docs_count",
                len(retrieved_docs)
            )
        # ➎ 생성 단계 추적
        with tracer.start_as_current_span(
            "generation"
        ) as child_span:
            # 실제 생성 로직 위치
            answer = "RAG는 검색한 문서를 기반으로 답변을 생성하는 방식입니다."
            # 사용 모델 기록
            child_span.set_attribute(
                "llm.model_name",
                "gpt-4o"
            )
            # 생성 결과 길이 기록
            child_span.set_attribute(
                "answer_length",
                len(answer)
            )