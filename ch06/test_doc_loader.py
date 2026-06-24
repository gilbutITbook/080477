from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredMarkdownLoader
)
import os

# PDF 로딩
if os.path.exists("sample_document.pdf"):
    pdf_loader = PyPDFLoader("sample_document.pdf")  # ➊
    pdf_documents = pdf_loader.load()

    print(f"PDF 로드 후 문서 개수: {len(pdf_documents)}")

    if pdf_documents:
        print("--- PDF 첫 페이지 메타데이터 ---")
        print(pdf_documents[0].metadata)
else:
    print("sample_document.pdf 파일을 찾을 수 없습니다.")

# 마크다운 파일 로딩
if os.path.exists("sample_blog_post.md"):
    md_loader = UnstructuredMarkdownLoader("sample_blog_post.md")  # ➋
    md_documents = md_loader.load()

    print(f"\n마크다운 파일 로드 후 문서 개수: {len(md_documents)}")

    if md_documents:
        print("--- 마크다운 파일 첫 번째 내용(일부) ---")
        print(md_documents[0].page_content[:200])
else:
    print("sample_blog_post.md 파일을 찾을 수 없습니다.")