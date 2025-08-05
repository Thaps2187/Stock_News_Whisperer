import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "db/stockwhisperer.db"

def backfill_all_tickers(days=30):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all tickers that exist in DB
    cursor.execute("SELECT DISTINCT ticker FROM news")
    tickers = [row[0] for row in cursor.fetchall()]

    for ticker in tickers:
        # ✅ Get all headlines for this ticker
        cursor.execute("SELECT title, url, timestamp, sentiment FROM news WHERE ticker = ?", (ticker,))
        headlines = cursor.fetchall()

        if not headlines:
            print(f"⚠ No headlines to backfill for {ticker}")
            continue

        print(f"🔄 Backfilling {days} days for {ticker} (using {len(headlines)} base headlines)")

        for i in range(1, days+1):
            fake_date = (datetime.now() - timedelta(days=i)).isoformat()

            for title, url, timestamp, sentiment in headlines:
                cursor.execute("""
                    INSERT INTO news (ticker, title, url, timestamp, scraped_at, sentiment)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    ticker,
                    title,
                    url,
                    timestamp,
                    fake_date,
                    sentiment + random.uniform(-0.1, 0.1)
                ))

    conn.commit()
    conn.close()
    print("✅ Backfill complete for ALL tickers!")

if __name__ == "__main__":
    backfill_all_tickers(30)
