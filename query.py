import sqlite3

def fetch_recent_news(ticker):
    conn = sqlite3.connect("db/stockwhisperer.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title, url, timestamp, sentiment, scraped_at
        FROM news
        WHERE ticker = ?
        ORDER BY scraped_at DESC
        LIMIT 10
    """, (ticker.upper(),))

    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        print(f"\n {row[0]}\n {row[1]}\n {row[2]} | Sentiment: {row[3]:.2f} | Scraped: {row[4]}\n")

if __name__ == "__main__":
    ticker = input("Enter ticker symbol (e.g., AAPL): ")
    fetch_recent_news(ticker)
