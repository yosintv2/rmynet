import os
import json
from datetime import date

# =========================
# BASIC CONFIG
# =========================
SITE_URL = "https://reducemyweight.net"
OUTPUT_DIR = "output"

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

CURRENT_YEAR = date.today().year
END_YEAR = CURRENT_YEAR + 5   # increase later safely

# =========================
# ENSURE OUTPUT DIRECTORY
# =========================
os.makedirs(OUTPUT_DIR, exist_ok=True)
print("✅ Output directory ready")

# =========================
# LOAD FAQ DATA (SAFE)
# =========================
FAQS = []
try:
    with open("data/faq.json", "r", encoding="utf-8") as f:
        FAQS = json.load(f)
    print("✅ FAQ data loaded")
except FileNotFoundError:
    print("⚠️ data/faq.json not found — continuing without FAQs")

# =========================
# SEASON LOGIC
# =========================
def get_season(month):
    if month in ["December", "January", "February"]:
        return "Winter"
    elif month in ["March", "April", "May"]:
        return "Spring"
    elif month in ["June", "July", "August"]:
        return "Summer"
    return "Autumn"

# =========================
# HTML PAGE GENERATOR
# =========================
def generate_page(month, year):
    slug = f"weight-loss-plan-{month.lower()}-{year}"
    filename = f"{OUTPUT_DIR}/{slug}.html"
    url = f"{SITE_URL}/{slug}.html"
    season = get_season(month)

    title = f"{month} {year} Weight Loss Plan – Diet, Calories & Workout"
    description = f"Follow the best {month} {year} weight loss plan with calorie targets, diet tips, and workouts optimized for {season}."

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": []
    }

    for faq in FAQS:
        faq_schema["mainEntity"].append({
            "@type": "Question",
            "name": faq["question"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["answer"]
            }
        })

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="canonical" href="{url}">

<script type="application/ld+json">
{json.dumps({
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": title,
    "url": url
}, indent=2)}
</script>

<script type="application/ld+json">
{json.dumps(faq_schema, indent=2)}
</script>
</head>

<body>
<header>
  <h1>{month} {year} Weight Loss Plan</h1>
  <p>Optimized for {season} • Updated {year}</p>
</header>

<main>
  <section>
    <h2>Daily Calorie Target</h2>
    <p>A daily calorie deficit of <strong>500–700 calories</strong> can help you lose weight safely this month.</p>
  </section>

  <section>
    <h2>Recommended Diet</h2>
    <ul>
      <li>High-protein meals</li>
      <li>Seasonal vegetables</li>
      <li>Controlled rice portions</li>
    </ul>
  </section>

  <section>
    <h2>Workout Plan</h2>
    <ul>
      <li>Walking – 30 minutes daily</li>
      <li>Strength training – 3x per week</li>
      <li>Stretching & recovery</li>
    </ul>
  </section>

  <section>
    <h2>FAQs</h2>
    <ul>
"""

    for faq in FAQS:
        html += f"<li><strong>{faq['question']}</strong><br>{faq['answer']}</li>"

    html += """
    </ul>
  </section>

  <p><em>Disclaimer: This content is for informational purposes only. Consult a healthcare professional.</em></p>
</main>

<footer>
  <p>© ReduceMyWeight.net</p>
</footer>
</body>
</html>
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"📝 Generated: {filename}")

# =========================
# BUILD ALL PAGES
# =========================
page_count = 0

print("🚀 Build started")

for year in range(CURRENT_YEAR, END_YEAR + 1):
    for month in MONTHS:
        generate_page(month, year)
        page_count += 1

print(f"✅ Build finished — {page_count} HTML pages generated")
