import os
import requests
from PIL import Image, ImageDraw, ImageFont
import datetime

# ---- CONFIG ----
SERPAPI_KEY = os.environ["SERPAPI_KEY"]
SCHOLAR_ID = "DDRMDg4AAAAJ"
OUTPUT = "badge.png"

WIDTH, HEIGHT = 620, 200
TEXT_COLOR = (70, 70, 70, 255) 
SUBTLE_TEXT = (120, 120, 120, 255) 
ACCENT = (0, 158, 230, 255)        

# ---- FETCH DATA (SerpAPI) ----
params = {
    "engine": "google_scholar_author",
    "author_id": SCHOLAR_ID,
    "api_key": SERPAPI_KEY
}

resp = requests.get("https://serpapi.com/search.json", params=params, timeout=10)
resp.raise_for_status()
data = resp.json()

author = data.get("author", {})
cited_by = data.get("cited_by", {})
table = cited_by.get("table", [])

# citations
citations = table[0]["citations"]["all"] if len(table) > 0 and "citations" in table[0] else 0
# h-index
hindex = table[1]["h_index"]["all"] if len(table) > 1 and "h_index" in table[1] else 0
# i10-index
i10 = table[2]["i10_index"]["all"] if len(table) > 2 and "i10_index" in table[2] else 0

# ---- IMAGE ----
img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

try:
    font_title = ImageFont.truetype("fonts/Inter_18pt-Medium.ttf", 22)
    font_big   = ImageFont.truetype("fonts/Inter_18pt-Medium.ttf", 52)
    font_small = ImageFont.truetype("fonts/Inter_18pt-Medium.ttf", 18)

except:
    font_big = font_small = ImageFont.load_default()

draw.text((30, 20), "Google Scholar Metrics", fill=ACCENT, font=font_small)

draw.text((30, 60), f"{citations}", fill=TEXT_COLOR, font=font_big)
draw.text((30, 120), "Citations", fill=SUBTLE_TEXT, font=font_small)

draw.text((300, 60), f"{hindex}", fill=TEXT_COLOR, font=font_big)
draw.text((300, 120), "h-index", fill=SUBTLE_TEXT, font=font_small)

draw.text((520, 60), f"{i10}", fill=TEXT_COLOR, font=font_big)
draw.text((520, 120), "i10-index", fill=SUBTLE_TEXT, font=font_small)

timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
draw.text((WIDTH - 200, HEIGHT - 30), f"Updated {timestamp}", fill=(140,140,140), font=font_small)

img.save(OUTPUT, "PNG")
