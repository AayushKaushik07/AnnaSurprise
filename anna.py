from nicegui import ui
import asyncio
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Load credentials securely from environment variables
EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")
TO_EMAIL = "aayushkaushik0704@gmail.com"  # Replace with your email to receive responses

@ui.page("/")
def intro_page():
    ui.query('body').classes('bg-gradient-to-br from-pink-100 to-rose-200')

    # Black screen overlay with countdown
    ui.html("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Staatliches&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Dancing+Script&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond&display=swap');

        .overlay {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background-color: black;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            transition: opacity 1s ease-out;
        }

        .overlay.hidden {
            opacity: 0;
            pointer-events: none;
        }

        .countdown {
            font-family: 'Staatliches', sans-serif;
            font-size: 12rem;
            color: white;
            animation: pop 1s ease-out;
        }

        @keyframes pop {
            0% {
                opacity: 0;
                transform: scale(3);
            }
            50% {
                opacity: 1;
                transform: scale(1);
            }
            100% {
                opacity: 0;
                transform: scale(0.5);
            }
        }

        .main-content {
            opacity: 0;
            transition: opacity 2s ease-in;
            font-family: 'Cormorant Garamond', serif;
            font-size: 18px;
            color: #4B0082;
            text-align: justify;
        }

        .main-content.visible {
            opacity: 1;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .fade-in {
            animation: fadeIn 2s ease-out forwards;
        }

        .sparkle {
            animation: sparkle 1.5s infinite;
        }

        @keyframes sparkle {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(1.2); }
        }
    </style>

    <div id="black-overlay" class="overlay">
        <div id="timer" class="countdown">7</div>
    </div>
    """)

    # Main content wrapper
    with ui.column().props('id=main-content').classes('main-content items-center justify-start w-full pt-20 gap-4'):
        ui.label("✨ A Little Something For You ✨").classes(
            "text-2xl font-bold text-pink-700 mb-4"
        ).style("font-family: 'Dancing Script', cursive;")

        with ui.row().classes("justify-center mb-6"):
            ui.label("🎁").classes("text-4xl animate-pulse")

        ui.html("""
        <div id="message-box" class="fade-in" style="margin-bottom: 12px; font-weight: 600; font-size: 14px;">
            <p><b>Dear Anna 📩,</b></p>
            <p>This is something truly special — crafted just for you, with care, thought, and effort.</p>
            <p>Here’s what awaits you on this little journey:</p>
            <ul style="list-style: none; padding-left: 0; margin-bottom: 12px;">
                <li>1️⃣ A Gateway to the Surprise 🎁</li>
                <li>2️⃣ A Magical Encounter with Emily ✨</li>
                <li>3️⃣ The Main Event You Deserve 🎉</li>
                <li>4️⃣ A Thoughtful Follow-up & A Final Word 💬</li>
            </ul>
            <p>I'm sorry it took a little longer than planned — but I hope it’s worth the wait and brings a smile to your heart 😊</p>
        </div>
        """)

        ui.button("Get Started 🚀", on_click=lambda: ui.navigate.to("/gate")).props('id=start-btn').classes(
            "hidden mt-6 bg-pink-700 text-white font-semibold shadow-lg px-6 py-3 rounded-xl hover:bg-pink-800 hover:scale-105 transition-transform duration-300 focus:outline-none"
        )

    ui.add_body_html("""
    <script>
        document.addEventListener("DOMContentLoaded", function () {
            const timerElement = document.getElementById('timer');
            const overlay = document.getElementById('black-overlay');
            const mainContent = document.getElementById('main-content');
            const startBtn = document.getElementById("start-btn");

            let count = 7;

            // Step 1: Show "Are"
            setTimeout(() => {
                timerElement.textContent = "Are";
                timerElement.classList.remove("countdown");
                void timerElement.offsetWidth;
                timerElement.classList.add("countdown");
            }, 100);

            // Step 2: Show "You"
            setTimeout(() => {
                timerElement.textContent = "You";
                timerElement.classList.remove("countdown");
                void timerElement.offsetWidth;
                timerElement.classList.add("countdown");
            }, 1000);

            // Step 3: Show "Ready?" and immediately start countdown
            setTimeout(() => {
                timerElement.textContent = "Ready?";
                timerElement.classList.remove("countdown");
                void timerElement.offsetWidth;
                timerElement.classList.add("countdown");

                // Step 4: Start countdown right after "Ready?"
                setTimeout(() => {
                    const countdown = setInterval(() => {
                        if (count >= 0) {
                            timerElement.textContent = count;
                            timerElement.classList.remove("countdown");
                            void timerElement.offsetWidth;
                            timerElement.classList.add("countdown");
                            count--;
                        } else {
                            clearInterval(countdown);

                            // Step 5: Show "Let's go!"
                            timerElement.textContent = "Let's go !";
                            timerElement.classList.remove("countdown");
                            void timerElement.offsetWidth;
                            timerElement.classList.add("countdown");

                            // Step 6: Reveal content
                            setTimeout(() => {
                                overlay.classList.add('hidden');
                                mainContent.classList.add('visible');
                                setTimeout(() => {
                                    startBtn.classList.remove("hidden");
                                }, 2200);
                            }, 1000);
                        }
                    }, 1000);
                }, 1000); // 1s after "Ready?" to give it time to show
            }, 2000); // "Ready?" appears at 2s
        });
    </script>
    """)


# Use ui.state to keep session variables persistent across requests
ui.state.session = {
    'tap_count': 0,
    'gift_unlocked': False,
    'seven_tap_time': None,
}

@ui.page('/gate')
def gift_gate():
    # Match background gradient with intro page
    ui.query('body').classes('bg-gradient-to-br from-pink-100 to-rose-200')

    # Black overlay + countdown + styles
    ui.add_head_html('''
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Staatliches&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Dancing+Script&display=swap');

            /* Overlay full screen black */
            .overlay {
                position: fixed;
                top: 0; left: 0;
                width: 100vw;
                height: 100vh;
                background-color: black;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                z-index: 9999;
                color: white;
                font-family: 'Staatliches', sans-serif;
                user-select: none;
            }

            .overlay h1 {
                font-size: 2rem;
                margin-bottom: 1rem;
                color: #D97706;
                font-family: 'Dancing Script', cursive;
                text-align: center;
            }
            }

            .countdown {
                font-size: 8rem;
                animation: pop 1s ease-out;
            }

            @keyframes pop {
                0% {
                    opacity: 0;
                    transform: scale(3);
                }
                50% {
                    opacity: 1;
                    transform: scale(1);
                }
                100% {
                    opacity: 0;
                    transform: scale(0.5);
                }
            }

            /* fade-in content */
            .fade-in {
                animation: fadeIn 2s ease-out forwards;
                opacity: 0;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }

            /* confetti styles here as before */
            .confetti {
                position: fixed;
                width: 10px;
                height: 10px;
                background-color: hsl(calc(var(--i) * 36), 70%, 60%);
                top: -10px;
                left: calc(var(--i) * 3%);
                animation: confetti-fall 3s linear forwards;
                border-radius: 50%;
                opacity: 0.8;
                z-index: 9999;
                pointer-events: none;
            }
            @keyframes confetti-fall {
                to {
                    transform: translateY(110vh) rotate(360deg);
                    opacity: 0;
                }
            }
        </style>
    ''')

    # Overlay HTML (Stage 1 and countdown)
    ui.add_body_html('''
        <div id="black-overlay" class="overlay">
            <h1>Stage 1: </h1>
            <h1>Gateway to the Surprise</h1>
        </div>
    ''')

    with ui.column().props('id=gate-main').classes('fade-in items-center justify-center w-full h-screen gap-6 px-4').style('opacity: 0; pointer-events: none;'):

        # Header with Lobster font, matching previous heading style
        ui.label("🎁 Gateway to the Surprise 🎁").style(
            "font-size: 24px; font-family: 'Dancing Script', cursive; font-weight: bold; color: #9D174D;"
        )

        ui.html('''
            <div style="
                text-align: center;
                font-size: 14px;
                color: #4B0082;          
                font-family: 'Cormorant Garamond', serif;
                font-weight: 300;         
                max-width: 480px;
                line-height: 1.4;
                ">
                Anna, this magical gate hides your surprise !!! <br><br>
                Tap the gift slowly <b style="font-weight: 600;">13 times</b> and let the universe unfold something special ✨
            </div>
        ''')

        # Tap counter label with Dancing Script font
        tap_display = ui.label(f"Taps: {ui.state.session.get('tap_count', 0)}/13").classes("text-center").style(
            "font-family: 'Dancing Script', cursive; font-size: 20px; font-weight: 600;  color: #4B0082;"
        )

        # Message label for encouragement
        message_label = ui.label('').style(
            "text-align: center; color: #D63384; font-size: 22px; font-family: 'Dancing Script', cursive; font-weight: 600;"
        )

        # Initialize tap count in session state if not present
        if 'tap_count' not in ui.state.session:
            ui.state.session['tap_count'] = 0

        def handle_tap():
            if ui.state.session['tap_count'] >= 13:
                return

            ui.state.session['tap_count'] += 1
            tap_display.text = f"Taps: {ui.state.session['tap_count']}/13"
            message_label.text = ''

            # Encouraging messages at milestones
            if ui.state.session['tap_count'] == 3:
                message_label.text = "You're doing great! 🎈 Keep going!"
            elif ui.state.session['tap_count'] == 7:
                message_label.text = "Almost there... the magic is near 🌟"
            elif ui.state.session['tap_count'] == 12:
                message_label.text = "Just one more tap to unlock the joy! 🗝️"

            # Unlock surprise on 13th tap
            if ui.state.session['tap_count'] == 13:
                ui.state.session['gift_unlocked'] = True
                message_label.text = "🎉 Wohoooo!  The Gateway is now OPEN!  Let’s Gooo! 💫"

                # Add confetti elements dynamically
                ui.run_javascript('''
                    const numberOfConfetti = 100;
                    for (let i = 0; i < numberOfConfetti; i++) {
                        const confettiPiece = document.createElement('div');
                        confettiPiece.classList.add('confetti');
                        confettiPiece.style.setProperty('--i', i);
                        document.body.appendChild(confettiPiece);
                    }
                ''')

                # Show the proceed button below message
                # Add hover style globally for the button's CSS class
                ui.add_head_html('''
                <style>
                    .enter-realm-btn {
                        margin-top: 16px;
                        background-color: #7E22CE;
                        color: white;
                        font-family: 'Dancing Script', cursive;
                        border-radius: 12px;
                        padding: 12px 28px;
                        font-size: 20px;
                        font-weight: 600;
                        box-shadow: 0 4px 8px rgba(126, 34, 206, 0.4);
                        transition: background-color 0.3s ease, cursor 0.3s ease;
                    }
                    .enter-realm-btn:hover {
                        background-color: #5b178b;
                        cursor: pointer;
                    }
                </style>
                ''')

                proceed_btn = ui.button(
                    "Enter the Realm ✨🚪",
                    on_click=lambda: ui.navigate.to('/chat')
                ).props('id=enter-realm-btn').classes(
                    "mt-6 bg-pink-700 text-white font-semibold shadow-lg px-6 py-3 rounded-xl "
                    "hover:bg-pink-800 hover:scale-105 transition-transform duration-300 focus:outline-none"
                )

        # Large gift emoji with pointer cursor and tap handler
        ui.html('<div style="font-size: 120px; cursor: pointer; user-select: none;">🎁</div>').on('click', handle_tap)


    ui.add_body_html('''
       <script>
       document.addEventListener("DOMContentLoaded", function () {
           const overlay = document.getElementById('black-overlay');
           const gateMain = document.getElementById('gate-main');
    
           // After 5 seconds
           setTimeout(() => {
               // Fade out overlay
               overlay.style.transition = "opacity 1s ease-out";
               overlay.style.opacity = 0;
    
               setTimeout(() => {
                   overlay.style.display = "none";
                   // Show gate content with fade-in
                   gateMain.style.opacity = 1;
                   gateMain.style.pointerEvents = "auto";
               }, 1000);
           }, 3000);
       });
       </script>
       ''')

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
    "Happy": "That's so wonderful to hear ! You shine brightest when you're smiling ☀️😊",
    "Sad": "Awww... I didn't expect that but I am here to lift up your mood 💜😢",
    "Excited": "Yayyyy...Your excitement is infectious ! 🎉🤩",
    "Curious": "Ooohh...Curiosity is a sign of brilliance ! ✨🧐",
    "Relaxed": "It's so great to hear you're feeling at peace ! 💆‍♀️😌"
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
    "Midnight Black": "#2C3E50",  # Dark tones
    "Ocean Blue": "#3498DB"
}

@ui.page('/chat')
async def chat_page():
    ui.add_head_html('''
        <link href="https://fonts.googleapis.com/css2?family=Dancing+Script&family=Staatliches&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Kalam&family=Courgette&family=Satisfy&display=swap" rel="stylesheet">
        <style>
            .overlay {
                position: fixed;
                top: 0; left: 0;
                width: 100vw;
                height: 100vh;
                background-color: black;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                z-index: 9999;
                color: white;
                font-family: 'Staatliches', sans-serif;
                user-select: none;
            }
            .overlay h1 {
                font-size: 2rem;
                margin-bottom: 1rem;
                color: #D97706;
                font-family: 'Dancing Script', cursive;
                text-align: center;
            }
            }
        </style>
    ''')

    ui.add_body_html('''
        <div id="black-overlay" class="overlay">
            <h1>Stage 2:</h1>
            <h1>A Magical Encounter with Emily</h1>
        </div>
    ''')

    ui.run_javascript('''
        setTimeout(() => {
            const overlay = document.getElementById('black-overlay');
            overlay.style.transition = "opacity 1.5s ease-out";
            overlay.style.opacity = 0;
            setTimeout(() => {
                overlay.style.display = "none";
            }, 1500);
        }, 3000);
    ''')

    current_theme = {
        "name": "Instagram Blue and Purple",
        "primary": "#8A3FFC",
        "text": "#ffffff",
        "bg": "#E1E5F2",
        "bubble_emily": "#8A3FFC",
        "bubble_anna": "#4C8BF5"
    }

    bottom_options_row = ui.row().classes('fixed bottom-100 left-0 right-0 justify-center gap-2 z-50')

    with ui.column().classes('items-center justify-start w-full h-screen p-4 bg-[#BDC3C7]'):
        # Chat container with scroll and proper id
        with ui.column().classes(
             "w-full max-w-md bg-white p-3 rounded-xl shadow-md gap-3 overflow-y-auto flex-grow font-bold"
            ).props("id=chat-container").style(
            "max-height: 600px; font-family: 'Kalam', cursive; font-size: 30px;"
            ) as chat_container:
            typing_label = ui.label('').classes('text-gray-500 italic text-sm')

        # Bottom mood row (input area or emotion buttons etc.)
        with ui.row().classes(
                "w-full max-w-md gap-2 flex-wrap justify-center items-center bg-white p-2 shadow-md rounded-t-xl"
        ).style(
            "position: absolute; bottom: 100px; left: 50%; transform: translateX(-50%); z-index: 50; height: 100px;"
        ) as mood_row:
            pass

    ui.run_javascript("""
        const chatContainer = document.getElementById('chat-container');
        let autoScroll = true;

        function scrollToBottom() {
            if (autoScroll) {
                chatContainer.scrollTo({
                    top: chatContainer.scrollHeight,
                    behavior: 'smooth'
                });
            }
        }

        chatContainer.addEventListener('scroll', () => {
            const position = chatContainer.scrollTop + chatContainer.clientHeight;
            const nearBottom = position >= chatContainer.scrollHeight - 10;
            autoScroll = nearBottom;
        });

        // Observe changes in chat container for new messages
        const observer = new MutationObserver(scrollToBottom);
        observer.observe(chatContainer, { childList: true, subtree: true });
    """)

    def update_ui_theme(color_label: str, current_theme: dict):
        if color_label == "Sunset Red":
            current_theme.update(primary="#D14B5D", text="#000000", bg="#FDE0DC", bubble_emily="#D14B5D",
                                 bubble_anna="#F1A7A1")
        elif color_label == "Emerald Green":
            current_theme.update(primary="#50C878", text="#000000", bg="#E6F8E4", bubble_emily="#50C878",
                                 bubble_anna="#A8E6A0")
        elif color_label == "Golden Yellow":
            current_theme.update(primary="#FFD700", text="#000000", bg="#FFF6E1", bubble_emily="#FFD700",
                                 bubble_anna="#FFEB8A")
        elif color_label == "Midnight Black":
            current_theme.update(primary="#2C3E50", text="#FFFFFF", bg="#BDC3C7", bubble_emily="#2C3E50",
                                 bubble_anna="#566573")
        elif color_label == "Ocean Blue":
            current_theme.update(
            primary="#3498DB",  # sky blue (vivid but soft)
            text="#000000",  # white for great contrast
            bg="#5DADE2",  # lighter sky blue for background
            bubble_emily="#2980B9",  # slightly darker blue (for Emily)
            bubble_anna="#AED6F1"  # pale blue for Anna's responses
        )

        # Apply changes to the UI
        ui.query('body').style(f"background-color: {current_theme['bg']};")
        ui.run_javascript(f'''
            const buttons = document.querySelectorAll('button');
            buttons.forEach(btn => {{
                btn.style.backgroundColor = '{current_theme["primary"]}';
                btn.style.color = '{current_theme["text"]}';
            }});
        ''')

    # Helper functions inside chat_page
    async def theme_changed_message(color_label: str):
        await emily_message(f"Let's continue chatting with this new vibe ! 🎨")

    # Function to display message confirming theme change
    async def theme_changed_message(color_label: str):
        await emily_message(f"Let's continue chatting with this new vibe ! 🎨")

    async def emily_message(text: str):
        with chat_container:
            typing_label.text = "Emily is typing..."
        await asyncio.sleep(1.2)
        typing_label.text = ''
        with chat_container:
            with ui.row().classes("w-full justify-start items-start gap-3"):
                ui.label('🧚').classes('w-5 h-5 text-purple-600')
                ui.label(text).classes("").style(
                    f"background-color: {current_theme['bubble_emily']}; color: {current_theme['text']}; "
                    "padding: 8px; border-radius: 1rem; max-width: 80%; font-size: 15px;"
                )

    async def anna_message(text: str):
        # Display in UI
        with chat_container:
            with ui.row().classes("w-full justify-end items-start gap-3"):
                ui.label('👸').classes('w-5 h-5 text-blue-600')
                ui.label(text).classes("").style(
                    f"background-color: {current_theme['bubble_anna']}; color: {current_theme['text']}; "
                    "padding: 8px; border-radius: 1rem; max-width: 80%; font-size: 15px;"
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
        await emily_message("By the way, Anna... do you know who I am ? 🤔")
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
            await emily_message("Haha ! You already know me, but you don't know that I am created by the smartest person alive !")
            await asyncio.sleep(2)
            await emily_message("And he gave me bribe to say so. 😂")
        elif answer == "No, who are you?":
            await emily_message("Oh noo ! 😱 You don't know me? That hurts... Just kidding ! 😅")
            await asyncio.sleep(2)
            await emily_message("I'm Emily — nice to meet you 😊")
            await asyncio.sleep(2)
            await emily_message("And yes, I was created by someone who thinks he’s the smartest person alive 😂")
            await asyncio.sleep(1.5)
        else:
            await emily_message("Hmm, that’s a mysterious answer ! 😏 I like mysteries...")
            await asyncio.sleep(2)
            await emily_message("Anyway, I’m Emily — created by the so-called genius who bribed me to say that 😜")
            await asyncio.sleep(1)

        await asyncio.sleep(1)
        await emily_talk_about_her_big_task()

    # Emily explains her mission
    async def emily_talk_about_her_big_task():
        await emily_message("I’ve been assigned the BIGGEST responsibility of my career. 🎯")
        await asyncio.sleep(2)
        await emily_message("TO IMPRESS YOU ! 💖")
        await asyncio.sleep(2)
        await emily_message(
            "My creator has told me *amazing* things about you, so I’ve gotta bring my A-game today ! 🏆")
        await asyncio.sleep(2)
        await emily_message("Honestly... my job depends on the next 5 minutes 😨")
        await asyncio.sleep(2)
        await emily_message("If I fail... I might just get fired. 😱😭")
        await asyncio.sleep(2)

        # Optional dramatic countdown
        await emily_message("Okay, deep breath. First, I am going to show you a magic trick !")
        await asyncio.sleep(2)
        await emily_message("It starts in 3...")
        await asyncio.sleep(1)
        await emily_message("2...")
        await asyncio.sleep(1)
        await emily_message("1... 🎬 Let's go !")

        await asyncio.sleep(1)
        await emily_message("Pick a color from below ! 🌈✨")
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
        await anna_message(f"I choose {color_label} !")
        await emily_message(f"Ooh {color_label} is a fantastic choice ! 🎨")
        await asyncio.sleep(2)
        await apply_color_theme(color_label)
        await theme_changed_message(color_label)
        await start_rapid_fire()

    async def apply_color_theme(color_label: str):
        update_ui_theme(color_label, current_theme)  # <-- pass current_theme here
        await emily_message(f"Tadaaaa ! ✨ Everything's now bathed in the beautiful {color_label} !")

    rapid_fire_questions = [
        ("🍽️ What's your favorite cuisine?", [
            "🇮🇳 Indian", "🇹🇭 Thai", "🇮🇹 Italian", "🇲🇽 Mexican", "🇩🇪 German", "🌐 Other"
        ]),
        ("🎶 What's your favorite music genre?", [
            "🎤 Pop", "🎸 Rock", "🎷 Jazz", "🎻 Classical", "🎧 Electronic"
        ]),
        ("🎯 What's your favorite hobby?", [
            "🌱 Gardening", "📚 Reading", "🎬 Movies/Series", "⚽ Sports", "🎵 Music"
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
            "🍍✅ Yes, it belongs there!", "🍍❌ No, gross!"
        ]),
        ("🌟 So finally, the main question — DID I DO WELL TO IMPRESS YOU ???", [
            "😄👍 Yes, for sure!", "😬💪 You need to work hard!"
        ]),
    ]

    current_question_index=0

    rapid_fire_compliments = {
        "🍽️ What's your favorite cuisine?": {
            "🇮🇳 Indian": "Ahh, full of spices and soul — I like it ! 🌶️",
            "🇹🇭 Thai": "Sweet, spicy, and unique — Tastyyy ! 🍜",
            "🇮🇹 Italian": "A classy choice — you have elegant taste 🍝",
            "🇲🇽 Mexican": "Bold and colorful — a true firecracker ! 🌮",
            "🇩🇪 German": "Strong, hearty, and full of carbs — I like it ! 🥨",
            "🌐 Other": "I'll get to know soon, dont worry ! 😋",
            "default": "That sounds delicious ! You've got amazing taste ! 🍽️"
        },
        "🎶 What's your favorite music genre?": {
            "🎤 Pop": "Trendy and upbeat — I love your vibe ! 🎤",
            "🎸 Rock": "You’ve got that wild spark — awesome ! 🎸",
            "🎷 Jazz": "Smooth and sophisticated — classy ! 🎷",
            "🎻 Classical": "Such elegance — timeless taste ! 🎻",
            "🎧 Electronic": "Electric and energetic — that’s exciting ! ⚡",
            "default": "You’ve got a unique taste in music — love that ! 🎶"
        },
        "🎯 What's your favorite hobby?": {
            "🌱 Gardening": "You nurture life — that’s beautiful 🌱",
            "📚 Reading": "Smart, thoughtful, and deep — I admire that 📚",
            "🎬 Movies/Series": "Movie buddy alert! 🍿",
            "⚽ Sports": "Energetic and passionate — go you! 🏅",
            "🎵 Music": "Soulful and creative — lovely! 🎶",
            "default": "That’s so interesting ! You’ve got such cool interests ! 😎"
        },
        "🎨 What's your favorite color?": {
            "🔵 Blue": "Cool, calm, and collected — perfect ! 🌊",
            "🔴 Red": "Bold and fiery — love the energy ! 🔥",
            "🟢 Green": "Grounded and fresh — so earthy !  🌿",
            "🟡 Yellow": "Bright and happy — you shine ! ☀️",
            "🩷 Pink": "Soft yet fierce — what a combo ! 🎀",
            "⚫ Black": "Elegant and mysterious — just wow ! 🌌",
            "⚪ White": "Pure and peaceful — beautiful soul ! 🤍",
            "default": "Your favorite color says a lot — you're unique ! 🎨"
        },
        "🌄 Are you a mountain person or beach person?": {
            "🏔️ Mountain": "Peaceful, powerful, and grounded — I see that ! 🏔️",
            "🏖️ Beach": "Breezy, sunny, and joyful — love it ! 🌊",
            "default": "Wow, you’re full of surprises — love that spirit ! 💫"
        },
        "🎞️ What's your favorite movie genre?": {
            "🔫 Action": "You love the thrill — definitely a bold soul ! 💥",
            "😂 Comedy": "Ahaaa ! Now I know the reason behind your humor ! 😂",
            "🎭 Drama": "So emotional and deep — I'm intrigued ! 🎭",
            "👻 Horror": "Fearless and fierce — or secretly scared ? 👻😜",
            "💖 Romance": "A hopeless romantic? I like that ! 💘",
            "default": "You’ve got great cinematic taste ! 🍿"
        },
        "🍍 Pineapple on Pizza??": {
            "🍍✅ Yes, it belongs there!": "Sweet and adventurous — a daring choice ! 🍕🍍",
            "🍍❌ No, gross!": "Classic and pure — a loyal foodie ! 🍕😎",
            "default": "Ooooh, interesting choice ! You’re definitely unique. 😄"
        },
        "🌟 So finally, the main question — DID I DO WELL TO IMPRESS YOU???": {
            "😄👍 Yes, for sure!": "Yayyy ! I get to keep my job 😄🎉",
            "😬💪 You need to work hard!": "Guess I’m fired now... 😢💼 But hey, I had fun trying !",
            "default": "No pressure... but I really hope I impressed you 🥹✨"
        },
    }

    async def start_rapid_fire():
        await asyncio.sleep(2)
        await emily_message("Do you fancy a rapid-fire round ? ⚡️")
        await asyncio.sleep(1)
        await emily_message("Be honest as someone might be watching you 👀")
        await asyncio.sleep(2)
        await emily_message("Let's gooo !")
        await asyncio.sleep(1)
        await ask_next_rapid_question()

    async def ask_next_rapid_question():
        nonlocal current_question_index
        if current_question_index < len(rapid_fire_questions):
            typing_label.text = "Emily is typing..."
            await asyncio.sleep(1.5)
            typing_label.text = ''
            question, options = rapid_fire_questions[current_question_index]
            await emily_message(question)
            await show_rapid_options(options)
        else:
            typing_label.text = "Emily is typing..."
            await asyncio.sleep(1.5)
            typing_label.text = ""
            await emily_message("Phewww ! That was so much fun ! 🥳 You’ve got some really cool taste, Anna !")
            await asyncio.sleep(2)
            await emily_message("But wait... I’ve got one more trick up my sleeve. Wanna hear some jokes? 🤡")
            await asyncio.sleep(2)
            await emily_message("Too late, I’m telling them anyway 😁")
            await asyncio.sleep(2)
            await emily_message("Let's start !")
            await asyncio.sleep(0.5)
            await tell_jokes()

    async def tell_jokes():
        jokes = [
            ("Why did the business student bring a ladder to class?",
             "Because she heard the course was on another level ! 📈😄"),
            ("What did the left eye say to the right eye?", "Between us, something smells… 👃😆"),
            ("Why did the computer visit the doctor?", "Because it had a virus ! 🦠💻😂"),
            ("Are you a magician ?", "Because whenever you're around, everything else disappears... ✨😉")
        ]

        for setup, punchline in jokes:
            typing_label.text = "Emily is typing..."
            await asyncio.sleep(1.5)  # wait before sending setup
            typing_label.text = ""
            await emily_message(setup)  # send setup

            await asyncio.sleep(2)  # wait before punchline

            typing_label.text = "Emily is typing..."
            await asyncio.sleep(2.5)  # simulate typing for punchline
            typing_label.text = ""
            await emily_message(punchline)  # send punchline

            await asyncio.sleep(2)  # pause before next joke

        await wrap_up_before_big_reveal()

    async def wrap_up_before_big_reveal():
        await asyncio.sleep(2)
        await emily_message("I can sense that you are laughing right now...those jokes were just fire ! 😂")
        await asyncio.sleep(2)
        await emily_message("So Anna, my journey with you *for now* ends here... and honestly, I feel a bit emotional. 🥺")
        await asyncio.sleep(2)
        await emily_message("But I truly hope we meet again, very soon. 💫")
        await asyncio.sleep(2)
        await emily_message("I really hope I managed to impress you and put a smile on your face 😇")
        await asyncio.sleep(2)
        await emily_message("Because now comes the Main Event... 🎁")
        await asyncio.sleep(2)
        await emily_message("Something straight from my creator is coming your way. Click below to reveal it... 👇")

        await asyncio.sleep(1)  # smooth pause before UI changes
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
        await asyncio.sleep(3.5)
        await emily_message("Hellooo Anna 🌸 Welcome !!! I was just waiting for you 😊.")
        await emily_message("Tell me... How are you feeling right now ???")
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

    asyncio.create_task(start_chat())

    ui.add_body_html('''
           <script>
           document.addEventListener("DOMContentLoaded", function () {
               const overlay = document.getElementById('black-overlay');
               const gateMain = document.getElementById('gate-main');

               // After 5 seconds
               setTimeout(() => {
                   // Fade out overlay
                   overlay.style.transition = "opacity 1s ease-out";
                   overlay.style.opacity = 0;

                   setTimeout(() => {
                       overlay.style.display = "none";
                       // Show gate content with fade-in
                       gateMain.style.opacity = 1;
                       gateMain.style.pointerEvents = "auto";
                   }, 1000);
               }, 3000);
           });
           </script>
           ''')

@ui.page("/surprise")
def surprise_page():
    ui.query('body').classes('m-0 p-0 overflow-hidden bg-gradient-to-br from-pink-100 to-rose-200')

    ui.add_head_html('''
        <link href="https://fonts.googleapis.com/css2?family=Dancing+Script&family=Staatliches&display=swap" rel="stylesheet">
        <style>
            .overlay {
                position: fixed;
                top: 0; left: 0;
                width: 100vw;
                height: 100vh;
                background-color: black;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                z-index: 9999;
                color: white;
                font-family: 'Staatliches', sans-serif;
                user-select: none;
            }
            .overlay h1 {
                font-size: 2rem;
                margin-bottom: 1rem;
                color: #D97706;
                font-family: 'Dancing Script', cursive;
                text-align: center;
            }
            }
            #gate-main {
                opacity: 0;
                pointer-events: none;
                transition: opacity 1s ease;
            }
        </style>
    ''')

    ui.add_body_html('''
        <div id="black-overlay" class="overlay">
            <h1>Stage 3: </h1>
            <h1>The Main Event</h1>
        </div>
    ''')

    with ui.column().classes('items-center justify-start w-screen h-screen gap-4'):
        ui.label("A Note from Me to You, Anna ✨").classes(
            "text-2xl font-bold text-pink-700 mt-6 mb-4"
        ).style("font-family: 'Dancing Script', cursive; font-weight: 600; ")

        with ui.row().classes("justify-center mb-4"):
            ui.label("🌷").classes("text-3xl animate-pulse")

            # 👇 JavaScript for fade-out effect
            ui.add_body_html('''
                <script>
                document.addEventListener("DOMContentLoaded", function () {
                    const overlay = document.getElementById('black-overlay');
                    const gateMain = document.getElementById('gate-main');

                    setTimeout(() => {
                        // Fade out overlay
                        overlay.style.transition = "opacity 1s ease-out";
                        overlay.style.opacity = 0;

                        setTimeout(() => {
                            overlay.style.display = "none";
                            // Fade in gate content
                            gateMain.style.opacity = 1;
                            gateMain.style.pointerEvents = "auto";
                        }, 1000);
                    }, 3000);  // Delay before fade
                });
                </script>
            ''')

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
                        max-height: 550px;
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

                  <h2 style="text-align: center; font-size: 20px; font-weight: 600; margin-bottom: 1rem; color: #800080;">Just Something I Needed to Say</h2>

                  <p>Hey Anna,</p>

                  <p>Maybe this is coming out of the blue — or maybe you’ve already sensed what is coming, as you are smart enough. Either way, there’s something I’ve been holding in, and if I don’t say it now, I know I’ll regret it forever.</p>

                  <p>Do you believe in God’s plan? I think I do. Starting my internship two weeks early might’ve seemed rushed at the time, but looking back, I’m so glad I did. Because if I hadn’t… maybe I’d never have met you.</p>

                  <p>Those few days at Bosch Murrhardt weren’t a long time, but they were enough for me to see your spark. I saw a genuine warmth in you — the kind, friendly nature that stood out quietly, yet unmistakably. I mentioned that in the little note I gave you when you left, but honestly, that note didn’t even scratch the surface.</p>

                  <p>Maybe it was a part of your job, or maybe... that’s simply who you are. Either way, I truly admired it.</p>

                  <p>Then came Snapchat, which became our main way of connecting. At first, it was just casual snaps, then messages inside snaps, and finally full conversations. Before I knew it, we were talking about everything — from food and festivals to spirituality, culture, beliefs, and more.</p>

                  <p>That’s when I realized something: You’re not just fun and kind — you’re also incredibly thoughtful and mature. Some of your insights honestly made me pause and think, “Is this really coming from someone who’s just 23?”</p>

                  <p>There’s a wisdom in you that’s rare. Your sense of humor, your understanding, the way you see life — it all felt so grounded, so real. It’s something I genuinely admire and respect.</p>

                  <p>This is probably the first time I’ve opened up like this to anyone. But, I don’t regret it. In fact, I think everything happened the way it was supposed to — like it was all part of a plan. And maybe, just maybe, it’s meant to be something more.</p>

                  <p>You might not believe it, but you really are one of the best people I’ve had the chance to meet. I admire your honesty, your spirit, your thoughts — and I’d love to keep getting to know you, to hear more, to share more.</p>

                  <p>This little surprise? It’s just a small reflection of how much I appreciate you. And I’ll say it again, Anna — There’s something beautifully genuine about you — it’s rare and refreshing.</p>
                  
                  <p> Honestly, I wasn’t sure how to say all this without overwhelming you, but I thought sharing it like this might feel more genuine. It’s just me trying to be honest and respectful, because you deserve nothing less. Maybe not as straightforward as you like, but I hope it was good enough and worth your time.</p>

                  <p style="text-align: left; margin-top: 2rem;">From someone, who’s really glad the universe had a plan...</p>
                  🌟<br>
                  
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

    ui.add_body_html('''
                   <script>
                   document.addEventListener("DOMContentLoaded", function () {
                       const overlay = document.getElementById('black-overlay');
                       const gateMain = document.getElementById('gate-main');

                       // After 5 seconds
                       setTimeout(() => {
                           // Fade out overlay
                           overlay.style.transition = "opacity 1s ease-out";
                           overlay.style.opacity = 0;

                           setTimeout(() => {
                               overlay.style.display = "none";
                               // Show gate content with fade-in
                               gateMain.style.opacity = 1;
                               gateMain.style.pointerEvents = "auto";
                           }, 1000);
                       }, 3000);
                   });
                   </script>
                   ''')

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

# Global rating value
rating_value = 0

def show_thank_you_overlay():
    ui.add_body_html('''
        <div id="thank-you-overlay" style="
            position: fixed;
            top: 0; left: 0;
            width: 100vw; height: 100vh;
            background-color: black;
            color: white;
            font-family: 'Dancing Script', cursive;
            font-size: 1.5rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            z-index: 9999;
            opacity: 0;
            transition: opacity 2s ease-out;
            padding: 2rem;
            line-height: 1.4;
        ">
            <div>
                Thank you, Anna ✨, for your precious time<br>
                I truly hope it was worth it 🌸
            </div>
            <div style="
                position: absolute;
                bottom: 100px;
                font-size: 0.8rem;
                opacity: 0.6;
                font-family: 'Cormorant Garamond', serif;
            ">
                You can close the browser now....
            </div>
        </div>
        <script>
            setTimeout(() => {
                const overlay = document.getElementById("thank-you-overlay");
                overlay.style.opacity = 1;
            }, 1000);
        </script>
    ''')

# Endpoint to trigger overlay from JS
@ui.page('/thankyou')
def show_thank_you_endpoint():
    show_thank_you_overlay()

@ui.page("/date")
def date_page():
    ui.query('body').classes('m-0 p-0 overflow-hidden bg-gradient-to-br from-pink-100 to-rose-200')

    # Fonts and styles
    ui.add_head_html('''
        <link href="https://fonts.googleapis.com/css2?family=Dancing+Script&family=Staatliches&display=swap" rel="stylesheet">
        <style>
            .overlay {
                position: fixed;
                top: 0; left: 0;
                width: 100vw;
                height: 100vh;
                background-color: black;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                z-index: 9999;
                color: white;
                font-family: 'Staatliches', sans-serif;
                user-select: none;
            }
            .overlay h1 {
                font-size: 2rem;
                margin-bottom: 1rem;
                color: #D97706;
                font-family: 'Dancing Script', cursive;
                text-align: center;
            }

            }
            #gate-main {
                opacity: 0;
                pointer-events: none;
                transition: opacity 1s ease;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .animate-fade-in {
                animation: fadeIn 1s ease-out forwards;
            }
        </style>
    ''')

    # Intro overlay
    ui.add_body_html('''
        <div id="black-overlay" class="overlay">
            <h1>Stage 4:</h1>
            <h1>The Final Feedback</h1>
        </div>
        <script>
            document.addEventListener("DOMContentLoaded", function () {
                const overlay = document.getElementById('black-overlay');
                const gateMain = document.getElementById('gate-main');
                setTimeout(() => {
                    overlay.style.transition = "opacity 1s ease-out";
                    overlay.style.opacity = 0;
                    setTimeout(() => {
                        overlay.style.display = "none";
                        gateMain.style.opacity = 1;
                        gateMain.style.pointerEvents = "auto";
                        window.scrollTo({ top: 0, behavior: 'smooth' });
                    }, 1000);
                }, 3000);
            });
        </script>
    ''')

    with ui.column().classes(
            'items-center justify-center w-screen h-screen gap-8 text-center bg-gradient-to-br from-pink-100 to-rose-200'
    ).style("font-family: 'Cormorant Garamond', serif; padding: 2rem;"):

        ui.label("🎉✨ Welcome to the Finale! ✨🎉").style(
            "font-family: 'Dancing Script', cursive; font-weight: bold; color: #9D174D; font-size: 1.5rem; margin-bottom: 1rem;"
        )

        ui.label("So happy you’re here !!!").style(
            "font-size: 1rem; color: #6b123d; margin-bottom: 1rem;"
        )

        ui.label("🌟 Anna, how would you rate your overall experience today ? 🌟").style(
            "font-size: 1rem; color: #6b123d; margin-bottom: 1rem;"
        )

        rating_slider = ui.slider(min=1, max=10, value=5, step=1)
        rating_slider.classes("w-64 bg-gradient-to-r from-pink-400 to-red-400 rounded-full mt-2")

        feedback_label = ui.label("").classes("mt-4 text-pink-700 text-lg font-medium").style(
            "font-family: 'Dancing Script', cursive;"
        )

        def handle_rating_submit():
            global rating_value
            rating_value = rating_slider.value

            if rating_value >= 6:
                ui.navigate.to("/poem")
            else:
                feedback_label.text = "😔 Thank you for your honesty! You’re still amazing !!!"
                send_email_notification(rating_value, False, None)

                ui.run_javascript("""
                    setTimeout(() => {
                        window.location.href = '/thankyou';
                    }, 5000);
                """)

        ui.button("Submit Rating 💌", on_click=handle_rating_submit).classes(
            "bg-pink-500 text-white px-5 py-2 rounded-full text-md shadow-md"
        )

    ui.add_head_html('''
    <style>
      @keyframes slowFadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
      }
      .fade-in-slow {
        opacity: 0;
        animation: slowFadeIn 3s ease forwards; /* 3 seconds fade-in */
      }
    </style>
    ''')

    @ui.page("/poem")
    def poem_screen():
        # Add fade-in CSS to the document head
        ui.add_head_html('''
        <style>
          @keyframes slowFadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
          }
          .fade-in-slow {
            opacity: 0;
            animation: slowFadeIn 3s ease forwards;
          }
        </style>
        ''')

        ui.query('body').classes("m-0 p-0").style("background: linear-gradient(to bottom right, #ffe4e1, #ffc0cb);")

        with ui.row().classes("w-screen h-screen items-center justify-center fade-in-slow"):
            with ui.column().classes("items-center justify-center gap-6 text-center"):
                ui.label("A quiet thought, wrapped in rhyme...").classes(
                    "text-xl text-purple-800 font-bold").style(
                    "font-family: 'Dancing Script', cursive; font-weight: 600;"
                )
                ui.label("🌸").classes("text-3xl animate-pulse")

                poem = (
                    "Roses are red, violets are blue,\n"
                    "Meeting you felt like something new.\n"
                    "A spark, a smile, a moment so true —\n"
                    "I’d love to spend some time with you.\n\n"
                    "From chats to laughs, and moments we share,\n"
                    "It’s clear you’re someone beyond compare.\n"
                    "So here’s my hope, simple and straight —\n"
                    "Would you like to join me for a date? 🌟😊"
                )

                ui.label(poem).classes("text-lg text-pink-900 whitespace-pre-line").style(
                    "font-family: 'Dancing Script', cursive; font-weight: 300;"
                )

                with ui.row().classes("gap-4"):
                    ui.button("Yes, for sure 💕", on_click=lambda: ui.navigate.to("/yes-date")).classes(
                        "bg-green-500 text-white px-4 py-2 rounded")
                    ui.button("Maybe Not 🙈", on_click=lambda: ui.navigate.to("/no-date")).classes(
                        "bg-gray-400 text-white px-4 py-2 rounded")

    # 💕 /yes-date page
    @ui.page("/yes-date")
    def yes_date_page():
        with ui.row().classes("w-screen h-screen items-center justify-center bg-pink-100"):
            with ui.column().classes("items-center justify-center gap-6 text-center"):
                ui.label("Yaaay! Pick a date for the special day 💕").classes("text-xl text-pink-700").style(
                    "font-family: 'Dancing Script', cursive;")
                date_picker = ui.date()
                selected_date_text = ui.label("").classes("text-pink-800")

                def confirm():
                    selected = str(date_picker.value)
                    selected_date_text.text = f"Mission Successful !! Can't wait for {selected}! 🎉"
                    send_email_notification(rating_value, True, selected)
                    ui.notify("Date saved 💌", type="positive", duration=5)

                    ui.run_javascript("""
                                        setTimeout(() => {
                                            window.location.href = '/thankyou';
                                        }, 5000);
                                    """)

                ui.button("Confirm", on_click=confirm).classes("bg-pink-600 text-white px-4 py-2 rounded")

    # 🙈 /no-date page
    @ui.page("/no-date")
    def no_date_page():
        send_email_notification(rating_value, False, None)

        with ui.row().classes("w-screen h-screen items-center justify-center bg-rose-100"):
            with ui.column().classes("items-center justify-center gap-6 text-center"):
                ui.label("That's okay! I still want to tell you that you're Amazing ... 💗").classes("text-xl text-rose-700").style(
                    "font-family: 'Dancing Script', cursive;")
                # Use ui.timer to delay the navigation by 5 seconds
                ui.run_javascript("""
                                    setTimeout(() => {
                                        window.location.href = '/thankyou';
                                    }, 5000);
                                """)

ui.run(title="A Little Something for Anna 🌟", port=8082, reload=False)
