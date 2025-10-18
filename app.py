import streamlit as st
import pandas as pd
import altair as alt
import os

st.set_page_config(page_title="Crypto Dashboard", layout="wide")
st.title("💹 Cryptocurrency Dashboard")
st.caption("Built by Sonia Mannepuli — Week 5: Streamlit Visualization")

# ---------- Safe file loading ----------
possible_paths = [
    "data/clean/crypto_clean.csv",  # typical local path
    "crypto_clean.csv",             # if file is in root
]

FILE_PATH = None
for path in possible_paths:
    if os.path.exists(path):
        FILE_PATH = path
        break

if FILE_PATH is None:
    st.error("❌ Clean CSV not found! Upload or include 'crypto_clean.csv' in your repo.")
    st.stop()

df = pd.read_csv(FILE_PATH)
st.success(f"✅ Loaded dataset: {len(df)} rows")

# ---------- Identify crypto name column ----------
for col in ["name", "id", "symbol"]:
    if col in df.columns:
        name_col = col
        break
else:
    st.error("No column found for crypto identifier ('name', 'id', or 'symbol').")
    st.stop()

# ---------- Dropdown filter ----------
crypto_list = sorted(df[name_col].dropna().unique())
selected_crypto = st.selectbox("Select a cryptocurrency:", crypto_list)
filtered = df[df[name_col] == selected_crypto]

if filtered.empty:
    st.warning("No matching data for this selection.")
    st.stop()

# ---------- Summary metrics ----------
st.subheader("📊 Summary Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Price (USD)", f"${filtered['current_price'].iloc[0]:,.2f}")
col2.metric("Market Cap", f"${filtered['market_cap'].iloc[0]:,.0f}")
col3.metric("24h Change", f"{filtered['price_change_pct'].iloc[0]:.2f}%")

# ---------- Visualization ----------
if "fetched_at" in filtered.columns:
    chart = (
        alt.Chart(filtered)
        .mark_line(point=True)
        .encode(
            x=alt.X("fetched_at:N", title="Fetched Time"),
            y=alt.Y("current_price:Q", title="Price (USD)"),
            tooltip=[name_col, "current_price", "market_cap"]
        )
        .properties(title=f"Price Trend: {selected_crypto}")
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("⏳ No 'fetched_at' column found — trend plot skipped.")

# ---------- Insights Section ----------
st.markdown("### 💡 Highlighted Insights")
st.write("""
- **Market Leadership:** Bitcoin and Ethereum dominate total market capitalization.  
- **Trend Stability:** Large-cap coins show smoother movement and higher investor confidence.  
- **Volatility:** Smaller altcoins display sharp short-term fluctuations.
""")

