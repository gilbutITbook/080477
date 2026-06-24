import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY가 설정되어 있지 않습니다.")

client = OpenAI(api_key=api_key)

# ➊ 시스템 프롬프트: 역할 정의
system_prompt = """
너는 20년 경력의 파이썬 시니어 개발자야.
성능, 가독성, 안전성 기준으로 코드 리뷰를 수행해.
반드시 다음 JSON 형식으로만 답해.
{
  "summary": "string",
  "issues": [{"title": "string", "evidence": "string"}],
  "suggestions": [{"before": "string", "after": "string", "rationale": "string"}]
}
추측하지 말고 근거를 포함해.
"""

# ➋ 사용자 프롬프트: 작업 요청
user_prompt = """
다음 함수를 개선해 주세요.
def f(arr):
    out = []
    for x in arr:
        out.append(x*x)
    return out
"""

try:
    # ➌ API 호출
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    # ➍ JSON 파싱
    data = json.loads(response.output_text)

    print("\n--- 코드 리뷰 결과 ---")
    print(json.dumps(data, indent=2, ensure_ascii=False))

except Exception as e:
    print(f"\n[오류] API 호출 중 문제 발생: {e}")