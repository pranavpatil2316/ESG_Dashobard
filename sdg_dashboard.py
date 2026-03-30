import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="SDG Dashboard", layout="centered")

st.title("🌍 SDG ESG Dashboard")

st.write("Enter your details below:")

# ---------------- INPUTS ----------------

renewable = st.slider("Renewable Energy (%)", 0, 100, 50)

waste = st.selectbox("Waste Management", ["Low", "Medium", "High"])

transport = st.selectbox("Transport Type", ["Car", "Public"])

equality = st.selectbox("Gender Equality Level", ["Low", "Medium", "High"])

water = st.slider("Water Conservation (%)", 0, 100, 50)

# ---------------- SCORING ----------------

def get_score(level):
    if level == "Low":
        return -3
    elif level == "Medium":
        return 0
    else:
        return 3

def calculate_scores():
    scores = [0] * 17

    # SDG 7 - Energy
    scores[6] = (renewable / 20) - 2.5

    # SDG 12 - Waste
    scores[11] = get_score(waste)

    # SDG 11 & 13 - Transport
    if transport == "Public":
        scores[10] = 3
        scores[12] = 3
    else:
        scores[10] = -2
        scores[12] = -2

    # SDG 5 & 10 - Equality
    eq_score = get_score(equality)
    scores[4] = eq_score
    scores[9] = eq_score

    # SDG 6 - Water
    scores[5] = (water / 20) - 2.5

    # Clamp (-5 to +5)
    scores = [max(-5, min(5, s)) for s in scores]

    return scores

# ---------------- BUTTON ----------------

if st.button("Generate SDG Dashboard"):

    scores = calculate_scores()

    st.subheader("📊 SDG Scores (-5 to +5)")

    for i, s in enumerate(scores):
        st.write(f"SDG {i+1}: {round(s,2)}")

    # ---------------- RADAR GRAPH ----------------

    labels = [f"SDG{i+1}" for i in range(17)]
    values = scores + [scores[0]]

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))

    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    ax.set_ylim(-5, 5)
    ax.set_title("SDG Performance")

    st.pyplot(fig)

    # ---------------- SUMMARY ----------------

    st.subheader("📌 Summary")

    st.write("Best Score:", round(max(scores),2))
    st.write("Worst Score:", round(min(scores),2))

    # ---------------- SUGGESTIONS ----------------

    st.subheader("💡 Suggestions")

    if scores[11] < 0:
        st.write("Improve waste management (SDG 12)")
    if scores[6] < 0:
        st.write("Increase renewable energy usage (SDG 7)")
    if scores[4] < 0:
        st.write("Improve gender equality (SDG 5)")