import os
import json
from datetime import date

# =========================
# SITE CONFIG (FIXED)
# =========================
SITE_URL = "https://yosintv2.github.io/rmynet"
OUTPUT_DIR = "output"

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

CURRENT_YEAR = date.today().year
END_YEAR = CURRENT_YEAR + 5  # safe growth

# =========================
# ENSURE OUTPUT DIR
# =========================
os.makedirs(OUTPUT_DIR, exist_ok=True)
print("✅ Output directory ready")

# =========================
# LOAD FAQ (SAFE)
# =========================
FAQS = []
try:
    with open("data/faq.json", "r", encoding="utf-8") as f:
        FAQS = json.load(f)
    print("✅ FAQ loaded")
except Exception as e:
    print("⚠️ FAQ not loaded:", e)

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
# PAGE GENERATOR
# =========================
def generate_page(month, year):
    slug = f"weight-loss-plan-{month.lower()}-{year}.html"
    filepath = f"{OUTPUT_DIR}/{slug}"
    canonical = f"{SITE_URL}/{slug}"
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
            "name": faq.get("question", ""),
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq.get("answer", "")
            }
        })

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="canonical" href="{canonical}">

<script type="application/ld+json">
{json.dumps({
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": title,
    "url": canonical
}, indent=2)}
</script>

<script type="application/ld+json">
{json.dumps(faq_schema, indent=2)}
</script>
</head>

<body>
<header>
  <h1>{month} {year} Weight Loss Plan</h1>
  <p>Season: {season} • Updated {year}</p>
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
      <li>Strength training – 3× per week</li>
      <li>Stretching & recovery</li>
    </ul>
  </section>

  <section>
    <h2>Frequently Asked Questions</h2>
    <ul>
"""

    for faq in FAQS:
        html += f"<li><strong>{faq.get('question','')}</strong><br>{faq.get('answer','')}</li>"

    html += """
    </ul>
  </section>

  <p><em>Disclaimer: This content is informational only. Consult a healthcare professional before starting any program.</em></p>
</main>

<footer>
  <p>© ReduceMyWeight</p>
  <p><a href="../index.html">Home</a> | <a href="../sitemap.xml">Sitemap</a></p>
</footer>
</body>
</html>
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"📝 Generated: {filepath}")

# =========================
# BUILD ALL PAGES
# =========================
print("🚀 Build started")
count = 0

for year in range(CURRENT_YEAR, END_YEAR + 1):
    for month in MONTHS:
        generate_page(month, year)
        count += 1

print(f"✅ Build finished — {count} pages created")
