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

@app.route('/get_product', methods=['POST'])
def get_product():
    data = request.json
    kategorie = data.get('kategorie')
    smer = data.get('smer') # 'levnejsi' nebo 'drazsi'
    aktualni = data.get('aktualni', 'běžný model')

    # AI vybere konkrétní produkt a popíše ho
    prompt = f"""Uživatel prohlíží {kategorie}. Teď má vybraný model "{aktualni}". 
    Najdi jeden konkrétní existující model, který je {smer}.
    Odpověz PŘESNĚ v tomto formátu (nic jiného nepiš):
    NÁZEV: [Název produktu]
    PARAMETRY: [3 hlavní parametry]
    ODKAZ: https://www.heureka.cz/"""

    response = client.chat.completions.create(
        model="gemma3:27b",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return jsonify({"vysledek": response.choices[0].message.content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
