import requests
from bs4 import BeautifulSoup
import json
import os

# फोल्डर बनाना अगर मौजूद नहीं है
folder = 'data'
if not os.path.exists(folder):
    os.makedirs(folder)

url = "https://www.hamropatro.com/gold"
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# तारीख और भाव निकालना
date_info = soup.find('div', class_='currDate').text.strip()
gold_items = soup.find_all('li', class_='item') # Hamro Patro के वर्तमान स्ट्रक्चर के अनुसार

extracted_data = {
    "full_date_string": date_info,
    "rates": {}
}

for item in gold_items:
    label = item.find('span', class_='text').text.strip()
    price = item.find('span', class_='rate').text.strip()
    extracted_data["rates"][label] = price

# 'data/date.json' के रूप में सेव करना
file_path = os.path.join(folder, 'date.json')
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(extracted_data, f, ensure_ascii=False, indent=4)

print(f"Data successfully saved to {file_path}")
