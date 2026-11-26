import streamlit as st
import pandas as pd
import sqlite3
import io
import csv
from datetime import date, datetime

def render_health_power(st, student_id):
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
                st.success(f"BMI calculation: {val:.1f}"); st.caption("Formula: weight (kg) ÷ [height (m)]². BMI is not a diagnosis or a measure of personal worth."); st.rerun()
        if not bmi.empty:
            st.markdown("#### Your saved calculation history (numbers only)")
            st.dataframe(bmi.rename(columns={"log_date":"Date","age":"Age","height_cm":"Height (cm)","weight_kg":"Weight (kg)","bmi":"BMI calculation"}),use_container_width=True,hide_index=True)

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
            st.markdown("### Practice Result")
            st.metric("Correct Answers",f"{result['total']}/16",f"{result['total']/16*100:.0f}%")
            cols=st.columns(4)
            for col,(cat,score) in zip(cols,result["scores"].items()): col.metric(cat,f"{score}/4")
            weakest=min(result["scores"],key=result["scores"].get)
            suggestions={"Logic":"Try short deduction puzzles and explain your steps.","Pattern Recognition":"Practise number, letter and shape sequences.","Memory":"Use brief recall exercises and spaced review.","Reasoning":"Work through everyday maths and explain why an answer fits."}
            st.info(f"Practice idea for {weakest}: {suggestions[weakest]}")
            st.caption("This practice result reflects only these questions and is not an IQ score or diagnosis.")
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
        report_lines=["AB SCHOOL LOOP AI — HEALTH POWER AI WEEKLY REPORT",f"Student ID: {sid}",f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}","Period: Last 7 days",f"Activity minutes: {int(a_all.minutes.sum()) if not a_all.empty else 0}",f"Sleep average hours: {float(s_all.duration.mean()):.2f}" if not s_all.empty else "Sleep average hours: No records",f"Food learning entries: {len(f_all)}",f"BMI calculations: {len(b_all)}",f"Music sessions: {len(mu_all)}",f"Mind Skills attempts: {len(m_all)}"]
        report_text="\n".join(report_lines)
        st.download_button("⬇ Download TXT Report",report_text,"health_power_weekly_report.txt","text/plain",use_container_width=True)
        csv_buffer=io.StringIO(); writer=csv.writer(csv_buffer); writer.writerow(["Student ID",sid]); writer.writerow(["Generated",datetime.now().isoformat(timespec="minutes")]); writer.writerow([]); writer.writerow(["Section","Date","Details"])
        for _,row in a_all.iterrows(): writer.writerow(["Activity",row.log_date,f"{row.activity}: {row.minutes} min; outdoor={row.outdoor}"])
        for _,row in s_all.iterrows(): writer.writerow(["Sleep",row.log_date,f"{row.sleep_time}-{row.wake_time}: {row.duration} hours"])
        for _,row in f_all.iterrows(): writer.writerow(["Food",row.log_date,f"{row.food_name}; meal={row.meal_type}"])
        for _,row in b_all.iterrows(): writer.writerow(["BMI",row.log_date,f"BMI number={row.bmi}; age={row.age}; height={row.height_cm} cm; weight={row.weight_kg} kg"])
        for _,row in mu_all.iterrows(): writer.writerow(["Music",row.log_date,f"{row.sound_type}: {row.duration_minutes} min"])
        for _,row in m_all.iterrows(): writer.writerow(["Mind Skills",row.log_date,f"{row.total_score}/{row.total_questions}; Logic={row.logic_score}; Patterns={row.pattern_score}; Memory={row.memory_score}; Reasoning={row.reasoning_score}"])
        st.download_button("⬇ Download CSV Report",csv_buffer.getvalue(),"health_power_weekly_report.csv","text/csv",use_container_width=True)
        st.caption("Report data is filtered to this student's ID. Legacy habit records are preserved in the database but Habit Games is not displayed.")


if __name__ == "__main__":
    render_health_power(st, student_id="local_demo_user")
