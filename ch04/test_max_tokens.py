from openai import OpenAI
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# OpenAI 클라이언트 생성
client = OpenAI()

# JSON 생성 요청
prompt = """
책 제목 3개를 JSON 배열로 반환하세요.
각 항목은 {"title": "...", "reason": "..."} 형태로 작성하세요.
"""

# 1. 응답 길이가 부족한 경우
print("\n=== max_tokens 작음 (40) ===")

resp_small = client.responses.create(
    model="gpt-4o-mini",
    input=prompt,
    temperature=0.0,
    max_output_tokens=40
)

print("status:", resp_small.status)
print("incomplete_details:", resp_small.incomplete_details)
print(resp_small.output_text)

# 2. 충분한 응답 길이
print("\n=== max_tokens 충분 (200) ===")

resp_ok = client.responses.create(
    model="gpt-4o-mini",
    input=prompt,
    temperature=0.0,
    max_output_tokens=200
)

print("status:", resp_ok.status)
print("incomplete_details:", resp_ok.incomplete_details)
print(resp_ok.output_text)