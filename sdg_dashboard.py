import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("🌍 TCS SDG Intelligence Dashboard")

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
    compare_year = st.sidebar.selectbox("Compare With", df["Year"])

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
scores = []
for col in sdg_cols:
    val = df_year[col].iloc[0]
    scores.append(float(val))

sdg_data = pd.DataFrame({
    "SDG": sdg_cols,
    "Score": scores
})

# -------------------------
# KPI CARDS
# -------------------------
st.subheader(f"📊 SDG Overview ({year})")

cols = st.columns(5)

for i, sdg in enumerate(sdg_cols):
    val = scores[i]

    if val >= 80:
        color = "🟢"
    elif val >= 60:
        color = "🟡"
    else:
        color = "🔴"

    cols[i % 5].metric(sdg, f"{val:.1f} {color}")

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

if len(sdg_data) > 0:
    avg_score = sdg_data["Score"].mean()
    best = sdg_data.loc[sdg_data["Score"].idxmax()]
    worst = sdg_data.loc[sdg_data["Score"].idxmin()]

    st.info(f"""
📈 Average SDG Score: {avg_score:.2f}

🏆 Best Performing: {best['SDG']} ({best['Score']:.1f})

⚠️ Needs Improvement: {worst['SDG']} ({worst['Score']:.1f})
""")

# -------------------------
# LINE COMPARISON (OPTIONAL)
# -------------------------
if compare_toggle:

    if year == compare_year:
        st.warning("⚠️ Please select different years")
    else:
        st.subheader(f"📈 Comparison: {year} vs {compare_year}")

        df_compare = df[df["Year"] == compare_year]

        compare_scores = []
        for col in sdg_cols:
            compare_scores.append(float(df_compare[col].iloc[0]))

        compare_df = pd.DataFrame({
            "SDG": sdg_cols,
            str(year): scores,
            str(compare_year): compare_scores
        })

        fig_line = px.line(
            compare_df,
            x="SDG",
            y=[str(year), str(compare_year)],
            markers=True
        )

        st.plotly_chart(fig_line, use_container_width=True)

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