import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import re
#import schedule
#import time
import os


# === Config ===
URL = "https://www.amazon.com/SAMSUNG-Technology-Intelligent-Turbowrite-MZ-V9S2T0B/dp/B0DHLCRF91/ref=sr_1_3?crid=28VXXTKES7XBJ&dib=eyJ2IjoiMSJ9.2iJmllTU0r_cPP3pev4O6zLoHMscJKQC7wYkUiWPe-vMtCGfTU_IQCM54LM13hAxzbDj5cGm2tH6B7EIXdhid1_a1qyg6lSyjU8cx74XWDUk-kqH_YYTv40aQ1QIKgj5BfFfGiUype-fCQyVXrN-BvMyrcHgvFYRf3K80ekgs8MS7mFOSFL7awCEQiS-khDFwDIcReVQ0WB1fspgdJVX_2z3SG_jWx19CsCPuf7J8Mk.jKPBFXOapp7tJHwLKeWQcB4xN752WuepTiyr2iKCQEQ&dib_tag=se&keywords=SSD&qid=1746241233&sprefix=ssd%2Caps%2C165&sr=8-3&th=1"


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36", 
    "Accept_Language": "en-US,en;q=0.9"
}


# === Main Function ===
def scrape_price():
    # Send a GET request to the URL
    session = requests.Session()
    response = session.get( URL, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "lxml")
        print(soup.prettify())  # Print the HTML content for debugging
        try:
            title = soup.find(id="productTitle").get_text().strip()
            price_whole = soup.find("span", class_="a-price-whole").get_text()
            price_fraction = soup.find("span", class_="a-price-fraction").get_text()
            price = float(f"{price_whole}{price_fraction}")
            #price = float(re.sub(r"[^\d.]", "", price_str))

        except AttributeError as e:
            print(f"Error: {e}")
            print("Could not find product title or price. Structure may have changed.")
            title = "Unknown Product"
            price = None


        if price is not None:
            today = datetime.now().strftime("%Y-%m-%d")   # Get today's date
            CSV_FILE = "amazon_ssd_price_log.csv"
            file_exists = os.path.isfile(CSV_FILE)

            # Write the date, time, and price to a CSV file
            with open(CSV_FILE, mode="a", newline="") as file:
                writer = csv.writer(file)

                if not file_exists:
                    writer.writerow([title])  # write title once
                    writer.writerow(["Date", "Price"])  # write headers once

                writer.writerow([today, price])
            
            print(f"{today} | ${price} recorded.")

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")


scrape_price()  # Run the function once

#  *** Optional: Alternative to cron jobs or Windows Task Scheduler or cloud host ***
# === Schedule to Run Daily === 
# schedule.every().day.at("09:00").do(scrape_price)  # 9:00 AM daily

# print("📆 Scheduler started. Waiting for next run...")
# scrape_price()  # Run once immediately (optional)

# while True:
#     schedule.run_pending()
#     time.sleep(60)  # Check every minute
