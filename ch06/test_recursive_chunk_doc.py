from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredMarkdownLoader,
)

from langchain_text_splitters import RecursiveCharacterTextSplitter


def build_chunks():
    # 1단계: 문서 로딩
    pdf_loader = PyPDFLoader("sample_document.pdf")
    pdf_documents = pdf_loader.load()

    print(f"PDF 로드 후 문서 개수: {len(pdf_documents)}")

    md_loader = UnstructuredMarkdownLoader("sample_blog_post.md")
    md_documents = md_loader.load()

    print(f"마크다운 파일 로드 후 문서 개수: {len(md_documents)}")

    # 2단계: 문서 통합
    all_documents = pdf_documents + md_documents

    # 3단계: 청킹
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""], # 문단 → 줄 → 단어 → 문자 순서
        chunk_size=1000,     # 청크 최대 길이
        chunk_overlap=150,   # 청크 간 겹치는 길이
        length_function=len, # 길이 기준(문자 수)
    )

    chunks = text_splitter.split_documents(all_documents)

    print(f"생성된 청크 개수: {len(chunks)}")

    # 4단계: 메타데이터 보강
    chunks = enrich_chunk_metadata(chunks)

    return chunks


def enrich_chunk_metadata(docs):
    enriched = []

    for i, d in enumerate(docs):
        md = dict(d.metadata) if d.metadata else {}

        md["chunk_index"] = i
        md.setdefault("source", md.get("file_path", "unknown"))
        md.setdefault("page", md.get("page", None))

        md["chunk_id"] = f"{md['source']}#p{md['page']}#c{i}"

        d.metadata = md
        enriched.append(d)

    return enriched


chunks = build_chunks()

if chunks:
    print("--- 첫 번째 청크 미리보기 ---")
    print(chunks[0].page_content[:300])
    print("메타데이터:", chunks[0].metadata)
else:
    print("생성된 청크가 없습니다.")