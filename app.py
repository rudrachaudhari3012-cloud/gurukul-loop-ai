import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(
    page_title="AB SCHOOL LOOP AI | Student Growth Studio",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Transparent rule-based prototype; not a trained ML model.
def classify_topic(score):
    if score < 50:
        return (
            "Needs support", "High",
            "Rebuild the core idea, then solve 5 guided questions.", 25
        )
    if score < 75:
        return (
            "Growing", "Medium",
            "Revise key concepts and solve 5 mixed questions.", 15
        )
    return (
        "Strong", "Low",
        "Use spaced revision and try 2 challenge questions.", 5
    )


def make_plan(scores, study_minutes, screen_minutes, activity_minutes):
    rows = []

    for topic, score in sorted(scores.items(), key=lambda item: item[1]):
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


# --------------------------------------------------
# A + C MIX THEME
# Midnight Blue + Electric Cyan + Emerald + Mint
# --------------------------------------------------

st.markdown("""
<style>
:root {
    color-scheme: dark;

    --bg: #0B1020;
    --bg-secondary: #0E172A;
    --panel: #111C30;
    --panel-hover: #15243A;
    --emerald: #123D32;
    --cyan: #66F2FF;
    --mint: #55F7B0;
    --text: #EAF6FF;
    --muted: #9CB2C8;
    --border: rgba(102, 242, 255, 0.18);
}

/* Main background */
.stApp {
    background:
        radial-gradient(
            circle at 8% 3%,
            rgba(102, 242, 255, 0.10),
            transparent 26%
        ),
        radial-gradient(
            circle at 92% 22%,
            rgba(85, 247, 176, 0.08),
            transparent 25%
        ),
        linear-gradient(
            145deg,
            #080D19 0%,
            #0B1020 48%,
            #0D1D28 100%
        );
    color: var(--text);
}

/* Main page layout */
.block-container {
    max-width: 1440px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* General text */
.stApp,
.stApp p,
.stApp label,
.stApp li {
    color: var(--text);
}

.stMarkdown,
.stCaption,
[data-testid="stCaptionContainer"] {
    color: var(--muted);
}

h1, h2, h3, h4 {
    color: var(--text);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background:
        radial-gradient(
            circle at 10% 5%,
            rgba(102, 242, 255, 0.09),
            transparent 32%
        ),
        linear-gradient(
            180deg,
            #0B1020 0%,
            #10251F 100%
        );
    border-right: 1px solid rgba(85, 247, 176, 0.16);
}

[data-testid="stSidebar"] * {
    color: #EAF6FF;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
    color: var(--mint);
}

[data-testid="stSidebar"] input {
    color: #EAF6FF !important;
    background: #111C30 !important;
}

/* Select boxes */
[data-baseweb="select"] > div {
    background-color: #111C30;
    border-color: rgba(102, 242, 255, 0.28);
    border-radius: 10px;
    color: #EAF6FF;
}

[data-baseweb="popover"] {
    background: #111C30;
}

[data-baseweb="menu"] {
    background: #111C30;
}

[data-baseweb="menu"] * {
    color: #EAF6FF;
}

/* Hero section */
.hero {
    position: relative;
    overflow: hidden;
    padding: 2.5rem 2.3rem;
    border-radius: 26px;
    color: white;

    background:
        radial-gradient(
            circle at 90% 10%,
            rgba(102, 242, 255, 0.19),
            transparent 32%
        ),
        linear-gradient(
            120deg,
            #10182E 0%,
            #123D32 55%,
            #0C5260 100%
        );

    border: 1px solid rgba(102, 242, 255, 0.28);

    box-shadow:
        0 0 24px rgba(102, 242, 255, 0.07),
        0 18px 48px rgba(0, 0, 0, 0.30);
}

.hero:after {
    content: '✦';
    position: absolute;
    right: 5%;
    top: -55px;
    font-size: 190px;
    color: rgba(102, 242, 255, 0.10);
    pointer-events: none;
}

.eyebrow {
    letter-spacing: 0.18em;
    text-transform: uppercase;
    font-size: 0.75rem;
    font-weight: 800;
    color: var(--mint);
}

.hero h1 {
    color: #FFFFFF !important;
    font-size: clamp(2rem, 4vw, 3.35rem);
    line-height: 1.08;
    margin: 0.55rem 0 0.75rem 0;
    text-shadow: 0 0 22px rgba(102, 242, 255, 0.15);
}

.hero p {
    color: #D9F7F8;
    font-size: 1.05rem;
    max-width: 740px;
    margin-bottom: 0;
    line-height: 1.7;
}

.pill-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    margin-top: 1.35rem;
}

.pill {
    border: 1px solid rgba(102, 242, 255, 0.35);
    background: rgba(11, 16, 32, 0.40);
    border-radius: 999px;
    padding: 0.48rem 0.8rem;
    font-size: 0.82rem;
    color: #E8FFFF;
    backdrop-filter: blur(8px);
}

/* Section headings */
.section-kicker {
    color: var(--mint);
    font-size: 0.76rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}

.section-title {
    color: #F0FCFF;
    font-size: 1.55rem;
    font-weight: 800;
    margin-top: 0;
    margin-bottom: 0.45rem;
}

.subtle {
    color: #9CB2C8;
}

/* Cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    background:
        linear-gradient(
            145deg,
            rgba(20, 34, 54, 0.94),
            rgba(12, 25, 39, 0.96)
        );
    border: 1px solid rgba(102, 242, 255, 0.16);
    border-radius: 18px;

    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.14);

    transition:
        border-color 0.25s ease,
        box-shadow 0.25s ease,
        transform 0.25s ease;
}

[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: rgba(85, 247, 176, 0.45);
    box-shadow:
        0 0 18px rgba(102, 242, 255, 0.06),
        0 12px 30px rgba(0, 0, 0, 0.22);
}

/* Metrics */
div[data-testid="stMetric"] {
    background:
        linear-gradient(
            145deg,
            rgba(18, 61, 50, 0.60),
            rgba(17, 28, 48, 0.96)
        );

    border: 1px solid rgba(85, 247, 176, 0.24);
    padding: 1rem 1.1rem;
    border-radius: 17px;

    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.16);
}

div[data-testid="stMetricLabel"] {
    color: #AFC6D7;
}

div[data-testid="stMetricValue"] {
    color: var(--mint);
}

div[data-testid="stMetricDelta"] {
    color: var(--cyan);
}

/* Text inputs and number inputs */
.stTextInput input,
.stNumberInput input {
    background: #0D1728 !important;
    color: #EAF6FF !important;
    border: 1px solid rgba(102, 242, 255, 0.24) !important;
    border-radius: 10px !important;
}

.stTextInput input:focus,
.stNumberInput input:focus {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 0 1px rgba(102, 242, 255, 0.25) !important;
}

/* Sliders */
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: var(--mint);
    border-color: var(--mint);
}

.stSlider [data-testid="stTickBar"] {
    background: rgba(102, 242, 255, 0.35);
}

/* Buttons */
div.stButton > button {
    border: 1px solid rgba(102, 242, 255, 0.35);
    border-radius: 12px;
    background: #13283A;
    color: #EAF6FF;
    font-weight: 700;
    transition: all 0.25s ease;
}

div.stButton > button[kind="primary"] {
    border: 1px solid rgba(102, 242, 255, 0.75);
    border-radius: 13px;

    background:
        linear-gradient(
            100deg,
            #66F2FF 0%,
            #55F7B0 100%
        );

    color: #07131D;
    font-weight: 850;
    min-height: 3rem;

    box-shadow:
        0 0 12px rgba(102, 242, 255, 0.22),
        0 0 26px rgba(85, 247, 176, 0.10);
}

div.stButton > button[kind="primary"]:hover {
    border-color: #FFFFFF;
    color: #06121A;
    filter: brightness(1.06);

    box-shadow:
        0 0 18px rgba(102, 242, 255, 0.40),
        0 0 32px rgba(85, 247, 176, 0.20);

    transform: translateY(-1px);
}

div.stButton > button:not([kind="primary"]):hover {
    border-color: var(--mint);
    color: var(--mint);
    background: #152A35;
}

/* Download button */
[data-testid="stDownloadButton"] button {
    background: linear-gradient(100deg, #123D32, #0D5260);
    border: 1px solid rgba(85, 247, 176, 0.55);
    color: #EFFFF8;
    border-radius: 12px;
    font-weight: 750;
    transition: all 0.25s ease;
}

[data-testid="stDownloadButton"] button:hover {
    border-color: var(--mint);
    box-shadow: 0 0 18px rgba(85, 247, 176, 0.17);
}

/* Radio buttons */
[data-testid="stRadio"] label {
    color: #EAF6FF;
}

[data-testid="stRadio"] label:hover {
    color: var(--mint);
}

/* Expanders */
[data-testid="stExpander"] {
    background: rgba(17, 28, 48, 0.80);
    border: 1px solid rgba(102, 242, 255, 0.18);
    border-radius: 14px;
}

/* Alerts and information boxes */
div[data-testid="stAlert"] {
    border-radius: 14px;
    border: 1px solid rgba(102, 242, 255, 0.20);
    background: rgba(17, 36, 51, 0.88);
}

[data-testid="stAlert"] p {
    color: #EAF6FF;
}

/* Dividers */
hr {
    border-color: rgba(102, 242, 255, 0.16);
}

/* Captions */
[data-testid="stCaptionContainer"] {
    color: #9CB2C8;
}

/* Footer */
.footer {
    color: #8FAEBD;
    font-size: 0.82rem;
    text-align: center;
    padding: 1.5rem 0 0.5rem;
    border-top: 1px solid rgba(102, 242, 255, 0.13);
    margin-top: 1.8rem;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #0B1020;
}

::-webkit-scrollbar-thumb {
    background: #24544F;
    border-radius: 8px;
}

::-webkit-scrollbar-thumb:hover {
    background: #55F7B0;
}

/* Respect reduced-motion preferences */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        transition: none !important;
        animation: none !important;
    }
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HERO
# --------------------------------------------------

st.markdown("""
<div class="hero">
  <div class="eyebrow">Student growth • Learning science • Healthy habits</div>
  <h1>AB SCHOOL LOOP AI</h1>
  <p>
    Your learning day, made clearer. Turn quiz results into a practical
    next-step plan—while keeping focus, movement, and screen balance in view.
  </p>
  <div class="pill-row">
    <span class="pill">🎯 Personal practice plan</span>
    <span class="pill">📊 Topic insights</span>
    <span class="pill">🌱 Balanced routine</span>
    <span class="pill">🧪 Transparent prototype</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.write("")

with st.expander("ℹ️ About this demo — please read", expanded=False):
    st.write(
        "This student project currently uses a transparent rule-based baseline, "
        "not a trained machine-learning model. It offers educational suggestions "
        "only; it is not a medical or psychological assessment. The score "
        "thresholds are initial design choices and must be evaluated with "
        "consented data before making effectiveness claims."
    )


# --------------------------------------------------
# SIDEBAR: STUDENT PROFILE + DAILY RHYTHM
# --------------------------------------------------

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
        ["Class 8", "Class 9", "Class 10", "Class 11", "Class 12"],
        index=3
    )

    st.markdown("---")
    st.markdown("## 🕒 Daily rhythm")

    study_minutes = st.slider(
        "Focused study today (min)", 0, 360, 90, 15
    )

    screen_minutes = st.slider(
        "Non-study screen time (min)", 0, 600, 120, 15
    )

    activity_minutes = st.slider(
        "Physical activity (min)", 0, 180, 30, 5
    )

    st.markdown("---")
    st.caption(
        "🔒 Demo tip: avoid real student names or private information "
        "when presenting publicly."
    )


# --------------------------------------------------
# LEARNING SNAPSHOT
# --------------------------------------------------

st.markdown(
    '<div class="section-kicker">01 / Your learning snapshot</div>'
    '<div class="section-title">Add your latest quiz scores</div>'
    '<div class="subtle">Use the sample values to explore the prototype, '
    'or update them from a quiz you are allowed to use.</div>',
    unsafe_allow_html=True
)

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
                "Needs support" if val < 50
                else ("Growing" if val < 75 else "Strong")
            )

            emoji = (
                "🔴" if val < 50
                else ("🟠" if val < 75 else "🟢")
            )

            st.caption(f"{emoji} {label}")


# --------------------------------------------------
# GENERATE PERSONAL LEARNING LOOP
# --------------------------------------------------

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


# --------------------------------------------------
# PERSONALIZED RESULTS
# --------------------------------------------------

if st.session_state.get("generated"):

    current_scores = st.session_state["scores"]

    sm, scm, am = st.session_state["routine"]

    df, total, habit, screen, activity = make_plan(
        current_scores, sm, scm, am
    )

    avg = round(
        sum(current_scores.values()) / len(current_scores), 1
    )

    weak_topic = min(
        current_scores, key=current_scores.get
    )

    st.write("")

    st.markdown(
        '<div class="section-kicker">02 / Your personalised output</div>'
        '<div class="section-title">Your next steps, at a glance</div>',
        unsafe_allow_html=True
    )

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

    # Topic performance chart
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
                    "High": "#55F7B0",
                    "Medium": "#66F2FF",
                    "Low": "#238B72"
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
                margin=dict(l=8, r=28, t=15, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    color="#D9EAF5",
                    family="Arial"
                ),
                xaxis=dict(
                    title="Score (%)",
                    gridcolor="rgba(102,242,255,0.13)",
                    zeroline=False,
                    color="#AFC6D7"
                ),
                yaxis=dict(
                    title="",
                    gridcolor="rgba(0,0,0,0)",
                    color="#EAF6FF"
                ),
                legend_title_text="Priority",
                legend=dict(
                    font=dict(color="#D9EAF5")
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )

    # Recommended next steps
    with right:
        st.markdown("**🧭 Recommended next steps**")

        for _, row in df.iterrows():
            with st.container(border=True):

                badge = {
                    "High": "🟢 HIGH",
                    "Medium": "🔹 MEDIUM",
                    "Low": "🌿 LOW"
                }[row["Priority"]]

                st.markdown(
                    f"**{row['Topic']}** · {badge}"
                )

                st.write(row["Suggested action"])

                st.caption(
                    f"Suggested practice time: "
                    f"{row['Suggested minutes']} minutes"
                )

    # Healthy routine
    st.markdown(
        '<div class="section-kicker">03 / Healthy routine</div>'
        '<div class="section-title">Small habits that support learning</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        with st.container(border=True):
            st.markdown("### 📚 Focus")
            st.write(habit)

    with c2:
        with st.container(border=True):
            st.markdown("### 📵 Screen balance")
            st.write(screen)

    with c3:
        with st.container(border=True):
            st.markdown("### 🏃 Movement")
            st.write(activity)

    # CSV export
    st.markdown(
        '<div class="section-kicker">04 / Take it with you</div>'
        '<div class="section-title">Export your demo results</div>',
        unsafe_allow_html=True
    )

    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        "⬇️ Download recommendation report (CSV)",
        data=csv,
        file_name="ab_school_loop_recommendations.csv",
        mime="text/csv"
    )

else:
    st.writ
