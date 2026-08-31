from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app
from app.store import MemoryStore
from app.workflow import create_run, execute_run


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


def test_health_and_demo_page() -> None:
    client = TestClient(app)
    health = client.get("/healthz")
    page = client.get("/")

    assert health.json() == {"status": "ok", "service": "groundtruth"}
    assert page.status_code == 200
    assert "GroundTruth prevents" in page.text
    assert "Transparent synthetic scenario" in page.text
