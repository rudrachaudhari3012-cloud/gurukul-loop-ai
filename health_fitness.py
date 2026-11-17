import streamlit as st
import pandas as pd
from datetime import date
import plotly.express as px

def show_health_fitness(user):

    st.title("🏃 Health & Fitness Tracker")

    st.subheader("Daily Health Entry")

    with st.form("health_form"):

        log_date = st.date_input(
            "Date",
            value=date.today()
        )

        sleep = st.slider(
            "😴 Sleep Hours",
            0.0,
            12.0,
            8.0
        )

        water = st.slider(
            "💧 Water Glasses",
            0,
            20,
            8
        )

        exercise = st.slider(
            "🏋 Exercise Minutes",
            0,
            180,
            30
        )

        submit = st.form_submit_button(
            "✅ Save Health Record"
        )

    if submit:

        save_health_log(
            user["id"],
            str(log_date),
            sleep,
            water,
            exercise
        )

        st.success("Health record saved successfully.")

    logs = get_health_logs(user["id"])

    if logs:

        df = pd.DataFrame(logs)

        st.subheader("📊 Weekly Health Analytics")

        avg_sleep = round(
            df["sleep_hours"].mean(), 1
        )

        avg_water = round(
            df["water_glasses"].mean(), 1
        )

        avg_exercise = round(
            df["exercise_minutes"].mean(), 1
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Avg Sleep",
            f"{avg_sleep} hrs"
        )

        c2.metric(
            "Avg Water",
            f"{avg_water} glasses"
        )

        c3.metric(
            "Avg Exercise",
            f"{avg_exercise} min"
        )

        fig = px.line(
            df,
            x="log_date",
            y="sleep_hours",
            markers=True,
            title="Sleep Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        fig2 = px.line(
            df,
            x="log_date",
            y="exercise_minutes",
            markers=True,
            title="Exercise Trend"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        st.subheader("📋 Health History")
        st.dataframe(
            df[
                [
                    "log_date",
                    "sleep_hours",
                    "water_glasses",
                    "exercise_minutes"
                ]
            ],
            use_container_width=True
        )
