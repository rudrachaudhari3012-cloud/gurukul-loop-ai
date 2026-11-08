
import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import hashlib
import secrets
import io
from datetime import date, datetime

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

APP_TITLE = "AB SCHOOL LOOP AI"
DB_PATH = "ab_school_loop_ai.db"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# PREMIUM LIGHT MIND POWER THEME
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Manrope:wght@500;600;700;800&display=swap');

:root {
    --navy: #101d3b;
    --blue: #3679f6;
    --sky: #6bc9ff;
    --purple: #9250ed;
    --lavender: #eee6ff;
    --mint: #d7f8e9;
    --ink: #101b42;
    --muted: #63718f;
}

.stApp {
    background:
      radial-gradient(ellipse at 75% 5%, #dce9ff 0%, transparent 35%),
      linear-gradient(135deg,#f1f5ff,#ffffff 55%,#f3edff);
    color: var(--ink);
    font-family: Inter, sans-serif;
}

.block-container {
    max-width: 1600px;
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

[data-testid="stHeader"] {
    background: rgba(240,245,255,.75);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#101d3b,#0c1934 75%,#13264a);
    border-right: 1px solid rgba(100,170,255,.25);
}

[data-testid="stSidebar"] * {
    color: #f4f7ff !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: rgba(255,255,255,.035);
    border-radius: 10px;
    padding: 7px 10px;
    margin-bottom: 5px;
    transition: .2s;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(85,170,255,.22);
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(100deg,#9948f5,#397cf6);
    box-shadow: 0 4px 18px rgba(120,80,255,.35);
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,.13);
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 30px;
    border-radius: 24px;
    border: 1px solid #d8e3ff;
    background: linear-gradient(110deg,#dce7ff,#e9e7ff 52%,#d7eaff);
    box-shadow: 0 12px 35px rgba(75,100,170,.12);
    margin-bottom: 18px;
}

.hero:after {
    content: "✦";
    position: absolute;
    right: 35px;
    top: -40px;
    font-size: 190px;
    color: rgba(105,120,240,.10);
}

.hero h1 {
    color: #101b42 !important;
    font-family: Manrope,sans-serif;
    font-size: clamp(2rem,4vw,3rem);
    font-weight: 800;
    margin: 10px 0;
}

.hero p {
    color: #263a70 !important;
    font-size: 1.05rem;
}

.eyebrow {
    color: #7544db;
    font-weight: 800;
    letter-spacing: 2px;
    font-size: .75rem;
}

.mind-banner {
    background: linear-gradient(110deg,#d7e3ff,#eee4ff,#d5edff);
    padding: 24px;
    border: 1px solid #d9e1ff;
    border-radius: 22px;
    box-shadow: 0 9px 28px rgba(70,100,180,.12);
    margin-bottom: 16px;
}

.mind-banner h1 {
    color: #101b42;
    font-family: Manrope,sans-serif;
    font-size: clamp(1.8rem,3.4vw,2.8rem);
    font-weight: 800;
    margin: 8px 0;
}

.mind-banner p {
    color: #293e75;
    font-size: 1rem;
}

.section-title {
    color: #101b42;
    font-family: Manrope,sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    margin: 10px 0;
}

.kicker {
    color: #7950db;
    font-size: .72rem;
    letter-spacing: 2px;
    font-weight: 800;
    text-transform: uppercase;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg,#ffffff,#f2f5ff);
    border: 1px solid #e0e6fb;
    border-radius: 17px;
    padding: 17px;
    box-shadow: 0 5px 17px rgba(80,100,170,.09);
}

[data-testid="stMetricLabel"] {
    color: #45557e !important;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #101b42 !important;
    font-weight: 800;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,.90);
    border: 1px solid #e2e8fb;
    border-radius: 17px;
    box-shadow: 0 5px 18px rgba(90,110,180,.07);
}

.stButton > button,
.stDownloadButton > button,
[data-testid="stFormSubmitButton"] > button {
    border: 1px solid #8ca9ff;
    border-radius: 12px;
    background: linear-gradient(100deg,#9250ed,#438cf7);
    color: white !important;
    font-weight: 750;
    min-height: 2.65rem;
    transition: .2s;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: #ffffff;
    filter: brightness(1.08);
    box-shadow: 0 5px 18px rgba(110,90,220,.24);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: #e9edfb;
    padding: 7px;
    border-radius: 13px;
}

.stTabs [aria-selected="true"] {
    background: white !important;
    color: #7544db !important;
}

[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
.stMarkdown,
.stMarkdown p,
label {
    color: #17264d;
}

input, textarea,
[data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #15244a !important;
    border-color: #cbd8f5 !important;
    border-radius: 10px !important;
}

input::placeholder, textarea::placeholder {
    color: #7b87a4 !important;
}

[data-testid="stAlert"] {
    border-radius: 13px;
}

[data-testid="stAlert"] p {
    color: #17264d !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid #dce4fa;
    border-radius: 12px;
    overflow: hidden;
}

hr {
    border-color: #dce4f5;
}

.tip-card {
    background: linear-gradient(110deg,#f1edff,#edf2ff);
    padding: 13px 15px;
    border-radius: 13px;
    border: 1px solid #e1ddff;
    margin: 8px 0;
    color: #1a2a55;
}

.activity-card {
    padding: 17px;
    border-radius: 16px;
    min-height: 100px;
    border: 1px solid rgba(120,140,200,.14);
    box-shadow: 0 4px 12px rgba(80,100,160,.06);
}

.footer {
    text-align: center;
    color: #71809f;
    font-size: .78rem;
    padding: 22px 0 5px;
}

.small-note {
    border-left: 4px solid #8b5cf6;
    background: #f0edff;
    padding: 12px;
    border-radius: 0 10px 10px 0;
    color: #26365e;
}

</style>
""", unsafe_allow_html=True)

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

    st.markdown(f"""
    <div class="hero">
        <div class="eyebrow">STUDENT GROWTH · LEARNING SCIENCE</div>
        <h1>🎓 AB SCHOOL LOOP AI</h1>
        <p>{T['tagline']}<br>{T['intro']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Welcome to your learning studio")

    login_tab, register_tab = st.tabs([
        "🔐 " + T["login"],
        "✨ " + T["register"]
    ])

    with login_tab:
        with st.form("login_form"):
            login_user = st.text_input(T["username"])
            login_pass = st.text_input(
                T["password"], type="password"
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
                st.error(
                    "Incorrect username or password."
                )

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
                    "Class 8", "Class 9", "Class 10",
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
            MIDNIGHT AI · Learning Studio
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

    nav_items = [
        T["overview"],
        T["learning"],
        T["quiz"],
        T["Mind Power"],
        T["coach"],
        T["analytics"],
    ]

    if is_teacher:
        nav_items.insert(6, T["teacher_dash"])

    page = st.radio(
        "NAVIGATION",
        nav_items,
        label_visibility="collapsed"
    )

    st.divider()

    if st.button(
        "↩ " + T["logout"],
        use_container_width=True
    ):
        st.session_state.user = None
        st.rerun()

    st.caption("Prototype v2.0 · Mind Power Edition")


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
            color="#24345f"
        ),
        title_font=dict(
            color="#101b42",
            size=17
        ),
        margin=dict(l=15, r=15, t=55, b=15),
        xaxis=dict(
            gridcolor="#e5eafa",
            zerolinecolor="#e5eafa"
        ),
        yaxis=dict(
            gridcolor="#e5eafa",
            zerolinecolor="#e5eafa"
        )
    )
    return fig

# =====================================================
# MIND POWER DASHBOARD
# =====================================================

if page == T["mind"]:

    st.markdown("""
    <div class="mind-banner">
        <div class="eyebrow">🧠 MIND POWER · PERSONAL GROWTH</div>
        <h1>Unlock Your Mind Power</h1>
        <p>Think Better · Focus Deeper · Achieve More</p>
        <div style="font-size:14px;color:#52669a;">
            A focused mind builds a brighter future.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # MIND POWER METRICS

    focus_score = avg_score if results else 0

    energy_levels = {
        "Low": "Growing",
        "Okay": "Balanced",
        "Good": "Strong",
        "High": "High"
    }

    positive_count = 0

    with db() as conn:
        reflection_row = conn.execute(
            "SELECT COUNT(*) FROM reflections WHERE user_id=?",
            (user["id"],)
        ).fetchone()

    positive_count = reflection_row[0] if reflection_row else 0

    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "🎯 Focus Score",
        f"{focus_score}%" if results else "—"
    )

    m2.metric(
        "⚡ Brain Energy",
        energy_levels.get(user.get("energy", ""), "Ready")
    )

    m3.metric(
        "🏆 Mind Streak",
        f"{len(results)} Activities"
    )

    m4.metric(
        "⭐ Positive Thoughts",
        positive_count
    )

    st.write("")

    # PROGRESS + TIPS

    left, right = st.columns([1.08, 1])

    with left:

        with st.container(border=True):

            st.markdown(
                "### 📊 Your Mind Progress"
            )

            if results:

                progress_df = pd.DataFrame({
                    "Attempt": range(1, len(results) + 1),
                    "Focus": [
                        round(
                            r["score"] /
                            max(r["total"], 1) * 100
                        )
                        for r in reversed(results)
                    ]
                })

                fig = px.area(
                    progress_df,
                    x="Attempt",
                    y="Focus",
                    range_y=[0, 100],
                    markers=True
                )

                fig.update_traces(
                    line_color="#438cf7",
                    fillcolor="rgba(67,140,247,.20)",
                    marker_color="#9250ed"
                )

                style_chart(fig)
                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:
                st.info(
                    "Complete your first quiz to start tracking "
                    "your learning progress."
                )

    with right:

        with st.container(border=True):

            st.markdown("### 💡 Mind Power Tips")

            tips = [
                "Practice deep breathing for 2 minutes daily.",
                "Use the Pomodoro technique for focused study.",
                "Replace negative thoughts with constructive ones.",
                "Maintain a regular and healthy sleep routine."
            ]

            for tip in tips:
                st.markdown(
                    f"""
                    <div class="tip-card">
                        <span style="color:#16a34a;">✔</span>
                        &nbsp; {tip}
                    </div>
                    """,
                    unsafe_allow_html=True
           

# =====================================================
# OVERVIEW
# =====================================================

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
        linear-gradient(105deg,#d9eaff,#e9e7ff 55%,#ffe8ef);
        border:1px solid #cbdcff;
        border-radius:22px;
        padding:28px;
        min-height:205px;
        box-shadow:0 10px 30px rgba(70,100,180,.13);
        position:relative;
        overflow:hidden;
    }

    .home-hero h1 {
        color:#101b42;
        font-size:clamp(25px,3vw,38px);
        font-weight:850;
        margin:12px 0 5px;
    }

    .home-hero p {
        color:#344777;
        font-size:16px;
        margin:5px 0;
    }

    .hero-label {
        display:inline-block;
        background:rgba(255,255,255,.72);
        color:#7544db;
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
        color:#101b42;
        font-size:21px;
        font-weight:800;
        margin:8px 0 13px;
    }

    .quick-card {
        padding:17px 12px;
        border-radius:17px;
        min-height:105px;
        border:1px solid rgba(120,140,200,.18);
        transition:all .2s ease;
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
        color:#15234d;
        font-weight:800;
        font-size:15px;
    }

    .quick-sub {
        color:#53668d;
        font-size:12px;
    }

    .focus-item {
        background:linear-gradient(100deg,#f0edff,#edf3ff);
        border-radius:12px;
        padding:10px 13px;
        margin:8px 0;
        color:#18264d;
        border:1px solid #e4e8ff;
    }

    .remember-card {
        background:linear-gradient(120deg,#fff0d8,#ffe7ed);
        border:1px solid #ffe3c1;
        border-radius:18px;
        padding:20px;
        min-height:120px;
    }

    .remember-card h3 {
        color:#17264d;
        font-size:18px;
    }

    .remember-card p {
        color:#273a69;
        font-size:17px;
        font-weight:700;
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
        <div class="hero-art">🧠 ✨</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

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
                    font=dict(color="#24345f"),
                    yaxis=dict(
                        range=[0,100],
                        gridcolor="#e3eafa"
                    ),
                    xaxis=dict(
                        gridcolor="#e3eafa"
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
        (
            q1, "🧠", "Mind Power",
            "Brain Games & Focus", "#eee0ff"
        ),
        (
            q2, "🧩", "AI Quiz",
            "Practice & Test", "#d7f7e6"
        ),
        (
            q3, "😊", "AI Coach",
            "Get Guidance", "#ffefd8"
        ),
        (
            q4, "📊", "Analytics",
            "Track Progress", "#d9f5fb"
        )
    ]

    for col, icon, title, subtitle, color in quick_items:

        with col:

            with st.container(border=True):

                st.markdown(
                    f"""
                    <div class="quick-card"
                         style="background:{color};">
                        <div class="quick-icon">{icon}</div>
                        <div class="quick-title">{title}</div>
                        <div class="quick-sub">{subtitle}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
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
        AB SCHOOL LOOP AI · FUTURE LEARNING HUB<br>
        LEARN → GROW → THRIVE
    </div>
    """, unsafe_allow_html=True)




# =====================================================
# LEARNING DASHBOARD
# =====================================================

elif page == T["learning"]:

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
# ADVANCED AI COACH
# =====================================================

elif page == T["coach"]:

    st.markdown(
        '<div class="kicker">04 / PERSONAL STUDY COACH</div>'
        '<div class="section-title">Advanced AI Coach</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Transparent rule-based educational coaching."
    )

    energy = st.select_slider(
        "How is your energy right now?",
        ["Low", "Okay", "Good", "High"],
        value="Okay"
    )

    target = st.selectbox(
        "What do you want help with?",
        [
            "Understand a hard concept",
            "Remember formulas",
            "Prepare for a quiz",
            "Reduce distractions",
            "Plan a balanced study session"
        ]
    )

    context = st.text_area(
        "Topic or chapter (optional)",
        placeholder="Example: Newton's laws"
    )

    if st.button(
        "Generate My Coaching Steps",
        type="primary"
    ):

        advice = {
            "Understand a hard concept": [
                "Read one worked example slowly.",
                "Explain the concept in your own words.",
                "Solve two similar questions."
            ],
            "Remember formulas": [
                "Write the formula from memory.",
                "Check symbols and units.",
                "Apply it to two practice problems."
            ],
            "Prepare for a quiz": [
                "List three important subtopics.",
                "Attempt questions without notes.",
                "Review mistakes and retry."
            ],
            "Reduce distractions": [
                "Choose one small task.",
                "Keep notifications away during focus time.",
                "Take a short break after completing it."
            ],
            "Plan a balanced study session": [
                "Choose one 20–25 minute study block.",
                "Take a short movement and water break.",
                "Finish with a two-minute recall check."
            ]
        }

        prefix = (
            "Start with a gentle 10-minute task."
            if energy == "Low"
            else "Use one focused block, then review."
        )

        st.success(prefix)

        if context.strip():
            st.info(f"Focus topic: {context.strip()}")

        for i, step in enumerate(advice[target], 1):
            st.markdown(f"**{i}.** {step}")


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
<div class="footer">
    AB SCHOOL LOOP AI · MIND POWER EDITION<br>
    Student Learning Support Prototype<br>
    Learn → Recall → Reflect → Improve
</div>
""", unsafe_allow_html=True)
