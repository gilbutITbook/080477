import os
import psycopg2
#import psycopg2.extras 
from openai import OpenAI
from psycopg2.extras import RealDictCursor
from typing import List, Any, Dict
from document import Document
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")

class Retriever:
    """PostgreSQL/PGVector 데이터베이스에서 문서를 검색하는 클래스 """
    def __init__(self, config: Dict[str, Any]): 
        """설정 딕셔너리를 받아 초기화"""
        self.db_config = config['db_config']
        self.embedding_model = config.get('embedding_model', "text-embedding-3-small")
        self.top_k = config.get('top_k', 5)
        
        # API Key는 환경 변수에서 로드
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.embedding_cache = {}

    def _get_embedding(self, text: str) -> List[float]: 
        """텍스트를 임베딩 벡터로 변환하는 private 헬퍼 메서드(캐시 적용)"""
        if text in self.embedding_cache:
            return self.embedding_cache[text]

        response = self.client.embeddings.create(
            input=[text],
            model=self.embedding_model
        )
        embedding = response.data[0].embedding
        self.embedding_cache[text] = embedding
        return embedding
    def retrieve(self, query: str, top_k: int = None) -> list[Document]:
        """metadata 칼럼을 조회하고, 이를 Document 객체에 포함"""
        if top_k is None:
            top_k = self.top_k
        query_vector = self._get_embedding(query)
        # SQL 쿼리에 metadata 칼럼 추가
        sql_query = """
            SELECT id, content, metadata, (embedding <=> %s::vector) AS distance
            FROM documents 
            ORDER BY distance 
            LIMIT %s
        """
        params = (str(query_vector), top_k)
        results = []
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(sql_query, params)
                    fetched_rows = cur.fetchall()
                    for row in fetched_rows:
                        # DB에서 가져온 메타데이터 활용
                        # DB에 저장된 metadata(딕셔너리)를 가져오고 없으면 빈 딕셔너리.
                        doc_metadata = row.get("metadata") or {}                     
                        # 검색 정보(id, distance)를 기존 메타데이터에 추가(병합)
                        doc_metadata["id"] = row["id"]
                        doc_metadata["distance"] = row["distance"]                    
                        doc = Document(
                            page_content=row["content"],
                            metadata=doc_metadata, # 수정된 메타데이터 전달
                            score=1 - row["distance"]
                        )
                        results.append(doc)
        except Exception as e:
            print(f"Retriever DB 작업 중 오류 발생: {e}")
            return []            
        return results
