import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("🌍 TCS SDG Intelligence Dashboard")

st.write("")
st.markdown("""
<div style="
position: absolute;
top: 15px;
right: 25px;
background-color: rgba(255,255,255,0.9);
padding: 8px 12px;
border-radius: 10px;
box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
text-align: right;
font-size: 13px;
">
<b>Pranav Patil</b> - 22108A0038<br>
<b>Ayush Agrawal</b> - 22108A0068
</div>
""", unsafe_allow_html=True)

# -------------------------
# SDG NAMES
# -------------------------
sdg_names = {
    "SDG1": "No Poverty",
    "SDG2": "Zero Hunger",
    "SDG3": "Good Health",
    "SDG4": "Quality Education",
    "SDG5": "Gender Equality",
    "SDG6": "Clean Water",
    "SDG7": "Clean Energy",
    "SDG8": "Decent Work",
    "SDG9": "Industry & Innovation",
    "SDG10": "Reduced Inequality",
    "SDG11": "Sustainable Cities",
    "SDG12": "Responsible Consumption",
    "SDG13": "Climate Action",
    "SDG14": "Life Below Water",
    "SDG15": "Life on Land",
    "SDG16": "Strong Institutions",
    "SDG17": "Partnerships"
}

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_excel("tcs_sdg_full.xlsx")
df = df.reset_index(drop=True)

# -------------------------
# ESG → SDG CONVERSION
# -------------------------
df["SDG1"] = df["Employee_Training_Hours"] * 0.8
df["SDG2"] = df["Waste_Recycled_%"] * 0.9
df["SDG3"] = df["Employee_Training_Hours"]
df["SDG4"] = df["Employee_Training_Hours"] * 1.1
df["SDG5"] = df["Women_Workforce_%"]
df["SDG6"] = df["Water_Usage_Reduction_%"]
df["SDG7"] = df["Renewable_Energy_%"]
df["SDG8"] = df["Employee_Training_Hours"]
df["SDG9"] = df["Renewable_Energy_%"] * 0.8
df["SDG10"] = df["Women_Workforce_%"] * 0.9
df["SDG11"] = df["Waste_Recycled_%"]
df["SDG12"] = df["Waste_Recycled_%"]
df["SDG13"] = df["Carbon_Emissions_Reduction_%"]
df["SDG14"] = df["Water_Usage_Reduction_%"] * 0.8
df["SDG15"] = df["Waste_Recycled_%"] * 0.7
df["SDG16"] = df["Governance_Score"]
df["SDG17"] = (df["Governance_Score"] + df["Employee_Training_Hours"]) / 2

# -------------------------
# SDG COLUMNS
# -------------------------
sdg_cols = [col for col in df.columns if col.startswith("SDG")]

if len(sdg_cols) == 0:
    st.error("❌ SDG columns not found")
    st.stop()

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.header("🔎 Controls")

year = st.sidebar.selectbox("Select Year", df["Year"])

compare_toggle = st.sidebar.checkbox("Enable Comparison")

if compare_toggle:
    compare_years = st.sidebar.multiselect(
        "Select Years to Compare",
        df["Year"].tolist(),
        default=[year]
    )
    compare_years = sorted(compare_years)

# -------------------------
# FILTER DATA
# -------------------------
df_year = df[df["Year"] == year]

if df_year.empty:
    st.error("❌ No data for selected year")
    st.stop()

# -------------------------
# EXTRACT SCORES
# -------------------------
scores = [float(df_year[col].iloc[0]) for col in sdg_cols]

sdg_labels = [f"{sdg} - {sdg_names.get(sdg, '')}" for sdg in sdg_cols]

sdg_data = pd.DataFrame({
    "SDG": sdg_labels,
    "Score": scores
})

# -------------------------
# SDG OVERVIEW + LEGEND
# -------------------------
st.subheader(f"📊 SDG Overview ({year})")

st.markdown("""
<div style="background-color:#ffffff; padding:15px; border-radius:12px; 
box-shadow:0px 2px 8px rgba(0,0,0,0.1); color:black">

<h4>📌 SDG Score Interpretation</h4>

🔴 <b>0–40</b> → Poor performance<br>
🟡 <b>40–70</b> → Moderate performance<br>
🟢 <b>70–100</b> → Strong performance

</div>
""", unsafe_allow_html=True)

# -------------------------
# KPI CARDS
# -------------------------
cols = st.columns(5)

for i, sdg in enumerate(sdg_cols):
    val = scores[i]

    if val >= 70:
        color = "🟢"
    elif val >= 40:
        color = "🟡"
    else:
        color = "🔴"

    cols[i % 5].metric(
        f"{sdg} - {sdg_names.get(sdg, '')}",
        f"{val:.1f} {color}"
    )

# -------------------------
# BAR GRAPH
# -------------------------
st.subheader("📊 SDG Performance")

fig = px.bar(
    sdg_data,
    x="SDG",
    y="Score",
    text="Score"
)

fig.update_traces(textposition="outside")
fig.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# RADAR GRAPH
# -------------------------
st.subheader("🕸 SDG Radar Analysis")

fig_radar = px.line_polar(
    sdg_data,
    r="Score",
    theta="SDG",
    line_close=True
)

st.plotly_chart(fig_radar, use_container_width=True)

# -------------------------
# INSIGHTS
# -------------------------
st.subheader("🧠 Insights")

avg_score = sdg_data["Score"].mean()
best = sdg_data.loc[sdg_data["Score"].idxmax()]
worst = sdg_data.loc[sdg_data["Score"].idxmin()]

st.info(f"""
📈 Average SDG Score: {avg_score:.2f}

🏆 Best Performing: {best['SDG']} ({best['Score']:.1f})

⚠️ Needs Improvement: {worst['SDG']} ({worst['Score']:.1f})
""")

# -------------------------
# MULTI-YEAR COMPARISON
# -------------------------
if compare_toggle:

    if len(compare_years) < 2:
        st.warning("⚠️ Select at least 2 years")
    else:
        st.subheader("📈 Multi-Year Comparison")

        compare_df = pd.DataFrame({
            "SDG": sdg_labels
        })

        for y in compare_years:
            temp = df[df["Year"] == y]

            temp_scores = []
            for col in sdg_cols:
                try:
                    temp_scores.append(float(temp[col].iloc[0]))
                except:
                    temp_scores.append(0)

            compare_df[str(y)] = temp_scores

        fig_multi = px.line(
            compare_df,
            x="SDG",
            y=[str(y) for y in compare_years],
            markers=True
        )

        st.plotly_chart(fig_multi, use_container_width=True)

# -------------------------
# TREND GRAPH
# -------------------------
st.subheader("📈 SDG Trends Over Time")

fig_trend = px.line(
    df,
    x="Year",
    y=sdg_cols,
    markers=True
)

st.plotly_chart(fig_trend, use_container_width=True)

# -------------------------
# DATA TABLE
# -------------------------
st.subheader("📄 Data Table")
st.dataframe(df)