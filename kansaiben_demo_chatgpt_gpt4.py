
import streamlit as st
import pandas as pd
import openai
import os

# OpenAI APIキーの設定（環境変数で設定推奨）
openai.api_key = os.getenv("OPENAI_API_KEY")

# CSVの読み込み
df = pd.read_csv("koubai_rireki.csv")

# タイトル
st.title("文房具購買履歴AI（関西弁 + GPT-4）")

# ユーザー入力
query = st.text_input("質問してや（例：ボールペンの単価どれくらい？）")

# ChatGPTに問い合わせる関数（GPT-4）
def ask_chatgpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role": "system",
                "content": "あなたはフレンドリーな関西弁を話す事務スタッフです。購買履歴データに基づいて、親しみやすく、ちょっと笑いもある口調で答えてください。"
            }, {
                "role": "user",
                "content": prompt
            }]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"エラーが発生したで: {e}"

# ユーザー入力に応じてCSVからデータを抽出し、ChatGPTへ送る
def create_prompt_from_query(query):
    for _, row in df.iterrows():
        item = row["品名"]
        if item in query:
            info = f"{item}：単価 {row['単価']}円、数量 {row['数量']}、ステータス「{row['ステータス']}」"
            return f"{query} この情報を使って答えてな：{info}"
    return f"{query} せやけど、該当する文房具がデータに載ってへんみたいやわ。"

# 結果表示
if query:
    prompt = create_prompt_from_query(query)
    response = ask_chatgpt(prompt)
    st.write("🗨️ " + response)
