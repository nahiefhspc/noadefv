from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import requests
import html

# Replace with your bot token
BOT_TOKEN = "6361809314:AAGYdd-ksah0cXvHdRdyh0oHSP8SIQoHT0o"

# Function to get token from the URL
def get_token_from_url():
    url = "https://pretty-lu-ckejcjdjwj-8805a949.koyeb.app/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("token")
    return None

# Fetch token for API requests
TOKEN = get_token_from_url()

# Class and Batch data for each year
YEAR_CLASSES = {
    "2024-25": {
        "11th": {
            "Vijay 2.0(PCM)": "98",
            "Vijay 3.0(PCM)": "110",
            "Vijay 4.0(PCM)": "116",
            "Vijay 5.0(PCM)": "119",
        },
        "12th": {
            "Vijeta 2.0 Chem Spl": "89",
            "Vijeta 4.0 (PCM)": "99",
        },
        "13th": {
            "Vishesh 2.0 (PCM)": "100",
            "Vishesh 3.0 (PCM)": "108",
            "Vishesh 4.0 (PCM)": "114",
            "Vishesh 5.0 (PCM)": "117",
        },
        "CrashCourse": {
            "Adv Ranker (PCM)": "94",
            "Victroy 1.0 (PCM)": "123",
            "Test Series (PCM)": "124",
        },
    },
    "2025-26": {
        "11th": {
            "Backlog Silver Chem": "131",
            "Vijeta 1.0 Gold (11+12) Chem": "132",
            "Vijeta 1.0 Silver (11+12) Chem": "133",
            "Vijeta 1.0 Diamond (11+12) Chem": "134",
        },
        "12th": {
            "Vijeta 1.0 Silver (PCM)": "126",
            "Vijeta 1.0 GOLD (PCM)": "128",
            "Vijeta 1.0 Diamond (PCM)": "130",
            "Vijeta 1.0 Gold (11+12) Chem": "132",
            "Vijeta 1.0 Silver (11+12) Chem": "133",
            "Vijeta 1.0 Diamond (11+12) Chem": "134",
        },
    },
}

# Mapping of user IDs to indexes
USER_ID_TO_IDX = {
    "7423360734": 1,
    "9374253829": 2,
}

# Function to fetch subjects for a batch
def fetch_subjects(batch_id):
    url = f"https://spec.iitschool.com/api/v1/batch-subject/{batch_id}"
    headers = {
        "Accept": "application/json",
        "origintype": "web",
        "token": TOKEN,  # Use dynamically fetched token
        "usertype": "2",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["responseCode"] == 200:
            return data["data"]["batch_subject"]
    return []

# Function to fetch topics for a subject
def fetch_topics(batch_id, subject_id):
    url = f"https://spec.iitschool.com/api/v1/batch-topic/{subject_id}?type=class"
    headers = {
        "Accept": "application/json",
        "origintype": "web",
        "token": TOKEN,  # Use dynamically fetched token
        "usertype": "2",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["responseCode"] == 200:
            return data["data"]["batch_topic"]
    return []

# Function to fetch lessons for a subject and topic
def fetch_lessons(batch_id, subject_id, topic_id):
    url = f"https://spec.iitschool.com/api/v1/batch-detail/{batch_id}?subjectId={subject_id}&topicId={topic_id}"
    headers = {
        "Accept": "application/json",
        "origintype": "web",
        "token": TOKEN,  # Use dynamically fetched token
        "usertype": "2",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["responseCode"] == 200:
            return data["data"]["class_list"]["classes"]
    return []

# Function to fetch notes for a subject and topic
def fetch_notes(batch_id, subject_id, topic_id):
    url = f"https://spec.iitschool.com/api/v1/batch-notes/{batch_id}?subjectId={subject_id}&topicId={topic_id}"
    headers = {
        "Accept": "application/json",
        "origintype": "web",
        "token": TOKEN,  # Use dynamically fetched token
        "usertype": "2",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["responseCode"] == 200:
            return data["data"]["notesDetails"]
    return []

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    if user_id not in USER_ID_TO_IDX:
        await update.message.reply_text("You are not a member of the channel. Please join the channel to proceed.",
        parse_mode="HTML",
        protect_content=True
        )
        return

    keyboard = [
        [InlineKeyboardButton("2024-25", callback_data="year_2024-25")],
        [InlineKeyboardButton("2025-26", callback_data="year_2025-26")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = await update.message.reply_text("Welcome! Select your academic year:", 
                                              parse_mode="HTML",
                                              reply_markup=reply_markup,
                                              protect_content=True)

    # Schedule the deletion after 60 seconds
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    user_id = str(query.from_user.id)
    idx = USER_ID_TO_IDX.get(user_id, None)
    if idx is None:
        await query.edit_message_text(
            text="You are not a member of the channel. Please join the channel to proceed.",
            parse_mode="HTML"
        )
        return

    if data.startswith("year_"):
        year = data.split("_")[1]
        keyboard = [
            [InlineKeyboardButton("11th", callback_data=f"class_{year}_11th")],
            [InlineKeyboardButton("12th", callback_data=f"class_{year}_12th")],
            [InlineKeyboardButton("13th", callback_data=f"class_{year}_13th")],
            [InlineKeyboardButton("CrashCourse", callback_data=f"class_{year}_CrashCourse")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"<b>Select your class for {year}:</b>",
            parse_mode="HTML",
            reply_markup=reply_markup
        )

    elif data.startswith("class_"):
        _, year, class_name = data.split("_")
        batches = YEAR_CLASSES[year][class_name]
        keyboard = [[InlineKeyboardButton(name, callback_data=f"batch_{batch_id}")] for name, batch_id in batches.items()]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="<b>Select a batch:</b>",
            parse_mode="HTML",
            reply_markup=reply_markup
        )

    elif data.startswith("batch_"):
        batch_id = data.split("_")[1]
        subjects = fetch_subjects(batch_id)
        if subjects:
            keyboard = [
                [InlineKeyboardButton(subject["subjectName"], callback_data=f"subject_{batch_id}_{subject['id']}")]
                for subject in subjects
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                text="<b>Select a subject:</b>",
                parse_mode="HTML",
                reply_markup=reply_markup
            )

    elif data.startswith("subject_"):
        _, batch_id, subject_id = data.split("_")
        topics = fetch_topics(batch_id, subject_id)
        if topics:
            keyboard = [
                [InlineKeyboardButton(topic["topicName"], callback_data=f"topic_{batch_id}_{subject_id}_{topic['id']}")]
                for topic in topics
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                text="<b>Select a topic:</b>",
                parse_mode="HTML",
                reply_markup=reply_markup
            )

    elif data.startswith("topic_"):
        _, batch_id, subject_id, topic_id = data.split("_")
        lessons = fetch_lessons(batch_id, subject_id, topic_id)
        notes = fetch_notes(batch_id, subject_id, topic_id)

        lessons_str = "\n".join([lesson["lessonName"] for lesson in lessons]) if lessons else "No lessons found."
        notes_str = "\n".join([note["notesName"] for note in notes]) if notes else "No notes found."

        response_text = f"<b>Lessons:</b>\n{lessons_str}\n\n<b>Notes:</b>\n{notes_str}"
        await query.edit_message_text(
            text=response_text,
            parse_mode="HTML"
        )

# Main function to start the bot
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == "__main__":
    main()
