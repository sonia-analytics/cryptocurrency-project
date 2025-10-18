import streamlit as st
import pandas as pd
import altair as alt
import os

st.set_page_config(page_title="Crypto Dashboard", layout="wide")
st.title("Cryptocurrency Dashboard")
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
st.title("Charts Below")
top5 = df.nlargest(5, "market_cap")
plt.figure(figsize=(10,5))
plt.plot(top5["name"], top5["current_price"], marker="o")
plt.title("Top 5 Cryptos – Current Price")
plt.ylabel("Price (USD)")
plt.xticks(rotation=30)
plt.show()

# Moving average example
df["price_ma"] = df["current_price"].rolling(5, min_periods=1).mean()
plt.figure(figsize=(10,5))
plt.plot(df["current_price"], label="Price")
plt.plot(df["price_ma"], label="5-Day MA")
plt.legend(); plt.title("Price vs Moving Average"); plt.show()


st.markdown("---")
st.write("Data source: CoinGecko API | Visualization by Sonia Mannepuli")
