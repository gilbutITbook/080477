import os
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, APIError, AuthenticationError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# .env 파일 로드
load_dotenv()

# 환경 변수에서 API 키 읽기
api_key = os.getenv("OPENAI_API_KEY")

# OpenAI 클라이언트 생성
client = OpenAI(api_key=api_key)


@retry(
    retry=retry_if_exception_type((RateLimitError, APIError)), 
    stop=stop_after_attempt(3), 
    wait=wait_exponential(multiplier=1, min=2, max=60) 
)
def call_llm_api_with_retry(): 
    """LLM API 호출 및 재시도 로직"""
    print("API 호출 시도 중...")
    response = client.responses.create(
        model="gpt-4.1-nano",
        input="MLOps에서 재시도의 중요성을 간결하게 설명해 주세요.",
        temperature=0.0
    )
    return response

try:
    result = call_llm_api_with_retry()

    print("\n[성공] LLM 응답:")
    print(result.output_text)

except AuthenticationError as e:
    print(f"\n[오류] 인증 실패: API 키를 확인하세요. {e}")

except RateLimitError:
    print("\n[오류] 요청 제한 초과: 재시도 횟수를 모두 소진했습니다.")

except Exception as e:
    print(f"\n[오류] 예상치 못한 오류 발생: {e}")