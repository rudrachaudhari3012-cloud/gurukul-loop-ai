import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

# ==========================================
# AB SCHOOL LOOP AI
# Cyber AI Theme
# Midnight Blue + Electric Cyan + Neon Mint
# ==========================================

st.set_page_config(
    page_title="AB SCHOOL LOOP AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------
# CYBER AI COLOUR THEME — ULTRA GLOW
# ------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
    --midnight: #050816;
    --navy: #0B1230;
    --cyan: #00D6FF;
    --mint: #00F5B8;
    --white: #F4FAFF;
    --muted: #A8B9D4;
    --glass: rgba(12, 24, 55, 0.78);
    --border: rgba(0, 214, 255, 0.32);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 5%,
            rgba(0, 214, 255, 0.17), transparent 34%),
        radial-gradient(ellipse at 90% 20%,
            rgba(0, 245, 184, 0.13), transparent 35%),
        radial-gradient(ellipse at 50% 100%,
            rgba(75, 70, 255, 0.16), transparent 40%),
        linear-gradient(135deg, #050816 0%, #0B1230 48%, #050816 100%);
    color: var(--white);
}

.stApp::before {
    content: "";
    position: fixed;
    z-index: 0;
    width: 420px;
    height: 420px;
    top: 8%;
    right: -8%;
    border-radius: 50%;
    background: rgba(0, 214, 255, 0.10);
    filter: blur(85px);
    pointer-events: none;
}

.stApp::after {
    content: "";
    position: fixed;
    z-index: 0;
    width: 350px;
    height: 350px;
    bottom: 4%;
    left: -8%;
    border-radius: 50%;
    background: rgba(0, 245, 184, 0.09);
    filter: blur(80px);
    pointer-events: none;
}

[data-testid="stHeader"] {
    background: rgba(5, 8, 22, 0.4);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B1230, #060A1C);
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * {
    color: var(--white);
}

.block-container {
    position: relative;
    z-index: 1;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

h1, h2, h3, h4 {
    color: var(--white) !important;
    letter-spacing: -0.5px;
}

p, label, .stMarkdown, [data-testid="stCaptionContainer"] {
    color: var(--muted);
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 38px 32px;
    border-radius: 25px;
    border: 1px solid rgba(0, 214, 255, 0.40);
    background:
        linear-gradient(120deg,
            rgba(0, 214, 255, 0.13),
            rgba(11, 18, 48, 0.92) 45%,
            rgba(0, 245, 184, 0.10));
    box-shadow:
        0 0 22px rgba(0, 214, 255, 0.20),
        0 0 65px rgba(0, 214, 255, 0.09),
        inset 0 0 25px rgba(0, 214, 255, 0.04);
    margin-bottom: 25px;
}

.hero::before {
    content: "";
    position: absolute;
    z-index: 0;
    width: 400px;
    height: 400px;
    right: -10%;
    top: 10%;
    border-radius: 50%;
    background: rgba(0, 214, 185, 0.10);
    filter: blur(55px);
    pointer-events: none;
}

.hero-content {
    position: relative;
    z-index: 1;
}

.hero h1 {
    font-size: clamp(2rem, 5vw, 3.4rem);
    font-weight: 900;
    line-height: 1.12;
    margin: 0;
    background: linear-gradient(90deg, #FFFFFF, #00D6FF, #00F5B8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 13px rgba(0, 214, 255, 0.30));
}

.hero-subtitle {
    font-size: 1.02rem;
    margin-top: 14px;
    color: #C2D6F3;
    max-width: 760px;
    line-height: 1.7;
}

.eyebrow {
    display: inline-block;
    padding: 7px 12px;
    border-radius: 30px;
    border: 1px solid rgba(0, 245, 184, 0.45);
    background: rgba(0, 245, 184, 0.08);
    color: #00F5B8;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 1.4px;
    margin-bottom: 16px;
}

.glass-card {
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: 19px;
    padding: 22px;
    box-shadow:
        0 0 16px rgba(0, 214, 255, 0.08),
        inset 0 0 18px rgba(0, 214, 255, 0.025);
    margin-bottom: 16px;
    transition: all 0.25s ease;
}

.glass-card:hover {
    border-color: rgba(0, 245, 184, 0.55);
    box-shadow:
        0 0 24px rgba(0, 214, 255, 0.14),
        0 0 42px rgba(0, 245, 184, 0.06);
    transform: translateY(-2px);
}

.card-title {
    color: #00D6FF;
    font-size: 1.02rem;
    font-weight: 800;
    margin-bottom: 10px;
}

.card-description {
    color: #A8B9D4;
    line-height: 1.65;
    font-size: 0.9rem;
}

div[data-testid="stMetric"] {
    background: linear-gradient(135deg,
        rgba(0, 214, 255, 0.10),
        rgba(12, 24, 55, 0.82));
    border: 1px solid rgba(0, 214, 255, 0.30);
    border-radius: 17px;
    padding: 18px 20px;
    box-shadow: 0 0 18px rgba(0, 214, 255, 0.07);
}

div[data-testid="stMetricLabel"] {
    color: #A8B9D4 !important;
}

div[data-testid="stMetricValue"] {
    color: #00F5B8 !important;
    font-weight: 900;
    text-shadow: 0 0 12px rgba(0, 245, 184, 0.22);
}

.stButton > button {
    background: linear-gradient(100deg, #00D6FF, #00F5B8);
    color: #04101F !important;
    border: 0;
    border-radius: 12px;
    padding: 0.72rem 1.25rem;
    font-weight: 900;
    box-shadow: 0 0 18px rgba(0, 214, 255, 0.24);
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow:
        0 0 25px rgba(0, 214, 255, 0.40),
        0 0 35px rgba(0, 245, 184, 0.16);
    border: 1px solid #FFFFFF;
}

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background: rgba(5, 8, 22, 0.85) !important;
    color: #F4FAFF !important;
    border: 1px solid rgba(0, 214, 255, 0.32) !important;
    border-radius: 10px !important;
}

.stSelectbox [data-baseweb="select"] > div {
    background: #0B1230;
    color: #F4FAFF;
    border-color: rgba(0, 214, 255, 0.32);
}

.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: #00F5B8;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(8, 15, 37, 0.7);
    padding: 7px;
    border: 1px solid rgba(0, 214, 255, 0.20);
    border-radius: 14px;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #A8B9D4;
    border-radius: 9px;
    font-weight: 700;
}

.stTabs [aria-selected="true"] {
    background: rgba(0, 214, 255, 0.15) !important;
    color: #00F5B8 !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 13px;
    overflow: hidden;
}

hr {
    border-color: rgba(0, 214, 255, 0.22);
}

div[data-testid="stAlert"] {
    border-radius: 13px;
    border: 1px solid rgba(0, 214, 255, 0.25);
}

.footer {
    text-align: center;
    padding: 25px 10px;
    color: #7F95B7;
    font-size: 0.8rem;
    border-top: 1px solid rgba(0, 214, 255, 0.17);
    margin-top: 35px;
}

.small-tag {
    color: #00F5B8;
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.8px;
}

div[data-testid="stExpander"] {
    border: 1px solid rgba(0, 214, 255, 0.25);
    border-radius: 13px;
    background: rgba(10, 19, 45, 0.55);
}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------
# LEARNING LOGIC
# ------------------------------------------

def classify_topic(score):
    if score < 40:
        return "Needs Support"
    elif score < 60:
        return "Building"
    elif score < 80:
        return "Developing"
    return "Strong"


def make_plan(scores, study_minutes, screen_minutes, activity_minutes):
    recommendations = []

    for topic, score in scores.items():
        if score < 40:
            priority = "High"
            practice = 30
            action = "Revise fundamentals and solve guided examples."
        elif score < 60:
            priority = "Medium"
            practice = 20
            action = "Review key concepts and practise basic questions."
        elif score < 80:
            priority = "Normal"
            practice = 15
            action = "Practise mixed questions and correct mistakes."
        else:
            priority = "Maintain"
            practice = 10
            action = "Use spaced revision and challenge questions."

        recommendations.append({
            "Topic": topic,
            "Score (%)": score,
            "Status": classify_topic(score),
            "Priority": priority,
            "Practice (min)": practice,
            "Suggested Action": action
        })

    plan_df = pd.DataFrame(recommendations)
    plan_df = plan_df.sort_values("Score (%)", ascending=True)

    balance = {
        "Study minutes": study_minutes,
        "Screen minutes": screen_minutes,
        "Activity minutes": activity_minutes
    }

    return plan_df, balance


# ------------------------------------------
# HERO
# ------------------------------------------

st.markdown("""
<div class="hero">
  <div class="hero-content">
    <div class="eyebrow">AI-POWERED STUDENT LEARNING SUPPORT</div>
    <h1>AB SCHOOL LOOP AI</h1>
    <div class="hero-subtitle">
      Measure learning. Understand progress. Practise with purpose.
      Build a healthier and more balanced learning routine.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="glass-card">
  <div class="card-title">✦ Your Personal Learning Dashboard</div>
  <div class="card-description">
    Explore topic performance, receive practice suggestions and reflect on
    your daily learning habits. This is a student research prototype, not a
    diagnostic or fully trained machine-learning system.
  </div>
</div>
""", unsafe_allow_html=True)


# ------------------------------------------
# SIDEBAR
# ------------------------------------------

st.sidebar.markdown("""
<div style="padding:10px 0 18px 0;">
  <div style="color:#00F5B8;font-size:0.75rem;font-weight:900;
  letter-spacing:1.5px;">AB SCHOOL LOOP AI</div>
  <h2 style="color:#F4FAFF;margin-top:5px;">Control Panel</h2>
  <div style="color:#A8B9D4;font-size:0.85rem;">
    Personalise your learning session
  </div>
</div>
""", unsafe_allow_html=True)

student_name = st.sidebar.text_input("Student name", value="Student")
student_class = st.sidebar.selectbox(
    "Class",
    ["Class 8", "Class 9", "Class 10", "Class 11", "Class 12"],
    index=3
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Daily Rhythm")

study_minutes = st.sidebar.slider(
    "Focused study (minutes)",
    min_value=0,
    max_value=600,
    value=180,
    step=15
)

screen_minutes = st.sidebar.slider(
    "Non-study screen time (minutes)",
    min_value=0,
    max_value=600,
    value=120,
    step=15
)

activity_minutes = st.sidebar.slider(
    "Physical activity (minutes)",
    min_value=0,
    max_value=240,
    value=45,
    step=5
)

st.sidebar.markdown("---")
st.sidebar.caption("Cyber AI theme • Ultra Glow")


# ------------------------------------------
# TOPIC SCORE INPUTS
# ------------------------------------------

st.markdown("## 📊 Learning Performance")
st.caption("Enter your recent test or practice scores as percentages.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    physics_score = st.number_input(
        "Physics — Motion",
        min_value=0,
        max_value=100,
        value=42,
        step=1
    )

with col2:
    chemistry_score = st.number_input(
        "Chemistry — Bonding",
        min_value=0,
        max_value=100,
        value=68,
        step=1
    )

with col3:
    maths_score = st.number_input(
        "Mathematics — Trigonometry",
        min_value=0,
        max_value=100,
        value=81,
        step=1
    )

with col4:
    english_score = st.number_input(
        "English — Comprehension",
        min_value=0,
        max_value=100,
        value=55,
        step=1
    )

scores = {
    "Physics — Motion": physics_score,
    "Chemistry — Bonding": chemistry_score,
    "Mathematics — Trigonometry": maths_score,
    "English — Comprehension": english_score
}

generate = st.button(
    "⚡ Generate My Learning Plan",
    use_container_width=True
)

if "generated" not in st.session_state:
    st.session_state.generated = False

if generate:
    st.session_state.generated = True
    st.session_state.plan_scores = scores.copy()
    st.session_state.plan_name = student_name
    st.session_state.plan_class = student_class
    st.session_state.plan_data = make_plan(
        scores,
        study_minutes,
        screen_minutes,
        activity_minutes
    )

if st.session_state.generated:
    plan_df, balance = st.session_state.plan_data
    display_scores = st.session_state.plan_scores
    average_score = sum(display_scores.values()) / len(display_scores)
    weakest_topic = min(display_scores, key=display_scores.get)
    strongest_topic = max(display_scores, key=display_scores.get)

    st.markdown("---")
    st.markdown(
        f"## Welcome, {st.session_state.plan_name} 👋"
    )
    st.caption(
        f"{st.session_state.plan_class} • Learning plan • {date.today()}"
    )

    # --------------------------------------
    # METRICS
    # --------------------------------------

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("Average Score", f"{average_score:.1f}%")

    with m2:
        st.metric("Needs Most Support", weakest_topic.split(" — ")[0])

    with m3:
        st.metric("Topics Tracked", len(display_scores))

    with m4:
        st.metric(
            "Suggested Practice",
            f"{int(plan_df['Practice (min)'].sum())} min"
        )

    # --------------------------------------
    # TABS
    # --------------------------------------

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard",
        "🎯 Practice Plan",
        "⚖️ Daily Balance",
        "🧠 Recall Lab",
        "🔬 How It Works"
    ])

    with tab1:
        st.markdown("### Topic Performance")

        chart_df = pd.DataFrame({
            "Topic": list(display_scores.keys()),
            "Score": list(display_scores.values())
        })

        fig = px.bar(
            chart_df,
            x="Topic",
            y="Score",
            color="Score",
            color_continuous_scale=[
                "#0B1230",
                "#00D6FF",
                "#00F5B8"
            ],
            range_y=[0, 100],
            text="Score"
        )

        fig.update_traces(
            texttemplate="%{text}%",
            textposition="outside",
            marker_line_color="#00D6FF",
            marker_line_width=1
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#DCEBFF",
            xaxis_title="",
            yaxis_title="Score (%)",
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=25, b=10),
            yaxis=dict(
                gridcolor="rgba(0,214,255,0.14)",
                zerolinecolor="rgba(0,214,255,0.18)"
            ),
            xaxis=dict(
                gridcolor="rgba(0,214,255,0.10)"
            )
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Learning Snapshot")

        left, right = st.columns(2)

        with left:
            st.markdown(f"""
            <div class="glass-card">
              <div class="card-title">🔎 Focus Area</div>
              <div class="card-description">
                <strong style="color:#00F5B8;">{weakest_topic}</strong>
                is your current lowest-scoring topic. Start with concept
                revision, then solve a few guided questions.
              </div>
            </div>
            """, unsafe_allow_html=True)

        with right:
            st.markdown(f"""
            <div class="glass-card">
              <div class="card-title">🚀 Strength to Maintain</div>
              <div class="card-description">
                <strong style="color:#00F5B8;">{strongest_topic}</strong>
                is your strongest topic. Keep it active with short,
                spaced-revision sessions.
              </div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### Personalised Practice Plan")
        st.caption(
            "Suggestions are generated from score ranges using transparent rules."
        )

        for _, row in plan_df.iterrows():
            st.markdown(f"""
            <div class="glass-card">
              <div class="card-title">{row['Topic']}</div>
              <div class="card-description">
                Score: <strong style="color:#00F5B8;">
                {row['Score (%)']}%</strong>
                &nbsp; | &nbsp; Status: {row['Status']}
                &nbsp; | &nbsp; Priority: {row['Priority']}
                <br><br>
                <strong style="color:#00D6FF;">
                Suggested practice: {row['Practice (min)']} minutes
                </strong>
                <br>
                {row['Suggested Action']}
              </div>
            </div>
            """, unsafe_allow_html=True)

        csv_data = plan_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Download Practice Plan (CSV)",
            data=csv_data,
            file_name="ab_school_loop_recommendations.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.dataframe(
            plan_df,
            use_container_width=True,
            hide_index=True
        )

    with tab3:
        st.markdown("### Daily Balance Check")

        balance_cols = st.columns(3)

        with balance_cols[0]:
            st.metric("Focused Study", f"{study_minutes} min")

        with balance_cols[1]:
            st.metric("Non-study Screen", f"{screen_minutes} min")

        with balance_cols[2]:
            st.metric("Physical Activity", f"{activity_minutes} min")

        if activity_minutes < 30:
            st.info(
                "Try adding a little more movement to your day, "
                "such as walking, outdoor play or stretching."
            )
        else:
            st.success(
                "You have included physical activity in your routine. "
                "Keep balancing study, rest and movement."
            )

        if screen_minutes > study_minutes:
            st.info(
                "Consider short screen breaks and a clear stopping time "
                "for entertainment apps."
            )
        else:
            st.success(
                "Your reported non-study screen time is not higher than "
                "your focused study time."
            )

        routine_df = pd.DataFrame({
            "Activity": [
                "Focused study",
                "Non-study screen time",
                "Physical activity"
            ],
            "Minutes": [
                study_minutes,
                screen_minutes,
                activity_minutes
            ]
        })

        balance_fig = px.bar(
            routine_df,
            x="Activity",
            y="Minutes",
            color="Activity",
            color_discrete_sequence=[
                "#00D6FF",
                "#7C83FF",
                "#00F5B8"
            ]
        )

        balance_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#DCEBFF",
            showlegend=False,
            margin=dict(l=10, r=10, t=20, b=10),
            yaxis=dict(
                gridcolor="rgba(0,214,255,0.14)"
            )
        )

        st.plotly_chart(balance_fig, use_container_width=True)

        st.caption(
            "This section provides general routine suggestions, not medical advice."
        )

    with tab4:
        st.markdown("### 🧠 Recall Lab")
        st.caption(
            "Try a short question to practise re
