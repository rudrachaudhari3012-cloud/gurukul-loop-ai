
# =====================================================
# PREMIUM HOME DASHBOARD
# FUTURE LEARNING HUB
# =====================================================

if page == T["overview"]:

    st.markdown("""
    <style>
    .home-hero {
        background:
        radial-gradient(circle at 15% 50%,
        rgba(36,194,255,.30),transparent 30%),
        linear-gradient(105deg,#d9eaff,#e9e7ff 55%,#ffe8ef);
        border:1px solid #cbdcff;
        border-radius:22px;
        padding:28px;
        min-height:205px;
        box-shadow:0 10px 30px rgba(70,100,180,.13);
        position:relative;
        overflow:hidden;
    }

    .home-hero h1 {
        color:#101b42;
        font-size:clamp(25px,3vw,38px);
        font-weight:850;
        margin:12px 0 5px;
    }

    .home-hero p {
        color:#344777;
        font-size:16px;
        margin:5px 0;
    }

    .hero-label {
        display:inline-block;
        background:rgba(255,255,255,.72);
        color:#7544db;
        padding:7px 15px;
        border-radius:30px;
        font-weight:800;
        font-size:13px;
    }

    .hero-art {
        position:absolute;
        right:25px;
        top:25px;
        font-size:95px;
        filter:drop-shadow(0 8px 12px rgba(80,80,200,.2));
    }

    .home-section {
        color:#101b42;
        font-size:21px;
        font-weight:800;
        margin:8px 0 13px;
    }

    .quick-card {
        padding:17px 12px;
        border-radius:17px;
        min-height:105px;
        border:1px solid rgba(120,140,200,.18);
        transition:all .2s ease;
    }

    .quick-card:hover {
        transform:translateY(-3px);
        box-shadow:0 8px 20px rgba(90,100,180,.15);
    }

    .quick-icon {
        font-size:30px;
        margin-bottom:8px;
    }

    .quick-title {
        color:#15234d;
        font-weight:800;
        font-size:15px;
    }

    .quick-sub {
        color:#53668d;
        font-size:12px;
    }

    .focus-item {
        background:linear-gradient(100deg,#f0edff,#edf3ff);
        border-radius:12px;
        padding:10px 13px;
        margin:8px 0;
        color:#18264d;
        border:1px solid #e4e8ff;
    }

    .remember-card {
        background:linear-gradient(120deg,#fff0d8,#ffe7ed);
        border:1px solid #ffe3c1;
        border-radius:18px;
        padding:20px;
        min-height:120px;
    }

    .remember-card h3 {
        color:#17264d;
        font-size:18px;
    }

    .remember-card p {
        color:#273a69;
        font-size:17px;
        font-weight:700;
    }
    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------
    # HERO BANNER
    # -------------------------------------------------

    st.markdown(f"""
    <div class="home-hero">
        <div class="hero-label">
            🎓 WELCOME BACK, {user['full_name'].upper()}!
        </div>
        <h1>AB SCHOOL LOOP AI</h1>
        <h2 style="
            color:#3978ee;
            font-size:25px;
            font-weight:850;
            margin:5px 0;">
            Learn &nbsp; • &nbsp;
            <span style="color:#08a9d9;">Grow</span>
            &nbsp; • &nbsp;
            <span style="color:#9250ed;">Thrive</span>
        </h2>
        <p>Your Smart Learning Partner for a Brighter Future ✨</p>
        <p style="font-size:13px;">
            STUDENT GROWTH · SMART LEARNING · MIND POWER
        </p>
        <div class="hero-art">🧠 ✨</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # -------------------------------------------------
    # DASHBOARD METRICS
    # -------------------------------------------------

    total_attempts = len(results)

    total_correct = sum(
        r["score"] for r in results
    )

    total_questions = sum(
        r["total"] for r in results
    )

    learning_score = (
        round(total_correct / total_questions * 100)
        if total_questions else 0
    )

    brain_energy = user.get("energy") or "Ready"

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "🎯 Learning Score",
            f"{learning_score}%" if results else "—"
        )

    with m2:
        st.metric(
            "⚡ Brain Energy",
            brain_energy
        )

    with m3:
        st.metric(
            "🏆 Quiz Attempts",
            total_attempts
        )

    with m4:
        st.metric(
            "⭐ Growth Points",
            total_attempts * 10
        )

    st.write("")

    # -------------------------------------------------
    # PROGRESS GRAPH
    # -------------------------------------------------

    left, right = st.columns([1.08, 1])

    with left:

        with st.container(border=True):

            st.markdown(
                '<div class="home-section">'
                '📊 Your Learning Progress'
                '</div>',
                unsafe_allow_html=True
            )

            if results:

                graph_data = list(reversed(results))

                graph_df = pd.DataFrame({
                    "Attempt": [
                        f"Test {i+1}"
                        for i in range(len(graph_data))
                    ],
                    "Score": [
                        round(
                            r["score"] /
                            max(r["total"], 1) * 100
                        )
                        for r in graph_data
                    ]
                })

                fig = px.area(
                    graph_df,
                    x="Attempt",
                    y="Score",
                    range_y=[0, 100],
                    markers=True
                )

                fig.update_traces(
                    line=dict(
                        color="#438cf7",
                        width=3
                    ),
                    fillcolor="rgba(67,140,247,.20)",
                    marker=dict(
                        color="#9250ed",
                        size=8
                    )
                )

                fig.update_layout(
                    height=280,
                    showlegend=False,
                    yaxis_title="Score (%)",
                    xaxis_title="",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=5,r=10,t=20,b=5),
                    font=dict(color="#24345f"),
                    yaxis=dict(
                        range=[0,100],
                        gridcolor="#e3eafa"
                    ),
                    xaxis=dict(
                        gridcolor="#e3eafa"
                    )
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:

                st.info(
                    "Complete your first quiz to see "
                    "your learning progress here."
                )

    # -------------------------------------------------
    # TODAY'S FOCUS
    # -------------------------------------------------

    with right:

        with st.container(border=True):

            st.markdown(
                '<div class="home-section">'
                '💡 Today’s Focus'
                '</div>',
                unsafe_allow_html=True
            )

            focus_tasks = [
                "Revise one difficult subject",
                "Attempt 10 practice questions",
                "Complete one Mind Power activity",
                "Stay positive and focused"
            ]

            for i, task in enumerate(focus_tasks):

                st.markdown(
                    '<div class="focus-item">'
                    '✨ &nbsp; ' + task +
                    '</div>',
                    unsafe_allow_html=True
                )

            st.caption(
                "Small steps every day create progress."
            )

    st.write("")

    # -------------------------------------------------
    # QUICK ACCESS
    # -------------------------------------------------

    st.markdown(
        '<div class="home-section">'
        '🚀 Quick Access'
        '</div>',
        unsafe_allow_html=True
    )

    q1, q2, q3, q4 = st.columns(4)

    quick_items = [
        (
            q1, "🧠", "Mind Power",
            "Brain Games & Focus", "#eee0ff"
        ),
        (
            q2, "🧩", "AI Quiz",
            "Practice & Test", "#d7f7e6"
        ),
        (
            q3, "😊", "AI Coach",
            "Get Guidance", "#ffefd8"
        ),
        (
            q4, "📊", "Analytics",
            "Track Progress", "#d9f5fb"
        )
    ]

    for col, icon, title, subtitle, color in quick_items:

        with col:

            with st.container(border=True):

                st.markdown(
                    f"""
                    <div class="quick-card"
                         style="background:{color};">
                        <div class="quick-icon">{icon}</div>
                        <div class="quick-title">{title}</div>
                        <div class="quick-sub">{subtitle}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.write("")

    # -------------------------------------------------
    # BOTTOM REMEMBER SECTION
    # -------------------------------------------------

    r1, r2 = st.columns([2.5, 1])

    with r1:

        with st.container(border=True):

            st.markdown(
                "### 🌟 Your Growth Journey"
            )

            st.write(
                "Learn something new. Practise consistently. "
                "Reflect on your progress. Keep improving."
            )

            st.progress(
                min(learning_score / 100, 1.0)
            )

            st.caption(
                f"Your current quiz accuracy: "
                f"{learning_score}%"
                if results else
                "Your progress will appear after your first quiz."
            )

    with r2:

        st.markdown("""
        <div class="remember-card">
            <h3>⭐ Remember</h3>
            <p>Dream Big.<br>Study Smart!</p>
            <div style="
                text-align:right;
                font-size:25px;
                color:#7654e8;">
                ♡
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        AB SCHOOL LOOP AI · FUTURE LEARNING HUB<br>
        LEARN → GROW → THRIVE
    </div>
    """, unsafe_allow_html=True)
