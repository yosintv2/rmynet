import requests
from bs4 import BeautifulSoup
import json
import os
import re

def scrape():
    # Ensure data folder exists
    folder = 'data'
    if not os.path.exists(folder):
        os.makedirs(folder)

    url = "https://www.ashesh.com.np/gold/widget.php?api=820174j460"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. Extract Date
        # The date is usually in a div or span. We look for the DD-Mon-YYYY pattern.
        date_text = soup.get_text()
        date_match = re.search(r'(\d{1,2}-[A-Za-z]+-\d{4})', date_text)
        date_info = date_match.group(1) if date_match else "Date Not Found"

        # 2. Extract Gold/Silver Rates
        rates = []
        # The widget uses a table. We find all rows <tr>
        rows = soup.find_all('tr')
        
        for row in rows:
            cols = row.find_all('td')
            # Look for rows that have data (usually 3 or more columns)
            if len(cols) >= 3:
                item_name = cols[0].get_text(strip=True).replace('▶', '')
                price = cols[1].get_text(strip=True)
                unit = cols[2].get_text(strip=True)
                
                # Filter out header rows like "Items", "Unit", "Price"
                if "Price" not in price and price:
                    rates.append({
                        "item": item_name,
                        "price": price,
                        "unit": unit
                    })

        output = {
            "full_date_string": date_info,
            "data": rates
        }

        # Save to data/date.json
        file_path = os.path.join(folder, 'date.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
            
        print(f"Scraped successfully for date: {date_info}")

    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    scrape()
