from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,                    # 청크의 최대 길이
    chunk_overlap=50,                  # 청크 간 겹치는 길이
    separators=["\n\n", "\n", " ", ""] # 분리 기준 우선순위
)
long_text = "첫 번째 문단입니다. 이 문단은 여러 문장으로 구성됩니다.\n\n두 번째 문단입니다. 이 문단 또한 마찬가지입니다."
chunks = text_splitter.split_text(long_text)
for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i+1} ---")
    print(chunk)
