import os
from flask import Flask, render_template, request, jsonify
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
    # AI simulujeme, že "vidí" náhodný obrázek
    prompt = "Uživatel právě najel myší na náhodný obrázek z internetu. Vymysli si jeden konkrétní, vtipný a krátký komentář k tomu, co by na tom obrázku mohlo být (např. o tlusté kočce, divném mraku nebo starém kole). Buď kreativní a stručný."

    response = client.chat.completions.create(
        model="gemma3:27b",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return jsonify({"odpoved": response.choices[0].message.content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
