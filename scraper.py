import requests 
from bs4 import BeautifulSoup
import json
import re
import os

def scrape_gold_rates():
    url = "https://www.ashesh.com.np/gold/widget.php"
    headers = {'User-Agent': 'Mozilla/5.0'}
    filename = "gold_rates.json"
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        # Prepare the new entry
        new_entry = {
            "date": "",
            "currency": "NPR",
            "rates": []
        }
        
        # Extract Date
        date_match = re.search(r'\d{2}-[A-Za-z]+-\d{4}', text)
        if date_match:
            new_entry["date"] = date_match.group(0)

        # Extraction logic
        for i, line in enumerate(lines):
            if "Gold" in line or "Silver" in line:
                item_name = line
                price, unit = None, ""
                for j in range(i + 1, min(i + 6, len(lines))):
                    clean = lines[j].replace('▶', '').strip()
                    if clean.replace('.', '', 1).isdigit() and price is None:
                        price = float(clean)
                    elif any(u in clean.lower() for u in ["tola", "gram"]):
                        unit = clean
                        break
                
                if price:
                    new_entry["rates"].append({
                        "item": item_name, 
                        "unit": unit, 
                        "price": price
                    })

        # --- APPENDING LOGIC ---
        # 1. Load existing data if file exists, else start a new list
        if os.path.exists(filename):
            with open(filename, "r") as f:
                try:
                    all_data = json.load(f)
                    if not isinstance(all_data, list):
                        all_data = [all_data]
                except json.JSONDecodeError:
                    all_data = []
        else:
            all_data = []

        # 2. Check if the date is already in our data to avoid duplicates
        existing_dates = [entry.get("date") for entry in all_data]
        if new_entry["date"] not in existing_dates:
            all_data.append(new_entry)
            with open(filename, "w") as f:
                json.dump(all_data, f, indent=4)
            print(f"Data for {new_entry['date']} added.")
        else:
            print(f"Data for {new_entry['date']} already exists. Skipping.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_gold_rates()
