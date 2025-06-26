import base64
import os
from openai import OpenAI
from dotenv import load_dotenv
import PyPDF2
import pandas as pd



load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_scout_message(profile_text: str, tone: str = "professional") -> str:
    prompt = f"""
あなたは人材スカウトのプロです。
以下の候補者プロフィールを読み取り、魅力的でトーンが「{tone}」なスカウトメッセージを1通書いてください。

【候補者プロフィール】

名前やコンタクトインフォメーションもここから読み取り、メッセージに入れてください。
{profile_text}

【スカウトメッセージ】
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"エラーが発生しちゃった…：{str(e)}"
    
def summarize_profile(profile_text: str) -> str:
    prompt = f"""
以下のプロフィール文から、名前、コンタクトインフォ、職歴、スキル、志向性を簡潔にまとめてください：

{profile_text}
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=300
    )
    return response.choices[0].message.content.strip()    

def extract_text_from_pdf(uploaded_file) -> str:
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return f"読み取りエラー：{e}"
    
def read_uploaded_profiles(uploaded_file):
    if uploaded_file is None:
        return None

    filename = uploaded_file.name.lower()
    if filename.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    elif filename.endswith(".txt"):
        content = uploaded_file.read().decode("utf-8")
        return pd.DataFrame({"profile": [content]})
    elif filename.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file)
        return pd.DataFrame({"profile": [text]})
    else:
        return None
    
def read_multiple_profiles(files):
    profiles = []

    for file in files:
        name = file.name.lower()
        if name.endswith(".csv"):
            df = pd.read_csv(file)
            for _, row in df.iterrows():
                profiles.append(row.get("profile", ""))
        elif name.endswith(".txt"):
            content = file.read().decode("utf-8")
            profiles.append(content)
        elif name.endswith(".pdf"):
            profiles.append(extract_text_from_pdf(file))
        else:
            continue

    return pd.DataFrame({"profile": profiles})
    
def get_csv_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="scout_results.csv">📥 スカウト結果をダウンロード</a>'
    return href