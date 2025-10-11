from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
app = Flask(__name__)

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    print("⚠ OPENAI_API_KEY が読み込めていません（.envを確認）")
client = OpenAI(api_key=API_KEY)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        prompt = (data or {}).get("prompt", "").strip()
        if not prompt:
            return jsonify({"error": "プロンプトが空です"}), 400

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたは自分史作成のサポートAIです。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
        )
        text = res.choices[0].message.content.strip()
        return jsonify({"result": text})
    except Exception as e:
        # サーバー側のログに詳細を出す
        import traceback; traceback.print_exc()
        # ブラウザ側にも原因が分かるよう返す
        return jsonify({"error": f"SERVER_ERROR: {type(e).__name__}: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
