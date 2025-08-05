import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
from textblob import TextBlob

def scrape_finviz_news(ticker):
    url = f"https://finviz.com/quote.ashx?t={ticker}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve data for {ticker}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    news_table = soup.find("table", class_="fullview-news-outer")
    if not news_table:
        return []

    rows = news_table.find_all("tr")
    news = []

    for row in rows[:10]:
        cols = row.find_all("td")
        if len(cols) >= 2:
            time = cols[0].text.strip()
            link_tag = cols[1].find("a")
            if link_tag:
                title = link_tag.text.strip()
                link = link_tag["href"]
                sentiment = TextBlob(title).sentiment.polarity  # ✅ CALCULATE SENTIMENT
                news.append({
                    "title": title,
                    "url": link,
                    "timestamp": time,
                    "sentiment": sentiment  # ✅ STORE SENTIMENT
                })
    return news

def save_to_db(ticker, articles):
    conn = sqlite3.connect("db/stockwhisperer.db")
    cursor = conn.cursor()

    scraped_at = datetime.now().isoformat()

    for article in articles:
        cursor.execute("""
            INSERT INTO news (ticker, title, url, timestamp, scraped_at, sentiment)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            ticker,
            article['title'],
            article['url'],
            article['timestamp'],
            scraped_at,
            article['sentiment']  # ✅ INSERT SENTIMENT
        ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    tickers_to_scrape = ["AAPL", "TSLA", "MSFT", "GOOG", "AMZN",
                         "ETON", "NVDA", "SOFI", "HBAN", "APLD"]  

    for ticker in tickers_to_scrape:
        print(f"\n Scraping news for {ticker}...")
        headlines = scrape_finviz_news(ticker)

        if headlines:
            save_to_db(ticker, headlines)
            print(f"✅ Saved {len(headlines)} headlines for {ticker}")
        else:
            print(f"⚠️ No headlines found for {ticker}")


