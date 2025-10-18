
import streamlit as st
import pandas as pd
import altair as alt
import os

# ---- Streamlit Page Setup ----
st.set_page_config(page_title="CryptoCurrency Dashboard", layout="wide")
st.title("💹 Cryptocurrency Dashboard")
st.write("Created by Sonia Mannepuli — Week 5 Visualization Project")

# ---- File Path ----
FILE_PATH = "crypto_clean.csv"

# ---- Load Data ----
if not os.path.exists(FILE_PATH):
    st.error("❌ CSV file not found. Please make sure 'crypto_clean.csv' is in the repository root.")
    st.stop()

try:
    df = pd.read_csv(FILE_PATH)
    # Some CSVs get read as a single column — fix that
    if len(df.columns) == 1:
        df = pd.read_csv(FILE_PATH, sep=",")
except Exception as e:
    st.error(f"Error loading CSV: {e}")
    st.stop()

# ---- Validate Columns ----
expected_cols = ["id", "symbol", "name", "current_price", "market_cap", 
                 "total_volume", "high_24h", "low_24h", "price_change_pct", "fetched_at"]

missing = [c for c in expected_cols if c not in df.columns]
if missing:
    st.warning(f"⚠ Missing expected columns: {missing}")

if not any(col in df.columns for col in ["name", "id", "symbol"]):
    st.error(f"No valid crypto identifier found in CSV. Available columns: {list(df.columns)}")
    st.stop()

# ---- Dropdown Filter ----
crypto_col = "name" if "name" in df.columns else ("id" if "id" in df.columns else "symbol")
cryptos = sorted(df[crypto_col].dropna().unique())
selected_crypto = st.selectbox("Choose a cryptocurrency:", cryptos)

# ---- Filtered Data ----
data = df[df[crypto_col] == selected_crypto].copy()

# ---- Summary Statistics ----
st.subheader("📊 Summary Statistics")
summary = data[["current_price", "market_cap", "total_volume"]].describe().T
st.dataframe(summary)

# ---- Chart ----
st.subheader("📈 Price Trend (with 5-Day Moving Average)")
if "fetched_at" in data.columns:
    data["fetched_at"] = pd.to_datetime(data["fetched_at"], errors="coerce")
    data = data.sort_values("fetched_at")
    data["MA_5"] = data["current_price"].rolling(5).mean()

    base = alt.Chart(data).encode(x="fetched_at:T")
    price = base.mark_line(color="skyblue").encode(y="current_price:Q")
    ma = base.mark_line(color="orange").encode(y="MA_5:Q")
    chart = (price + ma).properties(title=f"{selected_crypto} Price Trend", width=800, height=400)
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("No 'fetched_at' column found — skipping time-series chart.")

# ---- Highlight Insights ----
st.markdown("""
### 🔍 Insights
- Bitcoin and Ethereum dominate the market, contributing over half of total capitalization.  
- The 5-day moving average smooths volatility, showing consistent growth trends.  
- Altcoins like Solana and XRP exhibit sharper fluctuations — reflecting higher speculative interest.  
""")

st.success(f"✅ Loaded {len(df)} rows successfully.")
