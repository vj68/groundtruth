from __future__ import annotations

import json

import pytest

from app.assurance_store import MemoryAssuranceStore
from app.assurance_workflow import create_assurance_run, execute_assurance
from app.config import get_settings
from app.kubernetes_evidence import (
    WITHHELD_GROUND_TRUTH,
    allowed_evidence_packet,
    compare_with_withheld_ground_truth,
    discover_exposures,
    run_aliasing_reproducer,
)
from app.learning_ledger import LearningLedger


def test_blind_packet_excludes_the_historical_answer_key() -> None:
    packet = allowed_evidence_packet()
    serialized = json.dumps(packet)

    assert "29641" not in serialized
    assert "expected_paths" not in packet
    assert packet["issue"]["id"] == "kubernetes/kubernetes#29297"
    assert len(packet["source_snapshots"]) == 4


def test_trusted_scan_and_reproducer_match_historical_scope() -> None:
    packet = allowed_evidence_packet()
    findings = discover_exposures(packet)
    proof = run_aliasing_reproducer()
    comparison = compare_with_withheld_ground_truth(findings)

    assert [item["component"] for item in findings] == [
        "ConfigMap",
        "Secret",
        "Downward API",
        "GitRepo",
    ]
    assert proof["vulnerable"]["same_nested_object"] is True
    assert proof["vulnerable"]["a_after_interleave"] == "wrapped_config-b"
    assert proof["remediated"]["same_nested_object"] is False
    assert proof["remediated"]["a_after_interleave"] == "wrapped_config-a"
    assert comparison["exact_scope_match"] is True
    assert comparison["precision"] == 1.0
    assert comparison["recall"] == 1.0
    assert comparison["answer_key"]["id"] == WITHHELD_GROUND_TRUTH["id"]


def test_learning_ledger_is_append_only_and_hash_linked() -> None:
    ledger = LearningLedger()
    first = ledger.append("L-1", "HYPOTHESIS_RECORDED", "Agent", {"claim": "bounded"})
    second = ledger.append("L-1", "EVIDENCE_VERIFIED", "Evaluator", {"passed": True})

    assert first.previous_hash == "GENESIS"
    assert second.previous_hash == first.event_hash
    assert ledger.verify()["valid"] is True
    detached = ledger.list()
    detached[0].payload["claim"] = "tampered outside store"
    assert ledger.list()[0].payload["claim"] == "bounded"
    assert not hasattr(ledger, "save")
    assert not hasattr(ledger, "delete")


@pytest.mark.asyncio
async def test_blind_replay_produces_verified_organizational_learning(monkeypatch) -> None:
    monkeypatch.setenv("ENABLE_GEMINI", "false")
    monkeypatch.setenv("DEMO_DELAY_MS", "0")
    get_settings.cache_clear()
    store = MemoryAssuranceStore()
    run = create_assurance_run()
    store.create(run)

    await execute_assurance(run.id, store)

    complete = store.get(run.id)
    assert complete is not None
    assert complete.status == "complete"
    assert complete.mode == "grounded-local-fallback"
    assert len(complete.artifacts) == 5
    assert len(complete.exposures) == 4
    assert all(item.status == "EXPOSURE VERIFIED" for item in complete.exposures)
    assert [check.decision for check in complete.evaluations] == [
        "PASS",
        "FAIL AS EXPECTED",
        "PASS",
    ]
    assert complete.ground_truth is not None
    assert complete.ground_truth["exact_scope_match"] is True
    assert complete.ledger_verification is not None
    assert complete.ledger_verification["valid"] is True
    assert len(complete.ledger_events) == 4
    assert complete.memory_update is not None
    assert complete.memory_update["learning_id"] == "GT-K8S-0001"
    assert any(action["id"] == "NSTR-204" for action in complete.proactive_actions)
    assert complete.decision == "LESSON VERIFIED · FUTURE RECURRENCE BLOCKED"
    get_settings.cache_clear()
