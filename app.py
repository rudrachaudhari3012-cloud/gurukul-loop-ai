import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(
    page_title="GURUKUL LOOP AI | Student Growth Studio",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 1. RULE-BASED LEARNING ENGINE
# Transparent prototype — not a trained ML model.
# =========================================================

def classify_topic(score):
    if score < 50:
        return (
            "Needs support",
            "High",
            "Rebuild the core idea, then solve 5 guided questions.",
            25
        )
    if score < 75:
        return (
            "Growing",
            "Medium",
            "Revise key concepts and solve 5 mixed questions.",
            15
        )
    return (
        "Strong",
        "Low",
        "Use spaced revision and try 2 challenge questions.",
        5
    )


def make_plan(scores, study_minutes, screen_minutes, activity_minutes):
    rows = []

    for topic, score in sorted(
        scores.items(),
        key=lambda item: item[1]
    ):
        status, priority, action, mins = classify_topic(score)

        rows.append({
            "Topic": topic,
            "Quiz score (%)": score,
            "Status": status,
            "Priority": priority,
            "Suggested action": action,
            "Suggested minutes": mins
        })

    total = sum(row["Suggested minutes"] for row in rows)

    habit = (
        "Start with one focused 25-minute study block and a 5-minute break."
        if study_minutes < 30
        else "Use focused blocks, short breaks, and a brief end-of-day review."
    )

    screen = (
        "Try a screen-free break and keep entertainment screen time separate from study."
        if screen_minutes > 180
        else "Keep balancing study, entertainment, sleep, and offline time."
    )

    activity = (
        "Consider a short movement break or outdoor activity."
        if activity_minutes < 30
        else "Nice routine signal—keep regular movement and rest in your day."
    )

    return pd.DataFrame(rows), total, habit, screen, activity


# =========================================================
# 2. PURPLE NEON DESIGN SYSTEM
# Theme: Purple Neon + Mixed Background + Glow Effects
# =========================================================

st.markdown("""
<style>

/* ---------- COLOR VARIABLES ---------- */

:root {
    color-scheme: light;

    --purple-deep: #100B20;
    --purple-dark: #1A1033;
    --purple-card: #28154B;
    --purple-main: #8B5CF6;
    --purple-bright: #A970FF;
    --purple-pink: #D946EF;
    --purple-soft: #F3EDFF;
    --purple-border: #E5D9FF;
    --text-main: #24163D;
    --text-muted: #766A8D;
    --white: #FFFFFF;
}

/* ---------- MAIN BACKGROUND ---------- */

.stApp {
    background:
        radial-gradient(
            circle at 5% 0%,
            rgba(169, 112, 255, 0.12) 0,
            transparent 28%
        ),
        radial-gradient(
            circle at 95% 35%,
            rgba(217, 70, 239, 0.07) 0,
            transparent 25%
        ),
        linear-gradient(
            180deg,
            #F8F5FF 0%,
            #FFFFFF 48%,
            #F7F4FF 100%
        );

    color: var(--text-main);
}

/* ---------- PAGE WIDTH ---------- */

.block-container {
    max-width: 1440px;
    padding-top: 1.2rem;
    padding-bottom: 2.5rem;
}

/* ---------- SIDEBAR ---------- */

[data-testid="stSidebar"] {
    background:
        radial-gradient(
            circle at 0% 0%,
            rgba(169, 112, 255, 0.17),
            transparent 38%
        ),
        linear-gradient(
            180deg,
            #100B20 0%,
            #1A1033 55%,
            #24113F 100%
        );

    border-right: 1px solid rgba(169, 112, 255, 0.25);
}

[data-testid="stSidebar"] * {
    color: #F6F0FF !important;
}

[data-testid="stSidebar"] input {
    color: #24163D !important;
    background: #FFFFFF !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] {
    color: #24163D !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #24163D !important;
}

[data-testid="stSidebar"] [data-baseweb="slider"] {
    accent-color: #A970FF;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.15);
}

/* ---------- HERO SECTION ---------- */

.hero {
    position: relative;
    overflow: hidden;

    padding: 2.1rem 2.2rem;
    border-radius: 28px;

    color: white;

    background:
        radial-gradient(
            circle at 90% 5%,
            rgba(217, 70, 239, 0.28),
            transparent 30%
        ),
        linear-gradient(
            115deg,
            #100B20 0%,
            #28154B 53%,
            #6030A0 100%
        );

    border: 1px solid rgba(169, 112, 255, 0.30);

    box-shadow:
        0 18px 45px rgba(53, 24, 91, 0.18),
        0 0 25px rgba(139, 92, 246, 0.10);
}

.hero:after {
    content: '✦';

    position: absolute;
    right: 5%;
    top: -45px;

    font-size: 180px;
    color: rgba(255, 255, 255, 0.09);

    pointer-events: none;
}

.eyebrow {
    letter-spacing: 0.18em;
    text-transform: uppercase;

    font-size: 0.75rem;
    font-weight: 800;

    color: #D9C5FF;
}

.hero h1 {
    color: #FFFFFF !important;

    font-size: clamp(2rem, 4vw, 3.3rem);
    line-height: 1.05;

    margin: 0.45rem 0 0.6rem 0;

    text-shadow:
        0 0 18px rgba(169, 112, 255, 0.28);
}

.hero p {
    color: #EDE4FF;

    font-size: 1.05rem;
    max-width: 720px;

    margin-bottom: 0;
}

.pill-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;

    margin-top: 1.2rem;
}

.pill {
    border: 1px solid rgba(255, 255, 255, 0.24);

    background: rgba(255, 255, 255, 0.08);

    border-radius: 999px;
    padding: 0.42rem 0.75rem;

    font-size: 0.82rem;
    color: #FFFFFF;

    backdrop-filter: blur(8px);

    transition: all 0.25s ease;
}

.pill:hover {
    background: rgba(169, 112, 255, 0.22);
    border-color: #C4A5FF;
}

/* ---------- SECTION HEADINGS ---------- */

.section-kicker {
    color: #8650D6;

    font-size: 0.76rem;
    font-weight: 800;

    letter-spacing: 0.13em;
    text-transform: uppercase;

    margin-bottom: 0.15rem;
}

.section-title {
    color: #24163D;

    font-size: 1.55rem;
    font-weight: 800;

    margin-top: 0;
    margin-bottom: 0.35rem;
}

.subtle {
    color: #766A8D;
}

/* ---------- METRIC CARDS ---------- */

div[data-testid="stMetric"] {
    background:
        linear-gradient(
            145deg,
            #FFFFFF 0%,
            #F7F2FF 100%
        );

    border: 1px solid #E5D9FF;

    padding: 1rem 1.1rem;
    border-radius: 18px;

    box-shadow:
        0 8px 22px rgba(53, 24, 91, 0.06);

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease,
        border-color 0.25s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);

    border-color: #C4A5FF;

    box-shadow:
        0 12px 28px rgba(139, 92, 246, 0.13),
        0 0 12px rgba(169, 112, 255, 0.08);
}

div[data-testid="stMetricLabel"] {
    color: #766A8D;
}

div[data-testid="stMetricValue"] {
    color: #6030A0;
}

/* ---------- GLOW BUTTONS ---------- */

div.stButton > button[kind="primary"] {
    border: 1px solid #B99AFF;
    border-radius: 14px;

    background:
        linear-gradient(
            100deg,
            #7C3AED 0%,
            #A855F7 55%,
            #D946EF 100%
        );

    color: #FFFFFF;
    font-weight: 800;

    min-height: 3rem;

    box-shadow:
        0 0 10px rgba(169, 112, 255, 0.38),
        0 0 22px rgba(139, 92, 246, 0.18),
        0 8px 18px rgba(76, 29, 149, 0.18);

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease,
        filter 0.25s ease;
}

div.stButton > button[kind="primary"]:hover {
    border-color: #E9D5FF;

    filter: brightness(1.10);
    transform: translateY(-2px);

    box-shadow:
        0 0 14px rgba(169, 112, 255, 0.62),
        0 0 32px rgba(217, 70, 239, 0.24),
        0 10px 24px rgba(76, 29, 149, 0.24);
}

div.stButton > button[kind="primary"]:active {
    transform: translateY(0);
}

/* ---------- SECONDARY BUTTONS ---------- */

div.stButton > button:not([kind="primary"]) {
    border: 1px solid #D7C5FF;
    border-radius: 12px;

    background: #FFFFFF;
    color: #6030A0;

    font-weight: 700;

    transition: all 0.2s ease;
}

div.stButton > button:not([kind="primary"]):hover {
    border-color: #A970FF;

    background: #F6F0FF;
    color: #51258B;

    box-shadow:
        0 0 12px rgba(169, 112, 255, 0.15);
}

/* ---------- DOWNLOAD BUTTON ---------- */

div.stDownloadButton > button {
    border: 1px solid #B99AFF;
    border-radius: 12px;

    background: linear-gradient(
        100deg,
        #6D28D9,
        #A855F7
    );

    color: #FFFFFF;
    font-weight: 700;

    transition: all 0.25s ease;

    box-shadow:
        0 0 12px rgba(139, 92, 246, 0.20);
}

div.stDownloadButton > button:hover {
    border-color: #D8B4FE;

    filter: brightness(1.08);

    box-shadow:
        0 0 18px rgba(169, 112, 255, 0.35);
}

/* ---------- CONTENT CARDS ---------- */

[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 17px !important;

    border: 1px solid #E5D9FF !important;

    background: rgba(255, 255, 255, 0.88) !important;

    box-shadow:
        0 6px 18px rgba(53, 24, 91, 0.035);

    transition:
        border-color 0.25s ease,
        box-shadow 0.25s ease,
        transform 0.25s ease;
}

[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: #D0B7FF !important;

    box-shadow:
        0 10px 24px rgba(139, 92, 246, 0.075);
}

/* ---------- INPUTS ---------- */

div[data-baseweb="input"] {
    border-radius: 10px;
}

div[data-baseweb="input"]:focus-within {
    border-color: #A970FF !important;

    box-shadow:
        0 0 0 2px rgba(169, 112, 255, 0.16);
}

div[data-baseweb="select"]:focus-within {
    border-color: #A970FF !important;
}

/* ---------- RADIO BUTTONS ---------- */

div[data-testid="stRadio"] label {
    color: #35224F;
}

/* ---------- ALERTS ---------- */

div[data-testid="stAlert"] {
    border-radius: 14px;
}

/* ---------- EXPANDER ---------- */

[data-testid="stExpander"] {
    border: 1px solid #E5D9FF;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.78);
}

/* ---------- DIVIDERS ---------- */

hr {
    border-color: #E9E0F8;
}

/* ---------- FOOTER ---------- */

.footer {
    color: #8B7CA4;

    font-size: 0.82rem;
    text-align: center;

    padding: 1.2rem 0 0.4rem;
}

/* ---------- ACCESSIBILITY ---------- */

button:focus-visible,
input:focus-visible {
    outline: 2px solid #A970FF !important;
    outline-offset: 3px;
}

/* ---------- REDUCED MOTION ---------- */

@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        transition: none !important;
        animation: none !important;
    }
}

/* ---------- MOBILE ---------- */

@media (max-width: 768px) {
    .hero {
        padding: 1.5rem 1.25rem;
        border-radius: 20px;
    }

    .hero:after {
        font-size: 120px;
        right: 0;
    }

    .section-title {
        font-size: 1.3rem;
    }

    .pill {
        font-size: 0.75rem;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. HERO / WELCOME SECTION
# =========================================================

st.markdown("""
<div class="hero">

    <div class="eyebrow">
        Student Growth • Learning Science • Healthy Habits
    </div>

    <h1>GURUKUL LOOP AI</h1>

    <p>
        Your learning day, made clearer.
        Turn quiz results into a practical next-step plan—
        while keeping focus, movement, and screen balance in view.
    </p>

    <div class="pill-row">
        <span class="pill">🎯 Personal practice plan</span>
        <span class="pill">📊 Topic insights</span>
        <span class="pill">🌱 Balanced routine</span>
        <span class="pill">🧪 Transparent prototype</span>
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# 4. ABOUT THE PROJECT
# =========================================================

st.write("")

with st.expander("ℹ️ About this demo — please read", expanded=False):
    st.write(
        "This student project currently uses a transparent "
        "rule-based baseline, not a trained machine-learning model. "
        "It offers educational suggestions only; it is not a medical "
        "or psychological assessment. The score thresholds are initial "
        "design choices and must be evaluated with consented data "
        "before making effectiveness claims."
    )


# =========================================================
# 5. SIDEBAR — STUDENT PROFILE AND DAILY ROUTINE
# =========================================================

with st.sidebar:

    st.markdown("## 👤 Student profile")

    st.caption(
        "Personalise the demo using sample or permission-approved data."
    )

    student_name = st.text_input(
        "Student name",
        value="Demo Student"
    )

    grade = st.selectbox(
        "Class / grade",
        [
            "Class 8",
            "Class 9",
            "Class 10",
            "Class 11",
            "Class 12"
        ],
        index=3
    )

    st.markdown("---")

    st.markdown("## 🕒 Daily rhythm")

    study_minutes = st.slider(
        "Focused study today (min)",
        0, 360, 90, 15
    )

    screen_minutes = st.slider(
        "Non-study screen time (min)",
        0, 600, 120, 15
    )

    activity_minutes = st.slider(
        "Physical activity (min)",
        0, 180, 30, 5
    )

    st.markdown("---")

    st.caption(
        "🔒 Demo tip: avoid real student names or private "
        "information when presenting publicly."
    )


# =========================================================
# 6. LEARNING SNAPSHOT
# =========================================================

st.markdown("""
<div class="section-kicker">
    01 / Your learning snapshot
</div>

<div class="section-title">
    Add your latest quiz scores
</div>

<div class="subtle">
    Use the sample values to explore the prototype, or update
    them from a quiz you are allowed to use.
</div>
""", unsafe_allow_html=True)


default_scores = {
    "Physics · Motion": 42,
    "Chemistry · Bonding": 68,
    "Mathematics · Trigonometry": 81,
    "English · Comprehension": 55
}

cols = st.columns(4, gap="medium")
scores = {}

for col, (topic, default) in zip(cols, default_scores.items()):

    with col:

        with st.container(border=True):

            st.markdown(f"**{topic}**")

            scores[topic] = st.number_input(
                "Score (%)",
                min_value=0,
                max_value=100,
                value=default,
                step=1,
                key=f"score_{topic}",
                label_visibility="collapsed"
            )

            val = scores[topic]

            label = (
                "Needs support"
                if val < 50
                else ("Growing" if val < 75 else "Strong")
            )

            emoji = (
                "🔴" if val < 50
                else ("🟠" if val < 75 else "🟢")
            )

            st.caption(f"{emoji} {label}")


# =========================================================
# 7. BUILD PERSONAL LEARNING LOOP
# =========================================================

if st.button(
    "✨ Build my personal learning loop",
    type="primary",
    use_container_width=True
):

    st.session_state["generated"] = True

    st.session_state["scores"] = scores

    st.session_state["routine"] = (
        study_minutes,
        screen_minutes,
        activity_minutes
    )

    st.session_state["student"] = (
        student_name.strip() or "Demo Student"
    )

    st.session_state["grade"] = grade


# =========================================================
# 8. PERSONALIZED RESULTS DASHBOARD
# =========================================================

if st.session_state.get("generated"):

    current_scores = st.session_state["scores"]

    sm, scm, am = st.session_state["routine"]

    df, total, habit, screen, activity = make_plan(
        current_scores,
        sm,
        scm,
        am
    )

    avg = round(
        sum(current_scores.values()) / len(current_scores),
        1
    )

    weak_topic = min(
        current_scores,
        key=current_scores.get
    )

    st.write("")

    st.markdown("""
    <div class="section-kicker">
        02 / Your personalised output
    </div>

    <div class="section-title">
        Your next steps, at a glance
    </div>
    """, unsafe_allow_html=True)

    st.caption(
        f"Prepared for {st.session_state['student']} · "
        f"{st.session_state['grade']} · "
        f"{date.today().strftime('%d %b %Y')}"
    )

    k1, k2, k3, k4 = st.columns(4, gap="medium")

    k1.metric(
        "Average quiz score",
        f"{avg}%",
        help="Average of the four entered scores"
    )

    k2.metric(
        "First focus topic",
        weak_topic.split(" · ")[0],
        help="Lowest entered quiz score"
    )

    k3.metric(
        "Topics reviewed",
        f"{len(current_scores)} / 4"
    )

    k4.metric(
        "Suggested practice",
        f"{total} min"
    )

    left, right = st.columns([1.05, 1], gap="large")

    # ---------- TOPIC PERFORMANCE CHART ----------

    with left:

        with st.container(border=True):

            st.markdown("**📊 Topic performance**")

            fig = px.bar(
                df.sort_values(
                    "Quiz score (%)",
                    ascending=True
                ),
                x="Quiz score (%)",
                y="Topic",
                orientation="h",
                color="Priority",
                text="Quiz score (%)",
                range_x=[0, 100],

                color_discrete_map={
                    "High": "#D946EF",
                    "Medium": "#A970FF",
                    "Low": "#6D28D9"
                }
            )

            fig.update_traces(
                texttemplate="%{text}%",
                textposition="outside",
                cliponaxis=False,
                marker_line_width=0
            )

            fig.update_layout(
                height=360,

                margin=dict(
                    l=8,
                    r=28,
                    t=15,
                    b=10
                ),

                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",

                font=dict(
                    color="#493660",
                    family="Arial"
                ),

                xaxis=dict(
                    title="Score (%)",
                    gridcolor="#E9E0F8",
                    zeroline=False,
                    tickfont=dict(color="#766A8D"),
                    title_font=dict(color="#493660")
                ),

                yaxis=dict(
                    title="",
                    gridcolor="rgba(0,0,0,0)",
                    tickfont=dict(color="#493660")
                ),

                legend_title_text="Priority",

                legend=dict(
                    font=dict(color="#493660")
                ),

                hoverlabel=dict(
                    bgcolor="#28154B",
                    font_color="#FFFFFF"
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )

    # ---------- RECOMMENDED NEXT STEPS ----------

    with right:

        st.markdown("**🧭 Recommended next steps**")

        for _, row in df.iterrows():

            with st.container(border=True):

                badge = {
                    "High": "🔴 HIGH",
                    "Medi
