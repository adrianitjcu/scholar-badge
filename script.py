from scholarly import scholarly
from PIL import Image, ImageDraw, ImageFont
import datetime

# ---- CONFIG ----
SCHOLAR_ID = "DDRMDg4AAAAJ"
OUTPUT = "badge.png"

WIDTH, HEIGHT = 800, 200
BG_COLOR = (15, 15, 15)
TEXT_COLOR = (235, 235, 235)
ACCENT = (90, 180, 255)

# ---- FETCH DATA ----
author = scholarly.search_author_id(SCHOLAR_ID)
author = scholarly.fill(author)

citations = author.get("citedby", 0)
hindex = author.get("hindex", 0)
i10 = author.get("i10index", 0)

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

timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
draw.text((WIDTH - 200, HEIGHT - 30), f"Updated {timestamp}", fill=(140,140,140), font=font_small)

img.save(OUTPUT)
