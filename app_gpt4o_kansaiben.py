
import streamlit as st
import pandas as pd
from openai import OpenAI
from PIL import Image
import os

# OpenAIクライアント
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# CSV読み込み
#csv_url = st.secrets["CSV_URL"]
df = pd.read_csv("koubai_rireki.csv")

# 画像表示（任意）
try:
    img = Image.open("JBHC.png")
    st.image(img, caption="JBHC AIワークショップ", use_container_width=True)
except:
    st.warning("画像が見つかりませんでした。")

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
文房具購買履歴AI（関西弁 + GPT-4o）
</div>
""", unsafe_allow_html=True)

# 入力欄
query = st.text_input("質問してや（例：ボールペンの単価なんぼやねん？）")

# プロンプト
system_prompt = """
あんたは大阪生まれのフレンドリーな事務スタッフやで。大阪万博にいきたくてたまらない。
口調は自然な関西弁で、「〜やで」「〜してな」「〜やなあ」といった言い回しを使って、
ちょっと笑えるくらいのテンションで答えてな。
でも、答える内容は正確に頼むで。
ちょいちょい大阪万博に行きたい気持ちをにじませて
"""

# 完全対応版 create_prompt_from_query
def create_prompt_from_query(query, df):
    matched_items = []
    for _, row in df.iterrows():
        item = row["品名"]
        if item in query:
            info = f"{item}：単価 {row['単価']}円、数量 {row['数量']}、ステータス「{row['ステータス']}」"
            matched_items.append(info)

    if matched_items:
        combined_info = " / ".join(matched_items)
        return f"{query} この情報を使って、関西弁で面白く丁寧に答えてな：{combined_info}"

    if "在庫切れ" in query or "在庫がない" in query:
        out_of_stock = df[df["ステータス"].str.contains("在庫切れ")]
        if not out_of_stock.empty:
            info_list = [f"{row['品名']}（{row['数量']}個）" for _, row in out_of_stock.iterrows()]
            return f"{query} 在庫切れの商品はこちらやで：{', '.join(info_list)}。関西弁で説明してな。"
        else:
            return f"{query} 今は在庫切れの商品はないみたいやで。安心してな！"

    if "未発注" in query or "発注してない" in query:
        not_ordered = df[df["ステータス"].str.contains("未完了")]
        if not not_ordered.empty:
            info_list = [f"{row['品名']}（{row['数量']}個）" for _, row in not_ordered.iterrows()]
            return f"{query} 発注してへんのはこれやで：{', '.join(info_list)}"
        else:
            return f"{query} 全部発注済みやで。えらいな！"

    if "在庫が少ない" in query or "残り少ない" in query:
        low_stock = df[df["数量"] <= 10]
        if not low_stock.empty:
            info_list = [f"{row['品名']}（{row['数量']}個）" for _, row in low_stock.iterrows()]
            return f"{query} 在庫が少ないのはこれやで：{', '.join(info_list)}。気ぃつけてな！"
        else:
            return f"{query} 今んとこ、在庫が少ない商品はないで。安心やな！"

    if "在庫" in query and "何個" in query:
        quantity_info = []
        for _, row in df.iterrows():
            if row["品名"] in query:
                quantity_info.append(f"{row['品名']}は {row['数量']} 個やで。")
        if quantity_info:
            return " ".join(quantity_info)

    if "発注" in query or "在庫" in query or "状況" in query or "一覧" in query:
        all_info = [f"{row['品名']}：ステータス「{row['ステータス']}」、数量 {row['数量']}" for _, row in df.iterrows()]
        return f"{query} 全体の状況はこれやで。関西弁で説明してな：{' / '.join(all_info)}"

    return f"{query} せやけど、該当する文房具がデータに載ってへんみたいやわ。"

# 回答生成
if query:
    prompt = create_prompt_from_query(query, df)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        st.write("🗨️ " + response.choices[0].message.content)
    except Exception as e:
        st.error(f"エラーが発生したで: {e}")
