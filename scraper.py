import requests
from bs4 import BeautifulSoup
import json
import re

def scrape_gold_rates():
    url = "https://www.ashesh.com.np/gold/widget.php"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        result = {"date": "", "rates": []}
        
        # Extract Date
        date_match = re.search(r'\d{2}-[A-Za-z]+-\d{4}', text)
        if date_match:
            result["date"] = date_match.group(0)

        # Extraction logic
        for i, line in enumerate(lines):
            if "Gold" in line or "Silver" in line:
                item_name = line
                # Look ahead for price and unit
                price, unit = None, ""
                for j in range(i + 1, min(i + 6, len(lines))):
                    clean = lines[j].replace('▶', '').strip()
                    if clean.replace('.', '', 1).isdigit() and price is None:
                        price = float(clean)
                    elif any(u in clean.lower() for u in ["tola", "gram"]):
                        unit = clean
                        break
                
                if price:
                    result["rates"].append({"item": item_name, "unit": unit, "price": price})

        with open("gold_rates.json", "w") as f:
            json.dump(result, f, indent=4)
        print("Successfully updated gold_rates.json")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_gold_rates()
