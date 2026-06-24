import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def get_embedding(text: str, model: str = "text-embedding-3-small") -> list:
    """텍스트를 벡터로 변환"""
    response = client.embeddings.create(
        model=model,
        input=text
    ) # ➊
    return response.data[0].embedding # ➋