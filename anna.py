from nicegui import ui
import asyncio
from datetime import datetime
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

conn = sqlite3.connect('responses.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rating INTEGER,
    accepted_date_invite BOOLEAN,
    selected_date TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()

# Load credentials securely from environment variables
EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")
TO_EMAIL = "aayushkaushik0704@gmail.com"  # Replace with your email to receive responses

@ui.page("/")
def intro_page():
    # Apply background gradient globally to body
    ui.query('body').classes('bg-gradient-to-br from-pink-100 to-rose-200')

    with ui.column().classes('items-center justify-center w-full h-screen gap-4'):
        ui.label("✨ A Little Something for You ✨").classes("text-2xl font-bold text-pink-700 mb-4").style(
            "font-family: 'Dancing Script', cursive;")

        with ui.row().classes("justify-center mb-6"):
            ui.label("🎁").classes("text-3xl animate-pulse")

        # CSS and message with fade-in class
        ui.html("""
        <style>
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .fade-in {
                animation: fadeIn 2s ease-out forwards;
            }
        </style>

        <div id="message-box" class="fade-in" style="font-family: 'Dancing Script', cursive; text-align: justify; font-size: 18px; color: #4B0082;">
            <p style="margin-bottom: 12px;"><b>Dear Anna 📩,</b></p>
            <p style="margin-bottom: 12px;">This is something truly special, crafted just for you — with time, thought, and innovation.</p>
            <p style="margin-bottom: 12px;">Here's what awaits you:</p>
            <ul style="list-style: none; padding-left: 0; margin-bottom: 12px;">
                <li>1️⃣ A Gate to the Surprise 🎁</li>
                <li>2️⃣ A Magical Encounter with Emily ✨</li>
                <li>3️⃣ The Main Event 🎉</li>
                <li>4️⃣ A heartfelt Feedback & Follow-up 💬</li>
            </ul>
            <p style="margin-bottom: 12px;">I am sorry I made you wait a bit more than I wanted to, but the surprise is finally ready and I hope it brings a smile to your face 😊</p>
        </div>
        """)

        # Hidden button initially
        ui.button("Get Started 🚀", on_click=lambda: ui.navigate.to("/gate")).props('id=start-btn').classes(
            "hidden mt-6 bg-purple text-black-600 border border-pink-300 px-4 py-2 rounded-lg")

    # Add JS to show button after fade-in completes
    ui.add_body_html("""
    <script>
        setTimeout(() => {
            document.getElementById("start-btn").classList.remove("hidden");
        }, 2200); // show after fade-in
    </script>
    """)

# Use ui.state to keep session variables persistent across requests
ui.state.session = {
    'tap_count': 0,
    'gift_unlocked': False,
    'seven_tap_time': None,
}

ui.add_head_html(''' 
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&family=Roboto:wght@400;700&family=Dancing+Script&family=Lobster&display=swap" rel="stylesheet">
    <style>
        @keyframes confetti {
            0% { transform: translateY(0); opacity: 1; }
            100% { transform: translateY(100vh); opacity: 0; }
        }
        .confetti {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 5px;
            height: 10px;
            background-color: #FFD700;
            animation: confetti 2s infinite;
            animation-delay: calc(-0.5s * var(--i));
        }
    </style>
''')

@ui.page('/gate')
def gift_gate():
    # Match background with intro page
    ui.query('body').classes('bg-gradient-to-br from-pink-100 to-rose-200')

    with ui.column().classes('items-center justify-center w-full h-screen gap-4'):

        # Friendly and exciting header
        ui.label("🎁 Ready for the Surprise? 🎁").style(
            "font-size: 30px; font-family: 'Lobster', cursive; font-weight: bold; color: #9D174D;"
        )

        # Light instruction and emotional continuity
        ui.html(''' 
            <div style="text-align: center; font-size: 20px; color: #7851A9; font-family: 'Dancing Script', cursive;">
                Anna, this magical gate hides your surprise!<br><br>
                Tap the gift slowly <b>13 times</b> and let the universe unfold something special ✨
            </div>
        ''')

        # Tap counter display
        tap_display = ui.label(f"Taps: {ui.state.session.get('tap_count', 0)}/13").classes("text-center text-md").style(
            "font-family: 'Dancing Script', cursive; font-size: 18px;"
        )

        # Message shown during tapping
        message_label = ui.label('').style(
            "text-align: center; color: #D63384; font-size: 20px; font-family: 'Dancing Script', cursive; font-weight: bold;"
        )

        # Ensure session variable exists
        if 'tap_count' not in ui.state.session:
            ui.state.session['tap_count'] = 0

        def handle_tap():
            if ui.state.session['tap_count'] >= 13:
                return

            ui.state.session['tap_count'] += 1
            tap_display.text = f"Taps: {ui.state.session['tap_count']}/13"
            message_label.text = ''

            if ui.state.session['tap_count'] == 3:
                message_label.text = "You're doing great! 🎈 Keep going!"
            elif ui.state.session['tap_count'] == 7:
                message_label.text = "Almost there... the magic is near 🌟"
            elif ui.state.session['tap_count'] == 12:
                message_label.text = "Just one more tap to unlock the joy! 🗝️"

            if ui.state.session['tap_count'] == 13:
                ui.state.session['gift_unlocked'] = True
                message_label.text = "🎉 Wohoooo! The gateway is now OPEN! Let’s go! 💫"

                ui.add_head_html(''' 
                    <script>
                        let numberOfConfetti = 100;
                        for (let i = 0; i < numberOfConfetti; i++) {
                            let confettiPiece = document.createElement('div');
                            confettiPiece.classList.add('confetti');
                            confettiPiece.style.setProperty('--i', i);
                            document.body.appendChild(confettiPiece);
                        }
                    </script>
                ''')

                # Button to proceed to chat
                ui.button("Enter the Realm 💖", on_click=lambda: ui.navigate.to('/chat')).style(
                    "margin-top: 16px; background-color: #7E22CE; color: white; font-family: 'Dancing Script', cursive; border-radius: 12px; padding: 12px 24px; font-size: 18px;"
                )

        # Gift emoji click area
        ui.html('<div style="font-size: 120px; cursor: pointer;">🎁</div>').on('click', handle_tap)


# Emojis and messages organized for reuse
MOODS = {
    "😊 Happy": "Happy",
    "😢 Sad": "Sad",
    "🤩 Excited": "Excited",
    "🧐 Curious": "Curious",
    "😌 Relaxed": "Relaxed"
}

MOOD_EMOJIS = {
    "Happy": "😊",
    "Sad": "😢",
    "Excited": "🤩",
    "Curious": "🧐",
    "Relaxed": "😌"
}

compliments = {
    "Happy": "That's so wonderful to hear! You shine brightest when you're smiling ☀️😊",
    "Sad": "Awww... I didn't expect that but I am here to lift up your mood 💜😢",
    "Excited": "Yayyyyyy! Your excitement is infectious! 🎉🤩",
    "Curious": "Ooooo, curiosity is a sign of brilliance ✨🧐",
    "Relaxed": "It's so great to hear you're feeling at peace! 💆‍♀️😌"
}

IDENTITY_CHOICES = {
    "Yes, I know!": "Yes, I know!",
    "No, who are you?": "No, who are you?",
    "Not sure, are you famous?": "Not sure, are you famous?"
}

# New Theme Colors for Instagram-like look
THEME_COLORS = {
    "Sunset Red": "#D14B5D",  # Red tones
    "Emerald Green": "#50C878",  # Green tones
    "Golden Yellow": "#FFD700",  # Yellow tones
    "Midnight Black": "#2C3E50"  # Dark tones
}

@ui.page('/chat')
async def chat_page():
    # Variables to store the current theme
    current_theme = {
        "name": "Instagram Blue and Purple",
        "primary": "#8A3FFC",  # Purple for Emily
        "text": "#ffffff",
        "bg": "#E1E5F2",  # Light background like Instagram
        "bubble_emily": "#8A3FFC",  # Purple for Emily's bubble
        "bubble_anna": "#4C8BF5"  # Blue for Anna's bubble
    }

    # JS function to scroll chat to bottom
    def scroll_chat_to_bottom():
        ui.run_javascript("""
            const chatContainer = document.querySelector('[style*="max-height: 600px"]');
            if (chatContainer) {
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
        """)

    # Timer to scroll chat every second
    ui.timer(0.5, scroll_chat_to_bottom)  # every 1 second

    # Bottom options row with buttons or options
    bottom_options_row = ui.row().classes('fixed bottom-100 left-0 right-0 justify-center gap-2 z-50')

    with ui.column().classes('items-center justify-start w-full h-screen p-4 bg-[#BDC3C7]'):

        # Chat container with max height above the bottom space
        with ui.column().classes(
                "w-full max-w-md bg-white p-3 rounded-xl shadow-md gap-3 overflow-y-auto flex-grow font-bold"
        ).style(
            "max-height: 600px; font-family: 'Dancing Script', cursive; font-size: 30px;"
        ) as chat_container:
            typing_label = ui.label('').classes('text-gray-500 italic text-sm')

        # Mood row (buttons or options) at the bottom
        with ui.row().classes(
                "w-full max-w-md gap-2 flex-wrap justify-center items-center bg-white p-2 shadow-md rounded-t-xl"
        ).style(
            "position: absolute; bottom: 100px; left: 50%; transform: translateX(-50%); z-index: 50; height: 100px;"
        ) as mood_row:
            pass

        # Function to update the UI theme
        def update_ui_theme(color_label: str):
            # Get the new color
            chosen_color = THEME_COLORS[color_label]
            if color_label == "Sunset Red":
                current_theme.update(primary="#D14B5D", text="#000000", bg="#FDE0DC", bubble_emily="#D14B5D", bubble_anna="#F1A7A1")
            elif color_label == "Emerald Green":
                current_theme.update(primary="#50C878", text="#000000", bg="#E6F8E4", bubble_emily="#50C878", bubble_anna="#A8E6A0")
            elif color_label == "Golden Yellow":
                current_theme.update(primary="#FFD700", text="#000000", bg="#FFF6E1", bubble_emily="#FFD700", bubble_anna="#FFEB8A")
            elif color_label == "Midnight Black":
                current_theme.update(primary="#2C3E50", text="#ffffff", bg="#BDC3C7", bubble_emily="#2C3E50", bubble_anna="#566573")

            # Apply changes to the UI
            ui.query('body').style(f"background-color: {current_theme['bg']};")
            ui.run_javascript(f'''
                const buttons = document.querySelectorAll('button');
                buttons.forEach(btn => {{
                    btn.style.backgroundColor = '{current_theme["primary"]}';
                    btn.style.color = '{current_theme["text"]}';
                }});
            ''')

        # Function to display message confirming theme change
        async def theme_changed_message(color_label: str):
            await emily_message(f"Let's continue chatting with this new vibe! 🎨")

        async def emily_message(text: str):
            with chat_container:
                typing_label.text = "Emily is typing..."
            await asyncio.sleep(1.2)
            typing_label.text = ''
            with chat_container:
                with ui.row().classes("w-full justify-start items-start gap-3"):
                    ui.label('🤖').classes('w-6 h-6 text-purple-600')
                    ui.label(text).classes("").style(
                        f"background-color: {current_theme['bubble_emily']}; color: {current_theme['text']}; "
                        "padding: 8px; border-radius: 1rem; max-width: 80%; font-size: 14px;"
                    )

        async def anna_message(text: str):
            # Display in UI
            with chat_container:
                with ui.row().classes("w-full justify-end items-start gap-3"):
                    ui.label('👸').classes('w-6 h-6 text-blue-600')
                    ui.label(text).classes("").style(
                        f"background-color: {current_theme['bubble_anna']}; color: {current_theme['text']}; "
                        "padding: 8px; border-radius: 1rem; max-width: 80%; font-size: 14px;"
                    )

            # Send Email
            try:
                EMAIL_ADDRESS = os.getenv("EMAIL_USER")
                EMAIL_PASSWORD = os.getenv("EMAIL_PASS")
                TO_EMAIL = "aayushkaushik0704@gmail.com"

                msg = MIMEMultipart("alternative")
                msg["Subject"] = "Anna's Reply in Chat"
                msg["From"] = EMAIL_ADDRESS
                msg["To"] = TO_EMAIL

                html_content = f"""
                <html>
                    <body>
                        <p><strong>Anna said:</strong><br>{text}</p>
                    </body>
                </html>
                """

                msg.attach(MIMEText(html_content, "html"))

                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
            except Exception as e:
                print("Failed to send email:", e)

        async def handle_mood_selection(feeling: str):
            mood_row.clear()
            emojis = {
                "Happy": "😊",
                "Sad": "😢",
                "Excited": "🤩",
                "Curious": "🧐",
                "Relaxed": "😌"
            }
            await anna_message(f"I'm feeling {feeling.lower()} {emojis[feeling]}")
            await respond_with_compliment(feeling)

        async def respond_with_compliment(feeling: str):
            await emily_message(compliments[feeling])
            await asyncio.sleep(2)
            await ask_about_emily()

        async def ask_about_emily():
            await emily_message("By the way, Anna... do you know who I am? 🤔")
            await asyncio.sleep(1)
            await show_know_emily_options()

        async def show_know_emily_options():
            await asyncio.sleep(1)
            mood_row.clear()
            with mood_row:
                options = {
                    "Yes, I know!": "Yes, I know!",
                    "No, who are you?": "No, who are you?",
                    "Not sure, are you famous?": "Not sure, are you famous?"
                }
                for label, value in options.items():
                    ui.button(
                        label,
                        on_click=lambda e=None, m=value: handle_anna_answer(m)
                    ).classes("bg-pink-400 text-white text-sm px-3 py-1.5 rounded-lg font-medium").props(
                        "flat").style("margin-bottom: 6px;")

        async def handle_anna_answer(answer: str):
            mood_row.clear()
            await anna_message(answer)
            await emily_reaction_based_on_answer(answer)

        async def emily_reaction_based_on_answer(answer: str):
            if answer == "Yes, I know!":
                await emily_message("Haha! You already know me, but I still have a HUGE task ahead! 💼")
            elif answer == "No, who are you?":
                await emily_message(
                    "Oh noo! 😱 Well, I’m Emily, and I've been created by the smartest person alive 😊...")
                await emily_message(
                    "He gave me bribe to say so 😂")
            else:
                await emily_message("That's a mystery! 😏 Well, I'm Emily and I've been created by the smartest person alive 😊...")
                await emily_message(
                    "He gave me bribe to say so 😂")
            await asyncio.sleep(2)
            await emily_talk_about_her_big_task()

        async def emily_talk_about_her_big_task():
            await emily_message("I’ve been assigned the BIGGEST responsibility of my career. 🎯 - TO IMPRESS YOU !")
            await asyncio.sleep(2)
            await emily_message("My job depends on the next 5 minutes... if I fail, I might just get fired! 😨")
            await asyncio.sleep(2)
            await emily_message("Firstly, let me show you a little magic trick 🪄. Pick a color from below!")
            await show_color_options()

        async def show_color_options():
            await asyncio.sleep(1)
            mood_row.clear()
            with mood_row:
                for label in THEME_COLORS.keys():
                    ui.button(
                        label,
                        on_click=lambda e=None, c=label: handle_color_selection(c)
                    ).classes("bg-pink-400 text-white text-sm px-3 py-1.5 rounded-lg font-medium").props("flat")

        async def handle_color_selection(color_label: str):
            mood_row.clear()
            await anna_message(f"I choose {color_label}!")
            await emily_message(f"Ooh {color_label} is a fantastic choice! 🎨")
            await asyncio.sleep(1)
            await apply_color_theme(color_label)
            await theme_changed_message(color_label)
            await start_rapid_fire()

        async def apply_color_theme(color_label: str):
            update_ui_theme(color_label)
            await emily_message(f"Tadaaaa! ✨ Everything's now bathed in the beautiful {color_label}!")

        rapid_fire_questions = [
            ("🍽️ What's your favorite cuisine?", [
                "🇮🇳 Indian", "🇹🇭 Thai", "🇮🇹 Italian", "🇲🇽 Mexican", "🇩🇪 German", "🌐 Other"
            ]),
            ("🎶 What's your favorite music genre?", [
                "🎤 Pop", "🎸 Rock", "🎷 Jazz", "🎻 Classical", "🎧 Electronic"
            ]),
            ("🎯 What's your favorite hobby?", [
                "🌱 Gardening", "📚 Reading", "🎬 Movies/Series", "🏀 Sports", "🎵 Music"
            ]),
            ("🎨 What's your favorite color?", [
                "🔵 Blue", "🔴 Red", "🟢 Green", "🟡 Yellow", "🩷 Pink", "⚫ Black", "⚪ White"
            ]),
            ("🌄 Are you a mountain person or beach person?", [
                "🏔️ Mountain", "🏖️ Beach"
            ]),
            ("🎞️ What's your favorite movie genre?", [
                "🔫 Action", "😂 Comedy", "🎭 Drama", "👻 Horror", "💖 Romance"
            ]),
            ("🍍 Pineapple on Pizza??", [
                "🍍✅ Yes, it tastes lovely!", "🍍❌ No, gross!"
            ]),
            ("🌟 So finally the main question — DID I DO WELL TO IMPRESS YOU???", [
                "😄👍 Yes, for sure!", "😬💪 You need to work hard!"
            ]),
        ]

        rapid_fire_compliments = {
            "🍽️ What's your favorite cuisine?": {
                "🇮🇳 Indian": "Ahh, full of spices and soul — I like it! 🌶️",
                "🇹🇭 Thai": "Sweet, spicy, and unique — Tastyyy! 🍜",
                "🇮🇹 Italian": "A classy choice — you have elegant taste 🍝",
                "🇲🇽 Mexican": "Bold and colorful — certainly a true firecracker! 🌮",
                "🇩🇪 German": "Strong, hearty, and full of surprises — I like it! 🥨",
                "🌐 Other": "I will get to know shortly!"
            },
            "🎶 What's your favorite music genre?": {
                "🎤 Pop": "Trendy and upbeat — lovelyyy! 🎤",
                "🎸 Rock": "You’ve got that rebellious spark — I like it! 🎸",
                "🎷 Jazz": "Smooth, classy, and full of depth — Niceee 🎷",
                "🎻 Classical": "Such grace and poise — your taste is timeless 🎻",
                "🎧 Electronic": "Energetic and electric — Awesomeeee! ⚡"
            },
            "🎯 What's your favorite hobby?": {
                "🌱 Gardening": "You nurture life — that’s beautiful 🌱",
                "📚 Reading": "Smart, thoughtful, and deep — I admire that 📚",
                "🎬 Movies/Series": "Nicee! I guess you love a bucket of popcorn alongside 🍿",
                "🏀 Sports": "A powerhouse of energy and passion — I see you! 🏅",
                "🎵 Music": "Creative and soulful — Nice vibe! 🎶"
            },
            "🎨 What's your favorite color?": {
                "🔵 Blue": "Cool, calm, and full of depth — beautiful choice! 🌊",
                "🔴 Red": "Fiery and bold — just like your spirit! 🔥",
                "🟢 Green": "Fresh, grounded, and full of life 🌿",
                "🟡 Yellow": "Bright and full of joy — sunshine vibes! ☀️",
                "🩷 Pink": "Soft yet powerful — a heart made of gold (and glitter)! 🎀",
                "⚫ Black": "Elegant and mysterious — like a midnight dream 🌌",
                "⚪ White": "Pure and peaceful — a calming presence 🤍"
            },
            "🌄 Are you a mountain person or beach person?": {
                "🏔️ Mountain": "Peaceful, powerful, and grounded — I love it! 🏔️",
                "🏖️ Beach": "Breezy, bright, and full of sunshine — Awesomeee! 🌊"
            },
            "🎞️ What's your favorite movie genre?": {
                "🔫 Action": "You love the thrill — definitely a bold soul! 🎬",
                "😂 Comedy": "Now I know the reason for your good Humor! 😂",
                "🎭 Drama": "So deep and emotional — I’m intrigued by your depth 🎭",
                "👻 Horror": "Fearless and fierce — Uhhhhhh! I hope you get scared 👻",
                "💖 Romance": "Good choice... you’re a true heart-throb 💖"
            },
            "🍍 Pineapple on Pizza??": {
                "🍍✅ Yes, it tastes lovely!": "Sweet and adventurous — you’ve got a bold palate! 🍕🍍",
                "🍍❌ No, gross!": "Classic and pure — sticking to the real deal! 🍕😎"
            },
            "🌟 So finally the main question — DID I DO WELL TO IMPRESS YOU???": {
                "😄👍 Yes, for sure!": "Yayyyy, I will keep my job 😄🎉",
                "😬💪 You need to work hard!": "I will be fired now 😢💼💔"
            },
        }

        async def start_rapid_fire():
            await asyncio.sleep(1)
            await emily_message("Let's play a rapid-fire round! ⚡️")
            await asyncio.sleep(0.5)
            await emily_message("Be honest as someone is watching you 👀")
            await asyncio.sleep(0.5)
            await ask_next_rapid_question()

        async def ask_next_rapid_question():
            nonlocal current_question_index
            if current_question_index < len(rapid_fire_questions):
                typing_label.text = "Emily is typing..."
                await asyncio.sleep(1.2)
                typing_label.text = ''
                question, options = rapid_fire_questions[current_question_index]
                await emily_message(question)
                await show_rapid_options(options)
            else:
                await emily_message("Wowwwww, that was soo much fun, Anna! Thanks for playing with me 😄 !!")
                await asyncio.sleep(1)
                await emily_message("Now let’s move to the next and the best part of this surprise... The MAIN EVENT ✨")
                await asyncio.sleep(1)
                await emily_message("My creator has something special for you. Click below to view it 💌")

                # Show button to proceed
                bottom_options_row.clear()
                ui.button(
                    "View the Main Event 💝",
                    on_click=lambda: ui.navigate.to("/surprise")
                ).classes("bg-pink-500 text-white px-4 py-2 rounded-full text-lg shadow-md").props("flat")

        async def show_rapid_options(options):
            await asyncio.sleep(0.5)
            bottom_options_row.clear()
            for opt in options:
                ui.button(
                    opt,
                    on_click=lambda e=None, a=opt: handle_rapid_answer(a)
                ).classes("bg-pink-400 text-white text-sm px-3 py-1.5 rounded-lg font-medium").props("flat")

        async def handle_rapid_answer(answer: str):
            nonlocal current_question_index
            mood_row.clear()
            await anna_message(answer)
            await asyncio.sleep(0.5)

            # Get question
            question, _ = rapid_fire_questions[current_question_index]
            # Look up custom compliment
            compliment = rapid_fire_compliments.get(question, {}).get(answer, "That's a lovely choice!")
            await emily_message(compliment)

            current_question_index += 1
            await asyncio.sleep(1)
            await ask_next_rapid_question()

        async def start_chat():
            await emily_message("Hi Anna 🌸 Welcome !!! I was waiting for you 😊.")
            await emily_message("Tell me...How are you feeling right now???")
            await show_mood_buttons()

        async def show_mood_buttons():
            await asyncio.sleep(1)
            with mood_row:
                moods = {
                    "😊 Happy": "Happy",
                    "😢 Sad": "Sad",
                    "🤩 Excited": "Excited",
                    "🧐 Curious": "Curious",
                    "😌 Relaxed": "Relaxed"
                }
                for label, value in moods.items():
                    ui.button(
                        label,
                        on_click=lambda e=None, m=value: handle_mood_selection(m)
                    ).classes("bg-pink-400 text-white text-sm px-3 py-1.5 rounded-lg font-small").props("flat")

        await start_chat()

@ui.page("/surprise")
def surprise_page():
    with ui.column().classes("items-center justify-start w-full min-h-screen bg-gradient-to-br from-pink-100 to-rose-200"):
        ui.label("A Note from Me to You, Anna 💕").classes(
            "text-2xl font-bold text-pink-700 mt-6 mb-4"
        ).style("font-family: 'Dancing Script', cursive;")

        with ui.row().classes("justify-center mb-4"):
            ui.label("💗").classes("text-3xl animate-pulse")

        with ui.row().classes("justify-center w-full"):
            with ui.column().classes("items-center w-full max-w-2xl px-4"):
                ui.html("""
                <style>
                    @keyframes fadeIn {
                        from { opacity: 0; transform: translateY(20px); }
                        to { opacity: 1; transform: translateY(0); }
                    }
                    .fade-in {
                        animation: fadeIn 2.5s ease-out forwards;
                    }
                    .scroll-box {
                        max-height: 500px;
                        overflow-y: auto;
                        scroll-behavior: smooth;
                    }
                    .scroll-box::-webkit-scrollbar {
                        width: 8px;
                    }
                    .scroll-box::-webkit-scrollbar-thumb {
                        background-color: #e0aaff;
                        border-radius: 4px;
                    }
                </style>

                <div class="fade-in scroll-box" style="font-family: 'Dancing Script', cursive; text-align: justify; font-size: 18px; color: #4B0082; background-color: #fdf6ff; border-radius: 12px; padding: 1.8rem; line-height: 1.7; box-shadow: 0 6px 14px rgba(0, 0, 0, 0.1);">

                  <h2 style="text-align: center; font-size: 26px; margin-bottom: 1rem; color: #800080;">Just Something I Needed to Say</h2>

                  <p>Hey Anna,</p>

                  <p>Maybe this is coming out of the blue — or maybe you’re sharp enough to have sensed it. Either way, there’s something I’ve been holding in, and if I don’t say it now, I know I’ll regret it.</p>

                  <p>Do you believe in God’s plan? I think I do. Starting my internship two weeks early might’ve seemed rushed at the time, but looking back, I’m so glad I did. Because if I hadn’t… maybe I’d never have met you.</p>

                  <p>Those few days at Bosch Murrhardt weren’t a long time, but they were enough for something to spark. I saw a genuine warmth in you — the kind, friendly nature that stood out quietly yet unmistakably. I mentioned that in the little note I gave you when you left, but honestly, that note didn’t even scratch the surface.</p>

                  <p>Maybe it was just your job, or maybe... that’s simply who you are. Either way, I truly admired it.</p>

                  <p>Then came Snapchat — oddly enough, on your birthday — and that small streak turned into full conversations. At first, it was just casual snaps. Then came the messages. Then came the chats. And before I knew it, we were talking about everything from food and festivals to spirituality, culture, beliefs, and more.</p>

                  <p>That’s when I realized something: You’re not just fun and kind — you’re also incredibly thoughtful and mature. Some of your insights honestly made me pause and think, “Is this really coming from someone who’s just 23?”</p>

                  <p>There’s a wisdom in you that’s rare. Your sense of humor, your understanding, the way you see life — it all felt so grounded, so real. It’s something I genuinely admire and respect.</p>

                  <p>This is probably the first time I’ve opened up like this to anyone. But I don’t regret it. In fact, I think everything happened the way it was supposed to — like it was all part of a quiet plan. And maybe, just maybe, it’s meant to be something more.</p>

                  <p>You might not believe it, but you really are one of the best people I’ve had the chance to meet. I admire your honesty, your spirit, your thoughts — and I’d love to keep getting to know you, to hear more, to share more.</p>

                  <p>This little surprise? It’s just a small reflection of how much I appreciate you. And I’ll say it again, Anna — you truly are a wonderful person.</p>

                  <p style="text-align: right; margin-top: 2rem;">🌟<br>Someone who’s really glad the universe had a quiet plan</p>
                </div>
                """)

        ui.button("Continue to the Last Stage →", on_click=lambda: ui.navigate.to("/date")).props(
            'id=continue-btn').classes(
            "hidden mt-6 bg-purple text-black-600 border border-pink-300 px-4 py-2 rounded-lg"
        )

    # Reveal button after 2.3s
    ui.add_body_html("""
    <script>
        setTimeout(() => {
            document.getElementById("continue-btn").classList.remove("hidden");
        }, 2300);
    </script>
    """)

def send_email_notification(rating, accepted, selected_date=None):
    subject = "💌 New Response from Anna"

    if accepted:
        message = (
            f"Anna rated the experience {rating}/10 and said YES to the date! 💖\n"
            f"Selected date: {selected_date}"
        )
    else:
        message = f"Anna rated the experience {rating}/10 and declined the date invite. 🙁"

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("✅ Email sent.")
    except Exception as e:
        print("❌ Failed to send email:", e)

@ui.page("/date")
def date_page():
    state = {"date_handled": False}

    with ui.column().classes(
        'h-screen w-full justify-center items-center bg-gradient-to-br from-pink-100 to-rose-200 gap-8'
    ):
        ui.html("""
        <style>
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes fadeOut {
                from { opacity: 1; transform: translateY(0); }
                to { opacity: 0; transform: translateY(20px); }
            }
            .fade-in {
                animation: fadeIn 1.2s ease-out forwards;
            }
            .fade-out {
                animation: fadeOut 0.8s ease-in forwards;
            }
        </style>
        <div class="fade-in">
            <h1 style="font-size: 1.5rem; font-weight: bold; text-align: center;">🎉 Welcome to the Final Stage! 🎉</h1>
        </div>
        """)

        ui.label("🌟 Anna, how would you rate your overall experience?").classes("text-lg font-semibold")

        rating_slider = ui.slider(min=1, max=10, value=5, step=1)
        rating_slider.classes("w-64 bg-gradient-to-r from-pink-400 to-red-400 rounded-full")

        feedback_label = ui.label("").classes("mt-2 text-pink-700 text-lg font-medium").style(
            "font-family: 'Dancing Script', cursive;"
        )
        submit_button_container = ui.row().classes("mt-4")
        date_container = ui.column().classes("items-center justify-center gap-4 mt-6")

        def ask_for_date():
            ui.timer(2.0, lambda: render_date_question(), once=True)

        def render_date_question():
            def show_question():
                with date_container:
                    question_label = ui.label("💬 Would you like to go on a Date with me?").classes(
                        "text-xl font-bold text-pink-800 opacity-0 transition-opacity duration-1000"
                    ).style("font-family: 'Dancing Script', cursive;").props('id="date-question"')

                    ui.timer(0.2, lambda: question_label.classes(remove="opacity-0"), once=True)

                    with ui.row().classes("gap-4 mt-2"):
                        def yes_response():
                            state["date_handled"] = True
                            feedback_label.text = ""
                            question_label.classes(add="fade-out")
                            ui.timer(0.8, lambda: (
                                date_container.clear(),
                                show_date_picker()
                            ), once=True)

                        def no_response():
                            state["date_handled"] = True
                            feedback_label.text = ""
                            question_label.classes(add="fade-out")
                            ui.timer(0.8, lambda: (
                                date_container.clear(),
                                show_not_ready_message()
                            ), once=True)

                        ui.button("Yes 💕", on_click=yes_response).classes("bg-green-500 text-white px-4 py-2 rounded")
                        ui.button("Not yet 🙈", on_click=no_response).classes("bg-gray-300 text-black px-4 py-2 rounded")

            def show_date_picker():
                with date_container:
                    ui.label("🥰 Yaaay! I'm so excited! Just a few more things...").classes(
                        "text-lg text-pink-700"
                    ).style("font-family: 'Dancing Script', cursive;")

                    ui.label("Pick a date for our special day:").classes("mt-4")
                    date_picker = ui.date()
                    date_text_input = ui.input("Selected date").classes("w-64")
                    date_text_input.visible = False

                    def update_date_input():
                        if date_picker.value:
                            date_text_input.value = str(date_picker.value)
                            date_text_input.visible = True
                            date_picker.visible = False

                    date_picker.on_value_change(update_date_input)

                    def submit_final():
                        selected_date = str(date_text_input.value)
                        rating = rating_slider.value
                        accepted = True

                        cursor.execute('''
                            INSERT INTO responses (rating, accepted_date_invite, selected_date)
                            VALUES (?, ?, ?)
                        ''', (rating, accepted, selected_date))
                        conn.commit()

                        send_email_notification(rating, accepted, selected_date)

                        ui.label("Yayyyy, the efforts paid off !!!").classes(
                            "text-lg text-pink-600"
                        ).style("font-family: 'Dancing Script', cursive;")
                        ui.notify(f"Can't wait for {selected_date} 🎉", type="positive", duration=6)

                    ui.button("Confirm 💕", on_click=submit_final).classes(
                        "mt-4 bg-pink-600 text-white px-4 py-2 rounded"
                    )

            def show_not_ready_message():
                rating = rating_slider.value
                accepted = False

                cursor.execute('''
                    INSERT INTO responses (rating, accepted_date_invite, selected_date)
                    VALUES (?, ?, ?)
                ''', (rating, accepted, None))
                conn.commit()

                send_email_notification(rating, accepted, None)

                with date_container:
                    ui.label("That's okay! I'll be right here when you're ready. 💗").classes(
                        "text-lg text-pink-600"
                    ).style("font-family: 'Dancing Script', cursive;")

            ui.timer(1.0, show_question, once=True)

        def handle_rating_submit():
            submit_button_container.clear()
            if rating_slider.value >= 6:
                feedback_label.text = "✨ Awww, I'm so glad! I have one last question for you..."
                ask_for_date()
            else:
                feedback_label.text = (
                    "😔 Oh no... I tried my best to impress you but thank you for being honest. You’re still amazing 💖\n"
                    "You can exit the browser now!"
                )

                cursor.execute('''
                    INSERT INTO responses (rating, accepted_date_invite, selected_date)
                    VALUES (?, ?, ?)
                ''', (rating_slider.value, False, None))
                conn.commit()

                send_email_notification(rating_slider.value, False, None)

        with submit_button_container:
            ui.button("Go Ahead 💌", on_click=handle_rating_submit).classes(
                "bg-pink-500 text-white px-4 py-2 rounded-full text-md shadow-md")

        def close_browser():
            ui.notify("Please close the browser tab manually. 💖", type="warning", duration=4)

        with ui.row().classes("mt-4"):
            ui.button("Exit ❌", on_click=close_browser).classes("bg-red-500 text-white px-4 py-2 rounded")

ui.run(title="A Little Something for Anna", port=8082, reload=False)
