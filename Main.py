from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, ChatJoinRequestHandler
from telegram.error import NetworkError, TimedOut, RetryAfter
import json
import os
import asyncio
from datetime import datetime

BOT_TOKEN = 8307172728:AAHaGmRRNRKgqZosDEPFvJe9mhkYNier8SA

FILE_PATH = "ITACHI VIP INJECTOR.apk"
USERS_FILE = "users.json"

DM_LINK = "https://t.me/ULTRON_HACK_MANAGER?text=HELLO%20ULTRON%20BHAI%20MUJHE%20LOSS%20RECOVER%20KRWANA%20HAI"
VIP_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("VIP CHANNEL LINK ❤️✨", url=DM_LINK)]
])


def load_users():
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r") as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        pass
    return []


def save_users(users):
    try:
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)
    except IOError as e:
        print(f"Error saving users: {e}")


def add_user(user, users):
    if not any(u["id"] == user.id for u in users):
        users.append({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "joined_at": datetime.now().isoformat()
        })
        save_users(users)
    return users


async def send_button_to_all_users(context: ContextTypes.DEFAULT_TYPE):
    users = load_users()
    print(f"[{datetime.now()}] Sending VIP button to {len(users)} users...")

    for user_data in users:
        try:
            await context.bot.send_message(
                chat_id=user_data["id"],
                text="🔥 𝗧𝗥𝗔𝗗𝗘𝗥𝗦 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 🔥\n\n✅ Tap below for VIP support!",
                reply_markup=VIP_BUTTON
            )
        except RetryAfter as e:
            await asyncio.sleep(e.retry_after)
            try:
                await context.bot.send_message(
                    chat_id=user_data["id"],
                    text="🔥 𝗨𝗟𝗧𝗥𝗢𝗡 𝗧𝗥𝗔𝗗𝗘𝗥𝗦 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 🔥\n\n✅ Tap below for VIP support!",
                    reply_markup=VIP_BUTTON
                )
            except Exception:
                pass
        except Exception as e:
            print(f"Could not send to {user_data['id']}: {e}")

    print(f"[{datetime.now()}] Finished sending VIP button to all users.")


async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    chat_id = update.chat_join_request.chat.id

    for attempt in range(3):
        try:
            await context.bot.approve_chat_join_request(chat_id, user.id)

            users = load_users()
            add_user(user, users)

            await context.bot.send_message(
                chat_id=user.id,
                text="🚀🔥 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗨𝗟𝗧𝗥𝗢𝗡 𝗧𝗥𝗔𝗗𝗘𝗥𝗦 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗕𝗢𝗧 🔥",
                reply_markup=VIP_BUTTON
            )

            if os.path.exists(FILE_PATH):
                with open(FILE_PATH, "rb") as f:
                    await context.bot.send_document(
                        chat_id=user.id,
                        document=f,
                        filename="ITACHI INJECTOR (PREMIUM).apk",
                        caption=(
                            "✅ 100% NUMBER HACK 💥\n\n"
                            "( ONLY FOR PREMIUM USERS ⚡️ )\n"
                            "( 100% LOSS RECOVER GUARANTEE ⚡️ )\n\n"
                          
  "𝐇𝐎𝐖 𝐓𝐎 𝐔𝐒𝐄 𝐇𝐀𝐂𝐊 :- https://t.me/HOW_TO_USE_ULTRON_HACK/10"
                           
 "FOR HELP @ULTRON_HACK_MANAGER"
                        ),
                        reply_markup=VIP_BUTTON
                    )

            print(f"[{datetime.now()}] Approved user: {user.id} (@{user.username})")
            break
except RetryAfter as e:
            print(f"Rate limited, waiting {e.retry_after} seconds...")
            await asyncio.sleep(e.retry_after)
        except (NetworkError, TimedOut) as e:
            print(f"Network error (attempt {attempt + 1}/3): {e}")
            if attempt < 2:
                await asyncio.sleep(5)
        except Exception as e:
            print(f"Error handling join request: {e}")
            break


def main():
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN environment variable not set")
        print("Waiting 30 seconds before retry...")
        import time
        time.sleep(30)
        return

    print(f"[{datetime.now()}] Bot starting...")

    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .get_updates_pool_timeout(30)
        .get_updates_read_timeout(30)
        .get_updates_write_timeout(30)
        .get_updates_connect_timeout(30)
        .build()
    )
    app.add_handler(ChatJoinRequestHandler(join_request))

    app.job_queue.run_repeating(
        send_button_to_all_users,
        interval=7200,
        first=10
    )

    print(f"[{datetime.now()}] Bot running - waiting for join requests...")
    print(f"[{datetime.now()}] VIP button will be sent to all users every 2 hours.")

    app.run_polling(
        drop_pending_updates=True,
        allowed_updates=["chat_join_request"]
    )


if name == "main":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("Bot stopped by user")
            break
        except Exception as e:
            print(f"[{datetime.now()}] Bot crashed: {e}")
            print("Restarting in 10 seconds...")
            import time
            time.sleep(10)
