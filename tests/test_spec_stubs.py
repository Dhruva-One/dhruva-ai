import re

from fastapi.testclient import TestClient

from app.main import app
from app.spec_stubs import load_catalog

client = TestClient(app)


def test_every_catalog_endpoint_answers():
    missing = []
    for e in load_catalog():
        url = re.sub(r"\{\w+\}", "x1", e["p"])
        if client.request(e["m"], url).status_code in (404, 405):
            missing.append(f"{e['m']} {e['p']}")
    assert missing == []


def test_stub_names_its_requirements():
    body = client.post("/internal/v1/capabilities/timetable_generator").json()
    assert body["statusCode"] == 501
    assert "AI-TTG" in body["requirements"]


def test_every_endpoint_serves_a_requirement_module():
    assert all(e["req"] for e in load_catalog())
