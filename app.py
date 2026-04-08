from flask import Flask, request, render_template, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    dotaz = data.get('search', 'nic')
    prompt = f"Uživatel vyhledává: '{dotaz}'. Doporuč mu 3 související věci."
    
    response = client.chat.completions.create(
        model="gemma3:27b",
        messages=[{"role": "user", "content": prompt}]
    )
    return jsonify({"odpoved": response.choices[0].message.content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

