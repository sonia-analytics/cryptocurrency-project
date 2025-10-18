import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Crypto Dashboard", layout="wide")
st.title("💹 Cryptocurrency Dashboard")
st.caption("Created by Sonia Mannepuli — Week 5 Visualization Project")

FILE = "crypto_clean.csv"

# --- Load data safely ---
try:
    df = pd.read_csv(FILE)
    if len(df.columns) == 1:  # handle single-column issue
        df = pd.read_csv(FILE, sep=",")
except Exception as e:
    st.error(f"Error reading file: {e}")
    st.stop()

# --- Split combined column if needed ---
if df.columns[0].count(",") > 1:
    df = df[df.columns[0]].str.split(",", expand=True)
    df.columns = ["id","symbol","name","current_price","market_cap","total_volume",
                  "high_24h","low_24h","price_change_pct","fetched_at"]

# --- Dropdown filter ---
if "name" in df.columns:
    crypto = st.selectbox("Select cryptocurrency:", sorted(df["name"].dropna().unique()))
    data = df[df["name"] == crypto]
else:
    st.error("❌ Could not find 'name' column — check your CSV header.")
    st.stop()

# --- Summary stats ---
st.subheader("📊 Summary Stats")
st.write(data[["current_price","market_cap","total]()]()

