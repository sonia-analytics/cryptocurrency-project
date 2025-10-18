import streamlit as st
import pandas as pd
import altair as alt
import ast
import os

st.title("CryptoCurrenecy Project")
st.write("Created By Sonia Mannepuli.")

df = pd.read_csv("crypto_clean.csv")

crypto = st.selectbox("Choose a cryptocurrency:", df["name"].unique())

filtered = df[df["name"] == crypto]

st.metric("Current Price (USD)", f"{filtered['current_price'].values[0]:,.2f}")
st.metric("Market Cap (USD)", f"{filtered['market_cap'].values[0]:,.0f}")

chart = alt.Chart(filtered).mark_line(point=True).encode(
    x=alt.X("fetched_at:N", title="Fetch Date"),
    y=alt.Y("current_price:Q", itle="Price USD")
)

st.altair_chart(chart, use_container_width=True)

st.title("Highlight insights with visual storytelling")
st.writw("Bitcoin and Ethereum dominate the global crypto market, contributing more than half of the total market capitalization. The 5-day moving average smooths daily volatility and reveals steady upward momentum, reflecting overall investor confidence. Meanwhile, altcoins such as Solana and XRP show sharper fluctuations, highlighting higher speculative activity and the contrasting behavior between stable large-cap assets and more volatile emerging tokens")
