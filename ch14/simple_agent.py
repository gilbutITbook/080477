import re
import os
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from openai import OpenAI

load_dotenv()

# ➊ 도구 정의 (실제 웹 검색 연동)
def web_search(query: str) -> str:
    """DuckDuckGo를 이용해 실제 웹 검색을 수행하는 도구"""

    print(f"--- Executing web_search(query='{query}') ---")

    try:
        # DuckDuckGo 검색 수행
        with DDGS() as ddgs:
            # 상위 3개 검색 결과만 가져오기
            results = list(ddgs.text(query, max_results=3))
        if not results:
            return "No information found."
        # 검색 결과를 LLM이 읽기 쉬운 형태로 정리
        snippets = []
        for i, res in enumerate(results, 1):
            title = res.get("title", "No title")
            body = res.get("body", "")
            snippets.append(
                f"[Result {i}] Title: {title}\n"
                f"Snippet: {body}"
            )
        return "\n\n".join(snippets)

    except Exception as e:
        return f"Error occurred during web search: {str(e)}"


# ➋ ReAct 프롬프트 정의
REACT_PROMPT_TEMPLATE = """
You are an agent that uses tools to answer questions.

Available tools:
- web_search(query: str)

Follow this format strictly:

Question: {question}
Thought: reasoning about what to do next
Action: web_search
Action Input: input for the tool
Observation: result of the tool
... (repeat as needed)
Thought: I now know the final answer
Final Answer: final answer to the question

{scratchpad}
"""

class SimpleAgent:
    def __init__(self, model="gpt-4.1-mini"):
        self.client = OpenAI()
        self.model = model

    def run(self, question: str):
        scratchpad = ""  # ➊ 단기 메모리 초기화
        max_loops = 5    # ➋ 반복 제한

        for i in range(max_loops):
            # ➌ 프롬프트 생성
            prompt = REACT_PROMPT_TEMPLATE.format(
                question=question,
                scratchpad=scratchpad
            )

            print("--- Sending prompt to LLM ---")

            # ➍ LLM 호출
            response = self.client.responses.create(
                model=self.model,
                input=prompt,
            )

            output = response.output_text

            print("\n--- LLM Response(Thought Process) ---")
            print(output)

            # ➎ 종료 조건 확인
            if "Final Answer:" in output:
                print("\n--- Agent Finished ---")
                return output.split("Final Answer:")[-1].strip()

            # ➏ Action 파싱
            action_match = re.search(r"Action:\s*(.*)", output)
            input_match = re.search(r"Action Input:\s*(.*)", output)

            if not action_match or not input_match:
                print("Action 파싱 실패")
                return None

            action = action_match.group(1).strip()
            action_input = input_match.group(1).strip()

            # ➐ 도구 실행
            if action == "web_search":
                observation = web_search(query=action_input)
            else:
                observation = "Unknown action"

            # ➑ 메모리 업데이트
            scratchpad += f"\n{output}\nObservation: {observation}\n"

        print("\n--- Max steps reached ---")
        return "The agent stopped because it reached the maximum number of steps."


if __name__ == "__main__":
    agent = SimpleAgent()
    goal = "서울시의 최근 인구 수와 외국인들이 가장 많이 방문한 관광지는 어디인가요?"
    answer = agent.run(goal)
    print("\nFinal Answer:")
    print(answer)