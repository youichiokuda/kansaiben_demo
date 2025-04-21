
# 文房具購買履歴AI（関西弁 + GPT-4）

このアプリは、文房具の購買履歴データをもとに、ChatGPT（GPT-4）を使って関西弁で応答するデモ用アプリです。  
Streamlit で構築されており、軽快な操作感でワークショップや展示用にピッタリです。

---

## 🚀 デモ内容

ユーザーが「ボールペンの単価どれくらいや？」のような質問をすると、  
購買履歴に基づいて関西弁で答えてくれます。

---

## 📁 含まれているファイル

| ファイル名 | 説明 |
|------------|------|
| `app.py` | Streamlitアプリの本体（ChatGPT API利用） |
| `koubai_rireki.csv` | 文房具の購買履歴サンプル |
| `requirements.txt` | 必要なPythonパッケージ |
| `.streamlit/config.toml` | Streamlitクラウド用設定ファイル |

---

## 🔧 セットアップ手順（ローカル or Streamlit Cloud）

### 1. 必要なライブラリをインストール（ローカルの場合）

```bash
pip install -r requirements.txt
```

### 2. OpenAI APIキーを環境変数に設定

```bash
export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

または `.streamlit/secrets.toml` に記載（Streamlit Cloudの場合）

```toml
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### 3. アプリを起動

```bash
streamlit run app.py
```

---

## 🌍 Streamlit Cloudで動かす方法

1. このリポジトリを GitHub にアップ
2. [https://streamlit.io/cloud](https://streamlit.io/cloud) にログインし「New App」
3. リポジトリ・ブランチ・ファイル名（`app.py`）を指定
4. 「Advanced settings」から `OPENAI_API_KEY` を追加
5. Deployをクリック！

---

## 🗨️ 使用例（関西弁応答）

**Q:** ノートの在庫ある？  
**A:** ノートは今、在庫切れや。次の便に期待やな！

---

## 📄 ライセンス

MIT License

---

制作・監修：AIワークショップ実行チーム 🚀
