"""Smoke tests for the browser GUI backend (`dev-gui` investigation).

These run only when the ``gui`` extra (FastAPI + a test client) is installed, so the
default suite is unaffected. They exercise the three endpoints end to end with the
deterministic (no-model) path, mirroring how the core library is tested.
"""

from __future__ import annotations

import pytest

# The GUI backend is optional; skip the whole module without the `gui` extra.
pytest.importorskip("fastapi")
starlette_testclient = pytest.importorskip("starlette.testclient")

from standpoint.api import app  # noqa: E402  (after importorskip by design)

client = starlette_testclient.TestClient(app)


def test_gui_page_served() -> None:
    """`GET /gui` returns the single-page HTML app."""
    r = client.get("/gui")
    assert r.status_code == 200
    assert "Standpoint" in r.text and "vega-embed" in r.text


def test_root_redirects_to_gui() -> None:
    """`GET /` redirects to the GUI page."""
    r = client.get("/", follow_redirects=False)
    assert r.status_code in (307, 308)
    assert r.headers["location"].endswith("/gui")


def test_example_endpoint_returns_csv() -> None:
    """`GET /api/example` returns a non-empty CSV starter table."""
    r = client.get("/api/example")
    assert r.status_code == 200
    assert r.text.splitlines()[0].startswith("Language,")


def test_position_roundtrip_deterministic() -> None:
    """`POST /api/position` returns a full, drawable result on a valid table."""
    table = "Language,Speed,Safety,Jobs\nPython,2,2,5\nRust,5,5,3\nGo,4,4,4\nJava,4,4,5"
    r = client.post("/api/position", json={"table": table, "reference": "0", "use_llm": False})
    assert r.status_code == 200
    data = r.json()
    assert data["reference"] == "Python"
    assert data["roles"]["Python"] == "best"
    assert data["vega"]["layer"]  # a real Vega-Lite spec the browser can render
    assert data["markdown"].startswith("# Python")
    assert "meta:" in data["yaml"]


def test_position_rejects_degenerate_table() -> None:
    """A table with too few options yields a clean 400, not a 500."""
    r = client.post("/api/position", json={"table": "A,B\nonly,1", "use_llm": False})
    assert r.status_code == 400
    assert "detail" in r.json()


def test_position_rejects_empty_table() -> None:
    """An empty table body is rejected with 400."""
    r = client.post("/api/position", json={"table": "   ", "use_llm": False})
    assert r.status_code == 400
