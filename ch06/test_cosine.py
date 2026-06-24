import numpy as np
from numpy.linalg import norm

# 코사인 유사도 계산 함수
def cosine_similarity(vec_a: list, vec_b: list) -> float:
    """두 벡터 간 코사인 유사도 계산"""
    # NumPy 배열로 변환
    vec_a_np = np.array(vec_a)
    vec_b_np = np.array(vec_b)
    # 코사인 유사도 공식: np.dot (A, B) / (||A|| * ||B||)
    # np.dot(A, B): 두 벡터의 곱을 모두 더한 값(내적)
    # norm(A): 벡터의 길이(크기)
    return np.dot(vec_a_np, vec_b_np) / (norm(vec_a_np) * norm(vec_b_np)) # ❶

# 비교할 문장
sentence1 = "오늘 서울의 날씨는 어때?"
sentence2 = "서울의 현재 기상 상태를 알려줘."
sentence3 = "AI 기술의 미래 전망은 밝다."

# 임베딩 벡터 생성
print("임베딩 벡터 생성 중...")
vector1 = get_embedding(sentence1)
vector2 = get_embedding(sentence2)
vector3 = get_embedding(sentence3)
print("임베딩 벡터 생성 완료.")

# 코사인 유사도 계산
sim_1_2 = cosine_similarity(vector1, vector2)
sim_1_3 = cosine_similarity(vector1, vector3)
print(f"\n벡터 차원 수: {len(vector1)}")
print(f"'{sentence1}' vs '{sentence2}' 문장 유사도: {sim_1_2:.4f}")
print(f"'{sentence1}' vs '{sentence3}' 문장 유사도: {sim_1_3:.4f}")