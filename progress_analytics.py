import streamlit as st
import pandas as pd

def show_progress_analytics():

    st.title("📈 Progress Analytics")

    quiz_score = st.slider("Average Quiz Score", 0, 100, 78)
    attendance = st.slider("Attendance", 0, 100, 92)
    homework = st.slider("Homework Completion", 0, 100, 85)
    discipline = st.slider("Discipline Score", 0, 100, 90)

    progress = (
        quiz_score +
        attendance +
        homework +
        discipline
    ) / 4

    st.metric("🚀 Overall Progress", f"{progress:.1f}%")
    st.progress(int(progress))

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Quiz", f"{quiz_score}%")
    col2.metric("Attendance", f"{attendance}%")
    col3.metric("Homework", f"{homework}%")
    col4.metric("Discipline", f"{discipline}%")

    st.subheader("📊 Student Analytics")

    chart_data = pd.DataFrame({
        "Category": [
            "Quiz",
            "Attendance",
            "Homework",
            "Discipline"
        ],
        "Score": [
            quiz_score,
            attendance,
            homework,
            discipline
        ]
    })

    st.bar_chart(chart_data.set_index("Category"))

    st.subheader("🏆 Performance Status")

    if progress >= 85:
        st.success("Excellent Progress")
    elif progress >= 70:
        st.info("Good Progress")
    else:
        st.warning("Needs Improvement")

    st.subheader("🎯 Next Target")

    st.write(f"Current Progress: {progress:.1f}%")
    st.write("Target: 90%+ Overall Performance")
