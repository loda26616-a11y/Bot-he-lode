import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "TASHAN PANNEL.apk")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send /apk to download file.")

async def apk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Looking for file at:", FILE_PATH)
    print("Files available:", os.listdir(BASE_DIR))

    if os.path.exists(FILE_PATH):
        await update.message.reply_document(document=open(FILE_PATH, "rb"))
    else:
        await update.message.reply_text("File not found ❌")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("apk", apk))

print("Bot started...")
app.run_polling()
