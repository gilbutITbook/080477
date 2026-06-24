import json
import logging
import uuid

# ➊ JSON 포맷터 정의
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", None),
            "extra_info": getattr(record, "extra_info", {}),
        }
        return json.dumps(log_record, ensure_ascii=False)
    
# ➋ 로거 설정
logger = logging.getLogger("RAGAppLogger")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)

# ➌ 예시용 검색 함수
def retrieve_documents(query):
    return ["RAG 개념 문서", "검색 증강 생성 설명 문서"]

# ➍ 예시용 생성 함수
def generate_answer(query, docs):
    return "RAG는 검색한 문서를 바탕으로 답변을 생성하는 방식입니다."

# ➎ 요청 처리
def handle_request(query, user_id):
    request_id = str(uuid.uuid4())
    extra = {
        "request_id": request_id,
        "extra_info": {"user_id": user_id},
    }
    logger.info(f"Received query: {query}", extra=extra)
    retrieved_docs = retrieve_documents(query)
    logger.info(f"Retrieved {len(retrieved_docs)} documents.", extra=extra)
    final_answer = generate_answer(query, retrieved_docs)
    logger.info("Generated answer.", extra=extra)
    return final_answer

if __name__ == "__main__":
    answer = handle_request("What is RAG?", "user-123")
    print(answer)