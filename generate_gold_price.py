import json
from datetime import datetime

# ===============================
# CONFIG
# ===============================
DATA_FILE = "gold_rates.json"
OUTPUT_FILE = "index.html"
SITE_URL = "/"

# ===============================
# LOAD DATA
# ===============================
with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

rates = data[0]["rates"]

# ===============================
# DATE HANDLING
# ===============================
today = datetime.now()
date_str = today.strftime("%d-%b-%Y")
iso_date = today.strftime("%Y-%m-%d")

# ===============================
# SEO TEXT
# ===============================
title = f"Gold Price in Nepal Today | {date_str}"
description = (
    f"Gold price in Nepal today ({date_str}). "
    "Latest gold hallmark 9999, Tajabi gold and silver rates "
    "per Tola and 10 gram updated daily."
)

# ===============================
# TABLE ROWS
# ===============================
table_rows = ""
for r in rates:
    table_rows += f"""
      <tr>
        <td>{r['item']}</td>
        <td>{r['unit']}</td>
        <td>NPR {r['price']:,.2f}</td>
      </tr>
    """

# ===============================
# HTML TEMPLATE
# ===============================
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>

<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{description}">
<meta name="keywords" content="Gold Price Nepal Today, Nepal Gold Rate, Gold Price Tola Nepal, Gold Price 10 Gram Nepal">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{SITE_URL}">

<!-- Open Graph -->
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="article">
<meta property="og:locale" content="en_NP">

<!-- Schema -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "{title}",
  "datePublished": "{iso_date}",
  "dateModified": "{iso_date}",
  "author": {{
    "@type": "Organization",
    "name": "Gold Price Nepal"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "Gold Price Nepal"
  }},
  "mainEntityOfPage": {{
    "@type": "WebPage",
    "@id": "{SITE_URL}"
  }}
}}
</script>

<style>
body {{
  font-family: -apple-system, BlinkMacSystemFont, sans-serif;
  background: #f6f6f6;
  margin: 0;
  padding: 20px;
  color: #111;
}}
.container {{
  max-width: 900px;
  margin: auto;
  background: #ffffff;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0,0,0,.06);
}}
h1 {{
  font-size: 28px;
  margin-bottom: 6px;
}}
.date {{
  color: #666;
  margin-bottom: 20px;
}}
table {{
  width: 100%;
  border-collapse: collapse;
}}
th, td {{
  padding: 14px;
  border-bottom: 1px solid #eee;
}}
th {{
  background: #fafafa;
  text-align: left;
}}
footer {{
  margin-top: 30px;
  font-size: 14px;
  color: #666;
}}
</style>
</head>

<body>
<main class="container">
  <h1>{title}</h1>
  <p class="date">Updated on {date_str}</p>

  <table>
    <thead>
      <tr>
        <th>Metal</th>
        <th>Unit</th>
        <th>Price</th>
      </tr>
    </thead>
    <tbody>
      {table_rows}
    </tbody>
  </table>

  <footer>
    <p>Prices are based on Nepal market rates and may vary by location.</p>
  </footer>
</main>
</body>
</html>
"""

# ===============================
# WRITE FILE
# ===============================
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ index.html generated successfully!")
