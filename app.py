import streamlit as st
import pandas as pd
import altair as alt
import os

st.title("Cryptocurrency Project")
st.write("Created by Sonia Mannepuli")

# Load dataset
df = pd.read_csv("data/clean/crypto_clean.csv")

# Display available columns (for debugging)
st.write("Columns in dataset:", list(df.columns))

# Choose a column that exists
if "name" in df.columns:
    options = df["name"].unique()
    label = "name"
elif "id" in df.columns:
    options = df["id"].unique()
    label = "id"
elif "symbol" in df.columns:
    options = df["symbol"].unique()
    label = "symbol"
else:
    st.error("No valid crypto name column found (expected 'name', 'id', or 'symbol').")
    st.stop()

# Dropdown
crypto = st.selectbox("Choose a cryptocurrency:", options)

# Filter data
filtered = df[df[label] == crypto]

# Display metrics
st.metric("Current Price (USD)", f"{filtered['current_price'].values[0]:,.2f}")
st.metric("Market Cap (USD)", f"{filtered['market_cap'].values[0]:,.0f}")

# Chart
chart = alt.Chart(filtered).mark_line(point=True).encode(
    x=alt.X("fetched_at:N", title="Fetch Date"),
    y=alt.Y("current_price:Q", title="Price (USD)")
)
st.altair_chart(chart, use_container_width=True)

st.subheader("Highlights & Insights")
st.write(
    "Bitcoin and Ethereum dominate the global crypto market, contributing more than half of the total market capitalization. "
    "The 5-day moving average smooths daily volatility and reveals steady upward momentum, reflecting overall investor confidence. "
    "Meanwhile, altcoins such as Solana and XRP show sharper fluctuations, highlighting higher speculative activity and "
    "the contrasting behavior between stable large-cap assets and more volatile emerging tokens."
)
