import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import hashlib
import secrets
import io
import json
from datetime import date, datetime

# Optional PDF support: install reportlab (listed in requirements.txt).
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

APP_TITLE = "AB SCHOOL LOOP AI"
DB_PATH = "ab_school_loop_ai.db"

st.set_page_config(page_title=APP_TITLE, page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

# ---------------------------
# MIDNIGHT / CYAN / MINT THEME
# ---------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Manrope:wght@500;600;700;800&display=swap');
:root { color-scheme: dark; }
.stApp { background: radial-gradient(ellipse at 8% 0%,rgba(34,211,238,.14),transparent 32%), radial-gradient(ellipse at 94% 8%,rgba(94,234,212,.11),transparent 28%), #08111f; color:#f4f8ff; }
.block-container { max-width:1450px; padding-top:1.4rem; padding-bottom:3rem; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#0b1728,#101f34 72%,#0b1b2b); border-right:1px solid rgba(34,211,238,.22); }
[data-testid="stSidebar"] * { color:#f4f8ff !important; }
[data-testid="stHeader"] { background:rgba(8,17,31,.86); }
.hero { padding:clamp(1.5rem,4vw,3rem); border:1px solid rgba(34,211,238,.38); border-radius:26px; background:linear-gradient(120deg,#0b1424 0%,#122c49 55%,#075b63 100%); box-shadow:0 22px 65px rgba(0,0,0,.30); position:relative; overflow:hidden; }
.hero:after { content:'✦'; position:absolute; right:5%; top:-55px; font-size:205px; color:rgba(255,255,255,.07); }
.eyebrow { color:#5eead4; letter-spacing:.16em; text-transform:uppercase; font-size:.72rem; font-weight:800; }
.hero h1 { color:#fff !important; font-family:Manrope,Inter,sans-serif; font-size:clamp(2.2rem,5vw,4.1rem); line-height:1.05; margin:.5rem 0; font-weight:800; }
.hero p { color:#d9eaff; max-width:800px; font-size:1.05rem; margin:0; }
.pills { display:flex; flex-wrap:wrap; gap:.55rem; margin-top:1.1rem; }
.pill { border:1px solid rgba(94,234,212,.32); background:rgba(34,211,238,.08); padding:.42rem .75rem; border-radius:999px; color:#f3ffff; font-size:.78rem; }
.kicker { color:#5eead4; font-size:.72rem; letter-spacing:.15em; font-weight:800; text-transform:uppercase; margin:.3rem 0; }
.section-title { color:#fff; font-size:1.55rem; font-weight:800; margin:0 0 .45rem; }
.subtle, [data-testid="stCaptionContainer"] { color:#b8c7d9 !important; }
div[data-testid="stMetric"] { background:linear-gradient(145deg,#14243a,#0d1a2b); border:1px solid rgba(34,211,238,.22); padding:1rem; border-radius:17px; }
div[data-testid="stMetricLabel"] { color:#b8c7d9 !important; }
div[data-testid="stMetricValue"] { color:#fff !important; }
[data-testid="stVerticalBlockBorderWrapper"] { background:rgba(16,31,51,.78); border:1px solid rgba(34,211,238,.18); border-radius:17px; }
.stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] > button { border:1px solid rgba(94,234,212,.5); border-radius:12px; background:linear-gradient(100deg,#22d3ee,#5eead4); color:#061321; font-weight:800; min-height:2.65rem; }
.stButton > button:hover, .stDownloadButton > button:hover { filter:brightness(1.08); border-color:#fff; }
.stTabs [data-baseweb="tab-list"] { gap:.35rem; background:#111f32; padding:.4rem; border-radius:13px; }
.stTabs [aria-selected="true"] { background:rgba(34,211,238,.13) !important; color:#5eead4 !important; }
[data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p, .stMarkdown, .stMarkdown p, label { color:#f4f8ff; }
input, textarea, [data-baseweb="select"] > div { background:#101f32 !important; color:#fff !important; border-color:rgba(34,211,238,.35) !important; }
input::placeholder, textarea::placeholder { color:#b8c7d9 !important; }
hr { border-color:rgba(34,211,238,.18); }
.footer { text-align:center; color:#91a8c2; font-size:.78rem; padding:1.5rem 0 .3rem; }
.small-note { border-left:3px solid #5eead4; background:rgba(94,234,212,.07); padding:.7rem .9rem; border-radius:0 10px 10px 0; color:#d8e9f7; }
/* AI Coach: replace dark/black alert text with a clear premium light palette */
[data-testid="stAlert"] { background:linear-gradient(135deg,rgba(17,43,68,.98),rgba(12,34,52,.98)) !important; border:1px solid rgba(94,234,212,.38) !important; border-radius:14px !important; }
[data-testid="stAlert"] *, [data-testid="stAlert"] p, [data-testid="stAlert"] div { color:#eaf7ff !important; }
[data-testid="stAlert"] svg { fill:#5eead4 !important; }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# BILINGUAL LABELS
# ---------------------------
TEXT = {
    "English": {
        "tagline": "Smart Learning · Healthy Life · Bright Future",
        "intro": "A student-support studio that turns practice results into clear next steps and encourages balanced routines.",
        "login": "Login", "register": "Create account", "username": "Username", "password": "Password",
        "name": "Student / Teacher name", "role": "Account type", "student": "Student", "teacher": "Teacher",
        "class": "Class / Grade", "goal": "Main learning goal", "energy": "Study energy today", "intention": "One intention for today",
        "enter": "Enter dashboard", "cancel": "Cancel / Clear", "logout": "Log out", "language": "Language",
        "overview": "Overview", "learning": "Learning Dashboard", "quiz": "AI Quiz Generator", "coach": "Advanced AI Coach",
        "teacher_dash": "Teacher Dashboard", "values": "Values & Reflection", "transparent": "Transparent Prototype",
        "showcase": "Project Showcase", "roadmap": "Roadmap & Team", "judge": "Judge Q&A", "analytics": "Performance Analytics",
        "profile": "Student Profile", "welcome": "Welcome", "build_plan": "Build my learning plan", "download": "Download PDF report",
        "goal_options": ["Understand difficult concepts", "Improve memory and recall", "Improve exam performance", "Build a balanced routine", "Improve reading comprehension"],
        "energy_options": ["Low", "Okay", "Good", "High"]
    },
    "ગુજરાતી": {
        "tagline": "સ્માર્ટ લર્નિંગ · સ્વસ્થ જીવન · ઉજ્જવળ ભવિષ્ય",
        "intro": "અભ્યાસના પરિણામોને આગળના સ્પષ્ટ પગલાંમાં ફેરવતું અને સંતુલિત દિનચર્યાને પ્રોત્સાહન આપતું વિદ્યાર્થી સહાયક પ્લેટફોર્મ.",
        "login": "લૉગિન", "register": "એકાઉન્ટ બનાવો", "username": "યુઝરનેમ", "password": "પાસવર્ડ",
        "name": "વિદ્યાર્થી / શિક્ષકનું નામ", "role": "એકાઉન્ટનો પ્રકાર", "student": "વિદ્યાર્થી", "teacher": "શિક્ષક",
        "class": "ધોરણ", "goal": "મુખ્ય અભ્યાસ લક્ષ્ય", "energy": "આજની અભ્યાસ ઊર્જા", "intention": "આજનો એક સંકલ્પ",
        "enter": "ડેશબોર્ડ ખોલો", "cancel": "રદ કરો / સાફ કરો", "logout": "લૉગઆઉટ", "language": "ભાષા",
        "overview": "ઝાંખી", "learning": "લર્નિંગ ડેશબોર્ડ", "quiz": "AI ક્વિઝ જનરેટર", "coach": "એડવાન્સ્ડ AI કોચ",
        "teacher_dash": "ટીચર ડેશબોર્ડ", "values": "મૂલ્યો અને આત્મચિંતન", "transparent": "પારદર્શક પ્રોટોટાઇપ",
        "showcase": "પ્રોજેક્ટ શોકેસ", "roadmap": "રોડમેપ અને ટીમ", "judge": "જજ પ્રશ્નોત્તરી", "analytics": "પરફોર્મન્સ એનાલિટિક્સ",
        "profile": "વિદ્યાર્થી પ્રોફાઇલ", "welcome": "સ્વાગત છે", "build_plan": "મારો અભ્યાસ પ્લાન બનાવો", "download": "PDF રિપોર્ટ ડાઉનલોડ કરો",
        "goal_options": ["મુશ્કેલ વિષયો સમજવા", "યાદશક્તિ અને રિકોલ સુધારવા", "પરીક્ષાનું પ્રદર્શન સુધારવા", "સંતુલિત દિનચર્યા બનાવવી", "વાંચન સમજ સુધારવી"],
        "energy_options": ["ઓછી", "ઠીક", "સારી", "ખૂબ સારી"]
    }
}

# ---------------------------
# DATABASE + PASSWORD HELPERS
# ---------------------------
def db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL, salt TEXT NOT NULL, full_name TEXT NOT NULL,
            role TEXT NOT NULL, grade TEXT, goal TEXT, energy TEXT, intention TEXT,
            created_at TEXT NOT NULL)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
            subject TEXT NOT NULL, topic TEXT NOT NULL, score INTEGER NOT NULL,
            total INTEGER NOT NULL, created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id))""")
        conn.execute("""CREATE TABLE IF NOT EXISTS reflections (
            id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
            answer TEXT NOT NULL, created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id))""")


def password_hash(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 180000).hex()


def create_user(username, password, full_name, role, grade, goal, energy, intention):
    salt = secrets.token_hex(16)
    hashed = password_hash(password, salt)
    with db() as conn:
        conn.execute("INSERT INTO users(username,password_hash,salt,full_name,role,grade,goal,energy,intention,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
                     (username.lower().strip(), hashed, salt, full_name.strip(), role, grade, goal, energy, intention.strip(), datetime.now().isoformat(timespec="seconds")))


def authenticate(username, password):
    with db() as conn:
        user = conn.execute("SELECT * FROM users WHERE username=?", (username.lower().strip(),)).fetchone()
    if not user:
        return None
    return user if secrets.compare_digest(password_hash(password, user["salt"]), user["password_hash"]) else None


def get_user_results(user_id=None):
    with db() as conn:
        if user_id is None:
            rows = conn.execute("SELECT q.*,u.full_name,u.username,u.grade FROM quiz_results q JOIN users u ON q.user_id=u.id ORDER BY q.id DESC").fetchall()
        else:
            rows = conn.execute("SELECT * FROM quiz_results WHERE user_id=? ORDER BY id DESC", (user_id,)).fetchall()
    return [dict(r) for r in rows]


def save_result(user_id, subject, topic, score, total):
    with db() as conn:
        conn.execute("INSERT INTO quiz_results(user_id,subject,topic,score,total,created_at) VALUES(?,?,?,?,?,?)",
                     (user_id, subject, topic, score, total, datetime.now().isoformat(timespec="seconds")))


def save_reflection(user_id, answer):
    with db() as conn:
        conn.execute("INSERT INTO reflections(user_id,answer,created_at) VALUES(?,?,?)", (user_id, answer, datetime.now().isoformat(timespec="seconds")))


init_db()

# ---------------------------
# QUIZ CONTENT (transparent, template-based generator)
# ---------------------------
QUIZ_BANK = {
    "Physics": {
        "Motion": [
            ("Which quantity is a vector?", ["Speed", "Distance", "Displacement", "Time"], 2, "Displacement has magnitude and direction."),
            ("The SI unit of acceleration is:", ["m/s", "m/s²", "km/h", "N"], 1, "Acceleration is change in velocity per unit time."),
            ("The slope of a velocity-time graph represents:", ["Distance", "Acceleration", "Speed", "Momentum"], 1, "The gradient is change in velocity divided by time.")],
        "Force": [
            ("Newton's first law is also called the law of:", ["Acceleration", "Inertia", "Action", "Gravitation"], 1, "It describes the tendency to resist change in motion."),
            ("The SI unit of force is:", ["Joule", "Watt", "Newton", "Pascal"], 2, "Force is measured in newtons (N)."),
            ("If net force is zero, acceleration is:", ["Zero", "Maximum", "Negative", "Infinite"], 0, "Zero net force means zero acceleration.")]
    },
    "Chemistry": {
        "Chemical Bonding": [
            ("Which bond involves sharing electron pairs?", ["Ionic", "Covalent", "Metallic", "Hydrogen"], 1, "Covalent bonds form through shared electron pairs."),
            ("The shape of methane (CH₄) is:", ["Linear", "Bent", "Tetrahedral", "Trigonal planar"], 2, "Four bonding pairs arrange tetrahedrally."),
            ("A polar covalent bond forms when electrons are:", ["Shared equally", "Transferred fully", "Shared unequally", "Removed"], 2, "Different electronegativities cause unequal sharing.")],
        "Periodic Trends": [
            ("Across a period, atomic radius generally:", ["Increases", "Decreases", "Stays same", "Doubles"], 1, "Effective nuclear charge generally increases across a period."),
            ("The energy needed to remove an electron is called:", ["Electron affinity", "Ionisation enthalpy", "Bond energy", "Lattice energy"], 1, "Ionisation enthalpy is the energy required to remove an electron."),
            ("Elements in the same group generally have the same number of:", ["Neutrons", "Shells", "Valence electrons", "Isotopes"], 2, "For main-group elements, group position relates to valence electrons.")]
    },
    "Mathematics": {
        "Trigonometry": [
            ("What is sin 30°?", ["0", "1/2", "√3/2", "1"], 1, "sin 30° = 1/2."),
            ("What is cos 60°?", ["0", "1/2", "√3/2", "1"], 1, "cos 60° = 1/2."),
            ("The value of tan 45° is:", ["0", "1/√3", "1", "√3"], 2, "tan 45° = 1.")],
        "Algebra": [
            ("If x + 5 = 12, x equals:", ["5", "6", "7", "17"], 2, "Subtract 5 from both sides."),
            ("The factorisation of x² − 9 is:", ["(x−9)(x+1)", "(x−3)(x+3)", "(x−3)²", "(x+9)²"], 1, "Use the difference of two squares."),
            ("The coefficient of x in 4x + 7 is:", ["4", "7", "11", "x"], 0, "The coefficient multiplying x is 4.")]
    },
    "English": {
        "Vocabulary": [
            ("Choose the closest meaning of 'brief'.", ["Short", "Angry", "Distant", "Heavy"], 0, "Brief means short in duration or length."),
            ("Choose the opposite of 'ancient'.", ["Old", "Modern", "Historic", "Past"], 1, "Modern is the opposite of ancient."),
            ("A person who writes poems is a:", ["Painter", "Poet", "Pilot", "Editor"], 1, "A poet writes poems.")]
    }
}


def make_pdf(user, results, intention):
    if not PDF_AVAILABLE:
        return None
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 55
    pdf.setFillColorRGB(.04, .12, .22)
    pdf.rect(0, height-115, width, 115, fill=1, stroke=0)
    pdf.setFillColorRGB(.36, .92, .85)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(42, height-58, "AB SCHOOL LOOP AI")
    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(42, height-80, "Student learning progress report")
    y = height - 145
    pdf.setFillColorRGB(.08, .13, .20)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(42, y, "Student details")
    y -= 22
    pdf.setFont("Helvetica", 10)
    for line in [f"Name: {user['full_name']}", f"Class: {user['grade'] or 'Not specified'}", f"Main learning goal: {user['goal'] or 'Not specified'}", f"Study energy: {user['energy'] or 'Not specified'}", f"Report date: {date.today().strftime('%d %b %Y')}"]:
        pdf.drawString(48, y, line); y -= 17
    y -= 10
    pdf.setFont("Helvetica-Bold", 12); pdf.drawString(42, y, "Quiz history"); y -= 20
    pdf.setFont("Helvetica", 9)
    if results:
        for item in results[:12]:
            line = f"{item['subject']} / {item['topic']}: {item['score']} of {item['total']} ({round(item['score']/max(item['total'],1)*100)}%)"
            pdf.drawString(48, y, line[:105]); y -= 15
            if y < 95:
                pdf.showPage(); y = height - 55; pdf.setFont("Helvetica", 9)
    else:
        pdf.drawString(48, y, "No quiz attempts recorded yet."); y -= 17
    y -= 8
    pdf.setFont("Helvetica-Bold", 12); pdf.drawString(42, y, "Today's intention"); y -= 20
    pdf.setFont("Helvetica", 10)
    for part in (intention or "Not entered").splitlines()[:4]:
        pdf.drawString(48, y, part[:105]); y -= 15
    pdf.setFont("Helvetica-Oblique", 8)
    pdf.drawString(42, 35, "Prototype report. Suggestions are educational prompts, not a formal assessment.")
    pdf.save(); buffer.seek(0)
    return buffer.getvalue()

# ---------------------------
# LOGIN / REGISTRATION GATE
# ---------------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "language" not in st.session_state:
    st.session_state.language = "English"

# The language selector is available on the first screen and in the sidebar.
head_left, head_right = st.columns([4, 1])
with head_right:
    st.session_state.language = st.selectbox("Language / ભાષા", ["English", "ગુજરાતી"], index=["English", "ગુજરાતી"].index(st.session_state.language), key="language_pick")
T = TEXT[st.session_state.language]

st.markdown(f"""
<div class="hero">
  <div class="eyebrow">STUDENT GROWTH · LEARNING SCIENCE · HEALTHY LIFE</div>
  <h1>AB SCHOOL LOOP AI</h1>
  <p>{T['tagline']}<br>{T['intro']}</p>
  
</div>
""", unsafe_allow_html=True)

if st.session_state.user is None:
    st.markdown('<div class="kicker">WELCOME / SECURE DEMO ACCESS</div><div class="section-title">Your learning space starts here</div>', unsafe_allow_html=True)
    login_tab, register_tab = st.tabs([f"🔐 {T['login']}", f"✨ {T['register']}"])
    with login_tab:
        with st.form("login_form"):
            login_user = st.text_input(T["username"], key="login_username")
            login_pass = st.text_input(T["password"], type="password", key="login_password")
            login_go = st.form_submit_button(T["login"], type="primary", use_container_width=True)
        if login_go:
            found = authenticate(login_user, login_pass)
            if found:
                st.session_state.user = dict(found)
                st.rerun()
            else:
                st.error("Incorrect username or password. / યુઝરનેમ અથવા પાસવર્ડ ખોટો છે.")
    with register_tab:
        st.caption("Create a local demo account. Teacher accounts are for the project demonstration only.")
        with st.form("register_form", clear_on_submit=False):
            full_name = st.text_input(T["name"])
            username = st.text_input(T["username"])
            password = st.text_input(T["password"] + " (minimum 8 characters)", type="password")
            role_label = st.selectbox(T["role"], [T["student"], T["teacher"]])
            grade = st.selectbox(T["class"], ["Class 8", "Class 9", "Class 10", "Class 11", "Class 12", "Not applicable"])
            # Optional profile fields are intentionally omitted from registration.
            goal, energy, intention = "", "", ""
            b1, b2 = st.columns(2)
            with b1:
                register_go = st.form_submit_button("✅ " + T["enter"], type="primary", use_container_width=True)
            with b2:
                clear_go = st.form_submit_button("✖ " + T["cancel"], use_container_width=True)
        if clear_go:
            st.rerun()
        if register_go:
            if not all([full_name.strip(), username.strip(), password]):
                st.error("Please complete your name, username and password. / નામ, યુઝરનેમ અને પાસવર્ડ ભરો.")
            elif len(password) < 8:
                st.error("Use a password with at least 8 characters. / ઓછામાં ઓછા 8 અક્ષરનો પાસવર્ડ રાખો.")
            else:
                try:
                    role = "Teacher" if role_label == T["teacher"] else "Student"
                    create_user(username, password, full_name, role, grade, goal, energy, intention)
                    found = authenticate(username, password)
                    st.session_state.user = dict(found)
                    st.success("Account created. Welcome! / એકાઉન્ટ બની ગયું.")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("That username is already taken. / આ યુઝરનેમ પહેલેથી વપરાય છે.")
    st.markdown('<div class="small-note">🔒 Demo privacy: account information and quiz results are stored in a local SQLite database on the computer running this app. This is a classroom prototype, not a production identity system.</div>', unsafe_allow_html=True)
    st.stop()

# ---------------------------
# AUTHENTICATED APP
# ---------------------------
user = st.session_state.user
is_teacher = user["role"] == "Teacher"

with st.sidebar:
    st.markdown("# 🎓 AB SCHOOL LOOP AI")
    st.caption("MIDNIGHT AI · Learning studio")
    st.markdown(f"**{user['full_name']}**")
    st.caption(f"{user['role']} · {user['grade'] or '—'}")
    st.divider()
    nav_items = [T["overview"], T["learning"], T["quiz"], T["coach"], T["analytics"], T["showcase"], T["roadmap"]]
    if is_teacher:
        nav_items.insert(4, T["teacher_dash"])
    page = st.radio("NAVIGATION", nav_items, label_visibility="collapsed")
    st.divider()
    if st.button("↩ " + T["logout"], use_container_width=True):
        st.session_state.user = None
        st.rerun()
    st.caption("Prototype v2.0 · Navy / Cyan / Mint")

results = get_user_results(user["id"])
score_values = [round(r["score"] / max(r["total"], 1) * 100) for r in results]
avg_score = round(sum(score_values) / len(score_values), 1) if score_values else 0

# ---------------------------
# OVERVIEW
# ---------------------------
if page == T["overview"]:
    st.markdown(f'<div class="kicker">01 / STUDENT HOME</div><div class="section-title">{T["welcome"]}, {user["full_name"]} 👋</div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Quiz attempts", len(results)); c2.metric("Average score", f"{avg_score}%" if results else "—")
    c3.metric("Account", user["role"]); c4.metric("Class", user["grade"] or "—")
    st.markdown("### Your learning loop")
    cols = st.columns(4)
    for col, icon, title, desc in zip(cols, ["📘","🧩","🔎","🚀"], ["Learn","Recall","Reflect","Improve"], ["Study one clear concept.","Try a quiz without notes.","Review mistakes calmly.","Choose your next small step."]):
        with col:
            with st.container(border=True):
                st.markdown(f"### {icon} {title}"); st.caption(desc)
    st.markdown("<div class='small-note'>The app uses transparent educational rules and sample question templates. It does not claim to be a trained AI model.</div>", unsafe_allow_html=True)

# ---------------------------
# LEARNING DASHBOARD
# ---------------------------
elif page == T["learning"]:
    st.markdown('<div class="kicker">02 / LEARNING DASHBOARD</div><div class="section-title">Build your next practice plan</div>', unsafe_allow_html=True)
    st.caption("Enter a recent quiz score for each subject. These are editable inputs, not imported exam records.")
    subjects = ["Physics", "Chemistry", "Mathematics", "English"]
    cols = st.columns(4)
    entered = {}
    for col, subject in zip(cols, subjects):
        with col:
            with st.container(border=True):
                entered[subject] = st.slider(subject, 0, 100, 65, key=f"score_{subject}")
                st.caption("Needs support" if entered[subject] < 50 else "Growing" if entered[subject] < 75 else "Strong")
    if st.button("✨ " + T["build_plan"], type="primary", use_container_width=True):
        st.session_state.practice_plan = entered
    if "practice_plan" in st.session_state:
        plan = st.session_state.practice_plan
        df = pd.DataFrame([{"Subject": s, "Score": v, "Status": "Needs support" if v < 50 else "Growing" if v < 75 else "Strong", "Next step": "Revisit one core idea + 5 guided questions" if v < 50 else "Revise key concepts + 5 mixed questions" if v < 75 else "Spaced revision + 2 challenge questions"} for s,v in plan.items()])
        st.dataframe(df, use_container_width=True, hide_index=True)
        fig = px.bar(df, x="Subject", y="Score", color="Status", range_y=[0,100], color_discrete_map={"Needs support":"#fb7185","Growing":"#fbbf24","Strong":"#5eead4"}, title="Subject performance")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#eaf2ff")
        st.plotly_chart(fig, use_container_width=True)
        st.download_button("Download practice plan CSV", df.to_csv(index=False).encode("utf-8-sig"), "ab_school_loop_practice_plan.csv", "text/csv")

# ---------------------------
# AI QUIZ GENERATOR
# ---------------------------
elif page == T["quiz"]:
    st.markdown('<div class="kicker">03 / ACTIVE RECALL LAB</div><div class="section-title">AI Quiz Generator</div>', unsafe_allow_html=True)
    st.caption("Transparent quiz generator: selects questions from the built-in question bank. It is not generating new facts with a trained AI model.")
    s1,s2,s3 = st.columns(3)
    with s1: subject = st.selectbox("Subject", list(QUIZ_BANK.keys()))
    with s2: topic = st.selectbox("Topic", list(QUIZ_BANK[subject].keys()))
    with s3: count = st.selectbox("Number of questions", [3])
    if st.button("⚡ Generate quiz", type="primary"):
        st.session_state.active_quiz = {"subject":subject, "topic":topic, "questions":QUIZ_BANK[subject][topic], "answers":{}}
    quiz = st.session_state.get("active_quiz")
    if quiz:
        st.markdown(f"### {quiz['subject']} · {quiz['topic']}")
        with st.form("quiz_attempt_form"):
            answers = []
            for i,(question, options, correct, explanation) in enumerate(quiz["questions"][:count]):
                st.markdown(f"**Q{i+1}. {question}**")
                answers.append(st.radio("Choose an answer", options, key=f"attempt_{quiz['subject']}_{quiz['topic']}_{i}", index=None))
            submitted = st.form_submit_button("Submit answers", type="primary", use_container_width=True)
        if submitted:
            if any(a is None for a in answers):
                st.warning("Answer every question before submitting.")
            else:
                correct_count = sum(1 for a, q in zip(answers, quiz["questions"]) if a == q[1][q[2]])
                save_result(user["id"], quiz["subject"], quiz["topic"], correct_count, len(answers))
                st.session_state.last_quiz_review = [(q[0], a, q[1][q[2]], q[3]) for a,q in zip(answers, quiz["questions"])]
                st.session_state.pop("active_quiz", None)
                st.success(f"Your score: {correct_count}/{len(answers)} ({round(correct_count/len(answers)*100)}%).")
                st.rerun()
    if st.session_state.get("last_quiz_review"):
        with st.expander("Review the latest answers", expanded=True):
            for q,a,correct,why in st.session_state.last_quiz_review:
                st.markdown(f"**{q}**")
                st.write(f"Your answer: {a} · Correct answer: {correct}")
                st.caption(why)

# ---------------------------
# ADVANCED AI COACH
# ---------------------------
elif page == T["coach"]:
    st.markdown('<div class="kicker">04 / STUDY COACH</div><div class="section-title">Advanced AI Coach</div>', unsafe_allow_html=True)
    st.caption("Rule-based coaching prompts. No external AI service or personal data transmission is used.")
    energy_now = st.select_slider("How is your energy right now?", ["Low", "Okay", "Good", "High"], value="Okay")
    target = st.selectbox("What do you want help with?", ["Understand a hard concept", "Remember formulas", "Prepare for a quiz", "Reduce distractions", "Plan a balanced study session"])
    context = st.text_area("Optional: topic or chapter", placeholder="Example: Newton's laws / Chemical bonding")
    if st.button("Generate my coaching steps", type="primary"):
        advice = {
            "Understand a hard concept":["Read one worked example slowly.","Explain the concept in your own words.","Solve two similar questions and check each step."],
            "Remember formulas":["Write the formula from memory.","Check symbols and units.","Use it in one direct and one mixed problem."],
            "Prepare for a quiz":["List the 3 most important subtopics.","Attempt questions without notes.","Review errors and retry one similar question."],
            "Reduce distractions":["Choose one small task.","Keep notifications away for one focus block.","Take a short break and note what you completed."],
            "Plan a balanced study session":["Choose one 20–25 minute learning block.","Add a short movement and water break.","Finish with a 2-minute recall check."]}
        prefix = "Start gently with a 10-minute first step." if energy_now == "Low" else "Use one focused block, then review your progress."
        st.success(prefix)
        if context.strip(): st.info(f"Focus topic: {context.strip()}")
        for i,step in enumerate(advice[target],1): st.markdown(f"**{i}.** {step}")

# ---------------------------
# TEACHER DASHBOARD
# ---------------------------
elif is_teacher and page == T["teacher_dash"]:
    st.markdown('<div class="kicker">05 / TEACHER CONTROL ROOM</div><div class="section-title">Teacher Dashboard</div>', unsafe_allow_html=True)
    with db() as conn:
        students = [dict(r) for r in conn.execute("SELECT id,full_name,username,grade,goal,created_at FROM users WHERE role='Student' ORDER BY full_name").fetchall()]
    all_results = get_user_results()
    a,b,c = st.columns(3)
    a.metric("Registered students", len(students)); b.metric("Quiz attempts", len(all_results))
    c.metric("Average score", f"{round(sum(r['score']/max(r['total'],1)*100 for r in all_results)/len(all_results),1)}%" if all_results else "—")
    st.markdown("### Student directory")
    if students:
        st.dataframe(pd.DataFrame(students)[["full_name","username","grade","goal","created_at"]], use_container_width=True, hide_index=True)
    else:
        st.info("No student accounts yet. Ask students to register with Student account type.")
    st.markdown("### Recent quiz activity")
    if all_results:
        rdf = pd.DataFrame(all_results)
        rdf["Score (%)"] = (rdf["score"] / rdf["total"] * 100).round(1)
        st.dataframe(rdf[["full_name","grade","subject","topic","Score (%)","created_at"]], use_container_width=True, hide_index=True)
        st.download_button("Download class activity CSV", rdf.to_csv(index=False).encode("utf-8-sig"), "teacher_class_activity.csv", "text/csv")
    else:
        st.info("Quiz activity will appear after students complete a quiz.")
    st.caption("Teacher view is a local demo feature. Use fictional/demo accounts for public presentations.")

# ---------------------------
# PERFORMANCE ANALYTICS
# ---------------------------
elif page == T["analytics"]:
    st.markdown('<div class="kicker">06 / PERFORMANCE INTELLIGENCE</div><div class="section-title">Performance Analytics</div>', unsafe_allow_html=True)
    if results:
        df = pd.DataFrame(results)
        df["Score (%)"] = (df["score"] / df["total"] * 100).round(1)
        x,y,z = st.columns(3)
        x.metric("Attempts", len(df)); y.metric("Average", f"{df['Score (%)'].mean():.1f}%"); z.metric("Best", f"{df['Score (%)'].max():.1f}%")
        df["Attempt"] = range(1,len(df)+1)
        fig = px.line(df.sort_values("id"), x="Attempt", y="Score (%)", markers=True, title="Quiz score trend", range_y=[0,100])
        fig.update_traces(line_color="#22d3ee", marker_color="#5eead4")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#eaf2ff")
        st.plotly_chart(fig, use_container_width=True)
        by_subject = df.groupby("subject",as_index=False)["Score (%)"].mean()
        fig2 = px.bar(by_subject,x="subject",y="Score (%)",title="Average by subject",range_y=[0,100],color="subject")
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#eaf2ff",showlegend=False)
        st.plotly_chart(fig2,use_container_width=True)
        st.dataframe(df[["subject","topic","score","total","Score (%)","created_at"]],use_container_width=True,hide_index=True)
    else:
        st.info("Complete your first quiz to unlock personal analytics.")

# ---------------------------
# VALUES & REFLECTION
# ---------------------------
elif page == T["values"]:
    st.markdown('<div class="kicker">07 / VALUES & REFLECTION</div><div class="section-title">Grow with honesty, effort and kindness</div>', unsafe_allow_html=True)
    prompts = ["What did I learn today?", "Where did I show patience or honesty?", "Who did I help or thank today?", "What is one small improvement for tomorrow?"]
    with st.form("reflection_form"):
        answers = [st.text_area(prompt, max_chars=300, key=f"value_prompt_{i}") for i,prompt in enumerate(prompts)]
        submitted = st.form_submit_button("Save reflection", type="primary")
    if submitted:
        combined = "\n".join(f"{p} {a.strip()}" for p,a in zip(prompts,answers) if a.strip())
        if combined:
            save_reflection(user["id"], combined)
            st.success("Reflection saved in the local project database.")
        else:
            st.warning("Write at least one reflection before saving.")

# ---------------------------
# TRANSPARENT PROTOTYPE
# ---------------------------
elif page == T["transparent"]:
    st.markdown('<div class="kicker">08 / RESPONSIBLE DESIGN</div><div class="section-title">Transparent Prototype</div>', unsafe_allow_html=True)
    st.warning("This is a rule-based educational prototype, not a trained machine-learning model or a validated assessment tool.")
    rules = pd.DataFrame([( "0–49%", "Needs support", "Revisit the core idea + guided practice"),("50–74%","Growing","Revise concepts + mixed practice"),("75–100%","Strong","Spaced revision + challenge questions")],columns=["Score range","Status","Suggested next step"])
    st.dataframe(rules,use_container_width=True,hide_index=True)
    st.markdown("### What the prototype does")
    st.write("- Stores local demo accounts and quiz attempts in SQLite.\n- Uses fixed rules and a built-in question bank.\n- Displays progress charts and downloadable reports.\n- Does not diagnose health, measure intelligence, or predict a student's future.\n- Public demos should use fictional student data and appropriate permission.")

# ---------------------------
# PROJECT SHOWCASE
# ---------------------------
elif page == T["showcase"]:
    st.markdown('<div class="kicker">09 / PROJECT PRESENTATION</div><div class="section-title">Project Showcase</div>', unsafe_allow_html=True)
    st.markdown("### Problem statement")
    st.write("Students may find it difficult to decide what to practise next while balancing academic learning and everyday routines.")
    st.markdown("### Proposed solution")
    st.write("AB SCHOOL LOOP AI combines a student learning dashboard, question-bank quiz generator, transparent coaching prompts, teacher overview, reflection, and performance analytics.")
    st.markdown("### System architecture")
    st.code("Student / Teacher → Login → Profile & Learning Inputs → Quiz / Rule Engine → Analytics → Reflection → Next Practice",language="text")
    st.markdown("### Technology stack")
    st.write("Python · Streamlit · SQLite · Pandas · Plotly · ReportLab (PDF export)")
    st.markdown("### Key modules")
    modules = st.columns(3)
    for col,icon,title,desc in zip(modules,["🔐","🧠","📊"],["Access","Learning","Insights"],["Local login and role-based views.","Quiz bank and guided coach prompts.","Progress charts and teacher activity view."]):
        with col:
            with st.container(border=True): st.markdown(f"### {icon} {title}"); st.write(desc)

# ---------------------------
# ROADMAP + PERFORMANCE GRAPH + STUDY ASSISTANT
# ---------------------------
elif page == T["roadmap"]:
    st.markdown('<div class="kicker">10 / EXECUTION PLAN</div><div class="section-title">Complete Student Growth Roadmap</div>', unsafe_allow_html=True)
    roadmap = pd.DataFrame([
        ("Week 1", 1, "Baseline assessment, student needs research and success metrics"),
        ("Week 2", 2, "Registration, UI refinement and student/teacher role testing"),
        ("Week 3", 3, "Question bank, quiz evaluation and transparent coaching rules"),
        ("Week 4", 4, "Performance graphs, subject analysis and teacher dashboard"),
        ("Week 5", 5, "Pilot testing, student feedback, accessibility and bug fixes"),
        ("Week 6", 6, "Final prototype validation, presentation, poster and demo rehearsal"),
    ], columns=["Timeline", "Week", "Milestone"])
    st.dataframe(roadmap[["Timeline", "Milestone"]], use_container_width=True, hide_index=True)
    fig_roadmap = px.bar(roadmap, x="Week", y="Timeline", orientation="h", color="Week",
                         hover_data={"Milestone": True, "Week": False}, title="Six-week project execution graph")
    fig_roadmap.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font_color="#eaf2ff", showlegend=False, yaxis_title="Project phase", xaxis_title="Week")
    st.plotly_chart(fig_roadmap, use_container_width=True)

    st.markdown("### Full student improvement roadmap")
    student_steps = pd.DataFrame([
        ("1. Measure", "Record current marks by subject and identify topics needing attention."),
        ("2. Understand", "Relearn one weak concept using class notes and a worked example."),
        ("3. Practise", "Solve a small set of basic questions, then attempt mixed questions."),
        ("4. Review", "Check every mistake and write why the correct method works."),
        ("5. Re-test", "Take a short topic test after revision and compare the result."),
        ("6. Improve", "Repeat the cycle and update the next week's targets."),
    ], columns=["Stage", "Action"])
    st.dataframe(student_steps, use_container_width=True, hide_index=True)

    st.markdown("### Team responsibilities")
    team = pd.DataFrame([
        ("Student 1", "Research, student feedback and evaluation metrics"),
        ("Student 2", "UI/UX design, accessibility and presentation visuals"),
        ("Student 3", "Python, database, quiz engine and analytics"),
        ("Student 4", "Testing, documentation, demo and presentation"),
    ], columns=["Role", "Responsibility"])
    st.dataframe(team, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("### 📘 Marks-based Study Assistant")
    st.caption("Enter recent marks out of 100. The assistant uses clear score bands and study suggestions; it is a rule-based prototype, not a trained AI model.")
    subjects = ["Physics", "Chemistry", "Mathematics", "English"]
    mark_cols = st.columns(4)
    marks = {}
    for col, subject in zip(mark_cols, subjects):
        with col:
            marks[subject] = st.number_input(subject, min_value=0, max_value=100, value=60, step=1, key=f"roadmap_mark_{subject}")
    if st.button("Generate my improvement roadmap", type="primary", use_container_width=True):
        weakest = min(marks, key=marks.get)
        average = sum(marks.values()) / len(marks)
        st.metric("Current average", f"{average:.1f}%")
        st.success(f"Priority subject: {weakest} ({marks[weakest]}%). Start with this subject, while maintaining revision in the others.")
        advice = []
        for subject, mark in marks.items():
            if mark < 50:
                advice.append((subject, mark, "Foundation focus", "Revise definitions and one worked example; solve 5 basic questions; ask a teacher about doubts."))
            elif mark < 75:
                advice.append((subject, mark, "Build consistency", "Revise key concepts; solve 8 mixed questions; maintain an error notebook."))
            else:
                advice.append((subject, mark, "Strengthen mastery", "Use spaced revision; solve 3 challenging questions; explain the concept without notes."))
        advice_df = pd.DataFrame(advice, columns=["Subject", "Marks", "Level", "Recommended next steps"])
        st.dataframe(advice_df, use_container_width=True, hide_index=True)
        fig_marks = px.bar(advice_df, x="Subject", y="Marks", color="Level", range_y=[0, 100],
                           title="Your subject-wise marks", color_discrete_map={"Foundation focus":"#fb7185", "Build consistency":"#fbbf24", "Strengthen mastery":"#5eead4"})
        fig_marks.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#eaf2ff")
        st.plotly_chart(fig_marks, use_container_width=True)
        st.markdown("#### Your next 7-day action plan")
        st.write(f"1. **Day 1–2:** Give extra attention to {weakest}; revise one core topic each day.")
        st.write("2. **Day 3–4:** Practise questions in all four subjects and record mistakes.")
        st.write("3. **Day 5:** Revisit incorrect questions and clarify doubts.")
        st.write("4. **Day 6:** Take a short self-test in the priority subject.")
        st.write("5. **Day 7:** Compare marks, note progress and set the next week's target.")

# ---------------------------
# JUDGE Q&A
# ---------------------------
elif page == T["judge"]:
    st.markdown('<div class="kicker">11 / PRESENTATION PREPARATION</div><div class="section-title">Judge Questions & Answers</div>', unsafe_allow_html=True)
    qa = [
        ("What problem does your project solve?", "It helps students turn quiz results into a clear next practice step while encouraging reflection and balanced routines."),
        ("Is this a real AI model?", "The current version is a transparent rule-based prototype with a built-in question bank. It is not a trained ML model."),
        ("How does the quiz generator work?", "It selects questions from a reviewed subject/topic question bank and checks answers automatically."),
        ("How is student progress shown?", "Quiz attempts are stored locally and displayed as score trends and subject averages."),
        ("How is student information handled?", "The demo stores account and quiz data in a local SQLite file. Public demos should use fictional data and appropriate permission."),
        ("What can be improved next?", "A reviewed curriculum-aligned question bank, stronger deployment security, teacher feedback workflows and carefully evaluated ML features.")]
    for question,answer in qa:
        with st.expander(question): st.write(answer)

# ---------------------------
# PROFILE + PDF REPORT (always available at bottom)
# ---------------------------
st.divider()
with st.expander("👤 Profile & PDF Report", expanded=False):
    st.write(f"**Name:** {user['full_name']}  ·  **Role:** {user['role']}  ·  **Class:** {user['grade'] or '—'}")
    if PDF_AVAILABLE:
        pdf_data = make_pdf(user, results, user.get("intention", ""))
        st.download_button("📄 " + T["download"], pdf_data, "AB_SCHOOL_LOOP_AI_Report.pdf", "application/pdf", type="primary")
    else:
        st.warning("PDF library not installed. Run: pip install reportlab")
    st.caption("PDF report uses English text to keep the generated file readable with ReportLab's built-in fonts. The app interface supports Gujarati and English.")

st.markdown('<div class="footer">AB SCHOOL LOOP AI · Midnight AI v2.0 · Student learning support prototype · Learn → Recall → Reflect → Improve</div>', unsafe_allow_html=True)
