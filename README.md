# 💌 AI Scout Assistant

> Automatically generate personalized scout messages and match scores from candidate profiles using AI ✨

---

## 🖼 Screenshot

![image](https://github.com/user-attachments/assets/8bd120dd-1c28-42a4-a1c7-ea19662a901a)


---

## ✨ Features

- 📎 Supports PDF, TXT, and CSV candidate profile uploads
- 🧠 Calculates match scores between job descriptions and profiles using Sentence-BERT (cosine similarity)
- 💌 Generates warm, personalized scout messages using OpenAI GPT
- 🎨 Tone options: `friendly`, `polite`, `enthusiastic`
- 💚 Auto-labels top candidates (`Recommended!`) based on match score
- 📊 Results downloadable as CSV
- 🌐 Deployed on Streamlit with a simple, intuitive UI

---

## 🚀 Live Demo

👉 https://recruitingagent.streamlit.app/

---

## 🛠 Installation (for local use)

```bash
git clone https://github.com/yourname/yourrepo.git
cd yourrepo
pip install -r requirements.txt
streamlit run app/main.py
