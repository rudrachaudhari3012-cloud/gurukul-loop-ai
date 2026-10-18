import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="AB SCHOOL LOOP AI | Student Growth Studio",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------
# Theme CSS
# ---------------------------
CSS = r"""
<style>
:root {
    color-scheme: dark;
    --bg: #050816;
    --bg-secondary: #09132B;
    --panel: #0D1933;
    --cyan: #00D6FF;
    --mint: #00F5B8;
    --text: #F2FAFF;
    --muted: #A8BED8;
}
.stApp {
    background:
        radial-gradient(ellipse at 8% 4%, rgba(0,214,255,.18), transparent 30%),
        radial-gradient(ellipse at 92% 20%, rgba(0,245,184,.13), transparent 30%),
        radial-gradient(ellipse at 50% 100%, rgba(55,78,255,.13), transparent 40%),
        linear-gradient(135deg, #050816 0%, #09132B 48%, #061A25 100%);
    color: var(--text);
}
.block-container { max-width: 1440px; padding-top: 1.5rem; padding-bottom: 3rem; }
.stApp, .stApp p, .stApp label, .stApp li { color: var(--text); }
h1, h2, h3, h4 { color: var(--text); }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080F24 0%, #071D25 100%);
    border-right: 1px solid rgba(0,245,184,.28);
}
[data-testid="stSidebar"] * { color: #F2FAFF; }
[data-testid="stSidebar"] input,
.stTextInput input, .stNumberInput input, .stDateInput input, .stTextArea textarea {
    background: #080F24 !important;
    color: #F2FAFF !important;
    border: 1px solid rgba(0,214,255,.34) !important;
    border-radius: 10px !important;
}
[data-baseweb="select"] > div {
    background-color: #0D1933;
    border-color: rgba(0,214,255,.38);
    border-radius: 10px;
    color: #F2FAFF;
}
[data-baseweb="popover"], [data-baseweb="menu"] { background: #0D1933; }
[data-baseweb="menu"] * { color: #F2FAFF; }
.hero {
    position: relative;
    overflow: hidden;
    padding: 2.2rem;
    border-radius: 24px;
    background:
        radial-gradient(circle at 90% 10%, rgba(0,214,255,.24), transparent 34%),
        radial-gradient(circle at 8% 100%, rgba(0,245,184,.15), transparent 40%),
        linear-gradient(120deg, #080F24 0%, #0A3040 52%, #073D38 100%);
    border: 1px solid rgba(0,214,255,.55);
    box-shadow: 0 0 20px rgba(0,214,255,.15), 0 18px 48px rgba(0,0,0,.30);
}
.eyebrow {
    color: var(--mint);
    letter-spacing: .16em;
    text-transform: uppercase;
    font-size: .75rem;
    font-weight: 800;
}
.hero h1 {
    color: #fff !important;
    font-size: clamp(2rem, 4vw, 3.2rem);
    line-height: 1.1;
    margin: .55rem 0 .75rem;
    text-shadow: 0 0 14px rgba(0,214,255,.28);
}
.hero p { color: #D9F7FF; font-size: 1.02rem; line-height: 1.65; max-width: 800px; }
.pill-row { display: flex; flex-wrap: wrap; gap: .55rem; margin-top: 1rem; }
.pill {
    border: 1px solid rgba(0,214,255,.42);
    background: rgba(5,8,22,.60);
    border-radius: 999px;
    padding: .42rem .75rem;
    font-size: .8rem;
}
.section-kicker { color: var(--mint); font-size: .76rem; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; }
.section-title { color: #F2FAFF; font-size: 1.45rem; font-weight: 800; margin: .1rem 0 .35rem; }
.subtle { color: #A8BED8; }
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(0,214,255,.12), rgba(9,19,43,.97) 60%, rgba(0,245,184,.06));
    border: 1px solid rgba(0,214,255,.35);
    padding: 1rem 1.1rem;
    border-radius: 16px;
    box-shadow: 0 0 17px rgba(0,214,255,.07);
}
div[data-testid="stMetricLabel"] { color: #A8BED8; }
div[data-testid="stMetricValue"] { color: var(--mint); }
div.stButton > button {
    border: 1px solid rgba(0,214,255,.38);
    border-radius: 12px;
    background: linear-gradient(110deg, #0D1933, #10283B);
    color: #F2FAFF;
    font-weight: 700;
    transition: all .2s ease;
}
div.stButton > button[kind="primary"] {
    border: 1px solid rgba(0,214,255,.85);
    background: linear-gradient(100deg, #00D6FF 0%, #00F5B8 100%);
    color: #04101D;
    font-weight: 800;
    min-height: 2.8rem;
}
div.stButton > button:hover { border-color: var(--mint); }
[data-testid="stDownloadButton"] button {
    background: linear-gradient(100deg, #073D38, #0A3040);
    border: 1px solid rgba(0,245,184,.60);
    color: #EFFFF8;
    border-radius: 12px;
    font-weight: 750;
}
[data-testid="stExpander"] {
    background: rgba(9,19,43,.90);
    border: 1px solid rgba(0,214,255,.30);
    border-radius: 14px;
}
div[data-testid="stAlert"] {
    border-radius: 14px;
    border: 1px solid rgba(0,214,255,.30);
}
hr { border-color: rgba(0,214,255,.23); }
.footer {
    color: #8EAAC5;
    font-size: .82rem;
    text-align: center;
    padding: 1.4rem 0 .5rem;
    border-top: 1px solid rgba(0,214,255,.22);
    margin-top: 1.8rem;
}
@media (max-width: 700px) {
    .hero { padding: 1.25rem; border-radius: 18px; }
    .block-container { padding-top: 1rem; }
}
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { transition: none !important; animation: none !important; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ---------------------------
# Prototype logic (transparent rules, not a trained ML model)
# ---------------------------
def classify_topic(score: float):
    if score < 50:
        return "Needs support", "High", "Start with a short recap, then practise 3 easy questions."
    if score < 75:
        return "Growing", "Medium", "Review mistakes and practise 5 mixed questions."
    return "Strong", "Low", "Try an advanced question and explain the concept to someone else."

def safe_score(value):
    return max(0, min(100, int(value)))

# ---------------------------
# Sidebar
# ---------------------------
with st.sidebar:
    st.markdown("## 🎓 SCHOOL LOOP AI")
    st.caption("Student Growth Studio · Prototype")
    page = st.radio(
        "Navigation",
        ["Dashboard", "Add Student Record", "Learning Insights", "About & Limitations"],
        index=0,
    )
    st.divider()
    st.markdown("### ⚙️ Demo settings")
    show_demo = st.checkbox("Load sample data", value=True)
    st.caption("Demo records are fictional. Do not enter sensitive personal information.")

# ---------------------------
# Session state and sample data
# ---------------------------
if "records" not in st.session_state:
    st.session_state.records = []

if show_demo and not st.session_state.records:
    st.session_state.records = [
        {"student": "Student A", "topic": "Algebra", "score": 42, "study_minutes": 25, "activity_date": str(date.today())},
        {"student": "Student B", "topic": "Physics", "score": 68, "study_minutes": 35, "activity_date": str(date.today())},
        {"student": "Student C", "topic": "Chemistry", "score": 86, "study_minutes": 40, "activity_date": str(date.today())},
    ]

records = st.session_state.records
df = pd.DataFrame(records)

# ---------------------------
# Header
# ---------------------------
st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">AI-assisted learning · transparent prototype</div>
      <h1>AB SCHOOL LOOP AI</h1>
      <p>A student-growth dashboard that turns practice scores into clear next steps.
      It supports reflection and planning; it does not diagnose students or replace teachers.</p>
      <div class="pill-row">
        <span class="pill">⚡ Learning insights</span>
        <span class="pill">📈 Progress tracking</span>
        <span class="pill">🧠 Practice recommendations</span>
        <span class="pill">🔒 Demo-first privacy</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

if page == "Dashboard":
    st.markdown('<div class="section-kicker">Overview</div><div class="section-title">Learning at a glance</div>', unsafe_allow_html=True)
    if df.empty:
        st.info("No records yet. Open **Add Student Record** to enter a practice result.")
        total_students, avg_score, total_sessions = 0, 0, 0
    else:
        total_students = df["student"].nunique()
        avg_score = round(df["score"].mean(), 1)
        total_sessions = len(df)

    c1, c2, c3 = st.columns(3)
    c1.metric("Students in records", total_students)
    c2.metric("Average practice score", f"{avg_score}/100")
    c3.metric("Practice records", total_sessions)

    st.write("")
    left, right = st.columns([1.35, 1])
    with left:
        st.subheader("📊 Score by topic")
        if not df.empty:
            topic_df = df.groupby("topic", as_index=False)["score"].mean().sort_values("score")
            st.bar_chart(topic_df.set_index("topic"), y="score")
        else:
            st.caption("Topic chart will appear after you add records.")
    with right:
        st.subheader("🧭 Suggested next steps")
        if not df.empty:
            for row in df.sort_values("score").head(4).itertuples():
                status, priority, suggestion = classify_topic(row.score)
                st.markdown(f"**{row.student} · {row.topic}**")
                st.caption(f"Score: {row.score}/100 · {status} · Priority: {priority}")
                st.write(suggestion)
                st.divider()
        else:
            st.write("Add a practice record to receive a rule-based suggestion.")

    if not df.empty:
        st.subheader("Recent records")
        st.dataframe(df.sort_values("activity_date", ascending=False), use_container_width=True, hide_index=True)

elif page == "Add Student Record":
    st.markdown('<div class="section-kicker">Input</div><div class="section-title">Add a practice record</div>', unsafe_allow_html=True)
    st.caption("Use a nickname or anonymous ID. This demo stores records only in the current app session.")
    with st.form("student_record_form", clear_on_submit=True):
        student = st.text_input("Student nickname / ID", placeholder="e.g. Student D")
        topic = st.selectbox("Topic", ["Mathematics", "Physics", "Chemistry", "Biology", "English", "Other"])
        score = st.slider("Practice score (%)", min_value=0, max_value=100, value=60)
        study_minutes = st.number_input("Practice time (minutes)", min_value=0, max_value=600, value=30, step=5)
        activity_date = st.date_input("Practice date", value=date.today())
        submitted = st.form_submit_button("Save record", type="primary", use_container_width=True)

    if submitted:
        if not student.strip():
            st.error("Please enter a nickname or anonymous ID.")
        else:
            new_record = {
                "student": student.strip()[:60],
                "topic": topic,
                "score": safe_score(score),
                "study_minutes": int(study_minutes),
                "activity_date": str(activity_date),
            }
            st.session_state.records.append(new_record)
            status, priority, suggestion = classify_topic(new_record["score"])
            st.success("Record added to this session.")
            st.markdown(f"**Status:** {status}  ·  **Priority:** {priority}")
            st.write(suggestion)
            st.rerun()

elif page == "Learning Insights":
    st.markdown('<div class="section-kicker">Analysis</div><div class="section-title">Learning insights</div>', unsafe_allow_html=True)
    if df.empty:
        st.info("There are no records to analyse yet. Add a practice record first.")
    else:
        topic_summary = df.groupby("topic", as_index=False).agg(
            Average_score=("score", "mean"),
            Records=("score", "count"),
            Average_practice_minutes=("study_minutes", "mean"),
        )
        topic_summary["Average_score"] = topic_summary["Average_score"].round(1)
        topic_summary["Average_practice_minutes"] = topic_summary["Average_practice_minutes"].round(1)
        st.subheader("Topic summary")
        st.dataframe(topic_summary, use_container_width=True, hide_index=True)
        st.subheader("Score distribution")
        st.bar_chart(df["score"].value_counts().sort_index())
        st.subheader("Records needing review")
        needs_review = df[df["score"] < 75].copy()
        if needs_review.empty:
            st.success("No records below 75% in this dataset. Consider offering optional challenge questions.")
        else:
            needs_review["Recommendation"] = needs_review["score"].apply(lambda x: classify_topic(x)[2])
            st.dataframe(needs_review, use_container_width=True, hide_index=True)

    if not df.empty:
        csv_data = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "⬇️ Download records as CSV",
            data=csv_data,
            file_name="school_loop_ai_records.csv",
            mime="text/csv",
            use_container_width=True,
        )

elif page == "About & Limitations":
    st.markdown('<div class="section-kicker">Transparency</div><div class="section-title">What this prototype does — and does not do</div>', unsafe_allow_html=True)
    st.markdown("""
    **What it does**
    - Stores practice records in the current Streamlit session.
    - Summarises scores by topic and displays charts.
    - Gives simple recommendations using explicit score thresholds.
    - Allows CSV export of the current records.

    **Important limitations**
    - This is a **rule-based prototype**, not a trained machine-learning model.
    - Score thresholds are demonstration choices, not validated educational standards.
    - Session data may be lost when the app session restarts; there is no database.
    - It does not infer attention, intelligence, mental health, or a student's ability from limited scores.
    - Use anonymised demo data for presentations and obtain appropriate consent before using real student data.
    """)
    st.info("For a research project, evaluate recommendations against teacher judgement and compare outcomes on a consented, appropriately anonymised dataset before making claims.")

st.markdown(
    '<div class="footer">AB SCHOOL LOOP AI · Student Growth Studio · Prototype for learning and research</div>',
    unsafe_allow_html=True,
)
