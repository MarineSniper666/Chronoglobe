"""Tests for Chronoglobe Story Mode tours: /api/tours, /api/tours/{id}."""
import os
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://temporal-atlas-2.preview.emergentagent.com").rstrip("/")

EXPECTED_TOUR_IDS = {"wheel", "dyings", "silk-road", "moon", "discovery"}


@pytest.fixture(scope="module")
def s():
    sess = requests.Session()
    sess.headers.update({"Content-Type": "application/json"})
    return sess


class TestToursList:
    def test_list_returns_5_tours(self, s):
        r = s.get(f"{BASE_URL}/api/tours", timeout=20)
        assert r.status_code == 200
        data = r.json()
        assert "tours" in data
        tours = data["tours"]
        assert len(tours) == 5, f"expected 5 tours, got {len(tours)}"
        ids = {t["id"] for t in tours}
        assert ids == EXPECTED_TOUR_IDS, f"tour id mismatch: {ids}"

    def test_each_tour_has_required_fields(self, s):
        tours = s.get(f"{BASE_URL}/api/tours", timeout=20).json()["tours"]
        for t in tours:
            for k in ["id", "title", "subtitle", "description", "stops"]:
                assert k in t, f"{t.get('id')} missing {k}"
            assert isinstance(t["stops"], list) and len(t["stops"]) > 0
            assert isinstance(t["title"], str) and t["title"]
            assert isinstance(t["subtitle"], str) and t["subtitle"]
            assert isinstance(t["description"], str) and t["description"]


class TestSingleTour:
    @pytest.mark.parametrize("tid", sorted(EXPECTED_TOUR_IDS))
    def test_get_single_tour(self, s, tid):
        r = s.get(f"{BASE_URL}/api/tours/{tid}", timeout=20)
        assert r.status_code == 200
        data = r.json()
        assert data["id"] == tid
        assert isinstance(data["stops"], list) and len(data["stops"]) > 0

    def test_get_unknown_tour_returns_404(self, s):
        r = s.get(f"{BASE_URL}/api/tours/does-not-exist", timeout=20)
        assert r.status_code == 404


class TestTourStopsResolvable:
    def test_every_stop_resolves_to_real_event(self, s):
        tours = s.get(f"{BASE_URL}/api/tours", timeout=20).json()["tours"]
        events = s.get(f"{BASE_URL}/api/events", timeout=20).json()["events"]
        event_ids = {e["id"] for e in events}
        total = 0
        for t in tours:
            for eid in t["stops"]:
                total += 1
                assert eid in event_ids, f"tour {t['id']} stop {eid} not a real event"
        assert total == 27, f"expected 27 total stops across all tours, got {total}"

    def test_moon_tour_first_stop_is_watt_steam(self, s):
        r = s.get(f"{BASE_URL}/api/tours/moon", timeout=20).json()
        assert r["stops"][0] == "tech-steam"
        ev = s.get(f"{BASE_URL}/api/events/tech-steam", timeout=20).json()
        assert ev["year"] == 1769
