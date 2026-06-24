import requests
from typing import List, Dict, Any

from document import Document


class Generator:
    """검색된 컨텍스트와 질문을 바탕으로 Ollama API를 호출해 응답을 생성하는 클래스"""

    def __init__(self, config: Dict[str, Any]):
        """설정 딕셔너리를 받아 초기화"""

        # [변경] OpenAI 모델 대신 Ollama 로컬 모델 사용
        self.model_name = config.get(
            "model_name",
            "llama3"
        )
        # [변경] OpenAI API 대신 Ollama 로컬 API 주소 사용
        self.base_url = "http://localhost:11434/api/generate"
        # 기존 프롬프트 템플릿 재사용
        self.prompt_template = config.get(
            "prompt_template",
            ""
        )

    def _format_context(
        self,
        context_docs: List[Document]
    ) -> str:
        """검색된 문서 조각들을 하나의 문자열로 결합"""

        if not context_docs:
            return ""

        # 문서 간 경계를 명확히 하기 위해 구분자 사용
        return "\n\n---\n\n".join(
            doc.page_content for doc in context_docs
        )

    def format_prompt(
        self,
        query: str,
        context_docs: List[Document]
    ) -> str:
        """프롬프트 템플릿에 데이터 주입"""

        formatted_context = self._format_context(
            context_docs
        )

        return self.prompt_template.format(
            context=formatted_context,
            question=query
        )

    def generate(
        self,
        query: str,
        context_docs: List[Document]
    ) -> str:
        """Ollama API를 호출해 최종 응답 생성"""

        # 프롬프트 생성
        final_prompt = self.format_prompt(
            query,
            context_docs
        )

        # [변경] Ollama API 요청 데이터 구성
        payload = {
            "model": self.model_name,
            "prompt": final_prompt,

            # [변경] 스트리밍 대신 완성된 응답을 한 번에 반환
            "stream": False
        }

        try:
            # [변경] OpenAI SDK 대신 requests.post() 사용
            response = requests.post(
                self.base_url,
                json=payload,
                timeout=120
            )

            # HTTP 오류 발생 시 예외 처리
            response.raise_for_status()

            # JSON 응답 파싱
            result = response.json()

            # [변경] Ollama 응답의 response 필드 사용
            return result.get(
                "response",
                "응답을 생성하지 못했습니다."
            )

        # [변경] 로컬 서버 연결 오류 처리
        except requests.exceptions.RequestException as e:
            return f"Ollama 서버 연결 오류: {e}"

        except Exception as e:
            return f"응답 생성 중 알 수 없는 오류 발생: {e}"