import schedule
import time
from scraping.yahoo_scraper import scrape_finviz_news, save_to_db

def job():
    tickers_to_scrape = ["AAPL", "TSLA", "MSFT", "GOOG", "AMZN",
                         "ETON", "NVDA", "SOFI", "HBAN", "APLD"]
    for ticker in tickers_to_scrape:
        print(f"📡 Scraping {ticker}...")
        headlines = scrape_finviz_news(ticker)
        if headlines:
            save_to_db(ticker, headlines)
            print(f"✅ Saved {len(headlines)} headlines for {ticker}")
        else:
            print(f"⚠️ No headlines found for {ticker}")

# ✅ Run every day at 8:00 AM
schedule.every().day.at("08:00").do(job)

print("⏳ Auto-scraper started. Waiting for next run...")

while True:
    schedule.run_pending()
    time.sleep(60) # every minute
