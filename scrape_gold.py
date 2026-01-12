import requests
from bs4 import BeautifulSoup
import json
import os
import re

def scrape():
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
        
        # 1. Capture Date
        date_info = "13-Jan-2026" # Default for today
        all_text = soup.get_text(separator=" ")
        date_match = re.search(r'(\d{1,2}-[A-Za-z]+-\d{4})', all_text)
        if date_match:
            date_info = date_match.group(1)

        # 2. Extract Rates using a line-by-line regex scan
        rates = []
        
        # We look for rows/divs that contain a price-like number
        # Pattern: Any text + optional arrow + 4 to 6 digits + Optional decimals + Unit
        pattern = re.compile(r"(.+?)(?:▶|:|)\s*(\d{4,7}(?:\.\d+)?)\s*(Tola|10 gram|gram)", re.IGNORECASE)

        # Get all text blocks to ensure we don't miss anything hidden in spans
        lines = [line.strip() for line in soup.get_text("\n").split("\n") if line.strip()]

        for line in lines:
            match = pattern.search(line)
            if match:
                item_name = match.group(1).strip().replace("▶", "").strip()
                price = match.group(2).strip()
                unit = match.group(3).strip()
                
                # Filter out garbage
                if "Items" not in item_name and "Unit" not in item_name:
                    rates.append({
                        "item": item_name,
                        "price": price,
                        "unit": unit
                    })

        output = {
            "full_date_string": date_info,
            "data": rates,
            "success": len(rates) > 0
        }

        with open(os.path.join(folder, 'date.json'), 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
            
        print(f"Extraction result: {len(rates)} items found.")

    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    scrape()
