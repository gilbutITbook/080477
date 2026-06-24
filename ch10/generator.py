import os
from typing import Any, Dict, List

import requests
from openai import OpenAI

from document import Document

class Generator:
    """검색 결과를 기반으로 답변을 생성하는 클래스"""

    def __init__(self, config: Dict[str, Any]):
        self.model_name = config.get("model_name", "gpt-4.1-mini")
        self.llm_type = config.get("llm_type", "openai")
        self.temperature = config.get("temperature", 0.1)

        if self.llm_type == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
            self.client = OpenAI(api_key=api_key)

        self.prompt_template = """
### Instruction:
당신은 사용자의 질문에 대해 주어진 Context 정보만을 사용해 답변하는 AI 어시스턴트입니다.

- 반드시 Context에 명시된 내용에 근거해 답변해야 합니다.
- Context에 답이 없는 경우 "제공된 정보만으로는 답변할 수 없습니다."라고 답변합니다.
- 절대로 사전 지식을 사용하거나 정보를 지어내지 마세요.
- 답변은 한국어로 명확하고 간결하게 작성해 주세요.

### Context:
{context}

### User Question:
{question}

### Answer:
"""

    def _format_context(self, context_docs: List[Document]) -> str:
        """검색된 Document 리스트를 하나의 문자열로 변환"""
        return "\n\n---\n\n".join(
            [doc.page_content for doc in context_docs]
        )

    def format_prompt(
        self,
        query: str,
        context_docs: List[Document]
    ) -> str:
        """최종 프롬프트 생성"""
        formatted_context = self._format_context(context_docs)

        return self.prompt_template.format(
            context=formatted_context,
            question=query
        )

    def generate(
        self,
        query: str,
        context_docs: List[Document]
    ) -> str:
        """LLM API를 호출해 답변 생성"""
        final_prompt = self.format_prompt(query, context_docs) # ➊
        if self.llm_type == "openai": # ➋
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {
                            "role": "user",
                            "content": final_prompt
                        }
                    ],
                    temperature=self.temperature
                )
                return response.choices[0].message.content
            except Exception as e:
                return f"OpenAI API 호출 중 오류 발생: {e}"
        elif self.llm_type == "ollama": # ➌
            try:
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": self.model_name,
                        "prompt": final_prompt,
                        "stream": False
                    },
                    timeout=60
                )
                response.raise_for_status()
                return response.json()["response"]
            except Exception as e:
                return f"Ollama API 호출 중 오류 발생: {e}"
        return "지원하지 않는 LLM 타입입니다."