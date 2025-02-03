from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import requests
import html

# Replace with your bot token
BOT_TOKEN = "7810054325:AAExvvvqzsYoeJR06Ozec-VZJAlNZ_d9NTU"

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
    "5034929962": 2,
    "5487643307": 3,
    "7137002799": 4,
    "6038536979": 5,
    "1737051944": 6,
    "6568611832": 7,
}

# Function to fetch subjects for a batch
def fetch_subjects(batch_id):
    url = f"https://spec.iitschool.com/api/v1/batch-subject/{batch_id}"
    headers = {
        "Accept": "application/json",
        "origintype": "web",
        "token": TOKEN,
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
        "token": TOKEN,
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
        "token": TOKEN,
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
        "token": TOKEN,
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
        [InlineKeyboardButton("𝟐𝟎𝟐𝟒 ✦ 𝟐𝟎𝟐𝟓", callback_data="year_2024-25")],
        [InlineKeyboardButton("𝟐𝟎𝟐𝟓 ✦ 𝟐𝟎𝟐𝟔", callback_data="year_2025-26")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = await update.message.reply_text("<b>Select Which Year Batches You want 😁</b>", 
                                              parse_mode="HTML",
                                              reply_markup=reply_markup,
                                              protect_content=True)

    # Schedule the deletion after 60 seconds

# Function to delete buttons and send a new message after 60 seconds
# Callback for button interactions
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
            [InlineKeyboardButton("𝟭𝟭𝘁𝗵", callback_data=f"class_{year}_11th")],
            [InlineKeyboardButton("𝟭𝟮𝘁𝗵", callback_data=f"class_{year}_12th")],
            [InlineKeyboardButton("𝟭𝟯𝘁𝗵", callback_data=f"class_{year}_13th")],
            [InlineKeyboardButton("𝗖𝗿𝗮𝘀𝗵𝗖𝗼𝘂𝗿𝘀𝗲", callback_data=f"class_{year}_CrashCourse")],
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
        else:
            await query.edit_message_text(
                text="<b>No subjects found for this batch.</b>",
                parse_mode="HTML"
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
        else:
            await query.edit_message_text(
                text="<b>No topics found for this subject.</b>",
                parse_mode="HTML"
            )

    elif data.startswith("topic_"):
        _, batch_id, subject_id, topic_id = data.split("_")
        lessons = fetch_lessons(batch_id, subject_id, topic_id)
        notes = fetch_notes(batch_id, subject_id, topic_id)

        if lessons:
            keyboard = [
                [InlineKeyboardButton(lesson["lessonName"], web_app=WebAppInfo(url=f'https://vercelsop.vercel.app/{lesson["id"]}'))]
                for lesson in lessons
            ]
            if notes:
                keyboard.append([InlineKeyboardButton("Notes", callback_data=f"notes_{batch_id}_{subject_id}_{topic_id}")])
            reply_markup = InlineKeyboardMarkup(keyboard)
        # Edit message with web preview enabled
            await query.edit_message_text(
                text="Select a lesson or view notes:",
                reply_markup=reply_markup,
                disable_web_page_preview=False  # Enable web preview
            )
        elif notes:
            notes_message = "\n\n".join([
                f"🌟<a href=\"{html.escape(note['docUrl'])}\">{html.escape(note['docTitle'])}</a>"
                for note in notes
            ])
            await query.edit_message_text(
                text=(
                    "<b> 𝐀𝐋𝐋 𝐍𝐎𝐓𝐄𝐒 𝐁𝐄𝐋𝐎𝐖 👇</b>\n"
                    "------------------------------------------------------------\n\n"
                    f"<b>{notes_message}</b>\n"
                    "------------------------------------------------------------\n\n"
                    "<b>𝗠𝗮𝗱𝗲 𝗕𝘆 𝗛𝗔𝗖𝗞𝗛𝗘𝗜𝗦𝗧 😈</b>\n"
                    "CONTACT US - @TEAM_OPTECH\n\n"
                    "You Are on Last page for more Lectures,Notes - /start"
                ),
                parse_mode="HTML",
                disable_web_page_preview=False  # Enable web preview
            )
        else:
            await query.edit_message_text(text="No lessons or notes found for this topic.")

    elif data.startswith("notes_"):
        _, batch_id, subject_id, topic_id = data.split("_")
        notes = fetch_notes(batch_id, subject_id, topic_id)
        if notes:
            notes_message = "\n\n".join([f"🌟<a href=\"{html.escape(note['docUrl'])}\">{html.escape(note['docTitle'])}</a>" for note in notes])
            await query.edit_message_text(text=f"<b> 𝐀𝐋𝐋 𝐍𝐎𝐓𝐄𝐒 𝐁𝐄𝐋𝐎𝐖 👇</b>\n------------------------------------------------------------\n\n<b>{notes_message}</b>\n------------------------------------------------------------\n\n<b>𝗠𝗮𝗱𝗲 𝗕𝘆 𝗛𝗔𝗖𝗞𝗛𝗘𝗜𝗦𝗧 😈</b>\nCONTACT US - @TEAM_OPTECH\n\nYou Are on Last page for more Lectures,Notes - /start",
            parse_mode="HTML"
            )
        else:
            await query.edit_message_text(text="No notes available.")

# Main function
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()
