import os
import requests
from PIL import Image, ImageDraw, ImageFont
import datetime

# ---- CONFIG ----
SERPAPI_KEY = os.environ["SERPAPI_KEY"]
SCHOLAR_ID = "DDRMDg4AAAAJ"
OUTPUT = "badge.png"

WIDTH, HEIGHT = 800, 200
BG_COLOR = (15, 15, 15)
TEXT_COLOR = (235, 235, 235)
ACCENT = (90, 180, 255)

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
img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

try:
    font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 52)
    font_small = ImageFont.truetype("DejaVuSans.ttf", 24)
except:
    font_big = font_small = ImageFont.load_default()

draw.text((30, 20), "Google Scholar", fill=ACCENT, font=font_small)

draw.text((30, 60), f"{citations}", fill=TEXT_COLOR, font=font_big)
draw.text((30, 120), "Citations", fill=TEXT_COLOR, font=font_small)

draw.text((300, 60), f"{hindex}", fill=TEXT_COLOR, font=font_big)
draw.text((300, 120), "h-index", fill=TEXT_COLOR, font=font_small)

draw.text((520, 60), f"{i10}", fill=TEXT_COLOR, font=font_big)
draw.text((520, 120), "i10-index", fill=TEXT_COLOR, font=font_small)

timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d")
draw.text((WIDTH - 200, HEIGHT - 30), f"Updated {timestamp}", fill=(140,140,140), font=font_small)

img.save(OUTPUT)
