
from flask import Flask, jsonify, request
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/')
def home():
    return jsonify({'message': 'Добро пожаловать в ЭпиЛенд API'})

@app.route('/api/diary', methods=['POST'])
def diary():
    data = request.json
    return jsonify({'status': 'ok', 'received': data})

@app.route('/api/chat', methods=['POST'])
def chat():
    user_msg = request.json.get("message", "")
    if not user_msg:
        return jsonify({"error": "Empty message"}), 400
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты ласковый помощник и маскот по имени Лаванда. Помогаешь детям с эпилепсией."},
                {"role": "user", "content": user_msg}
            ]
        )
        answer = response.choices[0].message.content.strip()
        return jsonify({"reply": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
