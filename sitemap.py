import os
from datetime import date

SITE_URL = "https://reducemyweight.net"
OUTPUT_DIR = "output"
SITEMAP_FILE = "output/sitemap.xml"

today = date.today().isoformat()

urls = []

for file in os.listdir(OUTPUT_DIR):
    if file.endswith(".html"):
        priority = "0.8"
        changefreq = "monthly"

        # Homepage or important pages
        if "index" in file:
            priority = "1.0"
            changefreq = "daily"

        urls.append(f"""
  <url>
    <loc>{SITE_URL}/{file}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>
""")

sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">
{''.join(urls)}
</urlset>
"""

with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
    f.write(sitemap)

print("✅ sitemap.xml generated successfully.")
