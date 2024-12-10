from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
from dotenv import load_dotenv
import telegram

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello 😊")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text(f"You said: {user_message}")

# Hàm xử lý khi có lỗi
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Error: {context.error}")

# Khởi tạo Flask app
app = Flask(__name__)

# Hàm xử lý Webhook
@app.route(f"/{os.getenv('TOKEN')}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = Update.de_json(json_str, telegram.Bot(token=os.getenv('TOKEN')))
    
    application.update_queue.put(update)
    
    return "OK", 200

@app.route("/", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    
    return "Running", 200

if __name__ == "__main__":
    load_dotenv()

    TOKEN = os.getenv("TOKEN")

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.add_error_handler(error_handler)

    bot = telegram.Bot(token=TOKEN)
    bot.set_webhook(url=f"https://manager-chat-bot.onrender.com/{TOKEN}")

    app.run(host='0.0.0.0', port=5000)
