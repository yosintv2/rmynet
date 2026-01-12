import requests
from bs4 import BeautifulSoup
import json
import os
import re

def scrape():
    folder = 'data'
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Note: Use the exact URL with the API key as provided
    url = "https://www.ashesh.com.np/gold/widget.php?api=820174j460"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        # Force encoding to handle Nepali characters if necessary
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. Extract Date
        date_info = "Date Not Found"
        # Look for the date header (usually inside a div with id 'gold-date' or similar)
        date_div = soup.find(id='gold-date') or soup.find(class_='date')
        if date_div:
            date_info = date_div.get_text(strip=True)
        else:
            # Fallback regex for DD-Mon-YYYY
            match = re.search(r'(\d{1,2}-[A-Za-z]+-\d{4})', soup.get_text())
            if match:
                date_info = match.group(1)

        # 2. Extract Data (Targeting specific structure)
        rates = []
        # The widget often places each rate inside a <tr> or a <div> with specific classes
        items = soup.find_all('tr')
        
        for item in items:
            text = item.get_text(" ", strip=True)
            # We look for the "▶" symbol which is a unique separator in this widget
            if "▶" in text:
                parts = text.split("▶")
                # parts[0] is usually "Item Unit"
                # parts[1] is usually "Price Unit"
                
                # Cleanup and extract price using regex
                price_match = re.search(r'(\d+\.?\d*)', parts[1])
                if price_match:
                    price = price_match.group(1)
                    # Extract the label from the first part
                    label = parts[0].strip()
                    # Determine unit (Tola vs 10 gram)
                    unit = "Tola" if "Tola" in text else "10 gram"
                    
                    rates.append({
                        "item": label,
                        "price": price,
                        "unit": unit
                    })

        # Save to JSON
        output = {
            "full_date_string": date_info,
            "data": rates,
            "success": len(rates) > 0
        }

        with open(os.path.join(folder, 'date.json'), 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
            
        print(f"Items found: {len(rates)}")

    except Exception as e:
        print(f"Critical Error: {e}")
        exit(1)

if __name__ == "__main__":
    scrape()
