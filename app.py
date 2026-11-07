import os
import requests
from flask import Flask

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

@app.route("/")
def home():
    return "HellaSmart bot is running!"

@app.route("/health")
def health():
    return "OK", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    from flask import request
    data = request.get_json(silent=True) or {}
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")

    if chat_id and text == "/start":
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": "أهلاً بك في حِلّها 💡\nأنا هنا لمساعدتك بأفكار المشاريع والمهارات وطرق الدخل الواقعية."
            },
            timeout=10
        )

    return "OK", 200
@app.route("/webhook-info")
def webhook_info():
    return {
        "webhook_route": "/webhook",
        "token_configured": bool(TOKEN)
    }
