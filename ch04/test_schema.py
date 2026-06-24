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
다음 사용자 리뷰를 분석해 JSON 형식으로 정리해 주세요.

User Review:
배송은 빨라서 좋았는데, 막상 써보니 배터리가 너무 빨리 닳네요.
배터리 시간만 좀 늘려주면 완벽할 것 같아요.
"""

try:
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "review_analysis",
                "schema": {
                    "type": "object",
                    "properties": {
                        "sentiment": {
                            "type": "string",
                            "enum": ["positive", "negative", "neutral"]
                        },
                        "key_issues": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "suggested_improvement": {
                            "type": ["string", "null"]
                        }
                    },
                    "required": [
                        "sentiment",
                        "key_issues",
                        "suggested_improvement"
                    ],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
    )

    print("--- LLM JSON 응답 ---")

    json_text = response.output_text
    print(json_text)

    # JSON 파싱
    parsed_data = json.loads(json_text)

    print("\n--- 파싱된 JSON 데이터 ---")
    print(json.dumps(parsed_data, indent=2, ensure_ascii=False))

except Exception as e:
    print(f"\n[오류] API 호출 중 문제 발생: {e}")