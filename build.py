import os
import json
from datetime import date

SITE_URL = "https://reducemyweight.net"
OUTPUT_DIR = "output"

MONTHS = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

CURRENT_YEAR = date.today().year
END_YEAR = CURRENT_YEAR + 50  # unlimited scaling

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------- LOAD FAQ DATA ----------
with open("data/faq.json", "r", encoding="utf-8") as f:
    FAQS = json.load(f)

# ---------- SEASON LOGIC ----------
def get_season(month):
    if month in ["December", "January", "February"]:
        return "Winter"
    elif month in ["March", "April", "May"]:
        return "Spring"
    elif month in ["June", "July", "August"]:
        return "Summer"
    else:
        return "Autumn"

# ---------- SCHEMA GENERATORS ----------
def faq_schema(faqs):
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": []
    }

    for faq in faqs:
        schema["mainEntity"].append({
            "@type": "Question",
            "name": faq["question"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["answer"]
            }
        })
    return json.dumps(schema, indent=2)

def webpage_schema(title, url):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "url": url
    }, indent=2)

# ---------- PAGE BUILDER ----------
def build_page(month, year):
    slug = f"weight-loss-plan-{month.lower()}-{year}"
    url = f"{SITE_URL}/{slug}.html"
    season = get_season(month)

    title = f"{month} {year} Weight Loss Plan – Diet, Calories & Workout"
    description = f"Follow the best {month} {year} weight loss plan with calorie targets, diet tips, workouts, and fat loss strategies updated for this month."

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="canonical" href="{url}">

<script type="application/ld+json">
{webpage_schema(title, url)}
</script>

<script type="application/ld+json">
{faq_schema(FAQS)}
</script>

</head>
<body>

<h1>{month} {year} Weight Loss Plan</h1>

<p>This <strong>{month} {year}</strong> weight loss plan is optimized for the <strong>{season}</strong> season and focuses on safe, sustainable fat loss.</p>

<h2>Daily Calorie Target</h2>
<p>A healthy calorie deficit of <strong>500–700 calories per day</strong> can help you lose 2–3 kg safely this month.</p>

<h2>Recommended Diet for {month}</h2>
<ul>
  <li>High protein meals</li>
  <li>Seasonal vegetables</li>
  <li>Controlled rice portions</li>
</ul>

<h2>Workout Plan</h2>
<ul>
  <li>Walking – 30 minutes daily</li>
  <li>Bodyweight workouts – 3x/week</li>
  <li>Stretching and recovery</li>
</ul>

<h2>Frequently Asked Questions</h2>
<ul>
"""
    for faq in FAQS:
        html += f"<li><strong>{faq['question']}</strong><br>{faq['answer']}</li>"

    html += """
</ul>

<p><em>Disclaimer: This plan provides estimates only. Consult a healthcare professional before starting any weight loss program.</em></p>

</body>
</html>
"""

    with open(f"{OUTPUT_DIR}/{slug}.html", "w", encoding="utf-8") as f:
        f.write(html)

# ---------- RUN GENERATOR ----------
for year in range(CURRENT_YEAR, END_YEAR):
    for month in MONTHS:
        build_page(month, year)

print("✅ Unlimited SEO pages generated successfully.")
