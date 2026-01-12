import os
from datetime import date

# =========================
# CONFIG
# =========================
SITE_URL = "https://www.reducemyweight.net"

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

START_YEAR = date.today().year
END_YEAR = START_YEAR + 5

ALL_PAGES = []

# =========================
# PAGE GENERATOR
# =========================
def generate_page(month, year):
    slug = f"weight-loss-plan-{month.lower()}-{year}.html"

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
<meta name="description" content="Best weight loss plan for {month} {year}.">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="canonical" href="{SITE_URL}/{slug}">
<script src="https://cdn.tailwindcss.com"></script>
</head>

<body class="bg-gray-100 text-gray-900">
<div class="max-w-3xl mx-auto p-6">

<nav class="mb-6">
  <a href="/" class="text-blue-600 font-semibold">← Home</a>
</nav>

<h1 class="text-3xl font-bold mb-4">{month} {year} Weight Loss Plan</h1>

<p class="mb-4">
This monthly plan helps you lose weight safely using diet control and workouts.
</p>

<h2 class="text-xl font-semibold mt-6">Diet Plan</h2>
<ul class="list-disc ml-6">
  <li>High-protein foods</li>
  <li>Low sugar intake</li>
  <li>Seasonal vegetables</li>
</ul>

<h2 class="text-xl font-semibold mt-6">Workout Plan</h2>
<ul class="list-disc ml-6">
  <li>Walking – 30 minutes daily</li>
  <li>Strength training – 3× per week</li>
</ul>

<footer class="mt-10 text-sm text-gray-500">
© ReduceMyWeight
</footer>

</div>
</body>
</html>
"""

    with open(slug, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"📝 Generated: {slug}")

# =========================
# INDEX PAGE
# =========================
def generate_index():
    pages_by_year = {}

    for p in ALL_PAGES:
        pages_by_year.setdefault(p["year"], []).append(p)

    listing = ""
    for year in sorted(pages_by_year.keys(), reverse=True):
        listing += f"<h2 class='text-2xl font-bold mt-8'>{year}</h2>"
        listing += "<div class='grid sm:grid-cols-2 gap-4 mt-4'>"

        for p in pages_by_year[year]:
            listing += f"""
            <a href="/{p['slug']}" class="block bg-white p-4 rounded shadow hover:shadow-lg transition">
              <h3 class="font-semibold">{p['month']} {p['year']} Weight Loss Plan</h3>
            </a>
            """

        listing += "</div>"

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Reduce My Weight</title>
<meta name="description" content="Automated monthly weight loss plans.">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://cdn.tailwindcss.com"></script>
</head>

<body class="bg-gray-100 text-gray-900">
<div class="max-w-5xl mx-auto p-6">

<header class="mb-10">
  <h1 class="text-4xl font-bold">Reduce My Weight</h1>
  <p class="text-gray-600">Monthly Weight Loss Plans</p>

  <nav class="mt-4 space-x-4">
    <a href="/" class="text-blue-600 font-semibold">Home</a>
  </nav>
</header>

{listing}

<footer class="mt-12 text-sm text-gray-500">
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
# BUILD
# =========================
print("🚀 Build started")

for year in range(START_YEAR, END_YEAR + 1):
    for month in MONTHS:
        generate_page(month, year)

generate_index()

print(f"✅ Build finished — {len(ALL_PAGES)} pages created")
