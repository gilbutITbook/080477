import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

from test_recursive_chunk_doc import build_chunks


load_dotenv()

# 클라이언트 초기화
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Pinecone 인덱스 연결
index = pc.Index("my-vector-index")

# 6.5.3절에서 생성한 청크 가져오기
chunks = build_chunks()


def get_embedding(text: str) -> List[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


vectors: List[Dict[str, Any]] = []

for i, chunk in enumerate(chunks):
    text = chunk.page_content

    if not text or not text.strip():
        continue

    embedding = get_embedding(text)

    metadata = dict(chunk.metadata) if chunk.metadata else {}
    metadata.setdefault("preview", text[:200])
    metadata.setdefault("source", metadata.get("source", "unknown"))
    metadata.setdefault("chunk_index", i)

    clean_metadata = {
        key: value for key, value in metadata.items()
        if value is not None
    }

    vectors.append({
        "id": f"id-{i}",
        "values": embedding,
        "metadata": clean_metadata,
    })

if vectors:
    index.upsert(vectors=vectors)
    print(f"{len(vectors)}개 벡터 업로드 완료!")
else:
    print("업로드할 데이터가 없습니다.")


query = "벡터 데이터베이스란?"

query_embedding = client.embeddings.create(
    model="text-embedding-3-small",
    input=query
).data[0].embedding

results = index.query(
    vector=query_embedding,
    top_k=2,
    include_metadata=True
)

matches = (
    results.get("matches", [])
    if isinstance(results, dict)
    else getattr(results, "matches", [])
)

for match in matches:
    score = (
        match.get("score", 0.0)
        if isinstance(match, dict)
        else getattr(match, "score", 0.0)
    )

    metadata = (
        match.get("metadata", {})
        if isinstance(match, dict)
        else getattr(match, "metadata", {})
    ) or {}

    preview = metadata.get("preview", "")
    source = metadata.get("source", "unknown")

    print(f"유사도 점수: {score:.3f}, 출처: {source}")
    print(f"미리보기: {preview[:100]}")