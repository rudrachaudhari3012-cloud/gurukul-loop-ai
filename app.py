import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

# =========================================================
# AB SCHOOL LOOP AI — THEME A / MIXED / ULTRA GLOW
# =========================================================

st.set_page_config(
    page_title="AB SCHOOL LOOP AI | Student Growth Studio",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- CORE LOGIC -------------------------

def classify_topic(score):
    if score < 40:
        return "Critical Support", "🔴"
    elif score < 60:
        return "Needs Practice", "🟠"
    elif score < 80:
        return "Developing", "🟡"
    return "Strong", "🟢"


def make_plan(scores, study_minutes, screen_minutes, activity_minutes):
    recommendations = []

    for topic, score in scores.items():
        status, _ = classify_topic(score)

        if score < 40:
            practice = 35
            message = "Start with fundamentals and solve guided examples."
        elif score < 60:
            practice = 25
            message = "Revise concepts, then solve 5–10 targeted questions."
        elif score < 80:
            practice = 15
            message = "Practise mixed questions and review mistakes."
        else:
            practice = 10
            message = "Maintain your strength with spaced revision."

        recommendations.append({
            "Topic": topic,
            "Score (%)": score,
            "Status": status,
            "Suggested Practice (min)": practice,
            "Action": message
        })

    recommendations.sort(key=lambda item: item["Score (%)"])

    routine = []

    if study_minutes < 60:
        routine.append(
            "📚 Study: Try one distraction-free 25-minute focus session."
        )
    elif study_minutes < 120:
        routine.append(
            "📚 Study: Keep focused sessions and short breaks consistent."
        )
    else:
        routine.append(
            "📚 Study: Protect breaks and review whether your sessions are effective."
        )

    if screen_minutes > 180:
        routine.append(
            "📱 Screen balance: Consider replacing some recreational screen "
            "time with reading, hobbies, or offline activities."
        )
    else:
        routine.append(
            "📱 Screen balance: Keep checking that screen time supports your goals."
        )

    if activity_minutes < 30:
        routine.append(
            "🏃 Movement: Add a comfortable walk, outdoor play, or another "
            "enjoyable movement break."
        )
    else:
        routine.append(
            "🏃 Movement: Keep making room for enjoyable physical activity."
        )

    return recommendations, routine


# -------------------- ULTRA THEME CSS ---------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
    --bg: #050816;
    --panel: rgba(13, 24, 48, 0.78);
    --panel-strong: rgba(9, 18, 38, 0.96);
    --cyan: #00E5FF;
    --cyan-soft: #73F5FF;
    --mint: #00FFB3;
    --mint-soft: #9BFFD9;
    --blue: #246BFD;
    --text: #ECF8FF;
    --muted: #9BB3CF;
    --border: rgba(0, 229, 255, 0.30);
    --glow-cyan: 0 0 12px rgba(0,229,255,.50),
                 0 0 30px rgba(0,229,255,.20);
    --glow-mint: 0 0 12px rgba(0,255,179,.42),
                 0 0 30px rgba(0,255,179,.17);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    color: var(--text);
    background:
        radial-gradient(ellipse at 8% 8%, rgba(0,229,255,.17), transparent 35%),
        radial-gradient(ellipse at 92% 16%, rgba(0,255,179,.13), transparent 33%),
        radial-gradient(ellipse at 50% 100%, rgba(36,107,253,.20), transparent 45%),
        linear-gradient(135deg, #030611 0%, #07152B 45%, #041D27 100%);
    background-attachment: fixed;
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    background:
        linear-gradient(115deg,
            transparent 0%,
            rgba(0,229,255,.035) 35%,
            transparent 55%,
            rgba(0,255,179,.035) 80%,
            transparent 100%);
    background-size: 250% 250%;
    animation: auroraFlow 12s ease-in-out infinite alternate;
}

@keyframes auroraFlow {
    0% { background-position: 0% 20%; }
    100% { background-position: 100% 80%; }
}

[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stMain"],
.main {
    background: transparent !important;
}

[data-testid="stHeader"] {
    background: rgba(5,8,22,.55) !important;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.6rem;
    padding-bottom: 3rem;
    position: relative;
    z-index: 1;
}

h1, h2, h3, h4, p, label, li {
    color: var(--text);
}

h1, h2, h3 {
    letter-spacing: -.5px;
}

p, li {
    line-height: 1.7;
}

small, .muted {
    color: var(--muted);
}

/* HERO */
.hero {
    position: relative;
    overflow: hidden;
    padding: 36px 34px;
    margin: 0 0 26px 0;
    border-radius: 25px;
    background:
        radial-gradient(ellipse at 0% 0%, rgba(0,229,255,.20), transparent 48%),
        radial-gradient(ellipse at 100% 100%, rgba(0,255,179,.18), transparent 45%),
        linear-gradient(135deg, rgba(12,28,59,.96), rgba(4,27,38,.92));
    border: 1px solid rgba(0,229,255,.48);
    box-shadow:
        0 0 0 1px rgba(0,255,179,.08),
        0 0 25px rgba(0,229,255,.25),
        0 0 65px rgba(0,229,255,.10),
        inset 0 0 35px rgba(0,229,255,.055);
}

.hero::before {
    content: "";
    position: absolute;
    width: 350px;
    height: 350px;
    right: -90px;
    top: -180px;
    border-radius: 50%;
    background: rgba(0,229,255,.13);
    filter: blur(10px);
    box-shadow: 0 0 80px rgba(0,229,255,.18);
    pointer-events: none;
}

.hero::after {
    content: "";
    position: absolute;
    width: 230px;
    height: 230px;
    right: 18%;
    bottom: -190px;
    border-radius: 50%;
    background: rgba(0,255,179,.15);
    filter: blur(10px);
    pointer-events: none;
}

.hero h1 {
    font-size: clamp(2rem, 5vw, 3.4rem);
    font-weight: 900;
    margin: 8px 0 10px;
    line-height: 1.12;
    background: linear-gradient(90deg, #FFFFFF, #73F5FF, #00FFB3);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 13px rgba(0,229,255,.28));
}

.hero p {
    color: #B9D9EE;
    max-width: 800px;
    margin-bottom: 0;
}

.eyebrow {
    color: var(--mint-soft);
    text-transform: uppercase;
    font-size: .76rem;
    font-weight: 800;
    letter-spacing: 2.5px;
}

/* GLASS CARDS */
.glass-card, [data-testid="stMetric"] {
    background:
        linear-gradient(145deg, rgba(16,35,66,.80), rgba(5,19,35,.84));
    border: 1px solid var(--border);
    border-radius: 19px;
    padding: 20px;
    box-shadow:
        0 0 18px rgba(0,229,255,.10),
        inset 0 1px 0 rgba(255,255,255,.045);
    transition: transform .25s ease, box-shadow .25s ease,
                border-color .25s ease;
}

.glass-card:hover, [data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: rgba(0,255,179,.60);
    box-shadow: var(--glow-cyan), var(--glow-mint);
}

.section-heading {
    font-weight: 800;
    font-size: 1.28rem;
    margin: 24px 0 12px;
    color: #F0FCFF;
}

.section-heading span {
    color: var(--cyan);
    text-shadow: 0 0 13px rgba(0,229,255,.48);
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background:
        radial-gradient(ellipse at 15% 0%, rgba(0,229,255,.13), transparent 45%),
        linear-gradient(180deg, #08162D, #07101F 65%, #061B20);
    border-right: 1px solid rgba(0,229,255,.30);
}

[data-testid="stSidebar"] > div:first-child {
    background: transparent;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #C7E1F5;
}

/* INPUTS */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"],
.stMultiSelect div[data-baseweb="select"] {
    color: var(--text) !important;
    background-color: rgba(5,15,32,.88) !important;
    border-radius: 12px !important;
}

.stTextInput input:focus,
.stNumberInput input:focus,
.stTextArea textarea:focus {
    border-color: var(--cyan) !important;
    box-shadow: var(--glow-cyan) !important;
}

[data-baseweb="slider"] [role="slider"] {
    background-color: var(--mint) !important;
    border: 2px solid #D8FFF2 !important;
    box-shadow: var(--glow-mint) !important;
}

.stSlider [data-testid="stTickBar"] {
    background: rgba(0,229,255,.45);
}

/* BUTTONS */
.stButton > button,
.stDownloadButton > button,
[data-testid="stFormSubmitButton"] button {
    color: #03131C !important;
    font-weight: 800 !important;
    border: 1px solid rgba(125,255,239,.95) !important;
    border-radius: 13px !important;
    background: linear-gradient(100deg, #00E5FF 0%, #55F4DD 48%, #00FFB3 100%) !important;
    box-shadow: var(--glow-cyan), var(--glow-mint) !important;
    transition: all .22s ease !important;
    min-height: 43px;
}

.stButton > button:hover,
.stDownloadButton > button:hover,
[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-2px);
    filter: brightness(1.12);
    box-shadow:
        0 0 18px rgba(0,229,255,.75),
        0 0 42px rgba(0,255,179,.42) !important;
}

.stButton > button:focus,
.stDownloadButton > button:focus {
    outline: 2px solid #FFFFFF !important;
    outline-offset: 3px !important;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(7,18,36,.75);
    padding: 8px;
    border: 1px solid rgba(0,229,255,.20);
    border-radius: 15px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    color: #BBD6EA;
    padding: 10px 16px;
}

.stTabs [aria-selected="true"] {
    color: #03131C !important;
    background: linear-gradient(100deg, #00E5FF, #00FFB3) !important;
    font-weight: 800;
}

/* METRICS */
[data-testid="stMetricLabel"] {
    color: #9ED9F0 !important;
    font-weight: 700;
}

[data-testid="stMetricValue"] {
    color: #F1FFFF !important;
    text-shadow: 0 0 15px rgba(0,229,255,.35);
    font-weight: 900;
}

[data-testid="stMetricDelta"] {
    color: var(--mint-soft) !important;
}

/* CHART & TABLE */
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    border: 1px solid rgba(0,229,255,.22);
    border-radius: 14px;
    overflow: hidden;
}

.js-plotly-plot {
    border-radius: 17px;
    overflow: hidden;
    border: 1px solid rgba(0,229,255,.23);
    box-shadow: 0 0 20px rgba(0,229,255,.08);
}

/* ALERTS */
[data-testid="stAlert"] {
    border-radius: 14px;
    border: 1px solid rgba(0,229,255,.35);
    background: rgba(8,27,46,.84);
    box-shadow: 0 0 16px rgba(0,229,255,.08);
}

/* EXPANDERS */
[data-testid="stExpander"] {
    background: rgba(7,19,38,.65);
    border: 1px solid rgba(0,229,255,.24);
    border-radius: 15px;
    overflow: hidden;
}

[data-testid="stExpander"] summary {
    color: var(--cyan-soft);
    font-weight: 700;
}

/* RADIO / CHECKBOX */
.stRadio label, .stCheckbox label {
    color: #D8EDFA !important;
}

/* DIVIDER */
hr {
    border-color: rgba(0,229,255,.24) !important;
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
}

/* BADGES */
.badge {
    display: inline-block;
    padding: 6px 11px;
    margin: 4px 4px 4px 0;
    border-radius: 999px;
    font-size: .75rem;
    font-weight: 800;
    color: #DFFFF8;
    border: 1px solid rgba(0,255,179,.42);
    background: rgba(0,255,179,.08);
    box-shadow: 0 0 12px rgba(0,255,179,.10);
}

/* FOOTER */
.footer {
    text-align: center;
    color: #8EADC6;
    font-size: .83rem;
    padding: 24px 12px 10px;
    border-top: 1px solid rgba(0,229,255,.20);
    margin-top: 35px;
}

.footer strong {
    color: var(--cyan-soft);
}

/* MOBILE */
@media (max-width: 768px) {
    .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .hero {
        padding: 24px 20px;
        border-radius: 19px;
    }

    .glass-card {
        padding: 15px;
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: .01ms !important;
        transition-duration: .01ms !important;
    }
}
</style>
""", unsafe_allow_html=True)


# -------------------- HERO -------------------------------

st.markdown("""
<div class="hero">
    <div class="eyebrow">✦ Student Growth Studio · AI Research Prototype</div>
    <h1>AB SCHOOL LOOP AI</h1>
    <p>
        Learn smarter. Practise intentionally. Reflect continuously.
        A student-centred learning support prototype that converts topic
        scores and daily routine inputs into clear practice suggestions.
    </p>
    <div style="margin-top:18px;">
        <span class="badge">⚡ ULTRA GLOW</span>
        <span class="badge">◈ CYBER AI</span>
        <span class="badge">✧ ELECTRIC CYAN</span>
        <span class="badge">⬡ NEON MINT</span>
        <span class="badge">◉ MIXED AURORA</span>
    </div>
</div>
""", unsafe_allow_html=True)


# -------------------- TRANSPARENCY -----------------------

with st.expander("🔬 About this AI prototype — read before using"):
    st.write(
        "This version uses transparent, rule-based recommendations. "
        "It does not train a machine-learning model, diagnose a student, "
        "or guarantee academic improvement. Recommendations depend on "
        "the scores and routine values entered by the user."
    )


# -------------------- SIDEBAR -----------------------------

with st.sidebar:
    st.markdown("## 🎓 Student Studio")
    st.caption("Your learning journey starts here.")

    st.markdown("---")
    st.markdown("### 👤 Student Profile")

    student_name = st.text_input(
        "Student name",
        value="Student"
    )

    student_class = st.selectbox(
        "Class / level",
        ["Class 9", "Class 10", "Class 11", "Class 12", "Other"],
        index=2
    )

    st.markdown("---")
    st.markdown("### ⏱️ Daily Rhythm")

    study_minutes = st.slider(
        "Focused study (minutes/day)",
        min_value=0,
        max_value=480,
        value=120,
        step=15
    )

    screen_minutes = st.slider(
        "Non-study screen time (minutes/day)",
        min_value=0,
        max_value=600,
        value=120,
        step=15
    )

    activity_minutes = st.slider(
        "Physical activity (minutes/day)",
        min_value=0,
        max_value=180,
        value=30,
        step=5
    )

    st.markdown("---")
    st.caption("Theme A · Mixed Aurora · Ultra Glow")
    st.caption("Midnight Blue × Electric Cyan × Neon Mint")


# -------------------- TOPIC INPUTS -----------------------

st.markdown(
    '<div class="section-heading"><span>01 /</span> Learning Snapshot</div>',
    unsafe_allow_html=True
)

st.write(
    "Enter your current topic scores from 0 to 100. "
    "Use recent tests or your own revision checks."
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    physics = st.number_input(
        "⚛️ Physics — Motion",
        min_value=0, max_value=100, value=42, step=1
    )

with c2:
    chemistry = st.number_input(
        "🧪 Chemistry — Bonding",
        min_value=0, max_value=100, value=68, step=1
    )

with c3:
    mathematics = st.number_input(
        "📐 Mathematics — Trigonometry",
        min_value=0, max_value=100, value=81, step=1
    )

with c4:
    english = st.number_input(
        "📖 English — Comprehension",
        min_value=0, max_value=100, value=55, step=1
    )

scores = {
    "Physics — Motion": physics,
    "Chemistry — Bonding": chemistry,
    "Mathematics — Trigonometry": mathematics,
    "English — Comprehension": english
}

st.markdown("---")

run_col, info_col = st.columns([1, 2])

with run_col:
    generate = st.button(
        "⚡ Generate My Learning Plan",
        use_container_width=True
    )

with info_col:
    st.caption(
        "Your plan is generated from the values you enter. "
        "Change scores or routine values and run it again to update the plan."
    )

if generate:
    recommendations, routine = make_plan(
        scores,
        study_minutes,
        screen_minutes,
        activity_minutes
    )

    st.session_state["recommendations"] = recommendations
    st.session_state["routine"] = routine
    st.session_state["generated_scores"] = scores.copy()
    st.session_state["generated_name"] = student_name
    st.session_state["generated_class"] = student_class
    st.session_state["generated_date"] = str(date.today())


# -------------------- RESULTS ----------------------------

if "recommendations" in st.session_state:
    recommendations = st.session_state["recommendations"]
    routine = st.session_state["routine"]
    active_scores = st.session_state["generated_scores"]

    average_score = round(
        sum(active_scores.values()) / len(active_scores), 1
    )

    weakest_topic = min(
        active_scores,
        key=active_scores.get
    )

    total_practice = sum(
        item["Suggested Practice (min)"]
        for item in recommendations
    )

    st.markdown("---")
    st.markdown(
        '<div class="section-heading"><span>02 /</span> Your Learning Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"### Welcome, {st.session_state['generated_name']} 👋"
    )
    st.caption(
        f"{st.session_state['generated_class']} · "
        f"Plan generated on {st.session_state['generated_date']}"
    )

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "Average score",
            f"{average_score}%",
            help="Mean of the four topic scores."
        )

    with m2:
        st.metric(
            "Priority topic",
            weakest_topic.split(" — ")[0],
            f"{active_scores[weakest_topic]}%"
        )

    with m3:
        st.metric(
            "Topics tracked",
            len(active_scores)
        )

    with m4:
        st.metric(
            "Suggested practice",
            f"{total_practice} min",
            help="Sum of the topic-level practice suggestions."
        )

    # Tabs keep the dashboard organised.
    tab_dashboard, tab_plan, tab_routine, tab_quiz, tab_method = st.tabs([
        "📊 Dashboard",
        "🎯 Practice Plan",
        "🌱 Daily Balance",
        "🧠 Recall Lab",
        "🔬 How It Works"
    ])

    # ---------------- DASHBOARD TAB ----------------------

    with tab_dashboard:
        left, right = st.columns([1.4, 1])

        with left:
            st.markdown("### Topic Performance")

            chart_df = pd.DataFrame({
                "Topic": list(active_scores.keys()),
                "Score": list(active_scores.values())
            })

            fig = px.bar(
                chart_df,
                x="Topic",
                y="Score",
                color="Score",
                range_y=[0, 100],
                color_continuous_scale=[
                    "#FF6584",
                    "#246BFD",
                    "#00E5FF",
                    "#00FFB3"
                ],
                text="Score",
                title="Your current topic snapshot"
            )

            fig.update_traces(
                texttemplate="%{text}%",
                textposition="outside",
                marker_line_width=0
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    color="#DDF7FF",
                    family="Inter, sans-serif"
                ),
                title_font=dict(size=18, color="#73F5FF"),
                xaxis=dict(
                    title="",
                    tickfont=dict(color="#C5E7F6"),
                    gridcolor="rgba(0,229,255,.10)"
                ),
                yaxis=dict(
                    title="Score (%)",
