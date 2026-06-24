import os
from dotenv import load_dotenv
import json
from openai import OpenAI
from tools import get_current_weather, tools_spec

# .env 파일 로드
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY 환경 변수가 설정되어 있지 않습니다.")

client = OpenAI(api_key=api_key)

def run_conversation(user_prompt: str) -> None:
    # ➊ 입력 메시지 준비
    input_items = [{"role": "user", "content": user_prompt}]
    print(f"User: {user_prompt}")
    # ➋ 1차 요청: 사용자 질문 + 도구 명세 전달
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=input_items,
        tools=tools_spec,
    )
    # ➌ 모델이 반환한 출력 항목을 이후 단계에서도 유지
    input_items += response.output
    # ➍ function_call 항목을 찾아 실제 함수 실행
    tool_called = False

    for item in response.output:
        if item.type != "function_call":
            continue
        tool_called = True
        function_name = item.name
        try:
            function_args = json.loads(item.arguments)
        except json.JSONDecodeError:
            function_args = {}
        print("[INFO] LLM이 도구 호출을 요청했습니다.")
        print(f"[DEBUG] 함수: {function_name}, 인자: {function_args}")
        if function_name == "get_current_weather":
            location = function_args.get("location")
            if not location:
                function_result = json.dumps({
                    "error": "location 값이 필요합니다."
                })
            else:
                function_result = get_current_weather(location=location)
            # ➎ 실행 결과를 function_call_output으로 다시 전달
            input_items.append(
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": function_result,
                }
            )

    # ➏ 도구 호출이 있었다면 2차 요청으로 최종 응답 생성
    if tool_called:
        print("[INFO] 도구 실행 결과를 바탕으로 최종 답변을 요청합니다.")

        final_response = client.responses.create(
            model="gpt-4o",
            input=input_items,
            tools=tools_spec,
        )
        print(f"Bot: {final_response.output_text}")
    else:
        print(f"Bot: {response.output_text}")

# 테스트 실행
if __name__ == "__main__":
    run_conversation("What's the weather like in Seoul?")