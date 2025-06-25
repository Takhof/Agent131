import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_scout_message(profile_text: str, tone: str = "professional") -> str:
    prompt = f"""
あなたは人材スカウトのプロです。
以下の候補者プロフィールを読み取り、魅力的でトーンが「{tone}」なスカウトメッセージを1通書いてください。

【候補者プロフィール】
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