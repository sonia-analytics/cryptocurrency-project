import streamlit as st
import pandas as pd
import altair as alt
import os

st.set_page_config(page_title="Crypto Dashboard", layout="wide")
st.title("💹 Cryptocurrency Dashboard")
st.caption("Created by Sonia Mannepuli — Week 5 Visualization Project")

FILE = "crypto_clean.csv"

# --- Load data safely ---
try:
    df = pd.read_csv(FILE)
    # Fix single-column issue where commas are inside one column
    if len(df.columns) == 1:
        df = df[df.columns[0]].str.split(",", expand=True)
        df.columns = ["id","symbol","name","current_price","market_cap",
                      "total_volume","high_24h","low_24h","price_change_pct","fetched_at"]
except Exception as e:
    st.error(f"Error loading {FILE}: {e}")
    st.stop()

# --- Dropdown filter ---
if "name" in df.columns:
    crypto = st.selectbox("Select cryptocurrency:", sorted(df["name"].dropna().unique()))
    data = df[df["name"] == crypto]
else:
    st.error("❌ Missing 'name' column. Please check your CSV.")
    st.stop()

# --- Data preview ---
st.subheader("📊 Data Preview")
st.dataframe(data.head(10))

# --- Summary stats ---
st.subheader("📈 Summary Stats")
st.write(data[["current_price", "market_cap", "total_volume"]].describe())

# --- Chart ---
if "fetched_at" in data.columns:
    data["fetched_at"] = pd.to_datetime(data["fetched_at"], errors="coerce")
    chart = (
        alt.Chart(data)
        .mark_line(point=True)
        .encode(x="fetched_at:T", y="current_price:Q", color=alt.value("skyblue"))
        .properties(title=f"{crypto} Price Trend")
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.warning("No 'fetched_at' column found for trend chart.")

st.markdown("---")
st.write("Data source: CoinGecko API | Visualization by Sonia Mannepuli")
