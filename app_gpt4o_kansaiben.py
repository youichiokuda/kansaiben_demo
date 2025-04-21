
import streamlit as st
import pandas as pd
from openai import OpenAI
import os
from PIL import Image

# 画像読み込み
img = Image.open("JBHC.png")

st.markdown("""
<div style='
    font-size:18px;
    font-weight:bold;
    text-align:center;
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
'>
文房具購買履歴AI（関西弁 + GPT-4o）
</div>
""", unsafe_allow_html=True)

# 修正
st.image(img, caption="JBHC AIワークショップ", use_container_width=True)

# OpenAI クライアント
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# CSVデータ読み込み
df = pd.read_csv("koubai_rireki.csv")

# Streamlit UI
#st.title("文房具購買履歴AI（関西弁 + GPT-4o）")
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
#def create_prompt_from_query(query):
    #for _, row in df.iterrows():
        #item = row["品名"]
        #if item in query:
            #info = f"{item}：単価 {row['単価']}円、数量 {row['数量']}、ステータス「{row['ステータス']}」"
            #return f"{query} この情報を使って、関西弁で面白く丁寧に答えてな：{info}"
    #return f"{query} せやけど、該当する文房具がデータに載ってへんみたいやわ。"

def create_prompt_from_query(query, df):
    matched_items = []

    # 品名に一致した商品を収集
    for _, row in df.iterrows():
        item = row["品名"]
        if item in query:
            info = f"{item}：単価 {row['単価']}円、数量 {row['数量']}、ステータス「{row['ステータス']}」"
            matched_items.append(info)

    # 質問内容に応じて条件分岐
    if matched_items:
        combined_info = " / ".join(matched_items)
        return f"{query} この情報を使って、関西弁で面白く丁寧に答えてな：{combined_info}"

    # 「在庫切れ」の商品を聞かれた場合
    if "在庫切れ" in query or "在庫がない" in query:
        out_of_stock = df[df["ステータス"].str.contains("在庫切れ")]
        if not out_of_stock.empty:
            info_list = [f"{row['品名']}（{row['数量']}個）" for _, row in out_of_stock.iterrows()]
            return f"{query} 在庫切れの商品はこちらやで：{', '.join(info_list)}。関西弁で説明してな。"
        else:
            return f"{query} 今は在庫切れの商品はないみたいやで。安心してな！"

    # 「未発注」商品の問い合わせ
    if "未発注" in query or "発注してない" in query:
        not_ordered = df[df["ステータス"].str.contains("未完了")]
        if not not_ordered.empty:
            info_list = [f"{row['品名']}（{row['数量']}個）" for _, row in not_ordered.iterrows()]
            return f"{query} 発注してへんのはこれやで：{', '.join(info_list)}"
        else:
            return f"{query} 全部発注済みやで。えらいな！"

    # 「在庫が少ない」商品の問い合わせ（しきい値10個）
    if "在庫が少ない" in query or "残り少ない" in query:
        low_stock = df[df["数量"] <= 10]
        if not low_stock.empty:
            info_list = [f"{row['品名']}（{row['数量']}個）" for _, row in low_stock.iterrows()]
            return f"{query} 在庫が少ないのはこれやで：{', '.join(info_list)}。気ぃつけてな！"
        else:
            return f"{query} 今んとこ、在庫が少ない商品はないで。安心やな！"

    # 「〜の在庫は？」→ 数量だけを答える
    if "在庫" in query and "何個" in query:
        quantity_info = []
        for _, row in df.iterrows():
            if row["品名"] in query:
                quantity_info.append(f"{row['品名']}は {row['数量']} 個やで。")
        if quantity_info:
            return " ".join(quantity_info)

    # 「全体の発注状況」などを尋ねる汎用
    if "発注" in query or "在庫" in query or "状況" in query or "一覧" in query:
        all_info = [f"{row['品名']}：ステータス「{row['ステータス']}」、数量 {row['数量']}" for _, row in df.iterrows()]
        return f"{query} 全体の状況はこれやで。関西弁で説明してな：{' / '.join(all_info)}"

    return f"{query} せやけど、該当する文房具がデータに載ってへんみたいやわ。"

# Streamlitで結果表示
if query:
    prompt = create_prompt_from_query(query)
    response = ask_chatgpt(prompt)
    st.write("🗨️ " + response)


