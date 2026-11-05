import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import hashlib
import secrets
from datetime import date, datetime
from io import BytesIO

# =========================================================
# 1. APP CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AB SCHOOL LOOP AI | Student Growth Studio",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

APP_TITLE = "AB SCHOOL LOOP AI"
DB_PATH = "ab_school_loop_ai.db"

# =========================================================
# 2. DATABASE
# =========================================================

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def create_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT DEFAULT 'Student'
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            subject TEXT,
            topic TEXT,
            score INTEGER,
            total INTEGER,
            created_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS study_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            subject TEXT,
            topic TEXT,
            minutes INTEGER,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


create_database()


# =========================================================
# 3. USER AUTHENTICATION
# =========================================================

def hash_password(password):
    salt = secrets.token_hex(16)

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        100000
    ).hex()

    return salt + ":" + hashed


def verify_password(password, stored_password):
    try:
        salt, original_hash = stored_password.split(":")

        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt.encode(),
            100000
        ).hex()

        return secrets.compare_digest(new_hash, original_hash)

    except Exception:
        return False


def register_user(username, password, role):
    conn = get_connection()

    try:
        conn.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hash_password(password), role)
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def authenticate_user(username, password):
    conn = get_connection()

    user = conn.execute(
        "SELECT username, password, role FROM users WHERE username=?",
        (username,)
    ).fetchone()

    conn.close()

    if user and verify_password(password, user[1]):
        return user[0], user[2]

    return None


# =========================================================
# 4. DATABASE FUNCTIONS
# =========================================================

def save_quiz_result(username, subject, topic, score, total):
    conn = get_connection()

    conn.execute("""
        INSERT INTO quiz_results
        (username, subject, topic, score, total, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        username,
        subject,
        topic,
        score,
        total,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))

    conn.commit()
    conn.close()


def save_study_record(username, subject, topic, minutes):
    conn = get_connection()

    conn.execute("""
        INSERT INTO study_records
        (username, subject, topic, minutes, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        username,
        subject,
        topic,
        minutes,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))

    conn.commit()
    conn.close()


def get_quiz_results(username=None):
    conn = get_connection()

    if username:
        df = pd.read_sql_query(
            "SELECT * FROM quiz_results WHERE username=? ORDER BY id DESC",
            conn,
            params=(username,)
        )
    else:
        df = pd.read_sql_query(
            "SELECT * FROM quiz_results ORDER BY id DESC",
            conn
        )

    conn.close()
    return df


def get_study_records(username=None):
    conn = get_connection()

    if username:
        df = pd.read_sql_query(
            "SELECT * FROM study_records WHERE username=? ORDER BY id DESC",
            conn,
            params=(username,)
        )
    else:
        df = pd.read_sql_query(
            "SELECT * FROM study_records ORDER BY id DESC",
            conn
        )

    conn.close()
    return df


# =========================================================
# 5. COLOR THEME AND CSS
# =========================================================

st.markdown("""
<style>

/* MAIN BACKGROUND */

.stApp {
    background:
        radial-gradient(circle at 10% 5%,
        rgba(125, 150, 255, 0.15), transparent 30%),
        radial-gradient(circle at 90% 80%,
        rgba(110, 220, 255, 0.12), transparent 35%),
        linear-gradient(135deg, #080F25, #101B39 55%, #10152E);

    color: #F5F7FF;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #080F25,
        #111D3A,
        #17264A
    );

    border-right: 1px solid rgba(150, 180, 255, 0.18);
}

/* TEXT */

h1, h2, h3, h4 {
    color: #F5F7FF !important;
}

p, label, span {
    color: #DCE5FF;
}

/* HERO */

.hero {
    padding: 35px;
    border-radius: 25px;

    background: linear-gradient(
        120deg,
        rgba(55, 91, 170, 0.35),
        rgba(100, 210, 230, 0.13),
        rgba(150, 135, 255, 0.18)
    );

    border: 1px solid rgba(170, 200, 255, 0.25);
    box-shadow: 0 12px 40px rgba(0,0,0,0.25);

    margin-bottom: 25px;
}

/* CRYSTAL MIND HERO */

.mind-hero {
    padding: 35px;
    border-radius: 26px;

    background: linear-gradient(
        125deg,
        #E9E7FF,
        #DDF3FF,
        #F8F9FF
    );

    color: #202B50 !important;
    box-shadow: 0 15px 40px rgba(125, 160, 255, 0.18);
}

.mind-hero h1,
.mind-hero h2,
.mind-hero p {
    color: #202B50 !important;
}

/* CARDS */

.custom-card {
    padding: 22px;
    border-radius: 20px;

    background: linear-gradient(
        145deg,
        rgba(36, 55, 100, 0.80),
        rgba(21, 34, 69, 0.90)
    );

    border: 1px solid rgba(160, 190, 255, 0.20);
    box-shadow: 0 8px 25px rgba(0,0,0,0.18);

    min-height: 130px;
}

/* MIND CARDS */

.mind-card {
    padding: 22px;
    border-radius: 20px;

    background: linear-gradient(
        140deg,
        #F6F5FF,
        #E8F6FF
    );

    border: 1px solid #D8E5FF;
    box-shadow: 0 8px 25px rgba(130, 160, 220, 0.15);

    color: #273456;
    min-height: 140px;
}

.mind-card h3,
.mind-card p {
    color: #273456 !important;
}

/* METRICS */

div[data-testid="stMetric"] {
    background: rgba(35, 55, 100, 0.65);
    border: 1px solid rgba(140, 180, 255, 0.20);
    padding: 18px;
    border-radius: 18px;
}

/* BUTTONS */

.stButton > button {
    background: linear-gradient(
        100deg,
        #42C9E8,
        #71E2CE
    );

    color: #07162B !important;
    border: none;
    border-radius: 12px;
    padding: 10px 22px;
    font-weight: 700;

    transition: 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 7px 22px rgba(70, 210, 230, 0.25);
}

/* INPUTS */

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background: #172647 !important;
    color: white !important;
    border: 1px solid #425B8A !important;
    border-radius: 10px !important;
}

.stSelectbox div[data-baseweb="select"] {
    background: #172647;
    border-radius: 10px;
}

/* TABS */

.stTabs [data-baseweb="tab"] {
    color: #C6D5FF;
}

.stTabs [aria-selected="true"] {
    color: #67E4E1 !important;
}

/* DIVIDER */

hr {
    border-color: rgba(150, 180, 255, 0.20);
}

/* FOOTER */

.footer {
    text-align: center;
    color: #91A8D5;
    padding: 25px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 6. SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = "Student"


# =========================================================
# 7. LOGIN AND REGISTRATION
# =========================================================

def login_page():

    st.markdown("""
    <div class="hero">
        <h1>🎓 AB SCHOOL LOOP AI</h1>
        <h3>Student Growth Studio</h3>
        <p>SMART LEARNING • MIND POWER • HEALTHY GROWTH</p>
    </div>
    """, unsafe_allow_html=True)

    login_tab, register_tab = st.tabs([
        "🔐 Login",
        "✨ Create Account"
    ])

    with login_tab:

        st.subheader("Welcome Back")

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login", use_container_width=True):

            result = authenticate_user(username, password)

            if result:

                st.session_state.logged_in = True
                st.session_state.username = result[0]
                st.session_state.role = result[1]

                st.success("Login successful!")
                st.rerun()

            else:
                st.error("Incorrect username or password.")

    with register_tab:

        st.subheader("Create Your Account")

        new_username = st.text_input(
            "Choose Username",
            key="register_username"
        )

        new_password = st.text_input(
            "Choose Password",
            type="password",
            key="register_password"
        )

        role = st.selectbox(
            "Account Type",
            ["Student", "Teacher"]
        )

        if st.button("Create Account", use_container_width=True):

            if len(new_username.strip()) < 3:
                st.warning("Username must contain at least 3 characters.")

            elif len(new_password) < 6:
                st.warning("Password must contain at least 6 characters.")

            else:

                success = register_user(
                    new_username.strip(),
                    new_password,
                    role
                )

                if success:
                    st.success("Account created! Please login.")

                else:
                    st.error("This username is already registered.")


# =========================================================
# 8. QUIZ QUESTION BANK
# =========================================================

QUIZ_BANK = {

    "Physics": {

        "Motion": [

            {
                "question": "What is the SI unit of velocity?",
                "options": ["Metre", "Metre/second", "Second", "Newton"],
                "answer": "Metre/second"
            },

            {
                "question": "Which quantity is a vector?",
                "options": ["Distance", "Speed", "Velocity", "Time"],
                "answer": "Velocity"
            },

            {
                "question": "The slope of a displacement-time graph represents:",
                "options": ["Acceleration", "Velocity", "Force", "Mass"],
                "answer": "Velocity"
            }

        ],

        "Force": [

            {
                "question": "What is the SI unit of force?",
                "options": ["Joule", "Newton", "Watt", "Pascal"],
                "answer": "Newton"
            },

            {
                "question": "Newton's first law is also called:",
                "options": [
                    "Law of inertia",
                    "Law of energy",
                    "Law of acceleration",
                    "Law of gravity"
                ],
                "answer": "Law of inertia"
            }

        ]
    },

    "Chemistry": {

        "Chemical Bonding": [

            {
                "question": "Which bond involves sharing of electrons?",
                "options": [
                    "Ionic bond",
                    "Covalent bond",
                    "Metallic bond",
                    "Hydrogen bond"
                ],
                "answer": "Covalent bond"
            },

            {
                "question": "The shape of methane is:",
                "options": [
                    "Linear",
                    "Trigonal planar",
                    "Tetrahedral",
                    "Bent"
                ],
                "answer": "Tetrahedral"
            }

        ],

        "Periodic Trends": [

            {
                "question": "Across a period, atomic radius generally:",
                "options": [
                    "Increases",
                    "Decreases",
                    "Remains constant",
                    "Becomes zero"
                ],
                "answer": "Decreases"
            }

        ]
    },

    "Mathematics": {

        "Trigonometry": [

            {
                "question": "sin²θ + cos²θ = ?",
                "options": ["0", "1", "2", "tan θ"],
                "answer": "1"
            },

            {
                "question": "Value of sin 90° is:",
                "options": ["0", "1", "-1", "1/2"],
                "answer": "1"
            }

        ],

        "Algebra": [

            {
                "question": "What is (a+b)²?",
                "options": [
                    "a²+b²",
                    "a²+2ab+b²",
                    "a²-2ab+b²",
                    "a²-b²"
                ],
                "answer": "a²+2ab+b²"
            }

        ]
    },

    "English": {

        "Vocabulary": [

            {
                "question": "Choose the synonym of 'Rapid'.",
                "options": [
                    "Slow",
                    "Fast",
                    "Weak",
                    "Small"
                ],
                "answer": "Fast"
            },

            {
                "question": "Choose the opposite of 'Ancient'.",
                "options": [
                    "Old",
                    "Modern",
                    "Historic",
                    "Traditional"
                ],
                "answer": "Modern"
            }

        ]
    }

}


# =========================================================
# 9. COMMON PAGE HEADER
# =========================================================

def page_header(title, subtitle):

    st.markdown(f"""
    <div class="hero">
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# 10. MIND POWER PAGE
# =========================================================

def mind_power_page():

    st.markdown("""
    <div class="mind-hero">
        <h1>🧠 Mind Power</h1>
        <h3>Train Your Mind. Unlock Your Potential.</h3>
        <p>
        Build focus, memory, creativity and positive thinking
        through simple daily activities.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="mind-card">
            <h3>🎯 Focus</h3>
            <p>Improve attention and concentration during study sessions.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="mind-card">
            <h3>🧩 Memory</h3>
            <p>Practice recall and strengthen learning through revision.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="mind-card">
            <h3>💡 Creativity</h3>
            <p>Explore new ideas and develop problem-solving skills.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    st.subheader("✨ Daily Mind Training")

    activity = st.selectbox(
        "Choose Your Activity",
        [
            "Focus Challenge",
            "Memory Challenge",
            "Creative Thinking",
            "Logical Thinking"
        ]
    )

    if activity == "Focus Challenge":

        st.markdown("""
        <div class="mind-card">
            <h3>🎯 Focus Challenge</h3>
            <p>
            Take a short study session. Select one task and
            concentrate on it without switching between activities.
            </p>
        </div>
        """, unsafe_allow_html=True)

        minutes = st.slider(
            "Choose your focus session",
            5, 30, 15
        )

        st.info(
            f"Your selected focus session is {minutes} minutes."
        )

        st.write(
            "Tip: Take a comfortable break after your session."
        )

    elif activity == "Memory Challenge":

        st.markdown("""
        <div class="mind-card">
            <h3>🧩 Memory Challenge</h3>
            <p>Remember these five words:</p>
            <h3>APPLE • RIVER • BOOK • STAR • CLOUD</h3>
            <p>Now try to recall them without looking.</p>
        </div>
        """, unsafe_allow_html=True)

        memory_answer = st.text_input(
            "Write the words you remember"
        )

        if st.button("Check Memory Practice"):

            correct_words = [
                "apple", "river", "book", "star", "cloud"
            ]

            entered_words = [
                x.strip().lower()
                for x in memory_answer.split(",")
            ]

            score = sum(
                1 for word in correct_words
                if word in entered_words
            )

            st.success(
                f"You recalled {score} out of 5 words."
            )

    elif activity == "Creative Thinking":

        st.markdown("""
        <div class="mind-card">
            <h3>💡 Creative Thinking</h3>
            <p>
            Think of three different ways technology can
            make school learning better.
            </p>
        </div>
        """, unsafe_allow_html=True)

        creative_answer = st.text_area(
            "Write your ideas"
        )

        if creative_answer:
            st.info("Great! Keep exploring your ideas.")

    elif activity == "Logical Thinking":

        st.markdown("""
        <div class="mind-card">
            <h3>🔍 Logical Thinking</h3>
            <p>
            Complete the number sequence:
            </p>
            <h2>2, 4, 8, 16, __</h2>
        </div>
        """, unsafe_allow_html=True)

        logical_answer = st.text_input(
            "Your answer",
            key="logical_answer"
        )

        if st.button("Check Answer"):

            if logical_answer.strip() == "32":
                st.success("Correct! Excellent logical thinking.")

            else:
                st.warning("Try again. Look at the pattern.")

    st.divider()

    st.subheader("🌱 Mind Power Habits")

    habits = [
        "Practice focused learning",
        "Take regular breaks",
        "Get enough sleep",
        "Read something interesting",
        "Spend time on creative activities"
    ]

    for habit in habits:
        st.checkbox(habit, key="mind_" + habit)

    st.caption(
        "Mind Power activities are educational exercises, "
        "not a medical or psychological assessment."
    )


# ==
