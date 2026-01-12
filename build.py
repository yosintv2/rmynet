from datetime import datetime
import calendar

SITE_URL = "https://www.reducemyweight.net"

START_YEAR = 2025
END_YEAR = 2035  # unlimited future (change anytime)

def write_file(name, content):
    with open(name, "w", encoding="utf-8") as f:
        f.write(content)

# ---------------- HOME PAGE ----------------
index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Reduce My Weight – Monthly Weight Loss Plans</title>
<meta name="description" content="Monthly weight loss plans, diet guides, and fitness tips updated automatically.">
<link rel="canonical" href="{SITE_URL}/">
</head>
<body>
<h1>Reduce My Weight</h1>
<p>Automated monthly weight loss plans.</p>

<ul>
"""

pages = []

for year in range(START_YEAR, END_YEAR + 1):
    for month in range(1, 13):
        month_name = calendar.month_name[month].lower()
        filename = f"weight-loss-plan-{month_name}-{year}.html"
        url = f"{SITE_URL}/{filename}"
        pages.append((filename, url))

        index_html += f'<li><a href="{filename}">{month_name.title()} {year} Weight Loss Plan</a></li>\n'

index_html += """
</ul>
</body>
</html>
"""

write_file("index.html", index_html)

# ---------------- MONTHLY PAGES ----------------
for filename, url in pages:
    title = filename.replace("-", " ").replace(".html", "").title()

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<meta name="description" content="{title} with diet plan, workout routine, and fat loss tips.">
<link rel="canonical" href="{url}">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "author": {{
    "@type": "Organization",
    "name": "Reduce My Weight"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "Reduce My Weight"
  }},
  "mainEntityOfPage": "{url}"
}}
</script>
</head>
<body>
<h1>{title}</h1>

<h2>Diet Plan</h2>
<p>High-protein, calorie-controlled meals.</p>

<h2>Workout Plan</h2>
<p>Cardio + strength training routine.</p>

<h2>FAQ</h2>
<h3>Is this plan safe?</h3>
<p>Yes, it follows healthy weight loss guidelines.</p>

</body>
</html>
"""
    write_file(filename, html)

# ---------------- SITEMAP ----------------
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap += '<urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">\n'

sitemap += f"""<url>
  <loc>{SITE_URL}/</loc>
</url>
"""

for _, url in pages:
    sitemap += f"""<url>
  <loc>{url}</loc>
</url>
"""

sitemap += '</urlset>'

write_file("sitemap.xml", sitemap)
