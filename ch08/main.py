import yaml
from components.generator import Generator
from components.retriever import Retriever

# 설정 파일을 로드하는 함수
def load_config(path="config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main_pipeline(query: str):
    # 설정 로드
    config = load_config()
    # 1. 문서 검색
    print("1. Retriever로 문서 검색 중...")
    retriever = Retriever(config["retriever"])
    retrieved_documents = retriever.retrieve(
        query,
        top_k=3
    )
    if not retrieved_documents:
        print("관련 문서를 찾지 못했습니다.")
        return
    # 2. 응답 생성
    print("2. Generator로 응답 생성 중...")
    generator = Generator(config["generator"])
    final_answer = generator.generate(
        query,
        retrieved_documents
    )
    # 3. 결과 출력
    print("\n" + "=" * 50)
    print(f"질문: {query}")
    print("---")
    print(f"응답: {final_answer}")
    print("=" * 50)

if __name__ == "__main__":
    user_question = "RAG 시스템에서 청킹은 왜 중요한가요?"
    main_pipeline(user_question)