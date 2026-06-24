import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

try:
    print("\n--- API 호출 (stop=['---']) ---")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "파이썬의 장점 3가지를 각각 한 문장으로 설명하고, 각 항목 끝에 '---'를 붙여줘."
            }
        ],
        temperature=0.0,
        stop=["---"]
    )
    generated_text = response.choices[0].message.content
    print("모델 출력:")
    print(generated_text)
    print(f"\nFinish Reason(중단 이유): {response.choices[0].finish_reason}")

except Exception as e:
    print(f"\n[오류] API 호출 중 문제가 발생했습니다: {e}")