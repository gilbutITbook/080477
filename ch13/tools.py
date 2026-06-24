import json
import requests

# ➊ 실제 실행할 로컬 함수 정의 (wttr.in API 사용)
def get_current_weather(location: str) -> str:
    """주어진 위치의 현재 날씨 정보를 가져오는 함수"""

    # wttr.in 서비스에 JSON 형식(format=j1)으로 요청
    url = f"https://wttr.in/{location}?format=j1"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        # LLM이 이해하기 쉽도록 핵심 정보만 추출
        current_condition = data["current_condition"][0]
        weather_info = {
            "location": location.title(),
            "temperature": current_condition["temp_C"],
            "condition": current_condition["weatherDesc"][0]["value"]
        }
        # 도구 실행 결과를 JSON 문자열 형태로 반환
        return json.dumps(weather_info)

    except requests.exceptions.RequestException as e:
        return json.dumps({
            "location": location,
            "error": f"날씨 정보를 가져오지 못했습니다: {str(e)}"
        })

# ➋ 도구 명세(tool specification)
tools_spec = [
    {
        "type": "function",
        "name": "get_current_weather",        # ← 바깥으로 이동
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name, e.g. Seoul"
                }
            },
            "required": ["location"]
        }
    }
]