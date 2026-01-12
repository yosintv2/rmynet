import os
import json
from datetime import date

# =========================
# SITE CONFIG
# =========================
SITE_URL = "https://yosintv2.github.io/rmynet"
OUTPUT_DIR = "output"

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

CURRENT_YEAR = date.today().year
END_YEAR = CURRENT_YEAR + 5

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# LOAD FAQ
# =========================
FAQS = []
try:
    with open("data/faq.json", "r", encoding="utf-8") as f:
        FAQS = json.load(f)
    print("✅ FAQ data loaded")
except:
    print("⚠️ No FAQ file found")

# =========================
# PAGE STORAGE
# =========================
ALL_PAGES = []

# =========================
# PAGE GENERATOR
# =========================
def generate_page(month, year):
    slug = f"weight-loss-plan-{month.lower()}-{year}.html"
    filepath = f"{OUTPUT_DIR}/{slug}"
    canonical = f"{SITE_URL}/{slug}"

    ALL_PAGES.append({
        "month": month,
        "year": year,
        "slug": slug
    })

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{month} {year} Weight Loss Plan</title>
<meta name="description" content="Best {month} {year} weight loss plan with diet, calories and workouts.">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="canonical" href="{canonical}">
</head>

<body class="bg-gray-100 text-gray-900">
<div class="max-w-3xl mx-auto p-6">

<nav class="mb-6">
  <a href="../index.html" class="text-blue-600 font-semibold">← Home</a>
</nav>

<h1 class="text-3xl font-bold mb-4">{month} {year} Weight Loss Plan</h1>

<p class="mb-4">A safe and effective weight loss plan for {month} {year}.</p>

<h2 class="text-xl font-semibold mt-6 mb-2">Diet</h2>
<ul class="list-disc ml-6">
  <li>High protein meals</li>
  <li>Seasonal vegetables</li>
  <li>Low sugar intake</li>
</ul>

<h2 class="text-xl font-semibold mt-6 mb-2">Workout</h2>
<ul class="list-disc ml-6">
  <li>Walking – 30 minutes daily</li>
  <li>Strength training – 3× weekly</li>
</ul>

<footer class="mt-10 text-sm text-gray-600">
  © ReduceMyWeight
</footer>

</div>
</body>
</html>
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"📝 Generated: {filepath}")

# =========================
# INDEX PAGE GENERATOR
# =========================
def generate_index():
    pages_by_year = {}
    for p in ALL_PAGES:
        pages_by_year.setdefault(p["year"], []).append(p)

    content = ""

    for year in sorted(pages_by_year.keys(), reverse=True):
        content += f"""
        <section class="mb-10">
          <h2 class="text-2xl font-bold mb-4">{year}</h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        """
        for p in pages_by_year[year]:
            content += f"""
            <a href="output/{p['slug']}" class="block bg-white p-4 rounded shadow hover:shadow-lg transition">
              <h3 class="font-semibold">{p['month']} {p['year']} Weight Loss Plan</h3>
            </a>
            """
        content += "</div></section>"

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Reduce My Weight – Monthly Plans</title>
<meta name="description" content="Monthly weight loss plans by year with diet and workouts.">
<meta name="viewport" content="width=device-width, initial-scale=1">

<script src="https://cdn.tailwindcss.com"></script>
</head>

<body class="bg-gray-100 text-gray-900">
<div class="max-w-5xl mx-auto p-6">

<header class="mb-10">
  <h1 class="text-4xl font-bold mb-2">Reduce My Weight</h1>
  <p class="text-gray-700">Monthly Weight Loss Plans (Auto Generated)</p>

  <nav class="mt-4 space-x-4">
    <a href="index.html" class="text-blue-600 font-semibold">Home</a>
    <a href="sitemap.xml" class="text-blue-600">Sitemap</a>
  </nav>
</header>

{content}

<footer class="mt-10 text-sm text-gray-600">
  © ReduceMyWeight
</footer>

</div>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

    print("🏠 index.html generated")

# =========================
# BUILD PROCESS
# =========================
print("🚀 Build started")

for year in range(CURRENT_YEAR, END_YEAR + 1):
    for month in MONTHS:
        generate_page(month, year)

generate_index()

print(f"✅ Build finished — {len(ALL_PAGES)} pages created")
