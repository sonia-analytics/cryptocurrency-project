import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import os

st.title("Cryptocurrency Dashboard")
st.write("Author: Sonia Mannepuli — Week 5 Visualization Project")

FILE = "crypto_clean.csv"

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

if "name" in df.columns:
    crypto = st.selectbox("Select cryptocurrency:", sorted(df["name"].dropna().unique()))
    data = df[df["name"] == crypto]
else:
    st.error("Missing 'name' column. Please check your CSV.")
    st.stop()

st.subheader("Data Preview")
st.dataframe(data.head(10))

st.subheader("Summary Stats")
st.write(data[["current_price", "market_cap", "total_volume"]].describe())

if "fetched_at" in data.columns:
    data["fetched_at"] = pd.to_datetime(data["fetched_at"], errors="coerce")
    chart = (
        alt.Chart(data)
        .mark_line(point=True)
        .encode(x="fetched_at:T", y="current_price:Q", color=alt.value("skyblue"))
        .properties(title=f"{crypto} Price Trend")
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.warning("No 'fetched_at' column found for trend chart.")

st.subheader("Additional Charts")

try:
    # Convert market_cap to numeric
    df["market_cap"] = pd.to_numeric(df["market_cap"], errors="coerce")
    top5 = df.nlargest(5, "market_cap").dropna(subset=["market_cap"])
    fig1, ax1 = plt.subplots(figsize=(8,4))
    ax1.bar(top5["name"], top5["current_price"], color="gold")
    ax1.set_title("Top 5 Cryptos – Current Price")
    ax1.set_ylabel("Price (USD)")
    ax1.set_xticklabels(top5["name"], rotation=30)
    st.pyplot(fig1)
except Exception as e:
    st.warning(f"Could not plot Top 5 chart: {e}")

try:
    df["price_ma"] = df["current_price"].rolling(5, min_periods=1).mean()

    fig2, ax2 = plt.subplots(figsize=(6,3))  # compact and clean
    ax2.plot(df["current_price"], label="Price", color="steelblue", linewidth=1.3)
    ax2.plot(df["price_ma"], label="5-Day MA", color="darkorange", linewidth=1.6, linestyle="--")

    ax2.set_title("Price vs 5-Day Moving Average", fontsize=11, pad=10)
    ax2.set_xlabel("Index", fontsize=9)
    ax2.set_ylabel("Price (USD)", fontsize=9)
    ax2.legend(fontsize=8, frameon=False, loc="upper left")  # 🔹 Removes dark box
    ax2.grid(alpha=0.3)
    ax2.tick_params(axis="both", labelsize=8)

    st.pyplot(fig2)
except Exception as e:
    st.warning(f"Could not plot Moving Average chart: {e}")

st.markdown("---")
st.write("Data source: CoinGecko API | Visualization by Sonia Mannepuli")
