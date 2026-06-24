import os
from openai import OpenAI
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# OpenAI 클라이언트 생성
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# LLM이 사용할 수 있는 도구 정의
tool_definitions = [
    {
        "type": "function",
        "name": "get_weather_forecast",                          
        "description": "특정 도시의 현재 날씨 정보를 가져옵니다.",   
        "parameters": {                                          
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "날씨를 확인할 도시 이름 (예: 서울, 부산)"
                }
            },
            "required": ["city"]
        }
    }
]


def check_for_tool_call(user_query: str):
    """LLM 응답을 분석해 Tool Use 여부를 확인"""
    print(f"\n사용자 질문: {user_query}")

    response = client.responses.create(
        model="gpt-4.1-nano",
        input=user_query,
        tools=tool_definitions,
        temperature=0.0
    )

    # 토큰 사용량 출력
    print(f"총 토큰 사용량: {response.usage.total_tokens}")

    # 응답 분석
    for item in response.output:
        
        # Tool Call 발생
        if item.type == "function_call":
            print("\n[Tool Call 요청 감지]")
            print(f" - 호출 함수: {item.name}")
            print(f" - 인수: {item.arguments}")

        # 일반 텍스트 응답
        elif item.type == "message":
            print("\n[일반 텍스트 응답]")
            print(item.content[0].text)


# 실행
try:
    check_for_tool_call("오늘 서울 날씨가 어때?")
    check_for_tool_call("TCP와 UDP 차이를 설명해줘.")

except Exception as e:
    print(f"\n[오류] API 호출 중 문제가 발생했습니다: {e}")