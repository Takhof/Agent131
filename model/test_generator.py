from generator import generate_scout_message

profile = """
名前：トム
3年以上のWebアプリケーション開発経験。主にPythonとReactを使用。
最近は自然言語処理に興味があり、独自にChatGPT APIを活用したボット開発を行っている。
"""

message = generate_scout_message(profile)
print("\n💌 スカウトメッセージ:\n")
print(message)