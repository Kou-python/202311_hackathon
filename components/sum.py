import openai
import re

# OpenAI APIキーを設定
openai.api_key = ""


# 入力されたテキストを要約する関数
def summarize_text(text):
    # OpenAIにテキストを送信して、要約を取得
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Summarize the following text:\n{text}\n---\nSummary:",
        temperature=0.5,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    # 要約を取得
    summary = response.choices[0].text.strip()
    # 要約内の改行を削除
    summary = re.sub(r"\n+", " ", summary)
    return summary


# テスト用のテキスト
text = "OpenAIは、人工知能の研究・開発を行う企業である。本社はアメリカ合衆国カリフォルニア州サンフランシスコにあり、2015年に設立された。創業者は、イーロン・マスク、サム・アルトマン、グレッグ・ブロックマン、ジョン・ショークリー、イリア・スシャンスキーの5人である。"
# テキストを要約
summary = summarize_text(text)
# 要約を出力
print(summary)
