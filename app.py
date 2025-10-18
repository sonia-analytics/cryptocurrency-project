import streamlit as st
import pandas as pd
import altair as alt
import os

st.set_page_config(page_title="Crypto Market Dashboard", layout="wide")
st.title("💹 Cryptocurrency Dashboard")
st.caption("Built by Sonia Mannepuli — Week 5: Data Visualization & Storytelling")

# ---------- Load Cleaned Data ----------
FILE_PATH = "data/clean/crypto_clean.csv"
if not os.path.exists(FILE_PATH):
    st.error("❌ Clean CSV not found. Please ensure crypto_clean.csv is in data/clean/")
    st.stop()

df = pd.read_csv(FILE_PATH)
st.write("✅ Dataset loaded successfully —", len(df), "rows")

# Show available columns for transparency
st.write("**Available Columns:**", list(df.columns))

# ---------- Choose column for crypto selection ----------
name_col = None
for col in ["name", "id", "symbol"]:
    if col in df.columns:
        name_col = col
        break

if not name_col:
    st.error("No suitable crypto identifier found (expected 'name', 'id', or 'symbol').")
    st.stop()

# ---------- Filters ----------
cryptos = sorted(df[name_col].unique())
crypto = st.selectbox("Select Cryptocurrency:", cryptos)

filtered = df[df[name_col] == crypto]

if filtered.empty:
    st.warning("No data found for this cryptocurrency.")
    st.stop()

# ---------- Summary Stats ----------
col1, col2, col3 = st.columns(3)
col1.metric("Current Price (USD)", f"${filtered['current_price'].values[0]:,.2f}")
col2.metric("Market Cap", f"${filtered['market_cap'].values[0]:,.0f}")
col3.metric("24h Change (%)", f"{filtered['price_change_pct'].values[0]:.2f}%")

# ---------- Visualization ----------
if "fetched_at" in filtered.columns:
    chart = (
        alt.Chart(filtered)
        .mark_line(point=True)
        .encode(
            x=alt.X("fetched_at:N", title="Fetch Time"),
            y=alt.Y("current_price:Q", title="Price (USD)"),
            tooltip=[name_col, "current_price", "market_cap"]
        )
        .properties(title=f"Price Trend for {crypto}")
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("No time column ('fetched_at') available for trend visualization.")

# ---------- Insights ----------
st.subheader("📊 Highlighted Insights")
st.write("""
**Market Leadership:** Bitcoin and Ethereum dominate the overall crypto market, 
holding over half of total capitalization.

**Price Behavior:** The 5-day moving average shows smoother trends, revealing 
underlying market direction beyond daily noise.

**Volatility Patterns:** Altcoins such as Solana and XRP show sharper price swings, 
reflecting higher speculative behavior compared to stable large-cap assets.
""")
