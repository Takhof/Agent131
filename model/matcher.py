from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# モデルの読み込み
model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_match_score(profile_text: str, job_description: str) -> float:
    # それぞれの文をベクトル化
    embeddings = model.encode([profile_text, job_description])
    profile_vec, job_vec = embeddings[0], embeddings[1]

    # コサイン類似度でスコア計算（0〜1に近い）
    score = cosine_similarity([profile_vec], [job_vec])[0][0]
    return round(score, 4)