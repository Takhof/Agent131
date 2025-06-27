from matcher import compute_match_score

profile = "3年のPython経験。NLPとGPT APIの活用に興味あり。"
job = "自然言語処理エンジニアを募集しています。Pythonでの開発経験必須。"

score = compute_match_score(profile, job)
print(f"💡 マッチ度スコア: {score}")