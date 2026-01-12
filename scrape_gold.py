import requests
from bs4 import BeautifulSoup
import json
import os

# Create folder if it doesn't exist
folder = 'data'
if not os.path.exists(folder):
    os.makedirs(folder)

url = "https://www.hamropatro.com/gold"
# Adding a common User-Agent to avoid being blocked by the server
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status() # Check if the request was successful
    soup = BeautifulSoup(response.text, 'html.parser')

    # Targeted selection: Hamro Patro uses 'column-left' or specific classes for the gold section
    # Let's try to find the date more reliably
    date_element = soup.find('div', class_='currDate')
    date_info = date_element.text.strip() if date_element else "Date Not Found"

    # Find the gold/silver list
    # The structure is usually an unordered list <ul> inside the gold-silver container
    gold_items = soup.select('ul.gold-silver-rate li')

    rates = {}
    for item in gold_items:
        try:
            name = item.find('span', class_='text').text.strip()
            price = item.find('span', class_='rate').text.strip()
            rates[name] = price
        except AttributeError:
            continue

    extracted_data = {
        "full_date_string": date_info,
        "rates": rates
    }

    # Save to data/date.json
    file_path = os.path.join(folder, 'date.json')
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=4)

    print(f"Successfully saved data to {file_path}")

except Exception as e:
    print(f"An error occurred: {e}")
    # Create an empty/error file so the workflow doesn't just fail silently
    exit(1)
