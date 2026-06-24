import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

messages = [
    {
        "role": "user", 
        "content": "파이썬의 장점을 세 문장으로 설명해줘."
    }
]

try:
    # 1. 기본 설정(페널티 없음)
    resp_default = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.0,
        max_tokens=150
    )

    # 2. 페널티 적용
    resp_penalty = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.0,
        max_tokens=150,
        presence_penalty=0.6,
        frequency_penalty=0.6
    )

    print("\n=== 기본 설정 ===")
    print(resp_default.choices[0].message.content.strip())

    print("\n=== 페널티 적용 ===")
    print(resp_penalty.choices[0].message.content.strip())

except Exception as e:
    print(f"\n[오류] API 호출 중 문제 발생: {e}")