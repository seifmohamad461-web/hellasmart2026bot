
import os
import logging
import requests
from flask import Flask, request

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

@app.route("/")
def home():
    return "HellaSmart bot is running!", 200

@app.route("/health")
def health():
    return "OK", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "").strip()

    if not chat_id or not text:
        return "OK", 200

    if text == "/start" or text.startswith("/start@"):
        if not TOKEN:
            app.logger.error("TELEGRAM_BOT_TOKEN is missing")
            return "OK", 200

        try:
            response = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": "أهلاً بك في حِلّها 💡\nأنا هنا لمساعدتك بأفكار المشاريع والمهارات وطرق الدخل الواقعية."
                },
                timeout=15
            )
            app.logger.info(
                "Telegram sendMessage status=%s response=%s",
                response.status_code,
                response.text[:500]
            )
            response.raise_for_status()
        except requests.RequestException:
            app.logger.exception("Failed to send Telegram message")

    return "OK", 200

@app.route("/webhook-info")
def webhook_info():
    return {
        "webhook_route": "/webhook",
        "token_configured": bool(TOKEN)
    }
    

@app.route("/version")
def version():
    return "HELLASMART-V2", 200
    
