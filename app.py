import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scoring.scorer import calculate_score

# ----------------------------
# Streamlit page configuration
# ----------------------------
st.set_page_config(page_title="AI Lead Scoring Demo", layout="wide")
st.title("3D In-Vitro Lead Scoring Dashboard")

# ----------------------------
# Load CSV
# ----------------------------
df = pd.read_csv("data/leads.csv")

# Normalize column names
df.columns = (
    df.columns
      .str.strip()           
      .str.lower()           
      .str.replace(" ", "_") 
      .str.replace("?", "")  
)

st.subheader("Columns after normalization")
st.write(df.columns.tolist())

st.subheader("Sample Leads")
st.dataframe(df.head())

# ----------------------------
# Calculate Probability Score
# ----------------------------
df["probability_score"] = df.apply(calculate_score, axis=1)

# Sort by score descending
df = df.sort_values("probability_score", ascending=False)

# ----------------------------
# Visualize Distribution
# ----------------------------
st.subheader("Probability Score Distribution")
fig, ax = plt.subplots(figsize=(10, 4))
ax.hist(df["probability_score"], bins=20, color='skyblue', edgecolor='black')
ax.set_xlabel("Probability Score")
ax.set_ylabel("Number of Leads")
ax.set_title("Histogram of Probability Scores")
st.pyplot(fig)

# ----------------------------
# Ranked Leads Table
# ----------------------------
st.subheader("Ranked Leads")
st.dataframe(df, use_container_width=True)

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("Filters")

min_score = st.sidebar.slider("Minimum Score", 0, 100, 50)
filter_location = st.sidebar.text_input("Filter by Location (leave empty to ignore)")

filtered_df = df[df["probability_score"] >= min_score]

if filter_location:
    filtered_df = filtered_df[filtered_df["location"].str.contains(filter_location, case=False)]

st.subheader("Filtered Results")
st.dataframe(filtered_df, use_container_width=True)

# ----------------------------
# Export filtered CSV
# ----------------------------
st.download_button(
    label="Download Filtered CSV",
    data=filtered_df.to_csv(index=False),
    file_name="ranked_leads.csv",
    mime="text/csv"
)
