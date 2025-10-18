import streamlit as st
import pandas as pd
import altair as alt
import os

st.set_page_config(page_title="Crypto Dashboard", layout="wide")
st.title("💹 Cryptocurrency Dashboard")
st.caption("Created by Sonia Mannepuli — Week 5 Visualization Project")

# -------- File loading --------
possible_files = [
    "data/clean/crypto_clean.csv",
    "crypto_clean.csv"
]

file_path = next((f for f in possible_files if os.path.exists(f)), None)

if not file_path:
    st.error("❌ Could not find crypto_clean.csv. Please upload it to your GitHub repo (root or data/clean/).")
    st.stop()

df = pd.read_csv(file_path)
df.columns = [c.lower().strip() for c in df.columns]  # normalize columns
st.success(f"✅ Loaded {len(df)} rows")

# -------- Identify crypto name column --------
crypto_col = next((c for c in ["name", "id", "symbol"] if c in df.columns), None)

if not crypto_col:
    st.error("No column found for crypto identifier ('name', 'id', or 'symbol'). Check your CSV headers.")
    st.write("Here are your CSV columns:", list(df.columns))
    st.stop()

# -------- Filter by crypto --------
cryptos = sorted(df[crypto_col].dropna().unique())
selected_crypto = st.selectbox("Choose a cryptocurrency:", cryptos)

filtered = df[df[crypto_col] == selected_crypto]

if filtered.empty:
    st.warning("No data found for the selected cryptocurrency.")
    st.stop()

# -------- Summary stats --------
st.subheader("📊 Summary Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Current Price (USD)", f"${filtered['current_price'].iloc[0]:,.2f}")
col2.metric("Market Cap", f"${filtered['market_cap'].iloc[0]:,.0f}")
col3.metric("24h Change (%)", f"{filtered['price_change_pct'].iloc[0]:.2f}")

# -------- Chart --------
if "fetched_at" in filtered.columns:
    chart = (
        alt.Chart(filtered)
        .mark_line(point=True)
        .encode(
            x=alt.X("fetched_at:N", title="Fetch Timestamp"),
            y=alt.Y("current_price:Q", title="Price (USD)"),
            tooltip=[crypto_col, "current_price", "market_cap", "price_change_pct"]
        )
        .properties(title=f"{selected_crypto} Price
