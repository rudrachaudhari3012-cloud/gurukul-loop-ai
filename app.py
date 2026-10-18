import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(page_title="AB SCHOOL LOOP AI | Premium Learning Studio", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

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
    habit = ("Start with one focused 25-minute study block and a 5-minute break." if study_minutes < 30 else "Use focused blocks, short breaks, and a brief end-of-day review.")
    screen = ("Try a screen-free break and keep entertainment screen time separate from study." if screen_minutes > 180 else "Keep balancing study, entertainment, sleep, and offline time.")
    activity = ("Consider a short movement break or outdoor activity." if activity_minutes < 30 else "Nice routine signal—keep regular movement and rest in your day.")
    return pd.DataFrame(rows), total, habit, screen, activity

# Premium dark theme and responsive card styles
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Manrope:wght@400;600;700;800&display=swap');
:root { color-scheme: dark; }
.stApp { background: radial-gradient(ellipse at 10% 0%,rgba(0,204,255,.12),transparent 30%), radial-gradient(ellipse at 95% 8%,rgba(30,215,160,.10),transparent 25%), #07111f; color:#eaf2ff; }
.block-container { max-width:1480px; padding-top:1.25rem; padding-bottom:3rem; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#0b1930,#102747 70%,#0c1b2d); border-right:1px solid rgba(105,190,255,.15); }
[data-testid="stSidebar"] * { color:#eaf2ff; }
[data-testid="stSidebar"] input, [data-testid="stSidebar"] [data-baseweb="select"] { color:#102039 !important; }
[data-testid="stHeader"] { background:rgba(7,17,31,.82); }
.hero { position:relative; overflow:hidden; padding:clamp(1.5rem,4vw,3.2rem); border:1px solid rgba(106,215,255,.28); border-radius:28px; color:#fff; background:linear-gradient(120deg,#0d1c35 0%,#123b61 52%,#087d83 100%); box-shadow:0 24px 70px rgba(0,0,0,.28); }
.hero:after { content:'✦'; position:absolute; right:5%; top:-52px; font-size:210px; color:rgba(255,255,255,.08); pointer-events:none; }
.eyebrow { letter-spacing:.17em; text-transform:uppercase; font-size:.72rem; font-weight:800; color:#91f3ef; }
.hero h1 { color:#fff !important; font-size:clamp(2.3rem,5vw,4.4rem); font-weight:800; line-height:1.03; margin:.5rem 0 .75rem; }
.hero p { color:#d7eaff; font-size:1.08rem; max-width:780px; margin-bottom:0; }
.pill-row { display:flex; flex-wrap:wrap; gap:.55rem; margin-top:1.25rem; }
.pill { border:1px solid rgba(255,255,255,.23); background:rgba(255,255,255,.08); border-radius:999px; padding:.48rem .8rem; font-size:.8rem; color:#fff; }
.section-kicker { color:#5eead4; font-size:.72rem; font-weight:800; letter-spacing:.14em; text-transform:uppercase; margin:.25rem 0 .2rem; }
.section-title { color:#f0f7ff; font-size:1.55rem; font-weight:800; margin-top:0; margin-bottom:.4rem; }
.subtle, [data-testid="stCaptionContainer"] { color:#9fb3cb; }
div[data-testid="stMetric"] { background:linear-gradient(145deg,rgba(21,43,69,.95),rgba(11,27,45,.95)); border:1px solid rgba(107,190,230,.18); padding:1rem 1.1rem; border-radius:18px; box-shadow:0 10px 30px rgba(0,0,0,.15); }
div[data-testid="stMetricLabel"] { color:#a7bfd8; }
div[data-testid="stMetricValue"] { color:#f4fbff; }
[data-testid="stVerticalBlockBorderWrapper"] { border-radius:18px; border-color:rgba(111,190,230,.20); background:rgba(13,31,51,.76); }
div.stButton > button[kind="primary"], .stDownloadButton button { border:1px solid rgba(123,255,232,.3); border-radius:13px; background:linear-gradient(100deg,#00a6c7,#08b99a); color:#031523; font-weight:800; min-height:2.8rem; box-shadow:0 8px 24px rgba(0,190,180,.14); }
div.stButton > button:hover, .stDownloadButton button:hover { filter:brightness(1.12); border-color:#5eead4; }
.stTabs [data-baseweb="tab-list"] { gap:.35rem; background:rgba(12,29,48,.85); padding:.45rem; border-radius:15px; }
.stTabs [data-baseweb="tab"] { border-radius:10px; color:#bdd0e5; padding:.55rem .85rem; }
.stTabs [aria-selected="true"] { background:#123b54; color:#69f5e3; }
[data-testid="stAlert"] { border-radius:14px; }
hr { border-color:rgba(124,190,225,.16); }
.footer { color:#7f96b2; font-size:.8rem; text-align:center; padding:1.5rem 0 .4rem; }
.small-note { border-left:3px solid #28d5c1; padding:.6rem .9rem; background:rgba(40,213,193,.07); border-radius:0 10px 10px 0; color:#bdd4e8; }
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
  <div class="eyebrow">Student growth · Learning science · Healthy life</div>
  <h1>AB SCHOOL LOOP AI</h1>
  <p>Smart Learning · Healthy Life · Bright Future. A student-support prototype that turns quiz results into clear next steps while keeping healthy routines in view.</p>
  <div class="pill-row"><span class="pill">🧠 Mind power</span><span class="pill">📚 Smart learning</span><span class="pill">🏃 Healthy habits</span><span class="pill">🌱 Values & reflection</span><span class="pill">🔎 Transparent prototype</span></div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("# 🎓 AB SCHOOL LOOP AI")
    st.caption("Premium student growth studio")
    page = st.radio("Navigate", ["Overview", "Learning Dashboard", "Recall Quiz", "AI Coach", "Project Showcase", "Roadmap & Team", "Judge Q&A"], label_visibility="collapsed")
    st.divider()
    st.markdown("### 👤 Student profile")
    student_name = st.text_input("Student name", value="Demo Student")
    grade = st.selectbox("Class / grade", ["Class 8", "Class 9", "Class 10", "Class 11", "Class 12"], index=3)
    st.markdown("### 🕒 Daily rhythm")
    study_minutes = st.slider("Focused study today (min)", 0, 360, 90, 15)
    screen_minutes = st.slider("Non-study screen time (min)", 0, 600, 120, 15)
    activity_minutes = st.slider("Physical activity (min)", 0, 180, 30, 5)
    st.caption("Demo only: avoid entering private information for public presentations.")

st_scores = {"Physics · Motion": 42, "Chemistry · Bonding": 68, "Mathematics · Trigonometry": 81, "English · Comprehension": 55}
with st.expander("ℹ️ Prototype transparency", expanded=False):
    st.write("This version uses transparent rules and sample data; it is not a trained machine-learning model. It is not a medical or psychological assessment. Thresholds are initial design choices and must be evaluated using consented data before making effectiveness claims.")

if page == "Overview":
    st.markdown('<div class="section-kicker">01 / Project introduction</div><div class="section-title">A balanced loop for student growth</div>', unsafe_allow_html=True)
    st.write("AB SCHOOL LOOP AI is designed to help students notice what to practise next, reflect on quiz results, and remember that learning works best alongside movement, rest, and healthy screen habits.")
    a,b,c = st.columns(3)
    with a:
        with st.container(border=True): st.markdown("### 🧠 Mind power"); st.write("Short recall practice, reflection, and focused learning.")
    with b:
        with st.container(border=True): st.markdown("### 🏃 Healthy life"); st.write("Gentle reminders to balance study, movement, rest, and screens.")
    with c:
        with st.container(border=True): st.markdown("### 🤝 Values & support"); st.write("A supportive tool for students, teachers, and families—not a replacement for them.")
    st.markdown('<div class="section-kicker">02 / The learning loop</div><div class="section-title">Learn → Recall → Reflect → Improve</div>', unsafe_allow_html=True)
    loop = st.columns(4)
    for col, icon, title, desc in zip(loop, ["📘","🧩","🔎","🚀"], ["Learn","Recall","Reflect","Improve"], ["Study one clear concept.","Answer without looking at notes.","Understand mistakes and gaps.","Choose a small next practice step."]):
        with col:
            with st.container(border=True): st.markdown(f"### {icon} {title}"); st.caption(desc)
    st.markdown('<div class="section-kicker">03 / System overview</div><div class="section-title">From student input to useful next steps</div>', unsafe_allow_html=True)
    st.code("Student / Quiz Results  →  Rule-based Analysis  →  Suggested Practice Plan  →  Student Reflection  →  Next Quiz", language="text")
    st.markdown('<div class="small-note">Research principle: show how each suggestion is produced, test it with permission-based data, and report limitations honestly.</div>', unsafe_allow_html=True)

elif page == "Learning Dashboard":
    st.markdown('<div class="section-kicker">04 / Learning dashboard</div><div class="section-title">Build a personal practice plan</div>', unsafe_allow_html=True)
    st.caption("Change any score below, then build the plan. Sample scores are illustrative.")
    cols = st.columns(4, gap="medium"); scores = {}
    for col, (topic, default) in zip(cols, st_scores.items()):
        with col:
            with st.container(border=True):
                st.markdown(f"**{topic}**")
                scores[topic] = st.number_input("Quiz score (%)", 0, 100, default, 1, key=f"dash_{topic}")
                st.caption("🔴 Needs support" if scores[topic] < 50 else ("🟠 Growing" if scores[topic] < 75 else "🟢 Strong"))
    if st.button("✨ Build my learning plan", type="primary", use_container_width=True):
        st.session_state["plan_ready"] = True
        st.session_state["plan_scores"] = scores
        st.session_state["plan_routine"] = (study_minutes, screen_minutes, activity_minutes)
        st.session_state["plan_student"] = student_name.strip() or "Demo Student"
        st.session_state["plan_grade"] = grade
    if st.session_state.get("plan_ready"):
        current = st.session_state["plan_scores"]; sm, scm, am = st.session_state["plan_routine"]
        df, total, habit, screen, activity = make_plan(current, sm, scm, am)
        avg = round(sum(current.values())/len(current), 1); weak = min(current, key=current.get)
        st.caption(f"Prepared for {st.session_state['plan_student']} · {st.session_state['plan_grade']} · {date.today().strftime('%d %b %Y')}")
        k1,k2,k3,k4 = st.columns(4)
        k1.metric("Average score", f"{avg}%"); k2.metric("First focus", weak.split(" · ")[0]); k3.metric("Topics reviewed", f"{len(current)} / 4"); k4.metric("Suggested practice", f"{total} min")
        left,right = st.columns([1.05,1], gap="large")
        with left:
            with st.container(border=True):
                st.markdown("**📊 Topic performance**")
                fig = px.bar(df.sort_values("Quiz score (%)"), x="Quiz score (%)", y="Topic", orientation="h", color="Priority", text="Quiz score (%)", range_x=[0,100], color_discrete_map={"High":"#fb7185","Medium":"#fbbf24","Low":"#2dd4bf"})
                fig.update_traces(texttemplate="%{text}%", textposition="outside", cliponaxis=False)
                fig.update_layout(height=360, margin=dict(l=8,r=28,t=15,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#dcecff"), xaxis=dict(title="Score (%)",gridcolor="rgba(150,190,220,.15)"), yaxis=dict(title="",gridcolor="rgba(0,0,0,0)"), legend_title_text="Priority")
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        with right:
            st.markdown("**🧭 Recommended next steps**")
            for _, row in df.iterrows():
                with st.container(border=True):
                    st.markdown(f"**{row['Topic']}** · {row['Priority']} priority")
                    st.write(row["Suggested action"]); st.caption(f"Suggested time: {row['Suggested minutes']} minutes")
        st.markdown("### 🌿 Healthy routine signals")
        c1,c2,c3 = st.columns(3)
        for col, title, desc in [(c1,"📚 Focus",habit),(c2,"📵 Screen balance",screen),(c3,"🏃 Movement",activity)]:
            with col:
                with st.container(border=True): st.markdown(f"**{title}**"); st.write(desc)
        st.download_button("⬇️ Download practice report (CSV)", df.to_csv(index=False).encode("utf-8-sig"), "ab_school_loop_practice_report.csv", "text/csv")
    else:
        st.info("Adjust the sample scores if needed, then click **Build my learning plan**.")

elif page == "Recall Quiz":
    st.markdown('<div class="section-kicker">05 / Active recall lab</div><div class="section-title">Test what you remember</div>', unsafe_allow_html=True)
    st.write("Choose a subject, answer without checking notes, then read the explanation. This is a small demo quiz; it does not claim to measure overall intelligence.")
    subject = st.selectbox("Subject", ["Physics", "Chemistry", "Mathematics", "English"])
    quiz_bank = {
        "Physics": ("Which quantity is a vector?", ["Speed", "Distance", "Displacement", "Time"], "Displacement", "A vector has magnitude and direction. Displacement includes both."),
        "Chemistry": ("Which type of bond involves sharing electron pairs?", ["Ionic bond", "Covalent bond", "Metallic bond", "Hydrogen bond"], "Covalent bond", "A covalent bond forms when atoms share electron pairs."),
        "Mathematics": ("What is sin 30°?", ["0", "1/2", "√3/2", "1"], "1/2", "For the standard angle 30°, sin 30° = 1/2."),
        "English": ("Choose the closest meaning of ‘brief’. ", ["Short", "Angry", "Distant", "Heavy"], "Short", "‘Brief’ means short in duration or length.")}
    q, options, answer, explanation = quiz_bank[subject]
    st.markdown(f"#### {q}")
    selected = st.radio(
        "Select one answer",
        options,
        key=f"quiz_{subject}",
        on_change=lambda s=subject: st.session_state.pop(f"quiz_checked_{s}", None),
    )
    if st.button("Check answer", type="primary"):
        st.session_state[f"quiz_checked_{subject}"] = True
        st.session_state[f"quiz_correct_{subject}"] = selected == answer
    if st.session_state.get(f"quiz_checked_{subject}"):
        if st.session_state.get(f"quiz_correct_{subject}"):
            st.success("Correct! Nice recall.")
        else:
            st.warning(f"Not quite. Correct answer: {answer}")
        st.info(explanation)
        st.caption("Reflection prompt: What clue helped you choose, and what will you revise before trying again?")

elif page == "AI Coach":
    st.markdown('<div class="section-kicker">06 / Study coach</div><div class="section-title">A small next step beats a perfect plan</div>', unsafe_allow_html=True)
    mood = st.select_slider("How is your study energy today?", options=["Low", "Okay", "Good", "High"], value="Okay")
    goal = st.selectbox("What do you want to work on?", ["Understand a hard concept", "Remember formulas", "Improve reading comprehension", "Reduce distractions", "Build a balanced routine"])
    if st.button("Suggest my next step", type="primary"):
        suggestions = {
            "Understand a hard concept": "Study one example slowly, explain it in your own words, then solve two similar questions.",
            "Remember formulas": "Write the formula from memory, check it, and use it in one simple question and one mixed question.",
            "Improve reading comprehension": "Read a short passage, summarise it in two sentences, then answer who/what/why questions.",
            "Reduce distractions": "Put notifications away for one 20–25 minute block, then take a short break.",
            "Build a balanced routine": "Pick one realistic study block, include movement and rest, and keep entertainment screen time separate."}
        energy = "Start with just 10 minutes and make the first step easy." if mood == "Low" else "Try one focused block, then check how it felt." if mood == "Okay" else "Use your energy for one focused block and a short recall check."
        st.success(suggestions[goal]); st.info(energy)
    st.markdown('<div class="small-note">These are fixed, rule-based coaching prompts in this prototype, not AI-generated personalised predictions.</div>', unsafe_allow_html=True)

elif page == "Project Showcase":
    st.markdown('<div class="section-kicker">07 / Project proposal</div><div class="section-title">Problem, solution & system architecture</div>', unsafe_allow_html=True)
    st.markdown("### The problem")
    st.write("Students can find it difficult to decide what to practise next while balancing academic learning, physical activity, and screen time. A single score does not explain the next useful action.")
    st.markdown("### Proposed solution")
    st.write("AB SCHOOL LOOP AI combines quiz scores and self-reported routine inputs to create transparent practice suggestions and a reflection loop. The current prototype uses simple rules that can be tested and improved.")
    st.markdown("### System architecture")
    st.code("Student → Web App → Input Validation → Rule-based Analysis → Practice Plan + Charts → Student Reflection → Next Quiz", language="text")
    st.markdown("### Main modules")
    modules = st.columns(3)
    for col, icon, title, desc in zip(modules,["📘","🏃","🤝"],["Learning module","Health & fitness module","Behaviour & values module"],["Scores, recall quiz, practice plan.","Self-reported activity and screen-balance reminders.","Reflection, supportive habits, parent/teacher discussion."]):
        with col:
            with st.container(border=True): st.markdown(f"### {icon} {title}"); st.write(desc)
    st.markdown("### Hardware & software options")
    st.write("Software: Python, Streamlit, Pandas, Plotly; optional future ML libraries only after a clear research question and evaluation plan. Hardware is not required for the current software demo. Raspberry Pi/ESP32, camera or fitness sensors would be optional extensions and require consent, privacy safeguards, and a clear use case.")
    budget = pd.DataFrame([("Raspberry Pi / ESP32", "₹1,500–3,000"),("Camera module", "₹800–1,500"),("Fitness tracker / sensors", "₹1,000–2,000"),("Wires, power, storage", "₹500–1,000"),("Enclosure / mounting", "₹300–800"),("Other components", "₹500–1,000")], columns=["Optional item", "Estimated cost"])
    st.markdown("### Illustrative optional hardware budget")
    st.dataframe(budget, use_container_width=True, hide_index=True)
    st.caption("These are planning estimates, not verified live prices. A laptop-only prototype can be built without this hardware.")
    st.markdown("### Evaluation plan")
    st.write("Compare a baseline practice plan with a revised plan using consented pilot data. Track quiz performance over repeated attempts, completion rate, user feedback, and error patterns. Use a small sample only as exploratory evidence; do not claim causation without an appropriate study design.")

elif page == "Roadmap & Team":
    st.markdown('<div class="section-kicker">08 / Six-week execution</div><div class="section-title">Roadmap & four-person team</div>', unsafe_allow_html=True)
    roadmap = pd.DataFrame([( "Week 1", "Research question, problem statement, success metrics"),("Week 2", "UI polish, input checks, quiz content review"),("Week 3", "Practice-plan rules and data logging with consent"),("Week 4", "Dashboard, charts, and CSV export testing"),("Week 5", "Pilot tests, feedback, bug fixes, limitation review"),("Week 6", "Final demo, poster/PPT, rehearsal, Q&A")], columns=["Week", "Deliverables"])
    for _, row in roadmap.iterrows():
        with st.container(border=True):
            st.markdown(f"**{row['Week']}**  ·  {row['Deliverables']}")
    st.markdown("### Team roles")
    roles = [("Student 1", "Research & data analysis", "Research question, metrics, data quality, report."),("Student 2", "Hardware & IoT", "Optional sensors, setup, safety and privacy checks."),("Student 3", "Software & app", "Streamlit UI, testing, charts, deployment."),("Student 4", "Research & presentation", "Literature comparison, Gujarati PPT, demo and Q&A.")]
    cols = st.columns(2)
    for i,(person, role, desc) in enumerate(roles):
        with cols[i%2]:
            with st.container(border=True): st.markdown(f"### 👨‍🎓 {person}"); st.markdown(f"**{role}**"); st.write(desc)
    st.markdown("### Practical checklist")
    st.write("☐ Define one measurable research question · ☐ Review privacy and consent · ☐ Test with sample data first · ☐ Record bugs and results honestly · ☐ Prepare a backup offline demo")

elif page == "Judge Q&A":
    st.markdown('<div class="section-kicker">09 / Presentation preparation</div><div class="section-title">Judge questions & honest answers</div>', unsafe_allow_html=True)
    qa = [
        ("What problem does your project solve?", "It helps students turn quiz results into a clear next practice step while considering self-reported routine signals. It is a learning-support prototype, not a replacement for teachers."),
        ("Is this a real AI model?", "The current prototype is rule-based, not a trained ML model. Our next research step is to define a measurable question, collect consented data, compare baselines, and only then decide whether ML adds value."),
        ("How do you evaluate results?", "We plan to track repeated quiz scores, task completion, feedback, and error patterns. Any pilot result will be reported with sample size and limitations."),
        ("How do you protect student privacy?", "Use demo data during public presentations, minimise collected information, obtain appropriate permission for pilots, and avoid collecting sensitive health or personal details."),
        ("What is innovative about the approach?", "The project brings together a transparent practice recommendation loop and balanced-routine prompts in one student-facing demo. We will compare it with existing learning tools before making novelty claims."),
        ("What is the budget?", "The current laptop-only software demo does not require hardware. Optional sensor components are only planning estimates and would be purchased only if the research question needs them.")]
    for q,a in qa:
        with st.expander(q): st.write(a)

st.divider()
st.markdown('<div class="footer">AB SCHOOL LOOP AI · Student research prototype · Premium UI v1 · Learning support, not diagnosis · Transparent rule-based baseline</div>', unsafe_allow_html=True)
