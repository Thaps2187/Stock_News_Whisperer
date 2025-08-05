import sqlite3
import pandas as pd

def export_news(ticker):
    conn = sqlite3.connect("db/stockwhisperer.db")
    df = pd.read_sql_query("""
        SELECT * FROM news
        WHERE ticker = ?
        ORDER BY scraped_at DESC
    """, conn, params=(ticker.upper(),))

    conn.close()

    if df.empty:
        print(f"❌ No news found for {ticker.upper()}")
    else:
        filename = f"{ticker.upper()}_news.csv"
        df.to_csv(filename, index=False)
        print(f"✅ Exported {len(df)} articles to {filename}")

if __name__ == "__main__":
    ticker = input("Enter ticker symbol to export: ")
    export_news(ticker)

 