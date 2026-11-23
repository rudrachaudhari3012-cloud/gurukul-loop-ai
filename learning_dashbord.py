
# ============================================================
# AB SCHOOL LOOP AI
# PREMIUM LEARNING DASHBOARD
# Design 2 + Neon Intelligence Combination
# Midnight AI Learning Studio
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import streamlit as st

def show_learning_dashboard(style_chart):
    st.title("📚 Learning Dashboard")

    st.write("Welcome to Learning Dashboard")

# ============================================================
# THEME
# ============================================================

BG = "#061225"
CARD = "#0B1D35"
CYAN = "#22D3EE"
MINT = "#5EEAD4"
PURPLE = "#A78BFA"
GOLD = "#FBBF24"
WHITE = "#F4F8FF"
MUTED = "#A9BCD2"


# ============================================================
# MAIN FUNCTION
# ============================================================

def show_learning_dashboard():

    # --------------------------------------------------------
    # SESSION STATE
    # --------------------------------------------------------

    if "learning_stream" not in st.session_state:
        st.session_state.learning_stream = None

    if "learning_scores" not in st.session_state:
        st.session_state.learning_scores = {}

    if "learning_plan" not in st.session_state:
        st.session_state.learning_plan = False

    # --------------------------------------------------------
    # PREMIUM CSS
    # --------------------------------------------------------

    st.markdown("""
    <style>

    .learning-hero {
        background:
        radial-gradient(circle at 85% 20%,
        rgba(34,211,238,.20), transparent 35%),
        linear-gradient(120deg,#102A49,#071629,#102C46);

        padding:35px 30px;
        border-radius:24px;
        border:1px solid #164E73;
        box-shadow:0 0 30px rgba(34,211,238,.12);
        margin-bottom:25px;
    }

    .learning-hero h1 {
        color:#F4F8FF;
        font-size:38px;
        font-weight:850;
        margin-bottom:5px;
    }

    .learning-hero p {
        color:#9EDFF1;
        font-size:15px;
    }

    .eyebrow {
        color:#22D3EE;
        font-size:11px;
        letter-spacing:3px;
        font-weight:800;
    }

    .subject-card {
        background:linear-gradient(145deg,#102B49,#08182D);
        border:1px solid #164C70;
        border-radius:19px;
        padding:20px;
        min-height:180px;
        box-shadow:0 5px 22px rgba(0,0,0,.25);
        transition:all .3s ease;
        margin-bottom:12px;
    }

    .subject-card:hover {
        transform:translateY(-5px);
        border-color:#22D3EE;
        box-shadow:0 0 22px rgba(34,211,238,.22);
    }

    .subject-icon {
        font-size:35px;
    }

    .subject-name {
        color:#FFFFFF;
        font-size:19px;
        font-weight:800;
        margin-top:10px;
    }

    .subject-score {
        font-size:35px;
        font-weight:900;
        margin:7px 0;
    }

    .subject-status {
        display:inline-block;
        background:#123E49;
        color:#5EEAD4;
        padding:6px 13px;
        border-radius:30px;
        font-size:12px;
        font-weight:700;
    }

    .section-title {
        color:#F4F8FF;
        font-size:23px;
        font-weight:800;
        margin-top:22px;
        margin-bottom:15px;
    }

    .premium-panel {
        background:linear-gradient(145deg,#102B49,#071629);
        border:1px solid #164C70;
        padding:22px;
        border-radius:20px;
        margin-bottom:15px;
    }

    .plan-banner {
        background:
        radial-gradient(circle at 10% 50%,
        rgba(167,139,250,.3),transparent 30%),
        linear-gradient(110deg,#073B68,#075985,#123C66);

        border:1px solid #22D3EE;
        border-radius:20px;
        padding:25px;
        text-align:center;
        box-shadow:0 0 22px rgba(34,211,238,.17);
    }

    .plan-banner h2 {
        color:white;
        font-size:25px;
        font-weight:850;
    }

    .plan-banner p {
        color:#A5F3FC;
    }

    div.stButton > button {
        background:linear-gradient(100deg,#0891B2,#2563EB);
        color:white;
        border:1px solid #22D3EE;
        border-radius:12px;
        font-weight:800;
        min-height:45px;
        transition:.3s;
    }

    div.stButton > button:hover {
        box-shadow:0 0 20px rgba(34,211,238,.4);
        border-color:#5EEAD4;
        color:white;
    }

    div[data-testid="stMetric"] {
        background:#10243D;
        border:1px solid #164C70;
        padding:15px;
        border-radius:15px;
    }

    div[data-testid="stMetricLabel"] {
        color:#A9BCD2;
    }

    div[data-testid="stMetricValue"] {
        color:#22D3EE;
    }

    </style>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown("""
    <div class="learning-hero">

        <div class="eyebrow">
        AB SCHOOL LOOP AI • LEARNING INTELLIGENCE
        </div>

        <h1>🎓 Learning Dashboard</h1>

        <p>
        Track Your Progress • Improve Your Skills •
        Reach Your Goals
        </p>

        <h3 style="color:#FFFFFF;">
        ✨ Small Steps Today... Big Success Tomorrow!
        </h3>

        <p>
        Your Learning Journey Starts Here.
        </p>

    </div>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # STREAM SELECTION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">🚀 Choose Your Science Stream</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Select your stream to unlock your personalized learning dashboard."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("⚛️ PCM", use_container_width=True):
            st.session_state.learning_stream = "PCM"
            st.rerun()

    with c2:
        if st.button("🧬 PCB", use_container_width=True):
            st.session_state.learning_stream = "PCB"
            st.rerun()

    with c3:
        if st.button("🔬 PCMB", use_container_width=True):
            st.session_state.learning_stream = "PCMB"
            st.rerun()

    # --------------------------------------------------------
    # STREAM DETAILS
    # --------------------------------------------------------

    stream = st.session_state.learning_stream

    if stream is None:

        st.info(
            "👆 Select PCM, PCB or PCMB to open your Learning Dashboard."
        )

        st.markdown("""
        <div class="premium-panel">

        <h2 style="color:#22D3EE;text-align:center;">
        YOUR FUTURE STARTS HERE
        </h2>

        <p style="color:#B8C7D9;text-align:center;">
        Personalized Learning • Smart Progress Tracking
        • Better Performance
        </p>

        </div>
        """, unsafe_allow_html=True)

        return

    subjects_by_stream = {
        "PCM": [
            ("Physics", "⚛️", CYAN),
            ("Chemistry", "🧪", MINT),
            ("Mathematics", "📐", PURPLE),
            ("English", "📖", GOLD)
        ],

        "PCB": [
            ("Physics", "⚛️", CYAN),
            ("Chemistry", "🧪", MINT),
            ("Biology", "🧬", PURPLE),
            ("English", "📖", GOLD)
        ],

        "PCMB": [
            ("Physics", "⚛️", CYAN),
            ("Chemistry", "🧪", MINT),
            ("Mathematics", "📐", PURPLE),
            ("Biology", "🧬", GOLD),
            ("English", "📖", "#F472B6")
        ]
    }

    subjects = subjects_by_stream[stream]

    st.success(f"Your selected stream: {stream}")

    if st.button("🔄 Change Stream"):
        st.session_state.learning_stream = None
        st.rerun()

    # --------------------------------------------------------
    # SUBJECT SCORES
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">📚 Your Subject Performance</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Update your recent subject scores to track your progress."
    )

    cols = st.columns(4)

    for index, (name, icon, color) in enumerate(subjects):

        key = f"learning_score_{stream}_{name}"

        if key not in st.session_state:
            st.session_state[key] = 65

        with cols[index % 4]:

            st.markdown(f"""
            <div class="subject-card">

                <div class="subject-icon">{icon}</div>

                <div class="subject-name">{name}</div>

                <div class="subject-score"
                style="color:{color};">
                {st.session_state[key]}%
                </div>

            </div>
            """, unsafe_allow_html=True)

            score = st.slider(
                f"{name} Score",
                0,
                100,
                value=st.session_state[key],
                key=f"slider_{stream}_{name}"
            )

            st.session_state[key] = score

            if score < 50:
                st.warning("⚠️ Needs Support")
            elif score < 75:
                st.info("📈 Growing")
            else:
                st.success("⭐ Strong")

    # --------------------------------------------------------
    # OVERALL PERFORMANCE
    # --------------------------------------------------------

    scores = {
        name: st.session_state[f"learning_score_{stream}_{name}"]
        for name, icon, color in subjects
    }

    overall = round(sum(scores.values()) / len(scores))

    st.markdown(
        '<div class="section-title">📊 Overall Performance</div>',
        unsafe_allow_html=True
    )

    p1, p2, p3 = st.columns(3)

    p1.metric("Overall Score", f"{overall}%")

    p2.metric(
        "Strong Subjects",
        sum(1 for x in scores.values() if x >= 75)
    )

    p3.metric(
        "Need Support",
        sum(1 for x in scores.values() if x < 50)
    )

    # Progress Ring
    fig = go.Figure(go.Pie(
        values=[overall, 100 - overall],
        hole=0.76,
        marker=dict(
            colors=[CYAN, "#18304B"],
            line=dict(color=BG, width=2)
        ),
        textinfo="none",
        sort=False
    ))

    fig.update_layout(
        annotations=[dict(
            text=f"<b>{overall}%</b>",
            x=0.5,
            y=0.5,
            font=dict(size=32, color="white"),
            showarrow=False
        )],
        showlegend=False,
        height=250,
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)

    # --------------------------------------------------------
    # BUILD LEARNING PLAN
    # --------------------------------------------------------

    st.markdown("""
    <div class="plan-banner">

        <h2>⚡ Build My Learning Plan</h2>

        <p>
        Get Your Personalized Study Plan with AI
        </p>

    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "🚀 GENERATE MY LEARNING PLAN",
        use_container_width=True
    ):
        st.session_state.learning_plan = True

    if st.session_state.learning_plan:

        st.markdown(
            '<div class="section-title">🎯 Your Learning Plan</div>',
            unsafe_allow_html=True
        )

        sorted_subjects = sorted(
            scores.items(),
            key=lambda item: item[1]
        )

        for name, score in sorted_subjects:

            if score < 50:
                st.error(
                    f"🔴 {name}: Focus on fundamentals and practice questions."
                )

            elif score < 75:
                st.info(
                    f"🟡 {name}: Revise important concepts and solve more questions."
                )

            else:
                st.success(
                    f"🟢 {name}: Maintain performance and try advanced questions."
                )

        st.caption(
            "This is a rule-based personalized recommendation prototype, "
            "not a trained AI prediction model."
        )

    # --------------------------------------------------------
    # QUICK ACTIONS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">⚡ Quick Actions</div>',
        unsafe_allow_html=True
    )

    q1, q2, q3, q4 = st.columns(4)

    with q1:
        st.markdown("### 🎮")
        st.write("Take Quiz")

    with q2:
        st.markdown("### 🧠")
        st.write("Boost Mind Power")

    with q3:
        st.markdown("### 📈")
        st.write("View Analytics")

    with q4:
        st.markdown("### 📄")
        st.write("PDF Report")

    # --------------------------------------------------------
    # LEARNING JOURNEY
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">📅 Your Learning Journey</div>',
        unsafe_allow_html=True
    )

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    progress_data = [35, 42, 50, 47, 63, 67, overall]

    journey = pd.DataFrame({
        "Day": days,
        "Progress": progress_data
    })

    chart = px.line(
        journey,
        x="Day",
        y="Progress",
        markers=True
    )

    chart.update_traces(
        line=dict(color=CYAN, width=4),
        marker=dict(size=10, color=MINT)
    )

    chart.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=WHITE,
        yaxis=dict(
            range=[0, 100],
            gridcolor="#19344E"
        ),
        xaxis=dict(
            gridcolor="#19344E"
        ),
        height=300,
        margin=dict(t=20, b=20, l=10, r=10)
    )

    st.plotly_chart(chart, use_container_width=True)

    # --------------------------------------------------------
    # STUDY TIPS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">💡 Smart Study Tips</div>',
        unsafe_allow_html=True
    )

    weakest = min(scores, key=scores.get)

    st.markdown(f"""
    <div class="premium-panel">

        <h3 style="color:#22D3EE;">
        🤖 Your Learning Assistant
        </h3>

        <p style="color:#F4F8FF;">
        Your current focus subject is
        <b>{weakest}</b>.
        </p>

        <p style="color:#A9BCD2;">
        • Revise important concepts regularly.<br>
        • Practice questions after learning each topic.<br>
        • Review your mistakes and track improvements.<br>
        • Take short breaks between study sessions.
        </p>

    </div>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.markdown("""
    <div style="
    text-align:center;
    padding:25px;
    color:#22D3EE;
    border-top:1px solid #164C70;
    margin-top:30px;">

    <h3>∞ AB SCHOOL LOOP AI</h3>

    <p style="color:#A9BCD2;">
    Learn • Grow • Thrive
    </p>

    <p style="color:#FBBF24;">
    Keep Learning... Keep Growing... 🚀
    </p>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# END OF LEARNING DASHBOARD
# ============================================================
# render_learning_dashboard()
