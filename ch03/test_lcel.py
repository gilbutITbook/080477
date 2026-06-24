import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# .env 파일 로드
load_dotenv()

# 1. 프롬프트 생성
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 사용자 입력을 30자 이내로 간결하게 요약하는 전문가입니다."),
    ("user", "다음 주제를 요약해 주세요. -> {topic}")
])

# 2. 모델 설정 (경량 모델 사용)
llm = ChatOpenAI(
    model="gpt-4.1-nano",
    temperature=0.0
)

# 3. 출력 파서
parser = StrOutputParser()

# 4. LCEL 체인 구성
chain = prompt | llm | parser

# 입력 데이터
input_data = {
    "topic": "The importance of large language models in modern software development."
}

print(f"사용자 입력: {input_data['topic']}")

try:
    # 체인 실행
    result = chain.invoke(input_data)

    print("\n[LCEL 체인 응답]")
    print(result)

except Exception as e:
    print(f"\n[오류] 체인 실행 중 문제가 발생했습니다: {e}")