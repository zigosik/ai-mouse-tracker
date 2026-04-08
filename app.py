import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Nastavení AI klienta z proměnných prostředí
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
    mouse_points = data.get('mouse_data', [])
    
    # Příprava dat pro AI - uděláme ze souřadnic textový popis
    pohyb_popis = ", ".join([f"[{p['x']},{p['y']}]" for p in mouse_points[:20]])

    prompt = f"""
    Uživatel se právě pohyboval myší po obrazovce. Tady je vzorek jeho souřadnic: {pohyb_popis}.
    Zkus z toho odhadnout jeho náladu nebo co právě na webu hledá. 
    Odpovídej vtipně, stručně a česky.
    """

    response = client.chat.completions.create(
        model="gemma3:27b",
        messages=[
            {"role": "system", "content": "Jsi expert na psychologii pohybu myši."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return jsonify({"odpoved": response.choices[0].message.content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
