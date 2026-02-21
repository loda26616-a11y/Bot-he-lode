import os
import json
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, ChatJoinRequestHandler
from telegram.error import RetryAfter, NetworkError, TimedOut

# ================= CONFIG =================

BOT_TOKEN = os.getenv("BOT_TOKEN")
USERS_FILE = "users.json"
FILE_PATH = "TASHAN PANNEL.apk"  # Yaha apni legal file ka naam likho
BUTTON_URL = "https://t.me/kesehobhai"

BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("Join Channel 🚀", url=BUTTON_URL)]
])

# ===========================================


def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def add_user(user):
    users = load_users()
    if not any(u["id"] == user.id for u in users):
        users.append({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "joined_at": datetime.now().isoformat()
        })
        save_users(users)


async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    chat_id = update.chat_join_request.chat.id

    try:
        await context.bot.approve_chat_join_request(chat_id, user.id)

        add_user(user)

        await context.bot.send_message(
            chat_id=user.id,
            text="🎉 Welcome!\n\nThanks for joining our channel.",
            reply_markup=BUTTON
        )

        # Send file if exists
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "rb") as f:
                await context.bot.send_document(
                    chat_id=user.id,
                    document=f,
                    caption="Here is your file 📂",
                    reply_markup=BUTTON
                )

        print(f"[{datetime.now()}] Approved user {user.id}")

    except RetryAfter as e:
        await asyncio.sleep(e.retry_after)

    except (NetworkError, TimedOut):
        await asyncio.sleep(5)

    except Exception as e:
        print("Error:", e)


def main():
    if not BOT_TOKEN:
        print("BOT_TOKEN not set")
        return

    print("Bot starting...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(join_request))

    print("Bot running...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
