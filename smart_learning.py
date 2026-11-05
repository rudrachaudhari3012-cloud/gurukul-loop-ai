import streamlit as st
import pandas as pd

def show_smart_learning():

    st.title("📚 Smart Learning Dashboard")

    math = st.slider("Mathematics", 0, 100, 75)
    physics = st.slider("Physics", 0, 100, 70)
    chemistry = st.slider("Chemistry", 0, 100, 80)

    learning_score = (math + physics + chemistry) / 3

    st.metric("🎯 Learning Score", f"{learning_score:.1f}%")
    st.progress(int(learning_score))

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Math", f"{math}%")

    with col2:
        st.metric("Physics", f"{physics}%")

    with col3:
        st.metric("Chemistry", f"{chemistry}%")

    st.subheader("📊 Subject Performance")

    data = pd.DataFrame({
        "Subject": ["Math", "Physics", "Chemistry"],
        "Score": [math, physics, chemistry]
    })

    st.bar_chart(data.set_index("Subject"))

    st.subheader("🤖 AI Study Coach")

    weak = min(
        {"Math": math, "Physics": physics, "Chemistry": chemistry},
        key=lambda x: {"Math": math, "Physics": physics, "Chemistry": chemistry}[x]
    )

    st.warning(f"Focus more on {weak}")

    st.subheader("✅ Daily Learning Checklist")

    st.checkbox("Complete today's revision")
    st.checkbox("Solve 20 MCQs")
    st.checkbox("Review mistakes")
    st.checkbox("Study for 2 hours")
