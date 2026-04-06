import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="SDG Dashboard", layout="wide")

st.title("🌍 ESG SDG Dashboard (Auto from Excel)")

# ---------------- LOAD EXCEL ----------------
try:
    df = pd.read_excel("ESG_Audit_TCS.xlsx")
except:
    st.error("Excel file not found!")
    st.stop()

st.subheader("📄 Data Preview")
st.dataframe(df)

# ---------------- HELPER FUNCTIONS ----------------

def level_score(val):
    val = str(val).lower()
    if "low" in val:
        return -3
    elif "medium" in val:
        return 0
    elif "high" in val:
        return 3
    else:
        return 0

def normalize(x):
    return (x / 20) - 2.5

# ---------------- CALCULATE ----------------

all_scores = []

for _, row in df.iterrows():

    scores = [0] * 17

    energy = row.get("Energy", 50)
    renewable = row.get("Renewable", 30)
    water = row.get("Water", 50)
    waste = row.get("Waste", "Medium")
    transport = row.get("Transport", "Car")
    education = row.get("Education", "Medium")
    health = row.get("Health", "Medium")
    equality = row.get("Equality", "Medium")
    income = row.get("Income", "Medium")
    employment = row.get("Employment", "Medium")
    innovation = row.get("Innovation", "Medium")
    governance = row.get("Governance", "Medium")

    # ENVIRONMENT
    scores[6] = normalize(renewable) + normalize(100 - energy)
    scores[5] = normalize(water)
    scores[11] = level_score(waste)
    scores[12] = normalize(100 - energy) + (3 if transport == "Public" else -1)
    scores[13] = level_score(waste) / 2
    scores[14] = level_score(waste) / 2

    # SOCIAL
    scores[0] = level_score(income)
    scores[1] = level_score(income) / 2
    scores[2] = level_score(health)
    scores[3] = level_score(education)
    scores[4] = level_score(equality)
    scores[9] = level_score(equality)
    scores[10] = 2 if transport == "Public" else -1

    # GOVERNANCE
    scores[7] = level_score(employment)
    scores[8] = level_score(innovation)
    scores[15] = level_score(governance)
    scores[16] = (level_score(governance) + level_score(innovation)) / 2

    # Clamp
    scores = [max(-5, min(5, s)) for s in scores]

    all_scores.append(scores)

all_scores = np.array(all_scores)

# ---------------- AVERAGE ----------------

avg_scores = np.mean(all_scores, axis=0)

st.subheader("📊 Average SDG Scores")

cols = st.columns(3)
for i, s in enumerate(avg_scores):
    cols[i % 3].metric(f"SDG {i+1}", round(s, 2))

# ---------------- RADAR ----------------

labels = [f"SDG{i+1}" for i in range(17)]
values = avg_scores.tolist() + [avg_scores[0]]

angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(7,7), subplot_kw=dict(polar=True))
ax.plot(angles, values)
ax.fill(angles, values, alpha=0.25)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)
ax.set_ylim(-5, 5)

st.pyplot(fig)

# ---------------- INDIVIDUAL VIEW ----------------

st.subheader("🔍 Individual Record")

index = st.selectbox("Select Row", df.index)

selected = all_scores[index]

st.write("### Selected SDG Scores")

for i, s in enumerate(selected):
    st.write(f"SDG {i+1}: {round(s,2)}")