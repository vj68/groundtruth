from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient
from flask import Request
from werkzeug.test import EnvironBuilder

from app.config import get_settings
from app.main import app
from app.store import MemoryStore
from app.workflow import create_run, execute_run
from main import groundtruth_web


@pytest.mark.asyncio
async def test_workflow_produces_verified_learning(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("ENABLE_GEMINI", "false")
    monkeypatch.setenv("DEMO_DELAY_MS", "0")
    monkeypatch.setenv("ARTIFACT_DIR", str(tmp_path))
    get_settings.cache_clear()
    store = MemoryStore()
    run = create_run()
    store.create(run)

    await execute_run(run.id, store)

    complete = store.get(run.id)
    assert complete is not None
    assert complete.status == "complete"
    assert complete.mode == "grounded-local-fallback"
    assert complete.learning is not None
    assert complete.learning.status == "verified"
    assert [result.decision for result in complete.evaluations] == [
        "BLOCK",
        "PASS",
        "BLOCK",
        "BLOCK",
        "PASS",
    ]
    artifact = tmp_path / run.id / "learning-record.json"
    assert json.loads(artifact.read_text())["status"] == "complete"
    get_settings.cache_clear()


def test_health_and_platform_shell() -> None:
    client = TestClient(app)
    health = client.get("/healthz")
    page = client.get("/")

    assert health.json() == {"status": "ok", "service": "groundtruth"}
    assert page.status_code == 200
    assert "Institutional learning control plane" in page.text
    assert "Assurance workspace" in page.text
    assert 'href="/static/platform.css"' in page.text
    assert 'src="/static/platform.js"' in page.text


def test_cloud_function_adapter_and_public_base_path(monkeypatch) -> None:
    monkeypatch.setenv("PUBLIC_BASE_PATH", "/groundtruth-web")
    request = Request(EnvironBuilder(path="/", method="GET").get_environ())

    response = groundtruth_web(request)
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'data-base-path="/groundtruth-web"' in page
    assert 'href="/groundtruth-web/static/platform.css"' in page
    assert 'src="/groundtruth-web/static/platform.js"' in page


def test_all_platform_pages_and_payload_are_available() -> None:
    client = TestClient(app)
    for path in [
        "/overview",
        "/changes",
        "/changes/K8S-29297",
        "/memory",
        "/incidents",
        "/capability",
        "/outcomes",
    ]:
        response = client.get(path)
        assert response.status_code == 200, path

    payload = client.get("/api/platform").json()
    assert payload["organization"]["name"] == "Northstar Engineering"
    assert payload["change_detail"]["issue"]["id"] == "kubernetes/kubernetes#29297"
    assert len(payload["change_detail"]["source_snapshots"]) == 4

    missing = client.get("/changes/UNKNOWN")
    assert missing.status_code == 404
