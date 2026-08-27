"""Tests for Chronoglobe snapshot cards: /api/og PNG + /api/share HTML, plus regressions."""
import os
import re

import pytest
import requests
from dotenv import dotenv_values

frontend_env = dotenv_values("/app/frontend/.env")
base_url = os.environ.get("REACT_APP_BACKEND_URL") or frontend_env.get("REACT_APP_BACKEND_URL")
if not base_url:
    raise RuntimeError("REACT_APP_BACKEND_URL missing")
BASE_URL = base_url.rstrip("/")


@pytest.fixture(scope="module")
def s():
    sess = requests.Session()
    return sess


# ---- /api/og PNG generation ----
class TestOgCard:
    def test_og_valid_event(self, s):
        r = s.get(f"{BASE_URL}/api/og", params={"event": "pan-blackdeath"}, timeout=60)
        assert r.status_code == 200, f"{r.status_code} {r.text[:300]}"
        assert r.headers.get("content-type", "").startswith("image/png")
        assert len(r.content) > 10_000, f"png too small: {len(r.content)}"
        assert r.content[:8] == b"\x89PNG\r\n\x1a\n", "not a valid PNG signature"

    def test_og_dimensions(self, s):
        r = s.get(f"{BASE_URL}/api/og", params={"event": "civ-mongol"}, timeout=60)
        assert r.status_code == 200
        # PNG IHDR: width/height big-endian at bytes 16..24
        w = int.from_bytes(r.content[16:20], "big")
        h = int.from_bytes(r.content[20:24], "big")
        assert (w, h) == (1200, 630), f"got {w}x{h}"

    def test_og_invalid_event_404(self, s):
        r = s.get(f"{BASE_URL}/api/og", params={"event": "invalid"}, timeout=30)
        assert r.status_code == 404, f"{r.status_code} {r.text[:200]}"

    def test_og_missing_param_422(self, s):
        r = s.get(f"{BASE_URL}/api/og", timeout=30)
        assert r.status_code == 422

    def test_og_cache_header(self, s):
        # NOTE: app sets Cache-Control: public, max-age=86400 but the preview
        # ingress overrides it with no-store. Only assert the response is OK.
        r = s.get(f"{BASE_URL}/api/og", params={"event": "tech-web"}, timeout=60)
        assert r.status_code == 200
        assert r.headers.get("content-type", "").startswith("image/png")


# ---- /api/share HTML with OG meta tags ----
class TestShareHtml:
    def test_share_meta_tags(self, s):
        r = s.get(f"{BASE_URL}/api/share",
                  params={"event": "pan-blackdeath", "year": 1347}, timeout=30)
        assert r.status_code == 200, f"{r.status_code} {r.text[:300]}"
        assert "text/html" in r.headers.get("content-type", "")
        html = r.text
        for needle in ['property="og:title"', 'property="og:description"',
                       'property="og:image"', 'name="twitter:card"',
                       'property="og:url"', 'property="og:image:width"']:
            assert needle in html, f"missing {needle}"
        assert 'content="summary_large_image"' in html
        # og:image points at the /api/og endpoint for this event
        m = re.search(r'property="og:image" content="([^"]+)"', html)
        assert m and "/api/og?event=pan-blackdeath" in m.group(1), m.group(1) if m else "no og:image"

    def test_share_redirect_to_spa(self, s):
        r = s.get(f"{BASE_URL}/api/share",
                  params={"event": "pan-blackdeath", "year": 1347}, timeout=30)
        html = r.text
        m = re.search(r'http-equiv="refresh" content="0; url=([^"]+)"', html)
        assert m, "missing http-equiv refresh redirect"
        dest = m.group(1)
        assert "year=1347" in dest and "event=pan-blackdeath" in dest, dest
        assert "/api/" not in dest, f"redirect should target SPA, got {dest}"

    def test_share_og_urls_use_public_host(self, s):
        """og:image / redirect must use the public host, not the internal cluster host."""
        r = s.get(f"{BASE_URL}/api/share", params={"event": "civ-mongol"}, timeout=30)
        html = r.text
        img = re.search(r'property="og:image" content="([^"]+)"', html).group(1)
        dest = re.search(r'http-equiv="refresh" content="0; url=([^"]+)"', html).group(1)
        assert img.startswith("https://"), f"og:image not https: {img}"
        assert "cluster" not in img and "emergentcf.cloud" not in img, f"internal host leaked: {img}"
        assert "cluster" not in dest and "emergentcf.cloud" not in dest, f"internal host leaked: {dest}"

    def test_share_og_image_url_fetchable(self, s):
        r = s.get(f"{BASE_URL}/api/share", params={"event": "civ-mongol"}, timeout=30)
        m = re.search(r'property="og:image" content="([^"]+)"', r.text)
        assert m
        img = s.get(m.group(1), timeout=60)
        assert img.status_code == 200 and img.headers["content-type"].startswith("image/png")

    def test_share_without_year_uses_event_year(self, s):
        r = s.get(f"{BASE_URL}/api/share", params={"event": "pan-blackdeath"}, timeout=30)
        assert r.status_code == 200
        assert "1347" in r.text or re.search(r"year=\-?\d+", r.text)

    def test_share_urls_exactly_match_public_origin(self, s):
        """og:image / og:url / canonical / meta-refresh must use exactly BASE_URL."""
        r = s.get(f"{BASE_URL}/api/share",
                  params={"event": "tech-gutenberg", "year": 1440}, timeout=30)
        assert r.status_code == 200
        html = r.text
        img = re.search(r'property="og:image" content="([^"]+)"', html).group(1)
        dest = re.search(r'http-equiv="refresh" content="0; url=([^"]+)"', html).group(1)
        canon = re.search(r'rel="canonical" href="([^"]+)"', html).group(1)
        ogurl = re.search(r'property="og:url" content="([^"]+)"', html).group(1)
        assert img == f"{BASE_URL}/api/og?event=tech-gutenberg", img
        assert dest == f"{BASE_URL}/?year=1440&event=tech-gutenberg", dest
        assert canon == dest, canon
        assert ogurl.startswith(f"{BASE_URL}/api/share"), ogurl

    def test_share_html_escaping(self, s):
        """Titles/summary must be HTML-escaped inside meta attributes."""
        r = s.get(f"{BASE_URL}/api/share", params={"event": "civ-mongol"}, timeout=30)
        html = r.text
        m = re.search(r'<meta name="description" content="([^"]*)"', html)
        assert m, "description meta missing/broken by unescaped quote"
        # No raw unescaped double quote can appear inside attribute values
        assert '&quot;' in html or '"' not in m.group(1)

    def test_share_dest_loads_spa(self, s):
        """The redirect destination must return the SPA (200 HTML), not 403."""
        r = s.get(f"{BASE_URL}/api/share", params={"event": "civ-mongol"}, timeout=30)
        dest = re.search(r'http-equiv="refresh" content="0; url=([^"]+)"', r.text).group(1)
        page = s.get(dest, timeout=60)
        assert page.status_code == 200, f"{page.status_code} for {dest}"
        assert "text/html" in page.headers.get("content-type", "")
        assert "403" not in page.text[:400]

    def test_share_invalid_event_404(self, s):
        r = s.get(f"{BASE_URL}/api/share", params={"event": "invalid"}, timeout=30)
        assert r.status_code == 404


# ---- Regression on core endpoints ----
class TestRegression:
    def test_events(self, s):
        r = s.get(f"{BASE_URL}/api/events", timeout=30)
        assert r.status_code == 200
        d = r.json()
        assert d["count"] >= 60 and isinstance(d["events"], list)
        assert all("_id" not in e for e in d["events"]), "MongoDB _id leaked"

    def test_arcs(self, s):
        r = s.get(f"{BASE_URL}/api/arcs", timeout=30)
        assert r.status_code == 200
        arcs = r.json()["arcs"]
        assert len(arcs) == 11, f"expected 11 arcs, got {len(arcs)}"
        assert all("_id" not in a for a in arcs)

    def test_root(self, s):
        r = s.get(f"{BASE_URL}/api/", timeout=30)
        assert r.status_code == 200 and r.json()["events"] > 0

    def test_empires(self, s):
        r = s.get(f"{BASE_URL}/api/empires", timeout=30)
        assert r.status_code == 200 and len(r.json()["empires"]) >= 24

    def test_expand_streams(self, s):
        # /api/expand is an SSE stream (text/event-stream)
        r = s.post(f"{BASE_URL}/api/expand", json={"event_id": "pan-blackdeath"},
                   timeout=120, stream=True)
        assert r.status_code == 200, f"{r.status_code} {r.text[:300]}"
        assert "text/event-stream" in r.headers.get("content-type", "")
        chunks = []
        for line in r.iter_lines(decode_unicode=True):
            if line:
                chunks.append(line)
            if len(chunks) > 5:
                break
        r.close()
        assert chunks and any(c.startswith("data:") for c in chunks)

    def test_tts(self, s):
        r = s.post(f"{BASE_URL}/api/tts", json={"text": "A short test.", "voice": "onyx"}, timeout=90)
        assert r.status_code == 200, f"{r.status_code} {r.text[:300]}"
        assert r.headers.get("content-type", "").startswith("audio/mpeg")
        assert len(r.content) > 5_000
