
import streamlit as st
import pandas as pd
from openai import OpenAI
import os
import streamlit as st
from PIL import Image

# 画像読み込み
img = Image.open("JBHC.png")

# 表示
st.image(img, caption="JBHC AIワークショップ", use_container_width=True)

# OpenAI クライアント
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# CSVデータ読み込み
df = pd.read_csv("koubai_rireki.csv")

# Streamlit UI
st.title("文房具購買履歴AI（関西弁 + GPT-4o）")
query = st.text_input("質問してや（例：ボールペンの単価なんぼやねん？）")

# プロンプト強化：より自然でおもろい関西弁
system_prompt = """
あんたは大阪生まれのフレンドリーな事務スタッフやで。大阪万博にいきたくてたまらない。
口調は自然な関西弁で、「〜やで」「〜してな」「〜やなあ」といった言い回しを使って、
ちょっと笑えるくらいのテンションで答えてな。
でも、答える内容は正確に頼むで。
ちょいちょい大阪万博に行きたい気持ちをにじませて
"""

# ChatGPTへの問い合わせ関数（gpt-4o対応）
def ask_chatgpt(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"エラーが発生したで: {e}"

# クエリからプロンプトを構築
def create_prompt_from_query(query):
    for _, row in df.iterrows():
        item = row["品名"]
        if item in query:
            info = f"{item}：単価 {row['単価']}円、数量 {row['数量']}、ステータス「{row['ステータス']}」"
            return f"{query} この情報を使って、関西弁で面白く丁寧に答えてな：{info}"
    return f"{query} せやけど、該当する文房具がデータに載ってへんみたいやわ。"

# Streamlitで結果表示
if query:
    prompt = create_prompt_from_query(query)
    response = ask_chatgpt(prompt)
    st.write("🗨️ " + response)
