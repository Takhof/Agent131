import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
from model.generator import generate_scout_message

st.set_page_config(page_title="スカウト文ジェネレーター", page_icon="💌")

st.title("💌 スカウト文自動生成アシスタント")
st.caption("候補者プロフィールから、魅力的なスカウト文を自動で作成しちゃうよ✨")

# プロフィール入力欄
profile_text = st.text_area("🎯 候補者プロフィールを入力してね：", height=200)

# トーン選択（カジュアル/丁寧/熱意あふれる）
tone = st.selectbox("🗣️ スカウト文のトーンは？", ["friendly", "polite", "enthusiastic"])

if st.button("💌 スカウト文を生成！"):
    if profile_text.strip() == "":
        st.warning("プロフィールを入力してね〜！")
    else:
        with st.spinner("スカウト文を生成中だよ…✨"):
            message = generate_scout_message(profile_text, tone)
            st.success("できたよ〜！✨")
            st.markdown("#### ✉️ スカウトメッセージ")
            st.text_area("結果はこちら！", message, height=250)