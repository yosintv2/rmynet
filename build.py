from datetime import date

SITE_URL = "https://www.reducemyweight.net"

MONTHS = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

START_YEAR = date.today().year
END_YEAR = START_YEAR + 5

PAGES = []

# =========================
# PAGE GENERATOR
# =========================
def generate_page(month, year):
    slug = f"weight-loss-plan-{month.lower()}-{year}.html"
    PAGES.append(slug)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{month} {year} Weight Loss Plan</title>
<meta name="description" content="Safe and effective weight loss plan for {month} {year}.">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="canonical" href="{SITE_URL}/{slug}">
</head>

<body style="font-family: Arial, sans-serif; background:#f3f4f6; color:#111;">
<div style="max-width:900px;margin:auto;padding:24px;background:#fff;">

<nav style="margin-bottom:20px;">
<a href="/" style="color:#2563eb;font-weight:bold;">← Home</a>
</nav>

<h1 style="font-size:32px;margin-bottom:16px;">
{month} {year} Weight Loss Plan
</h1>

<p>
This monthly plan helps you lose weight safely using calorie control,
balanced diet, and daily movement.
</p>

<h2>Diet Guidelines</h2>
<ul>
<li>High protein meals</li>
<li>Seasonal vegetables</li>
<li>Reduced sugar intake</li>
</ul>

<h2>Workout Guidelines</h2>
<ul>
<li>Walking 30 minutes daily</li>
<li>Strength training 3× weekly</li>
</ul>

<footer style="margin-top:40px;font-size:14px;color:#555;">
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
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Reduce My Weight</title>
<meta name="description" content="Monthly automated weight loss plans.">
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>

<body style="font-family:Arial;background:#f3f4f6;">
<div style="max-width:1000px;margin:auto;padding:24px;background:#fff;">

<h1 style="font-size:36px;">Reduce My Weight</h1>
<p>Monthly weight loss plans by year</p>

<hr>
"""

    current_year = None
    for slug in sorted(PAGES, reverse=True):
        year = slug.split("-")[-1].replace(".html","")
        if year != current_year:
            html += f"<h2 style='margin-top:24px;'>{year}</h2>"
            current_year = year

        html += f"""
        <p>
        <a href="/{slug}" style="color:#2563eb;">
        {slug.replace('-', ' ').replace('.html','').title()}
        </a>
        </p>
        """

    html += """
<footer style="margin-top:40px;font-size:14px;color:#555;">
© ReduceMyWeight
</footer>

</div>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("🏠 index.html generated")

# =========================
# SITEMAP GENERATOR
# =========================
def generate_sitemap():
    urls = [f"{SITE_URL}/{slug}" for slug in PAGES]
    urls.append(SITE_URL + "/")

    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for url in urls:
        sitemap += f"""
<url>
  <loc>{url}</loc>
  <changefreq>monthly</changefreq>
  <priority>0.8</priority>
</url>
"""

    sitemap += "</urlset>"

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap)

    print("🧭 sitemap.xml generated")

# =========================
# BUILD
# =========================
print("🚀 Build started")

for year in range(START_YEAR, END_YEAR + 1):
    for month in MONTHS:
        generate_page(month, year)

generate_index()
generate_sitemap()

print(f"✅ Build finished — {len(PAGES)} pages")
