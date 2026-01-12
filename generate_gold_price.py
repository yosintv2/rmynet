import json
from datetime import datetime

# Load data
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)[0]

# Use today's date automatically
today = datetime.now()
date_str = today.strftime("%d-%b-%Y")
iso_date = today.strftime("%Y-%m-%d")

rates = data["rates"]

# SEO values
title = f"Gold Price in Nepal Today | {date_str}"
description = (
    f"Gold price in Nepal today ({date_str}). "
    "Check latest gold hallmark, Tajabi gold and silver rates per Tola and 10 gram."
)

# Generate table rows
rows = ""
for r in rates:
    rows += f"""
      <tr>
        <td>{r['item']}</td>
        <td>{r['unit']}</td>
        <td>NPR {r['price']:,.2f}</td>
      </tr>
    """

# HTML Output
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>

  <meta name="description" content="{description}">
  <meta name="keywords" content="Gold Price Nepal Today, Nepal Gold Rate, Gold Price Tola Nepal, Gold Price 10 Gram Nepal">
  <meta name="author" content="Gold Price Nepal">
  <meta name="robots" content="index, follow">

  <link rel="canonical" href="https://www.yoursite.com/gold-price-nepal-today.html">

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
      "@id": "https://www.yoursite.com/gold-price-nepal-today.html"
    }}
  }}
  </script>

  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
      background: #fafafa;
      margin: 0;
      padding: 20px;
      color: #111;
    }}
    .container {{
      max-width: 900px;
      margin: auto;
      background: #fff;
      padding: 24px;
      border-radius: 12px;
      box-shadow: 0 10px 30px rgba(0,0,0,.05);
    }}
    h1 {{
      font-size: 28px;
      margin-bottom: 10px;
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
      text-align: left;
    }}
    th {{
      background: #f5f5f5;
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
    <p class="date">Updated on: {date_str}</p>

    <table>
      <thead>
        <tr>
          <th>Metal</th>
          <th>Unit</th>
          <th>Price</th>
        </tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>

    <footer>
      <p>Gold prices are based on Nepal market rates and may vary slightly by city.</p>
    </footer>
  </main>
</body>
</html>
"""

# Save HTML
with open("gold-price-nepal-today.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Gold price HTML updated successfully!")
