import streamlit as st
import pandas as pd

def show_mind_power():

    st.title("🧠 Brain Analytics Dashboard")

    # Inputs
    memory = st.slider("Memory", 0, 100, 75)
    focus = st.slider("Focus", 0, 100, 70)
    concentration = st.slider("Concentration", 0, 100, 80)
    energy = st.slider("Energy", 0, 100, 85)
    stress = st.slider("Stress", 0, 100, 25)

    # Score
    brain_score = (
        memory + focus + concentration + energy + (100 - stress)
    ) / 5

    st.metric("🧠 Brain Power Score", f"{brain_score:.1f}%")
    st.progress(int(brain_score))

    # Analytics Cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Memory", f"{memory}%")

    with col2:
        st.metric("Focus", f"{focus}%")

    with col3:
        st.metric("Energy", f"{energy}%")

    st.divider()

    # Performance Chart
    st.subheader("📊 Brain Performance Analysis")

    chart_data = pd.DataFrame({
        "Category": ["Memory", "Focus", "Concentration", "Energy", "Stress"],
        "Score": [memory, focus, concentration, energy, stress]
    })

    st.bar_chart(
        chart_data.set_index("Category")
    )

    st.divider()

    # AI Analysis
    st.subheader("🤖 AI Brain Report")

    if brain_score >= 85:
        st.success(
            "Excellent brain performance. You are ready for high-level study sessions."
        )

    elif brain_score >= 70:
        st.info(
            "Good performance. Maintain consistency and healthy habits."
        )

    else:
        st.warning(
            "Brain efficiency is low. Improve sleep, hydration and focus."
        )

    st.divider()

    # JEE Study Suggestion
    st.subheader("🎯 JEE Preparation Suggestions")

    suggestions = []

    if memory < 70:
        suggestions.append("📚 Practice revision daily.")

    if focus < 70:
        suggestions.append("⏳ Use Pomodoro Method (25 + 5).")

    if stress > 50:
        suggestions.append("😌 Take short breaks and meditation.")

    if energy < 70:
        suggestions.append("🥗 Sleep 7-8 hours and eat healthy.")

    if not suggestions:
        suggestions.append("🔥 Excellent! Keep studying like this.")

    for item in suggestions:
        st.write(item)
