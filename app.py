
import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import hashlib
import secrets
import io
import os
from ai_coach import create_ai_chat
import base64
from pathlib import Path
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_base64 = get_base64_image("logo.png")

from supabase import create_client
from health_power import render_health_power
from datetime import date, datetime
from mind_power import render_mind_power
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

APP_TITLE = "AB SCHOOL LOOP AI"
DB_PATH = "ab_school_loop_ai.db"
# =====================================================
# SUPABASE CONNECTION
# =====================================================

@st.cache_resource
def get_supabase_client():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_PUBLISHABLE_KEY"]

        return create_client(url, key)

    except Exception as e:
        st.error(f"Supabase connection setup error: {e}")
        return None

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
) 

# ==========================================
# AB SCHOOL LOOP AI - PREMIUM CLEAR THEME
# ==========================================

from pathlib import Path
import base64
import streamlit as st

bg_path = Path(__file__).parent / "background.png"

if bg_path.exists():
    bg = base64.b64encode(bg_path.read_bytes()).decode()

    st.markdown(f"""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {{
        --text: #FFFFFF;
        --muted: #D6E4F5;
        --cyan: #48E5FF;
        --blue: #168DFF;
    }}

    /* BACKGROUND */
    .stApp {{
        background:
            linear-gradient(
                rgba(3, 9, 27, 0.82),
                rgba(3, 9, 27, 0.88)
            ),
            url("data:image/png;base64,{bg}");

        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        font-family: 'Inter', sans-serif !important;
    }}

    /* MAIN CONTENT */
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    .main,
    .block-container {{
        background: transparent !important;
    }}

    /* HEADINGS */
    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4 {{
        color: #FFFFFF !important;
        font-weight: 800 !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }}

    /* ALL TEXT */
    .stApp p,
    .stApp li,
    .stApp label,
    .stApp span,
    .stMarkdown,
    [data-testid="stWidgetLabel"] {{
        color: #F4F8FF !important;
    }}

    /* SECONDARY TEXT */
    [data-testid="stCaptionContainer"] {{
        color: #D6E4F5 !important;
    }}

    /* SIDEBAR */
    [data-testid="stSidebar"] {{
        background: linear-gradient(
            180deg,
            #061329,
            #0B2043,
            #101633
        ) !important;

        border-right: 1px solid #168DFF;
    }}

    [data-testid="stSidebar"] * {{
        color: #FFFFFF !important;
    }}

    /* GLASS CARDS */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: rgba(7, 22, 48, 0.97) !important;
        border: 1px solid rgba(72, 229, 255, 0.55) !important;
        border-radius: 18px !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }}

    /* METRICS */
    [data-testid="stMetric"] {{
        background: #0B2043 !important;
        border: 1px solid #168DFF !important;
        border-radius: 16px !important;
        padding: 18px !important;
    }}

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] p {{
        color: #D6E4F5 !important;
    }}

    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] * {{
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }}

    /* BUTTONS */
    .stButton > button,
    .stDownloadButton > button,
    [data-testid="stFormSubmitButton"] > button {{
        background: linear-gradient(
            100deg,
            #087EFF,
            #6848D9
        ) !important;

        color: #FFFFFF !important;
        border: 1px solid #48E5FF !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        min-height: 44px;
    }}

    /* INPUTS */
    .stTextInput input,
    .stTextArea textarea,
    [data-baseweb="select"] > div {{
        background: #102443 !important;
        color: #FFFFFF !important;
        border: 1px solid #48A9FF !important;
        border-radius: 10px !important;
    }}

    input::placeholder,
    textarea::placeholder {{
        color: #C5D5E9 !important;
        opacity: 1 !important;
    }}

    /* TABS */
    .stTabs [data-baseweb="tab-list"] {{
        background: #0B1C38 !important;
        border-radius: 12px;
    }}

    .stTabs [data-baseweb="tab"] {{
        color: #FFFFFF !important;
    }}

    .stTabs [aria-selected="true"] {{
        color: #48E5FF !important;
    }}

    /* ALERTS */
    [data-testid="stAlert"] {{
        background: #102443 !important;
    }}

    [data-testid="stAlert"] * {{
        color: #FFFFFF !important;
    }}

    /* HEADER */
    [data-testid="stHeader"] {{
        background: transparent !important;
    }}

    /* DIVIDERS */
    hr {{
        border-color: rgba(72,229,255,0.3) !important;
    }}

    </style>
    """, unsafe_allow_html=True)

else:
    st.error("background.png not found!")

# =====================================================
# LANGUAGE
# =====================================================

TEXT = {
    "English": {
        "tagline": "Smart Learning · Healthy Life · Bright Future",
        "intro": "A student growth and learning support studio.",
        "login": "Login",
        "register": "Create account",
        "username": "Username",
        "password": "Password",
        "name": "Student / Teacher name",
        "role": "Account type",
        "student": "Student",
        "teacher": "Teacher",
        "class": "Class / Grade",
        "enter": "Enter dashboard",
        "cancel": "Cancel / Clear",
        "logout": "Log out",
        "overview": "Overview",
        "mind": "Mind Power",
        "learning": "Learning Dashboard",
        "quiz": "AI Quiz Generator",
        "coach": "Advanced AI Coach",
        "analytics": "Performance Analytics",
        "health":"Health",
        "teacher_dash": "Teacher Dashboard",
        "values": "Values & Reflection",
        "transparent": "Transparent Prototype",
        "showcase": "Project Showcase",
        "roadmap": "Roadmap & Team",
        "judge": "Judge Q&A",
        "download": "Download PDF report",
        "goal_options": [
            "Understand difficult concepts",
            "Improve memory and recall",
            "Improve exam performance",
            "Build a balanced routine"
        ],
        "energy_options": ["Low", "Okay", "Good", "High"]
    },
    "ગુજરાતી": {
        "tagline": "સ્માર્ટ લર્નિંગ · સ્વસ્થ જીવન · ઉજ્જવળ ભવિષ્ય",
        "intro": "વિદ્યાર્થી વિકાસ અને અભ્યાસ માટેનું સહાયક પ્લેટફોર્મ.",
        "login": "લૉગિન",
        "register": "એકાઉન્ટ બનાવો",
        "username": "યુઝરનેમ",
        "password": "પાસવર્ડ",
        "name": "વિદ્યાર્થી / શિક્ષકનું નામ",
        "role": "એકાઉન્ટનો પ્રકાર",
        "student": "વિદ્યાર્થી",
        "teacher": "શિક્ષક",
        "class": "ધોરણ",
        "enter": "ડેશબોર્ડ ખોલો",
        "cancel": "રદ કરો / સાફ કરો",
        "logout": "લૉગઆઉટ",
        "overview": "ઝાંખી",
        "mind": "માઇન્ડ પાવર",
        "learning": "લર્નિંગ ડેશબોર્ડ",
        "quiz": "AI ક્વિઝ જનરેટર",
        "coach": "એડવાન્સ્ડ AI કોચ",
        "analytics": "પરફોર્મન્સ એનાલિટિક્સ",
        "health": "હેલ્થ",
        "teacher_dash": "ટીચર ડેશબોર્ડ",
        "values": "મૂલ્યો અને આત્મચિંતન",
        "transparent": "પારદર્શક પ્રોટોટાઇપ",
        "showcase": "પ્રોજેક્ટ શોકેસ",
        "roadmap": "રોડમેપ અને ટીમ",
        "judge": "જજ પ્રશ્નોત્તરી",
        "download": "PDF રિપોર્ટ ડાઉનલોડ કરો",
        "goal_options": [
            "મુશ્કેલ વિષયો સમજવા",
            "યાદશક્તિ સુધારવા",
            "પરીક્ષાનું પ્રદર્શન સુધારવા",
            "સંતુલિત દિનચર્યા બનાવવી"
        ],
        "energy_options": ["ઓછી", "ઠીક", "સારી", "ખૂબ સારી"]
    }
}

# =====================================================
# DATABASE
# =====================================================

def db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL,
            grade TEXT,
            goal TEXT,
            energy TEXT,
            intention TEXT,
            created_at TEXT NOT NULL
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            topic TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS reflections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            answer TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS health_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            log_date TEXT NOT NULL,
            sleep_hours REAL,
            water_glasses INTEGER,
            exercise_minutes INTEGER,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)

def password_hash(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        180000
    ).hex()


def create_user(username, password, full_name, role, grade):
    salt = secrets.token_hex(16)
    hashed = password_hash(password, salt)

    with db() as conn:
        conn.execute("""
        INSERT INTO users
        (username,password_hash,salt,full_name,role,grade,goal,energy,intention,created_at)
        VALUES(?,?,?,?,?,?,?,?,?,?)
        """, (
            username.lower().strip(),
            hashed,
            salt,
            full_name.strip(),
            role,
            grade,
            "",
            "",
            "",
            datetime.now().isoformat(timespec="seconds")
        ))


def authenticate(username, password):
    with db() as conn:
        user = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username.lower().strip(),)
        ).fetchone()

    if not user:
        return None

    check = password_hash(password, user["salt"])

    return user if secrets.compare_digest(
        check, user["password_hash"]
    ) else None


def get_user_results(user_id=None):
    with db() as conn:
        if user_id is None:
            rows = conn.execute("""
            SELECT q.*,u.full_name,u.username,u.grade
            FROM quiz_results q
            JOIN users u ON q.user_id=u.id
            ORDER BY q.id DESC
            """).fetchall()
        else:
            rows = conn.execute("""
            SELECT * FROM quiz_results
            WHERE user_id=? ORDER BY id DESC
            """, (user_id,)).fetchall()

    return [dict(r) for r in rows]


def save_result(user_id, subject, topic, score, total):
    with db() as conn:
        conn.execute("""
        INSERT INTO quiz_results
        (user_id,subject,topic,score,total,created_at)
        VALUES(?,?,?,?,?,?)
        """, (
            user_id, subject, topic, score, total,
            datetime.now().isoformat(timespec="seconds")
        ))
        
def save_reflection(user_id, answer):
    with db() as conn:
        conn.execute("""
        INSERT INTO reflections(user_id,answer,created_at)
        VALUES(?,?,?)
        """, (
            user_id, answer,
            datetime.now().isoformat(timespec="seconds")
        ))


init_db()
init_db()


# =====================================================
# QUESTION BANK
# =====================================================

QUIZ_BANK = {
    "Physics": {
        "Motion": [
            ("Which quantity is a vector?",
             ["Speed", "Distance", "Displacement", "Time"],
             2, "Displacement has magnitude and direction."),
            ("SI unit of acceleration?",
             ["m/s", "m/s²", "km/h", "N"],
             1, "Acceleration is measured in m/s²."),
            ("Slope of velocity-time graph?",
             ["Distance", "Acceleration", "Speed", "Momentum"],
             1, "The slope represents acceleration.")
        ],
        "Force": [
            ("Newton's first law is the law of:",
             ["Acceleration", "Inertia", "Action", "Gravitation"],
             1, "It is also called the law of inertia."),
            ("SI unit of force?",
             ["Joule", "Watt", "Newton", "Pascal"],
             2, "Force is measured in Newtons."),
            ("If net force is zero, acceleration is:",
             ["Zero", "Maximum", "Negative", "Infinite"],
             0, "Zero net force means zero acceleration.")
        ]
    },
    "Chemistry": {
        "Chemical Bonding": [
            ("Which bond involves sharing electron pairs?",
             ["Ionic", "Covalent", "Metallic", "Hydrogen"],
             1, "Covalent bonds involve shared electron pairs."),
            ("Shape of methane?",
             ["Linear", "Bent", "Tetrahedral", "Trigonal planar"],
             2, "Methane has a tetrahedral shape."),
            ("Polar covalent bonds share electrons:",
             ["Equally", "Fully transferred", "Unequally", "Removed"],
             2, "Electronegativity differences cause unequal sharing.")
        ],
        "Periodic Trends": [
            ("Across a period atomic radius generally:",
             ["Increases", "Decreases", "Same", "Doubles"],
             1, "Atomic radius generally decreases across a period."),
            ("Energy to remove an electron:",
             ["Electron affinity", "Ionisation enthalpy", "Bond energy", "Lattice energy"],
             1, "This is called ionisation enthalpy."),
            ("Same group elements generally have similar:",
             ["Neutrons", "Shells", "Valence electrons", "Isotopes"],
             2, "Main-group elements have related valence electron counts.")
        ]
    },
    "Mathematics": {
        "Trigonometry": [
            ("What is sin 30°?", ["0", "1/2", "√3/2", "1"],
             1, "sin 30° = 1/2."),
            ("What is cos 60°?", ["0", "1/2", "√3/2", "1"],
             1, "cos 60° = 1/2."),
            ("What is tan 45°?", ["0", "1/√3", "1", "√3"],
             2, "tan 45° = 1.")
        ],
        "Algebra": [
            ("If x + 5 = 12, x equals:",
             ["5", "6", "7", "17"], 2, "Subtract 5 from both sides."),
            ("Factorisation of x² − 9:",
             ["(x−9)(x+1)", "(x−3)(x+3)", "(x−3)²", "(x+9)²"],
             1, "Use difference of two squares."),
            ("Coefficient of x in 4x + 7:",
             ["4", "7", "11", "x"], 0, "The coefficient is 4.")
        ]
    },
    "English": {
        "Vocabulary": [
            ("Closest meaning of 'brief':",
             ["Short", "Angry", "Distant", "Heavy"],
             0, "Brief means short."),
            ("Opposite of 'ancient':",
             ["Old", "Modern", "Historic", "Past"],
             1, "Modern is the opposite of ancient."),
            ("A person who writes poems:",
             ["Painter", "Poet", "Pilot", "Editor"],
             1, "A poet writes poems.")
        ]
    }
}

# =====================================================
# PDF REPORT
# =====================================================

def make_pdf(user, results):
    if not PDF_AVAILABLE:
        return None

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    pdf.setFillColorRGB(.08, .14, .30)
    pdf.rect(0, height-115, width, 115, fill=1, stroke=0)

    pdf.setFillColorRGB(.75, .83, 1)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(42, height-58, "AB SCHOOL LOOP AI")

    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(42, height-80, "Student Mind & Learning Report")

    y = height - 150
    pdf.setFillColorRGB(.08, .13, .25)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(42, y, "Student Details")
    y -= 24

    pdf.setFont("Helvetica", 10)
    for line in [
        f"Name: {user['full_name']}",
        f"Class: {user['grade'] or 'Not specified'}",
        f"Role: {user['role']}",
        f"Date: {date.today().strftime('%d %b %Y')}"
    ]:
        pdf.drawString(48, y, line)
        y -= 18

    y -= 10
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(42, y, "Quiz History")
    y -= 22

    pdf.setFont("Helvetica", 9)

    for item in results[:15]:
        percentage = round(
            item["score"] / max(item["total"], 1) * 100
        )
        line = (
            f"{item['subject']} / {item['topic']}: "
            f"{item['score']}/{item['total']} ({percentage}%)"
        )
        pdf.drawString(48, y, line[:100])
        y -= 16

        if y < 75:
            pdf.showPage()
            y = height - 55
            pdf.setFont("Helvetica", 9)

    pdf.setFont("Helvetica-Oblique", 8)
    pdf.drawString(
        42, 35,
        "Educational prototype report. Not a formal assessment."
    )

    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()


# =====================================================
# LOGIN SESSION
# =====================================================

if "user" not in st.session_state:
    st.session_state.user = None

if "language" not in st.session_state:
    st.session_state.language = "English"


# =====================================================
# LOGIN / REGISTRATION
# =====================================================

head_left, head_right = st.columns([4, 1])

with head_right:
    st.session_state.language = st.selectbox(
        "Language / ભાષા",
        ["English", "ગુજરાતી"],
        index=["English", "ગુજરાતી"].index(
            st.session_state.language
        ),
        key="language_pick"
    )

T = TEXT[st.session_state.language]

if st.session_state.user is None:

    st.markdown("""
    <style>
    /* AB SCHOOL LOOP AI - PREMIUM HERO */
    .hero {
        background: linear-gradient(
            120deg,
            #101D36 0%,
            #142A4B 55%,
            #211D43 100%
        ) !important;
        border: 1px solid rgba(72, 210, 255, 0.55) !important;
        border-radius: 24px !important;
        padding: 35px !important;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.30) !important;
    }

    .hero h1 {
        color: #FFFFFF !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        text-shadow: none !important;
    }

    .hero p {
        color: #EAF2FF !important;
        font-size: 1.05rem !important;
        line-height: 1.8 !important;
    }

    .hero .eyebrow {
        color: #55DFFF !important;
        font-weight: 700 !important;
        letter-spacing: 1.5px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">STUDENT GROWTH · LEARNING SCIENCE</div>
            <h1>🎓 AB SCHOOL LOOP AI</h1>
            <p>
        """ + T["tagline"] + """<br>""" + T["intro"] + """
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Welcome to your learning studio")

    login_tab, register_tab = st.tabs([
        "🔐 " + T["login"],
        "✨ " + T["register"]
    ])

    with login_tab:
        with st.form("login_form"):
            login_user = st.text_input(T["username"])

            login_pass = st.text_input(
                T["password"],
                type="password"
            )

            login_go = st.form_submit_button(
                T["login"],
                type="primary",
                use_container_width=True
            )

        if login_go:
            found = authenticate(login_user, login_pass)

            if found:
                st.session_state.user = dict(found)
                st.rerun()
            else:
                st.error("Incorrect username or password.")

    with register_tab:
        with st.form("register_form"):
            full_name = st.text_input(T["name"])
            username = st.text_input(T["username"])

            password = st.text_input(
                T["password"] + " (minimum 8 characters)",
                type="password"
            )

            role_label = st.selectbox(
                T["role"],
                [T["student"], T["teacher"]]
            )

            grade = st.selectbox(
                T["class"],
                [
                    "Class 9", "Class 10",
                    "Class 11", "Class 12",
                    "Not applicable"
                ]
            )

            register_go = st.form_submit_button(
                "✅ " + T["register"],
                type="primary",
                use_container_width=True
            )

        if register_go:
            if not all([
                full_name.strip(),
                username.strip(),
                password
            ]):
                st.error("Please complete all required fields.")

            elif len(password) < 8:
                st.error(
                    "Password must contain at least 8 characters."
                )

            else:
                try:
                    role = (
                        "Teacher"
                        if role_label == T["teacher"]
                        else "Student"
                    )

                    create_user(
                        username,
                        password,
                        full_name,
                        role,
                        grade
                    )

                    found = authenticate(username, password)
                    st.session_state.user = dict(found)

                    st.success("Account created successfully!")
                    st.rerun()

                except sqlite3.IntegrityError:
                    st.error("Username already exists.")

        st.markdown("""
        <div class="small-note">
        🔒 Local demo: account information and quiz results
        are stored in the local SQLite database.
        </div>
        """, unsafe_allow_html=True)

    st.stop()


# =====================================================
# AUTHENTICATED APP
# =====================================================

user = st.session_state.user
is_teacher = user["role"] == "Teacher"

with st.sidebar:

    st.markdown("""
    <div style="padding:8px 0 15px;">
        <div style="font-size:38px;">🎓</div>
        <div style="font-size:22px;font-weight:800;">
            AB SCHOOL<br>LOOP AI
        </div>
        <div style="font-size:12px;color:#a9c5ff;">
              · Learning Studio
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown(
        f"### 👤 {user['full_name']}"
    )

    st.caption(
        f"{user['role']} · {user['grade'] or '—'}"
    )

    st.divider()

    # Only the active student-platform sections are shown in navigation.
    # The five presentation-only sections are intentionally hidden.
    nav_items = [
        T["overview"],
        T["learning"],
        T["quiz"],
        T["mind"],
        T["coach"],
        T["analytics"],
        T["health"],
    ]

    if is_teacher:
        nav_items.insert(6, T["teacher_dash"])

    # Quick Access buttons update this radio selection through a callback,
    # so the same pages remain available from the sidebar and Overview.
    def navigate_to(target_page):
        st.session_state["main_navigation"] = target_page

    if st.session_state.get("main_navigation") not in nav_items:
        st.session_state["main_navigation"] = T["overview"]

    page = st.radio(
        "NAVIGATION",
        nav_items,
        index=nav_items.index(st.session_state["main_navigation"]),
        key="main_navigation",
        label_visibility="collapsed"
    )

    st.divider()

    if st.button(
        "↩ " + T["logout"],
        use_container_width=True
    ):
        st.session_state.user = None
        st.rerun()

    st.caption("Prototype v2.0")


results = get_user_results(user["id"])

score_values = [
    round(r["score"] / max(r["total"], 1) * 100)
    for r in results
]

avg_score = (
    round(sum(score_values) / len(score_values), 1)
    if score_values else 0
)


# =====================================================
# REUSABLE PLOT STYLE
# =====================================================

def style_chart(fig):
    fig.update_layout(
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(
            family="Inter",
            color="#EAF4FF"
        ),
        title_font=dict(
            color="#FFFFFF",
            size=17
        ),
        margin=dict(l=15, r=15, t=55, b=15),
        xaxis=dict(
            gridcolor="rgba(160,190,230,.22)",
            zerolinecolor="rgba(160,190,230,.28)"
        ),
        yaxis=dict(
            gridcolor="rgba(160,190,230,.22)",
            zerolinecolor="rgba(160,190,230,.28)"
        )
    )
    return fig
# =====================================================
# HEALTH POWER AI
# =====================================================
if page == T["health"]:
    render_health_power(
        st,
        student_id=str(user["id"])
    )

 
# =====================================================
# MIND POWER DASHBOARD
# =====================================================
if page == T["mind"]:
    render_mind_power()


# =====================================================
# PREMIUM HOME DASHBOARD
# FUTURE LEARNING HUB
# =====================================================

if page == T["overview"]:

    st.markdown("""
    <style>
    .home-hero {
        background:
        radial-gradient(circle at 15% 50%,
        rgba(36,194,255,.30),transparent 30%),
        linear-gradient(115deg,#07152F 0%,#102B55 52%,#211D43 100%);
        border:1px solid rgba(72,229,255,.55);
        border-radius:22px;
        padding:28px;
        min-height:205px;
        box-shadow:0 14px 38px rgba(0,0,0,.34),0 0 24px rgba(22,141,255,.12);
        position:relative;
        overflow:hidden;
    }

    .home-hero h1 {
        color:#FFFFFF !important;
        font-size:clamp(25px,3vw,38px);
        font-weight:850;
        margin:12px 0 5px;
    }

    .home-hero p {
        color:#DCEEFF !important;
        font-size:16px;
        margin:5px 0;
    }

    .hero-label {
        display:inline-block;
        background:rgba(0,180,255,.15);
        color:#00d4ff;
        padding:7px 15px;
        border-radius:30px;
        font-weight:800;
        font-size:13px;
    }

    .hero-art {
        position:absolute;
        right:25px;
        top:25px;
        font-size:95px;
        filter:drop-shadow(0 8px 12px rgba(80,80,200,.2));
    }

    .home-section {
        color:#FFFFFF;
        font-size:21px;
        font-weight:800;
        margin:8px 0 13px;
    }
    .quick-card {
    background:rgba(5,20,55,.90)!important;

    border:1px solid #00BFFF!important;

    color:white!important;

    border-radius:18px;

    box-shadow:
    0 0 15px rgba(0,191,255,.25);
    }

    .quick-card:hover {
        transform:translateY(-3px);
        box-shadow:0 8px 20px rgba(90,100,180,.15);
    }

    .quick-icon {
        font-size:30px;
        margin-bottom:8px;
    }

    .quick-title {
        color:#FFFFFF;
        font-weight:800;
        font-size:15px;
    }

    .quick-sub {
        color:#C6DDF7;
        font-size:12px;
    }

    .focus-item {
        background:linear-gradient(105deg,rgba(8,31,68,.96),rgba(24,37,82,.96));
        border-radius:12px;
        padding:10px 13px;
        margin:8px 0;
        color:#EAF4FF;
        border:1px solid rgba(72,229,255,.32);
    }

   .remember-card {
    background:
        linear-gradient(
        135deg,
        #071B3A,
        #101D4A
        ) !important;

    border:1px solid #00BFFF!important;
    }

    .remember-card h3 {
        color:#FFFFFF;
        font-size:18px;
    }

    .remember-card p {
        color:#DCEBFF;
        font-size:17px;
        font-weight:700;
    } 
    /* =====================================
   AB SCHOOL LOOP AI - TEXT VISIBILITY
   ===================================== */

/* HERO SECTION */
.hero, .mind-banner {
    background: rgba(3, 15, 48, 0.88) !important;
    border: 1px solid #168DFF !important;
    box-shadow: 0 0 22px rgba(0, 140, 255, 0.35) !important;
}

.hero h1, .mind-banner h1,
.hero p, .mind-banner p,
.hero span, .mind-banner span {
    color: #FFFFFF !important;
}

/* ALL MAIN TEXT */
[data-testid="stMain"] p,
[data-testid="stMain"] label,
[data-testid="stMain"] li,
[data-testid="stMain"] span {
    color: #EAF4FF;
}

/* SECTION HEADINGS */
.section-title,
.kicker,
.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3 {
    color: #FFFFFF !important;
    text-shadow: 0 0 10px rgba(0, 160, 255, 0.4);
}

/* METRIC CARDS */
[data-testid="stMetric"] {
    background: rgba(3, 18, 52, 0.92) !important;
    border: 1px solid #168DFF !important;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricValue"],
[data-testid="stMetricDelta"] {
    color: #FFFFFF !important;
}

/* PROGRESS AND FOCUS CARDS */
.tip-card,
.activity-card,
.small-note {
    background: rgba(4, 20, 55, 0.92) !important;
    color: #FFFFFF !important;
    border: 1px solid #168DFF !important;
}

.tip-card *,
.activity-card *,
.small-note * {
    color: #FFFFFF !important;
}

/* CONTAINERS */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(3, 15, 45, 0.88) !important;
    border: 1px solid rgba(0, 170, 255, 0.7) !important;
}

/* INPUT TEXT */
.stTextInput input,
.stTextArea textarea {
    color: #FFFFFF !important;
}
    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------
    # HERO BANNER
    # -------------------------------------------------
    st.markdown(f"""
    <div class="home-hero">
    <div class="hero-label">
        🎓 WELCOME BACK, {user['full_name'].upper()}!
    </div>
    <h1>AB SCHOOL LOOP AI</h1>
    <h2 style="
        color:#3978ee;
        font-size:25px;
        font-weight:850;
        margin:5px 0;">
        Learn &nbsp; • &nbsp;
        <span style="color:#08a9d9;">Grow</span>
        &nbsp; • &nbsp;
        <span style="color:#9250ed;">Thrive</span>
    </h2>
    <p>Your Smart Learning Partner for a Brighter Future ✨</p>
    <p style="font-size:13px;">
        STUDENT GROWTH · SMART LEARNING · MIND POWER
    </p>
    <div class="hero-art">
        <img src="data:image/png;base64,{logo_base64}" style="width:280px; height:auto; border-radius:120px;">
    </div>
</div>
""", unsafe_allow_html=True)

    # -------------------------------------------------
    # DASHBOARD METRICS
    # -------------------------------------------------

    total_attempts = len(results)

    total_correct = sum(
        r["score"] for r in results
    )

    total_questions = sum(
        r["total"] for r in results
    )

    learning_score = (
        round(total_correct / total_questions * 100)
        if total_questions else 0
    )

    brain_energy = user.get("energy") or "Ready"

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "🎯 Learning Score",
            f"{learning_score}%" if results else "—"
        )

    with m2:
        st.metric(
            "⚡ Brain Energy",
            brain_energy
        )

    with m3:
        st.metric(
            "🏆 Quiz Attempts",
            total_attempts
        )

    with m4:
        st.metric(
            "⭐ Growth Points",
            total_attempts * 10
        )

    st.write("")

    # -------------------------------------------------
    # PROGRESS GRAPH
    # -------------------------------------------------

    left, right = st.columns([1.08, 1])

    with left:

        with st.container(border=True):

            st.markdown(
                '<div class="home-section">'
                '📊 Your Learning Progress'
                '</div>',
                unsafe_allow_html=True
            )

            if results:

                graph_data = list(reversed(results))

                graph_df = pd.DataFrame({
                    "Attempt": [
                        f"Test {i+1}"
                        for i in range(len(graph_data))
                    ],
                    "Score": [
                        round(
                            r["score"] /
                            max(r["total"], 1) * 100
                        )
                        for r in graph_data
                    ]
                })

                fig = px.area(
                    graph_df,
                    x="Attempt",
                    y="Score",
                    range_y=[0, 100],
                    markers=True
                )

                fig.update_traces(
                    line=dict(
                        color="#438cf7",
                        width=3
                    ),
                    fillcolor="rgba(67,140,247,.20)",
                    marker=dict(
                        color="#9250ed",
                        size=8
                    )
                )

                fig.update_layout(
                    height=280,
                    showlegend=False,
                    yaxis_title="Score (%)",
                    xaxis_title="",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=5,r=10,t=20,b=5),
                    font=dict(color="#EAF4FF"),
                    yaxis=dict(
                        range=[0,100],
                        gridcolor="rgba(160,190,230,.22)"
                    ),
                    xaxis=dict(
                        gridcolor="rgba(160,190,230,.22)"
                    )
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:

                st.info(
                    "Complete your first quiz to see "
                    "your learning progress here."
                )

    # -------------------------------------------------
    # TODAY'S FOCUS
    # -------------------------------------------------

    with right:

        with st.container(border=True):

            st.markdown(
                '<div class="home-section">'
                '💡 Today’s Focus'
                '</div>',
                unsafe_allow_html=True
            )

            focus_tasks = [
                "Revise one difficult subject",
                "Attempt 10 practice questions",
                "Complete one Mind Power activity",
                "Stay positive and focused"
            ]

            for i, task in enumerate(focus_tasks):

                st.markdown(
                    '<div class="focus-item">'
                    '✨ &nbsp; ' + task +
                    '</div>',
                    unsafe_allow_html=True
                )

            st.caption(
                "Small steps every day create progress."
            )

    st.write("")

    # -------------------------------------------------
    # QUICK ACCESS
    # -------------------------------------------------

    st.markdown(
        '<div class="home-section">'
        '🚀 Quick Access'
        '</div>',
        unsafe_allow_html=True
    )

    q1, q2, q3, q4 = st.columns(4)
    quick_items = [
    (q1,"🧠","Mind Power","Brain Games & Focus",T["mind"],"#071B3A"),
    (q2,"🧩","AI Quiz","Practice & Test",T["quiz"],"#071B3A"),
    (q3,"😊","AI Coach","Get Guidance",T["coach"],"#071B3A"),
    (q4,"📊","Analytics","Track Progress",T["analytics"],"#071B3A"),
]

    for col, icon, title, subtitle, target_page, color in quick_items:
        with col:
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div class="quick-card" style="background:{color};">
                        <div class="quick-icon">{icon}</div>
                        <div class="quick-title">{title}</div>
                        <div class="quick-sub">{subtitle}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.button(
                    f"Open {title} →",
                    key=f"quick_access_{title.lower().replace(' ', '_')}",
                    use_container_width=True,
                    on_click=navigate_to,
                    args=(target_page,)
                )

    st.write("")

    # -------------------------------------------------
    # BOTTOM REMEMBER SECTION
    # -------------------------------------------------

    r1, r2 = st.columns([2.5, 1])

    with r1:

        with st.container(border=True):

            st.markdown(
                "### 🌟 Your Growth Journey"
            )

            st.write(
                "Learn something new. Practise consistently. "
                "Reflect on your progress. Keep improving."
            )

            st.progress(
                min(learning_score / 100, 1.0)
            )

            st.caption(
                f"Your current quiz accuracy: "
                f"{learning_score}%"
                if results else
                "Your progress will appear after your first quiz."
            )

    with r2:

        st.markdown("""
        <div class="remember-card">
            <h3>⭐ Remember</h3>
            <p>Dream Big.<br>Study Smart!</p>
            <div style="
                text-align:right;
                font-size:25px;
                color:#7654e8;">
                ♡
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        AB SCHOOL LOOP AI <br>
        LEARN → GROW → THRIVE
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# LEARNING DASHBOARD
# =====================================================

if page == T["learning"]:
    st.markdown(
        '<div class="kicker">02 / LEARNING INTELLIGENCE</div>'
        '<div class="section-title">Learning Dashboard</div>',
        unsafe_allow_html=True
    )
    st.caption(
        "Enter a recent score for each subject."
    )
    subjects = [
        "Physics", "Chemistry",
        "Mathematics", "English"
    ]

    cols = st.columns(4)
    entered = {}

    for col, subject in zip(cols, subjects):

        with col:
            with st.container(border=True):
                entered[subject] = st.slider(
                    subject,
                    0, 100, 65,
                    key=f"learning_{subject}"
                )

                status = (
                    "Needs support"
                    if entered[subject] < 50
                    else "Growing"
                    if entered[subject] < 75
                    else "Strong"
                )

                st.caption(status)

    if st.button(
        "✨ Build My Learning Plan",
        type="primary",
        use_container_width=True
    ):
        st.session_state.practice_plan = entered

    if "practice_plan" in st.session_state:

        plan = st.session_state.practice_plan

        df = pd.DataFrame([
            {
                "Subject": s,
                "Score": v,
                "Status": (
                    "Needs support" if v < 50
                    else "Growing" if v < 75
                    else "Strong"
                ),
                "Next Step": (
                    "Revise core concepts + guided practice"
                    if v < 50
                    else "Revise key concepts + mixed questions"
                    if v < 75
                    else "Spaced revision + challenge questions"
                )
            }
            for s, v in plan.items()
        ])

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        fig = px.bar(
            df,
            x="Subject",
            y="Score",
            color="Status",
            range_y=[0, 100],
            color_discrete_map={
                "Needs support": "#ed7292",
                "Growing": "#f2bb57",
                "Strong": "#24b88a"
            },
            title="Subject Performance"
        )

        style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

        st.download_button(
            "Download Practice Plan CSV",
            df.to_csv(index=False).encode("utf-8-sig"),
            "practice_plan.csv",
            "text/csv"
        )

 
    
  
# =====================================================
# AI QUIZ GENERATOR
# =====================================================

elif page == T["quiz"]:

    st.markdown(
        '<div class="kicker">03 / ACTIVE RECALL LAB</div>'
        '<div class="section-title">AI Quiz Generator</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Selects questions from the built-in question bank."
    )

    s1, s2 = st.columns(2)

    with s1:
        subject = st.selectbox(
            "Subject", list(QUIZ_BANK.keys())
        )

    with s2:
        topic = st.selectbox(
            "Topic", list(QUIZ_BANK[subject].keys())
        )

    if st.button(
        "⚡ Generate Quiz",
        type="primary"
    ):
        st.session_state.active_quiz = {
            "subject": subject,
            "topic": topic,
            "questions": QUIZ_BANK[subject][topic]
        }

    quiz = st.session_state.get("active_quiz")

    if quiz:

        st.markdown(
            f"### {quiz['subject']} · {quiz['topic']}"
        )

        with st.form("quiz_attempt_form"):

            answers = []

            for i, item in enumerate(quiz["questions"]):

                question, options, correct, explanation = item

                st.markdown(
                    f"**Q{i+1}. {question}**"
                )

                answers.append(
                    st.radio(
                        "Choose your answer",
                        options,
                        key=f"quiz_{quiz['subject']}_{quiz['topic']}_{i}",
                        index=None
                    )
                )

            submitted = st.form_submit_button(
                "Submit Answers",
                type="primary",
                use_container_width=True
            )

        if submitted:

            if any(a is None for a in answers):

                st.warning(
                    "Please answer every question."
                )

            else:

                correct_count = sum(
                    1 for a, q in zip(
                        answers, quiz["questions"]
                    )
                    if a == q[1][q[2]]
                )

                save_result(
                    user["id"],
                    quiz["subject"],
                    quiz["topic"],
                    correct_count,
                    len(answers)
                )

                st.session_state.last_quiz_review = [
                    (q[0], a, q[1][q[2]], q[3])
                    for a, q in zip(
                        answers, quiz["questions"]
                    )
                ]

                st.session_state.pop("active_quiz", None)

                st.success(
                    f"Score: {correct_count}/{len(answers)} "
                    f"({round(correct_count/len(answers)*100)}%)"
                )

                st.rerun()

    if st.session_state.get("last_quiz_review"):

        with st.expander(
            "Review Latest Answers",
            expanded=True
        ):

            for q, a, correct, why in (
                st.session_state.last_quiz_review
            ):
                st.markdown(f"**{q}**")
                st.write(
                    f"Your answer: {a} · Correct: {correct}"
                )
                st.caption(why)



# =====================================================
# ADVANCED AI COACH - GOOGLE GEMINI AI
# =====================================================

elif page == T["coach"]:

    st.markdown(
        '<div class="kicker">04 / PERSONAL AI LEARNING COACH</div>'
        '<div class="section-title">🤖 Advanced AI Coach</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Powered by Google Gemini AI · Your Personal Study Assistant"
    )

    # Get API key
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.error("Gemini API Key not found. Please configure your API key.")
        st.stop()

    # Create separate chat for each logged-in user
    if (
        "ai_chat" not in st.session_state
        or st.session_state.get("ai_chat_user") != user["id"]
    ):
        try:
            st.session_state.ai_chat = create_ai_chat(api_key)
            st.session_state.ai_chat_user = user["id"]
            st.session_state.ai_messages = []

        except Exception as e:
            st.error(f"AI Coach connection error: {e}")
            st.stop()

    # Chat controls
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("### 🎓 Hello, " + user["full_name"] + "!")

    with col2:
        if st.button("🗑️ Clear Chat"):
            st.session_state.ai_chat = create_ai_chat(api_key)
            st.session_state.ai_messages = []
            st.rerun()

    st.info(
        "Ask me anything about Maths, Science, English, "
        "homework, exams or study planning!"
    )

    # Display previous messages
    for message in st.session_state.ai_messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Student input
    question = st.chat_input(
        "💬 Ask your AI Coach anything..."
    )

    if question:

        # Display student message
        st.session_state.ai_messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        # Gemini response
        with st.chat_message("assistant"):

            with st.spinner("🤖 AI Coach is thinking..."):

                try:
                    response = st.session_state.ai_chat.send_message(
                        question
                    )

                    answer = response.text or "Please try again."

                    st.markdown(answer)

                    st.session_state.ai_messages.append({
                        "role": "assistant",
                        "content": answer
                    })

                except Exception as e:
                    st.error(f"AI Coach Error: {e}")

    st.divider()

    st.caption(
        "🌟 AB SCHOOL LOOP AI | Learn • Grow • Thrive"
    )

# =====================================================
# PERFORMANCE ANALYTICS
# =====================================================
elif page == T["analytics"]:

    st.markdown(
        '<div class="kicker">05 / PERFORMANCE INTELLIGENCE</div>'
        '<div class="section-title">Performance Analytics</div>',
        unsafe_allow_html=True
    )

    if results:

        df = pd.DataFrame(results)

        df["Score (%)"] = (
            df["score"] / df["total"] * 100
        ).round(1)

        a, b, c = st.columns(3)

        a.metric("Attempts", len(df))
        b.metric(
            "Average",
            f"{df['Score (%)'].mean():.1f}%"
        )
        c.metric(
            "Best Score",
            f"{df['Score (%)'].max():.1f}%"
        )

        df["Attempt"] = range(1, len(df) + 1)

        fig = px.line(
            df.sort_values("id"),
            x="Attempt",
            y="Score (%)",
            markers=True,
            range_y=[0, 100],
            title="Quiz Score Trend"
        )

        fig.update_traces(
            line_color="#438cf7",
            marker_color="#9250ed"
        )

        style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

        by_subject = df.groupby(
            "subject", as_index=False
        )["Score (%)"].mean()

        fig2 = px.bar(
            by_subject,
            x="subject",
            y="Score (%)",
            title="Average by Subject",
            range_y=[0, 100]
        )

        fig2.update_traces(
            marker_color="#8c69e8"
        )

        style_chart(fig2)
        st.plotly_chart(fig2, use_container_width=True)

        st.dataframe(
            df[
                [
                    "subject", "topic",
                    "score", "total",
                    "Score (%)", "created_at"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info(
            "Complete your first quiz to unlock analytics."
        )


# =====================================================
# TEACHER DASHBOARD
# =====================================================

elif is_teacher and page == T["teacher_dash"]:

    st.markdown(
        '<div class="kicker">06 / TEACHER CONTROL ROOM</div>'
        '<div class="section-title">Teacher Dashboard</div>',
        unsafe_allow_html=True
    )

    with db() as conn:

        students = [
            dict(r) for r in conn.execute("""
            SELECT id,full_name,username,grade,goal,created_at
            FROM users
            WHERE role='Student'
            ORDER BY full_name
            """).fetchall()
        ]

    all_results = get_user_results()

    a, b, c = st.columns(3)

    a.metric("Registered Students", len(students))
    b.metric("Quiz Attempts", len(all_results))

    average = (
        sum(
            r["score"] / max(r["total"], 1) * 100
            for r in all_results
        ) / len(all_results)
        if all_results else 0
    )

    c.metric("Average Score", f"{average:.1f}%")

    st.markdown("### Student Directory")

    if students:

        st.dataframe(
            pd.DataFrame(students)[
                [
                    "full_name",
                    "username",
                    "grade",
                    "goal",
                    "created_at"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No student accounts yet.")

    st.markdown("### Recent Quiz Activity")

    if all_results:

        rdf = pd.DataFrame(all_results)

        rdf["Score (%)"] = (
            rdf["score"] / rdf["total"] * 100
        ).round(1)

        st.dataframe(
            rdf[
                [
                    "full_name",
                    "grade",
                    "subject",
                    "topic",
                    "Score (%)",
                    "created_at"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Class Activity CSV",
            rdf.to_csv(index=False).encode("utf-8-sig"),
            "teacher_activity.csv",
            "text/csv"
        )

    else:
        st.info("Quiz activity will appear here.")


# =====================================================
# VALUES & REFLECTION
# =====================================================

elif page == T["values"]:

    st.markdown(
        '<div class="kicker">07 / PERSONAL GROWTH</div>'
        '<div class="section-title">Values & Reflection</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Reflect on learning, honesty, kindness and improvement."
    )

    prompts = [
        "What did I learn today?",
        "Where did I show patience or honesty?",
        "Who did I help or thank today?",
        "What is one small improvement for tomorrow?"
    ]

    with st.form("reflection_form"):

        answers = [
            st.text_area(
                prompt,
                max_chars=300,
                key=f"reflection_{i}"
            )
            for i, prompt in enumerate(prompts)
        ]

        submitted = st.form_submit_button(
            "Save Reflection",
            type="primary"
        )

    if submitted:

        combined = "\n".join(
            f"{p} {a.strip()}"
            for p, a in zip(prompts, answers)
            if a.strip()
        )

        if combined:
            save_reflection(user["id"], combined)
            st.success("Reflection saved successfully.")

        else:
            st.warning("Write at least one reflection.")


# =====================================================
# TRANSPARENT PROTOTYPE
# =====================================================

elif page == T["transparent"]:

    st.markdown(
        '<div class="kicker">08 / RESPONSIBLE DESIGN</div>'
        '<div class="section-title">Transparent Prototype</div>',
        unsafe_allow_html=True
    )

    st.warning(
        "This is a rule-based educational prototype, "
        "not a trained machine-learning model."
    )

    rules = pd.DataFrame([
        (
            "0–49%",
            "Needs support",
            "Core revision and guided practice"
        ),
        (
            "50–74%",
            "Growing",
            "Concept revision and mixed practice"
        ),
        (
            "75–100%",
            "Strong",
            "Spaced revision and challenge questions"
        )
    ], columns=[
        "Score Range",
        "Status",
        "Suggested Next Step"
    ])

    st.dataframe(
        rules,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### What the Prototype Does")

    st.write("""
    - Stores local demo accounts in SQLite.
    - Uses a built-in question bank.
    - Checks quiz answers automatically.
    - Displays progress charts.
    - Provides rule-based coaching prompts.
    - Supports teacher and student views.
    - Does not diagnose health or measure intelligence.
    """)


# =====================================================
# PROJECT SHOWCASE
# =====================================================

elif page == T["showcase"]:

    st.markdown(
        '<div class="kicker">09 / PROJECT PRESENTATION</div>'
        '<div class="section-title">Project Showcase</div>',
        unsafe_allow_html=True
    )

    st.markdown("### Problem Statement")

    st.write(
        "Students may find it difficult to decide what "
        "to practise next while balancing academic "
        "learning and everyday routines."
    )

    st.markdown("### Proposed Solution")

    st.write(
        "AB SCHOOL LOOP AI combines student learning, "
        "quiz generation, transparent coaching, reflection, "
        "teacher overview and performance analytics."
    )

    st.markdown("### System Architecture")

    st.code(
        "Student / Teacher → Login → Learning Inputs → "
        "Quiz / Rule Engine → Analytics → Reflection → "
        "Next Practice",
        language="text"
    )

    st.markdown("### Technology Stack")

    st.write(
        "Python · Streamlit · SQLite · Pandas · "
        "Plotly · ReportLab"
    )

    modules = st.columns(3)

    for col, icon, title, desc in zip(
        modules,
        ["🔐", "🧠", "📊"],
        ["Access", "Learning", "Insights"],
        [
            "Local login and role-based views.",
            "Question bank and coaching prompts.",
            "Progress charts and teacher activity."
        ]
    ):

        with col:
            with st.container(border=True):
                st.markdown(f"### {icon} {title}")
                st.write(desc)


# =====================================================
# ROADMAP & TEAM
# =====================================================

elif page == T["roadmap"]:

    st.markdown(
        '<div class="kicker">10 / EXECUTION PLAN</div>'
        '<div class="section-title">Roadmap & Team</div>',
        unsafe_allow_html=True
    )

    roadmap = pd.DataFrame([
        ("Week 1", 1, "Research and baseline assessment"),
        ("Week 2", 2, "UI and student registration"),
        ("Week 3", 3, "Quiz bank and coaching rules"),
        ("Week 4", 4, "Analytics and teacher dashboard"),
        ("Week 5", 5, "Testing and feedback"),
        ("Week 6", 6, "Final validation and presentation")
    ], columns=["Timeline", "Week", "Milestone"])

    st.dataframe(
        roadmap[["Timeline", "Milestone"]],
        use_container_width=True,
        hide_index=True
    )

    fig = px.bar(
        roadmap,
        x="Week",
        y="Timeline",
        orientation="h",
        color="Week",
        title="Six-Week Project Roadmap"
    )

    style_chart(fig)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Team Responsibilities")

    team = pd.DataFrame([
        ("Student 1", "Research and evaluation"),
        ("Student 2", "UI/UX and presentation"),
        ("Student 3", "Python and database"),
        ("Student 4", "Testing and documentation")
    ], columns=["Role", "Responsibility"])

    st.dataframe(
        team,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.markdown("### 📘 Marks-Based Study Assistant")

    subjects = [
        "Physics", "Chemistry",
        "Mathematics", "English"
    ]

    cols = st.columns(4)
    marks = {}

    for col, subject in zip(cols, subjects):

        with col:
            marks[subject] = st.number_input(
                subject,
                min_value=0,
                max_value=100,
                value=60,
                step=1,
                key=f"roadmap_{subject}"
            )

    if st.button(
        "Generate My Improvement Roadmap",
        type="primary",
        use_container_width=True
    ):

        weakest = min(marks, key=marks.get)
        average = sum(marks.values()) / len(marks)

        st.metric("Current Average", f"{average:.1f}%")

        st.success(
            f"Priority Subject: {weakest} "
            f"({marks[weakest]}%)"
        )

        advice = []

        for subject, mark in marks.items():

            if mark < 50:
                level = "Foundation Focus"
                next_step = (
                    "Revise definitions and worked examples; "
                    "solve 5 basic questions."
                )

            elif mark < 75:
                level = "Build Consistency"
                next_step = (
                    "Revise concepts and solve 8 mixed questions."
                )

            else:
                level = "Strengthen Mastery"
                next_step = (
                    "Use spaced revision and challenging questions."
                )

            advice.append(
                (subject, mark, level, next_step)
            )

        advice_df = pd.DataFrame(
            advice,
            columns=[
                "Subject",
                "Marks",
                "Level",
                "Recommended Next Steps"
            ]
        )

        st.dataframe(
            advice_df,
            use_container_width=True,
            hide_index=True
        )

        fig = px.bar(
            advice_df,
            x="Subject",
            y="Marks",
            color="Level",
            range_y=[0, 100],
            title="Subject-Wise Marks"
        )

        style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Your Next 7-Day Action Plan")

        st.write(
            f"1. **Day 1–2:** Focus on {weakest}."
        )
        st.write(
            "2. **Day 3–4:** Practise all four subjects."
        )
        st.write(
            "3. **Day 5:** Review incorrect questions."
        )
        st.write(
            "4. **Day 6:** Take a short self-test."
        )
        st.write(
            "5. **Day 7:** Compare progress and set targets."
        )


# =====================================================
# JUDGE Q&A
# =====================================================

elif page == T["judge"]:

    st.markdown(
        '<div class="kicker">11 / PRESENTATION PREPARATION</div>'
        '<div class="section-title">Judge Questions & Answers</div>',
        unsafe_allow_html=True
    )

    qa = [
        (
            "What problem does your project solve?",
            "It helps students turn quiz results into "
            "clear next practice steps."
        ),
        (
            "Is this a real AI model?",
            "The current version is a transparent "
            "rule-based prototype, not a trained ML model."
        ),
        (
            "How does the quiz generator work?",
            "It selects questions from a reviewed "
            "subject and topic question bank."
        ),
        (
            "How is student progress shown?",
            "Quiz attempts are stored locally and "
            "displayed through score trends."
        ),
        (
            "How is student information handled?",
            "The demo stores information in a local "
            "SQLite database."
        ),
        (
            "What can be improved next?",
            "Curriculum-aligned question banks, "
            "stronger security and evaluated ML features."
        )
    ]

    for question, answer in qa:

        with st.expander(question):
            st.write(answer)


# =====================================================
# PROFILE + PDF REPORT
# =====================================================

st.divider()

with st.expander(
    "👤 Profile & PDF Report",
    expanded=False
):

    st.write(
        f"**Name:** {user['full_name']}  ·  "
        f"**Role:** {user['role']}  ·  "
        f"**Class:** {user['grade'] or '—'}"
    )

    if PDF_AVAILABLE:

        pdf_data = make_pdf(user, results)

        st.download_button(
            "📄 " + T["download"],
            pdf_data,
            "AB_SCHOOL_LOOP_AI_Report.pdf",
            "application/pdf",
            type="primary"
        )

    else:

        st.warning(
            "PDF library not installed. "
            "Run: pip install reportlab"
        )

    st.caption(
        "PDF report uses English text with ReportLab "
        "built-in fonts."
    )


# =====================================================
# FOOTER
# =====================================================
st.markdown("""
<div class="footer" style="text-align: center;">
    AB SCHOOL LOOP AI <br>
    Student Learning Support Prototype<br>
    Learn → Recall → Reflect → Improve
</div>
""", unsafe_allow_html=True)
