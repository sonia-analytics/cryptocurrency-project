import streamlit as st
import pandas as pd
import altair as alt
import os

# Page title
st.title("Cryptocurrency Project")
st.write("Created by Sonia Mannepuli")

# Load dataset
df = pd.read_csv("data/clean/crypto_clean.csv")

# Make sure the correct column name exists (check for 'name' or 'id')
if "name" not in df.columns:
    st.error(" Column 'name' not found in your dataset. Please check your CSV headers.")
else:
    # Dropdown to select cryptocurrency
    crypto = st.selectbox("Choose a cryptocurrency:", df["name"].unique())

    # Filter data
    filtered = df[df["name"] == crypto]

    # Display key metrics
    st.metric("Current Price (USD)", f"{filtered['current_price'].values[0]:,.2f}")
    st.metric("Market Cap (USD)", f"{filtered['market_cap'].values[0]:,.0f}")

    # Price trend chart
    chart = alt.Chart(filtered).mark_line(point=True).encode(
        x=alt.X("fetched_at:N", title="Fetch Date"),
        y=alt.Y("current_price:Q", title="Price (USD)")
    )

    st.altair_chart(chart, use_container_width=True)

    # Insight section
    st.subheader("Highlights & Insights")
    st.write(
        "Bitcoin and Ethereum dominate the global crypto market, contributing more than half of the total market capitalization. "
        "The 5-day moving average smooths daily volatility and reveals steady upward momentum, reflecting overall investor confidence. "
        "Meanwhile, altcoins such as Solana and XRP show sharper fluctuations, highlighting higher speculative activity and "
        "the contrasting behavior between stable large-cap assets and more volatile emerging tokens."
    )
