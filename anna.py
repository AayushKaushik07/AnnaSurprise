from nicegui import ui
import asyncio
from datetime import datetime

# Use ui.state to keep session variables persistent across requests
ui.state.session = {
    'tap_count': 0,
    'gift_unlocked': False,
    'seven_tap_time': None,
}

# Fonts & Confetti styles
ui.add_head_html(''' 
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Lobster&family=Dancing+Script&display=swap" rel="stylesheet">
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

@ui.page('/')
def gift_gate():
    ui.query('body').style('background-color:  #C497D6; color: black;')

    with ui.column().classes('items-center justify-center w-full h-screen gap-4'):
        ui.label("🎁 Helloooo Anna 🎁").style(
            "font-size: 36px; font-family: 'Poppins', sans-serif; font-weight: bold; color: black;")

        ui.html(''' 
            <div style="text-align: center; font-size: 18px; color: black; font-family: 'Roboto', sans-serif;">
                The universe is delivering this specially curated surprise to you. ✨<br><br>
                Tap the gift <b>13 times</b> to open the gate to your surprise 🌟
            </div>
        ''')

        tap_display = ui.label(f"Taps: {ui.state.session['tap_count']}/13").classes("text-center text-md")
        message_label = ui.label('').style(
            "text-align: center; color: #E91E63; font-size: 18px; font-family: 'Roboto', sans-serif; font-weight: bold;")

        def handle_tap():
            if ui.state.session['tap_count'] >= 13:
                return

            ui.state.session['tap_count'] += 1
            tap_display.text = f"Taps: {ui.state.session['tap_count']}/13"

            # Clear previous message
            message_label.text = ''

            if ui.state.session['tap_count'] == 3:
                message_label.text = "Come on, keep going! 💪"
            elif ui.state.session['tap_count'] == 7:
                message_label.text = "😣 Slowww... it hurts! It's not a race :("

            if ui.state.session['tap_count'] == 13:
                ui.state.session['gift_unlocked'] = True
                message_label.text = "🎉 Wohoooo, You've successfully opened the gateway to your surprise! 🪄"

                # Add confetti
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

                ui.button("Get Started 💫", on_click=lambda: ui.navigate.to('/chat')).style(
                    "margin-top: 16px; background-color: #000000; color: white; font-family: 'Roboto', sans-serif; border-radius: 8px; padding: 10px 20px;")

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

    # Bottom options row with buttons or options
    bottom_options_row = ui.row().classes('fixed bottom-80 left-0 right-0 justify-center gap-2 z-50')

    with ui.column().classes('items-center justify-start w-full h-screen p-4 bg-[#BDC3C7]'):

        # Chat container with max height above the bottom space
        with ui.column().classes(
                "w-full max-w-md bg-white p-3 rounded-xl shadow-md gap-3 overflow-y-auto flex-grow"
        ).style(
            "max-height: 600px; font-family: 'Dancing Script', cursive; font-size: 15px;") as chat_container:
            typing_label = ui.label('').classes('text-gray-500 italic text-sm')

        # Mood row (buttons or options) at the bottom
        with ui.row().classes(
                "w-full max-w-md gap-2 flex-wrap justify-center items-center bg-white p-2 shadow-md rounded-t-xl"
        ).style(
            "position: absolute; bottom: 70px; left: 50%; transform: translateX(-50%); z-index: 50; height: 100px;") as mood_row:
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
            with chat_container:
                with ui.row().classes("w-full justify-end items-start gap-3"):
                    ui.label('👸').classes('w-6 h-6 text-blue-600')
                    ui.label(text).classes("").style(
                        f"background-color: {current_theme['bubble_anna']}; color: {current_theme['text']}; "
                        "padding: 8px; border-radius: 1rem; max-width: 80%; font-size: 14px;"
                    )

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
            await emily_message("I’ve been assigned the BIGGEST responsibility of my career. 🎯")
            await asyncio.sleep(2)
            await emily_message("My job depends on the next 5-10 minutes... if I fail, I might just get fired! 😨")
            await asyncio.sleep(2)
            await emily_message("Let me impress you with a little magic trick 🪄. Pick a color below!")
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
            await emily_message(f"Scroll down to see the magic !!!")
            await asyncio.sleep(1)
            await apply_color_theme(color_label)
            await theme_changed_message(color_label)
            await start_rapid_fire()

        async def apply_color_theme(color_label: str):
            update_ui_theme(color_label)
            await emily_message(f"Tada! ✨ Everything's now bathed in the beautiful {color_label}!")

        rapid_fire_questions = [
            ("What's your favorite cuisine?", ["Indian", "Thai", "Italian", "Mexican", "German", "Other"]),
            ("What's your favorite music genre?", ["Pop", "Rock", "Jazz", "Classical", "Electronic"]),
            ("What's your favorite hobby?", ["Gardening", "Reading", "Movies/Series", "Sports", "Music"]),
            ("Are you a mountain person or beach person?", ["Mountain", "Beach"]),
            ("What's your favorite movie genre?", ["Action", "Comedy", "Drama", "Horror", "Romance"]),
        ]

        current_question_index = 0

        rapid_fire_compliments = {
            "What's your favorite cuisine?": {
                "Indian": "Ahh, full of spices and soul — I like it! 🌶️",
                "Thai": "Sweet, spicy, and unique — Tastyyy! 🍜",
                "Italian": "A classy choice — you have elegant taste 🍝",
                "Mexican": "Bold and colorful — certainly a true firecracker! 🌮",
                "German": "Strong, hearty, and full of surprises — I like it! 🥨",
                "Other": "I will get to know shortly !"
            },
            "What's your favorite music genre?": {
                "Pop": "Trendy and upbeat — lovelyyy! 🎤",
                "Rock": "You’ve got that rebellious spark — I like it! 🎸",
                "Jazz": "Smooth, classy, and full of depth — Niceee 🎷",
                "Classical": "Such grace and poise — your taste is timeless 🎻",
                "Electronic": "Energetic and electric — Awesomeeee! ⚡"
            },
            "What's your favorite hobby?": {
                "Gardening": "You nurture life — that’s beautiful 🌱",
                "Reading": "Smart, thoughtful, and deep — I admire that 📚",
                "Movies/Series": "Niceeee! 🍿",
                "Sports": "A powerhouse of energy and passion — I see you! 🏅",
                "Music": "Creative and soulful — Nice vibe! 🎶"
            },
            "Are you a mountain person or beach person?": {
                "Mountain": "Peaceful, powerful, and grounded — Great ! 🏔️",
                "Beach": "Breezy, bright, and full of sunshine — Awesome ! 🌊"
            },
            "What's your favorite movie genre?": {
                "Action": "You love the thrill — definitely a bold soul! 🎬",
                "Comedy": "Now I know the reason for your good Humor! 😂",
                "Drama": "So deep and emotional — I’m intrigued by your depth 🎭",
                "Horror": "Fearless and fierce — Uhhhhhh! 👻",
                "Romance": "Good choice... you’re a true heart-throb 💖"
            }
        }

        async def start_rapid_fire():
            await asyncio.sleep(1)
            await emily_message("Let's play a rapid-fire round! ⚡️")
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
                await emily_message("Wowwwwwww, that was soo much fun, Anna! Thanks for playing with me !!")
                await asyncio.sleep(1)
                await emily_message("Now let’s move to the next and the best part of this surprise... ✨")
                await asyncio.sleep(1)
                await emily_message("My creator has something special for you. Click below to view it 💌")

                # Show button to proceed
                bottom_options_row.clear()
                ui.button(
                    "View the Surprise 💝",
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
            await emily_message("Hi Anna! 🌸 Welcome !!! I was waiting for you 😊.")
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
    ui.label("🎉 This is your surprise page! 🎉")
    with ui.column().classes("items-center justify-center w-full h-screen bg-gradient-to-br from-pink-100 to-rose-200"):
        ui.label("A Note from Me to You, Anna 💖").classes("text-3xl font-bold text-pink-700 mb-4").style(
            "font-family: 'Dancing Script', cursive;")

        with ui.row().classes("justify-center mb-6"):
            ui.label("💗").classes("text-6xl animate-pulse")

        # Personal message with handwritten font
        ui.label("""
                Hey Anna,

                I’ve been meaning to say this for a while — I genuinely feel lucky that our paths crossed.

                If I hadn’t started my internship early, maybe we’d never have met. But I did — and those two weeks gave me a glimpse of someone truly unforgettable.

                Over these past months, our conversations — about food, goals, beliefs, or just random jokes — have felt rare and real. You’ve shown a kind of wisdom and honesty I’ve never quite seen before. The way you see things, the clarity in your thoughts... it’s something I quietly admire more than you know.

                When I gave you that note, I said you have a charming personality — and I meant every word. You’ve only proven that more with time.

                It might sound a little cheesy, but I can’t help feeling like this was all meant to be. And honestly, I’m glad it happened.

                You’re a rare person, Anna. And I’d love to keep getting to know you.

                Maybe the universe had a quiet plan all along — and I’m really thankful it did. :)

                — Someone who's quietly grateful for it all 💫
                """).classes("text-lg text-center text-gray-800 max-w-xl px-4").style(
            "font-family: 'Dancing Script', cursive; text-align: justify;")

        ui.button("Continue to the Last Stage ->").on_click(lambda: ui.navigate.to("/date")).classes(
            "mt-6 bg-black text-pink-600 border border-pink-300 px-4 py-2 rounded-lg")

@ui.page('/date')
def date_page():
    ui.label("🎉 Welcome to the final stage! 🎉").classes("text-2xl font-bold text-center mt-4")

    with ui.column().classes("items-center justify-center w-full h-screen bg-gradient-to-br from-pink-100 to-rose-200"):
        ui.label("🌟 How would you rate your experience?").classes("text-lg font-semibold mt-2 mb-1")
        rating = ui.slider(min=1, max=10, value=5).classes("w-64")

        feedback_label = ui.label("").classes("mt-2 text-pink-700 text-lg font-medium").style("font-family: 'Dancing Script', cursive;")
        submit_button_container = ui.row().classes("mt-4")

        # Container for conditional interaction (date question and input)
        date_container = ui.column().classes("items-center justify-center gap-4 mt-6")

        def ask_for_date():
            with date_container:
                ui.label("💬 Would you like to go on a date with me?").classes(
                    "text-2xl font-bold text-pink-800 animate-pulse"
                ).style("font-family: 'Dancing Script', cursive;")

                with ui.row().classes("gap-4"):
                    def yes_response():
                        date_container.clear()

                        with date_container:
                            ui.label("🥰 Yaaay! I'm so excited! Just a few more things...").classes("text-lg text-pink-700").style(
                                "font-family: 'Dancing Script', cursive;"
                            )

                            ui.label("Pick a date for our special day:").classes("mt-4")
                            date_picker = ui.date()

                            date_text_input = ui.input("Selected date").classes("w-64")
                            date_text_input.visible = False

                            def update_date_input():
                                # If a date is selected, update the input field
                                if date_picker.value:
                                    date_text_input.value = str(date_picker.value)
                                    date_text_input.visible = True
                                    date_picker.visible = False

                            # Add an event listener for the value change, using the `on_change` method of the date picker widget
                            date_picker.on_value_change(update_date_input)

                            ui.label("What type of date would you enjoy?").classes("mt-4")
                            date_type = ui.select(["Dinner", "Movie", "Long Walk", "Surprise Me!"], value="Surprise Me!")

                            def submit_final():
                                ui.notify(f"Can't wait! 🎉 Date: {date_text_input.value}, Type: {date_type.value}",
                                          type="positive", duration=6)

                            ui.button("Confirm 💖", on_click=submit_final).classes("mt-4 bg-pink-600 text-white px-4 py-2 rounded")

                    def no_response():
                        date_container.clear()
                        ui.label("That's okay! I'll be right here when you're ready. 💗").classes(
                            "text-lg text-pink-600"
                        ).style("font-family: 'Dancing Script', cursive;")

                    ui.button("Yes 💕", on_click=yes_response).classes("bg-green-500 text-white px-4 py-2 rounded")
                    ui.button("Not yet 🙈", on_click=no_response).classes("bg-gray-300 text-black px-4 py-2 rounded")

        def handle_rating_submit():
            if rating.value >= 6:
                feedback_label.text = "✨ Awww, I'm so glad! I have one last question for you..."
                ask_for_date()
            else:
                feedback_label.text = "😔 Oh no... I tried my best to impress you but thank you for being honest. You’re still amazing 💖"
                feedback_label.text = "You can exit the browser now !"
            submit_button_container.clear()  # Hides the submit button

        with submit_button_container:
            ui.button("Submit Rating 💌", on_click=handle_rating_submit).classes(
                "bg-pink-500 text-white px-4 py-2 rounded-full text-md shadow-md")

ui.run(title="Surprise for Anna", port=8082, reload=False)
