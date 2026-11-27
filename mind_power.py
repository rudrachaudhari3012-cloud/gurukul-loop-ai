import streamlit as st
import random
import time
import html
import sqlite3
import uuid
from datetime import datetime

# =========================================================
# AB SCHOOL LOOP AI - MIND POWER MODULE
# Mind Power 1.1
# =========================================================

BG = "#08111F"
CARD = "#101F34"
CYAN = "#22D3EE"
MINT = "#5EEAD4"
WHITE = "#F4F8FF"
MUTED = "#B8C7D9"
PURPLE = "#A78BFA"

DB_PATH = "ab_school_loop_ai.db"


# ---------------------------------------------------------
# STUDENT ID
# ---------------------------------------------------------

def mp_get_student_id():

    possible_keys = ["user", "current_user", "student", "logged_user"]

    for key in possible_keys:

        user = st.session_state.get(key)

        if isinstance(user, dict):

            for field in ["id", "student_id", "username", "email"]:

                if user.get(field):
                    return str(user[field])

    if "mp_guest_id" not in st.session_state:

        st.session_state.mp_guest_id = str(uuid.uuid4())

    return st.session_state.mp_guest_id


# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------

def mp_db_init():

    try:

        conn = sqlite3.connect(DB_PATH)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS mp_game_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                game TEXT,
                score INTEGER,
                total INTEGER,
                accuracy INTEGER,
                played_at TEXT
            )
        """)

        conn.commit()
        conn.close()

    except Exception as e:

        st.warning(f"Mind Power database issue: {e}")


def mp_db_load_history(student_id):

    try:

        mp_db_init()

        conn = sqlite3.connect(DB_PATH)

        rows = conn.execute("""
            SELECT game, score, total, accuracy, played_at
            FROM mp_game_history
            WHERE student_id = ?
            ORDER BY id DESC
        """, (str(student_id),)).fetchall()

        conn.close()

        return [
            {
                "Game": row[0],
                "Score": row[1],
                "Total": row[2],
                "Accuracy": row[3],
                "Date": row[4]
            }
            for row in rows
        ]

    except Exception:

        return []


def mp_db_save_history(student_id, game, score, total, accuracy, played_at):

    try:

        mp_db_init()

        conn = sqlite3.connect(DB_PATH)

        conn.execute("""
            INSERT INTO mp_game_history
            (student_id, game, score, total, accuracy, played_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            str(student_id),
            game,
            int(score),
            int(total),
            int(accuracy),
            played_at
        ))

        conn.commit()
        conn.close()

        return True

    except Exception as e:

        st.error(f"Could not save Mind Power result: {e}")

        return False


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

def init_mind_state():

    defaults = {
        "mp_history": [],
        "mp_game": None,
        "mp_words": [],
        "mp_pattern": [],
        "mp_pattern_selected": [],
        "mp_game_started": False,
        "mp_color_questions": [],
        "mp_color_start": None,
        "mp_color_submitted": False,
        "mp_word_submitted": False,
        "mp_pattern_submitted": False,
        "mp_word_answers": "",
        "mp_word_score": None,
        "mp_color_score": None,
        "mp_pattern_score": None,
        "mp_color_round": 0,
        "mp_color_saved": False,
        "mp_word_saved": False,
        "mp_history_loaded": False,
        "mp_student_id": None,
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value

    student_id = mp_get_student_id()

    if (
        st.session_state.mp_student_id != student_id
        or not st.session_state.mp_history_loaded
    ):

        st.session_state.mp_student_id = student_id

        st.session_state.mp_history = mp_db_load_history(student_id)

        st.session_state.mp_history_loaded = True


# ---------------------------------------------------------
# DESIGN
# ---------------------------------------------------------

def mind_power_css():

    st.markdown("""
    <style>

    .mp-hero {
        background: linear-gradient(120deg,#101F34,#172B4A,#123C4B);
        border: 1px solid #22D3EE55;
        border-radius: 22px;
        padding: 30px;
        margin-bottom: 22px;
        box-shadow: 0 8px 35px #22D3EE15;
    }

    .mp-hero h1 {
        color: #F4F8FF;
        font-size: 34px;
        font-weight: 850;
        margin: 0;
    }

    .mp-hero p {
        color: #B8C7D9;
        margin-bottom: 0;
    }

    .mp-card {
        background: linear-gradient(145deg,#101F34,#142941);
        border: 1px solid #22D3EE40;
        border-radius: 18px;
        padding: 20px;
        min-height: 145px;
        margin-bottom: 12px;
    }

    .mp-card h3 {
        color: #5EEAD4;
    }

    .mp-card p {
        color: #B8C7D9;
    }

    .mp-word {
        display: inline-block;
        background: #172B45;
        border: 1px solid #22D3EE55;
        border-radius: 12px;
        padding: 14px 20px;
        margin: 5px;
        color: #F4F8FF;
        font-size: 23px;
        font-weight: 800;
    }

    .mp-result {
        background: linear-gradient(120deg,#123C4B,#101F34);
        border: 1px solid #5EEAD455;
        border-radius: 18px;
        padding: 22px;
        text-align: center;
    }

    .mp-result h2 {
        color: #5EEAD4;
    }

    div.stButton > button {
        border-radius: 12px;
        border: 1px solid #22D3EE66;
        background: linear-gradient(90deg,#155E75,#0E7490);
        color: white;
        font-weight: 700;
        min-height: 42px;
    }

    div.stButton > button:hover {
        border: 1px solid #5EEAD4;
        color: #5EEAD4;
    }

    </style>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# RESULT DISPLAY
# ---------------------------------------------------------

def show_game_result(title, score, total, message):

    percentage = round((score / total) * 100) if total else 0

    st.markdown(f"""
    <div class="mp-result">
        <h2>{html.escape(title)}</h2>
        <h1 style="color:#F4F8FF;font-size:42px;">
            {score}/{total}
        </h1>
        <h3>{percentage}% Accuracy</h3>
        <p style="color:#B8C7D9;">{html.escape(message)}</p>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# SAVE RESULT
# ---------------------------------------------------------

def save_result(game, score, total):

    percentage = round(score / total * 100) if total else 0

    played_at = datetime.now().strftime("%d-%m-%Y %H:%M")

    record = {
        "Game": game,
        "Score": int(score),
        "Total": int(total),
        "Accuracy": int(percentage),
        "Date": played_at
    }

    st.session_state.mp_history.insert(0, record)

    mp_db_save_history(
        student_id=st.session_state.mp_student_id,
        game=game,
        score=score,
        total=total,
        accuracy=percentage,
        played_at=played_at
    )


# ---------------------------------------------------------
# GAME 1 - WORD MEMORY
# ---------------------------------------------------------

def word_memory_game():

    st.subheader("🧠 Word Memory Challenge")

    st.write(
        "Remember: Five words will appear for 10 seconds. "
        "Then enter them in the exact same order."
    )

    # START
    if not st.session_state.mp_game_started:

        if st.button(
            "🚀 Start Memory Challenge",
            key="mp_start_word",
            use_container_width=True
        ):

            words = random.sample([
                "APPLE", "PLANET", "RIVER", "CAMERA",
                "MOUNTAIN", "FLOWER", "OCEAN", "ROCKET",
                "GARDEN", "CLOUD", "BRIDGE", "SUNRISE",
                "MIRROR", "LANTERN", "FOREST", "DIAMOND",
                "THUNDER", "CASTLE", "COMPASS", "GALAXY"
            ], 5)

            st.session_state.mp_words = words
            st.session_state.mp_game_started = True
            st.session_state.mp_word_submitted = False
            st.session_state.mp_word_score = None
            st.session_state.mp_word_saved = False

            st.rerun()

    # GAME STARTED
    if st.session_state.mp_game_started:

        if not st.session_state.mp_word_submitted:

            st.warning("Remember the exact order!")

            word_placeholder = st.empty()

            for remaining in range(10, 0, -1):

                word_html = "".join(
                    f'<span class="mp-word">{html.escape(w)}</span>'
                    for w in st.session_state.mp_words
                )

                word_placeholder.markdown(
                    f"""
                    <div style="text-align:center;">
                        <h2 style="color:#22D3EE;">
                            {remaining} seconds
                        </h2>
                            {word_html}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                time.sleep(1)

            word_placeholder.empty()

            st.session_state.mp_word_submitted = True

            st.rerun()

        # ANSWER
        if st.session_state.mp_word_submitted:

            st.info("⏳ Time finished! Enter the 5 words in the same order.")

            with st.form("mp_word_form"):

                answer = st.text_input(
                    "Enter words separated by commas",
                    placeholder="APPLE, RIVER, PLANET, ..."
                )

                submitted = st.form_submit_button(
                    "Submit Answer",
                    use_container_width=True
                )

            if submitted:

                entered = [
                    x.strip().upper()
                    for x in answer.split(",")
                    if x.strip()
                ]

                correct = st.session_state.mp_words

                score = sum(
                    1
                    for i in range(min(len(entered), len(correct)))
                    if entered[i] == correct[i]
                )

                st.session_state.mp_word_score = score

                if not st.session_state.mp_word_saved:

                    save_result("Word Memory", score, 5)

                    st.session_state.mp_word_saved = True

                st.rerun()

        # RESULT
        if (
            st.session_state.mp_word_submitted
            and st.session_state.mp_word_score is not None
        ):

            score = st.session_state.mp_word_score

            show_game_result(
                "Memory Result",
                score,
                5,
                "Sequence memory practice completed."
            )

            if score == 5:

                st.success("Excellent! Perfect sequence!")

            elif score >= 3:

                st.info("Good effort! Keep practising.")

            else:

                st.info("Keep practising your sequence memory.")

            with st.expander("View correct sequence"):

                st.write(" → ".join(st.session_state.mp_words))

            if st.button("🔄 Play Again", key="mp_word_again"):

                st.session_state.mp_game_started = False
                st.session_state.mp_word_submitted = False
                st.session_state.mp_words = []
                st.session_state.mp_word_score = None
                st.session_state.mp_word_saved = False

                st.rerun()


# ---------------------------------------------------------
# GAME 2 - COLOR STRATEGY / STROOP
# ---------------------------------------------------------

def color_strategy_game():

    st.subheader("🎨 Color Strategy Challenge")

    st.write(
        "Ignore the written word. Identify the actual FONT COLOR "
        "in which the word is displayed."
    )

    colors = {
        "RED": "#FF4545",
        "GREEN": "#27D980",
        "BLUE": "#3295FF",
        "YELLOW": "#FFD43B",
        "PURPLE": "#B58AFF"
    }

    color_names = list(colors.keys())

    # -----------------------------------------------------
    # START GAME
    # -----------------------------------------------------

    if not st.session_state.mp_color_questions:

        if st.button(
            "🚀 Start Color Challenge",
            key="mp_start_color",
            use_container_width=True
        ):

            questions = []

            for _ in range(10):

                word = random.choice(color_names)

                # Written word and font color MUST be different
                available_colors = [
                    c for c in color_names
                    if c != word
                ]

                font_color = random.choice(available_colors)

                questions.append({
                    "word": word,
                    "font_color": font_color
                })

            st.session_state.mp_color_questions = questions
            st.session_state.mp_color_start = time.time()
            st.session_state.mp_color_submitted = False
            st.session_state.mp_color_score = None
            st.session_state.mp_color_saved = False
            st.session_state.mp_color_round += 1

            st.rerun()

    questions = st.session_state.mp_color_questions

    # -----------------------------------------------------
    # LIVE GAME + TIMER
    # -----------------------------------------------------

    if questions and not st.session_state.mp_color_submitted:

        @st.fragment(run_every="1s")
        def live_color_game():

            elapsed = time.time() - st.session_state.mp_color_start

            remaining = max(0, 20 - int(elapsed))

            st.progress(min(elapsed / 20, 1.0))

            st.metric(
                "⏱️ Time Remaining",
                f"{remaining} seconds"
            )

            # All questions remain visible during the timer.
            with st.form(
                key=f"mp_color_form_{st.session_state.mp_color_round}"
            ):

                st.write(
                    "### Select the FONT COLOR, not the written word."
                )

                answers = []

                for i, q in enumerate(questions):

                    st.markdown(
                        f"""
                        <div style="
                            background:#101F34;
                            padding:12px;
                            border-radius:12px;
                            margin:5px 0;
                            text-align:center;
                            border:1px solid #22D3EE44;">

                            <h3 style="
                                color:{colors[q['font_color']]};
                                margin:0;
                                font-size:30px;
                                font-weight:900;">
                                {html.escape(q['word'])}
                            </h3>

                            <small style="color:#B8C7D9;">
                                Question {i+1}
                            </small>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    answer = st.selectbox(
                        f"Choose displayed color — Q{i+1}",
                        [
                            "Select",
                            "RED",
                            "GREEN",
                            "BLUE",
                            "YELLOW",
                            "PURPLE"
                        ],
                        key=(
                            f"mp_color_answer_"
                            f"{st.session_state.mp_color_round}_{i}"
                        )
                    )

                    answers.append(answer)

                # Submit only becomes available after 20 seconds.
                if remaining == 0:

                    submitted = st.form_submit_button(
                        "✅ Submit Color Answers",
                        use_container_width=True
                    )

                else:

                    st.info(
                        f"⏳ Wait for the countdown to finish. "
                        f"Submit will unlock in {remaining} seconds."
                    )

                    submitted = st.form_submit_button(
                        "🔒 Submit Color Answers",
                        disabled=True,
                        use_container_width=True
                    )

            if submitted:

                elapsed_now = time.time() - st.session_state.mp_color_start

                # Submission is accepted only after the countdown.
                if elapsed_now >= 20:

                    score = sum(
                        1
                        for i, q in enumerate(questions)
                        if answers[i] == q["font_color"]
                    )

                    st.session_state.mp_color_score = score
                    st.session_state.mp_color_submitted = True

                    if not st.session_state.mp_color_saved:

                        save_result("Color Strategy", score, 10)

                        st.session_state.mp_color_saved = True

                    st.rerun()

        live_color_game()

    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    if st.session_state.mp_color_submitted:

        score = st.session_state.mp_color_score or 0

        show_game_result(
            "Color Strategy Result",
            score,
            10,
            "Color recognition challenge completed."
        )

        if score == 10:

            st.success("🔥 Outstanding! All colors identified correctly.")

        elif score >= 7:

            st.success("🌟 Excellent focus! Great work.")

        elif score >= 4:

            st.info("👏 Good attempt! Keep practising.")

        else:

            st.info(
                "🧠 Keep practising. Focus on the displayed font color."
            )

        if st.button(
            "🔄 Restart Color Challenge",
            key="mp_color_again"
        ):

            old_round = st.session_state.mp_color_round

            for i in range(10):

                key = f"mp_color_answer_{old_round}_{i}"

                if key in st.session_state:

                    del st.session_state[key]

            st.session_state.mp_color_questions = []
            st.session_state.mp_color_start = None
            st.session_state.mp_color_submitted = False
            st.session_state.mp_color_score = None
            st.session_state.mp_color_saved = False

            st.rerun()


# ---------------------------------------------------------
# MAIN MIND POWER PAGE
# ---------------------------------------------------------

def render_mind_power():

    init_mind_state()
    mind_power_css()

    st.markdown("""
    <div class="mp-hero">

        <div style="
            color:#5EEAD4;
            font-weight:800;
            letter-spacing:3px;
            font-size:12px;">
            AB SCHOOL LOOP AI • BRAIN TRAINING STUDIO
        </div>

        <br>

        <h1>🧠 MIND POWER</h1>

        <p>
            Train your memory. Improve your focus.
            Challenge your thinking.
        </p>

        <br>

        <div style="color:#22D3EE;font-weight:700;">
            MEMORY • COLOUR • LOGIC
        </div>

    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # ANALYTICS
    # -----------------------------------------------------

    history = st.session_state.mp_history

    total_games = len(history)

    total_score = sum(x["Score"] for x in history)

    total_possible = sum(x["Total"] for x in history)

    accuracy = (
        round(total_score / total_possible * 100)
        if total_possible
        else 0
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("🎮 Games Played", total_games)

    c2.metric("🏆 Total Points", total_score)

    c3.metric("🎯 Accuracy", f"{accuracy}%")

    st.divider()

    # -----------------------------------------------------
    # GAME SELECTOR
    # -----------------------------------------------------

    game = st.radio(
        "Choose Your Brain Challenge",
        [
            "🧠 Word Memory",
            "🎨 Color Strategy",
        ],
        horizontal=True,
        key="mp_game_selector"
    )

    st.divider()

    # -----------------------------------------------------
    # GAME ROUTING
    # -----------------------------------------------------

    if game == "🧠 Word Memory":

        word_memory_game()

    elif game == "🎨 Color Strategy":

        color_strategy_game()

    st.divider()

    # -----------------------------------------------------
    # HISTORY
    # -----------------------------------------------------

    st.subheader("📊 Your Mind Power History")

    if history:

        import pandas as pd

        df = pd.DataFrame(history)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            df,
            x="Game",
            y="Accuracy"
        )

    else:

        st.info(
            "Complete your first challenge to see your progress here."
        )

    st.caption(
        "AB SCHOOL LOOP AI • MIND POWER "
        "Brain Training & Student Growth"
    )


# ---------------------------------------------------------
# OPTIONAL DIRECT TEST
# ---------------------------------------------------------

# render_mind_power()
