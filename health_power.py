# ============================================================
# AB SCHOOL LOOP AI - HEALTH POWER AI
# Student wellness learning dashboard (sensor-free, non-diagnostic)
# Compatible integration: render_health_power(st, student_id=...)
# ============================================================
from pathlib import Path
from datetime import date, datetime, timedelta
import sqlite3
import io
import csv
import math
import random
import struct
import wave
import streamlit as st
import pandas as pd

DB_PATH = Path(__file__).with_name("health_power_ai.db")
ASSETS_DIR = Path(__file__).with_name("assets")


def _ensure_builtin_audio():
    """Create short, original, royalty-free ambient WAV tracks on first run."""
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    sample_rate = 16000
    seconds = 18
    total = sample_rate * seconds
    tracks = {
        "memory_booster_ambient.wav": (220.0, 277.18, 329.63, "calm"),
        "soft_nature.wav": (174.61, 220.0, 261.63, "nature"),
        "focus_background.wav": (196.0, 246.94, 293.66, "focus"),
    }
    for filename, (f1, f2, f3, style) in tracks.items():
        path = ASSETS_DIR / filename
        if path.is_file():
            continue
        rng = random.Random(filename)
        with wave.open(str(path), "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            frames = bytearray()
            for i in range(total):
                t = i / sample_rate
                fade = min(1.0, t / 1.5, (seconds - t) / 1.5)
                slow = 0.72 + 0.18 * math.sin(2 * math.pi * 0.07 * t)
                pad = (0.48 * math.sin(2 * math.pi * f1 * t)
                       + 0.27 * math.sin(2 * math.pi * f2 * t)
                       + 0.16 * math.sin(2 * math.pi * f3 * t))
                if style == "nature":
                    # Soft synthesized breeze/rain texture, kept deliberately quiet.
                    texture = (rng.random() * 2 - 1) * 0.055
                    value = 0.15 * pad + texture
                elif style == "focus":
                    value = 0.30 * pad * (0.92 + 0.08 * math.sin(2 * math.pi * 0.11 * t))
                else:
                    value = 0.32 * pad * slow
                sample = int(max(-1.0, min(1.0, value * fade)) * 32767)
                frames.extend(struct.pack("<h", sample))
            wav.writeframes(frames)


def _connect():
    con = sqlite3.connect(DB_PATH, timeout=15)
    con.row_factory = sqlite3.Row
    return con



def _init_db():
    # CREATE IF NOT EXISTS preserves existing records/tables. Legacy habit_logs is untouched.
    with _connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT, student_id TEXT NOT NULL,
            log_date TEXT NOT NULL, activity TEXT NOT NULL, minutes INTEGER NOT NULL,
            outdoor INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL)""")
        con.execute("""CREATE TABLE IF NOT EXISTS sleep_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT, student_id TEXT NOT NULL,
            log_date TEXT NOT NULL, sleep_time TEXT NOT NULL, wake_time TEXT NOT NULL,
            duration REAL NOT NULL, created_at TEXT NOT NULL)""")
        con.execute("""CREATE TABLE IF NOT EXISTS food_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT, student_id TEXT NOT NULL,
            log_date TEXT NOT NULL, food_name TEXT NOT NULL, meal_type TEXT NOT NULL,
            created_at TEXT NOT NULL)""")
        con.execute("""CREATE TABLE IF NOT EXISTS bmi_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT, student_id TEXT NOT NULL,
            log_date TEXT NOT NULL, age INTEGER NOT NULL, height_cm REAL NOT NULL,
            weight_kg REAL NOT NULL, bmi REAL NOT NULL, created_at TEXT NOT NULL)""")
        con.execute("""CREATE TABLE IF NOT EXISTS music_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT, student_id TEXT NOT NULL,
            log_date TEXT NOT NULL, sound_type TEXT NOT NULL, duration_minutes INTEGER NOT NULL,
            created_at TEXT NOT NULL)""")
        con.execute("""CREATE TABLE IF NOT EXISTS mind_skill_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT, student_id TEXT NOT NULL,
            log_date TEXT NOT NULL, logic_score INTEGER NOT NULL,
            pattern_score INTEGER NOT NULL, memory_score INTEGER NOT NULL,
            reasoning_score INTEGER NOT NULL, total_score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL, created_at TEXT NOT NULL)""")
        con.commit()


def _df(sql, params=()):
    with _connect() as con:
        return pd.read_sql_query(sql, con, params=params)



def _save(sql, params):
    with _connect() as con:
        con.execute(sql, params)
        con.commit()



def _inject_css():
    st.markdown("""<style>
    .hp-hero{padding:26px;border-radius:22px;background:linear-gradient(120deg,#071326,#10304c 58%,#075b63);border:1px solid #22d3ee55;margin-bottom:14px}
    .hp-hero h1{color:#f4f8ff!important;font-size:30px;margin:5px 0}
    .hp-hero p{color:#d3e7f6!important;margin:0}
    .hp-kicker{color:#5eead4;font-weight:800;letter-spacing:2px;font-size:11px}
    .hp-note{background:#22d3ee12;border:1px solid #22d3ee35;padding:12px;border-radius:12px;margin:8px 0}
    div[data-testid="stMetric"]{background:#0b2043;border:1px solid #22d3ee33;padding:12px;border-radius:14px}
    </style>""", unsafe_allow_html=True)



FOOD_LIBRARY = {
    "દાળ / કઠોળ": ("Protein and fibre", "દાળ અને કઠોળ પ્રોટીન તથા ફાઇબરના સ્ત્રોત છે.", "વિવિધ કઠોળ વિશે શીખો."),
    "દૂધ / દહીં": ("Calcium and protein", "દૂધ અને દહીં કેલ્શિયમ તથા પ્રોટીન આપી શકે છે.", "ખોરાકની પસંદગી વ્યક્તિ પ્રમાણે બદલાય છે."),
    "ફળો": ("Vitamins and fibre", "ફળોમાં વિવિધ વિટામિન, ખનિજ અને ફાઇબર હોય છે.", "મોસમી ફળો વિશે જાણો."),
    "શાકભાજી": ("Vitamins, minerals and fibre", "શાકભાજી વિવિધ પોષક તત્ત્વો આપે છે.", "વિવિધ શાકભાજી વિશે શીખો."),
    "અનાજ / રોટલી": ("Energy-giving carbohydrates", "અનાજ કાર્બોહાઇડ્રેટ્સનો સ્ત્રોત છે.", "વિવિધ અનાજના પ્રકારો જાણો."),
    "સૂકા મેવા / બીજ": ("Nutrients and fats", "સૂકા મેવા અને બીજમાં વિવિધ પોષક તત્ત્વો હોય છે.", "એલર્જી હોય તો સાવચેતી રાખો."),
    "પાણી": ("Hydration", "પાણી શરીરના સામાન્ય કાર્યો માટે જરૂરી છે.", "દિવસભર પાણી ઉપલબ્ધ રાખો."),
}


MIND_QUESTIONS = [
    ("Logic", "All roses are flowers. Some flowers fade quickly. Which statement must be true?", ["All roses fade quickly", "All roses are flowers", "No flowers are roses", "All flowers are roses"], 1),
    ("Logic", "If today is Wednesday, what day is 3 days later?", ["Friday", "Saturday", "Sunday", "Monday"], 1),
    ("Logic", "A is taller than B, and B taller than C. Who is shortest?", ["A", "B", "C", "Cannot tell"], 2),
    ("Logic", "Which is the odd one out?", ["Square", "Triangle", "Circle", "Cube"], 3),
    ("Pattern Recognition", "2, 4, 8, 16, __", ["18", "24", "32", "30"], 2),
    ("Pattern Recognition", "A, C, E, G, __", ["H", "I", "J", "K"], 1),
    ("Pattern Recognition", "1, 4, 9, 16, __", ["20", "24", "25", "26"], 2),
    ("Pattern Recognition", "Which shape has 3 sides?", ["Circle", "Triangle", "Square", "Pentagon"], 1),
    ("Memory", "Remember this sequence: 5 – 2 – 9. Which number was in the middle?", ["5", "2", "9", "7"], 1),
    ("Memory", "Which word was shown? (Imagine remembering: ORBIT)", ["ORBIT", "ORANGE", "OBJECT", "OCEAN"], 0),
    ("Memory", "A list has: red, blue, green. Which was NOT included?", ["Red", "Blue", "Yellow", "Green"], 2),
    ("Memory", "Remember: 12, 7, 4. What was the last number?", ["12", "7", "4", "14"], 2),
    ("Reasoning", "If 3 notebooks cost ₹30, what is the cost of 1 at the same rate?", ["₹5", "₹10", "₹15", "₹30"], 1),
    ("Reasoning", "A clock shows 3:00. What is the angle between its hands?", ["30°", "60°", "90°", "180°"], 2),
    ("Reasoning", "Which is heavier: 1 kg cotton or 1 kg iron?", ["Cotton", "Iron", "Both equal", "Cannot tell"], 2),
    ("Reasoning", "If you rearrange LISTEN, which word can be made?", ["SILENT", "LITTLE", "STONE", "LINES"], 0),
]



def _recent(sid, table, columns, days=7, order="log_date DESC"):
    start = (date.today() - timedelta(days=days-1)).isoformat()
    return _df(f"SELECT {columns} FROM {table} WHERE student_id=? AND log_date>=? ORDER BY {order}", (sid, start))



def _make_insights(activity, sleep, food, bmi, music, mind):
    tips = []
    if activity.empty:
        tips.append(("Active Body", "તમારી અનુકૂળ પ્રવૃત્તિનો એક રેકોર્ડ ઉમેરો. આરામ અને પ્રવૃત્તિ બંને મહત્વના છે."))
    else:
        tips.append(("Active Body", f"છેલ્લા 7 દિવસમાં {int(activity.minutes.sum())} મિનિટની પ્રવૃત્તિ નોંધાઈ છે. પોતાની સુવિધા મુજબ નિયમિત વિરામ અને હલનચલન રાખો."))
    if sleep.empty:
        tips.append(("Sleep", "સૂવાનો અને જાગવાનો સમય નોંધવાથી તમારી રૂટિન સમજવામાં મદદ મળશે."))
    else:
        avg = float(sleep.duration.mean())
        tips.append(("Sleep", f"નોંધાયેલા સમયનો સરેરાશ {avg:.1f} કલાક છે. નિયમિત સૂવાની રૂટિન રાખવાનો પ્રયત્ન કરો."))
    tips.append(("Smart Food", "વિવિધ ખોરાક અને પોષક તત્ત્વો વિશે શીખતા રહો; એક જ ખોરાકને સર્વથા સારો કે ખરાબ ન ગણો." if not food.empty else "Food Libraryમાંથી એક ખોરાક પસંદ કરી તેની પોષક માહિતી વાંચો અને નોંધ ઉમેરો."))
    tips.append(("BMI", "BMI માત્ર ગણિતીય સૂચક છે. બાળકો અને કિશોરો માટે તેનું અર્થઘટન ઉંમર અને અન્ય સંદર્ભો સાથે જ થાય છે; અહીં કોઈ નિદાન થતું નથી." if not bmi.empty else "BMI ગણતરી કરવી વૈકલ્પિક છે. કિશોરો માટે BMIનું અર્થઘટન અહીં આપવામાં આવતું નથી."))
    tips.append(("Memory Music", "ઓડિયો સાંભળો તો આરામદાયક વોલ્યુમ રાખો અને વચ્ચે વિરામ લો." if not music.empty else "જો ઓડિયો ફાઇલ ઉપલબ્ધ હોય તો ટૂંકું આરામદાયક listening session અજમાવી શકો."))
    if mind.empty:
        tips.append(("Mind Skills", "Mind Skills practice test અજમાવો. આ શીખવા માટેની કસરત છે, પ્રમાણિત IQ પરીક્ષણ નથી."))
    else:
        last = int(mind.iloc[0].total_score)
        tips.append(("Mind Skills", f"તમારા તાજેતરના અભ્યાસ-કૌશલ્ય અભ્યાસમાં {last}/16 જવાબ સાચા હતા. પોતાની અગાઉની કોશિશ સાથે પ્રગતિ જોવી ઉપયોગી છે."))
    return tips



def _bmi_growth_report(age):
    """Safe, non-diagnostic age-context and supportive steps."""
    age = int(age)
    if age < 20:
        age_note = "બાળકો અને કિશોરોમાં BMI ને ઉંમર, sex-specific growth chart અને સમય સાથેના માપથી સમજવું પડે છે; BMI એકલો growth category નક્કી કરતો નથી."
    else:
        age_note = "BMI એક screening ગણતરી છે; તે એકલી આરોગ્ય નક્કી કરતી નથી."
    steps = [
        "• નિયમિત ભોજન લો અને અનાજ, દાળ, શાકભાજી, ફળ તથા અન્ય ખોરાકમાં વિવિધતા રાખો.",
        "• ભોજન છોડવાને બદલે ભૂખ અને શરીરની જરૂરિયાત પ્રમાણે ખાવાનું ધ્યાન રાખો.",
        "• ચાલવું, રમત, નૃત્ય અથવા તમને ગમતી પ્રવૃત્તિ આનંદથી કરો; આરામ પણ જરૂરી છે.",
        "• ઉંમર મુજબ પૂરતી ઊંઘ અને નિયમિત sleep routine રાખો.",
        "• Growth વિશે ચિંતા હોય તો trusted adult સાથે વાત કરી આરોગ્ય નિષ્ણાત પાસે growth chart review કરાવો."
    ]
    return age_note, steps


def _mind_practice_profile(total, scores):
    """Practice profile for this short quiz, not an IQ estimate."""
    if total >= 13:
        profile = "Strong performance on this practice set"
    elif total >= 9:
        profile = "Developing practice performance"
    else:
        profile = "More practice may help on this set"
    tips = {
        "Logic": "Try short deduction puzzles and write each step in your own words.",
        "Pattern Recognition": "Practise number, letter and shape patterns; explain the rule you spotted.",
        "Memory": "Use short recall games, then revisit information after a break.",
        "Reasoning": "Work through everyday maths and explain why the answer makes sense.",
    }
    weakest = min(scores, key=scores.get) if scores else None
    focus = f"Practice focus: {weakest}. {tips[weakest]}" if weakest else "Practice one skill at a time."
    return profile, focus, tips


def _mind_history_profile(total, total_questions=16):
    pct = (int(total) / max(1, int(total_questions))) * 100
    if pct >= 80:
        return "Strong practice result"
    if pct >= 55:
        return "Developing practice result"
    return "Practice opportunity"

def render_health_power(st, student_id=None):
    """Render Health Power inside the authenticated AB SCHOOL LOOP AI app."""
    if student_id is None or not str(student_id).strip():
        st.warning("Health Power ખોલવા માટે માન્ય logged-in student ID જરૂરી છે.")
        return
    sid = str(student_id).strip()[:100]
    _init_db()
    _ensure_builtin_audio()
    _inject_css()
    today = date.today().isoformat()
    st.markdown(f"""<div class="hp-hero"><div class="hp-kicker">AB SCHOOL LOOP AI · STUDENT WELL-BEING</div><h1>🧬 HEALTH POWER AI</h1><p>Active Body · Sleep · Smart Food · Mind Skills · Growth</p></div>""", unsafe_allow_html=True)
    st.markdown('<div class="hp-note">Student-entered wellness information only. This is an educational prototype, not a medical device or diagnosis tool.</div>', unsafe_allow_html=True)

    activity = _recent(sid, "activity_logs", "log_date, activity, minutes, outdoor")
    sleep = _recent(sid, "sleep_logs", "log_date, sleep_time, wake_time, duration")
    food = _recent(sid, "food_logs", "log_date, food_name, meal_type")
    bmi = _recent(sid, "bmi_logs", "log_date, age, height_cm, weight_kg, bmi")
    music = _recent(sid, "music_logs", "log_date, sound_type, duration_minutes")
    mind = _recent(sid, "mind_skill_logs", "log_date, logic_score, pattern_score, memory_score, reasoning_score, total_score, total_questions", order="log_date DESC, id DESC")
    activity_total = int(activity.minutes.sum()) if not activity.empty else 0
    sleep_avg = float(sleep.duration.mean()) if not sleep.empty else None
    m1,m2,m3,m4 = st.columns(4)
    m1.metric("🏃 Activity", f"{activity_total} min", "Last 7 days")
    m2.metric("🌙 Avg Sleep", f"{sleep_avg:.1f} hrs" if sleep_avg is not None else "—", "Self-reported")
    m3.metric("🧠 Mind Tests", str(len(mind)), "Attempts")
    m4.metric("🎵 Music Sessions", str(len(music)), "Saved sessions")

    tabs = st.tabs(["🏃 Active Body", "🌙 Sleep", "🥗 Smart Food", "📊 BMI Calculator", "🎵 Memory Booster Music", "🧠 Mind Skills Test", "✨ AI Insights", "📈 Growth Report"])

    # Active Body
    with tabs[0]:
        st.subheader("🏃 Active Body")
        st.write("તમારી રોજિંદી હલનચલન નોંધો. કોઈ sensor જરૂરી નથી.")
        with st.form("hp_activity_form", clear_on_submit=True):
            d = st.date_input("Activity date", date.today(), key="hp_act_date")
            kind = st.selectbox("Activity type", ["Walking", "Cycling", "Outdoor play", "Stretching", "Dance", "Yoga", "Sports", "Other"], key="hp_act_kind")
            mins = st.number_input("Duration (minutes)", 1, 300, 15, 5, key="hp_act_mins")
            outdoors = st.checkbox("Outdoor activity", key="hp_act_out")
            submit = st.form_submit_button("Save Activity", use_container_width=True)
            if submit:
                _save("INSERT INTO activity_logs(student_id,log_date,activity,minutes,outdoor,created_at) VALUES(?,?,?,?,?,?)", (sid,d.isoformat(),kind,int(mins),int(outdoors),datetime.now().isoformat(timespec="seconds")))
                st.success("Activity record saved!"); st.rerun()
        if not activity.empty:
            st.dataframe(activity.rename(columns={"log_date":"Date","activity":"Activity","minutes":"Minutes","outdoor":"Outdoor"}), use_container_width=True, hide_index=True)
            st.bar_chart(activity.groupby("log_date").minutes.sum())
        else: st.info("હજુ activity record નથી. ઉપરથી ઉમેરો.")

    # Sleep
    with tabs[1]:
        st.subheader("🌙 Sleep Tracker")
        with st.form("hp_sleep_form", clear_on_submit=True):
            sd = st.date_input("Sleep date (bedtime date)", date.today(), key="hp_sleep_date")
            c1,c2 = st.columns(2)
            with c1: bed = st.time_input("Bedtime", datetime.strptime("22:00","%H:%M").time(), key="hp_bed")
            with c2: wake = st.time_input("Wake-up time", datetime.strptime("06:00","%H:%M").time(), key="hp_wake")
            save_sleep = st.form_submit_button("Save Sleep", use_container_width=True)
            if save_sleep:
                bm=bed.hour*60+bed.minute; wm=wake.hour*60+wake.minute
                dur=((wm-bm)%(24*60))/60
                if dur<=0 or dur>18: st.error("સમય ફરી તપાસો; દાખલ કરેલો સમય માન્ય નથી.")
                else:
                    _save("INSERT INTO sleep_logs(student_id,log_date,sleep_time,wake_time,duration,created_at) VALUES(?,?,?,?,?,?)", (sid,sd.isoformat(),bed.strftime("%H:%M"),wake.strftime("%H:%M"),round(dur,2),datetime.now().isoformat(timespec="seconds")))
                    st.success(f"Sleep entry saved: {dur:.1f} hours"); st.rerun()
        if not sleep.empty:
            st.dataframe(sleep.rename(columns={"log_date":"Date","sleep_time":"Bedtime","wake_time":"Wake-up","duration":"Hours"}),use_container_width=True,hide_index=True)
            st.line_chart(sleep.set_index("log_date")[["duration"]])
        else: st.info("તમારી પ્રથમ sleep entry ઉમેરો.")
        st.caption("સામાન્ય માર્ગદર્શન: 13–18 વર્ષની કિશોરો માટે સામાન્ય રીતે 8–10 કલાક ઊંઘ સૂચવાય છે; વ્યક્તિગત જરૂરિયાત બદલાય શકે.")

    # Smart Food
    with tabs[2]:
        st.subheader("🥗 Smart Food Learning")
        selected = st.selectbox("Food Library", list(FOOD_LIBRARY), key="hp_food_select")
        group, detail, tip = FOOD_LIBRARY[selected]
        st.markdown(f"### {selected}"); st.info(f"**Nutrient group:** {group}\n\n{detail}\n\n**Learning tip:** {tip}")
        with st.form("hp_food_form", clear_on_submit=True):
            fd = st.date_input("Entry date", date.today(), key="hp_food_date")
            meal = st.selectbox("Meal", ["Breakfast","Lunch","Snack","Dinner"], key="hp_food_meal")
            note = st.text_input("Optional learning note", max_chars=300, key="hp_food_note")
            sf = st.form_submit_button("Save Food Learning", use_container_width=True)
            if sf:
                food_label = selected + (" — " + note.strip() if note.strip() else "")
                _save("INSERT INTO food_logs(student_id,log_date,food_name,meal_type,created_at) VALUES(?,?,?,?,?)", (sid,fd.isoformat(),food_label,meal,datetime.now().isoformat(timespec="seconds")))
                st.success("Food learning record saved."); st.rerun()
        if not food.empty: st.dataframe(food.rename(columns={"log_date":"Date","food_name":"Food / Note","meal_type":"Meal"}),use_container_width=True,hide_index=True)
        else: st.info("Food learning records અહીં દેખાશે.")

    # BMI Calculator
    with tabs[3]:
        st.subheader("📊 BMI Calculator")
        st.warning("BMI માત્ર ગણિતીય આંકડો છે. બાળકો/કિશોરોમાં તેનો અર્થ ઉંમર અને sex-specific growth references વડે સમજાય છે. આ પ્રોટોટાઇપ કોઈ category, diagnosis કે weight advice આપતું નથી.")
        with st.form("hp_bmi_form", clear_on_submit=True):
            bd = st.date_input("Record date", date.today(), key="hp_bmi_date")
            age = st.number_input("Age (years)", min_value=2, max_value=100, value=16, step=1, key="hp_bmi_age")
            height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=160.0, step=0.5, key="hp_bmi_height")
            weight = st.number_input("Weight (kg)", min_value=5.0, max_value=300.0, value=50.0, step=0.5, key="hp_bmi_weight")
            calc = st.form_submit_button("Calculate & Save BMI", use_container_width=True)
            if calc:
                hm=height/100.0
                val=weight/(hm**2)
                _save("INSERT INTO bmi_logs(student_id,log_date,age,height_cm,weight_kg,bmi,created_at) VALUES(?,?,?,?,?,?,?)", (sid,bd.isoformat(),int(age),float(height),float(weight),round(val,1),datetime.now().isoformat(timespec="seconds")))
                st.success(f"BMI calculation saved: {val:.1f}")
                age_note, bmi_steps = _bmi_growth_report(int(age))
                st.markdown("### Growth context")
                st.info(age_note)
                st.markdown("### Suggestions")
                for step in bmi_steps:
                    st.markdown(step)
                st.caption("Formula: weight (kg) ÷ [height (m)]². BMI is not a diagnosis or a target number.")
                st.rerun()
        if not bmi.empty:
            st.markdown("#### BMI History")
            st.dataframe(bmi.rename(columns={"log_date":"Date","age":"Age","height_cm":"Height (cm)","weight_kg":"Weight (kg)","bmi":"BMI calculation"}),use_container_width=True,hide_index=True)
            st.caption("BMI entries are calculation history only; growth interpretation requires age-appropriate chart context.")

    # Memory Booster Music
    with tabs[4]:
        st.subheader("🎵 Memory Booster Music")
        st.write("Optional original background audio for a quiet study or relaxation session. Music is not guaranteed to improve memory.")
        st.caption("ત્રણેય audio tracks આ app પહેલી વાર ખોલાય ત્યારે આપમેળે બને છે; અલગથી audio download કરવાની જરૂર નથી.")
        sound_options = {"Calm Ambient":"memory_booster_ambient.wav", "Soft Nature":"soft_nature.wav", "Focus Background":"focus_background.wav"}
        available = {label: ASSETS_DIR / fname for label,fname in sound_options.items() if (ASSETS_DIR/fname).is_file()}
        if available:
            chosen = st.selectbox("Sound option", list(available), key="hp_music_sound")
            st.audio(str(available[chosen]))
            st.caption("Use a comfortable volume and take breaks.")
            with st.form("hp_music_log_form", clear_on_submit=True):
                session_date = st.date_input("Session date", date.today(), key="hp_music_date")
                duration = st.selectbox("Session duration", [5,10,15,20,25,30], key="hp_music_duration")
                logmusic = st.form_submit_button("Save Listening Session", use_container_width=True)
                if logmusic:
                    _save("INSERT INTO music_logs(student_id,log_date,sound_type,duration_minutes,created_at) VALUES(?,?,?,?,?)", (sid,session_date.isoformat(),chosen,int(duration),datetime.now().isoformat(timespec="seconds")))
                    st.success("Listening session saved."); st.rerun()
        else:
            st.warning("Audio files generate થઈ શકી નથી. App ને ફરીથી reload કરો અથવા deployment logs તપાસો.")
        if not music.empty: st.dataframe(music.rename(columns={"log_date":"Date","sound_type":"Sound","duration_minutes":"Minutes"}),use_container_width=True,hide_index=True)
        else: st.caption("Listening history will appear here after you save a session.")

    # Mind Skills
    with tabs[5]:
        st.subheader("🧠 Mind Skills & Intelligence Practice Test")
        st.caption("16 original practice questions: Logic, Pattern Recognition, Memory and Reasoning. Not a standardized IQ test.")
        if "hp_mind_attempt" not in st.session_state: st.session_state.hp_mind_attempt = 0
        attempt = st.session_state.hp_mind_attempt
        already_saved = st.session_state.get("hp_mind_saved_attempt") == attempt
        with st.form("hp_mind_test_form"):
            answers=[]
            for i,(cat,q,opts,correct) in enumerate(MIND_QUESTIONS):
                st.markdown(f"**Q{i+1}. ({cat}) {q}**")
                answers.append(st.radio("Select one answer",options=opts,index=None,key=f"hp_mind_answer_{attempt}_{i}",label_visibility="collapsed"))
            submit_test=st.form_submit_button("Submit Practice Test",use_container_width=True,disabled=already_saved)
        if submit_test:
            if any(a is None for a in answers):
                st.warning("સબમિટ કરતા પહેલાં બધા 16 પ્રશ્નોના જવાબ પસંદ કરો.")
            else:
                scores={"Logic":0,"Pattern Recognition":0,"Memory":0,"Reasoning":0}
                for a,(cat,q,question_options,correct) in zip(answers,MIND_QUESTIONS):
                    if question_options.index(a)==correct: scores[cat]+=1
                total=sum(scores.values())
                st.session_state.hp_mind_result={"scores":scores,"total":total,"answers":answers}
                st.session_state.hp_mind_saved_attempt=attempt
                _save("INSERT INTO mind_skill_logs(student_id,log_date,logic_score,pattern_score,memory_score,reasoning_score,total_score,total_questions,created_at) VALUES(?,?,?,?,?,?,?,?,?)", (sid,today,scores["Logic"],scores["Pattern Recognition"],scores["Memory"],scores["Reasoning"],total,16,datetime.now().isoformat(timespec="seconds")))
        result=st.session_state.get("hp_mind_result")
        if result:
            st.markdown("### Practice Result & Learning Profile")
            st.metric("Correct Answers",f"{result['total']}/16",f"{result['total']/16*100:.0f}%")
            cols=st.columns(4)
            for col,(cat,score) in zip(cols,result["scores"].items()): col.metric(cat,f"{score}/4")
            profile, focus, tips = _mind_practice_profile(result["total"], result["scores"])
            st.markdown(f"**Practice profile:** {profile}")
            st.markdown("#### Suggestions")
            st.markdown(f"• {focus}")
            for cat, score in result["scores"].items():
                st.markdown(f"• **{cat} ({score}/4):** {tips[cat]}")
            st.caption("This is a short learning practice quiz. It does not measure IQ or determine intelligence.")
            if st.button("Start a new practice attempt",key="hp_new_mind_attempt"):
                st.session_state.hp_mind_attempt = attempt + 1
                st.session_state.pop("hp_mind_result",None)
                st.rerun()
        if not mind.empty:
            st.markdown("#### Previous attempts")
            st.dataframe(mind.rename(columns={"log_date":"Date","logic_score":"Logic /4","pattern_score":"Patterns /4","memory_score":"Memory /4","reasoning_score":"Reasoning /4","total_score":"Total /16","total_questions":"Questions"}),use_container_width=True,hide_index=True)


    # AI Insights
    with tabs[6]:
        st.subheader("✨ AI Insights")
        st.write("Transparent rule-based insights from your own recent records (not a trained ML model).")
        for heading,message in _make_insights(activity,sleep,food,bmi,music,mind):
            st.markdown(f"**{heading}**"); st.info(message)
        st.caption("Suggestions are educational and non-diagnostic. Only the current student's records are used.")

    # Growth Report - last tab
    with tabs[7]:
        st.subheader("📈 Growth Report")
        st.caption("Student-specific report for the last 7 days. BMI section lists saved calculations only.")
        a_all=_recent(sid,"activity_logs","log_date, activity, minutes, outdoor")
        s_all=_recent(sid,"sleep_logs","log_date, sleep_time, wake_time, duration")
        f_all=_recent(sid,"food_logs","log_date, food_name, meal_type")
        b_all=_recent(sid,"bmi_logs","log_date, age, height_cm, weight_kg, bmi")
        mu_all=_recent(sid,"music_logs","log_date, sound_type, duration_minutes")
        m_all=_recent(sid,"mind_skill_logs","log_date, logic_score, pattern_score, memory_score, reasoning_score, total_score, total_questions",order="log_date DESC, id DESC")
        r1,r2,r3,r4=st.columns(4); r1.metric("Activity records",len(a_all)); r2.metric("Sleep records",len(s_all)); r3.metric("Food entries",len(f_all)); r4.metric("Mind test attempts",len(m_all))
        if not a_all.empty: st.markdown("#### Activity by date"); st.bar_chart(a_all.groupby("log_date").minutes.sum())
        if not s_all.empty: st.markdown("#### Sleep duration"); st.line_chart(s_all.set_index("log_date")[["duration"]])
        if not m_all.empty: st.markdown("#### Mind Skills score history"); st.line_chart(m_all.set_index("log_date")[["total_score"]])
        if not a_all.empty: st.markdown("**Activity records**"); st.dataframe(a_all,use_container_width=True,hide_index=True)
        if not s_all.empty: st.markdown("**Sleep records**"); st.dataframe(s_all,use_container_width=True,hide_index=True)
        if not f_all.empty: st.markdown("**Food learning records**"); st.dataframe(f_all,use_container_width=True,hide_index=True)
        if not b_all.empty: st.markdown("**BMI calculations (number only; no categories)**"); st.dataframe(b_all,use_container_width=True,hide_index=True)
        if not mu_all.empty: st.markdown("**Music sessions**"); st.dataframe(mu_all,use_container_width=True,hide_index=True)
        if not m_all.empty: st.markdown("**Mind Skills attempts**"); st.dataframe(m_all,use_container_width=True,hide_index=True)
        report_lines=["AB SCHOOL LOOP AI — HEALTH POWER AI WEEKLY REPORT",f"Student ID: {sid}",f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}","Period: Last 7 days",f"Activity minutes: {int(a_all.minutes.sum()) if not a_all.empty else 0}",f"Sleep average hours: {float(s_all.duration.mean()):.2f}" if not s_all.empty else "Sleep average hours: No records",f"Food learning entries: {len(f_all)}",f"BMI calculations: {len(b_all)} (growth category not assigned)",f"Music sessions: {len(mu_all)}",f"Mind Skills attempts: {len(m_all)}"]
        report_text="\n".join(report_lines)
        st.download_button("⬇ Download TXT Report",report_text,"health_power_weekly_report.txt","text/plain",use_container_width=True)
        csv_buffer=io.StringIO(); writer=csv.writer(csv_buffer); writer.writerow(["Student ID",sid]); writer.writerow(["Generated",datetime.now().isoformat(timespec="minutes")]); writer.writerow([]); writer.writerow(["Section","Date","Details"])
        for _,row in a_all.iterrows(): writer.writerow(["Activity",row.log_date,f"{row.activity}: {row.minutes} min; outdoor={row.outdoor}"])
        for _,row in s_all.iterrows(): writer.writerow(["Sleep",row.log_date,f"{row.sleep_time}-{row.wake_time}: {row.duration} hours"])
        for _,row in f_all.iterrows(): writer.writerow(["Food",row.log_date,f"{row.food_name}; meal={row.meal_type}"])
        for _,row in b_all.iterrows(): writer.writerow(["BMI",row.log_date,f"BMI number={row.bmi}; age={row.age}; height={row.height_cm} cm; weight={row.weight_kg} kg"])
        for _,row in mu_all.iterrows(): writer.writerow(["Music",row.log_date,f"{row.sound_type}: {row.duration_minutes} min"])
        for _,row in m_all.iterrows(): writer.writerow(["Mind Skills",row.log_date,f"{row.total_score}/{row.total_questions}; Practice profile={_mind_history_profile(row.total_score,row.total_questions)}; Logic={row.logic_score}; Patterns={row.pattern_score}; Memory={row.memory_score}; Reasoning={row.reasoning_score}"])
        st.download_button("⬇ Download CSV Report",csv_buffer.getvalue(),"health_power_weekly_report.csv","text/csv",use_container_width=True)
        st.caption("Report data is filtered to this student's ID. Legacy habit records are preserved in the database but Habit Games is not displayed.")


if __name__ == "__main__":
    render_health_power(st, student_id="local_demo_user")
