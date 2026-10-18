import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(page_title="AB SCHOOL LOOP AI | Student Growth Studio", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

# Transparent rule-based prototype; not a trained ML model.
def classify_topic(score):
    if score < 50:
        return "Needs support", "High", "Rebuild the core idea, then solve 5 guided questions.", 25
    if score < 75:
        return "Growing", "Medium", "Revise key concepts and solve 5 mixed questions.", 15
    return "Strong", "Low", "Use spaced revision and try 2 challenge questions.", 5


def make_plan(scores, study_minutes, screen_minutes, activity_minutes):
    rows = []
    for topic, score in sorted(scores.items(), key=lambda item: item[1]):
        status, priority, action, mins = classify_topic(score)
        rows.append({"Topic": topic, "Quiz score (%)": score, "Status": status,
                     "Priority": priority, "Suggested action": action, "Suggested minutes": mins})
    total = sum(row["Suggested minutes"] for row in rows)
    habit = ("Start with one focused 25-minute study block and a 5-minute break."
             if study_minutes < 30 else "Use focused blocks, short breaks, and a brief end-of-day review.")
    screen = ("Try a screen-free break and keep entertainment screen time separate from study."
              if screen_minutes > 180 else "Keep balancing study, entertainment, sleep, and offline time.")
    activity = ("Consider a short movement break or outdoor activity."
                if activity_minutes < 30 else "Nice routine signal—keep regular movement and rest in your day.")
    return pd.DataFrame(rows), total, habit, screen, activity

st.markdown("""
<style>
:root { color-scheme: light; }
.stApp { background: radial-gradient(circle at 5% 0%, #e9f2ff 0, transparent 28%), linear-gradient(180deg,#f7f9ff 0%,#ffffff 48%,#f7fbfa 100%); }
.block-container { max-width: 1440px; padding-top: 1.2rem; padding-bottom: 2.5rem; }
[data-testid="stSidebar"] { background: linear-gradient(180deg,#101d3a 0%,#172b50 100%); }
[data-testid="stSidebar"] * { color: #f5f7ff !important; }
[data-testid="stSidebar"] input, [data-testid="stSidebar"] [data-baseweb="select"] { color: #17213b !important; }
.hero { position:relative; overflow:hidden; padding:2.1rem 2.2rem; border-radius:28px; color:white; background:linear-gradient(115deg,#101d3a 0%,#214b87 54%,#347d91 100%); box-shadow:0 18px 45px rgba(22,50,92,.18); }
.hero:after { content:'✦'; position:absolute; right:5%; top:-45px; font-size:180px; color:rgba(255,255,255,.10); }
.eyebrow { letter-spacing:.18em; text-transform:uppercase; font-size:.75rem; font-weight:800; color:#c7ddff; }
.hero h1 { color:#fff !important; font-size:clamp(2rem,4vw,3.3rem); line-height:1.05; margin:.45rem 0 .6rem 0; }
.hero p { color:#e5efff; font-size:1.05rem; max-width:720px; margin-bottom:0; }
.pill-row { display:flex; flex-wrap:wrap; gap:.5rem; margin-top:1.2rem; }
.pill { border:1px solid rgba(255,255,255,.28); background:rgba(255,255,255,.10); border-radius:999px; padding:.42rem .75rem; font-size:.82rem; color:#fff; }
.section-kicker { color:#3b68a5; font-size:.76rem; font-weight:800; letter-spacing:.13em; text-transform:uppercase; margin-bottom:.15rem; }
.section-title { color:#172849; font-size:1.55rem; font-weight:800; margin-top:0; margin-bottom:.35rem; }
.subtle { color:#64748b; }
div[data-testid="stMetric"] { background:linear-gradient(150deg,#fff,#f4f8ff); border:1px solid #e4ebf7; padding:1rem 1.1rem; border-radius:18px; box-shadow:0 8px 22px rgba(24,52,91,.05); }
div[data-testid="stMetricLabel"] { color:#64748b; }
div[data-testid="stMetricValue"] { color:#172849; }
div.stButton > button[kind="primary"] { border:0; border-radius:14px; background:linear-gradient(100deg,#e76e51,#f19a55); color:white; font-weight:800; min-height:3rem; box-shadow:0 8px 18px rgba(231,110,81,.22); }
div.stButton > button[kind="primary"]:hover { border:0; filter:brightness(1.04); }
[data-testid="stVerticalBlockBorderWrapper"] { border-radius:17px; border-color:#e3eaf5; background:rgba(255,255,255,.82); }
div[data-testid="stAlert"] { border-radius:14px; }
hr { border-color:#e5ebf4; }
.footer { color:#8190a8; font-size:.82rem; text-align:center; padding:1.2rem 0 .4rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="eyebrow">Student growth • Learning science • Healthy habits</div>
  <h1>GURUKUL LOOP AI</h1>
  <p>Your learning day, made clearer. Turn quiz results into a practical next-step plan—while keeping focus, movement, and screen balance in view.</p>
  <div class="pill-row"><span class="pill">🎯 Personal practice plan</span><span class="pill">📊 Topic insights</span><span class="pill">🌱 Balanced routine</span><span class="pill">🧪 Transparent prototype</span></div>
</div>
""", unsafe_allow_html=True)

st.write("")
with st.expander("ℹ️ About this demo — please read", expanded=False):
    st.write("This student project currently uses a transparent rule-based baseline, not a trained machine-learning model. It offers educational suggestions only; it is not a medical or psychological assessment. The score thresholds are initial design choices and must be evaluated with consented data before making effectiveness claims.")

with st.sidebar:
    st.markdown("## 👤 Student profile")
    st.caption("Personalise the demo using sample or permission-approved data.")
    student_name = st.text_input("Student name", value="Demo Student")
    grade = st.selectbox("Class / grade", ["Class 8", "Class 9", "Class 10", "Class 11", "Class 12"] , index=3)
    st.markdown("---")
    st.markdown("## 🕒 Daily rhythm")
    study_minutes = st.slider("Focused study today (min)", 0, 360, 90, 15)
    screen_minutes = st.slider("Non-study screen time (min)", 0, 600, 120, 15)
    activity_minutes = st.slider("Physical activity (min)", 0, 180, 30, 5)
    st.markdown("---")
    st.caption("🔒 Demo tip: avoid real student names or private information when presenting publicly.")

st.markdown('<div class="section-kicker">01 / Your learning snapshot</div><div class="section-title">Add your latest quiz scores</div><div class="subtle">Use the sample values to explore the prototype, or update them from a quiz you are allowed to use.</div>', unsafe_allow_html=True)
default_scores = {"Physics · Motion": 42, "Chemistry · Bonding": 68, "Mathematics · Trigonometry": 81, "English · Comprehension": 55}
cols = st.columns(4, gap="medium")
scores = {}
for col, (topic, default) in zip(cols, default_scores.items()):
    with col:
        with st.container(border=True):
            st.markdown(f"**{topic}**")
            scores[topic] = st.number_input("Score (%)", min_value=0, max_value=100, value=default, step=1, key=f"score_{topic}", label_visibility="collapsed")
            val = scores[topic]
            label = "Needs support" if val < 50 else ("Growing" if val < 75 else "Strong")
            st.caption(f"{['🔴','🟠','🟢'][0 if val < 50 else (1 if val < 75 else 2)]} {label}")

if st.button("✨ Build my personal learning loop", type="primary", use_container_width=True):
    st.session_state["generated"] = True
    st.session_state["scores"] = scores
    st.session_state["routine"] = (study_minutes, screen_minutes, activity_minutes)
    st.session_state["student"] = student_name.strip() or "Demo Student"
    st.session_state["grade"] = grade

if st.session_state.get("generated"):
    current_scores = st.session_state["scores"]
    sm, scm, am = st.session_state["routine"]
    df, total, habit, screen, activity = make_plan(current_scores, sm, scm, am)
    avg = round(sum(current_scores.values()) / len(current_scores), 1)
    weak_topic = min(current_scores, key=current_scores.get)
    st.write("")
    st.markdown('<div class="section-kicker">02 / Your personalised output</div><div class="section-title">Your next steps, at a glance</div>', unsafe_allow_html=True)
    st.caption(f"Prepared for {st.session_state['student']} · {st.session_state['grade']} · {date.today().strftime('%d %b %Y')}")
    k1, k2, k3, k4 = st.columns(4, gap="medium")
    k1.metric("Average quiz score", f"{avg}%", help="Average of the four entered scores")
    k2.metric("First focus topic", weak_topic.split(" · ")[0], help="Lowest entered quiz score")
    k3.metric("Topics reviewed", f"{len(current_scores)} / 4")
    k4.metric("Suggested practice", f"{total} min")
    left, right = st.columns([1.05, 1], gap="large")
    with left:
        with st.container(border=True):
            st.markdown("**📊 Topic performance**")
            fig = px.bar(df.sort_values("Quiz score (%)", ascending=True), x="Quiz score (%)", y="Topic", orientation="h", color="Priority", text="Quiz score (%)", range_x=[0, 100], color_discrete_map={"High":"#e76e51", "Medium":"#e9ad55", "Low":"#2a9d8f"})
            fig.update_traces(texttemplate="%{text}%", textposition="outside", cliponaxis=False, marker_line_width=0)
            fig.update_layout(height=360, margin=dict(l=8,r=28,t=15,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#35445f"), xaxis=dict(title="Score (%)", gridcolor="#e7edf5", zeroline=False), yaxis=dict(title="", gridcolor="rgba(0,0,0,0)"), legend_title_text="Priority")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with right:
        st.markdown("**🧭 Recommended next steps**")
        for _, row in df.iterrows():
            with st.container(border=True):
                badge = {"High":"🔴 HIGH", "Medium":"🟠 MEDIUM", "Low":"🟢 LOW"}[row["Priority"]]
                st.markdown(f"**{row['Topic']}**  ·  {badge}")
                st.write(row["Suggested action"])
                st.caption(f"Suggested practice time: {row['Suggested minutes']} minutes")
    st.markdown('<div class="section-kicker">03 / Healthy routine</div><div class="section-title">Small habits that support learning</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="section-kicker">04 / Take it with you</div><div class="section-title">Export your demo results</div>', unsafe_allow_html=True)
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("⬇️ Download recommendation report (CSV)", data=csv, file_name="gurukul_loop_recommendations.csv", mime="text/csv")
else:
    st.write("")
    st.info("👆 Enter or keep the sample scores, then select **Build my personal learning loop** to see the dashboard, practice recommendations, and routine reminders.")

st.write("")
st.markdown('<div class="section-kicker">The idea behind the loop</div><div class="section-title">Measure → Understand → Practise → Reflect</div>', unsafe_allow_html=True)
steps = st.columns(4, gap="medium")
for col, icon, title, desc in zip(steps, ["📝", "🔎", "🎯", "🔁"], ["Measure", "Understand", "Practise", "Reflect"], ["Enter quiz results", "Find the first topic to focus on", "Follow a small next step", "Review progress after the next quiz"]):
    with col:
        with st.container(border=True):
            st.markdown(f"### {icon} {title}")
            st.caption(desc)



st.markdown('<div class="section-kicker">05 / Interactive practice</div><div class="section-title">Recall Lab — test what you remember</div><div class="subtle">આ demo quiz છે. જવાબ પસંદ કરો અને તરત feedback મેળવો.</div>', unsafe_allow_html=True)
quiz_bank = {
    "Physics": {"q": "SI unit of velocity કયું છે?", "options": ["m/s", "m/s²", "Newton", "Joule"], "answer": "m/s", "why": "Velocity = displacement / time, તેથી SI unit metre per second (m/s) છે."},
    "Chemistry": {"q": "Covalent bond સામાન્ય રીતે કેવી રીતે બને છે?", "options": ["Electrons share કરીને", "Protons share કરીને", "Neutrons transfer કરીને", "Nucleus split કરીને"], "answer": "Electrons share કરીને", "why": "Covalent bondમાં atoms electron pair share કરે છે."},
    "Mathematics": {"q": "sin²θ + cos²θ બરાબર કેટલું?", "options": ["0", "1", "2", "tan θ"], "answer": "1", "why": "આ fundamental trigonometric identity છે: sin²θ + cos²θ = 1."},
    "English": {"q": "Choose the correct synonym of 'rapid'.", "options": ["Slow", "Quick", "Quiet", "Weak"], "answer": "Quick", "why": "Rapid means fast or quick."}
}
q_subject = st.selectbox("Choose a subject", list(quiz_bank.keys()), key="recall_subject")
q = quiz_bank[q_subject]
st.markdown(f"**{q['q']}**")
answer = st.radio("તમારો જવાબ પસંદ કરો", q["options"], key=f"recall_answer_{q_subject}", horizontal=False)
if st.button("Check my answer", key="check_recall", type="primary"):
    if answer == q["answer"]:
        st.success("સાચો જવાબ! હવે કારણ યાદ કરીને પોતાના શબ્દોમાં સમજાવવાનો પ્રયત્ન કર.")
    else:
        st.warning(f"હજી શીખવાની તક છે. સાચો જવાબ: {q['answer']}")
    st.info(q["why"])

st.markdown('<div class="section-kicker">06 / Project transparency</div><div class="section-title">How the current prototype works</div>', unsafe_allow_html=True)
arch1, arch2, arch3 = st.columns(3, gap="medium")
with arch1:
    with st.container(border=True):
        st.markdown("### 1. Measure")
        st.write("Student enters quiz scores and daily routine values.")
with arch2:
    with st.container(border=True):
        st.markdown("### 2. Rule-based analysis")
        st.write("Fixed score thresholds identify a suggested priority and practice time.")
with arch3:
    with st.container(border=True):
        st.markdown("### 3. Reflect & improve")
        st.write("Student follows the suggestion, takes another quiz, and compares progress.")
st.caption("Research note: this version does not train a machine-learning model or automatically verify student performance. Any impact claims require testing with appropriate consent and real evaluation data.")

st.markdown('<div class="footer">GURUKUL LOOP AI · Student research prototype · Version 0.2 · Designed for learning support, not diagnosis</div>', unsafe_allow_html=True)
