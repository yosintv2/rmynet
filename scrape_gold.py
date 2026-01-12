import json
import os
from playwright.sync_api import sync_playwright

def scrape():
    folder = 'data'
    if not os.path.exists(folder):
        os.makedirs(folder)

    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to URL
        url = "https://www.hamropatro.com/gold"
        page.goto(url, wait_until="networkidle")

        # 1. Extract Date
        # Trying common selectors for the date container
        date_info = page.locator('.currDate').inner_text() or "Date Not Found"

        # 2. Extract Rates
        rates = {}
        # Find the list items in the gold rate section
        items = page.locator('ul.gold-silver-rate li').all()
        
        for item in items:
            name = item.locator('.text').inner_text()
            price = item.locator('.rate').inner_text()
            if name and price:
                rates[name.strip()] = price.strip()

        # Build final JSON
        output = {
            "full_date_string": date_info.strip(),
            "rates": rates
        }

        # Save to file
        with open(os.path.join(folder, 'date.json'), 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)

        browser.close()
        print(f"Scraped Successfully: {date_info}")

if __name__ == "__main__":
    scrape()
