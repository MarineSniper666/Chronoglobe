"""
Open Graph card image + share HTML generator.
Renders a 1200x630 PNG per event for beautiful social previews.
"""
import html as _html
from io import BytesIO
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pathlib import Path

CAT_COLORS = {
    "civilizations": (212, 175, 55),  # gold
    "land":          (107, 142, 35),  # olive
    "pandemics":     (139, 0, 0),     # blood
    "technology":    (70, 130, 180),  # steel
}
CAT_LABELS = {
    "civilizations": "CIVILIZATIONS",
    "land":          "LAND TRANSFORMATION",
    "pandemics":     "PANDEMIC",
    "technology":    "TECHNOLOGY",
}


def _fmt_year(y: int) -> str:
    if y < 0:
        return f"{abs(y):,} BCE"
    return f"{y} CE"


def _load_font(size: int, bold: bool = False):
    # Try common system fonts; fallback to PIL default.
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _wrap(text: str, font, max_w: int, draw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        candidate = f"{cur} {w}".strip()
        bbox = draw.textbbox((0, 0), candidate, font=font)
        if bbox[2] - bbox[0] > max_w and cur:
            lines.append(cur)
            cur = w
        else:
            cur = candidate
    if cur:
        lines.append(cur)
    return lines


def render_og_card(event: dict) -> bytes:
    W, H = 1200, 630
    color = CAT_COLORS.get(event.get("category"), (212, 175, 55))
    label = CAT_LABELS.get(event.get("category"), "MOMENT")

    # Base dark canvas
    img = Image.new("RGB", (W, H), (3, 3, 4))
    draw = ImageDraw.Draw(img)

    # Radial-ish glow from the category color in the top-right
    glow = Image.new("RGB", (W, H), (3, 3, 4))
    g_draw = ImageDraw.Draw(glow)
    for r, alpha in [(520, 55), (360, 90), (220, 130), (110, 160)]:
        cx, cy = int(W * 0.78), int(H * 0.15)
        g_draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                       fill=(color[0] * alpha // 255,
                             color[1] * alpha // 255,
                             color[2] * alpha // 255))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    img = Image.blend(img, glow, 0.55)
    draw = ImageDraw.Draw(img)

    # Subtle grid of "stars"
    import random
    random.seed(event.get("id", "seed"))
    for _ in range(160):
        x = random.randint(0, W - 1)
        y = random.randint(0, H - 1)
        b = random.randint(80, 220)
        draw.ellipse([x, y, x + 1, y + 1], fill=(b, b, b))

    # Top brand row
    brand_font = _load_font(22, bold=True)
    tag_font = _load_font(20, bold=True)
    draw.text((60, 50), "CHRONOGLOBE", font=brand_font, fill=(212, 175, 55))
    draw.text((60, 82), "A WORLD HISTORY ATLAS", font=_load_font(14),
              fill=(255, 255, 255, 120))

    # Category tag pill
    tag_text = label
    tb = draw.textbbox((0, 0), tag_text, font=tag_font)
    pad_x, pad_y = 18, 10
    tag_w = tb[2] - tb[0] + pad_x * 2
    tag_h = tb[3] - tb[1] + pad_y * 2
    tx, ty = 60, 210
    draw.rounded_rectangle([tx, ty, tx + tag_w, ty + tag_h],
                           radius=tag_h // 2,
                           outline=color, width=2)
    # Small dot
    dot_r = 5
    draw.ellipse([tx + 14, ty + tag_h // 2 - dot_r,
                  tx + 14 + dot_r * 2, ty + tag_h // 2 + dot_r],
                 fill=color)
    draw.text((tx + 32, ty + pad_y - 2), tag_text, font=tag_font, fill=color)

    # Title
    title = event.get("title", "Untitled")
    title_font = _load_font(64, bold=True)
    max_w = W - 120
    lines = _wrap(title, title_font, max_w, draw)
    y = 275
    for line in lines[:3]:
        draw.text((60, y), line, font=title_font, fill=(247, 245, 240))
        y += 72

    # Year
    year_font = _load_font(52, bold=True)
    year_str = _fmt_year(event.get("year", 0))
    draw.text((60, y + 20), year_str, font=year_font, fill=color)

    # Region
    region = event.get("region", "")
    if region:
        rgn_font = _load_font(22)
        draw.text((60, y + 92), region.upper(),
                  font=rgn_font, fill=(255, 255, 255, 160))

    # Bottom bar
    draw.rectangle([0, H - 60, W, H], fill=(15, 15, 18))
    draw.text((60, H - 42),
              "chronoglobe.app  ·  Explore 25,000 years of history",
              font=_load_font(18), fill=(255, 255, 255, 140))

    buf = BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def render_share_html(event: dict, year: int, base_url: str, api_url: str, request_url: str) -> str:
    """Return an HTML page for social crawlers containing OG tags."""
    title = _html.escape(event.get("title", "A moment in history"))
    desc_raw = event.get("summary", "")
    if len(desc_raw) > 200:
        desc_raw = desc_raw[:197] + "…"
    desc = _html.escape(desc_raw)
    year_str = _fmt_year(year)
    og_image = f"{api_url}/api/og?event={event['id']}"
    dest = f"{base_url}/?year={year}&event={event['id']}"
    region = _html.escape(event.get('region', ''))

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title} · {year_str} · Chronoglobe</title>
<meta name="description" content="{desc}">

<meta property="og:type" content="article">
<meta property="og:title" content="{title} · {year_str}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{request_url}">
<meta property="og:site_name" content="Chronoglobe">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title} · {year_str}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_image}">

<meta http-equiv="refresh" content="0; url={dest}">
<link rel="canonical" href="{dest}">
<style>
  html,body {{ background:#030304; color:#F7F5F0; margin:0; height:100%; }}
  body {{ display:flex; flex-direction:column; align-items:center; justify-content:center;
          font-family: Georgia, serif; padding:2rem; text-align:center; }}
  a {{ color:#D4AF37; }}
  .k {{ font-family: monospace; color:#888; font-size:.85rem; letter-spacing:.2em; text-transform:uppercase; margin-bottom:1rem; }}
  h1 {{ font-size:2rem; margin:.4rem 0; }}
  .y {{ color:#D4AF37; font-family: monospace; }}
  .cta {{ margin-top:1.5rem; font-size:.95rem; opacity:.7; }}
</style>
</head>
<body>
  <div class="k">Chronoglobe · A World History Atlas</div>
  <h1>{title}</h1>
  <div class="y">{year_str} · {region}</div>
  <p style="max-width:640px;opacity:.75;">{desc}</p>
  <div class="cta">
    Redirecting to the interactive globe… <a href="{dest}">Continue &rarr;</a>
  </div>
</body>
</html>"""
