from flask import Flask, request
from telegram import Bot
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = f"https://manager-chat-bot.onrender.com/{TOKEN}"
app = Flask(__name__)
bot = Bot(token=TOKEN)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        bot.send_message(chat_id=chat_id, text=f"You said: {text}")

    return "ok", 200

@app.route(f"/", methods=["GET"])
def health():

    return "ok", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8443))

    bot.set_webhook(url=WEBHOOK_URL)
    print(f"Webhook set to {WEBHOOK_URL}")

    app.run(host="0.0.0.0", port=port)
