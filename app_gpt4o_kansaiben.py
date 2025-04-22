
import streamlit as st
import pandas as pd
from openai import OpenAI
from PIL import Image
import os

# OpenAIクライアント
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# CSV読み込み（ローカル想定）
df = pd.read_csv("koubai_rireki.csv")

# CSVの文字列表現（ChatGPTに投げる用）
csv_summary = df.to_string(index=False)


# タイトル（小さめ＆1行）
st.markdown("""
<div style='
    font-size:18px;
    font-weight:bold;
    text-align:center;
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
'>
文房具購買履歴AI（関西弁 + 生成AI）
</div>
""", unsafe_allow_html=True)

# 画像表示（任意）
try:
    img = Image.open("JBHC.png")
    st.image(img, caption="JBHC AIワークショップ", use_container_width=True)
except:
    st.warning("画像が見つかりませんでした。")
# 質問入力
query = st.text_input("質問してや（例：在庫切れの商品は？、一番高い商品は？）")

# プロンプト
system_prompt = """
あんたは大阪生まれのフレンドリーな事務スタッフやで。大阪万博にいきたくてたまらない。
口調は自然な関西弁で、「〜やで」「〜してな」「〜やなあ」といった言い回しを使って、
ちょっと笑えるくらいのテンションで答えてな。
でも、答える内容は正確に頼むで。
ちょいちょい大阪万博に行きたい気持ちをにじませて
"""

# 質問が入力されたら処理
if query:
    # ChatGPTへのプロンプト生成
    prompt = f"""
以下は購買履歴のCSVデータやで：

{csv_summary}

このデータをもとに、次の質問に答えてな：
「{query}」
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        st.markdown("### 👀 AIの答え：")
        st.write(response.choices[0].message.content)
    except Exception as e:
        st.error(f"エラーが発生したで：{e}")
