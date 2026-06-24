from typing import Iterator

def generate_stream(
    self,
    query: str,
    context_docs: List[Document]
) -> Iterator[str]:  # ➊ 문자열을 순차적으로 반환하는 스트리밍 함수

    # ➋ 최종 프롬프트 생성
    final_prompt = self.format_prompt(
        query,
        context_docs
    )
    # ➌ 스트리밍 세션 시작
    with self.client.responses.stream(
        model=self.model_name,
        input=final_prompt,
        temperature=0.1,
    ) as stream:
        # ➍ 서버 이벤트를 순차 처리
        for event in stream:
            # ➎ 생성 중인 텍스트 조각만 처리
            if event.type == "response.output_text.delta":
                if event.delta:
                    # ➏ 생성된 텍스트를 즉시 반환
                    yield event.delta