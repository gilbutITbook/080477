import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# 프롬프트 정의
prompt = """
다음 문제를 단계별로 계산하고 결과를 JSON 형식으로 출력해줘.

출력 형식:
{
  "inputs": "...",
  "intermediate": "...",
  "final": "...",
  "rationale": "..."
}

문제:
A: 기본 10GB, 초과 1GB당 5000원
B: 기본 20GB, 초과 1GB당 4000원
사용량: 25GB

각 요금제의 총 비용을 계산하고 더 저렴한 요금제를 판단해줘.
"""

response = client.responses.create(
    model="gpt-4o-mini",
    input=prompt,
    text={
        "format": {
            "type": "json_schema",
            "name": "plan_comparison",
            "schema": {
                "type": "object",
                "properties": {
                    "inputs": {"type": "string"},
                    "intermediate": {"type": "string"},
                    "final": {"type": "string"},
                    "rationale": {"type": "string"}
                },
                "required": ["inputs", "intermediate", "final", "rationale"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
)

json_text = response.output_text.strip()
data = json.loads(json_text)

print("\n--- LLM JSON 응답 ---")
print(json_text)

print("\n[INFO] 최종 결과:", data["final"])
print("[INFO] 근거:", data["rationale"])