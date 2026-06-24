import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# 환경 설정
load_dotenv()
client = OpenAI()

# 실제 파이썬 함수 정의
def get_current_weather(location: str):
    if location == "도쿄":
        return {"temperature": "18°C", "unit": "celsius", "condition": "맑음"}
    return {"temperature": "N/A", "unit": "N/A", "condition": "정보 없음"}


def search_flights(destination: str):
    if destination == "도쿄":
        return [
            {"flight_number": "KE703", "price": "35만 원"},
            {"flight_number": "OZ104", "price": "42만 원"},
        ]
    return []


# 함수 이름과 실제 파이썬 함수를 매핑하는 딕셔너리
available_functions = {
    "get_current_weather": get_current_weather,
    "search_flights": search_flights,
}

# Tool 정의
tools = [
    {
        "type": "function",
        "name": "get_current_weather",
        "description": "특정 도시의 현재 날씨를 조회합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "도시 이름(예: 도쿄)",
                }
            },
            "required": ["location"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "search_flights",
        "description": "특정 목적지로 가는 항공권 정보를 검색합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "destination": {
                    "type": "string",
                    "description": "여행 목적지(예: 도쿄)",
                }
            },
            "required": ["destination"],
            "additionalProperties": False,
        },
    },
]


def run_tool_use(user_query: str) -> str:
    input_items = [{"role": "user", "content": user_query}]

    # 1단계: LLM 1차 호출(필요한 도구 판단)
    response = client.responses.create(
        model="gpt-4o",
        input=input_items,
        tools=tools,
        temperature=0,
    )

    function_calls = [
        item for item in response.output
        if item.type == "function_call"
    ]

    if not function_calls:
        return response.output_text

    print("\n[단계 1 완료] LLM이 Function Call을 요청했습니다.")

    # 2단계: Function Call 확인 및 실제 함수 실행
    tool_outputs = []

    for call in function_calls:
        function_name = call.name
        function_args = json.loads(call.arguments)

        if function_name not in available_functions:
            raise ValueError(f"정의되지 않은 함수입니다: {function_name}")

        function_to_call = available_functions[function_name]
        function_response = function_to_call(**function_args)

        print(f"  -> 함수 실행 완료: {function_name}({function_args})")

        tool_outputs.append(
            {
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": json.dumps(function_response, ensure_ascii=False),
            }
        )

    print("\n[단계 2] 함수 실행 결과를 포함해 최종 응답을 요청합니다.")

    # 3단계: 2차 호출(함수 결과를 반영해 최종 답변 생성)
    final_response = client.responses.create(
        model="gpt-4o",
        previous_response_id=response.id,
        input=tool_outputs,
        tools=tools,
        temperature=0,
    )

    return final_response.output_text


if __name__ == "__main__":
    user_query = "도쿄 날씨와 항공권 정보를 알려줘."

    try:
        final_answer = run_tool_use(user_query)

        print("\n==================================================")
        print(f"사용자 질문: {user_query}")
        print("==================================================")
        print("[최종 LLM 답변]")
        print(final_answer)

    except Exception as e:
        print(f"\n[오류] Tool Use 워크플로 실행 중 문제 발생: {e}")