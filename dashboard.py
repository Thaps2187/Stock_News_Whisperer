import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta

import os

DB_PATH = os.path.abspath("db/stockwhisperer.db")

def get_tickers():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT DISTINCT ticker FROM news", conn)
    conn.close()
    return df["ticker"].tolist()

def get_data(ticker, start_date, end_date):
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT title, url, timestamp, sentiment, scraped_at
        FROM news
        WHERE ticker = ?
        AND scraped_at BETWEEN ? AND ?
        ORDER BY scraped_at DESC
    """
    df = pd.read_sql_query(query, conn, params=(ticker, start_date, end_date))
    conn.close()
    return df

st.title("📈 StockWhisperer Dashboard")

tickers = get_tickers()
if not tickers:
    st.warning("⚠ No data found. Run your scraper first!")
else:
    selected_ticker = st.selectbox("Select a ticker:", tickers)

    # ✅ Date Filter (Default: Last 30 days)
    today = datetime.now().date()
    default_start = today - timedelta(days=30)
    start_date = st.date_input("Start Date", default_start)
    end_date = st.date_input("End Date", today)

    df = get_data(selected_ticker, str(start_date), str(end_date))

    if df.empty:
        st.warning("⚠ No news found for this ticker in the selected date range.")
    else:
        # ✅ Average Sentiment
        avg_sentiment = df["sentiment"].mean()
        if avg_sentiment > 0.05:
            sentiment_label = "🟢 Positive"
        elif avg_sentiment < -0.05:
            sentiment_label = "🔴 Negative"
        else:
            sentiment_label = "🟡 Neutral"

        st.subheader(f"Overall Sentiment: {sentiment_label} ({avg_sentiment:.2f})")

        # ✅ Color-Coded Table
        def color_sentiment(val):
            if val > 0.05:
                return "background-color: lightgreen"
            elif val < -0.05:
                return "background-color: salmon"
            else:
                return "background-color: lightyellow"

        styled_df = df[["title", "sentiment", "timestamp", "url"]].style.applymap(color_sentiment, subset=["sentiment"])
        st.dataframe(styled_df)

        # ✅ Sentiment Trend
        st.subheader("📊 Sentiment Over Time")
        df_sorted = df.sort_values("scraped_at")
        plt.figure(figsize=(8, 4))
        plt.plot(df_sorted["scraped_at"], df_sorted["sentiment"], marker="o")
        plt.xticks(rotation=45)
        plt.ylabel("Sentiment")
        plt.title(f"Sentiment Trend for {selected_ticker}")
        st.pyplot(plt)

        # ✅ Sentiment Distribution
        st.subheader("📊 Sentiment Distribution")
        plt.figure(figsize=(6, 4))
        plt.hist(df["sentiment"], bins=10, color="skyblue", edgecolor="black")
        plt.xlabel("Sentiment Score")
        plt.ylabel("Number of Headlines")
        plt.title("Sentiment Distribution")
        st.pyplot(plt)
