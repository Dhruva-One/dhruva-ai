from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    body = client.get("/health").json()
    assert body["status"] == "ok"
    assert body["provider"] == "fake"


def test_notice_draft_needs_approval():
    r = client.post("/v1/drafts/notice", json={
        "tenant_id": "t1", "audience": "Parents of Class 10", "facts": ["PTM on Saturday"],
    })
    assert r.status_code == 200
    assert r.json()["needs_approval"] is True


def test_rejects_unknown_language():
    r = client.post("/v1/drafts/notice", json={"tenant_id": "t1", "audience": "x", "facts": ["y"], "language": "fr"})
    assert r.status_code == 422
