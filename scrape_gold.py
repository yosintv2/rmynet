import requests
from bs4 import BeautifulSoup
import json
import os

folder = 'data'
if not os.path.exists(folder):
    os.makedirs(folder)

url = "https://www.hamropatro.com/gold"
# A more realistic User-Agent to look like a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

try:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 1. Try to find the date
    # Method A: Look for the 'currDate' class
    # Method B: Look for the 'header' or 'title' if A fails
    date_section = soup.find('div', class_='currDate')
    if date_section:
        date_info = date_section.get_text(strip=True)
    else:
        # Fallback: Try to find any heading that looks like a date
        date_info = soup.select_one('section.repro_card h2')
        date_info = date_info.get_text(strip=True) if date_info else "Date Not Found"

    # 2. Extract Rates
    # On Hamro Patro, rates are usually in a list <li> inside a specific <ul>
    rates = {}
    # We look for the specific container for gold/silver
    items = soup.select('ul.gold-silver-rate li')

    for item in items:
        name_tag = item.find('span', class_='text')
        rate_tag = item.find('span', class_='rate')
        
        if name_tag and rate_tag:
            name = name_tag.get_text(strip=True)
            price = rate_tag.get_text(strip=True)
            rates[name] = price

    # Create the JSON structure
    output = {
        "full_date_string": date_info,
        "rates": rates
    }

    # Save to data/date.json
    with open(os.path.join(folder, 'date.json'), 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)

    # Debugging print to see what was found in the GitHub logs
    print(f"Scraped Date: {date_info}")
    print(f"Found {len(rates)} rate entries.")

except Exception as e:
    print(f"Error: {e}")
    exit(1)
