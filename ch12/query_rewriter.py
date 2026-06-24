from openai import OpenAI
from typing import List, Tuple


class QueryRewriter:
    """대화 이력을 바탕으로 후속 질문을 독립형 질문으로 재작성하는 클래스"""

    def __init__(
        self,
        model_name: str = "gpt-4.1-mini",
        api_key: str = None
    ):
        self.model_name = model_name
        self.client = OpenAI(api_key=api_key)

        self.prompt_template = """
### Instruction:
당신의 임무는 주어진 대화 이력(Chat History)을 참고해
문맥을 모르는 사람도 사용자의 후속 질문(Follow-up Question)을 이해할 수 있는
독립형 질문(Standalone Question)으로 재작성하는 것입니다.

- 후속 질문이 이미 독립적이라면 내용을 변경하지 말고 그대로 반환하세요.
- 대명사(예: 그, 그것, 저것)를 구체적인 명사로 바꾸세요.
- 재작성된 질문은 검색 엔진에 바로 입력할 수 있을 정도로 명확해야 합니다.

### Chat History:
{chat_history}

### Follow-up Question:
{question}

### Standalone Question:
"""

    def _format_chat_history(
        self,
        chat_history: List[Tuple[str, str]]
    ) -> str:
        """(질문, 답변) 기록을 문자열 형태로 변환"""

        if not chat_history:
            return "No history provided."

        return "\n".join(
            [f"Human: {q}\nAI: {a}" for q, a in chat_history]
        )

    def rewrite(
        self,
        question: str,
        chat_history: List[Tuple[str, str]]
    ) -> str:
        """쿼리 재작성 수행"""

        formatted_history = self._format_chat_history(chat_history)

        prompt = self.prompt_template.format(
            chat_history=formatted_history,
            question=question
        )

        try:
            response = self.client.responses.create(
                model=self.model_name,
                input=prompt,
                temperature=0.0
            )

            rewritten_question = response.output_text.strip()

            return rewritten_question

        except Exception as e:
            print(f"쿼리 재작성 API 호출 중 오류 발생: {e}")
            return question