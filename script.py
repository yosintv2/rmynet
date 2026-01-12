import json
import os
from datetime import datetime, timedelta

# --- CONFIGURATION ---
JSON_FILE = 'gold_rates.json'
OUTPUT_DIR = 'gold_reports'
SITEMAP_FILE = 'sitemap.xml'
# Replace with your actual GitHub Pages URL
BASE_URL = "https://www.reducemyweight.net" 

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def get_html_template(entry, is_index=False):
    """Generates the HTML content for a price page."""
    date_val = entry['date']
    currency = entry['currency']
    title = f"Today Gold Price in Nepal - {date_val}" if is_index else f"Gold Price in Nepal on {date_val}"
    
    rows = ""
    for rate in entry['rates']:
        rows += f"""
        <tr>
            <td>{rate['item']}</td>
            <td>{rate['unit']}</td>
            <td>{currency} {rate['price']:,}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; line-height: 1.6; max-width: 800px; margin: auto; padding: 20px; background-color: #f9f9f9; }}
        .card {{ background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        h1 {{ color: #b8860b; text-align: center; border-bottom: 3px solid #ffd700; padding-bottom: 10px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ border: 1px solid #eee; padding: 15px; text-align: left; }}
        th {{ background-color: #ffd700; color: #333; }}
        tr:nth-child(even) {{ background-color: #fffdf2; }}
        .status {{ text-align: center; font-style: italic; color: #666; margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>{title}</h1>
        <table>
            <thead>
                <tr><th>Item</th><th>Unit</th><th>Price (NPR)</th></tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
        <p class="status">Data for: {date_val} | Generated on: {datetime.now().strftime('%Y-%m-%d')}</p>
    </div>
</body>
</html>"""

def main():
    try:
        with open(JSON_FILE, 'r') as f:
            data = json.load(f)
            # Handle list structure
            entries = data[0] if isinstance(data[0], list) else data

        # 1. Logic for Today/Yesterday fallback
        today_str = datetime.now().strftime("%d-%b-%Y") # e.g., 12-Jan-2026
        yesterday_str = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")
        
        data_map = {e['date']: e for e in entries}
        
        if today_str in data_map:
            index_entry = data_map[today_str]
        elif yesterday_str in data_map:
            index_entry = data_map[yesterday_str]
        else:
            index_entry = entries[0] # Fallback to the latest item in the list

        # 2. Generate index.html
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(get_html_template(index_entry, is_index=True))

        # 3. Generate individual archive pages and collect URLs
        urls = [BASE_URL] # Add root URL to sitemap
        for entry in entries:
            date_slug = entry['date'].lower().replace(' ', '-')
            filename = f"gold-price-{date_slug}.html"
            
            with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
                f.write(get_html_template(entry))
            
            urls.append(f"{BASE_URL}{OUTPUT_DIR}/{filename}")

        # 4. Generate Sitemap.xml
        sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        for url in urls:
            sitemap_xml += f"  <url><loc>{url}</loc><lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod></url>\n"
        sitemap_xml += '</urlset>'
        
        with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
            f.write(sitemap_xml)

        print(f"Done! index.html is using data from {index_entry['date']}.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
