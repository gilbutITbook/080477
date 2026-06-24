from rag_pipeline import RAGPipeline


if __name__ == "__main__":

    # 설정 파일 기반 파이프라인 생성
    pipeline = RAGPipeline("config.yaml")

    # 사용자 질문
    question = "RAG 시스템에서 재순위 모델은 어떤 역할을 하나요?"

    # 전체 파이프라인 실행
    final_answer = pipeline.run(question)

    print("--- 최종 응답 ---")
    print(final_answer)