import os
from datetime import date

# =========================
# CONFIG
# =========================
SITE_PATH = "/rmynet"
OUTPUT_DIR = "output"

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

START_YEAR = date.today().year
END_YEAR = START_YEAR + 5

os.makedirs(OUTPUT_DIR, exist_ok=True)

ALL_PAGES = []

# =========================
# PAGE GENERATOR
# =========================
def generate_page(month, year):
    slug = f"weight-loss-plan-{month.lower()}-{year}.html"
    filepath = f"{OUTPUT_DIR}/{slug}"

    ALL_PAGES.append({
        "title": f"{month} {year} Weight Loss Plan",
        "slug": slug,
        "year": year,
        "month": month
    })

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{month} {year} Weight Loss Plan</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>

<body style="font-family: sans-serif; max-width: 800px; margin: auto;">
<nav>
  <a href="{SITE_PATH}/index.html">Home</a>
</nav>

<h1>{month} {year} Weight Loss Plan</h1>
<p>Simple and sustainable weight loss plan for {month} {year}.</p>

<footer>
  <p>© ReduceMyWeight</p>
</footer>
</body>
</html>
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"📝 Generated: {filepath}")

# =========================
# INDEX PAGE (ROOT)
# =========================
def generate_index():
    pages_by_year = {}

    for p in ALL_PAGES:
        pages_by_year.setdefault(p["year"], []).append(p)

    listing = ""

    for year in sorted(pages_by_year.keys(), reverse=True):
        listing += f"<h2>{year}</h2><ul>"
        for p in pages_by_year[year]:
            listing += f"""
            <li>
              <a href="{SITE_PATH}/output/{p['slug']}">
                {p['month']} {p['year']} Weight Loss Plan
              </a>
            </li>
            """
        listing += "</ul>"

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Reduce My Weight</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- Tailwind -->
<script src="https://cdn.tailwindcss.com"></script>
</head>

<body class="bg-gray-100 text-gray-900">
<div class="max-w-4xl mx-auto p-6">

<header class="mb-8">
  <h1 class="text-4xl font-bold">Reduce My Weight</h1>
  <p class="text-gray-600">Monthly Weight Loss Plans</p>

  <nav class="mt-4 space-x-4">
    <a href="{SITE_PATH}/index.html" class="text-blue-600">Home</a>
    <a href="{SITE_PATH}/sitemap.xml" class="text-blue-600">Sitemap</a>
  </nav>
</header>

{listing}

<footer class="mt-10 text-sm text-gray-500">
  © ReduceMyWeight
</footer>

</div>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

    print("🏠 index.html written at ROOT")

# =========================
# BUILD
# =========================
print("🚀 Build started")

for year in range(START_YEAR, END_YEAR + 1):
    for month in MONTHS:
        generate_page(month, year)

generate_index()

print(f"✅ Build finished — {len(ALL_PAGES)} pages")
