import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="SDG Dashboard", layout="wide")

st.title("🌍 ESG SDG Dashboard")

# ---------------- LOAD EXCEL ----------------
FILE_NAME = "ESG_Audit_TCS.xlsx"

try:
    df = pd.read_excel(ESG_Audit_TCS.xlsx)
except:
    st.error(f"❌ File '{FILE_NAME}' not found in repo")
    st.stop()

st.subheader("📄 Dataset Preview")
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
    try:
        return (float(x) / 20) - 2.5
    except:
        return 0

# ---------------- CALCULATION ----------------

all_scores = []

for _, row in df.iterrows():

    scores = [0] * 17

    # Safe extraction (auto-handle missing columns)
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

    # -------- ENVIRONMENT --------
    scores[6] = normalize(renewable)*2 + normalize(100-energy)
    scores[5] = normalize(water)
    scores[11] = level_score(waste)
    scores[12] = normalize(100-energy) + (3 if str(transport).lower()=="public" else -1)
    scores[13] = level_score(waste) / 2
    scores[14] = level_score(waste) / 2

    # -------- SOCIAL --------
    scores[0] = level_score(income)
    scores[1] = level_score(income) / 2
    scores[2] = level_score(health)
    scores[3] = level_score(education)
    scores[4] = level_score(equality)
    scores[9] = level_score(equality)
    scores[10] = 2 if str(transport).lower()=="public" else -1

    # -------- GOVERNANCE --------
    scores[7] = level_score(employment)
    scores[8] = level_score(innovation)
    scores[15] = level_score(governance)
    scores[16] = (level_score(governance) + level_score(innovation)) / 2

    # -------- CROSS-IMPACT (IMPORTANT 🔥) --------
    # Spread impact so no SDG stays zero
    scores[6] += scores[11] * 0.3   # waste affects environment
    scores[12] += scores[6] * 0.2   # energy affects climate
    scores[3] += scores[2] * 0.2    # health affects education
    scores[8] += scores[7] * 0.3    # jobs affect innovation

    # Clamp (-5 to +5)
    scores = [max(-5, min(5, s)) for s in scores]

    all_scores.append(scores)

all_scores = np.array(all_scores)

# ---------------- ESG SCORES ----------------

env_indices = [5,6,11,12,13,14]
soc_indices = [0,1,2,3,4,9,10]
gov_indices = [7,8,15,16]

env_score = np.mean(all_scores[:, env_indices])
soc_score = np.mean(all_scores[:, soc_indices])
gov_score = np.mean(all_scores[:, gov_indices])

# ---------------- AVERAGE SDG ----------------

avg_scores = np.mean(all_scores, axis=0)

st.subheader("📊 ESG Summary")

col1, col2, col3 = st.columns(3)
col1.metric("🌱 Environmental", round(env_score,2))
col2.metric("👥 Social", round(soc_score,2))
col3.metric("🏛 Governance", round(gov_score,2))

# ---------------- SDG GRID ----------------

st.subheader("📊 SDG Scores")

cols = st.columns(3)
for i, s in enumerate(avg_scores):
    cols[i % 3].metric(f"SDG {i+1}", round(s, 2))

# ---------------- RADAR CHART ----------------

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
ax.set_title("🌍 SDG Performance Radar")

st.pyplot(fig)

# ---------------- INDIVIDUAL VIEW ----------------

st.subheader("🔍 Analyze Individual Entry")

index = st.selectbox("Select Row", df.index)

selected_scores = all_scores[index]

for i, s in enumerate(selected_scores):
    st.write(f"SDG {i+1}: {round(s,2)}")

# ---------------- INSIGHTS ----------------

st.subheader("💡 Insights")

best = np.argmax(avg_scores)
worst = np.argmin(avg_scores)

st.success(f"Best Performing: SDG {best+1}")
st.error(f"Needs Improvement: SDG {worst+1}")

if avg_scores[11] < 0:
    st.write("➡ Improve waste management practices")
if avg_scores[6] < 0:
    st.write("➡ Increase renewable energy adoption")
if avg_scores[4] < 0:
    st.write("➡ Improve gender equality initiatives")