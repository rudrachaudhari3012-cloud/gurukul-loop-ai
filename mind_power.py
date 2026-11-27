import streamlit as st
import random, json, os, time
from datetime import datetime

# AB SCHOOL LOOP AI - Mind Power Infinite Training
# Games: Word Memory, Color Strategy, Focus Hunter, Decision Matrix, Distraction Shield
# Progress and history are saved locally in mind_power_data.json.

DATA_FILE = "mind_power_data.json"
COLORS = ["Red", "Blue", "Green", "Yellow", "Purple", "Orange"]
SYMBOLS = ["◆", "●", "▲", "■", "★", "✚", "⬟", "⬢"]


def _default_data():
    return {"players": {}}



def load_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and "players" in data:
                return data
    except Exception:
        pass
    return _default_data()



def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False



def get_player(data, student_id):
    sid = str(student_id or "guest").strip() or "guest"
    if sid not in data["players"]:
        data["players"][sid] = {"progress": {}, "history": []}
    player = data["players"][sid]
    player.setdefault("progress", {})
    player.setdefault("history", [])
    return sid, player



def game_level(player, game):
    return int(player["progress"].get(game, {}).get("unlocked_level", 1))



def save_attempt(data, sid, player, game, level, score, total, elapsed, details=None):
    pct = round((score / total) * 100) if total else 0
    passed = pct >= 70
    record = {
        "game": game, "level": level, "score": int(score), "total": int(total),
        "accuracy": pct, "passed": passed, "seconds": round(float(elapsed), 1),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "details": details or {}
    }
    player["history"].append(record)
    prog = player["progress"].setdefault(game, {"unlocked_level": 1, "best_accuracy": 0, "attempts": 0})
    prog["attempts"] = int(prog.get("attempts", 0)) + 1
    prog["best_accuracy"] = max(int(prog.get("best_accuracy", 0)), pct)
    # A level only unlocks after reaching 70% or better. Failed attempts stay at same level.
    if passed:
        prog["unlocked_level"] = max(int(prog.get("unlocked_level", 1)), level + 1)
    save_data(data)
    return record


def reset_game_state(game):
    for key in list(st.session_state.keys()):
        if key.startswith(f"mp_{game}_"):
            del st.session_state[key]


def game_header(game, level, subtitle):
    st.subheader(f"{game} · Level {level}")
    st.caption(subtitle)
    st.progress(min(level / (level + 5), 1.0), text=f"Training difficulty: Level {level} (infinite levels)")


def _result_block(record):
    st.markdown("### Round Result")
    st.metric("Score", f"{record['score']} / {record['total']}")
    st.metric("Accuracy", f"{record['accuracy']}%")
    if record["passed"]:
        st.success(f"Level cleared! Level {record['level'] + 1} is now unlocked.")
    else:
        st.warning(f"Level not cleared. You need at least 70% to unlock Level {record['level'] + 1}. Try this level again.")
    st.caption(f"Time: {record['seconds']} seconds")
    if st.button("Retry / Play Again", key=f"mp_retry_{record['game']}_{record['date']}"):
        reset_game_state(record["game"])
        st.rerun()


def word_memory(data, sid, player, level):
    game = "Word Memory"
    game_header(game, level, "Remember the words, then enter them in the same order.")
    count = min(4 + level, 18)
    words_pool = ["PLANET", "RIVER", "LANTERN", "SILVER", "GARDEN", "ORBIT", "WINDOW", "FOREST", "POCKET", "BRIDGE", "CANDLE", "MIRROR", "CLOUD", "THUNDER", "ANCHOR", "JOURNEY", "COMPASS", "FEATHER", "CRYSTAL", "HORIZON", "BOTTLE", "MOUNTAIN", "NOTEBOOK", "CAMERA"]
    key = f"mp_word_memory_{sid}_{level}"
    if key not in st.session_state:
        st.session_state[key] = random.sample(words_pool, count)
    words = st.session_state[key]
    with st.expander("Show memory words (practice view)", expanded=True):
        st.info("For a real memory round, view the words briefly, then collapse this panel before answering.")
        st.markdown("  •  ".join(words))
    answers = []
    with st.form(f"mp_word_form_{sid}_{level}"):
        st.write("Enter each word in the shown order:")
        for i in range(count):
            answers.append(st.text_input(f"Word {i+1}", key=f"mp_word_answer_{sid}_{level}_{i}").strip().upper())
        submitted = st.form_submit_button("Submit Memory")
    if submitted:
        score = sum(1 for a, b in zip(answers, words) if a == b)
        record = save_attempt(data, sid, player, game, level, score, count, 0, {"sequence": words})
        _result_block(record)


def color_strategy(data, sid, player, level):
    game = "Color Strategy"
    game_header(game, level, "Select the INK COLOR, not the written color word. Complete within 20 seconds.")
    n = min(5 + level, 12)
    statekey = f"mp_color_round_{sid}_{level}"
    if statekey not in st.session_state:
        q = []
        for _ in range(n):
            word = random.choice(COLORS)
            ink = random.choice([c for c in COLORS if c != word])
            q.append({"word": word, "ink": ink})
        st.session_state[statekey] = {"questions": q, "start": time.time(), "submitted": False}
    round_state = st.session_state[statekey]
    remaining = max(0, 20 - int(time.time() - round_state["start"]))
    timer_col, note_col = st.columns([1, 3])
    timer_col.metric("⏱ Time Left", f"{remaining}s")
    note_col.info(f"Questions: {n} · Level: {level} · 70% to pass")
    if remaining <= 0:
        st.warning("Time is up. Submit your answers to save this round.")
    answers = []
    with st.form(f"mp_color_form_{sid}_{level}"):
        for i, q in enumerate(round_state["questions"]):
            st.markdown(f"**Q{i+1}.** <span style='font-size:25px;color:{q['ink'].lower()}'>{q['word']}</span>", unsafe_allow_html=True)
            answers.append(st.selectbox("Choose ink color", ["Select Color"] + COLORS, key=f"mp_color_ans_{sid}_{level}_{i}"))
        submitted = st.form_submit_button("Submit Color Answers")
    if submitted:
        score = sum(1 for a, q in zip(answers, round_state["questions"]) if a == q["ink"])
        elapsed = min(20, time.time() - round_state["start"])
        rec = save_attempt(data, sid, player, game, level, score, n, elapsed, {"timed": True})
        _result_block(rec)
        with st.expander("Answer Review"):
            for i, q in enumerate(round_state["questions"]):
                st.write(f"Q{i+1}: word **{q['word']}** · correct ink color: **{q['ink']}** · your answer: **{answers[i]}**")


def focus_hunter(data, sid, player, level):
    game = "Focus Hunter"
    game_header(game, level, "Find the target symbol and count how many times it appears in the grid.")
    size = min(4 + level // 3, 8)
    total_cells = size * size
    round_key = f"mp_focus_round_{sid}_{level}"
    if round_key not in st.session_state:
        target = random.choice(SYMBOLS)
        grid = [random.choice(SYMBOLS) for _ in range(total_cells)]
        target_count = random.randint(max(1, total_cells // 8), max(2, total_cells // 3))
        positions = random.sample(range(total_cells), target_count)
        for p in positions:
            grid[p] = target
        for i in range(total_cells):
            if i not in positions:
                grid[i] = random.choice([s for s in SYMBOLS if s != target])
        st.session_state[round_key] = {"target": target, "grid": grid, "target_count": target_count}
    round_data = st.session_state[round_key]
    target, grid, target_count = round_data["target"], round_data["grid"], round_data["target_count"]
    st.markdown(f"### Target: **{target}**")
    st.write("Grid:")
    for r in range(size):
        st.markdown("  ".join(grid[r*size:(r+1)*size]))
    with st.form(f"mp_focus_form_{sid}_{level}"):
        choice = st.number_input("How many target symbols?", min_value=0, max_value=total_cells, step=1, key=f"mp_focus_ans_{sid}_{level}")
        submitted = st.form_submit_button("Submit Count")
    if submitted:
        score = 1 if int(choice) == target_count else 0
        rec = save_attempt(data, sid, player, game, level, score, 1, 0, {"target": target, "actual_count": target_count})
        _result_block(rec)
        st.caption(f"Correct count: {target_count}")


def decision_matrix(data, sid, player, level):
    game = "Decision Matrix"
    game_header(game, level, "Choose the most sensible option for each scenario. This is practice, not a personality test.")
    bank = [
        ("You have two assignments due soon. What is the best first step?", ["Start with the task and deadline, then plan time", "Ignore both", "Do whichever is easiest without checking", "Wait until the last minute"], 0),
        ("A group project has a disagreement. What should you do?", ["Listen to each idea and compare evidence", "Interrupt everyone", "Choose randomly", "Leave without discussing"], 0),
        ("A result seems surprising. What is a useful next step?", ["Check the data and repeat the calculation", "Assume it is correct", "Delete the result", "Copy someone else's answer"], 0),
        ("You are stuck on a problem. Which approach is useful?", ["Break it into smaller parts and try a new strategy", "Give up immediately", "Guess repeatedly", "Skip all learning"], 0),
        ("You receive conflicting information. What should you do?", ["Check reliable sources before deciding", "Believe the loudest claim", "Forward it immediately", "Ignore all facts"], 0),
        ("Level challenge: a plan is not working. What is a good response?", ["Review what failed and adjust the plan", "Repeat the same action without checking", "Blame others", "Stop thinking about it"], 0),
    ]
    count = min(3 + level // 4, len(bank))
    decision_key = f"mp_decision_round_{sid}_{level}"
    if decision_key not in st.session_state:
        st.session_state[decision_key] = random.sample(bank, count)
    chosen = st.session_state[decision_key]
    answers = []
    with st.form(f"mp_decision_form_{sid}_{level}"):
        for i, (question, options, correct) in enumerate(chosen):
            st.markdown(f"**Q{i+1}. {question}**")
            answers.append(st.radio("Select an option", options, key=f"mp_dec_ans_{sid}_{level}_{i}"))
        submitted = st.form_submit_button("Submit Decisions")
    if submitted:
        score = sum(1 for a, (_, options, correct) in zip(answers, chosen) if options.index(a) == correct)
        rec = save_attempt(data, sid, player, game, level, score, count, 0)
        _result_block(rec)
        with st.expander("Decision review"):
            for i, (q, options, correct) in enumerate(chosen):
                st.write(f"Q{i+1}: {q}")
                st.write(f"Best answer: {options[correct]}")


def distraction_shield(data, sid, player, level):
    game = "Distraction Shield"
    game_header(game, level, "Select only the requested target symbols. Avoid distractors.")
    count = min(12 + level * 2, 60)
    shield_key = f"mp_shield_round_{sid}_{level}"
    if shield_key not in st.session_state:
        target = random.choice(SYMBOLS)
        distractors = [s for s in SYMBOLS if s != target]
        sequence = [target if random.random() < 0.30 else random.choice(distractors) for _ in range(count)]
        correct_indices = [i for i, s in enumerate(sequence) if s == target]
        st.session_state[shield_key] = {"target": target, "sequence": sequence, "correct_indices": correct_indices}
    round_data = st.session_state[shield_key]
    target, sequence, correct_indices = round_data["target"], round_data["sequence"], round_data["correct_indices"]
    st.write(f"### Select every **{target}** and nothing else.")
    selected = []
    with st.form(f"mp_shield_form_{sid}_{level}"):
        cols = st.columns(6)
        for i, symbol in enumerate(sequence):
            with cols[i % 6]:
                selected.append(st.checkbox(symbol, key=f"mp_shield_pick_{sid}_{level}_{i}"))
        submitted = st.form_submit_button("Submit Selection")
    if submitted:
        chosen_indices = [i for i, val in enumerate(selected) if val]
        correct = len(set(chosen_indices) & set(correct_indices))
        false_picks = len(set(chosen_indices) - set(correct_indices))
        missed = len(set(correct_indices) - set(chosen_indices))
        score = max(0, len(correct_indices) - false_picks - missed)
        total = max(1, len(correct_indices))
        score = min(total, score)
        rec = save_attempt(data, sid, player, game, level, score, total, 0, {"target": target, "false_picks": false_picks, "missed": missed})
        _result_block(rec)
        st.write(f"Correct selections: {correct} · Missed: {missed} · Extra selections: {false_picks}")


def mind_booster_report(player):
    history = player.get("history", [])
    st.header("🧠 Mind Booster Report")
    if not history:
        st.info("Complete at least one game to see your training report.")
        return
    today = datetime.now().strftime("%Y-%m-%d")
    today_records = [r for r in history if str(r.get("date", "")).startswith(today)]
    st.caption("This report summarizes game practice performance. It is not an IQ or medical assessment.")
    total_games = len(today_records)
    avg = round(sum(r.get("accuracy", 0) for r in today_records) / total_games) if total_games else 0
    passed = sum(1 for r in today_records if r.get("passed"))
    c1, c2, c3 = st.columns(3)
    c1.metric("Games today", total_games)
    c2.metric("Average accuracy", f"{avg}%" if total_games else "—")
    c3.metric("Levels cleared today", passed)
    if today_records:
        best = max(today_records, key=lambda r: r.get("accuracy", 0))
        st.success(f"Today's best performance: {best['game']} · Level {best['level']} · {best['accuracy']}%")
        by_game = {}
        for r in today_records:
            by_game.setdefault(r["game"], []).append(r["accuracy"])
        st.subheader("Skill practice summary")
        for game, scores in by_game.items():
            st.write(f"**{game}** — {round(sum(scores)/len(scores))}% average accuracy across {len(scores)} attempt(s)")
        if len(today_records) >= 2:
            first = today_records[0]["accuracy"]
            last = today_records[-1]["accuracy"]
            delta = last - first
            st.write(f"Within today's sessions, accuracy changed by **{delta:+d} percentage points** from first to last recorded attempt.")
        st.info("Training takeaway: keep practicing steadily. A higher game score reflects better performance on these activities, not a measured increase in IQ or brain capacity.")
    st.subheader("Recent history")
    st.dataframe([{"Date": r.get("date"), "Game": r.get("game"), "Level": r.get("level"), "Score": f"{r.get('score')}/{r.get('total')}", "Accuracy": f"{r.get('accuracy')}%", "Passed": "Yes" if r.get("passed") else "No"} for r in history[-30:][::-1]], use_container_width=True, hide_index=True)


def render_mind_power(st_obj=None, student_id=None):
    # Compatible with calls from the main app that pass no student ID.
    data = load_data()
    sid, player = get_player(data, student_id or st.session_state.get("student_id") or st.session_state.get("user_id") or "guest")
    st.title("🧠 Mind Power")
    st.markdown("### Train your focus, memory, reasoning, and attention with progressive challenges.")
    st.caption(f"Progress is saved locally for student ID: {sid}. Each game has independent infinite levels; 70% accuracy clears a level.")
    games = ["Word Memory", "Color Strategy", "Focus Hunter", "Decision Matrix", "Distraction Shield", "Mind Booster Report"]
    selected = st.selectbox("Choose a training game", games, key="mp_game_selector")
    if selected == "Mind Booster Report":
        mind_booster_report(player)
    else:
        level = game_level(player, selected)
        st.metric("Current unlocked level", level)
        if selected == "Word Memory":
            word_memory(data, sid, player, level)
        elif selected == "Color Strategy":
            color_strategy(data, sid, player, level)
        elif selected == "Focus Hunter":
            focus_hunter(data, sid, player, level)
        elif selected == "Decision Matrix":
            decision_matrix(data, sid, player, level)
        elif selected == "Distraction Shield":
            distraction_shield(data, sid, player, level)
    st.divider()
    st.subheader("Level Progress")
    for g in games[:-1]:
        p = player["progress"].get(g, {})
        st.write(f"**{g}** · Unlocked level: {p.get('unlocked_level', 1)} · Best accuracy: {p.get('best_accuracy', 0)}% · Attempts: {p.get('attempts', 0)}")
