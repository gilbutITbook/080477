import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# 예시 기반 프롬프트 (Few-shot)
prompt = """
고객 문의 내용을 분석해 '문의 유형'과 '긴급도'를 JSON 형식으로 분류해줘.
반드시 JSON 객체만 출력해야 해.

[예시 1]
이메일: "비밀번호를 잃어버렸어요. 초기화 좀 해주세요."
결과: {"type": "계정 문의", "priority": "중간"}

[예시 2]
이메일: "결제가 안 돼요! 지금 빨리 처리해주지 않으면 서비스를 해지할 겁니다."
결과: {"type": "결제 오류", "priority": "높음"}

[예시 3]
이메일: "서비스 잘 쓰고 있습니다. 혹시 A 기능도 추가할 계획이 있나요?"
결과: {"type": "기능 제안", "priority": "낮음"}

[실제 문제]
이메일: "로그인이 안 돼서 급한 업무를 못 보고 있어요. 확인 부탁드립니다."
결과:
"""

try:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    json_text = response.output_text.strip()

    if json_text.startswith("```"):
        json_text = json_text.split("```")[1]
        if json_text.startswith("json"):
            json_text = json_text[4:]
        json_text = json_text.strip()
        
    parsed_data = json.loads(json_text)

    print("\n--- LLM JSON 응답(분류 결과) ---")
    print(json_text)

    print("\n[INFO] 문의 유형:", parsed_data["type"])
    print("[INFO] 긴급도:", parsed_data["priority"])

except Exception as e:
    print(f"\n[오류] API 호출 중 문제 발생: {e}")