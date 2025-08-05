import os
import subprocess

def run_scraper():
    print("📡 Running scraper for multiple tickers...")
    subprocess.run(["python", "scraping/finviz_scraper.py"])

def run_dashboard():
    print("📊 Starting Streamlit dashboard...")
    subprocess.run(["streamlit", "run", "dashboard.py"])

def run_backfill():
    print("🕒 Backfilling 30 days of fake data for testing...")
    subprocess.run(["python", "backfill_data.py"])

if __name__ == "__main__":
    print("""
    ==============================
       📈 STOCKWHISPERER MENU
    ==============================
    1️⃣  Run scraper (fetch news & save to DB)
    2️⃣  Run dashboard (visualize sentiment)
    3️⃣  Backfill 30 days of fake data
    4️⃣  Exit
    """)

    choice = input("Select an option (1-4): ")

    if choice == "1":
        run_scraper()
    elif choice == "2":
        run_dashboard()
    elif choice == "3":
        run_backfill()
    else:
        print("👋 Exiting StockWhisperer.")
