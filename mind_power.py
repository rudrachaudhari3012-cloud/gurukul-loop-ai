# ============================================================
# AB SCHOOL LOOP AI - HEALTH POWER AI
# Advanced Sensor-Free Student Well-being Module
# Version: 1.0
#
# Integration:
#   from health_power import render_health_power
#   render_health_power(st, student_id=st.session_state.get("username", "demo"))
#
# Run independently:
#   streamlit run health_power.py
#
# Notes:
# - Uses student-entered information; no sensors or medical diagnosis.
# - Stores records in health_power_ai.db in the same folder.
# - Keep this file separate from your existing app.py.
# ============================================================

import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

import streamlit as st
import pandas as pd

DB_PATH = Path(__file__).with_name("health_power_ai.db")

# --------------------------- THEME ----------------------------

def _inject_health_css():
    st.markdown("""
    <style>
    .hp-hero {
        padding: 28px 26px; border-radius: 22px;
        background: linear-gradient(120deg,#0b1424 0%,#12304a 58%,#075b63 100%);
        border: 1px solid rgba(34,211,238,.28);
        box-shadow: 0 12px 35px rgba(0,0,0,.18);
        margin-bottom: 18px;
    }
    .hp-kicker { color:#5eead4; font-size:11px; font-weight:800; letter-spacing:2px; }
    .hp-hero h1 { color:#f4f8ff; font-size:34px; margin:8px 0 4px 0; }
    .hp-hero p { color:#c7d8e8; margin:0; font-size:14px; }
    .hp-note {
        background:rgba(34,211,238,.08); border:1px solid rgba(34,211,238,.22);
        border-radius:13px; padding:12px 14px; color:inherit; margin:10px 0;
    }
    .hp-small { color:#9fb3c8; font-size:12px; }
    div[data-testid="stMetric"] {
        background:rgba(34,211,238,.055); border:1px solid rgba(34,211,238,.14);
        padding:14px; border-radius:15px;
    }
    </style>
    """, unsafe_allow_html=True)


# --------------------------- DATABASE -------------------------

def _connect():
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con


def _init_db():
    with _connect() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                log_date TEXT NOT NULL,
                activity TEXT NOT NULL,
                minutes INTEGER NOT NULL,
                outdoor INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS sleep_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                log_date TEXT NOT NULL,
                sleep_time TEXT NOT NULL,
                wake_time TEXT NOT NULL,
                duration REAL NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS food_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                log_date TEXT NOT NULL,
                food_name TEXT NOT NULL,
                meal_type TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS habit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                log_date TEXT NOT NULL,
                mission TEXT NOT NULL,
                xp INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                UNIQUE(student_id, log_date, mission)
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS quiz_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                log_date TEXT NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS bmi_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                log_date TEXT NOT NULL,
                age INTEGER NOT NULL,
                height_cm REAL NOT NULL,
                weight_kg REAL NOT NULL,
                bmi REAL NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS music_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                log_date TEXT NOT NULL,
                sound_type TEXT NOT NULL,
                duration_minutes INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS mind_test_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                log_date TEXT NOT NULL,
                logic_score INTEGER NOT NULL,
                pattern_score INTEGER NOT NULL,
                memory_score INTEGER NOT NULL,
                reasoning_score INTEGER NOT NULL,
                total_score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        con.commit()


def _query_df(sql, params):
    with _connect() as con:
        return pd.read_sql_query(sql, con, params=params)


# ---------------------- DATA / KNOWLEDGE ----------------------

FOOD_LIBRARY = {
    "દાળ / કઠોળ": {
        "group": "Protein and fibre",
        "detail": "Lentils and legumes are good sources of protein and fiber.",
        "tip": "Various lentils and legumes can be included in meals."
    },
    "દૂધ / દહીં": {
        "group": "Calcium and protein",
        "detail": "દૂધ અને દહીં કેલ્શિયમ તથા પ્રોટીન આપે છે.",
        "tip": "દૂધજન્ય ખોરાક દરેકને અનુકૂળ હોય એવું જરૂરી નથી; વિકલ્પો પણ ઉપલબ્ધ છે."
    },
    "ફળો": {
        "group": "Vitamins and fibre",
        "detail": "ફળોમાં વિટામિન, ખનિજ અને ફાઇબર હોય છે.",
        "tip": "મોસમી અને વિવિધ રંગનાં ફળો વિશે શીખો."
    },
    "શાકભાજી": {
        "group": "Vitamins, minerals and fibre",
        "detail": "શાકભાજી વિવિધ વિટામિન, ખનિજ અને ફાઇબર આપે છે.",
        "tip": "થાળીમાં વિવિધ રંગનાં શાકભાજી ઉમેરવાનો પ્રયત્ન કરો."
    },
    "અનાજ / રોટલી": {
        "group": "Energy-giving carbohydrates",
        "detail": "અનાજ શરીરને ઊર્જા આપતા કાર્બોહાઇડ્રેટ્સનો સ્ત્રોત છે.",
        "tip": "શક્ય હોય ત્યારે વિવિધ અનાજ વિશે જાણો."
    },
    "સૂકા મેવા / બીજ": {
        "group": "Healthy fats and nutrients",
        "detail": "સૂકા મેવા અને બીજમાં વિવિધ પોષક તત્ત્વો હોય છે.",
        "tip": "એલર્જી હોય તો તે ખોરાક ટાળો અને વડીલની સલાહ લો."
    },
    "પાણી": {
        "group": "Hydration",
        "detail": "પાણી શરીરના સામાન્ય કાર્યો માટે જરૂરી છે.",
        "tip": "તરસ લાગે ત્યારે પાણી પીવો અને દિવસભર પાણી ઉપલબ્ધ રાખો."
    },
}

FOOD_QUESTIONS = [
    ("દાળ અને કઠોળ કયા પોષક તત્ત્વના સારા સ્ત્રોત છે?", ["પ્રોટીન", "પ્લાસ્ટિક", "ધુમાડો"], 0,
     "દાળ અને કઠોળ પ્રોટીન તથા ફાઇબરના સારા સ્ત્રોત છે."),
    ("ફળોમાં સામાન્ય રીતે શું મળે છે?", ["વિટામિન અને ફાઇબર", "માત્ર મીઠું", "પ્લાસ્ટિક"], 0,
     "ફળોમાં વિવિધ વિટામિન, ખનિજ અને ફાઇબર હોય છે."),
    ("પાણી શા માટે જરૂરી છે?", ["શરીરના સામાન્ય કાર્યો માટે", "ઊંઘ દૂર કરવા જ", "હાડકાં રંગવા"], 0,
     "પાણી શરીરના અનેક સામાન્ય કાર્યોમાં મદદ કરે છે."),
    ("શાકભાજી કયા પોષક તત્ત્વો આપી શકે છે?", ["વિટામિન અને ખનિજ", "માત્ર ધુમાડો", "કોઈ નહીં"], 0,
     "શાકભાજી વિવિધ વિટામિન, ખનિજ અને ફાઇબર આપે છે."),
    ("દૂધ અને દહીંમાં કયું ખનિજ મળે છે?", ["કેલ્શિયમ", "પેટ્રોલ", "પ્લાસ્ટિક"], 0,
     "દૂધ અને દહીં કેલ્શિયમના જાણીતા સ્ત્રોત છે.")
]



# ---------------------- INTELLIGENCE ENGINE -------------------

def _build_recommendations(activity_df, sleep_df, food_df):
    recs = []
    recs.append(("🏃 Active Body", "Keep a comfortable balance of movement, study and rest." if not activity_df.empty else "Record an activity you enjoy."))
    recs.append(("🌙 Sleep", "Review your sleep pattern and aim for a regular routine." if not sleep_df.empty else "Record your sleep and wake-up times."))
    recs.append(("🥗 Smart Food", "Continue learning about a variety of foods and nutrients." if not food_df.empty else "Explore the Food Library and learn one nutrition fact."))
    return recs


MIND_QUESTIONS = [
    ("Logic", "All roses are flowers. Which statement must be true?", ["All roses fade", "All roses are flowers", "All flowers are roses", "No roses are flowers"], 1),
    ("Pattern", "What comes next: 2, 4, 8, 16, ...?", ["18", "24", "32", "30"], 2),
    ("Memory", "Remember: 7 - 2 - 9. What was the middle number?", ["7", "2", "9", "5"], 1),
    ("Reasoning", "Mina is taller than Ravi. Ravi is taller than Dev. Who is shortest?", ["Mina", "Ravi", "Dev", "Cannot tell"], 2),
    ("Logic", "Every book on a shelf is blue. This is a book on that shelf. What colour is it?", ["Red", "Blue", "Green", "Cannot tell"], 1),
    ("Pattern", "Which shape has the most sides?", ["Triangle", "Square", "Pentagon", "Hexagon"], 3),
    ("Memory", "Remember: river, candle, mango. Which word was second?", ["River", "Candle", "Mango", "Mountain"], 1),
    ("Reasoning", "A journey starts at 10:00 and takes one hour. When does it end?", ["10:30", "11:00", "11:30", "12:00"], 1),
]


def _mind_guidance(scores):
    tips = {
        "Logic": "Practice short logic puzzles and explain your reasoning step by step.",
        "Pattern": "Try number sequences, shape patterns and visual matching puzzles.",
        "Memory": "Try short recall activities: read a few items, hide them, then recall them.",
        "Reasoning": "Practice everyday word problems and break them into smaller steps."
    }
    if not scores:
        return "Complete the Mind Skills Check to receive practice suggestions."
    focus = min(scores, key=scores.get)
    return f"Suggested practice: {tips[focus]} This is a practice snapshot, not an IQ score or a measure of overall intelligence."


# --------------------------- MAIN UI --------------------------

def render_health_power(st, student_id="demo_student"):
    """Render Health Power AI inside an existing Streamlit app."""
    _init_db()
    _inject_health_css()

    sid = str(student_id or "demo_student").strip()[:100]
    today = date.today().isoformat()

    st.markdown("""
    <div class="hp-hero">
      <div class="hp-kicker">AB SCHOOL LOOP AI · STUDENT WELL-BEING</div>
      <h1>🧬 HEALTH POWER AI</h1>
      <p>Active Body · Sleep · Smart Food · BMI · Memory Music · Mind Skills</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="hp-note"><b>Sensor-free system:</b> This module works based on the information entered by the student. '
        'This is not a medical device and does not diagnose any disease.</div>',
        unsafe_allow_html=True
    )

    # Fetch recent data for this student
    week_start = (date.today() - timedelta(days=6)).isoformat()
    activity = _query_df("SELECT log_date, activity, minutes, outdoor FROM activity_logs WHERE student_id=? AND log_date>=? ORDER BY log_date", (sid, week_start))
    sleep = _query_df("SELECT log_date, sleep_time, wake_time, duration FROM sleep_logs WHERE student_id=? AND log_date>=? ORDER BY log_date", (sid, week_start))
    food = _query_df("SELECT log_date, food_name, meal_type FROM food_logs WHERE student_id=? AND log_date>=? ORDER BY log_date DESC", (sid, week_start))
    bmi_history = _query_df("SELECT log_date, age, height_cm, weight_kg, bmi FROM bmi_logs WHERE student_id=? ORDER BY log_date DESC LIMIT 30", (sid,))
    music_history = _query_df("SELECT log_date, sound_type, duration_minutes FROM music_logs WHERE student_id=? ORDER BY log_date DESC LIMIT 30", (sid,))
    mind_history = _query_df("SELECT log_date, logic_score, pattern_score, memory_score, reasoning_score, total_score, total_questions FROM mind_test_logs WHERE student_id=? ORDER BY log_date DESC LIMIT 20", (sid,))

    activity_total = int(activity["minutes"].sum()) if not activity.empty else 0
    sleep_avg = float(sleep["duration"].mean()) if not sleep.empty else 0
    latest_bmi = float(bmi_history.iloc[0]["bmi"]) if not bmi_history.empty else None
    latest_mind = int(mind_history.iloc[0]["total_score"]) if not mind_history.empty else None

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🏃 Activity", f"{activity_total} min", "Last 7 days")
    m2.metric("🌙 Avg. Sleep", f"{sleep_avg:.1f} hrs" if not sleep.empty else "—", "Last 7 days")
    m3.metric("⚖️ Latest BMI", f"{latest_bmi:.1f}" if latest_bmi is not None else "—", "Informational only")
    m4.metric("🧠 Mind Skills", f"{latest_mind}/8" if latest_mind is not None else "—", "Latest practice test")

    tabs = st.tabs(["🏃 Active Body", "🌙 Sleep", "🥗 Smart Food", "⚖️ BMI", "🎧 Memory Music", "🧠 IQ & Mind Skills", "✨ AI Insights", "📊 Growth Report"])

    # ---------------- ACTIVE BODY ----------------
    with tabs[0]:
        st.subheader("🏃 Active Body AI")
        st.write("Track your movement and activity. No wearable or step sensor required.")
        with st.form("hp_activity_form", clear_on_submit=True):
            a_date = st.date_input("Activity date", value=date.today(), key="hp_a_date")
            a_type = st.selectbox("Activity", [
                "Walking", "Cycling", "Outdoor play", "Stretching",
                "Dance", "Yoga", "Sports", "Other"
            ])
            a_minutes = st.number_input("Duration (minutes)", min_value=1, max_value=300, value=15, step=5)
            a_outdoor = st.checkbox("Did you do this activity outdoors?")
            a_submit = st.form_submit_button("Save Activity", use_container_width=True)
            if a_submit:
                with _connect() as con:
                    con.execute(
                        "INSERT INTO activity_logs(student_id,log_date,activity,minutes,outdoor,created_at) VALUES(?,?,?,?,?,?)",
                        (sid, a_date.isoformat(), a_type, int(a_minutes), int(a_outdoor), datetime.now().isoformat(timespec="seconds"))
                    )
                    con.commit()
                st.success("Activity record સાચવાઈ ગયો!")
                st.rerun()

        if not activity.empty:
            st.markdown("#### Recent activity records")
            st.dataframe(activity.rename(columns={
                "log_date": "Date", "activity": "Activity",
                "minutes": "Minutes", "outdoor": "Outdoor"
            }), use_container_width=True, hide_index=True)
            daily = activity.groupby("log_date", as_index=False)["minutes"].sum()
            st.bar_chart(daily.set_index("log_date"))
        else:
            st.info("No activity recorded yet. Add the first entry from above.")

    # ---------------- SLEEP ----------------
    with tabs[1]:
        st.subheader("🌙 Sleep Routine")
        st.write("Enter your bedtime and wake-up time.")
        with st.form("hp_sleep_form", clear_on_submit=True):
            s_date = st.date_input("Sleep record date", value=date.today(), key="hp_s_date")
            c1, c2 = st.columns(2)
            with c1:
                s_bed = st.time_input("Sleep Time", value=datetime.strptime("22:00", "%H:%M").time())
            with c2:
                s_wake = st.time_input("Wake Up Time", value=datetime.strptime("06:00", "%H:%M").time())
            s_submit = st.form_submit_button("Save Sleep Record", use_container_width=True)
            if s_submit:
                bed_mins = s_bed.hour * 60 + s_bed.minute
                wake_mins = s_wake.hour * 60 + s_wake.minute
                duration = (wake_mins - bed_mins) % (24 * 60) / 60
                if duration <= 0 or duration > 18:
                    st.error("સમય ફરી તપાસો. દાખલ કરેલો sleep duration માન્ય નથી.")
                else:
                    with _connect() as con:
                        con.execute(
                            "INSERT INTO sleep_logs(student_id,log_date,sleep_time,wake_time,duration,created_at) VALUES(?,?,?,?,?,?)",
                            (sid, s_date.isoformat(), s_bed.strftime("%H:%M"), s_wake.strftime("%H:%M"),
                             round(duration, 2), datetime.now().isoformat(timespec="seconds"))
                        )
                        con.commit()
                    st.success(f"Sleep record સાચવાયો: {duration:.1f} કલાક.")
                    st.rerun()

        if not sleep.empty:
            st.markdown("#### Recent sleep records")
            st.dataframe(sleep.rename(columns={
                "log_date": "Date", "sleep_time": "Bedtime",
                "wake_time": "Wake time", "duration": "Hours"
            }), use_container_width=True, hide_index=True)
            st.line_chart(sleep.set_index("log_date")[["duration"]])
        else:
            st.info("Add your first entry to understand your sleep routine.")
        st.caption(" General Guidance: Teenagers aged 13–18 are generally recommended to get 8–10 hours of sleep. Individual needs may vary.")
    # ---------------- SMART FOOD ----------------
    with tabs[2]:
        st.subheader("🥗 Smart Food Guide")
        st.write("Gain nutritional insights about food.")
        selected_food = st.selectbox("Choose the Food", list(FOOD_LIBRARY.keys()), key="hp_food_select")
        item = FOOD_LIBRARY[selected_food]
        st.markdown(f"### {selected_food}")
        st.info(f"**Nutrient group:** {item['group']}\n\n{item['detail']}\n\n**Learning tip:** {item['tip']}")

        with st.form("hp_food_form", clear_on_submit=True):
            f_date = st.date_input("Date", value=date.today(), key="hp_f_date")
            f_meal = st.selectbox("Meal", ["Breakfast", "Lunch", "Snack", "Dinner"])
            f_submit = st.form_submit_button("Save Food Learning / Entry", use_container_width=True)
            if f_submit:
                with _connect() as con:
                    con.execute(
                        "INSERT INTO food_logs(student_id,log_date,food_name,meal_type,created_at) VALUES(?,?,?,?,?)",
                        (sid, f_date.isoformat(), selected_food, f_meal, datetime.now().isoformat(timespec="seconds"))
                    )
                    con.commit()
                st.success("Food entry સાચવાઈ ગઈ!")
                st.rerun()

        st.markdown("#### 🧠 Nutrition Knowledge Quiz")
        q_index = st.selectbox("Question પસંદ કરો", list(range(len(FOOD_QUESTIONS))),
                               format_func=lambda x: f"Question {x + 1}", key="hp_quiz_q")
        question, options, correct, explanation = FOOD_QUESTIONS[q_index]
        answer = st.radio(question, options, key=f"hp_quiz_answer_{q_index}")
        if st.button("Check Answer", key="hp_check_quiz", use_container_width=True):
            is_correct = options.index(answer) == correct
            if is_correct:
                st.success("સાચો જવાબ! " + explanation)
            else:
                st.warning("ફરી પ્રયત્ન કરો. " + explanation)
            st.session_state["hp_last_quiz_result"] = int(is_correct)

        if not food.empty:
            st.markdown("#### Recent food learning entries")
            st.dataframe(food.rename(columns={
                "log_date": "Date", "food_name": "Food", "meal_type": "Meal"
            }), use_container_width=True, hide_index=True)

    # ---------------- AI INSIGHTS ----------------
    with tabs[4]:
        st.subheader("🧠 Health Intelligence Engine")
        st.write("This prototype provides suggestions based on the entered records using rule-based analysis.")
        recs = _build_recommendations(activity, sleep, food)
        for heading, message in recs:
            st.markdown(f"**{heading}**")
            st.info(message)
        st.markdown("""
        **Logic of this system:" or "This system's logic:**
        1. Reads student-entered records.
        2. Checks recent history and simple patterns.
        3. Selects rule-based personalized suggestions.
        4. Regenerates insights when new entries are added.
        """)
        st.caption("This is a Rule-Based AI prototype; it does not claim to be a trained machine-learning model.")

    # ---------------- GROWTH REPORT (ALWAYS LAST) ----------------
    with tabs[7]:
        st.subheader("📊 Student Growth Report")
        st.write("Personal summary of activity, sleep, food learning, BMI, music preferences and mind-skills practice.")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Activity records", len(activity))
        c2.metric("Sleep records", len(sleep))
        c3.metric("Food entries", len(food))
        c4.metric("Mind tests", len(mind_history))

        st.markdown("#### 🏃 Active Body")
        st.write(f"Recorded activity in the last 7 days: **{activity_total} minutes**.")
        if not activity.empty:
            st.bar_chart(activity.groupby("log_date")["minutes"].sum())

        st.markdown("#### 🌙 Sleep")
        st.write(f"Average recorded sleep: **{sleep_avg:.1f} hours**." if not sleep.empty else "No sleep records yet.")
        if not sleep.empty:
            st.line_chart(sleep.set_index("log_date")[["duration"]])

        st.markdown("#### 🥗 Smart Food")
        st.write(f"Food learning entries in the last 7 days: **{len(food)}**.")
        if not food.empty:
            st.dataframe(food.rename(columns={"log_date":"Date","food_name":"Food","meal_type":"Meal"}), use_container_width=True, hide_index=True)

        st.markdown("#### ⚖️ BMI")
        st.write(f"Latest BMI number: **{float(bmi_history.iloc[0]['bmi']):.1f}** (informational only; teen interpretation needs age- and sex-specific growth charts)." if not bmi_history.empty else "No BMI records yet.")
        if not bmi_history.empty:
            st.dataframe(bmi_history.rename(columns={"log_date":"Date","age":"Age","height_cm":"Height (cm)","weight_kg":"Weight (kg)","bmi":"BMI number"}), use_container_width=True, hide_index=True)

        st.markdown("#### 🎧 Memory Booster Music")
        st.write(f"Saved music sessions: **{len(music_history)}**.")
        if not music_history.empty:
            st.dataframe(music_history.rename(columns={"log_date":"Date","sound_type":"Sound","duration_minutes":"Minutes"}), use_container_width=True, hide_index=True)

        st.markdown("#### 🧠 Mind Skills Practice")
        st.write(f"Completed practice tests: **{len(mind_history)}**.")
        if not mind_history.empty:
            latest = mind_history.iloc[0]
            st.write(f"Latest practice result: **{int(latest['total_score'])}/{int(latest['total_questions'])}**. This is not an IQ score.")
            st.dataframe(mind_history.rename(columns={"log_date":"Date","logic_score":"Logic","pattern_score":"Patterns","memory_score":"Memory","reasoning_score":"Reasoning","total_score":"Correct","total_questions":"Questions"}), use_container_width=True, hide_index=True)

        report_parts = [
            f"HEALTH POWER AI - STUDENT GROWTH REPORT\nStudent ID: {sid}\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
            f"Activity minutes (last 7 days): {activity_total}",
            f"Average sleep hours (last 7 days): {sleep_avg:.2f}" if not sleep.empty else "Average sleep hours: No records",
            f"Food learning entries (last 7 days): {len(food)}",
            f"BMI records: {len(bmi_history)}",
            f"Music sessions: {len(music_history)}",
            f"Mind-skills practice tests: {len(mind_history)}",
            f"Latest mind-skills result: {int(mind_history.iloc[0]['total_score'])}/{int(mind_history.iloc[0]['total_questions'])} (not an IQ score)" if not mind_history.empty else "Latest mind-skills result: No records"
        ]
        st.download_button("⬇️ Download Student Growth Report (TXT)", data="\n".join(report_parts),
                           file_name="health_power_student_growth_report.txt", mime="text/plain", use_container_width=True)
        st.markdown("---")
        st.caption("Privacy: records are stored in health_power_ai.db and separated by student_id. This is an educational dashboard, not a medical diagnosis or standardized IQ assessment.")



# ---------------------- STANDALONE RUN ------------------------

if __name__ == "__main__":
    render_health_power(st, student_id="demo_student")
