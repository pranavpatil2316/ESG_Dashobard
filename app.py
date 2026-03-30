import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="SDG Dashboard", layout="wide")

st.title("🌍 ESG-Based SDG Dashboard")

st.write("Fill inputs to generate SDG Scores (-5 to +5)")

# ---------------- INPUTS ----------------

st.sidebar.header("User Inputs")

energy = st.sidebar.number_input("Energy Consumption (0-100)", 0, 100, 50)
renewable = st.sidebar.number_input("Renewable Energy % (0-100)", 0, 100, 30)
water = st.sidebar.number_input("Water Conservation % (0-100)", 0, 100, 50)

waste = st.sidebar.selectbox("Waste Management", ["Low", "Medium", "High"])
transport = st.sidebar.selectbox("Transport Mode", ["Car", "Bike", "Public"])
education = st.sidebar.selectbox("Education Level", ["Low", "Medium", "High"])
health = st.sidebar.selectbox("Healthcare Access", ["Low", "Medium", "High"])
equality = st.sidebar.selectbox("Gender Equality", ["Low", "Medium", "High"])
income = st.sidebar.selectbox("Income Level", ["Low", "Medium", "High"])
employment = st.sidebar.selectbox("Employment Quality", ["Low", "Medium", "High"])
innovation = st.sidebar.selectbox("Technology Usage", ["Low", "Medium", "High"])
governance = st.sidebar.selectbox("Governance Transparency", ["Low", "Medium", "High"])

# ---------------- HELPER FUNCTIONS ----------------

def level_score(val):
    return {"Low": -3, "Medium": 0, "High": 3}[val]

def normalize_100(x):
    return (x / 20) - 2.5  # maps 0–100 → -2.5 to +2.5

# ---------------- CALCULATION ----------------

def calculate_scores():
    scores = [0] * 17

    # Environmental SDGs
    scores[6] = normalize_100(renewable) + normalize_100(100 - energy)   # SDG7
    scores[5] = normalize_100(water)                                     # SDG6
    scores[11] = level_score(waste)                                      # SDG12
    scores[12] = normalize_100(100 - energy) + (3 if transport == "Public" else -1)  # SDG13
    scores[14] = level_score(waste) / 2                                   # SDG15
    scores[13] = level_score(waste) / 2                                   # SDG14

    # Social SDGs
    scores[0] = level_score(income)                                       # SDG1
    scores[1] = level_score(income) / 2                                   # SDG2
    scores[2] = level_score(health)                                       # SDG3
    scores[3] = level_score(education)                                    # SDG4
    scores[4] = level_score(equality)                                     # SDG5
    scores[9] = level_score(equality)                                     # SDG10
    scores[10] = 2 if transport == "Public" else -1                       # SDG11

    # Governance / Economic SDGs
    scores[7] = level_score(employment)                                   # SDG8
    scores[8] = level_score(innovation)                                   # SDG9
    scores[15] = level_score(governance)                                  # SDG16
    scores[16] = (level_score(governance) + level_score(innovation)) / 2  # SDG17

    # Clamp values (-5 to +5)
    scores = [max(-5, min(5, s)) for s in scores]

    return scores

# ---------------- BUTTON ----------------

if st.button("Generate Dashboard"):

    scores = calculate_scores()

    # ----------- DISPLAY SCORES -----------
    st.subheader("📊 SDG Scores")

    col1, col2, col3 = st.columns(3)

    for i in range(17):
        if i < 6:
            col1.metric(f"SDG {i+1}", round(scores[i], 2))
        elif i < 12:
            col2.metric(f"SDG {i+1}", round(scores[i], 2))
        else:
            col3.metric(f"SDG {i+1}", round(scores[i], 2))

    # ----------- RADAR CHART -----------
    labels = [f"SDG{i+1}" for i in range(17)]
    values = scores + [scores[0]]

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7,7), subplot_kw=dict(polar=True))

    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    ax.set_ylim(-5, 5)
    ax.set_title("🌍 SDG Performance Radar")

    st.pyplot(fig)

    # ----------- SUMMARY -----------
    st.subheader("📌 Summary")

    best_idx = scores.index(max(scores))
    worst_idx = scores.index(min(scores))

    st.success(f"Best: SDG {best_idx+1} → {round(max(scores),2)}")
    st.error(f"Worst: SDG {worst_idx+1} → {round(min(scores),2)}")

    # ----------- SUGGESTIONS -----------
    st.subheader("💡 Suggestions")

    if scores[6] < 0:
        st.write("Increase renewable energy usage (SDG 7)")
    if scores[11] < 0:
        st.write("Improve waste management (SDG 12)")
    if scores[4] < 0:
        st.write("Improve gender equality (SDG 5)")
    if scores[12] < 0:
        st.write("Reduce carbon footprint (SDG 13)")