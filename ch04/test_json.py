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

# 프롬프트 정의
prompt = """
다음 이메일 내용을 분석해 JSON 형식으로 정리해 주세요.

Email:
"안녕하세요, 저는 김철수입니다. 3/16/2026에 구매한 노트북을 사용 중인데,
배터리가 너무 빨리 닳아서 업무에 큰 지장을 받고 있습니다.
빠른 해결을 요청드립니다."
"""

try:
    response = client.responses.create(  # ➊
        model="gpt-4o-mini",
        input=prompt,
        text={
            "format": {  # ➋
                "type": "json_schema",  # ➌
                "name": "customer_issue",
                "schema": {
                    "type": "object",
                    "properties": {
                        "sender": {"type": "string"},
                        "issue_date": {"type": "string"},
                        "main_issue": {"type": "string"},
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high"]
                        }
                    },
                    "required": [
                        "sender",
                        "issue_date",
                        "main_issue",
                        "priority"
                    ],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
    )

    print("--- LLM JSON 응답 ---")

    json_text = response.output_text  # ➍
    print(json_text)

    # JSON 파싱
    data = json.loads(json_text)  # ➎

    print("\n--- 파싱된 JSON 데이터 ---")
    print("발신자:", data["sender"])
    print("문제:", data["main_issue"])
    print("우선순위:", data["priority"])

except Exception as e:
    print(f"\n[오류] API 호출 중 문제 발생: {e}")