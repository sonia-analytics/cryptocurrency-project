import streamlit as st
import pandas as pd
import altair as alt
import os

st.set_page_config(page_title="Crypto Dashboard", layout="wide")
st.title("Cryptocurrency Dashboard")
st.write("Created by Sonia Mannepuli — Week 5 Visualization Project")

FILE_PATH = "crypto_clean.csv"

if not os.path.exists(FILE_PATH):
    st.error("CSV file not found. Upload or check the path.")
    st.stop()

# --- Load CSV properly ---
try:
    df = pd.read_csv(FILE_PATH)
    if len(df.columns) == 1:
        df = pd.read_csv(FILE_PATH, sep=",")  # ensure proper delimiter
except Exception as e:
    st.error(f"Error reading CSV: {e}")
    st.stop()

# --- Confirm columns ---
if not any(col in df.columns for col in ["name", "id", "symbol"]):
    st.error(f"No column found for crypto identifier ('name', 'id', 'symbol'). Available columns: {list(df.columns)}")
    st.stop()

# --- Dropdown Filter ---
crypto_col = "name" if "name" in df.columns else ("id" if "id" in df.columns else "symbol")
cryptos = sorted(df[crypto_col].dropna().unique())
selected_crypto = st.selectbox("Choose a cryptocurrency:", cryptos)

# --- Filtered Data ---
data = df[df[crypto_col] == selected_crypto]

# --- Summary Statistics ---
st.subheader("📊 Summary Statistics")
st.write(data[["current_price", "market_cap", "total_volume"]].describe())

# --- Charts ---
st.subheader("📈 Price Trend (with Moving Average)")
if "fetched_at" in data.columns:
    data["fetched_at"] = pd.to_datetime(data["fetched_at"], errors="coerce")
    data = data.sort_values("fetched_at")
    data["MA_5"] = data["current_price"].rolling(5).mean()

    price_chart = (
        alt.Chart(data)
        .mark_line(point=True)
        .encode(x="fetched_at:T", y="current_price:Q", color=alt.value("skyblue"))
        .properties(title=f"{selected_crypto} - Price Trend")
    )
    ma_chart = alt.Chart(data).mark_line(color="orange").encode(x="fetched_at:T", y="MA_5:Q")
    st.altair_chart(price_chart + ma_chart, use_container_width=True)
else:
    st.info("No 'fetched_at' column found for time-series chart.")

  
# -------- Notes --------
st.markdown("---")
st.markdown(
    "**Insight:** Bitcoin and Ethereum dominate the global crypto market, "
    "with steady upward momentum in their 5-day moving averages. "
    "Smaller altcoins show sharper fluctuations, reflecting higher volatility and speculative behavior."
)
