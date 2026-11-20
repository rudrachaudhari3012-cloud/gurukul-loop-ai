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
        con.commit()


def _query_df(sql, params):
    with _connect() as con:
        return pd.read_sql_query(sql, con, params=params)


# ---------------------- DATA / KNOWLEDGE ----------------------

FOOD_LIBRARY = {
    "દાળ / કઠોળ": {
        "group": "Protein and fibre",
        "detail": "દાળ અને કઠોળ પ્રોટીન તથા ફાઇબરના સારા સ્ત્રોત છે.",
        "tip": "ભોજનમાં વિવિધ દાળ અને કઠોળનો સમાવેશ કરી શકાય."
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

MISSIONS = [
    ("Take a gentle movement break", 20, "થોડું ઊભા થાઓ, હળવું સ્ટ્રેચિંગ કરો અથવા ચાલો."),
    ("Explore one healthy food fact", 20, "આજે એક ખોરાક અને તેના પોષક તત્ત્વ વિશે વાંચો."),
    ("Record your sleep routine", 20, "ગઈ રાતનો સૂવાનો અને જાગવાનો સમય નોંધો."),
    ("Play or spend time outdoors", 20, "તમારી અનુકૂળતા મુજબ બહાર રમો અથવા ચાલો."),
    ("Complete a food knowledge quiz", 20, "Smart Food Guide માં નાનો ક્વિઝ પૂર્ણ કરો."),
    ("Take a screen break", 20, "સ્ક્રીનથી થોડો વિરામ લો અને આંખોને આરામ આપો.")
]


# ---------------------- INTELLIGENCE ENGINE -------------------

def _build_recommendations(activity_df, sleep_df, food_df, habit_df):
    recs = []

    if activity_df.empty:
        recs.append(("🏃 Active Body", "તમારી દૈનિક activity નોંધવાનું શરૂ કરો. નાની અને અનુકૂળ movement થી શરૂઆત કરો."))
    else:
        week_activity = int(activity_df["minutes"].sum())
        days = activity_df["log_date"].nunique()
        if week_activity == 0:
            recs.append(("🏃 Active Body", "આ અઠવાડિયે activity નોંધાઈ નથી. તમારી અનુકૂળતા મુજબ હળવી ચાલ અથવા સ્ટ્રેચિંગનો વિચાર કરો."))
        elif days < 3:
            recs.append(("🏃 Active Body", "આ અઠવાડિયે થોડા દિવસોની activity નોંધાઈ છે. શક્ય હોય તો અલગ-અલગ દિવસોમાં નાની movement breaks ઉમેરો."))
        else:
            recs.append(("🏃 Active Body", "સારી શરૂઆત! તમારી activity નોંધવાનું ચાલુ રાખો અને આરામ તથા અભ્યાસ વચ્ચે સંતુલન રાખો."))

    if sleep_df.empty:
        recs.append(("🌙 Sleep", "સૂવાનો અને જાગવાનો સમય નોંધો જેથી તમારી sleep routine સમજી શકાય."))
    else:
        avg_sleep = float(sleep_df["duration"].mean())
        if avg_sleep < 7:
            recs.append(("🌙 Sleep", "તમારી નોંધેલી ઊંઘનો સમય ઓછો દેખાય છે. નિયમિત bedtime માટે સમય ગોઠવો અને જરૂર પડે તો વાલી સાથે વાત કરો."))
        elif avg_sleep <= 10:
            recs.append(("🌙 Sleep", "તમારી નોંધેલી ઊંઘનો સમય સામાન્ય ભલામણની આસપાસ છે. નિયમિત sleep schedule જાળવવાનો પ્રયત્ન કરો."))
        else:
            recs.append(("🌙 Sleep", "નોંધેલા sleep/wake સમય ફરી તપાસો. સમય દાખલ કરવામાં ભૂલ તો નથી ને?"))

    if food_df.empty:
        recs.append(("🥗 Smart Food", "Food Library માંથી ખોરાક વિશે જાણો અને આજે શીખેલી એક વાત નોંધો."))
    else:
        recs.append(("🥗 Smart Food", "વિવિધ ખોરાક અને પોષક તત્ત્વો વિશે શીખતા રહો. કોઈ એક ખોરાકને સંપૂર્ણ સારો કે ખરાબ ગણશો નહીં."))

    if habit_df.empty:
        recs.append(("🎮 Habit Games", "આજનું એક સરળ mission પસંદ કરો. નાની આદતો સતત વિકસાવવી મહત્વપૂર્ણ છે."))
    else:
        recs.append(("🎮 Habit Games", "તમારી missions ની પ્રગતિ સારી રીતે નોંધાઈ રહી છે. પોતાની જૂની પ્રગતિ સાથે સરખામણી કરો, બીજા વિદ્યાર્થીઓ સાથે નહીં."))

    return recs


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
      <p>Active Body · Sleep Routine · Smart Food · Healthy Habit Games</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="hp-note"><b>Sensor-free system:</b> આ module વિદ્યાર્થી દ્વારા દાખલ કરેલી માહિતી પરથી કામ કરે છે. '
        'આ medical device નથી અને કોઈ રોગનું નિદાન કરતું નથી.</div>',
        unsafe_allow_html=True
    )

    # Fetch recent data
    activity = _query_df(
        "SELECT log_date, activity, minutes, outdoor FROM activity_logs WHERE student_id=? AND log_date>=? ORDER BY log_date",
        (sid, (date.today() - timedelta(days=6)).isoformat())
    )
    sleep = _query_df(
        "SELECT log_date, sleep_time, wake_time, duration FROM sleep_logs WHERE student_id=? AND log_date>=? ORDER BY log_date",
        (sid, (date.today() - timedelta(days=6)).isoformat())
    )
    food = _query_df(
        "SELECT log_date, food_name, meal_type FROM food_logs WHERE student_id=? AND log_date>=? ORDER BY log_date DESC",
        (sid, (date.today() - timedelta(days=6)).isoformat())
    )
    habits = _query_df(
        "SELECT log_date, mission, xp FROM habit_logs WHERE student_id=? AND log_date>=? ORDER BY log_date DESC",
        (sid, (date.today() - timedelta(days=6)).isoformat())
    )

    xp_total = int(habits["xp"].sum()) if not habits.empty else 0
    activity_total = int(activity["minutes"].sum()) if not activity.empty else 0
    sleep_avg = float(sleep["duration"].mean()) if not sleep.empty else 0
    missions_done = len(habits)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🏃 Activity", f"{activity_total} min", "Last 7 days")
    m2.metric("🌙 Avg. Sleep", f"{sleep_avg:.1f} hrs" if not sleep.empty else "—", "Self-reported")
    m3.metric("🎮 Missions", str(missions_done), "Last 7 days")
    m4.metric("⭐ XP Earned", str(xp_total), "Last 7 days")

    tabs = st.tabs([
        "🏃 Active Body",
        "🌙 Sleep",
        "🥗 Smart Food",
        "🎮 Habit Games",
        "🧠 AI Insights",
        "📊 Growth Report"
    ])

    # ---------------- ACTIVE BODY ----------------
    with tabs[0]:
        st.subheader("🏃 Active Body AI")
        st.write("તમારી movement અને activity નોંધો. કોઈ wearable અથવા step sensor જરૂરી નથી.")
        with st.form("hp_activity_form", clear_on_submit=True):
            a_date = st.date_input("Activity date", value=date.today(), key="hp_a_date")
            a_type = st.selectbox("Activity", [
                "Walking", "Cycling", "Outdoor play", "Stretching",
                "Dance", "Yoga", "Sports", "Other"
            ])
            a_minutes = st.number_input("Duration (minutes)", min_value=1, max_value=300, value=15, step=5)
            a_outdoor = st.checkbox("આ activity બહાર કરી?")
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
            st.info("હજુ activity record નથી. ઉપરથી પહેલી entry ઉમેરો.")

    # ---------------- SLEEP ----------------
    with tabs[1]:
        st.subheader("🌙 Sleep Routine")
        st.write("Enter your bedtime and wake-up time. The system will calculate the duration and routine history. (સૂવાનો અને જાગવાનો સમય દાખલ કરો. સિસ્ટમ સમયગાળો અને routine history ગણશે.)")
        with st.form("hp_sleep_form", clear_on_submit=True):
            s_date = st.date_input("Sleep record date (જે દિવસે જાગ્યા)", value=date.today(), key="hp_s_date")
            c1, c2 = st.columns(2)
            with c1:
                s_bed = st.time_input("Sleep Time (સૂવાનો સમય)", value=datetime.strptime("22:00", "%H:%M").time())
            with c2:
                s_wake = st.time_input("Wake Up Time (જાગવાનો સમય)", value=datetime.strptime("06:00", "%H:%M").time())
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
            st.info("Sleep routine સમજવા માટે પહેલી entry ઉમેરો.")
        st.caption(" General Guidance: Teenagers aged 13–18 are generally recommended to get 8–10 hours of sleep. Individual needs may vary. (સામાન્ય માર્ગદર્શન: 13–18 વર્ષની ઉંમરના કિશોરોને સામાન્ય રીતે 8–10 કલાક ઊંઘની ભલામણ થાય છે. વ્યક્તિગત જરૂરિયાત અલગ હોઈ શકે.)")

    # ---------------- SMART FOOD ----------------
    with tabs[2]:
        st.subheader("🥗 Smart Food Guide")
        st.write("ભારતીય અને ગુજરાતી ખોરાક વિશે પોષણની મૂળભૂત સમજ મેળવો.")
        selected_food = st.selectbox("ખોરાક પસંદ કરો", list(FOOD_LIBRARY.keys()), key="hp_food_select")
        item = FOOD_LIBRARY[selected_food]
        st.markdown(f"### {selected_food}")
        st.info(f"**પોષક જૂથ:** {item['group']}\n\n{item['detail']}\n\n**Learning tip:** {item['tip']}")

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

    # ---------------- HABIT GAMES ----------------
    with tabs[3]:
        st.subheader("🎮 Healthy Habit Games")
        st.write("નાના, સલામત અને સ્વૈચ્છિક missions પૂર્ણ કરીને XP મેળવો.")
        st.markdown(f"### ⭐ Your XP: {xp_total}")
        mission_date = st.date_input("Mission date", value=date.today(), key="hp_mission_date")
        for idx, (mission, xp, description) in enumerate(MISSIONS):
            already = _query_df(
                "SELECT id FROM habit_logs WHERE student_id=? AND log_date=? AND mission=?",
                (sid, mission_date.isoformat(), mission)
            )
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"**{mission}**")
                st.caption(description)
            with c2:
                if already.empty:
                    if st.button(f"+{xp} XP", key=f"hp_mission_{idx}", use_container_width=True):
                        try:
                            with _connect() as con:
                                con.execute(
                                    "INSERT INTO habit_logs(student_id,log_date,mission,xp,created_at) VALUES(?,?,?,?,?)",
                                    (sid, mission_date.isoformat(), mission, xp, datetime.now().isoformat(timespec="seconds"))
                                )
                                con.commit()
                            st.success("Mission recorded!")
                            st.rerun()
                        except sqlite3.IntegrityError:
                            st.info("આ mission પહેલેથી પૂર્ણ થયેલું છે.")
                else:
                    st.success("Done ✓")
        st.caption("XP માત્ર ભાગીદારી માટે છે; તે health score અથવા medical measurement નથી.")

    # ---------------- AI INSIGHTS ----------------
    with tabs[4]:
        st.subheader("🧠 Health Intelligence Engine")
        st.write("આ prototype rule-based analysis દ્વારા દાખલ કરેલા records પરથી સૂચનો આપે છે.")
        recs = _build_recommendations(activity, sleep, food, habits)
        for heading, message in recs:
            st.markdown(f"**{heading}**")
            st.info(message)
        st.markdown("""
        **આ સિસ્ટમનું logic:**
        1. Student-entered records વાંચે છે.
        2. Recent history અને simple patterns તપાસે છે.
        3. Rule-based personalized suggestions પસંદ કરે છે.
        4. નવી entries ઉમેરાય ત્યારે insights ફરી બનાવે છે.
        """)
        st.caption("આ Rule-Based AI prototype છે; trained machine-learning model હોવાનો દાવો કરતું નથી.")

    # ---------------- GROWTH REPORT ----------------
    with tabs[5]:
        st.subheader("📊 Student Growth Report")
        st.write("છેલ્લા 7 દિવસના દાખલ કરેલા records નો સારાંશ.")
        r1, r2, r3 = st.columns(3)
        r1.metric("Activity records", len(activity))
        r2.metric("Sleep records", len(sleep))
        r3.metric("Food entries", len(food))

        if not activity.empty:
            st.markdown("#### Activity by day")
            st.bar_chart(activity.groupby("log_date")["minutes"].sum())
        if not sleep.empty:
            st.markdown("#### Sleep duration by day")
            st.line_chart(sleep.set_index("log_date")[["duration"]])
        if not habits.empty:
            st.markdown("#### Missions completed")
            st.bar_chart(habits.groupby("log_date")["xp"].sum())

        report_parts = []
        report_parts.append(f"HEALTH POWER AI - WEEKLY REPORT\nStudent ID: {sid}\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        report_parts.append(f"Activity minutes: {activity_total}")
        report_parts.append(f"Average recorded sleep hours: {sleep_avg:.2f}" if not sleep.empty else "Average recorded sleep hours: No records")
        report_parts.append(f"Food entries: {len(food)}")
        report_parts.append(f"Missions completed: {missions_done}")
        report_parts.append(f"XP earned: {xp_total}")
        report_text = "\n".join(report_parts)
        st.download_button(
            "⬇️ Download Weekly Summary (TXT)",
            data=report_text,
            file_name="health_power_weekly_report.txt",
            mime="text/plain",
            use_container_width=True
        )

        st.markdown("---")
        st.caption("Privacy: records are stored locally in health_power_ai.db and are associated with the supplied student_id. Use a stable, non-public internal student identifier; do not display sensitive records to other students.")


# ---------------------- STANDALONE RUN ------------------------

if __name__ == "__main__":
    render_health_power(st, student_id="demo_student")
