import sys
from unittest.mock import MagicMock

# vertexai 모듈 경로를 Mock으로 대체
sys.modules['langchain_community.chat_models.vertexai'] = MagicMock()

from ragas import evaluate

import os
import pandas as pd
from datasets import Dataset
from dotenv import load_dotenv
from ragas import evaluate
from ragas.metrics import Faithfulness, AnswerRelevancy
from langchain_openai import OpenAIEmbeddings

load_dotenv()
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

eval_data = {
    "question": ["RAG에서 청킹이란 무엇이고 왜 중요한가요?"],
    "contexts": [[
        "청킹은 긴 문서를 작은 조각으로 나누는 과정입니다. "
        "이는 LLM의 컨텍스트 윈도우 한계를 극복하고 "
        "검색 정확도를 높이기 때문에 중요합니다."
    ]],
    "answer": [
        "청킹은 문서를 작은 조각으로 나누는 것을 의미하며 "
        "LLM의 컨텍스트 제한과 검색 성능 때문에 중요합니다."
    ],
    "ground_truth": [
        "청킹은 긴 문서를 의미 단위로 나누는 과정이며, "
        "컨텍스트 길이 제한을 해결하고 검색 정확도를 높이기 때문에 "
        "RAG에서 중요하다."
    ],
}

dataset = Dataset.from_pandas(pd.DataFrame(eval_data))
result = evaluate(dataset=dataset, metrics=[Faithfulness(), AnswerRelevancy()], embeddings=embeddings,)
print(result)