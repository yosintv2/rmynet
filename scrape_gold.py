import json
import os
from playwright.sync_api import sync_playwright

def scrape():
    folder = 'data'
    if not os.path.exists(folder):
        os.makedirs(folder)

    with sync_playwright() as p:
        # Launching Chromium
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = context.new_page()
        
        try:
            # Go to Hamro Patro Gold page
            page.goto("https://www.hamropatro.com/gold", wait_until="networkidle", timeout=60000)
            
            # Wait for the date element to appear
            page.wait_for_selector('.currDate')

            # Extract Data
            date_info = page.locator('.currDate').inner_text()
            
            rates = {}
            # Target the list items specifically
            items = page.locator('ul.gold-silver-rate li').all()
            
            for item in items:
                name = item.locator('.text').inner_text()
                price = item.locator('.rate').inner_text()
                if name and price:
                    rates[name.strip()] = price.strip()

            output = {
                "full_date_string": date_info.strip(),
                "rates": rates
            }

            # Save JSON
            file_path = os.path.join(folder, 'date.json')
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=4)
                
            print(f"Successfully scraped: {date_info}")

        except Exception as e:
            print(f"Error during scraping: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    scrape()
