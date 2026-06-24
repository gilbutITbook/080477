import os
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수에서 API 키 읽기
api_key = os.getenv("OPENAI_API_KEY")

# OpenAI 클라이언트 생성
client = OpenAI(api_key=api_key)

# 같은 프롬프트로 temperature 값에 따른 차이 비교
prompt = "새로운 SF 소설의 도입부를 세 문장으로 써줘."


def generate_story(temperature: float) -> str:
    response = client.responses.create(
        model="gpt-4.1-nano",
        input=prompt,
        temperature=temperature,
        top_p=1.0,
        max_output_tokens=120,
    )

    return response.output_text.strip()


# 1. 안정적인 설정
result_stable = generate_story(temperature=0.0)

# 2. 다양한 표현을 유도하는 설정
result_creative = generate_story(temperature=0.8)

print("=== temperature = 0.0 ===")
print(result_stable)

print("\n" + "-" * 50 + "\n")

print("=== temperature = 0.8 ===")
print(result_creative)