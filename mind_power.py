import streamlit as st
import random
import time

# =========================================================
# AB SCHOOL LOOP AI - WORD MEMORY GAME
# Only Word Memory Game
# =========================================================

def show_mind_power():

    st.title("🧠 Mind Power")
    st.subheader("📚 Word Memory Challenge")

    st.write("Remember the words and type them in the correct order.")

    # -----------------------------------------------------
    # WORD BANK
    # -----------------------------------------------------

    word_bank = [
        "Apple", "Tiger", "Ocean", "Book", "Mountain",
        "River", "Planet", "School", "Flower", "Window",
        "Rocket", "Camera", "Forest", "Orange", "Garden",
        "Mirror", "Laptop", "Cloud", "Diamond", "Bridge",
        "Shadow", "Sunlight", "Village", "Journey", "Rainbow",
        "Thunder", "Elephant", "Butterfly", "Knowledge", "Universe",
        "Adventure", "Energy", "Galaxy", "Freedom", "Creative",
        "Science", "Mystery", "Courage", "Dream", "Future",
        "Discovery", "Technology", "Imagine", "Brilliant", "Wisdom",
        "Strategy", "Focus", "Learning", "Intelligence", "Success"
    ]

    # -----------------------------------------------------
    # SESSION STATE
    # -----------------------------------------------------

    if "wm_level" not in st.session_state:
        st.session_state.wm_level = 1

    if "wm_score" not in st.session_state:
        st.session_state.wm_score = 0

    if "wm_stage" not in st.session_state:
        st.session_state.wm_stage = "start"

    if "wm_words" not in st.session_state:
        st.session_state.wm_words = []

    if "wm_attempts" not in st.session_state:
        st.session_state.wm_attempts = 0

    # -----------------------------------------------------
    # GAME INFORMATION
    # -----------------------------------------------------

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    col1.metric("🏆 Score", st.session_state.wm_score)
    col2.metric("🚀 Level", st.session_state.wm_level)
    col3.metric("🧠 Words", min(5 + st.session_state.wm_level - 1, 20))

    st.progress(min(st.session_state.wm_level / 20, 1.0))

    st.markdown("---")

    # -----------------------------------------------------
    # START GAME
    # -----------------------------------------------------

    if st.session_state.wm_stage == "start":

        st.info("Memorize the words carefully. Their order is important.")

        if st.button("▶ Start Memory Challenge", use_container_width=True):

            number_of_words = min(
                5 + st.session_state.wm_level - 1,
                20
            )

            st.session_state.wm_words = random.sample(
                word_bank,
                number_of_words
            )

            st.session_state.wm_stage = "memorize"

            st.rerun()

    # -----------------------------------------------------
    # MEMORIZATION STAGE
    # -----------------------------------------------------

    elif st.session_state.wm_stage == "memorize":

        st.success("👀 Memorize these words!")

        st.markdown(
            """
            <div style="
                padding:20px;
                border-radius:15px;
                background:linear-gradient(135deg,#14243D,#253B60);
                text-align:center;
                color:white;
                ">
            """,
            unsafe_allow_html=True
        )

        for i, word in enumerate(st.session_state.wm_words, start=1):

            st.markdown(
                f"""
                <h3 style="text-align:center;color:#5EEAD4;">
                    {i}. {word}
                </h3>
                """,
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

        st.warning("Remember all words and their exact order.")

        if st.button("🙈 Hide Words & Continue", use_container_width=True):

            st.session_state.wm_stage = "answer"

            st.rerun()

    # -----------------------------------------------------
    # ANSWER STAGE
    # -----------------------------------------------------

    elif st.session_state.wm_stage == "answer":

        st.info("Enter all remembered words in the correct order.")

        st.write(
            f"Number of words to remember: "
            f"{len(st.session_state.wm_words)}"
        )

        with st.form("word_memory_form"):

            user_answer = st.text_input(
                "Enter words separated by commas",
                placeholder="Apple, Tiger, Ocean, Book..."
            )

            submitted = st.form_submit_button(
                "Submit Answer",
                use_container_width=True
            )

        if submitted:

            user_words = [
                word.strip().lower()
                for word in user_answer.split(",")
                if word.strip()
            ]

            correct_words = [
                word.lower()
                for word in st.session_state.wm_words
            ]

            if user_words == correct_words:

                st.session_state.wm_score += (
                    st.session_state.wm_level * 10
                )

                st.session_state.wm_level += 1

                st.session_state.wm_stage = "success"

                st.rerun()

            else:

                st.session_state.wm_attempts += 1

                st.session_state.wm_stage = "failed"

                st.rerun()

    # -----------------------------------------------------
    # SUCCESS STAGE
    # -----------------------------------------------------

    elif st.session_state.wm_stage == "success":

        st.success("🎉 Excellent! All words are correct.")

        st.balloons()

        st.metric("Points Earned", (st.session_state.wm_level - 1) * 10)

        st.write("Your memory is progressing to the next level!")

        if st.button("➡ Next Level", use_container_width=True):

            st.session_state.wm_stage = "start"

            st.rerun()

    # -----------------------------------------------------
    # FAILED STAGE
    # -----------------------------------------------------

    elif st.session_state.wm_stage == "failed":

        st.error("❌ Incorrect order or missing words.")

        st.write("Correct word sequence:")

        st.write(" → ".join(st.session_state.wm_words))

        if st.button("🔄 Try Again", use_container_width=True):

            st.session_state.wm_stage = "start"

            st.rerun()

    # -----------------------------------------------------
    # RESTART
    # -----------------------------------------------------

    st.markdown("---")

    if st.button("🔁 Restart Word Memory Game"):

        st.session_state.wm_level = 1
        st.session_state.wm_score = 0
        st.session_state.wm_stage = "start"
        st.session_state.wm_words = []
        st.session_state.wm_attempts = 0

        st.rerun()
