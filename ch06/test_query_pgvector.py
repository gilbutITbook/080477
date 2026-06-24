import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 검색할 질의 문장
query = "파이썬으로 데이터 로딩"

# 임베딩 생성
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=query
)

query_embedding = response.data[0].embedding

print(f"벡터 차원 수: {len(query_embedding)}")
print(query_embedding[:10])  # 앞부분 일부만 출력