import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# API and Bot configurations
API_BASE_URL = "https://learning.motion.ac.in/motioneducation/api"
HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1NTU1NzEsImV4cGlyZXNfYXQiOiIyMDI1LTAxLTExIDEwOjIxOjM3In0._JCC-hCW4EdLzPVz-ktHdh2DhjX7u04cHxnD-RBJ3lc",
    "Content-Type": "application/json"
}

COURSES = [
    {"course_id": 221, "course_name": "Jee 12th GB SIR"},
    {"course_id": 223, "course_name": "Jee 12th Sanjivani"},
    {"course_id": 207, "course_name": "Jee 12th Online"},
    {"course_id": 228, "course_name": "Jee 12th STAR BATCH"},
   {"course_id": 217, "course_name": "Jee 13th (Online-English)"},
{"course_id": 229, "course_name": "Jee 13th STAR BATCH"},
]

CLASS_ID = 1
SUBJECTS = {
    "Physics": 1,
    "Chemistry": 2,
    "Maths": 3,
}

TOPICS ={
    "Physics": [
        {"topic_name": "Units & Dimensions and Basic Maths", "topic_id": 1},
        {"topic_name": "Wave Optics", "topic_id": 19},
        {"topic_name": "Electrostatics - I", "topic_id": 20},
        {"topic_name": "Electrostatics - II", "topic_id": 21},
        {"topic_name": "Gravitation", "topic_id": 22},
        {"topic_name": "Current Electricity", "topic_id": 23},
        {"topic_name": "Capacitor", "topic_id": 24},
        {"topic_name": "Magnetism", "topic_id": 25},
        {"topic_name": "Electromagnetic Induction", "topic_id": 26},
        {"topic_name": "Alternating Current", "topic_id": 27},
        {"topic_name": "Modern Physics-I", "topic_id": 28},
        {"topic_name": "Modern Physics-II", "topic_id": 29},
        {"topic_name": "Electronics (Semiconductor)", "topic_id": 30},
        {"topic_name": "Geo Optics", "topic_id": 18},
        {"topic_name": "Fluid", "topic_id": 15},
        {"topic_name": "Kinematics", "topic_id": 3},
        {"topic_name": "Constraint Motion NLM Friction", "topic_id": 4},
        {"topic_name": "Circular Motion", "topic_id": 5},
        {"topic_name": "Work, Power & Energy", "topic_id": 6},
        {"topic_name": "Center of Mass", "topic_id": 7},
        {"topic_name": "Rotational Motion", "topic_id": 8},
        {"topic_name": "Simple Harmonic Motion", "topic_id": 9},
        {"topic_name": "Waves", "topic_id": 10},
        {"topic_name": "Sound Waves", "topic_id": 11},
        {"topic_name": "Heat-1", "topic_id": 12},
        {"topic_name": "Heat-2", "topic_id": 13},
        {"topic_name": "Thermal Expansion + Elasticity", "topic_id": 14},
        {"topic_name": "Electro Magnetic Wave", "topic_id": 364}
    ],
    "Chemistry": [
        {"topic_name": "Ionic Equilibrium", "topic_id": 33},
        {"topic_name": "Amine (-NH2) Test of phenol", "topic_id": 63},
        {"topic_name": "Chemical Bonding", "topic_id": 64},
        {"topic_name": "Coordination", "topic_id": 65},
        {"topic_name": "P Block", "topic_id": 68},
        {"topic_name": "D & F Block", "topic_id": 69},
        {"topic_name": "Stoichiometry (I) /Mole", "topic_id": 158},
        {"topic_name": "GOC", "topic_id": 165},
        {"topic_name": "Chemical Kinetics", "topic_id": 228},
        {"topic_name": "Hydrocarbon", "topic_id": 355},
        {"topic_name": "Salt Analysis", "topic_id": 1443},
        {"topic_name": "Alcohol Phenol ether", "topic_id": 56},
        {"topic_name": "Carboxylic Acid & Derivative", "topic_id": 51},
        {"topic_name": "Biomolecule & Polymer", "topic_id": 50},
        {"topic_name": "Electro Chemistry", "topic_id": 34},
        {"topic_name": "Liquid Solution", "topic_id": 36},
        {"topic_name": "Atomic Structure", "topic_id": 40},
        {"topic_name": "Chemical Equilibrium", "topic_id": 42},
        {"topic_name": "Thermodynamics", "topic_id": 43},
        {"topic_name": "Thermochemistry", "topic_id": 44},
        {"topic_name": "Stoichiometry (II)/Redox Reactions", "topic_id": 45},
        {"topic_name": "Isomerism", "topic_id": 47},
        {"topic_name": "Alkyl Halide Aryl Halide", "topic_id": 48},
        {"topic_name": "Aromatic Compound", "topic_id": 49},
        {"topic_name": "Grignard Reagent", "topic_id": 2464}
    ],
    "Maths": [
        {"topic_name": "Basic Maths and Log", "topic_id": 110},
        {"topic_name": "VECTOR", "topic_id": 127},
        {"topic_name": "3-Dimension", "topic_id": 128},
        {"topic_name": "MATRIX", "topic_id": 129},
        {"topic_name": "Determinant", "topic_id": 130},
        {"topic_name": "Function", "topic_id": 131},
        {"topic_name": "Permutation Combination", "topic_id": 132},
        {"topic_name": "Probability", "topic_id": 136},
        {"topic_name": "Trigonometry Phase-I", "topic_id": 137},
        {"topic_name": "Complex Number", "topic_id": 138},
        {"topic_name": "Parabola, Ellipse & Hyperbola", "topic_id": 139},
        {"topic_name": "Tangents Normals", "topic_id": 140},
        {"topic_name": "Monotonicity", "topic_id": 141},
        {"topic_name": "Maxima & Minima", "topic_id": 142},
        {"topic_name": "Method of differentiation", "topic_id": 126},
        {"topic_name": "Area Under the Curve", "topic_id": 125},
        {"topic_name": "Quadratic Equation", "topic_id": 111},
        {"topic_name": "Progressions", "topic_id": 112},
        {"topic_name": "Binomial Theorem", "topic_id": 113},
        {"topic_name": "Trigonometry Phase-II", "topic_id": 114},
        {"topic_name": "Limits", "topic_id": 116},
        {"topic_name": "Continuity", "topic_id": 117},
        {"topic_name": "Differentiability", "topic_id": 118},
        {"topic_name": "Straight Line", "topic_id": 119},
        {"topic_name": "Circle", "topic_id": 120},
        {"topic_name": "Definite Integration", "topic_id": 121},
        {"topic_name": "Indefinite Integration", "topic_id": 122},
        {"topic_name": "Inverse Trigonometric Functions", "topic_id": 123},
        {"topic_name": "Differential equation", "topic_id": 124},
        {"topic_name": "JEE MAINS TOPICS", "topic_id": 1445}
    ]
}

# Global storage for dynamic selections
USER_SELECTIONS = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send buttons for courses."""
    keyboard = [
        [InlineKeyboardButton(course["course_name"], callback_data=f"course_{course['course_id']}")]
        for course in COURSES
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("<b>🏅Welcome to Our Bot This is made by HACKHEIST 😈</b>\n\n<b>If you don't know how to use bot Click on below button 🥰\n<a href='https://t.me/hotousebotes/6'>𝐇𝐎𝐖 𝐓𝐎 𝐔𝐒𝐄 𝐁𝐎𝐓 ?🧐</a></b>\n\nNOTE - M@TION tech Team wants to Remove this bot message me @HACKHEISTBOT\nTech Team Check <b><a href='https://t.me/RemoveIIT/3'>𝗚𝗨𝗜𝗗𝗘𝗟𝗜𝗡𝗘𝗦</a></b>\n\n<b><a href='https://t.me/HIDDEN_OFFICIALS_5/3'>✮:▹ 𝗖𝗹𝗶𝗰𝗸 𝗧𝗼 𝗚𝗲𝘁 𝗠𝗢𝗥𝗘 🤩</a></b>", 
        reply_markup=reply_markup,
        protect_content=True,
        parse_mode='HTML'
    )

async def course_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle course selection and fetch subjects."""
    query = update.callback_query
    await query.answer()
    course_id = int(query.data.split("_")[1])
    USER_SELECTIONS[query.from_user.id] = {"course_id": course_id}

    keyboard = [
        [InlineKeyboardButton(subject, callback_data=f"subject_{SUBJECTS[subject]}")]
        for subject in SUBJECTS.keys()
    ]
    keyboard.append([InlineKeyboardButton("𝗚𝗼 𝗯𝗮𝗰𝗸 𝗖𝗼𝘂𝗿𝘀𝗲𝘀", callback_data="go_back_courses")])  # Go back to course selection
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text("𝐂𝐡𝐨𝐨𝐬𝐞 𝐚 𝐒𝐮𝐛𝐣𝐞𝐜𝐭", reply_markup=reply_markup)

async def subject_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle subject selection and fetch topics."""
    query = update.callback_query
    await query.answer()
    subject_id = int(query.data.split("_")[1])
    USER_SELECTIONS[query.from_user.id]["subject_id"] = subject_id
    subject_name = [name for name, id in SUBJECTS.items() if id == subject_id][0]
    topics = TOPICS.get(subject_name, [])
    
    keyboard = [
        [InlineKeyboardButton(topic["topic_name"], callback_data=f"topic_{topic['topic_id']}")]
        for topic in topics
    ]
    keyboard.append([InlineKeyboardButton("𝐆𝐨 𝐁𝐚𝐜𝐤 𝐒𝐮𝐛𝐣𝐞𝐜𝐭 ", callback_data="go_back_subjects")])  # Go back to subject selection
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text("◆ ᴄʜᴏᴏsᴇ ᴄʜᴀᴘᴛᴇʀ 👻", reply_markup=reply_markup)

async def topic_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle topic selection and fetch videos and notes."""
    query = update.callback_query
    await query.answer()
    topic_id = int(query.data.split("_")[1])
    user_data = USER_SELECTIONS[query.from_user.id]
    subject_id = user_data["subject_id"]

    # Fetch video data
    video_url = f"{API_BASE_URL}/v1/get/live/videos/?subject_id={subject_id}&topic_id={topic_id}&type=live&page=1"
    video_response = requests.get(video_url, headers=HEADERS)
    video_message = "𝗟𝗘𝗖𝗧𝗨𝗥𝗘𝗦 ✨\n"
    if video_response.status_code == 200:
        videos = video_response.json().get("data", [])
        for video in videos:
            title = video.get("video_title", "N/A")
            faculty = video.get("faculty", "N/A")
            join_url = video.get("join_url", "N/A")
            playback_url = fetch_playback_url(join_url) if join_url != "N/A" else "N/A"
            video_message += f"★ Name - {title}\n◇ Link - {playback_url}\n💥 Teacher - {faculty}\n😈 𝗕𝗬 𝗛𝗔𝗖𝗞𝗛𝗘𝗜𝗦𝗧\n\n"
    else:
        video_message += "Failed to fetch videos.\n"
   

    # Fetch notes data
    notes_url = f"{API_BASE_URL}/user/NotesList?page=1&search=&course_id={user_data['course_id']}&subject_id={subject_id}&topic_id={topic_id}"
    notes_response = requests.get(notes_url, headers=HEADERS)
    notes_message = "🏅𝗡𝗢𝗧𝗘𝗦\n"
    if notes_response.status_code == 200:
        notes = notes_response.json().get("data", {}).get("NotesList", {}).get("data", [])
        for note in notes:
            notes_title = note.get("notes_title", "N/A")
            note_url = note.get("notes", "N/A")
            notes_message += f"☆NAME - {notes_title}\n:-)LINK - {note_url}\n😈𝐁𝐘 𝐇𝐀𝐂𝐊𝐇𝐄𝐈𝐒𝐓\n\n"
            
    else:
        notes_message += "Failed to fetch notes.\n"

    await query.message.reply_text(video_message, protect_content=True)
    await query.message.reply_text(notes_message, protect_content=True)

async def go_back_to_courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Go back to course selection."""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton(course["course_name"], callback_data=f"course_{course['course_id']}")]
        for course in COURSES
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text("Choose a course:", reply_markup=reply_markup, protect_content=True)

async def go_back_to_subjects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Go back to subject selection."""
    query = update.callback_query
    await query.answer()
    course_id = USER_SELECTIONS[query.from_user.id]["course_id"]

    keyboard = [
        [InlineKeyboardButton(subject, callback_data=f"subject_{SUBJECTS[subject]}")]
        for subject in SUBJECTS.keys()
    ]
    keyboard.append([InlineKeyboardButton("Go back", callback_data="go_back_courses")])  # Go back to course selection
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text("Choose a subject:", reply_markup=reply_markup, protect_content=True)

def fetch_playback_url(join_url):
    """Extract playback URL from join_url."""
    if not join_url:
        return "N/A"
    unique_id = "_".join(join_url.split("/")[-1].split("_")[:2])
    url = f"{API_BASE_URL}/v1/streamos?id={unique_id}&isMobile=false&type=Recorded%20Live&device=web&is_ios=0"
    response = requests.post(url, headers=HEADERS, json={"headers": HEADERS})
    if response.status_code == 200:
        return response.json().get("data", {}).get("playbackurl", "N/A")
    return "N/A"


def main():
    """Run the bot."""
    application = Application.builder().token("7928178215:AAHrEazWka1JSkF8_5ym1Q1oxFRC-QLj5ow").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(course_callback, pattern="^course_"))
    application.add_handler(CallbackQueryHandler(subject_callback, pattern="^subject_"))
    application.add_handler(CallbackQueryHandler(topic_callback, pattern="^topic_"))
    application.add_handler(CallbackQueryHandler(go_back_to_courses, pattern="^go_back_courses$"))
    application.add_handler(CallbackQueryHandler(go_back_to_subjects, pattern="^go_back_subjects$"))

    application.run_polling()


if __name__ == "__main__":
    main()
