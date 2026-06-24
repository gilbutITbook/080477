from db_memory import DatabaseChatMemory
from generator import Generator  # 또는 generator_ollama
from query_rewriter import QueryRewriter
from reranker import Reranker
from retriever import Retriever


def run_conversational_rag():
    # 데이터베이스 연결 정보
    db_config = {
        "dbname": "vectordb",
        "user": "user",
        "password": "password",
        "host": "localhost",
        "port": 5433
    }

    # 컴포넌트 초기화
    memory = DatabaseChatMemory(db_config)
    retriever = Retriever({
        "db_config": db_config,
        "embedding_model": "text-embedding-3-small",
        "top_k": 50
    })
    reranker = Reranker({
        "model_name": "cross-encoder/ms-marco-MiniLM-L-6-v2",
        "top_n": 5
    })
    rewriter = QueryRewriter(
        model_name="gpt-4.1-mini"
    )
    generator = Generator({
        "model_name": "gpt-4.1-mini",
        "temperature": 0.1,
        "llm_type": "openai"
    })

    # 사용자별 세션 ID 설정
    session_id = "user_123_session_001"
    print(f"--- [세션: {session_id}] 대화를 시작합니다. ---")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # ➊ 대화 이력 조회 
        history = memory.get_history(session_id, limit=5)
        # ➋ 쿼리 재작성
        rewritten_query = rewriter.rewrite(user_input, history)
        print(f"[검색용 쿼리]: {rewritten_query}")
        # ➌ 문서 검색
        retrieved_docs = retriever.retrieve(
            rewritten_query,
            top_k=5
        )
        if not retrieved_docs:
            print("관련 문서를 찾지 못했습니다.")
            continue
        # ➍ 문서 재정렬
        reranked_docs = reranker.rerank(
            query=rewritten_query,
            documents=retrieved_docs
        )
        # ➎ 응답 생성
        answer = generator.generate(
            user_input,
            reranked_docs
        )
        print(f"AI: {answer}")
        # ➏ 대화 저장
        memory.save_message(
            session_id,
            role="user",
            content=user_input
        )
        memory.save_message(
            session_id,
            role="ai",
            content=answer
        )

if __name__ == "__main__":
    run_conversational_rag()