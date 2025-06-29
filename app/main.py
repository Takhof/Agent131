import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pandas as pd
import streamlit as st
import openai
from model.generator import generate_scout_message
from model.generator import summarize_profile, extract_text_from_pdf, read_uploaded_profiles, get_csv_download_link, read_multiple_profiles
from model.matcher import compute_match_score

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="スカウト文ジェネレーター", page_icon="💌")

st.title("💌 お仕事マッチングエージェント")
st.caption("候補者プロフィールからマッチング度を計算して魅力的なスカウト文を自動で作成しちゃうよ✨")

st.markdown("---")

# 求人要件入力欄
job_description = st.text_area("📋 求人要件を入力してね：", placeholder="例）NLPに強いPythonエンジニア募集...")

# プロフィール入力欄
profile_text = st.text_area("🎯 候補者プロフィールを入力するか、下にアップロードしてね：", height=200)

# 履歴書アップロード
uploaded_file = st.file_uploader("📎 プロフィールファイルをアップロードしてね（PDF / CSV / TXT）", type=["pdf", "csv", "txt"],
                                accept_multiple_files=True
                                 )


if uploaded_file:
    df_profiles = read_multiple_profiles(uploaded_file)
    if df_profiles is not None and not df_profiles.empty:
        st.info(f"✅ {len(df_profiles)} 件のプロフィールを読み込みました。")

        tone = st.selectbox("🗣️ スカウト文のトーンは？", ["friendly", "polite", "enthusiastic"], key="tone_select")

        if st.button("✨ スカウト文を作る！"):
            with st.spinner("スカウト文を一括生成中..."):
                results = []
                for idx, row in df_profiles.iterrows():
                    profile = row.get("profile", "")
                    summary = summarize_profile(profile)
                    message = generate_scout_message(summary, tone)
                    results.append({
                        "summary": summary,
                        "scout_message": message
                    })
                df_result = pd.DataFrame(results)
                st.success("🎉 スカウト文ができたよ！")
                st.dataframe(df_result[["summary", "scout_message"]])
                st.markdown(get_csv_download_link(df_result), unsafe_allow_html=True)
                

if uploaded_file and job_description.strip() != "":
    if st.button("🔍 マッチ度スコアを計算する！"):
        df_profiles = read_multiple_profiles(uploaded_file)
        results = []
        for idx, row in df_profiles.iterrows():
            profile = row.get("profile", "")
            score = compute_match_score(profile, job_description)
                # 💚 おすすめフラグ付け
            if score >= 0.75:
                recommendation = "💚 おすすめ！"
            elif score < 0.5:
                recommendation = "🟡 あまりマッチしてないかも…"
            else:
                recommendation = "🤍 普通かな？"
            results.append({
                "recommendation": recommendation,
                "match_score": score,
                "profile": profile
            })
        df_score = pd.DataFrame(results)
        st.success("✨ マッチング完了！")
        st.dataframe(df_score)
        st.markdown(get_csv_download_link(df_score), unsafe_allow_html=True)