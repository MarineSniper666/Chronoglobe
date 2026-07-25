"""Tests for Chronoglobe new features: /api/arcs, /api/empires, /api/tts."""
import os
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://temporal-atlas-2.preview.emergentagent.com").rstrip("/")


@pytest.fixture(scope="module")
def s():
    sess = requests.Session()
    sess.headers.update({"Content-Type": "application/json"})
    return sess


# ---- Arcs ----
class TestArcs:
    def test_arcs_shape(self, s):
        r = s.get(f"{BASE_URL}/api/arcs", timeout=30)
        assert r.status_code == 200
        data = r.json()
        assert "arcs" in data and isinstance(data["arcs"], list)
        assert len(data["arcs"]) >= 10, f"Expected ~11 arcs, got {len(data['arcs'])}"
        ids = {a["id"] for a in data["arcs"]}
        for expected in ["arc-beringia", "arc-silkroad-cn-rome", "arc-columbian-e"]:
            assert expected in ids, f"missing {expected}"
        # Field check on one
        b = next(a for a in data["arcs"] if a["id"] == "arc-beringia")
        for k in ["id", "label", "start_year", "end_year", "category",
                  "start_lat", "start_lng", "end_lat", "end_lng", "color"]:
            assert k in b, f"arc-beringia missing {k}"


# ---- Empires ----
class TestEmpires:
    def test_empires_shape(self, s):
        r = s.get(f"{BASE_URL}/api/empires", timeout=30)
        assert r.status_code == 200
        data = r.json()
        assert "empires" in data and isinstance(data["empires"], list)
        assert len(data["empires"]) >= 18, f"Expected ~19, got {len(data['empires'])}"
        ids = {e["id"] for e in data["empires"]}
        for expected in ["emp-rome-emp", "emp-caliph", "emp-mongol", "emp-british"]:
            assert expected in ids, f"missing {expected}"
        cal = next(e for e in data["empires"] if e["id"] == "emp-caliph")
        for k in ["id", "name", "start_year", "end_year", "countries", "color"]:
            assert k in cal
        assert isinstance(cal["countries"], list) and len(cal["countries"]) > 0


# ---- TTS ----
class TestTTS:
    def test_tts_valid(self, s):
        r = s.post(
            f"{BASE_URL}/api/tts",
            json={"text": "The Roman Empire endured for centuries.", "voice": "onyx"},
            timeout=60,
        )
        assert r.status_code == 200, f"status={r.status_code} body={r.text[:300]}"
        assert r.headers.get("content-type", "").startswith("audio/mpeg")
        assert len(r.content) > 10_000, f"audio too small: {len(r.content)} bytes"

    def test_tts_empty_text(self, s):
        r = s.post(f"{BASE_URL}/api/tts", json={"text": "", "voice": "onyx"}, timeout=30)
        assert r.status_code == 400

    def test_tts_whitespace_text(self, s):
        r = s.post(f"{BASE_URL}/api/tts", json={"text": "   ", "voice": "onyx"}, timeout=30)
        assert r.status_code == 400

    def test_tts_invalid_voice_falls_back(self, s):
        r = s.post(
            f"{BASE_URL}/api/tts",
            json={"text": "Testing invalid voice fallback.", "voice": "not-a-voice"},
            timeout=60,
        )
        assert r.status_code == 200, f"status={r.status_code} body={r.text[:300]}"
        assert r.headers.get("content-type", "").startswith("audio/mpeg")
        assert len(r.content) > 5_000


# ---- Regression: original endpoints ----
class TestRegression:
    def test_root(self, s):
        r = s.get(f"{BASE_URL}/api/", timeout=20)
        assert r.status_code == 200
        assert "Chronoglobe" in r.json().get("message", "")

    def test_events(self, s):
        r = s.get(f"{BASE_URL}/api/events", timeout=20)
        assert r.status_code == 200
        data = r.json()
        assert data["count"] >= 60
        assert isinstance(data["events"], list)
