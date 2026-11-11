import streamlit as st
import random
import time
import html
from datetime import datetime

# =========================================================
# AB SCHOOL LOOP AI - MIND POWER MODULE
# Mind Power 1.0
# =========================================================

BG = "#08111F"
CARD = "#101F34"
CYAN = "#22D3EE"
MINT = "#5EEAD4"
WHITE = "#F4F8FF"
MUTED = "#B8C7D9"
PURPLE = "#A78BFA"

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
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


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
    .mp-card h3 {color:#5EEAD4;}
    .mp-card p {color:#B8C7D9;}
    .mp-word {
        display:inline-block;
        background:#172B45;
        border:1px solid #22D3EE55;
        border-radius:12px;
        padding:14px 20px;
        margin:5px;
        color:#F4F8FF;
        font-size:23px;
        font-weight:800;
    }
    .mp-result {
        background:linear-gradient(120deg,#123C4B,#101F34);
        border:1px solid #5EEAD455;
        border-radius:18px;
        padding:22px;
        text-align:center;
    }
    .mp-result h2 {color:#5EEAD4;}
    div.stButton > button {
        border-radius:12px;
        border:1px solid #22D3EE66;
        background:linear-gradient(90deg,#155E75,#0E7490);
        color:white;
        font-weight:700;
        min-height:42px;
    }
    div.stButton > button:hover {
        border:1px solid #5EEAD4;
        color:#5EEAD4;
    }
    </style>
    """, unsafe_allow_html=True)


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


def save_result(game, score, total):
    percentage = round(score / total * 100) if total else 0

    st.session_state.mp_history.append({
        "Game": game,
        "Score": score,
        "Total": total,
        "Accuracy": percentage,
        "Date": datetime.now().strftime("%d-%m-%Y %H:%M")
    })


# ---------------------------------------------------------
# GAME 1 - WORD MEMORY
# ---------------------------------------------------------

def word_memory_game():

    st.subheader("🧠 Word Memory Challenge")

    st.write(
        "યાદ રાખો: પાંચ શબ્દો 10 seconds માટે દેખાશે. "
        "પછી તેમને સાચા sequence માં લખવાના રહેશે."
    )

    if not st.session_state.mp_game_started:

        if st.button("🚀 Start Memory Challenge",
                     key="mp_start_word",
                     use_container_width=True):

            words = random.sample([
                "APPLE", "PLANET", "RIVER", "CAMERA",
                "MOUNTAIN", "FLOWER", "OCEAN", "ROCKET",
                "GARDEN", "CLOUD", "BRIDGE", "SUNRISE",
                "MIRROR", "LANTERN", "FOREST", "DIAMOND"
            ], 5)

            st.session_state.mp_words = words
            st.session_state.mp_game_started = True
            st.session_state.mp_word_submitted = False
            st.rerun()

    if st.session_state.mp_game_started:

        if not st.session_state.mp_word_submitted:

            st.warning("Remember the exact order!")

            word_placeholder = st.empty()

            # Display words for 10 seconds
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
                    1 for i in range(min(len(entered), len(correct)))
                    if entered[i] == correct[i]
                )

                st.session_state.mp_word_score = score
                save_result("Word Memory", score, 5)

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
                    st.write(" → ".join(correct))

                if st.button("🔄 Play Again", key="mp_word_again"):
                    st.session_state.mp_game_started = False
                    st.session_state.mp_word_submitted = False
                    st.session_state.mp_words = []
                    st.session_state.mp_word_score = None
                    st.rerun()


# ---------------------------------------------------------
# GAME 2 - COLOR STRATEGY / STROOP
# ---------------------------------------------------------

def color_strategy_game():

    st.subheader("🎨 Color Strategy Challenge")

    st.write(
        "Word નો અર્થ નહીં, પરંતુ તેના letters કયા રંગમાં "
        "દેખાય છે તે ઓળખો."
    )

    colors = {
        "RED": "#FF4545",
        "GREEN": "#27D980",
        "BLUE": "#3295FF",
        "YELLOW": "#FFD43B",
        "PURPLE": "#B58AFF"
    }

    if not st.session_state.mp_color_questions:

        if st.button("🚀 Start Color Challenge",
                     key="mp_start_color",
                     use_container_width=True):

            questions = []

            for _ in range(10):
                word = random.choice(list(colors.keys()))
                font_color = random.choice(list(colors.keys()))

                questions.append({
                    "word": word,
                    "font_color": font_color
                })

            st.session_state.mp_color_questions = questions
            st.session_state.mp_color_start = time.time()
            st.session_state.mp_color_submitted = False
            st.rerun()

    questions = st.session_state.mp_color_questions

    if questions and not st.session_state.mp_color_submitted:

        elapsed = time.time() - st.session_state.mp_color_start
        remaining = max(0, 20 - int(elapsed))

        st.progress(min(elapsed / 20, 1.0))
        st.metric("Time Remaining", f"{remaining} seconds")

        with st.form("mp_color_form"):

            st.write("Select the FONT COLOR, not the written word.")

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
                            margin:0;">
                            {html.escape(q['word'])}
                        </h3>
                        <small style="color:#B8C7D9;">
                            Question {i+1}
                        </small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                answers.append(
                    st.selectbox(
                        f"Choose font color — Q{i+1}",
                        ["Select", "RED", "GREEN", "BLUE",
                         "YELLOW", "PURPLE"],
                        key=f"mp_color_answer_{i}"
                    )
                )

            submitted = st.form_submit_button(
                "Submit Color Answers",
                use_container_width=True
            )

        if submitted:

            elapsed = time.time() - st.session_state.mp_color_start

            if elapsed > 20:
                st.session_state.mp_color_submitted = True
                st.session_state.mp_color_score = 0
                st.error("Time is over! Challenge completed.")
                st.rerun()

            else:
                score = sum(
                    1 for i, q in enumerate(questions)
                    if answers[i] == q["font_color"]
                )

                st.session_state.mp_color_score = score
                st.session_state.mp_color_submitted = True

                save_result("Color Strategy", score, 10)
                st.rerun()

    if st.session_state.mp_color_submitted:

        score = st.session_state.mp_color_score or 0

        show_game_result(
            "Color Strategy Result",
            score,
            10,
            "Color recognition challenge completed."
        )

        if st.button("🔄 Restart Color Challenge",
                     key="mp_color_again"):

            st.session_state.mp_color_questions = []
            st.session_state.mp_color_start = None
            st.session_state.mp_color_submitted = False
            st.session_state.mp_color_score = None
            st.rerun()


# ---------------------------------------------------------
# GAME 3 - PATTERN MASTER
# ---------------------------------------------------------

def pattern_master_game():

    st.subheader("🔷 Pattern Master Challenge")

    st.write(
        "Glow થતા boxes નો sequence યાદ રાખો અને પછી "
        "એ જ sequence પસંદ કરો."
    )

    if not st.session_state.mp_pattern:

        if st.button("🚀 Start Pattern Challenge",
                     key="mp_start_pattern",
                     use_container_width=True):

            pattern = random.sample(range(25), 5)

            st.session_state.mp_pattern = pattern
            st.session_state.mp_pattern_selected = []
            st.session_state.mp_pattern_submitted = False
            st.rerun()

    if st.session_state.mp_pattern:

        if not st.session_state.mp_pattern_submitted:

            st.warning("Observe the glowing sequence carefully!")

            for number in st.session_state.mp_pattern:

                placeholder = st.empty()

                grid_html = '<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:7px;">'

                for i in range(25):

                    bg = "#22D3EE" if i == number else "#172B45"

                    grid_html += f"""
                    <div style="
                        height:48px;
                        border-radius:9px;
                        background:{bg};
                        border:1px solid #5EEAD4;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        color:#FFFFFF;
                        font-weight:bold;">
                        {"★" if i == number else ""}
                    </div>
                    """

                grid_html += "</div>"

                placeholder.markdown(
                    grid_html,
                    unsafe_allow_html=True
                )

                time.sleep(1)

                placeholder.empty()

            st.session_state.mp_pattern_submitted = True
            st.rerun()

        if st.session_state.mp_pattern_submitted:

            st.info("Now select the 5 boxes in the same sequence.")

            selected = st.session_state.mp_pattern_selected

            st.write(
                f"Selected: {len(selected)}/5"
            )

            for row in range(5):

                cols = st.columns(5)

                for col in range(5):

                    number = row * 5 + col

                    with cols[col]:

                        if number in selected:
                            label = "✓"
                        else:
                            label = str(number + 1)

                        if st.button(
                            label,
                            key=f"mp_pattern_{number}",
                            use_container_width=True,
                            disabled=len(selected) >= 5 or number in selected
                        ):
                            st.session_state.mp_pattern_selected.append(
                                number
                            )
                            st.rerun()

            if len(selected) == 5:

                score = sum(
                    1 for i, number in enumerate(selected)
                    if number == st.session_state.mp_pattern[i]
                )

                st.session_state.mp_pattern_score = score

                show_game_result(
                    "Pattern Master Result",
                    score,
                    5,
                    "Visual sequence challenge completed."
                )

                if st.button("🔄 Play Again", key="mp_pattern_again"):

                    st.session_state.mp_pattern = []
                    st.session_state.mp_pattern_selected = []
                    st.session_state.mp_pattern_submitted = False
                    st.session_state.mp_pattern_score = None
                    st.rerun()


# ---------------------------------------------------------
# MAIN MIND POWER PAGE
# ---------------------------------------------------------

def render_mind_power():

    init_mind_state()
    mind_power_css()

    st.markdown("""
    <div class="mp-hero">
        <div style="color:#5EEAD4;font-weight:800;
                    letter-spacing:3px;font-size:12px;">
            AB SCHOOL LOOP AI • BRAIN TRAINING STUDIO
        </div>
        <br>
        <h1>🧠 MIND POWER</h1>
        <p>Train your memory. Improve your focus.
           Challenge your thinking.</p>
        <br>
        <div style="color:#22D3EE;font-weight:700;">
            MEMORY • COLOUR • LOGIC
        </div>
    </div>
    """, unsafe_allow_html=True)

    history = st.session_state.mp_history

    total_games = len(history)

    total_score = sum(x["Score"] for x in history)
    total_possible = sum(x["Total"] for x in history)

    accuracy = (
        round(total_score / total_possible * 100)
        if total_possible else 0
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("🎮 Games Played", total_games)
    c2.metric("🏆 Total Points", total_score)
    c3.metric("🎯 Accuracy", f"{accuracy}%")

    st.divider()

    game = st.radio(
        "Choose Your Brain Challenge",
        [
            "🧠 Word Memory",
            "🎨 Color Strategy",
            "🔷 Pattern Master"
        ],
        horizontal=True,
        key="mp_game_selector"
    )

    st.divider()

    if game == "🧠 Word Memory":
        word_memory_game()

    elif game == "🎨 Color Strategy":
        color_strategy_game()

    elif game == "🔷 Pattern Master":
        pattern_master_game()

    st.divider()

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
        "AB SCHOOL LOOP AI • MIND POWER 1.0 • "
        "Brain Training & Student Growth"
    )


# Optional direct testing:
# render_mind_power()
