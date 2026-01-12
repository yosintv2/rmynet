import requests
from bs4 import BeautifulSoup
import json
import os
import re

folder = 'data'
if not os.path.exists(folder):
    os.makedirs(folder)

url = "https://www.hamropatro.com/gold"
# Emulate a real Chrome browser to bypass bot detection
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}

def scrape():
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. Improved Date Extraction
        # Look for the date in multiple possible locations
        date_info = "Date Not Found"
        date_element = soup.select_one('.currDate, .current-date, #top-date')
        if date_element:
            date_info = date_element.get_text(strip=True)
        else:
            # Look for any text that matches the pattern "Day, Month Date, Year"
            match = re.search(r'\w+, \w+ \d+, \d{4}', response.text)
            if match:
                date_info = match.group(0)

        # 2. Extract Rates by searching for specific labels
        rates = {}
        # Hamro Patro labels for 2026
        target_labels = [
            "Gold Hallmark - tola", "Gold Tajabi - tola", "Silver - tola",
            "Gold Hallmark - 10g", "Gold Tajabi - 10g", "Silver - 10g"
        ]

        # Find all list items or spans that might contain the prices
        items = soup.find_all(['li', 'div'], class_=re.compile(r'item|rate-list'))
        
        for item in items:
            text_content = item.get_text(" ", strip=True)
            for label in target_labels:
                if label in text_content:
                    # Extract the price (usually looks like Nrs. XXX,XXX.XX)
                    price_match = re.search(r'Nrs\.\s*[\d,.]+', text_content)
                    if price_match:
                        rates[label] = price_match.group(0)

        # 3. Fallback: If rates is still empty, try parsing all spans with 'rate' class
        if not rates:
            price_spans = soup.select('.rate')
            for span in price_spans:
                parent_text = span.parent.get_text(strip=True)
                rates[parent_text[:20]] = span.get_text(strip=True)

        output = {
            "full_date_string": date_info,
            "rates": rates,
            "last_updated": str(os.popen('date').read().strip())
        }

        with open(os.path.join(folder, 'date.json'), 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)

        print(f"Scraped Date: {date_info}")
        print(f"Found {len(rates)} rates.")

    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    scrape()
